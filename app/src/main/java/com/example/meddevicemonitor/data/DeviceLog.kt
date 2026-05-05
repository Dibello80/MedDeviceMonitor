package com.example.meddevicemonitor.data

data class DeviceLog(
    val message: String,
    val timestamp: Long = System.currentTimeMillis()
)