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
Note: The highest level prim should act as just a container of all the individual parts of your robot and should not be a rigid body of its own. Furthermore, this prim should also be the Articulation Root of your robot as its the prim that represents the WHOLE robot.

```

## Step 3: Rigid bodies
Ensure your robot's hierarchy is properly structured before exporting. All Rigid Bodies should be direct descendants of your top-level prim. If a Rigid Body is tucked inside a sub-Xform, drag it out and drop it directly under the root container to prevent export errors.

### Physics and Mass Requirements

The URDF format is inherently physics-heavy. For a successful export, the physics engine requires a fully defined kinematic chain where every Rigid Body (any independent part of the robot) is connected via a Joint.

In addition to the structure, every Rigid Body must have its physical properties defined—specifically its Mass. Before exporting, ensure each body has a Mass API applied:

1. Select the Rigid Body in the Stage.

2. Navigate to `Add → Physics → Mass.`

Pro-tip: You can leave the values as **Autocomputed** for now, or enter specific values if you have the technical specifications for your robot's components.

### Why this matters

Without assigned mass and proper joint connections, the physics engine cannot calculate the inertia tensor or the dynamics of the robot. This will lead to errors in both the URDF export and any subsequent kinematics simulations in Lula or RMPflow.


## Step 4: Fixed Joints
This is a crucial point to explain because hierarchy errors are the #1 reason URDF exports fail or "explode" when loaded. I’ve refined your explanation to be more technical yet easy to follow, using clear formatting to highlight the **Body 0 / Body 1** logic.

### The Role of Fixed Joints

In URDF, every piece of geometry must be part of a continuous "tree." While **Revolute Joints** are obvious for moving parts, **Fixed Joints** are equally vital. They act as the "glue" that anchors your robot to the root and connects non-moving components.

To ensure the physics engine and the URDF exporter understand your robot’s structure, follow this hierarchical flow:

`[Top Prim] —(Fixed Joint)→ [Base Link] —(Fixed Joint)→ [Moving System] —(Revolute Joint)→ [Child Links]`

if your robot has more than one moving system-like a dual arm robot-then continue like this:
`[Top Prim] —(Fixed Joint)→ [Base Link] —(Fixed Joint)→ [First Moving System] —(Revolute Joint)→ [Child Links] && [Base link]—(Fixed Joint)→ [Second Moving System] and so on...`                                      `


### Body 0 and Body 1 Rule

When creating joints in Isaac Sim, you must explicitly define the parent-child relationship using the **Body 0** and **Body 1** fields in the Joint Properties. This tells the exporter which way the "physics" flow.

#### 1. Anchoring the Base

For the joint connecting your **Top Prim** to your **Base**:

* **Body 0 (Parent):** The Top Prim (Root Xform).
* **Body 1 (Child):** The Robot Base.
* **Joint Type:** Fixed.

#### 2. Connecting the First Moving Part

For the joint connecting your **Base** to the **First Link** of an arm or wheel system:

* **Body 0 (Parent):** The Robot Base.
* **Body 1 (Child):** The first part of the moving system (e.g., Shoulder or Axle).
* **Joint Type:** Fixed (or Revolute, depending on your design).

#### 3. Sequential Moving Joints

Continue this pattern down the chain:

* **Body 0:** The previous link.
* **Body 1:** The new link.
* **Joint Type:** Revolute, Prismatic, etc.

> **Why this matters:** If you reverse Body 0 and Body 1, you create a "circular dependency" or a reversed kinematic chain. This will cause your robot to behave erratically in simulations like Lula or move in ways that defy physics.

## Step 5: Joints scope
You might be wondering: "If all Rigid Bodies must be direct children of the top prim, where do I put the joints?" To keep your Stage clean and ensure a successful export, the best practice is to group all your joints into a Scope. Unlike an Xform, a Scope is a container that does not carry its own coordinate transformations, making it "invisible" to the kinematic math while keeping your file organized:

1. right click on the empty space on the stage tab then `create → scope → rename to **joints**`
2. drag all the joints under this scope.

> Note: Make sure all the joints are ONLY under this scope.

## Step 6: Colliders



## What next?