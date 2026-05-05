package com.example.meddevicemonitor.ui

import kotlinx.coroutines.delay
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.meddevicemonitor.data.DeviceLog
import com.example.meddevicemonitor.data.DeviceReading
import com.example.meddevicemonitor.data.NetworkDeviceClient
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale


data class DeviceUiState(
    val isMonitoring: Boolean = false,
    val isConnected: Boolean = false,
    val isConnecting: Boolean = false,
    val reading: DeviceReading? = null,
    val readingHistory: List<DeviceReading> = emptyList(),
    val logs: List<DeviceLog> = emptyList(),
    val errorMessage: String? = null,
    val alertMessage: String? = null
)

class MainViewModel : ViewModel() {

    private val deviceClient = NetworkDeviceClient()

    private val _uiState = MutableStateFlow(
        DeviceUiState(
            logs = listOf(DeviceLog("System ready. Waiting for device connection."))
        )
    )

    val uiState: StateFlow<DeviceUiState> = _uiState

    private var job: Job? = null

    fun startMonitoring() {
        if (job != null) return

        addLog("Monitoring started.")

        job = viewModelScope.launch {
            try {
                var firstReading = true

                _uiState.value = _uiState.value.copy(
                    isMonitoring = true,
                    isConnected = false,
                    isConnecting = true,
                    errorMessage = null,
                    alertMessage = null
                )

                deviceClient.streamReadings().collect { reading ->

                    val alert = when {
                        reading.heartRate > 100 -> "High heart rate detected"
                        reading.oxygenLevel < 95 -> "Low oxygen level detected"
                        reading.temperature > 99.0 -> "Elevated temperature detected"
                        else -> null
                    }

                    val updatedHistory =
                        (_uiState.value.readingHistory + reading).takeLast(20)

                    _uiState.value = _uiState.value.copy(
                        reading = reading,
                        readingHistory = updatedHistory,
                        isConnected = true,
                        isConnecting = false,
                        errorMessage = null,
                        alertMessage = alert
                    )

                    if (firstReading) {
                        addLog("Device connected successfully.")
                        firstReading = false
                    }

                    if (alert != null) {
                        addLog("Alert triggered: $alert")
                    }
                }

            } catch (e: Exception) {
                addLog("Network error: ${e.message}")

                _uiState.value = _uiState.value.copy(
                    isMonitoring = false,
                    isConnected = false,
                    isConnecting = false,
                    errorMessage = "Unable to connect to device server.",
                    alertMessage = null
                )

                job = null
            }
        }
    }

    fun stopMonitoring() {
        job?.cancel()
        job = null

        addLog("Monitoring stopped.")

        _uiState.value = _uiState.value.copy(
            isMonitoring = false,
            isConnected = false,
            isConnecting = false,
            errorMessage = null,
            alertMessage = null
        )
    }

    fun simulateDisconnect() {
        job?.cancel()
        job = null

        addLog("Device disconnected unexpectedly.")

        _uiState.value = _uiState.value.copy(
            isMonitoring = false,
            isConnected = false,
            errorMessage = "Device disconnected. Please restart monitoring.",
            alertMessage = null
        )
    }

    private fun addLog(message: String) {
        val time = SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(Date())
        val log = DeviceLog("[$time] $message")
        val updatedLogs = (_uiState.value.logs + log).takeLast(8)

        _uiState.value = _uiState.value.copy(
            logs = updatedLogs
        )
    }

    override fun onCleared() {
        super.onCleared()
        job?.cancel()
    }
}