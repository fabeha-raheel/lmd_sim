# Realtime Landmine Detection and Mapping Drone - ROS-Gazebo Simulation
This package simulates an autonomous landmine detection and mapping drone. For the purposes of simulation, landmines are recognized using computer vision / image processing techniques by detecting their characteristic red color. Once the landmines are detected, the drone records their GPS coordinates and updates them on a map.

## Installations
The package was tested on Ubuntu 20.04 with ROS Noetic and Gazebo installed. Instructions regarding installation of ROS Noetic can be found here. (add a hyperlink.)

The following packages also need to be installed:

1. MAVROS

    ```bash
    sudo apt-get install ros-noetic-mavros ros-noetic-mavros-extras
    wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh
    chmod a+x install_geographiclib_datasets.sh
    ./install_geographiclib_datasets.sh
    ```
    For more information, visit: https://ardupilot.org/dev/docs/ros-install.html#installing-mavros

2. Python Packages

    Python packages for OpenCV, ROSCVBridge, Imutils, Pickle, Tkinter and Tkintermapview.

    To install tkintermapview, refer to the following page: https://github.com/TomSchimansky/TkinterMapView

## Running the Simulation

1. Download Mission Planner on Linux and run it in one terminal.
2. Run the following launch file in the second terminal:
```bash
roslaunch lmd_sim lmd_simulation.launch
```
3. Adjust the windows: MavProxy console, ArduCopter terminal & Gazebo Simulator.
4. Right-click on the drone model in Gazebo and select Follow.
5. Open the Mission waypoints file and write it to the drone.
6. Shift drone to Auto Mode.         