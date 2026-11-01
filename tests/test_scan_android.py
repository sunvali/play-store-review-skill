import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(HERE, "..", "skills", "play-store-review", "scripts", "scan_android.py")
FIX = os.path.join(HERE, "fixtures")
GOLDEN = os.path.join(HERE, "golden", "native.json")


def run(*args):
    p = subprocess.run([sys.executable, "-B", SCAN] + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def scan(name_or_path, *args):
    path = name_or_path if os.path.isabs(name_or_path) else os.path.join(FIX, name_or_path)
    code, out, err = run(path, *args)
    return code, json.loads(out)


def perms(data):
    return {(p["permission"], p["source"]): p for p in data["permissions"]}


def elf64(aligns):
    """A minimal little-endian ELF64 whose PT_LOAD segments have the given p_align values."""
    header = struct.pack("<16sHHIQQQIHHHHHH", b"\x7fELF\x02\x01\x01", 3, 183, 1, 0, 64, 0, 0, 64, 56, len(aligns), 0, 0, 0)
    phdrs = b"".join(struct.pack("<IIQQQQQQ", 1, 5, 0, 0, 0, 0x100, 0x100, a) for a in aligns)
    return header + phdrs


class FixtureTests(unittest.TestCase):
    def test_native_matches_golden(self):
        code, data = scan("native")
        self.assertEqual(code, 0)
        if os.environ.get("UPDATE_GOLDEN"):
            with open(GOLDEN, "w") as f:
                json.dump(data, f, indent=2)
                f.write("\n")
        with open(GOLDEN) as f:
            self.assertEqual(data, json.load(f))

    def test_native_facts(self):
        _, d = scan("native")
        p = perms(d)
        self.assertEqual(p[("android.permission.READ_SMS", "manifest")]["class"], "restricted-declaration")
        self.assertTrue(p[("com.google.android.gms.permission.AD_ID", "manifest")]["removed"])
        self.assertEqual(p[("android.permission.WRITE_EXTERNAL_STORAGE", "manifest")]["maxSdkVersion"], "28")
        self.assertNotIn(("android.permission.SYSTEM_ALERT_WINDOW", "manifest"), p, "debug source set must be skipped")
        billing = [i for i in d["dependencies"]["items"] if i["category"] == "billing"]
        self.assertEqual(billing[0]["version"], "7.0.0")
        self.assertEqual(d["sdk"]["compileSdk"][0]["value"], 35)
        self.assertNotIn("com.onesignal:OneSignal", [i["name"] for i in d["dependencies"]["items"]], "test deps are skipped")
        self.assertEqual({c["name"] for c in d["components"]}, {".Reader", ".SyncService"})

    def test_flutter(self):
        _, d = scan("flutter")
        self.assertEqual(d["project_kind"]["primary"], "flutter")
        self.assertEqual(d["sdk"]["targetSdk"][0]["expr"], "flutter.targetSdkVersion")
        self.assertNotIn("value", d["sdk"]["targetSdk"][0])
        self.assertEqual(d["sdk"]["agp"][0]["value"], "8.1.0")
        names = {(i["name"], i["confidence"]) for i in d["dependencies"]["items"]}
        self.assertIn(("geolocator_android", "resolved"), names)
        self.assertTrue(any("Flutter plugin permissions" in u for u in d["unknown"]))

    def test_expo(self):
        _, d = scan("expo")
        p = perms(d)
        self.assertTrue(p[("android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK", "expo-config")]["blocked"])
        self.assertEqual(p[("android.permission.CAMERA", "expo-config")]["confidence"], "declared")
        self.assertEqual(p[("android.permission.RECORD_AUDIO", "expo-config")]["confidence"], "inferred")
        self.assertEqual(d["sdk"]["targetSdk"][0]["value"], 35)
        self.assertIn("expo-build-properties", d["project_kind"]["expo"]["plugins"])
        self.assertTrue(any("library permissions" in u for u in d["unknown"]))
        self.assertTrue(any("no android/ directory" in u for u in d["unknown"]))

    def test_react_native_uses_merged_manifest(self):
        _, d = scan("rn")
        p = perms(d)
        self.assertEqual(p[("android.permission.READ_MEDIA_VIDEO", "merged")]["confidence"], "resolved")
        self.assertEqual(d["sdk"]["targetSdk"][0]["value"], 34)
        self.assertEqual(d["sdk"]["targetSdk"][0]["confidence"], "resolved")
        self.assertEqual(d["sdk"]["ndk"][0]["value"], "26.1.10909125")
        self.assertFalse(any("No merged manifest" in u for u in d["unknown"]))

    def test_one_line_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "build.gradle.kts"), "w") as f:
                f.write('android {\n    compileSdk = 36\n    defaultConfig { minSdk = 26; targetSdk = 36; versionCode = 12 }\n}\n'
                        'dependencies { implementation("com.google.android.gms:play-services-ads:23.5.0") }\n')
            _, data = scan(d)
        self.assertEqual(data["sdk"]["targetSdk"][0]["value"], 36)
        self.assertEqual(data["sdk"]["minSdk"][0]["value"], 26)
        self.assertIn("ads", {i["category"] for i in data["dependencies"]["items"]})

    def project(self, files):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)
        for rel, text in files.items():
            os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
            with open(os.path.join(d, rel), "w") as f:
                f.write(text)
        return d

    def test_app_sdk_prefers_shared_script_over_wear_module(self):
        d = self.project({
            "common.gradle": "android {\n    compileSdk 36\n    defaultConfig { targetSdk propTarget.toInteger() }\n}\n",
            "gradle.properties": "propTarget=36\n",
            "app/build.gradle": 'apply plugin: "com.android.application"\nandroid {\n    defaultConfig { applicationId "a.b" }\n}\n',
            "app-wearos/build.gradle": 'android {\n    defaultConfig { applicationId "a.w"\n targetSdk 34\n }\n}\n'})
        app = scan(d)[1]["sdk"]["app"]["targetSdk"]
        self.assertEqual((app["value"], app["file"]), (36, "common.gradle"))

    def test_constant_in_convention_plugin(self):
        d = self.project({
            "build-plugin/src/main/kotlin/app.gradle.kts": "android {\n    defaultConfig { targetSdk = Config.sdkTarget }\n}\n",
            "build-plugin/src/main/kotlin/Config.kt": "object Config {\n    const val sdkTarget = 36\n}\n"})
        self.assertEqual(scan(d)[1]["sdk"]["app"]["targetSdk"]["value"], 36)

    def test_agp9_release_from_catalog_and_demo_module_is_not_the_app(self):
        block = "android {\n    compileSdk {\n        version = release(libs.versions.compileSdk.get().toInt())\n    }\n    defaultConfig { applicationId \"a.b\" }\n}\n"
        d = self.project({"gradle/libs.versions.toml": '[versions]\ncompileSdk = "37"\n',
                          "app/build.gradle.kts": block, "demo/camera/build.gradle.kts": block.replace("libs.versions.compileSdk.get().toInt()", "33")})
        app = scan(d)[1]["sdk"]["app"]["compileSdk"]
        self.assertEqual((app["value"], app["scope"]), (37, "app"))

    def test_catalog_bundle_and_add_form(self):
        d = self.project({
            "gradle/libs.versions.toml": '[libraries]\nfcm = { module = "com.google.firebase:firebase-messaging", version = "24.0.0" }\n'
                                         'ads = { module = "com.google.android.gms:play-services-ads", version = "23.0.0" }\n'
                                         '[bundles]\ngplay = [\n  "fcm",\n]\n',
            "app/build.gradle.kts": 'android {\n}\ndependencies {\n    add(flavor, libs.bundles.gplay)\n    implementation(libs.ads)\n}\n'})
        names = {i["name"] for i in scan(d)[1]["dependencies"]["items"]}
        self.assertEqual(names, {"com.google.firebase:firebase-messaging", "com.google.android.gms:play-services-ads"})

    def test_permissions_name_module_and_source_set(self):
        manifest = '<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/></manifest>'
        d = self.project({"app/src/website/AndroidManifest.xml": manifest})
        p = scan(d)[1]["permissions"][0]
        self.assertEqual((p["module"], p["source_set"]), ("app", "website"))

    def test_flavor_removal_is_linked_to_main_permission(self):
        head = '<manifest xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools">'
        name = 'android:name="android.permission.REQUEST_INSTALL_PACKAGES"'
        d = self.project({"app/src/main/AndroidManifest.xml": head + "<uses-permission %s/></manifest>" % name,
                          "app/src/gplay/AndroidManifest.xml": head + '<uses-permission %s tools:node="remove"/></manifest>' % name})
        main = [p for p in scan(d)[1]["permissions"] if p["source_set"] == "main"][0]
        self.assertEqual(main["removed_in"], ["gplay"])

    def test_expo_config_override_and_missing_override(self):
        pkg = '{"dependencies":{"expo":"58.0.0"}}'
        d = self.project({"package.json": pkg, "app.config.js": "export default { plugins: [['expo-build-properties', {android: {targetSdkVersion: 36}}]] }\n"})
        data = scan(d)[1]
        self.assertEqual(data["sdk"]["app"]["targetSdk"]["value"], 36)
        self.assertEqual(data["project_kind"]["expo"]["expoPackage"], "58.0.0")
        self.assertTrue(any("Expo sets the default" in u for u in scan(self.project({"package.json": pkg}))[1]["unknown"]))

    def test_catalog_nearest_the_module_and_multi_app(self):
        app = 'plugins { id("com.android.application") }\nandroid { compileSdk = 36\n  defaultConfig { applicationId = "com.x"; minSdk = 24; targetSdk = libs.versions.targetSdk.get().toInt() } }\n'
        d = self.project({"A/app/build.gradle.kts": app, "A/gradle/libs.versions.toml": '[versions]\ntargetSdk = "33"\n',
                          "B/app/build.gradle.kts": app, "B/gradle/libs.versions.toml": '[versions]\ntargetSdk = "36"\n',
                          "B/demo/build.gradle.kts": app})
        sdk = scan(d)[1]["sdk"]
        self.assertEqual([(a["module"], a["targetSdk"]) for a in sdk["apps"]], [("A/app", 33), ("B/app", 36)])
        self.assertTrue(sdk["app"]["ambiguous"])

    def test_demo_scope_is_never_the_app(self):
        d = self.project({"demo/build.gradle.kts": 'plugins { id("com.android.application") }\nandroid { defaultConfig { targetSdk = 33 } }\n'})
        data = scan(d)[1]
        self.assertNotIn("targetSdk", data["sdk"]["app"])
        self.assertEqual(data["sdk"]["apps"], [])
        self.assertTrue(any("demo, sample" in u for u in data["unknown"]))

    def test_configure_extension_and_multiline_assignment(self):
        d = self.project({
            "settings.gradle.kts": 'include(":app")\n', "gradle/libs.versions.toml": '[versions]\ntargetSdk = "37"\n',
            "app/build.gradle.kts": 'plugins { alias(libs.plugins.android.application) }\nconfigure<ApplicationExtension> {\n    compileSdk = 36\n'
                                    '    defaultConfig {\n        applicationId = "com.x"\n        minSdk = 29\n        targetSdk =\n            libs.versions.targetSdk\n'
                                    '                .get()\n                .toInt()\n    }\n}\n',
            "app/src/main/AndroidManifest.xml": '<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.READ_SMS"/></manifest>'})
        data = scan(d)[1]
        self.assertEqual(data["project_kind"]["primary"], "native-gradle")
        self.assertEqual([(m["path"], m["type"]) for m in data["modules"]], [("app", "application")])
        self.assertEqual({k: v["value"] for k, v in data["sdk"]["app"].items() if k != "ambiguous"}, {"compileSdk": 36, "minSdk": 29, "targetSdk": 37})
        self.assertEqual(len(data["permissions"]), 1)

    def test_module_identity(self):
        d = self.project({
            "gradle.properties": "APP_PACKAGE=com.from.props\n",
            "build.gradle.kts": 'plugins { alias(libs.plugins.android.application) apply false }\nplugins.withId("com.android.application") { android { compileSdk = 30 } }\n',
            "app/build.gradle.kts": 'plugins { id("com.android.application") }\nandroid {\n defaultConfig { applicationId = APP_PACKAGE }\n'
                                    ' productFlavors {\n  create("play") { ndk { abiFilters += "arm64-v8a" } }\n  create("fdroid") { ext { x = 1 } }\n }\n}\n'})
        data = scan(d)[1]
        self.assertEqual([m["path"] for m in data["modules"]], ["app"])
        self.assertEqual((data["modules"][0]["applicationId"], data["modules"][0]["flavors"]), ("com.from.props", ["fdroid", "play"]))

    def test_sdk_values_in_convention_plugin_kotlin(self):
        d = self.project({"app/build.gradle.kts": 'plugins { id("myapp.android.application") }\nandroid { namespace = "com.x" }\n',
                          "build-logic/convention/src/main/kotlin/AppPlugin.kt": "class AppPlugin { fun apply() { extensions.configure<ApplicationExtension> { defaultConfig.targetSdk = 36; compileSdk = 37; defaultConfig.minSdk = 24 } } }\n"})
        app = scan(d)[1]["sdk"]["app"]
        self.assertEqual((app["targetSdk"]["value"], app["compileSdk"]["value"], app["minSdk"]["value"]), (36, 37, 24))
        self.assertEqual(app["targetSdk"]["scope"], "shared build script")

    def test_expo_ads_config_is_redacted(self):
        d = self.project({"package.json": '{"dependencies":{"expo":"~55.0.0"}}',
                          "app.json": '{"expo":{"android":{"config":{"googleMobileAdsAppId":"ca-app-pub-1~2"}},"plugins":[["react-native-google-mobile-ads",{"androidAppId":"ca-app-pub-1~2"}]]}}'})
        out = run(d)[1]
        self.assertNotIn("ca-app-pub-1~2", out)
        items = {i["name"]: i for i in json.loads(out)["dependencies"]["items"]}
        self.assertEqual(items["android.config.googleMobileAdsAppId"]["masked"], "ca-a...")
        self.assertEqual(items["react-native-google-mobile-ads"]["category"], "ads")

    def test_cordova_config(self):
        cfg = ('<widget id="com.x" version="1.0"><platform name="android"><preference name="android-targetSdkVersion" value="34"/>'
               '<config-file target="AndroidManifest.xml" parent="/manifest"><uses-permission android:name="android.permission.READ_SMS"/></config-file></platform>'
               '<preference name="android-minSdkVersion" value="24"/><plugin name="cordova-plugin-camera" spec="^6"/><plugin name="cordova-admob-plus" spec="^1"/></widget>')
        data = scan(self.project({"config.xml": cfg}))[1]
        self.assertEqual(data["project_kind"]["primary"], "cordova")
        self.assertEqual((data["sdk"]["app"]["targetSdk"]["value"], data["sdk"]["app"]["minSdk"]["value"]), (34, 24))
        self.assertEqual([p["permission"] for p in data["permissions"]], ["android.permission.READ_SMS"])
        self.assertEqual([i["name"] for i in data["dependencies"]["items"]], ["cordova-admob-plus"])
        code, bad = scan(self.project({"config.xml": '<!DOCTYPE x [<!ENTITY a "b">]>' + cfg}))
        self.assertTrue(any("DOCTYPE" in e for e in bad["errors"]))

    def test_unity_settings_and_packages(self):
        d = self.project({"ProjectSettings/ProjectVersion.txt": "m_EditorVersion: 6000.0.1f1\n",
                          "ProjectSettings/ProjectSettings.asset": "PlayerSettings:\n  AndroidMinSdkVersion: 23\n  AndroidTargetSdkVersion: 0\n",
                          "Packages/manifest.json": '{"dependencies":{"com.unity.purchasing":"4.12.2","com.unity.services.mediation":"1.0.0","com.unity.ads":"4.4.2","com.unity.services.analytics":"6.0.0","com.unity.ugui":"2.0.0"}}'})
        data = scan(d)[1]
        self.assertEqual(data["sdk"]["minSdk"][0]["value"], 23)
        self.assertEqual((data["sdk"]["targetSdk"][0]["expr"], data["sdk"]["targetSdk"][0]["automatic"]), ("automatic (0)", True))
        self.assertEqual({i["name"]: i["category"] for i in data["dependencies"]["items"]},
                         {"com.unity.purchasing": "billing", "com.unity.services.mediation": "ads", "com.unity.ads": "ads", "com.unity.services.analytics": "analytics"})

    def test_unsupported_engines_are_named(self):
        cases = {
            "godot": {"game/project.godot": "config_version=5\n"},
            "maui": {"src/App.csproj": "<Project><PropertyGroup><TargetFrameworks>net9.0-android;net9.0-ios</TargetFrameworks></PropertyGroup></Project>"},
            "nativescript": {"nativescript.config.ts": "export default {}\n"},
            "tauri": {"src-tauri/tauri.conf.json": "{}\n"},
        }
        for kind, files in cases.items():
            data = scan(self.project(files))[1]
            self.assertEqual(data["project_kind"]["primary"], kind)
            self.assertEqual(sum("cannot read %s" % kind in u for u in data["unknown"]), 1, data["unknown"])
            self.assertFalse(any("No Android project markers" in u for u in data["unknown"]))

    def test_plain_dotnet_project_is_not_maui(self):
        data = scan(self.project({"Lib.csproj": "<Project><PropertyGroup><TargetFramework>net9.0</TargetFramework></PropertyGroup></Project>"}))[1]
        self.assertEqual(data["project_kind"]["primary"], "unknown")

    def test_dependency_configuration_and_false_positives(self):
        d = self.project({
            "app/build.gradle.kts": 'plugins { id("com.android.application") }\nandroid { defaultConfig { applicationId = "com.x" } }\ndependencies {\n'
                                    '  "playImplementation"("com.android.billingclient:billing:7.0.0")\n  standardImplementation("com.google.android.gms:play-services-ads-identifier:18.0.0")\n'
                                    '  implementation("com.google.androidbrowserhelper:billing:2.5.0")\n}\n',
            "buildscript-gradle.lockfile": "org.tensorflow:tensorflow-lite-metadata:0.2.0=classpath\n",
            "pubspec.yaml": "name: x\ndependencies:\n  in_app_purchase: ^3.0.0\n  in_app_purchase_storekit: ^0.3.0\n  google_mobile_ads_web: ^1.0.0\n"})
        items = scan(d)[1]["dependencies"]["items"]
        got = {(i["name"], i["category"], i.get("configuration")) for i in items}
        self.assertEqual(got, {("com.android.billingclient:billing", "billing", "playImplementation"),
                               ("com.google.android.gms:play-services-ads-identifier", "attribution", "standardImplementation"),
                               ("com.google.androidbrowserhelper:billing", "billing", "implementation"),
                               ("in_app_purchase", "billing", None)})

    def test_manifest_selection(self):
        head = '<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.%s"/></manifest>'
        d = self.project({
            "app/build.gradle": 'plugins { id "com.android.application" }\nandroid { sourceSets { release { manifest.srcFile \'config/release/AndroidManifest_prod.xml\' } } }\n',
            "app/config/release/AndroidManifest_prod.xml": head % "ACCESS_BACKGROUND_LOCATION",
            "app/config/debug/AndroidManifest.xml": head % "SYSTEM_ALERT_WINDOW",
            "app/src/freeDebug/AndroidManifest.xml": head % "READ_SMS",
            "app/src/main/AndroidManifest.xml": head % "CAMERA"})
        got = {(p["permission"].split(".")[-1], p["source_set"]) for p in scan(d)[1]["permissions"]}
        self.assertEqual(got, {("ACCESS_BACKGROUND_LOCATION", "release"), ("CAMERA", "main")})

    def test_npm_outside_project_root_is_not_counted(self):
        d = self.project({"app/build.gradle.kts": 'plugins { id("com.android.application") }\nandroid { }\n',
                          "website/package.json": '{"dependencies":{"@sentry/react-native":"^6"}}'})
        data = scan(d)[1]
        self.assertEqual(data["dependencies"]["items"], [])
        self.assertTrue(any("website/package.json" in u and "outside" in u for u in data["unknown"]))

    def test_may_add_permissions(self):
        gradle = 'plugins { id("com.android.application") }\nandroid { }\ndependencies { implementation("com.google.firebase:firebase-analytics-ktx:22.0.0") }\n'
        head = '<manifest xmlns:android="http://schemas.android.com/apk/res/android" xmlns:tools="http://schemas.android.com/tools">%s</manifest>'
        data = scan(self.project({"app/build.gradle.kts": gradle}))[1]
        hit = data["dependencies"]["mayAddPermissions"][0]
        self.assertEqual((hit["dependency"], hit["mayAdd"], hit["basis"]), ("com.google.firebase:firebase-analytics-ktx", ["com.google.android.gms.permission.AD_ID"], "field report, verify in the merged manifest"))
        removed = head % '<uses-permission android:name="com.google.android.gms.permission.AD_ID" tools:node="remove"/>'
        self.assertEqual(scan(self.project({"app/build.gradle.kts": gradle, "app/src/main/AndroidManifest.xml": removed}))[1]["dependencies"]["mayAddPermissions"], [])
        expo = scan(self.project({"package.json": '{"dependencies":{"expo":"~55","expo-audio":"1","expo-video":"1"}}',
                                  "app.json": '{"expo":{"android":{"blockedPermissions":["FOREGROUND_SERVICE_MEDIA_PLAYBACK"]}}}'}))[1]
        self.assertEqual(expo["dependencies"]["mayAddPermissions"], [])

    def test_output_flag_prints_one_summary_line(self):
        out = os.path.join(tempfile.mkdtemp(), "facts.json")
        self.addCleanup(shutil.rmtree, os.path.dirname(out))
        code, text, _ = run(os.path.join(FIX, "rn"), "--output", out)
        self.assertEqual(len(text.strip().splitlines()), 1)
        self.assertIn("wrote", text)
        with open(out) as f:
            self.assertEqual(json.load(f)["tool_version"], "1.4.0")

    def test_dangling_symlink_is_not_an_error(self):
        d = self.project({"app/build.gradle": "android {\n}\n"})
        os.symlink("missing.txt", os.path.join(d, "app", "title.txt"))
        code, data = scan(d)
        self.assertEqual((code, data["errors"]), (0, []))

    def test_output_is_deterministic_and_sectioned(self):
        a = run(os.path.join(FIX, "rn"))[1]
        self.assertEqual(a, run(os.path.join(FIX, "rn"))[1])
        _, d = scan("rn", "--section", "permissions")
        self.assertIn("permissions", d)
        self.assertNotIn("sdk", d)
        self.assertIn("unknown", d)

    def test_project_is_not_modified(self):
        def snapshot():
            return sorted((dp, tuple(sorted(fn))) for dp, _, fn in os.walk(FIX))
        before = snapshot()
        run(os.path.join(FIX, "native"))
        self.assertEqual(before, snapshot())


class HostileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.proj = os.path.join(self.tmp, "proj")
        shutil.copytree(os.path.join(FIX, "hostile"), self.proj)
        outside = os.path.join(self.tmp, "outside.txt")
        with open(outside, "w") as f:
            f.write("not part of the project")
        os.symlink(outside, os.path.join(self.proj, "escape.gradle"))
        with open(os.path.join(self.proj, "app", "big.properties"), "w") as f:
            f.write("x" * (2 * 1024 * 1024 + 1))
        # built at run time so no key-shaped string is committed
        self.secret = "AIza" + "Sy" + "A" * 33
        with open(os.path.join(self.proj, "app", "Keys.kt"), "w") as f:
            f.write('val key = "%s"\n' % self.secret)
        with open(os.path.join(self.proj, "app", "build.gradle"), "a") as f:
            f.write('signingConfigs { release { storePassword "hunter2hunter2" } }\n')

    def test_hostile_project(self):
        code, out, _ = run(self.proj)
        d = json.loads(out)
        self.assertEqual(code, 3)
        self.assertTrue(any("DOCTYPE" in e for e in d["errors"]))
        self.assertEqual(d["permissions"], [], "a rejected manifest yields no facts")
        self.assertTrue(any("escape.gradle" in u and "outside the project" in u for u in d["unknown"]))
        self.assertTrue(any("big.properties" in u and "2 MB" in u for u in d["unknown"]))
        kinds = {(s["kind"], s.get("masked"), s.get("key")) for s in d["secrets"]}
        self.assertIn(("google-api-key", "AIza...", None), kinds)
        self.assertIn(("hardcoded-signing-password", None, "storePassword"), kinds)
        self.assertNotIn(self.secret, out)
        self.assertNotIn("hunter2", out)
        self.assertNotIn("not part of the project", out)

    def test_output_must_be_outside_project(self):
        code, _, err = run(self.proj, "--output", os.path.join(self.proj, "facts.json"))
        self.assertEqual(code, 2)
        self.assertIn("outside PROJECT_DIR", err)

    def test_bad_arguments(self):
        self.assertEqual(run(os.path.join(self.tmp, "missing"))[0], 2)
        self.assertEqual(run(self.proj, "--nope")[0], 2)
        self.assertEqual(run(self.proj, "--section", "verdict")[0], 2)
        self.assertEqual(run(self.proj, "--artifact", os.path.join(self.tmp, "x.apk"))[0], 2)

    def test_large_output_prints_summary_and_writes_full_file(self):
        lines = "".join('<uses-permission android:name="com.example.P%d" />\n' % i for i in range(600))
        os.makedirs(os.path.join(self.proj, "app2", "src", "main"))
        with open(os.path.join(self.proj, "app2", "src", "main", "AndroidManifest.xml"), "w") as f:
            f.write('<manifest xmlns:android="http://schemas.android.com/apk/res/android">%s</manifest>' % lines)
        out = run(self.proj)[1]
        self.assertLess(len(out), 20000)
        self.assertTrue(json.loads(out)["truncated"])
        full = os.path.join(self.tmp, "facts.json")
        _, line, _ = run(self.proj, "--output", full)
        self.assertEqual(len(line.strip().splitlines()), 1)
        with open(full) as f:
            self.assertEqual(len(json.load(f)["permissions"]), 600)


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.proj = os.path.join(self.tmp, "empty")
        os.mkdir(self.proj)

    def make_zip(self, name, entries):
        path = os.path.join(self.tmp, name)
        with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as z:
            for n, data in entries.items():
                z.writestr(n, data)
        return path

    def test_elf_alignment_in_apk(self):
        manifest = '<manifest xmlns:android="http://schemas.android.com/apk/res/android"><uses-permission android:name="android.permission.CAMERA"/></manifest>'
        apk = self.make_zip("app.apk", {
            "AndroidManifest.xml": manifest,
            "lib/arm64-v8a/good.so": elf64([0x4000, 0x4000]),
            "lib/x86_64/bad.so": elf64([0x1000, 0x1000]),
            "lib/arm64-v8a/mixed.so": elf64([0x4000, 0x1000]),
            "lib/armeabi-v7a/ignored.so": elf64([0x1000]),
            "lib/arm64-v8a/junk.so": b"not an elf",
        })
        code, d = scan(self.proj, "--artifact", apk)
        self.assertEqual(code, 0)
        libs = {os.path.basename(x["file"]): x for x in d["native"]["libraries"]}
        self.assertEqual(set(libs), {"good.so", "bad.so", "mixed.so", "junk.so"})
        self.assertTrue(libs["good.so"]["compatible_16kb"])
        self.assertEqual((libs["good.so"]["p_align_min"], libs["good.so"]["p_align_max"]), (0x4000, 0x4000))
        self.assertFalse(libs["bad.so"]["compatible_16kb"])
        self.assertFalse(libs["mixed.so"]["compatible_16kb"], "every PT_LOAD must be 16 KB aligned")
        self.assertEqual(libs["junk.so"]["error"], "not an ELF file")
        self.assertIsInstance(libs["good.so"]["zip_aligned_16kb"], bool)
        self.assertEqual(libs["good.so"]["confidence"], "resolved")
        self.assertEqual(perms(d)[("android.permission.CAMERA", "artifact")]["class"], "must-have-core-use")

    def test_binary_manifest_without_aapt2_is_unknown(self):
        apk = self.make_zip("bin.apk", {"AndroidManifest.xml": b"\x03\x00\x08\x00binary"})
        env = {"PATH": "/nonexistent"}
        p = subprocess.run([sys.executable, "-B", SCAN, self.proj, "--artifact", apk], capture_output=True, text=True, env=env)
        self.assertTrue(any("aapt2" in u for u in json.loads(p.stdout)["unknown"]))

    def test_aab_reports_bundleconfig_unknown(self):
        aab = self.make_zip("app.aab", {"base/lib/arm64-v8a/a.so": elf64([0x4000]), "BundleConfig.pb": b"\x0a\x00"})
        _, d = scan(self.proj, "--artifact", aab)
        self.assertTrue(any("PAGE_ALIGNMENT_16K" in u for u in d["unknown"]))
        self.assertTrue(d["native"]["libraries"][0]["compatible_16kb"])
        self.assertNotIn("zip_aligned_16kb", d["native"]["libraries"][0])

    def test_source_tree_so_is_inferred(self):
        so = os.path.join(self.proj, "app", "src", "main", "jniLibs", "arm64-v8a")
        os.makedirs(so)
        with open(os.path.join(so, "libx.so"), "wb") as f:
            f.write(elf64([0x1000]))
        _, d = scan(self.proj)
        lib = d["native"]["libraries"][0]
        self.assertEqual((lib["confidence"], lib["compatible_16kb"]), ("inferred", False))


if __name__ == "__main__":
    unittest.main()
