#!/usr/bin/env python3
"""Collect facts about an Android project for a Google Play review.

Facts only, never verdicts. Read-only: no network, no project code or Gradle is
run, nothing is written inside the project. Build files are parsed as text.

Example:
  python3 -B scripts/scan_android.py . --output /tmp/facts.json --pretty
  python3 -B scripts/scan_android.py . --section permissions sdk --artifact app-release.apk

Exit codes: 0 facts emitted, 2 bad arguments, 3 partial (see "errors").
Debug, test, androidTest and testFixtures source sets are skipped.
"""
import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

TOOL_VERSION = "1.2.0"
SECTIONS = ["project_kind", "modules", "sdk", "build", "permissions", "components",
            "dependencies", "native", "listing", "secrets"]
MAX_TEXT = 2 * 1024 * 1024          # per file
MAX_FILES = 20000
READ_BUDGET = 256 * 1024 * 1024     # total bytes read from the project
MAX_STR = 200
STDOUT_LIMIT = 20000
ZIP_MAX_ENTRIES = 20000
ZIP_MAX_BYTES = 2 * 1024 ** 3       # declared uncompressed total
SKIP_DIRS = {".git", "node_modules", ".gradle", ".idea", "Pods", ".dart_tool", ".expo", "__pycache__"}
SKIP_SOURCE_SETS = {"debug", "test", "androidTest", "testFixtures"}
NON_APP_MODULE = re.compile(r"(^|/|-)(demo|demos|sample|samples|example|examples|\w*benchmark\w*|baseline\w*|test\w*|screener)(/|-|$)", re.I)
BUILD_LOGIC_KT = re.compile(r"(^|/)(buildSrc|build-logic|build-plugin|convention\w*)/.*\.kt$")
MERGED_DIRS = ("merged_manifests", "merged_manifest", "packaged_manifests")
ANDROID = "{http://schemas.android.com/apk/res/android}"
TOOLS = "{http://schemas.android.com/tools}"
PERM_TAGS = {"uses-permission", "uses-permission-sdk-23", "uses-permission-sdk-m"}
REF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")
SECRET_TEXT_EXT = {".kt", ".java", ".xml", ".gradle", ".kts", ".properties", ".json", ".js", ".ts",
                   ".tsx", ".jsx", ".dart", ".yaml", ".yml", ".env", ".toml", ".txt", ".cfg"}
