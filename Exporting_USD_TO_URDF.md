# How to export your robot in USD version to URDF?

In this tutorial, I’ll provide a step-by-step guide on how to export any robot model to URDF. Mastering this process is a crucial milestone in your robotics journey, as it sets the foundation for advanced tasks like kinematics and motion planning.

To ensure a successful export, your model must follow a specific articulation structure. I will walk you through the essential rules and best practices to get your robot simulation-ready.

## Step 1: Enabling the USD to URDF extension

Go to **window → extensions** then search for **USD to URDF** and then toggle it on.

This will enable the URDF exporter. Now you can go to **file → export_to_urdf** in order to export the USD file that you are **CURRENTLY** on.

## Step 2: Default Prim and Articulation Root

When using this exporter, keep in mind that the **default prim** and the **children** of that prim will be the **ONLY** ones that will be exported.

![alt text](image.png) 

Therefore, move your highest level xform/prim (my_robot in this case) and drag it out of **World** to be it's separate entity.

```
Note: The highest level prim should act as just a container of all the individual parts of your robot and should not be a rigid body of its own. Furthermore, this prim should also be the Articulation Root of your robot.

```

## Step 3: Rigid bodies
Moreover, this container should have ALL the rigid bodies that make up your robot, it can contain other things, but ALL rigid bodies must be directly below it.

## Step 4: Fixed Joints

## Step 5: Joints scope

## Step 6: Colliders

## What next?