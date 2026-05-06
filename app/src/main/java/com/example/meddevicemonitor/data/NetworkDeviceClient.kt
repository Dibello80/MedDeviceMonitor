package com.example.meddevicemonitor.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.URL

class NetworkDeviceClient {

    private val endpoint = "https://meddevicemonitor.onrender.com/api/reading"

    fun streamReadings(): Flow<DeviceReading> = flow {
        while (true) {
            try {
                val reading = fetchReading()
                emit(reading)
            } catch (e: Exception) {
                e.printStackTrace()
            }
            delay(1000)
        }
    }

    private suspend fun fetchReading(): DeviceReading {
        return withContext(Dispatchers.IO) {
            val response = URL(endpoint).readText()
            val json = JSONObject(response)

            DeviceReading(
                heartRate = json.getInt("heartRate"),
                oxygenLevel = json.getInt("oxygenLevel"),
                temperature = json.getDouble("temperature")
            )
        }
    }
}