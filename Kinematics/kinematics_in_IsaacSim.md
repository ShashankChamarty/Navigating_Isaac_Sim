# Kinematics using Lula robot description

Lula Robot description is Isaac Sim's inbuilt forward and inverse kinematics calculator that provides the angles in radians for each revolute joint to reach a certain target position for your specific robot articulation. 

Note: while creating the YAML files you also need to add collision spheres for the software to mathematically calculate the path towards a target position.

## PREREQUISITS for using Lula Software

You already need to have the following files ready before we can move forward with using the Lula Kinematics library:
    1. A URDF file version of your robot.
    2. A .yaml robot description file.


## Creation of the YAML File

The YAML file is generated using the **Robot Description Editor** extension within Isaac Sim. This tool automates the process by pulling data directly from your robot's USD.

### 1. Loading the Articulation
The editor requires your robot to be loaded as an **Articulation (USD file)**. Once selected, the editor automatically populates a list of every joint and link name directly from the USD hierarchy, ensuring naming consistency between the simulator and the solver.

### 2. Configuring Joint States
For every joint in the populated list, you must manually define its role:
* **Active:** Mark joints that the IK solver is permitted to move to reach a goal (e.g., the 6 revolute joints of an arm).
* **Fixed:** Mark joints that must remain stationary, such as base mounts, fixed chassis parts, or static sensors.
* **Chain Definition:** You must explicitly designate a **Base Link** (where the kinematics start) and a **Tip Link** (the end-effector).

### 3. Collision Spheres
Lula uses simplified geometry for real-time performance. 
* Within the editor, you must add **Collision Spheres** to each link in the kinematic chain.
* These spheres define the mathematical "hitbox" of the robot. The solver uses these to calculate a path that prevents the robot from colliding with its own links or external environment objects.

---

## Using the Lula Software for Kinematics

The Python implementation follows a standardized three-step logic: **Initialization, Synchronization, and Execution.**

### 1. Initializing the Solvers
First, create the `LulaKinematicsSolver` by pointing it to your YAML and URDF. Then, wrap it in an `ArticulationKinematicsSolver` to allow it to communicate directly with the USD Articulation in the stage.

```python
from omni.isaac.motion_generation import ArticulationKinematicsSolver, LulaKinematicsSolver

# 1. Initialize the math engine
lula_solver = LulaKinematicsSolver(robot_description_path, urdf_path)

# 2. Wrap it to interface with the USD Articulation
ik_solver = ArticulationKinematicsSolver(robot_articulation, lula_solver, "end_effector_name")
```
### 2. Synchronizing the Base Pose
Lula calculates joint solutions relative to the robot's origin. If the robot moves in the world, the solver must be updated with the robot's current world position every physics frame to ensure the target coordinates are mapped correctly.

```python
# Get current world pose from the robot articulation
base_pos, base_ori = robot_articulation.get_world_pose()

# Sync the solver with the current world state
lula_solver.set_robot_base_pose(base_pos, base_ori)
```
### 3. Executing the solution
The solver takes a target coordinate and returns the necessary joint positions as an action.

    1. Success Check: The solver returns a boolean. If the target is unreachable or would cause a self-collision (based on your YAML spheres), it returns False.

    2. Applying Action: If successful, apply the action to move the actual robot.

```python
# Compute the angles needed to reach the target position (X, Y, Z)
# Orientation can be passed as a quaternion or 'None' to ignore rotation
action, success = ik_solver.compute_inverse_kinematics(target_position, target_orientation)

if success:
    # Move the robot to the calculated positions
    robot_articulation.apply_action(action)
else:
    print("IK Solver: Target is unreachable or violates collision constraints.")
```

## Summary
Lula provides a robust mathematical pipeline for robot motion:

    1. Robot Description Editor extracts joint data from the USD to define Active/Fixed states and Collision Spheres.

    2. Lula Solver uses those constraints to understand the physical workspace.

    3. The Script feeds real-time coordinates from isaac simulaiton environment into the solver, which translates them into the precise radian angles that revolute joints must move in order to do the task.