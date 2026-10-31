plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
}

android {
    namespace = "com.example.demo"
    compileSdk = libs.versions.compileSdk.get().toInt()
    ndkVersion = "27.0.12077973"
    defaultConfig {
        applicationId = "com.example.demo"
        minSdk = 24
        targetSdk = 35
        versionCode = 7
        versionName = "1.2"
    }
    buildTypes {
        release {
            isMinifyEnabled = true
            signingConfig = signingConfigs.getByName("release")
        }
        debug {
            isDebuggable = true
        }
    }
    productFlavors {
        create("play") { dimension = "store" }
    }
    packaging { jniLibs { useLegacyPackaging = false } }
}

dependencies {
    implementation(libs.billing.ktx)
    implementation(libs.firebase.analytics)
    implementation(libs.play.ads)
    implementation("io.sentry:sentry-android:7.10.0")
    testImplementation("com.onesignal:OneSignal:5.0.0")
}
