package com.example.meddevicemonitor.data

data class DeviceReading(
    val heartRate: Int,
    val oxygenLevel: Int,
    val temperature: Double,
    val timestamp: Long = System.currentTimeMillis()
)