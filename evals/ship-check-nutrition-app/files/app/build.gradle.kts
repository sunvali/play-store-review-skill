plugins { id("com.android.application") }
android {
    namespace = "com.example.platecoach"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.example.platecoach"
        minSdk = 26
        targetSdk = 35
        versionCode = 41
        versionName = "1.4.0"
    }
    buildTypes { release { isMinifyEnabled = true } }
}
dependencies {
    implementation(libs.billing.ktx)
    implementation(libs.firebase.analytics)
    implementation(libs.imagepicker)
    implementation("com.squareup.okhttp3:okhttp:4.12.0")
}
