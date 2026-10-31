package com.example.stride

// Reads steps for the daily chart. HRV is requested for a planned recovery score and stored locally, but no screen shows it yet.
class HealthRepository {
    val permissions = setOf("READ_STEPS", "READ_HEART_RATE_VARIABILITY")
}
