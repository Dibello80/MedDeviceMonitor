package com.example.meddevicemonitor.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.URL

class NetworkDeviceClient {

    private val endpoint = "http://10.0.2.2:5000/api/reading"

    fun streamReadings(): Flow<DeviceReading> = flow {
        while (true) {
            val reading = fetchReading()
            emit(reading)
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