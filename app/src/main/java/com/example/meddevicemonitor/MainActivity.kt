package com.example.meddevicemonitor

import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.meddevicemonitor.data.DeviceReading
import com.example.meddevicemonitor.ui.MainViewModel
import com.example.meddevicemonitor.ui.theme.MedDeviceMonitorTheme
import com.example.meddevicemonitor.data.DeviceLog
import androidx.compose.animation.core.*
import androidx.compose.runtime.*
import androidx.compose.ui.graphics.Path
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            MedDeviceMonitorTheme {
                val viewModel: MainViewModel = viewModel()
                val state by viewModel.uiState.collectAsState()

                Scaffold(
                    modifier = Modifier.fillMaxSize(),
                    containerColor = Color(0xFF0D1117)
                ) { innerPadding ->

                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(innerPadding)
                            .padding(16.dp)
                            .verticalScroll(rememberScrollState()),
                        verticalArrangement = Arrangement.spacedBy(14.dp)
                    ) {

                        Text(
                            text = "MedDevice Monitor",
                            color = Color.White,
                            style = MaterialTheme.typography.headlineMedium,
                            fontWeight = FontWeight.Bold
                        )

                        Text(
                            text = "Real-time medical device dashboard",
                            color = Color(0xFF8B949E),
                            style = MaterialTheme.typography.bodyMedium
                        )

                        StatusCard(
                            connected = state.isConnected,
                            monitoring = state.isMonitoring,
                            connecting = state.isConnecting
                        )

                        state.errorMessage?.let {
                            AlertBanner(message = it)
                        }

                        state.alertMessage?.let {
                            AlertBanner(message = it)
                        }

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            VitalCard(
                                title = "Heart Rate",
                                value = state.reading?.heartRate?.toString() ?: "--",
                                unit = "bpm",
                                normalRange = "60–100",
                                isAlert = (state.reading?.heartRate ?: 0) > 100,
                                modifier = Modifier.weight(1f)
                            )

                            VitalCard(
                                title = "Oxygen",
                                value = state.reading?.oxygenLevel?.toString() ?: "--",
                                unit = "%",
                                normalRange = "95–100",
                                isAlert = (state.reading?.oxygenLevel ?: 100) < 95,
                                modifier = Modifier.weight(1f)
                            )
                        }

                        VitalCard(
                            title = "Temperature",
                            value = state.reading?.temperature?.let {
                                String.format("%.1f", it)
                            } ?: "--",
                            unit = "°F",
                            normalRange = "97.0–99.0°F",
                            isAlert = (state.reading?.temperature ?: 0.0) > 99.0,
                            modifier = Modifier.fillMaxWidth()
                        )

                        HeartRateChart(history = state.readingHistory)

                        DeviceLogs(logs = state.logs)

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            Button(
                                onClick = { viewModel.startMonitoring() },
                                enabled = !state.isMonitoring,
                                modifier = Modifier.weight(1f)
                            ) {
                                Text("Start")
                            }

                            Button(
                                onClick = { viewModel.stopMonitoring() },
                                enabled = state.isMonitoring,
                                modifier = Modifier.weight(1f)
                            ) {
                                Text("Stop")
                            }
                        }

                        OutlinedButton(
                            onClick = { viewModel.simulateDisconnect() },
                            enabled = state.isMonitoring,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("Simulate Disconnect")
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun StatusCard(
    connected: Boolean,
    monitoring: Boolean,
    connecting: Boolean
) {
    val statusText = when {
        connecting -> "CONNECTING..."
        connected && monitoring -> "CONNECTED / MONITORING"
        connected -> "CONNECTED"
        else -> "DISCONNECTED"
    }

    val statusColor = when {
        connecting -> Color(0xFFFFC107)
        connected -> Color(0xFF2ECC71)
        else -> Color(0xFFE74C3C)
    }

    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF161B22))
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(18.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text(
                    text = "Device Status",
                    color = Color.White,
                    fontWeight = FontWeight.Bold
                )

                Text(
                    text = "External sensor stream",
                    color = Color(0xFF8B949E),
                    style = MaterialTheme.typography.bodySmall
                )
            }

            Text(
                text = statusText,
                color = statusColor,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
fun VitalCard(
    title: String,
    value: String,
    unit: String,
    normalRange: String,
    isAlert: Boolean,
    modifier: Modifier = Modifier
) {
    val valueColor = if (isAlert) Color(0xFFFF5252) else Color(0xFF00E5FF)
    val statusText = if (isAlert) "WARNING" else "NORMAL"
    val statusColor = if (isAlert) Color(0xFFFF5252) else Color(0xFF2ECC71)

    Card(
        modifier = modifier,
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF161B22))
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Text(
                text = title,
                color = Color.White,
                fontWeight = FontWeight.Bold
            )

            Text(
                text = statusText,
                color = statusColor,
                style = MaterialTheme.typography.bodySmall,
                fontWeight = FontWeight.Bold
            )

            Row(verticalAlignment = Alignment.Bottom) {
                Text(
                    text = value,
                    color = valueColor,
                    style = MaterialTheme.typography.displaySmall,
                    fontWeight = FontWeight.Bold
                )

                Spacer(modifier = Modifier.width(6.dp))

                Text(
                    text = unit,
                    color = Color(0xFF8B949E),
                    style = MaterialTheme.typography.titleSmall
                )
            }

            Text(
                text = "Normal: $normalRange",
                color = Color(0xFF8B949E),
                style = MaterialTheme.typography.bodySmall
            )
        }
    }
}

@Composable
fun AlertBanner(message: String) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF5A1E1E))
    ) {
        Text(
            text = "ALERT: $message",
            color = Color.White,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(16.dp)
        )
    }
}

@Composable
fun HeartRateChart(history: List<DeviceReading>) {

    val animatedProgress by animateFloatAsState(
        targetValue = history.size.toFloat(),
        animationSpec = tween(durationMillis = 500),
        label = "chartAnim"
    )

    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(170.dp),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF161B22))
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "Live Heart Rate",
                color = Color.White,
                fontWeight = FontWeight.Bold
            )

            Spacer(modifier = Modifier.height(10.dp))

            Canvas(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(110.dp)
            ) {

                if (history.size < 2) return@Canvas

                val minHr = 60f
                val maxHr = 110f

                val widthStep = size.width / (history.size - 1)

                val path = Path()

                history.forEachIndexed { index, reading ->
                    val x = index * widthStep

                    val y = size.height - (
                            (reading.heartRate - minHr) /
                                    (maxHr - minHr) * size.height
                            )

                    if (index == 0) {
                        path.moveTo(x, y)
                    } else {
                        val prevX = (index - 1) * widthStep
                        val prevY = size.height - (
                                (history[index - 1].heartRate - minHr) /
                                        (maxHr - minHr) * size.height
                                )

                        val controlX = (prevX + x) / 2

                        path.quadraticBezierTo(
                            controlX, prevY,
                            x, y
                        )
                    }
                }

                drawPath(
                    path = path,
                    color = Color(0xFF00E5FF),
                    style = androidx.compose.ui.graphics.drawscope.Stroke(
                        width = 5f,
                        cap = StrokeCap.Round
                    )
                )
            }
        }
    }
}
@Composable
fun DeviceLogs(logs: List<DeviceLog>) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFF161B22))
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            Text(
                text = "Device Logs",
                color = Color.White,
                fontWeight = FontWeight.Bold
            )

            logs.takeLast(5).forEach { log ->
                Text(
                    text = log.message,
                    color = Color(0xFF8B949E),
                    style = MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}