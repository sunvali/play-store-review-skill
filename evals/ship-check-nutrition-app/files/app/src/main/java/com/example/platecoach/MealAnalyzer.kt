package com.example.platecoach

import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody

// Sends the meal photo and the user's goal weight to the coach backend, which forwards them to OpenAI.
class MealAnalyzer(private val client: OkHttpClient) {
    fun analyze(jpeg: ByteArray, goalWeightKg: Double): String {
        val request = Request.Builder()
            .url("https://api.platecoach.example/v1/analyze?goal=$goalWeightKg")
            .post(jpeg.toRequestBody("image/jpeg".toMediaType()))
            .build()
        return client.newCall(request).execute().use { it.body!!.string() }
    }
}
