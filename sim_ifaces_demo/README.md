# ROS 2 Simulation Interfaces Demo: Object Inspection in Jetty World

This demo showcases the practical application of the
[ROS 2 Simulation Interfaces](https://github.com/ros-simulation/simulation_interfaces)
within a simulated environment. These interfaces provide a standardized,
simulator-agnostic set of ROS 2 service, message, and action definitions for
controlling and interacting with various simulation platforms.

## Demo Overview

The primary goal of this demo is to illustrate the utility of the ROS 2
Simulation Interfaces by orchestrating a simulated object inspection process. We
simulate a scenario where:

1. Objects are spawned onto a conveyor belt.
2. The conveyor belt transports these objects to a designated inspection area.
3. A robot arm scans the objects using an attached camera, simulating a
   fictitious object pose estimation task.

## Key Simulation Interfaces Used

This demo leverages the following ROS 2 Simulation Interfaces services:

- `GetEntityState`. Used to get the pose of the tray so as to know where to span
  the objects and to monitor its movement along the conveyor belt.
- `ResetSimulation`: Resets the simulation to the initial state (before objects
  are spawned).
- `SetEntityState`: Used to control the velocity of the tray. _Note: While
  functional for demonstration, this method of implementing conveyor belt motion
  is not generally recommended._
- `SpawnEntity`: Used to spawn objects on the tray. The Gazebo implementation of
  this service supports spawning models from files, strings, or directly from
  **Gazebo Fuel**. The demo specifically highlights spawning models from Fuel by
  simply providing a Fuel URI.

In addition to the conveyor belt orchestration, you will find a script that
computes the bounding box of the spawned items using Gazebo's Python API. The
bounding box dimensions are used in a simple algorithm that attempts to spawn
the objects on the tray such that they are not initially in contact.

## Running the Demo

Terminal 1

```bash
ros2 launch sim_ifaces_demo demo.launch.xml
```

Terminal 2

```bash
ros2 run sim_ifaces_demo conveyor_controller
```

This will start the demo inside the Jetty Demo world as shown below:

![sim_ifaces_jetty_demo](https://github.com/user-attachments/assets/a26decf4-30eb-44b5-bbd6-214e67b84497)

You can edit `sim_ifaces_demo/launch/demo.launch.xml` and set the
`world_sdf_file` to `$(find-pkg-share jetty_demo)/worlds/sim_ifaces_demo.sdf`.
That is

```xml
...
<gz_server world_sdf_file="$(find-pkg-share jetty_demo)/worlds/sim_ifaces_demo.sdf"/>
...

```

This will run the demo inside an empty world as shown below:

![sim_ifaces](https://github.com/user-attachments/assets/bcb7fe49-0639-432c-8827-a131b179d3a0)
