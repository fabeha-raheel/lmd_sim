# 🛰️ Realtime Autonomous UAV for Landmine Detection, Localization, and Mapping

This project presents a **ROS–Gazebo based simulation** of an autonomous UAV system capable of **detecting, localizing, and mapping landmines in real time** using **computer vision and GPS-based geotagging**. The system integrates **ROS, MAVROS, ArduPilot SITL, and Gazebo** to simulate a drone that autonomously surveys a terrain, identifies potential landmines based on visual cues, and plots their coordinates on a live interactive map.

🎥 [Watch complete simulation](https://www.youtube.com/watch?v=o2FmneBpySA)

![LMD Simulation](assets/lmd.png) 

---

## 🎯 Key Highlights
- **Autonomous Mission Execution:** Fully automated waypoint navigation via MAVROS and ArduPilot SITL.
- **Realtime Landmine Detection:** Vision-based detection using **OpenCV** to identify landmines from live camera feed.
- **Geolocation Mapping:** Logs GPS coordinates of detected landmines and displays them on a **TkinterMapView GUI** in real time.
- **End-to-End ROS Integration:** Communication between Gazebo drone, MAVProxy, and ArduPilot for realistic flight behavior.
- **Interactive Visualization:** Map-based GUI for monitoring detections and mission progress.

---

## 🧩 System Architecture

| Component | Description |
|------------|-------------|
| **Gazebo Simulator** | Provides 3D simulation environment for UAV and terrain. |
| **ArduPilot SITL** | Runs flight control logic for autonomous navigation. |
| **ROS + MAVROS** | Middleware enabling communication between ArduPilot and ROS nodes. |
| **Computer Vision Node** | Detects landmines using OpenCV and publishes detections to ROS topics. |
| **Mapping GUI** | Displays detected landmine locations in real time using TkinterMapView. |

---

## ⚙️ Pre-requisites

The package was tested on **Ubuntu 20.04** with **ROS Noetic** and **Gazebo**.  
Installation instructions for ROS Noetic can be found [here](http://wiki.ros.org/noetic/Installation/Ubuntu).

### Required Packages

#### 1. MAVROS

``` bash
    sudo apt-get install ros-noetic-mavros ros-noetic-mavros-extras
    wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
    chmod a+x install_geographiclib_datasets.sh
    ./install_geographiclib_datasets.sh
```

For more information, visit: [Installing MAVROS Guide](https://ardupilot.org/dev/docs/ros-install.html#installing-mavros)


#### 2. Python Packages
    
Python packages for OpenCV, ROSCVBridge, Imutils, Pickle, Tkinter and [Tkintermapview](https://github.com/TomSchimansky/TkinterMapView).

```bash
    pip install opencv-python imutils pillow
```

To install tkintermapview, refer to the following page: https://github.com/TomSchimansky/TkinterMapView

#### 3. Mission Planner (optional)

While **Mission Planner** is Windows-native, it can be run on Linux using **Mono**. See instructions [here](https://ardupilot.org/planner/docs/mission-planner-installation.html#mission-planner-on-linux)

## 🚀 Pacakge Installation

To install the lmd_sim package, first create a new workspace directory similar to catkin_ws in your home directory:

```bash
cd
mkdir -p lmd_ws/src
cd lmd_ws/
catkin_make
```

Then clone the lmd_sim repository inside src:

```bash
cd ~/lmd_ws/src
git clone https://github.com/fabeha-raheel/lmd_sim.git
```

Then, select a branch to run.

## Running the Simulation

1. Download Mission Planner on Linux and run it in one terminal.
3. Run the following launch file in the second terminal to launch the Gazebo world with the Ardupilot drone:
```bash
    roslaunch lmd_sim lmd_simulation.launch
```
4. Use Mission Planner to connect with the drone. Plan an Autonomous searching mission and write it to the drone. Also save the misison waypoints for future missions.
5. Adjust the windows: MavProxy console, ArduCopter terminal, Gazebo Simulator, Drone Video Screen & Tkinter Mapping GUI.
6. Right-click on the drone model in Gazebo and select Follow.
7. Shift the Drone to Auto Mode using the following MAV commands:
```bash
    mode guided
    arm throttle
    takeoff 1
    mode auto
```





