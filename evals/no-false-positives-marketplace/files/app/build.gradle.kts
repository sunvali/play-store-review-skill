plugins { id("com.android.application") }
android {
    namespace = "com.example.farmbox"
    compileSdk = 36
    defaultConfig { applicationId = "com.example.farmbox"; minSdk = 26; targetSdk = 36; versionCode = 12; versionName = "1.2.0" }
    buildTypes { release { isMinifyEnabled = false } }
}
dependencies {
    implementation("com.stripe:stripe-android:21.0.0")
    implementation("com.google.firebase:firebase-analytics-ktx:22.1.2")
}
