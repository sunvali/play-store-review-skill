plugins { id("com.android.application") }
android {
    namespace = "com.example.helpdesk"
    compileSdk = 36
    defaultConfig {
        applicationId = "com.example.helpdesk"
        minSdk = 26
        targetSdk = 36
        versionCode = 77
        versionName = "5.2.0"
    }
}
dependencies {
    implementation("com.example.support:chat-sdk:3.4.0")
}
