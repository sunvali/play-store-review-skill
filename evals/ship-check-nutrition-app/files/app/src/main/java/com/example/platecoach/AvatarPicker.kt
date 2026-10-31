package com.example.platecoach

import android.app.Activity
import com.github.dhaval2404.imagepicker.ImagePicker

// Only use of the gallery: choosing a profile avatar once.
fun pickAvatar(activity: Activity) {
    ImagePicker.with(activity).galleryOnly().start()
}
