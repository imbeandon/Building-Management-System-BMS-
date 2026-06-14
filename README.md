# Smart Home Automation System

## Overview

This project is a Raspberry Pi–based Smart Home Automation System that monitors environmental conditions and automatically manages home security, lighting, and HVAC operations. The system integrates multiple sensors and actuators to create an energy-efficient and safety-focused home environment.

Features include:

* Temperature and humidity monitoring using a DHT11 sensor
* Motion detection using a PIR sensor
* Automated HVAC heating and cooling control
* Door and window security monitoring
* Fire detection and emergency alert system
* LCD status display
* Energy usage and cost tracking
* LED indicators for system status

---

## Hardware Components

* Raspberry Pi
* DHT11 Temperature/Humidity Sensor
* PIR Motion Sensor
* LCD1602 Display
* Red, Green, and Blue LEDs
* Push Buttons
* Door/Window Security Switch
* Jumper Wires and Breadboard

---

## System Features

### Environmental Monitoring

The system continuously reads temperature and humidity data from the DHT11 sensor. A heat index is calculated using recent temperature readings to provide a more stable representation of room conditions.

### HVAC Control

Users can adjust the desired room temperature using dedicated buttons.

The HVAC system automatically:

* Activates heating when the room temperature is significantly below the target temperature.
* Activates cooling when the room temperature is significantly above the target temperature.
* Turns off when the room reaches the desired range.

LED indicators display HVAC status:

| LED  | Status         |
| ---- | -------------- |
| Red  | Heating Active |
| Blue | Cooling Active |
| Off  | HVAC Disabled  |

### Motion Detection

A PIR sensor monitors room occupancy.

When motion is detected:

* Green LED turns on
* LCD updates room occupancy status

When no motion is detected:

* Green LED turns off
* LCD updates accordingly

### Security Monitoring

The system monitors door and window status.

If a door or window is opened:

* HVAC operation is suspended
* LCD displays a warning message
* System updates security status

When secured again:

* HVAC functionality resumes automatically

### Fire Detection and Emergency Response

If the calculated heat index exceeds a safety threshold:

* HVAC system is disabled
* Doors/windows are marked as open
* All LEDs flash repeatedly
* LCD displays evacuation warnings

Emergency alerts continue until safe temperature conditions return.

### Energy Consumption Tracking

The system tracks HVAC runtime and estimates:

* Energy consumption (kWh)
* Operating cost

When HVAC operation stops, energy statistics are displayed on the LCD.

---

## Software Architecture

The application uses Python multithreading to improve responsiveness.

### Threads

#### Temperature Monitoring Thread

Responsible for:

* Reading DHT11 sensor data
* Calculating heat index
* Detecting fire conditions
* Managing HVAC decisions

#### Motion Detection Thread

Responsible for:

* Monitoring occupancy
* Updating lighting status
* Updating LCD information

### Event-Driven Controls

GPIO interrupts are used for:

* Increasing target temperature
* Decreasing target temperature
* Toggling door/window security state

This reduces CPU usage compared to continuous polling.

---

## GPIO Pin Configuration

| Component               | GPIO Pin |
| ----------------------- | -------- |
| DHT11 Sensor            | 21       |
| PIR Motion Sensor       | 23       |
| Green LED               | 5        |
| Red LED                 | 26       |
| Blue LED                | 16       |
| Temperature Up Button   | 13       |
| Temperature Down Button | 27       |
| Security Button         | 25       |

---

## Required Python Libraries

```bash
pip install Adafruit_DHT
pip install RPi.GPIO
```

Additional modules:

```python
LCD1602
threading
time
```

---

## Running the Project

1. Connect all sensors and components to the Raspberry Pi.
2. Enable GPIO functionality.
3. Install required Python libraries.
4. Run the application:

```bash
python3 "EECS113 Final.py"
```

---

## Example LCD Display

Normal Operation:

```text
75/78     D:SAFE
H:COOL    L:ON
```

Where:

* 75 = Desired temperature
* 78 = Current temperature index
* SAFE = Doors/windows secured
* COOL = HVAC cooling mode
* ON = Motion detected

---

## Educational Objectives

This project demonstrates:

* Embedded systems programming
* GPIO interfacing
* Sensor integration
* Event-driven programming
* Multithreading
* Real-time monitoring
* Energy management concepts
* Home automation system design

---

## Future Improvements

* Mobile application integration
* Wi-Fi remote monitoring
* Cloud data logging
* Smart thermostat scheduling
* Email/SMS emergency notifications
* Additional environmental sensors
* Machine learning–based occupancy prediction

---

## Authors

**Brandon Huynh**
University of California, Irvine
B.S. Computer Engineering

**Course:** EECS 113 – Embedded Systems Design Project
