plugins { id("com.android.application") }
android { namespace = "com.example.quizpals"; compileSdk = 36
  defaultConfig { applicationId = "com.example.quizpals"; minSdk = 26; targetSdk = 36; versionCode = 3; versionName = "1.0.2" } }
dependencies { implementation("com.google.android.gms:play-services-ads:23.5.0") }
