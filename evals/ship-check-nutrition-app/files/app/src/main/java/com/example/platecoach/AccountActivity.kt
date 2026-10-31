package com.example.platecoach

import android.os.Bundle
import androidx.activity.ComponentActivity

// Sign up, sign in, sign out and edit profile. Users create accounts with email and password.
class AccountActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) { super.onCreate(savedInstanceState) }
    fun signUp(email: String, password: String) { Api.post("/signup", email, password) }
    fun signOut() { Api.post("/signout") }
}
object Api { fun post(path: String, vararg args: String) {} }
