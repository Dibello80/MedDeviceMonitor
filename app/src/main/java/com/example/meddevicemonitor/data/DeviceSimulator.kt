package com.example.meddevicemonitor.data

import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlin.random.Random

class DeviceSimulator {

    fun streamReadings(): Flow<DeviceReading> = flow {
        while (true) {
            delay(1000)

            val reading = DeviceReading(
                heartRate = Random.nextInt(65, 105),
                oxygenLevel = Random.nextInt(94, 100),
                temperature = Random.nextDouble(97.2, 99.8)
            )

            emit(reading)
        }
    }
}