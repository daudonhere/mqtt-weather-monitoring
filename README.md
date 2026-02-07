# IoT Weather Monitoring System – ESP32-Based Environmental Monitoring Node

## Project Description

This project is an implementation of an **Internet of Things (IoT)-based environmental monitoring system** designed to measure **temperature and humidity** in real time using an **ESP32 microcontroller** and a **DHT22 sensor**.

The measurement data is displayed locally on a **16x2 LCD with I2C interface** and transmitted to a server using the **MQTT protocol**, enabling remote monitoring and integration with dashboards or backend systems. The system is also equipped with an **environmental alert mechanism**, consisting of **LED indicators and a buzzer** that activate when temperature or humidity values exceed predefined safe thresholds.

Although the system already supports wireless communication and real-time data publishing, decision-making and alert handling are still performed locally on the device. Therefore, this system can be categorized as a **basic IoT monitoring node**, representing an early stage toward more advanced **smart environment** or **smart building** systems.

This project is suitable for **educational purposes**, **IoT experimentation**, and as a foundation for the development of more advanced **environmental monitoring and automation systems**.

---

![Project Screenshot](./screenshoot.png)

## Hardware Requirements

* ESP32 Development Board  
* DHT22 Temperature and Humidity Sensor  
* 16x2 LCD with I2C Interface  
* LEDs (Normal and Warning Indicators)  
* Buzzer  
* Connecting wires and power supply  

---

## Software Requirements

* MicroPython firmware for ESP32  
* MQTT Broker (e.g., broker.mqttdashboard.com)  
* WiFi connection  
* Optional: MQTT client or dashboard (Node-RED, MQTT Explorer, ThingsBoard)

---

## How to Run

### 1. Flash MicroPython Firmware
Install MicroPython on the ESP32 using `esptool.py`.

### 2. Upload the Code
Upload the MicroPython script to the ESP32 using one of the following tools:

* Thonny IDE  
* ampy  
* rshell  

### 3. Configure WiFi and MQTT
Edit the following variables in the source code to match your network and broker configuration:

```python
WIFI_SSID = "Your_WiFi_SSID"
WIFI_PASS = "Your_WiFi_Password"

MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC  = "wokwi/weather"
```

## 4. System Initialization and Operation

After deployment, the system automatically performs the following operations:

* Establishes a WiFi connection to the configured network  
* Connects to the specified MQTT broker  
* Periodically reads temperature and humidity data from the DHT22 sensor  
* Displays real-time sensor data on the LCD  
* Publishes sensor data to the configured MQTT topic in JSON format  
* Activates LED indicators and the buzzer when temperature or humidity values exceed predefined threshold limits  

---

## Notes

* Threshold values can be adjusted in the source code to accommodate different environmental conditions  
* Sensor calibration may be required to improve accuracy in real-world deployments  
* The current implementation is primarily intended for simulation, prototyping, and learning purposes  
* The system architecture can be extended with data logging, cloud integration, remote control capabilities, or multi-node deployment  
