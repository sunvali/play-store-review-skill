package com.example.platecoach

import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable

// Shows the generated meal plan. Output comes straight from the model.
@Composable
fun CoachReply(reply: String) {
    Column { Text(reply) }
}