SECRET_PATTERNS = [  # (kind, regex): the match itself is never output beyond 4 characters
    ("google-api-key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("aws-access-key", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("secret-key-token", re.compile(r"\bsk-[A-Za-z0-9]{20,}")),
    ("github-token", re.compile(r"\bghp_[A-Za-z0-9]{36}")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
]
SIGNING_KEYS = re.compile(r"\b(storePassword|keyPassword)\b\s*[=:]?\s*[\"'][^\"'\s]+[\"']")
SECRET_FILES = re.compile(r"(^|/)(google-services\.json|GoogleService-Info\.plist|key\.properties|"
                          r"keystore\.properties|.*\.(jks|keystore|p12|pfx|pem)|\.env(\..*)?|"
                          r"service[-_]?account.*\.json)$", re.I)
KEYISH = re.compile(r"(key|secret|token|password)", re.I)


# ---------- small helpers ----------

def trunc(v):
    return v if not isinstance(v, str) or len(v) <= MAX_STR else v[:MAX_STR] + "..."


def fact(file, line, conf, **kw):
    out = {"file": trunc(file), "line": line, "confidence": conf}
    out.update({k: trunc(v) for k, v in sorted(kw.items()) if v is not None})
    return out


def ordered(items):
    return sorted(items, key=lambda d: (d.get("file") or d.get("path") or "", d.get("permission") or d.get("name") or "",
                                        d.get("line") or 0, json.dumps(d, sort_keys=True)))


def line_of(text, needle):
    i = text.find(needle) if isinstance(needle, str) else needle
    return text.count("\n", 0, i) + 1 if i is not None and i >= 0 else None


def norm(alias):
    return re.sub(r"[-_.]", ".", alias).lower()


def block(text, pattern, start=0):
    """Body of the first `pattern {...}` block (pattern ends at the opening brace)."""
    m = re.compile(pattern).search(text, start)
    if not m:
        return None
    depth, i = 0, m.end() - 1
    # shortcut: braces inside strings or comments are counted, fine for typical Gradle
    for j in range(i, len(text)):
        depth += (text[j] == "{") - (text[j] == "}")
        if depth == 0:
            return m.start(), text[i + 1:j]
    return m.start(), text[i + 1:]


def load_ref(ctx, name):
    try:
        with open(os.path.join(REF_DIR, name), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        ctx["errors"].append("references/%s not loaded (%s); related classes and categories are missing" % (name, e))
        return {}


def parse_xml(data):
    if re.search(rb"<!\s*(?:DOCTYPE|ENTITY)", data, re.I):
        raise ValueError("DOCTYPE or ENTITY declaration rejected (entity expansion risk)")
    return ET.fromstring(data)


# ---------- file access ----------

def escapes(ctx, path):
    real = os.path.realpath(path)
    return os.path.commonpath([ctx["real"], real]) != ctx["real"]


def read_bytes(ctx, rel):
    p = os.path.join(ctx["root"], rel)
    try:
        size = os.path.getsize(p)
        if size > MAX_TEXT:
            if rel.endswith((".txt", "verification-metadata.xml")):
                return None
            ctx["unknown"].append("%s is %d bytes, over the 2 MB read cap, so it was not read: inspect it by hand." % (rel, size))
            return None
        ctx["budget"] -= size
        if ctx["budget"] < 0:
            ctx["unknown"].append("The 256 MB total read budget ran out: later files were not read; scan a narrower PROJECT_DIR.")
            return None
        with open(p, "rb") as f:
            return f.read()
    except OSError as e:
        ctx["errors"].append("%s: cannot read (%s)" % (rel, e.strerror))
        return None


def read_text(ctx, rel):
    data = read_bytes(ctx, rel)
    return None if data is None else data.decode("utf-8", "replace")


def merged_in(root, build_rel):
    """Merged manifests under build/intermediates (Gradle) or build/<module>/intermediates (Flutter)."""
    base = os.path.join(root, build_rel)
    bases = [base] + [os.path.join(base, d) for d in sorted(os.listdir(base)) if os.path.isdir(os.path.join(base, d))]
    found = []
    for b in bases:
        for sub in MERGED_DIRS:
            for dp, _, fns in os.walk(os.path.join(b, "intermediates", sub)):
                found += [os.path.relpath(os.path.join(dp, f), root).replace(os.sep, "/")
                          for f in fns if f == "AndroidManifest.xml"]
    return sorted(found)[:20]


def walk(ctx):
    root, files, merged = ctx["root"], [], []
    for dp, dirs, fns in os.walk(root):
        keep = []
        for d in sorted(dirs):
            full = os.path.join(dp, d)
            if os.path.islink(full):
                if escapes(ctx, full):
                    ctx["unknown"].append("Symlinked directory %s points outside the project and was not followed: copy the real files in to scan them." % os.path.relpath(full, root))
            elif d == "build":
                merged += merged_in(root, os.path.relpath(full, root))
            elif d not in SKIP_DIRS:
                keep.append(d)
        dirs[:] = keep
        for f in sorted(fns):
            full = os.path.join(dp, f)
            if os.path.islink(full) and not os.path.exists(full):
                continue
            if os.path.islink(full) and escapes(ctx, full):
                ctx["unknown"].append("Symlink %s points outside the project and was not read: copy the real file in to scan it." % os.path.relpath(full, root))
                continue
            files.append(os.path.relpath(full, root).replace(os.sep, "/"))
            if len(files) >= MAX_FILES:
                ctx["unknown"].append("Stopped after 20000 files: scan a narrower PROJECT_DIR to cover the rest.")
                return files, merged
    return files, merged


# ---------- Gradle, catalogs, variables ----------

def parse_catalog(text):
    versions, libs, plugins, sec = {}, {}, {}, None
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        m = re.match(r"\[(\w+)\]", s)
        if m:
            sec = m.group(1)
            continue
        m = re.match(r"([\w.\-]+)\s*=\s*(.+)", s)
        if not m or sec not in ("versions", "libraries", "plugins"):
            continue
        key, val = m.groups()
        if sec == "versions":
            vm = re.match(r"[\"']([^\"']+)", val) or re.search(r"(?:require|strictly)\s*=\s*\"([^\"]+)", val)
            if vm:
                versions[key] = vm.group(1)
            continue
        g, a = re.search(r"group\s*=\s*\"([^\"]+)", val), re.search(r"name\s*=\s*\"([^\"]+)", val)
        mod = re.search(r"(?:module|id)\s*=\s*\"([^\"]+)", val) or re.match(r"\"([^\"]+)\"", val)
        coord = mod.group(1) if mod else ("%s:%s" % (g.group(1), a.group(1)) if g and a else None)
        if not coord:
            continue
        ref = re.search(r"version\.ref\s*=\s*\"([^\"]+)", val)
        lit = re.search(r"version\s*=\s*\"([^\"]+)", val)
        parts = coord.split(":")
        ver = versions.get(ref.group(1)) if ref else (lit.group(1) if lit else (parts[2] if len(parts) > 2 else None))
        (libs if sec == "libraries" else plugins)[norm(key)] = (":".join(parts[:2]) if sec == "libraries" else coord, ver, n)
    bundles = re.search(r"^\[bundles\](.*?)(?=^\[|\Z)", text, re.M | re.S)
    for key, members in re.findall(r"^([\w.\-]+)\s*=\s*\[(.*?)\]", bundles.group(1) if bundles else "", re.M | re.S):
        libs["bundle:" + norm(key)] = [norm(m) for m in re.findall(r"\"([^\"]+)\"", members)]
    return versions, libs, plugins


def find_var(ctx, name, value=r"(\d+)"):
    pat = re.compile(r"\b%s\b\s*[=:]\s*[\"']?%s" % (re.escape(name), value))
    for rel in sorted(ctx["gradle"]):
        m = pat.search(ctx["gradle"][rel])
        if m:
            return m.group(1), rel, line_of(ctx["gradle"][rel], m.start())
    return None


def resolve(ctx, expr, numeric=True):
    """Resolve a Gradle expression to a literal through version catalogs and ext/properties vars."""
    expr = re.sub(r"\.(toInt|toInteger|toString|get)\(\)", "", expr)
    m = re.search(r"libs\.versions\.([\w.]+)", expr)
    if m:
        key = norm(re.sub(r"(\.(get|toInt|toString|asProvider))+$", "", m.group(1)))
        for versions, _, _, _ in ctx["catalogs"]:
            if key in versions:
                return versions[key]
    names = re.findall(r"[A-Za-z_]\w*", expr)
    if names and names[-1] not in ("get", "toInt", "toString"):
        hit = find_var(ctx, names[-1], r"(\d+)" if numeric else r"([^\"'\s]+)")
        if hit:
            return hit[0]
    return None


def num_setting(ctx, rel, text, names):
    """First `name 34` / `name = 34` / `name = ext.expr` in a module file."""
    for name in names:
        m = re.search(r"\b%s\s*\{[^}]*?\brelease\(([^\n{]*)\)" % name, text)  # AGP 9 compileSdk { version = release(36) }
        if m:
            ln, rest = line_of(text, m.start()), m.group(1).strip()
            val = rest if rest.isdigit() else resolve(ctx, rest)
            if val is not None and str(val).isdigit():
                return fact(rel, ln, "declared" if rest.isdigit() else "resolved", value=int(val))
            return fact(rel, ln, "inferred", expr=rest)
        m = re.search(r"\b%s\b[ \t]*(?:=[ \t]*)?\(?[ \t]*([^\n;}]+)" % name, text)  # one-line blocks separate with ;
        if not m:
            continue
        rest = m.group(1).strip()
        ln = line_of(text, m.start())
        lit = re.match(r"(?:release\()?(\d+)\)?\s*(?://.*)?$", rest)
        if lit:
            return fact(rel, ln, "declared", value=int(lit.group(1)))
        val = resolve(ctx, rest)
        if val is not None and str(val).isdigit():
            return fact(rel, ln, "resolved", value=int(val), expr=rest)
        return fact(rel, ln, "inferred", expr=rest)
    return None


def first_version(ctx, patterns, catalog_keys=()):
    for rel in sorted(ctx["gradle"]):
        for p in patterns:
            m = re.search(p, ctx["gradle"][rel])
            if m:
                return fact(rel, line_of(ctx["gradle"][rel], m.start()), "declared", value=m.group(1))
    for versions, _, rel, plugins in ctx["catalogs"]:
        for k in catalog_keys:
            if k in versions:
                return fact(rel, None, "resolved", value=versions[k])
        for pid, ver, n in plugins.values():
            if pid in catalog_keys and ver:
                return fact(rel, n, "resolved", value=ver)
    return None


def do_gradle(ctx, out):
    modules, sdk = [], {k: [] for k in ("targetSdk", "compileSdk", "minSdk", "agp", "gradleWrapper", "kotlin", "ndk")}
    build = {"gradle": [], "manifest": []}
    for rel in sorted(ctx["gradle"]):
        text = ctx["gradle"][rel]
        if not re.search(r"(^|/)build\.gradle(\.kts)?$", rel) or not re.search(r"\bandroid\s*\{", text):
            continue
        app = re.search(r"com\.android\.application|android\.application|androidApplication|\bapplicationId\b", text)
        mod = {"path": os.path.dirname(rel) or ".", "type": "application" if app else "library"}
        for key, pat in (("applicationId", r"\bapplicationId\b\s*=?\s*[\"']([^\"']+)"), ("namespace", r"\bnamespace\b\s*=?\s*[\"']([^\"']+)"),
                         ("versionCode", r"\bversionCode\b\s*=?\s*(\d+)"), ("versionName", r"\bversionName\b\s*=?\s*[\"']([^\"']+)")):
            m = re.search(pat, text)
            if m:
                mod[key] = int(m.group(1)) if key == "versionCode" else m.group(1)
        pf = block(text, r"\bproductFlavors\s*\{")
        # shortcut: nested blocks inside productFlavors (ndk, etc.) are listed too
        mod["flavors"] = sorted(set(re.findall(r"^\s*(?:create\(|register\(|maybeCreate\()?[\"']?(\w+)[\"']?\)?\s*\{", pf[1], re.M))) if pf else []
        modules.append(dict(sorted(mod.items())))
        for key, names in (("targetSdk", ("targetSdk", "targetSdkVersion")), ("minSdk", ("minSdk", "minSdkVersion")),
                           ("compileSdk", ("compileSdk", "compileSdkVersion"))):
            f = num_setting(ctx, rel, text, names)
            if f:
                sdk[key].append(f)
        bt = block(text, r"\bbuildTypes\s*\{")
        for name in ("release", "debug"):
            sub = block(bt[1], r"(?:getByName\(|named\(|create\()?[\"']?%s[\"']?\)?\s*\{" % name) if bt else None
            if not sub:
                continue
            body, ln = sub[1], line_of(text, text.find("{", bt[0]) + 1 + sub[0])
            items = {}
            m = re.search(r"\b(?:isMinifyEnabled|minifyEnabled)\b\s*=?\s*(true|false)", body)
            if m:
                items["minify"] = m.group(1) == "true"
            m = re.search(r"\b(?:isDebuggable|debuggable)\b\s*=?\s*(true|false)", body)
            if m:
                items["debuggable"] = m.group(1) == "true"
            items["signingConfig"] = bool(re.search(r"\bsigningConfig\b", body))
            build["gradle"].append(fact(rel, ln, "declared", build_type=name, **items))
        m = re.search(r"\buseLegacyPackaging\b\s*=?\s*(true|false)", text)
        if m:
            build["gradle"].append(fact(rel, line_of(text, m.start()), "declared", useLegacyPackaging=m.group(1) == "true"))
    for rel in sorted(ctx["gradle"]):  # common.gradle and convention plugins hold values for many modules
        if re.search(r"\.gradle(\.kts)?$", rel) and not re.search(r"(^|/)(build|settings)\.gradle(\.kts)?$", rel):
            for key, names in (("targetSdk", ("targetSdk", "targetSdkVersion")), ("minSdk", ("minSdk", "minSdkVersion")),
                               ("compileSdk", ("compileSdk", "compileSdkVersion"))):
                f = num_setting(ctx, rel, ctx["gradle"][rel], names)
                if f:
                    sdk[key].append(f)
    for rel in sorted(ctx["gradle"]):
        text = ctx["gradle"][rel]
        ndk = re.search(r"\bndkVersion\b\s*=?\s*([^\n]+)", text) if re.search(r"\.gradle(\.kts)?$", rel) else None
        if ndk:
            expr = ndk.group(1).strip()
            lit = re.match(r"[\"']([^\"'$]+)", expr)
            val = lit.group(1) if lit else (None if "$" in expr else resolve(ctx, expr, numeric=False))
            if val and val[0].isdigit():
                sdk["ndk"].append(fact(rel, line_of(text, ndk.start()), "declared" if lit else "resolved", value=val))
            else:
                sdk["ndk"].append(fact(rel, line_of(text, ndk.start()), "inferred", expr=expr))
    ag = first_version(ctx, [r"com\.android\.tools\.build:gradle:([\d][\w.\-]*)",
                             r"com\.android\.(?:application|library)[\"']\)?\s+version\s+[\"']([^\"']+)"],
                       ("agp", "com.android.application"))
    kt = first_version(ctx, [r"kotlin_?[vV]ersion\s*=\s*[\"']([^\"']+)", r"kotlin-gradle-plugin:([\d][\w.\-]*)",
                             r"org\.jetbrains\.kotlin\.android[\"']\)?\s+version\s+[\"']([^\"']+)",
                             r"kotlin\(\"android\"\)\s+version\s+\"([^\"]+)"],
                       ("kotlin", "org.jetbrains.kotlin.android"))
    for key, f in (("agp", ag), ("kotlin", kt)):
        if f:
            sdk[key].append(f)
    for rel in sorted(ctx["gradle"]):
        m = re.search(r"distributionUrl=.*gradle-([\d][\w.\-]*?)-(?:bin|all)\.zip", ctx["gradle"][rel])
        if m and rel.endswith("gradle-wrapper.properties"):
            sdk["gradleWrapper"].append(fact(rel, line_of(ctx["gradle"][rel], m.start()), "declared", value=m.group(1)))
    out["modules"] = ordered(modules)
    out["sdk"] = {k: ordered(v) for k, v in sdk.items()}
    out["build"] = build


def app_sdk(ctx, out):
    """Pick the values for the app people install, so a demo or library module cannot stand in for it."""
    paths = {m["path"]: m["type"] for m in out["modules"]}

    def rank(f):
        path = os.path.dirname(f["file"]) or "."
        if f.get("source") == "expo-build-properties":
            return 0
        if path not in paths:
            return 1
        if NON_APP_MODULE.search(path):
            return 4
        if re.search(r"wear|tv|automotive|car", path, re.I):
            return 2
        return 0 if paths[path] == "application" else 3

    picks = {}
    for key in ("targetSdk", "compileSdk", "minSdk"):
        facts = sorted(out["sdk"].get(key, []), key=lambda f: (rank(f), f["file"]))
        if facts:
            picks[key] = dict(facts[0], scope=("app", "shared build script", "other form factor", "library", "demo or test")[rank(facts[0])])
    out["sdk"]["app"] = dict(sorted(picks.items()))
    if "value" not in picks.get("targetSdk", {}):
        ctx["unknown"].append("The main app's targetSdk could not be read as a number: confirm it in Play Console's App bundle explorer or a release build before judging the target API requirement.")


# ---------- manifests ----------

def class_of(perms, name):
    e = perms.get(name)
    if e:
        return e["class"], e["alternative"]
    for k, v in perms.items():
        if k.endswith(".*") and name.startswith(k[:-1]):
            return v["class"], v["alternative"]
    if name.startswith("android.permission.FOREGROUND_SERVICE_"):
        return "foreground-service", perms.get("android.permission.FOREGROUND_SERVICE", {}).get("alternative")
    return None, None


def perm_fact(ctx, name, source, rel, line, conf, **kw):
    cls, alt = class_of(ctx["perms"], name)
    return fact(rel, line, conf, permission=name, source=source, **{"class": cls, "alternative": alt}, **kw)


def do_manifest(ctx, out, rel, source, data=None):
    data = data if data is not None else read_bytes(ctx, rel)
    if data is None:
        return
    try:
        root = parse_xml(data)
    except Exception as e:  # ParseError, ValueError
        ctx["errors"].append("%s: not parsed (%s)" % (rel, e))
        return
    text = data.decode("utf-8", "replace")
    conf = "resolved" if source != "manifest" else "declared"
    where = re.match(r"(?:(.+)/)?src/([^/]+)/", rel)
    place = {"module": where.group(1) or ".", "source_set": where.group(2)} if where else {}
    for el in root.iter():
        name = el.get(ANDROID + "name")
        if el.tag in PERM_TAGS and name:
            out["permissions"].append(perm_fact(
                ctx, name, source, rel, line_of(text, name), conf, maxSdkVersion=el.get(ANDROID + "maxSdkVersion"),
                removed=True if (el.get(TOOLS + "node") or "").startswith("remove") else None, **place))
        elif el.tag == "application":
            for k in ("allowBackup", "usesCleartextTraffic", "debuggable", "extractNativeLibs", "networkSecurityConfig"):
                if el.get(ANDROID + k) is not None:
                    out["build"]["manifest"].append(fact(rel, line_of(text, k), conf, attribute=k, value=el.get(ANDROID + k), source=source))
        elif el.tag in ("service", "activity", "activity-alias", "receiver", "provider"):
            exported = el.get(ANDROID + "exported")
            if el.tag != "service" and exported != "true":
                continue
            actions = sorted({a.get(ANDROID + "name") for a in el.iter("action") if a.get(ANDROID + "name")})[:10]
            out["components"].append(fact(
                rel, line_of(text, name) if name else None, conf, kind=el.tag, name=name, exported=exported,
                permission=el.get(ANDROID + "permission"), foregroundServiceType=el.get(ANDROID + "foregroundServiceType"),
                actions=actions or None, source=source))
        elif el.tag == "meta-data" and name and KEYISH.search(name):
            out["secrets"].append(fact(rel, line_of(text, name), conf, kind="manifest-meta-data", key=name))


def do_manifests(ctx, out, files, merged):
    for rel in files:
        parts = rel.split("/")
        if parts[-1] != "AndroidManifest.xml":
            continue
        i = parts.index("src") if "src" in parts else -1
        if i >= 0 and len(parts) > i + 1 and parts[i + 1] in SKIP_SOURCE_SETS:
            continue
        do_manifest(ctx, out, rel, "manifest")
    for rel in merged:
        do_manifest(ctx, out, rel, "merged")
    removed = {}
    for f in out["permissions"]:
        if f.get("removed") and f.get("source_set"):
            removed.setdefault((f["module"], f["permission"]), []).append(f["source_set"])
    for f in out["permissions"]:  # a flavor can strip what main declares
        hit = removed.get((f.get("module"), f["permission"]))
        if hit and not f.get("removed"):
            f["removed_in"] = sorted(hit)


# ---------- dependencies ----------

def categorize(sigs, name):
    for cat, prefixes in sigs.get("categories", {}).items():
        if any(name.startswith(p) for p in prefixes):
            return cat
    return None


def do_dependencies(ctx, out, files):
    seen = {}   # (ecosystem, name) -> (version, file, line, confidence)
    counts = {"gradle": 0, "npm": 0, "pub": 0}

    def put(eco, name, ver, rel, line, conf):
        counts[eco] += 1
        key = (eco, name, rel)
        if key not in seen or conf == "resolved":
            seen[key] = (ver, line, conf)

    def catalog_put(accessor, rel, n):
        if accessor.startswith(("versions", "plugins")):
            return
        name = re.sub(r"\.(get|asProvider)$", "", accessor)
        for _, libs, _, _ in ctx["catalogs"]:
            keys = libs.get("bundle:" + norm(name[8:]), []) if name.startswith("bundles.") else [norm(name)]
            for key in keys:
                if key in libs:
                    put("gradle", libs[key][0], libs[key][1], rel, n, "resolved")

    conf_re = re.compile(r"^\s*(\w+)\s*\(?\s*(.*)$")
    for rel in sorted(ctx["gradle"]):
        text = ctx["gradle"][rel]
        if rel.endswith("lockfile"):
            for n, line in enumerate(text.splitlines(), 1):
                m = re.match(r"([\w.\-]+:[\w.\-]+):([^=\s]+)=", line)
                if m:
                    put("gradle", m.group(1), m.group(2), rel, n, "resolved")
            continue
        if not re.search(r"\.gradle(\.kts)?$", rel):
            continue
        # one-line blocks: dependencies { implementation("a:b:1") }
        statements = [(n, s) for n, line in enumerate(text.splitlines(), 1) for s in re.split(r"[{;]", line)]
        for n, line in statements:
            added = re.match(r"\s*add\(\s*([^,]+),\s*libs\.([\w.]+)", line)
            if added and "test" not in added.group(1).lower():
                catalog_put(added.group(2), rel, n)
            m = conf_re.match(line)
            if not m or not re.fullmatch(r"(?:\w+)?(?:[Ii]mplementation|[Aa]pi|[Cc]ompileOnly|[Rr]untimeOnly)|classpath|kapt|ksp", m.group(1)) \
                    or m.group(1).startswith(("test", "androidTest")):
                continue
            rest = m.group(2)
            lit = re.search(r"[\"']([\w.\-]+:[\w.\-]+)(?::([^\"'\s]+))?[\"']", rest)
            if lit:
                ver, conf = lit.group(2), "declared"
                var = re.fullmatch(r"\$\{?(\w+)\}?", ver or "")
                if var:
                    ver = resolve(ctx, var.group(1), numeric=False)
                    conf = "resolved" if ver else "inferred"
                put("gradle", lit.group(1), ver, rel, n, conf)
                continue
            acc = re.search(r"\blibs\.([\w.]+)", rest)
            if acc:
                catalog_put(acc.group(1), rel, n)
    for rel in files:
        base = rel.rsplit("/", 1)[-1]
        if base == "pubspec.yaml":
            text, sec = read_text(ctx, rel), None
            for n, line in enumerate((text or "").splitlines(), 1):
                if re.match(r"\S", line):
                    sec = line.rstrip(":").strip() if line.rstrip().endswith(":") else None
                m = re.match(r"  ([\w\-]+):\s*(.*)$", line)
                if m and sec == "dependencies" and m.group(1) != "flutter":
                    v = m.group(2).strip().strip("\"'")
                    put("pub", m.group(1), v if re.match(r"[\^<>=\d]", v) else None, rel, n, "declared")
        elif base == "pubspec.lock":
            text = read_text(ctx, rel) or ""
            for m in re.finditer(r"^  ([\w\-]+):\n(?:    .*\n)*?    version: \"([^\"]+)\"", text, re.M):
                put("pub", m.group(1), m.group(2), rel, line_of(text, m.start()), "resolved")
        elif base == "package.json" and "node_modules" not in rel:
            text = read_text(ctx, rel)
            try:
                pkg = json.loads(text or "{}")
            except ValueError as e:
                ctx["errors"].append("%s: invalid JSON (%s)" % (rel, e))
                continue
            for sec in ("dependencies", "optionalDependencies"):
                for name, ver in sorted((pkg.get(sec) or {}).items()):
                    put("npm", name, ver if isinstance(ver, str) else None, rel, line_of(text, '"%s"' % name), "declared")
        elif base == "package-lock.json":
            try:
                lock = json.loads(read_text(ctx, rel) or "{}")
            except ValueError as e:
                ctx["errors"].append("%s: invalid JSON (%s)" % (rel, e))
                continue
            for path, info in sorted((lock.get("packages") or {}).items()):
                if path.startswith("node_modules/") and isinstance(info, dict):
                    put("npm", path[len("node_modules/"):].split("node_modules/")[-1], info.get("version"), rel, None, "resolved")
    items = []
    for (eco, name, rel), (ver, line, conf) in seen.items():
        cat = categorize(ctx["sigs"], name)
        if cat:
            items.append(fact(rel, line, conf, category=cat, ecosystem=eco, name=name, version=ver))
    out["dependencies"] = {"counts": counts, "items": ordered(items),
                           "note": "items lists only dependencies matching references/sdk-signatures.json"}
    if not any(r.endswith("lockfile") or r == "pubspec.lock" or r == "package-lock.json" for r in files):
        ctx["unknown"].append("Transitive dependencies are not visible without a lockfile: generate one (./gradlew dependencies --write-locks, flutter pub get, npm install) or pass a built --artifact.")


# ---------- project kind, Expo, Flutter ----------

def do_kind(ctx, out, files):
    kinds, markers = [], []

    def mark(kind, rel):
        if kind not in kinds:
            kinds.append(kind)
        markers.append(rel)

    pkg_deps, app_json = {}, None
    for rel in files:
        base, depth = rel.rsplit("/", 1)[-1], rel.count("/")
        if base == "package.json" and depth <= 1:
            try:
                pkg = json.loads(read_text(ctx, rel) or "{}")
                pkg_deps.update(pkg.get("dependencies") or {})
                pkg_deps.update(pkg.get("devDependencies") or {})
                markers.append(rel)
            except ValueError:
                pass
        elif base == "app.json" and depth <= 1:
            app_json = rel
        elif base == "pubspec.yaml" and depth <= 1:
            mark("flutter", rel)
        elif re.match(r"app\.config\.(js|ts|cjs|mjs|json)$", base) and depth <= 1:
            mark("expo", rel)
        elif base == "eas.json" and depth <= 1:
            mark("expo", rel)
        elif re.match(r"capacitor\.config\.", base):
            mark("capacitor", rel)
        elif base == "ProjectVersion.txt" and "ProjectSettings" in rel:
            mark("unity", rel)
        elif base in ("build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"):
            if re.search(r"multiplatform", ctx["gradle"].get(rel, "")):
                mark("kmp", rel)
            if base.startswith("build") and re.search(r"\bandroid\s*\{", ctx["gradle"].get(rel, "")):
                mark("native-gradle", rel)
    expo_cfg = None
    if app_json:
        try:
            expo_cfg = json.loads(read_text(ctx, app_json) or "{}").get("expo")
        except ValueError as e:
            ctx["errors"].append("%s: invalid JSON (%s)" % (app_json, e))
    if "expo" in pkg_deps or expo_cfg is not None:
        mark("expo", app_json or "package.json")
    if "react-native" in pkg_deps:
        mark("react-native", "package.json")
    if "cordova-android" in pkg_deps:
        mark("cordova", "package.json")
    order = ["expo", "react-native", "flutter", "capacitor", "cordova", "unity", "kmp", "native-gradle"]
    kinds = sorted(set(kinds), key=order.index)
    out["project_kind"] = {"primary": kinds[0] if kinds else "unknown", "all": kinds, "markers": sorted(set(markers))[:20], "markerCount": len(set(markers))}
    if not kinds:
        ctx["unknown"].append("No Android project markers (Gradle android block, pubspec.yaml, package.json, app.json) were found under PROJECT_DIR: point the scan at the project root.")
    has_android_dir = any(f.startswith("android/") or "/android/" in f for f in files)
    if "flutter" in kinds:
        do_flutter(ctx, out, files)
    if "expo" in kinds:
        do_expo(ctx, out, files, app_json, expo_cfg, has_android_dir)
        if pkg_deps.get("expo"):
            out["project_kind"]["expo"]["expoPackage"] = trunc(pkg_deps["expo"])
        if not out["sdk"]["targetSdk"]:
            ctx["unknown"].append("Expo sets the default target API from its SDK version and no override was found: confirm the targetSdk of a release build against the current requirement.")
    return kinds


def do_flutter(ctx, out, files):
    for rel in files:
        if rel == "pubspec.yaml":
            text = read_text(ctx, rel) or ""
            info = {}
            for key, pat in (("version", r"^version:\s*(\S+)"), ("flutterConstraint", r"^\s+flutter:\s*[\"']?([><=^][^\"'\n]*)"),
                             ("dartConstraint", r"^\s+sdk:\s*[\"']?([><=^][^\"'\n]*)")):
                m = re.search(pat, text, re.M)
                if m:
                    info[key] = m.group(1).strip()
            out["project_kind"]["flutter"] = dict(sorted(info.items()))
            ctx["unknown"].append("Flutter plugin permissions and the SDK-provided targetSdk/minSdk (flutter.targetSdkVersion) are not visible in source: build the release (flutter build appbundle) and scan build/ or pass --artifact.")


def do_expo(ctx, out, files, app_json, cfg, has_android_dir):
    info = {}
    if isinstance(cfg, dict):
        android = cfg.get("android") or {}
        text = read_text(ctx, app_json) or ""
        plugins = []
        for p in cfg.get("plugins") or []:
            name = p[0] if isinstance(p, list) and p else p
            if isinstance(name, str):
                plugins.append(trunc(name))
            if name == "expo-build-properties" and isinstance(p, list) and len(p) > 1 and isinstance(p[1], dict):
                for key, src in (("targetSdk", "targetSdkVersion"), ("compileSdk", "compileSdkVersion"), ("minSdk", "minSdkVersion")):
                    v = (p[1].get("android") or {}).get(src)
                    if isinstance(v, int):
                        out["sdk"][key].append(fact(app_json, line_of(text, src), "declared", value=v, source="expo-build-properties"))
        info["plugins"] = sorted(set(plugins))
        for key, flag in (("permissions", {}), ("blockedPermissions", {"blocked": True})):
            for perm in android.get(key) or []:
                if isinstance(perm, str):
                    name = perm if "." in perm else "android.permission." + perm
                    out["permissions"].append(perm_fact(ctx, name, "expo-config", app_json, line_of(text, '"%s"' % perm), "declared", **flag))
        for k in ("package", "versionCode"):
            if k in android:
                info[k] = android[k]
        info["sdkVersion"] = cfg.get("sdkVersion")
        info = {k: v for k, v in info.items() if v is not None}
    for rel in files:
        if re.match(r"app\.config\.(js|ts|cjs|mjs)$", rel):
            text = read_text(ctx, rel) or ""
            for key, src in (("targetSdk", "targetSdkVersion"), ("compileSdk", "compileSdkVersion"), ("minSdk", "minSdkVersion")):
                m = re.search(r"\b%s\s*:\s*(\d+)" % src, text)
                if m:
                    out["sdk"][key].append(fact(rel, line_of(text, m.start()), "inferred", value=int(m.group(1)), source="expo-build-properties"))
            for key, flag in (("permissions", {}), ("blockedPermissions", {"blocked": True})):
                for m in re.finditer(r"(?<![A-Za-z])%s\s*:\s*\[(.*?)\]" % key, text, re.S):
                    for perm in re.findall(r"[\"']([\w.]+)[\"']", m.group(1)):
                        name = perm if "." in perm else "android.permission." + perm
                        out["permissions"].append(perm_fact(ctx, name, "expo-config", rel, line_of(text, m.start()), "inferred", **flag))
            ctx["unknown"].append("%s is JavaScript and was matched as text only (low confidence): have the owner print the evaluated config (npx expo config --type public) and re-check permissions and plugins." % rel)
    out["project_kind"]["expo"] = info
    ctx["unknown"].append("Expo library permissions (for example expo-video, expo-audio, expo-contacts, expo-location, media libraries) are added at build time and are invisible in app.json: inspect the merged manifest of the release build or pass --artifact.")
    if not has_android_dir:
        ctx["unknown"].append("Expo managed project with no android/ directory: the real manifest and Gradle values are generated by prebuild, which this scanner does not run. Run prebuild in a scratch copy or inspect a built artifact.")


# ---------- native libraries ----------

def elf_align(data):
    """(min, max) p_align over PT_LOAD of a little-endian ELF64, or an error string."""
    if len(data) < 64 or data[:4] != b"\x7fELF":
        return "not an ELF file"
    if data[4] != 2 or data[5] != 1:
        return "not a little-endian ELF64 file"
    phoff, = struct.unpack_from("<Q", data, 0x20)
    phentsize, phnum = struct.unpack_from("<HH", data, 0x36)
    aligns = []
    for i in range(phnum):
        off = phoff + i * phentsize
        if off + 56 > len(data):
            return "program headers beyond the first 64 KB read"
        p_type, = struct.unpack_from("<I", data, off)
        if p_type == 1:
            aligns.append(struct.unpack_from("<Q", data, off + 48)[0])
    return (min(aligns), max(aligns)) if aligns else "no PT_LOAD segment"


def lib_fact(file, source, conf, abi, data, **kw):
    res = elf_align(data)
    if isinstance(res, str):
        return fact(file, None, conf, abi=abi, source=source, error=res, **kw)
    return fact(file, None, conf, abi=abi, source=source, p_align_min=res[0], p_align_max=res[1],
                compatible_16kb=res[0] >= 0x4000, **kw)


def do_native(ctx, out, files):
    libs, build_files = [], []
    for rel in files:
        parts = rel.split("/")
        if rel.endswith(".so") and len(parts) > 1 and parts[-2] in ("arm64-v8a", "x86_64"):
            try:
                with open(os.path.join(ctx["root"], rel), "rb") as f:
                    libs.append(lib_fact(rel, "source-tree", "inferred", parts[-2], f.read(65536)))
            except OSError as e:
                ctx["errors"].append("%s: cannot read (%s)" % (rel, e.strerror))
        elif parts[-1] in ("CMakeLists.txt", "Android.mk", "Application.mk"):
            text = read_text(ctx, rel) or ""
            build_files.append(fact(rel, None, "declared", flag_max_page_size_16384="max-page-size=16384" in text,
                                    flag_flexible_page_sizes="ANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES" in text))
    out["native"] = {"libraries": ordered(libs), "buildFiles": ordered(build_files), "artifact": None}
    if not ctx["artifact"]:
        ctx["unknown"].append("Native libraries pulled in by Gradle, pub or npm dependencies, and their 16 KB ELF alignment, are not in the source tree: build the release and pass --artifact app.apk.")


def read_libs(out, zf, raw, entries, kind):
    for e in sorted(entries, key=lambda e: e.filename):
        parts = e.filename.split("/")
        if not e.filename.endswith(".so") or len(parts) < 3 or parts[-2] not in ("arm64-v8a", "x86_64"):
            continue
        extra = {}
        if kind == "apk":  # an uncompressed .so must start on a 16 KB boundary inside the zip
            if e.compress_type == zipfile.ZIP_STORED:
                raw.seek(e.header_offset + 26)
                n, m = struct.unpack("<HH", raw.read(4))
                extra["zip_aligned_16kb"] = (e.header_offset + 30 + n + m) % 16384 == 0
            else:
                extra["zip_compressed"] = True
        with zf.open(e) as f:
            out["native"]["libraries"].append(lib_fact(e.filename, "artifact", "resolved", parts[-2], f.read(65536), **extra))


def do_artifact(ctx, out, path):
    name, kind = os.path.basename(path), path.lower().rsplit(".", 1)[-1]
    info = {"name": name, "kind": kind}
    out["native"]["artifact"] = info
    try:
        zf = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError) as e:
        ctx["errors"].append("%s: cannot open as zip (%s)" % (name, e))
        return
    with zf:
        entries = zf.infolist()
        total = sum(e.file_size for e in entries)
        info.update(entries=len(entries), uncompressed_bytes=total)
        if len(entries) > ZIP_MAX_ENTRIES or total > ZIP_MAX_BYTES:
            ctx["errors"].append("%s: refused (more than %d entries or %d declared uncompressed bytes, possible zip bomb)" % (name, ZIP_MAX_ENTRIES, ZIP_MAX_BYTES))
            return
        with open(path, "rb") as raw:
            read_libs(out, zf, raw, entries, kind)
        out["native"]["libraries"] = ordered(out["native"]["libraries"])
        if kind == "aab":
            ctx["unknown"].append("BundleConfig.pb and the AAB manifest are protobuf: run bundletool dump config --bundle=%s and look for PAGE_ALIGNMENT_16K, and bundletool dump manifest for permissions." % name)
            return
        try:
            data = zf.read("AndroidManifest.xml") if zf.getinfo("AndroidManifest.xml").file_size <= MAX_TEXT else None
        except KeyError:
            data = None
        if data is None:
            ctx["unknown"].append("%s has no readable AndroidManifest.xml: permissions of the artifact are unknown." % name)
        elif data.lstrip(b"\xef\xbb\xbf").startswith(b"<"):
            do_manifest(ctx, out, name + "!AndroidManifest.xml", "artifact", data)
        elif shutil.which("aapt2"):
            do_aapt2(ctx, out, path, name)
        else:
            ctx["unknown"].append("%s has a binary manifest (AXML) and aapt2 is not on PATH, so its permissions are unknown: install Android SDK build-tools and re-run, or run aapt2 dump permissions." % name)


def do_aapt2(ctx, out, path, name):
    try:
        r = subprocess.run(["aapt2", "dump", "permissions", path], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as e:
        ctx["errors"].append("aapt2 dump permissions failed (%s)" % e)
        return
    if r.returncode != 0:
        ctx["errors"].append("aapt2 dump permissions exited %d" % r.returncode)
        return
    for m in re.finditer(r"^uses-permission(?:-sdk-23)?: name='([^']+)'(?: maxSdkVersion='(\d+)')?", r.stdout, re.M):
        out["permissions"].append(perm_fact(ctx, m.group(1), "artifact", name, None, "resolved", maxSdkVersion=m.group(2)))


# ---------- listing and secrets ----------

def do_listing(ctx, out, files):
    locales, dirs, policy, login = {}, set(), [], []
    for rel in files:
        m = re.match(r"(.*fastlane/metadata/android/([^/]+))/(.+)$", rel)
        if m:
            loc = locales.setdefault(m.group(2), {})
            leaf = m.group(3)
            if leaf in ("title.txt", "short_description.txt", "full_description.txt"):
                loc[leaf[:-4] + "_chars"] = len((read_text(ctx, rel) or "").strip())
            elif leaf.startswith("images/"):
                loc["image_files"] = loc.get("image_files", 0) + 1
        if rel.split("/")[0] in ("play_store_assets", "store_assets", "playstore"):
            dirs.add(rel.split("/")[0])
        base = rel.rsplit("/", 1)[-1]
        k = re.search(r"privacy|terms|eula|delete[-_ ]?account|account[-_ ]?deletion|data[-_ ]?deletion", base, re.I)
        if k and not rel.endswith((".kt", ".java", ".dart")):
            policy.append(fact(rel, None, "inferred", match=k.group(0).lower()))
        if re.search(r"(login|signin|sign_in|signup|sign_up|auth)\w*\.(kt|java|dart|tsx|jsx|js|ts)$", base, re.I):
            login.append(fact(rel, None, "inferred"))
    out["listing"] = {"fastlane": {k: dict(sorted(v.items())) for k, v in sorted(locales.items())},
                      "storeAssetDirs": sorted(dirs), "policyLikeFiles": ordered(policy), "loginLikeFiles": ordered(login)[:30]}


def do_secrets(ctx, out, files):
    for rel in files:
        if SECRET_FILES.search(rel):
            out["secrets"].append(fact(rel, None, "declared", kind="secret-bearing-file"))
        base, ext = rel.rsplit("/", 1)[-1], os.path.splitext(rel)[1].lower()
        text = None
        if ext in SECRET_TEXT_EXT or base.startswith(".env") or base.endswith(".properties"):
            text = read_text(ctx, rel)
        if not text:
            continue
        if base.startswith(".env") or base.endswith(".properties"):
            for n, line in enumerate(text.splitlines(), 1):
                m = re.match(r"\s*([\w.\-]+)\s*[=:]\s*\S", line)
                if m and KEYISH.search(m.group(1)) and not line.lstrip().startswith("#"):
                    out["secrets"].append(fact(rel, n, "declared", kind="key-with-value", key=m.group(1)))
        for kind, pat in SECRET_PATTERNS:
            for m in pat.finditer(text):
                out["secrets"].append(fact(rel, line_of(text, m.start()), "declared", kind=kind, masked=m.group(0)[:4] + "..."))
        for m in SIGNING_KEYS.finditer(text):
            out["secrets"].append(fact(rel, line_of(text, m.start()), "declared", kind="hardcoded-signing-password", key=m.group(1)))


# ---------- assembly ----------

def scan(root, artifact):
    ctx = {"root": root, "real": os.path.realpath(root), "unknown": [], "errors": [], "budget": READ_BUDGET,
           "artifact": artifact, "gradle": {}, "catalogs": []}
    ctx["perms"] = load_ref(ctx, "permissions.json").get("permissions", {})
    ctx["sigs"] = load_ref(ctx, "sdk-signatures.json")
    files, merged = walk(ctx)
    for rel in files:
        base = rel.rsplit("/", 1)[-1]
        if re.search(r"\.gradle(\.kts)?$|^gradle\.properties$|^gradle-wrapper\.properties$|\.lockfile$|\.versions\.toml$", base) or BUILD_LOGIC_KT.search(rel):
            text = read_text(ctx, rel)
            if text is not None:
                ctx["gradle"][rel] = text
                if base.endswith(".versions.toml"):
                    v, l, p = parse_catalog(text)
                    ctx["catalogs"].append((v, l, rel, p))
    # catalog versions keyed by raw name; lookups in resolve() normalise them
    ctx["catalogs"] = [({norm(k): x for k, x in v.items()}, l, rel, p) for v, l, rel, p in ctx["catalogs"]]
    out = {"tool_version": TOOL_VERSION, "project_kind": None, "modules": [], "sdk": {}, "build": {},
           "permissions": [], "components": [], "dependencies": {}, "native": {}, "listing": {},
           "secrets": [], "unknown": [], "errors": []}
    do_gradle(ctx, out)
    do_kind(ctx, out, files)
    app_sdk(ctx, out)
    do_manifests(ctx, out, files, merged)
    do_dependencies(ctx, out, files)
    do_native(ctx, out, files)
    if artifact:
        do_artifact(ctx, out, artifact)
    do_listing(ctx, out, files)
    do_secrets(ctx, out, files)
    if not merged and not artifact:
        ctx["unknown"].append("No merged manifest found under build/intermediates, so permissions contributed by libraries and SDKs are not visible: run a release build (for example ./gradlew :app:processReleaseMainManifest) and re-scan, or pass --artifact.")
    if any(f.startswith(("buildSrc/", "build-logic/", "build-plugin/")) for f in files):
        ctx["unknown"].append("Values computed in convention plugins are only partly resolved because Gradle is never run: inspect the release build or its merged manifest.")
    ctx["unknown"].append("Play Console state (Data safety form, app content declarations, testing track status, store listing text beyond fastlane files) is not in the repository: check it in Play Console.")
    out["permissions"] = ordered(out["permissions"])
    out["components"] = ordered(out["components"])
    out["build"]["gradle"] = ordered(out["build"].get("gradle", []))
    out["build"]["manifest"] = ordered(out["build"].get("manifest", []))
    out["secrets"] = ordered(out["secrets"])
    out["unknown"] = sorted(set(ctx["unknown"]))
    out["errors"] = sorted(set(ctx["errors"]))
    return out


def summary(out):
    flagged = sorted({"%s (%s)" % (p["permission"], p["class"]) for p in out["permissions"] if p.get("class") and not p.get("removed") and not p.get("blocked")})
    return {"schema_version": 1, "tool_version": TOOL_VERSION, "truncated": True,
            "hint": "Full JSON is over %d bytes: re-run with --output FILE and read it in parts, or use --section." % STDOUT_LIMIT,
            "project_kind": out["project_kind"]["primary"] if out["project_kind"] else None,
            "counts": {k: len(out[k]) for k in ("modules", "permissions", "components", "secrets", "unknown", "errors")},
            "classified_permissions": flagged[:40], "unknown": out["unknown"][:20], "errors": out["errors"][:20]}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False)
    ap.add_argument("project_dir", metavar="PROJECT_DIR")
    ap.add_argument("--output", metavar="FILE", help="write the full JSON here (must be outside PROJECT_DIR)")
    ap.add_argument("--artifact", metavar="PATH", help="a built .apk or .aab to inspect")
    ap.add_argument("--section", nargs="+", choices=SECTIONS, metavar="NAME", help="only these sections: " + ", ".join(SECTIONS))
    ap.add_argument("--pretty", action="store_true", help="indent the JSON by 2 spaces")
    args = ap.parse_args(argv)
    root = args.project_dir
    if not os.path.isdir(root):
        ap.error("PROJECT_DIR is not a directory: %s" % root)
    if args.artifact and (not os.path.isfile(args.artifact) or not args.artifact.lower().endswith((".apk", ".aab"))):
        ap.error("--artifact must be an existing .apk or .aab file")
    real = os.path.realpath(root)
    if args.output and os.path.commonpath([real, os.path.realpath(args.output)]) == real:
        ap.error("--output must be outside PROJECT_DIR: this tool never writes into the project")
    out = scan(root, args.artifact)
    body = {"schema_version": 1}
    body.update({k: v for k, v in out.items() if k not in SECTIONS or not args.section or k in args.section})
    def dump(d):
        return json.dumps(d, indent=2 if args.pretty else None, separators=None if args.pretty else (",", ":")) + "\n"
    text = dump(body)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    sys.stdout.write(text if len(text) <= STDOUT_LIMIT else dump(summary(out)))
    return 3 if out["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
