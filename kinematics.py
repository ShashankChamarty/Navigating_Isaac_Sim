from isaacsim import SimulationApp
import os
import numpy as np

# 1. Start the app
simulation_app = SimulationApp({"headless": False})

from isaacsim.core.api.world import World
from isaacsim.core.api.robots.robot import Robot
from isaacsim.core.prims import SingleXFormPrim
from isaacsim.core.utils.stage import add_reference_to_stage
from omni.isaac.motion_generation import ArticulationKinematicsSolver, LulaKinematicsSolver

class DualArmKinematics:
    def __init__(self) -> None:
        self._world = World(physics_dt=1.0/60.0, rendering_dt=1.0/60.0)
        self._world.scene.add_default_ground_plane()

        # Paths
        self._downloads_path = os.path.expanduser("~/Downloads/Junebase_Primos")
        self._usd_path = os.path.join(self._downloads_path, "Junebase_Primos.usd")
        self._urdf_path = os.path.join(self._downloads_path, "primos_final.urdf")
        self._left_yaml = os.path.join(self._downloads_path, "Left_Arm.yaml")
        self._right_yaml = os.path.join(self._downloads_path, "Right_Arm.yaml")

        # Load Robot
        add_reference_to_stage(usd_path=self._usd_path, prim_path="/World/MyRobot")
        self._robot = self._world.scene.add(Robot(prim_path="/World/MyRobot", name="so_arm"))

        # Targets
        self._left_target = SingleXFormPrim("/World/LeftTarget", name="left_target")
        self._right_target = SingleXFormPrim("/World/RightTarget", name="right_target")
        
        # Initial positions
        self._left_target.set_world_pose(position=np.array([0.2, 0.15, 0.3]))
        self._right_target.set_world_pose(position=np.array([0.2, -0.15, 0.3]))

    def setup_left_arm(self):
        """Initializes everything specific to the LEFT arm"""
        self._left_lula = LulaKinematicsSolver(self._left_yaml, self._urdf_path)
        self._left_ik_solver = ArticulationKinematicsSolver(self._robot, self._left_lula, "LeftEndEffector")
        
        # Register the left-specific physics callback
        self._world.add_physics_callback("left_arm_loop", callback_fn=self.on_left_physics_step)
        print("Left Arm Solver Initialized")

    def setup_right_arm(self):
        """Initializes everything specific to the RIGHT arm"""
        self._right_lula = LulaKinematicsSolver(self._right_yaml, self._urdf_path)
        self._right_ik_solver = ArticulationKinematicsSolver(self._robot, self._right_lula, "RightEndEffector")
        
        # Register the right-specific physics callback
        self._world.add_physics_callback("right_arm_loop", callback_fn=self.on_right_physics_step)
        print("Right Arm Solver Initialized")

    def on_left_physics_step(self, step_size):
        # 1. Get BOTH Position and Orientation (the target_ori is a Quaternion)
        curr_pos, curr_ori = self._left_target.get_world_pose()
        base_pos, base_ori = self._robot.get_world_pose()
        
        # 2. Sync
        self._left_lula.set_robot_base_pose(base_pos, base_ori)
        
        # 3. Solve with ORIENTATION instead of None
        # Passing curr_ori forces the wrist to match the gizmo's rotation
        action, success = self._left_ik_solver.compute_inverse_kinematics(curr_pos, None)

        if success:
            self._robot.apply_action(action)
        else:
            # If it fails, it's likely because the wrist CAN'T reach that specific angle
            print("Left IK Fail: Target rotation might be impossible")

    def on_right_physics_step(self, step_size):
        # 1. Get Target and Base
        curr_pos, _ = self._right_target.get_world_pose()
        base_pos, base_ori = self._robot.get_world_pose()
        
        # 2. Sync and Solve
        self._right_lula.set_robot_base_pose(base_pos, base_ori)
        action, success = self._right_ik_solver.compute_inverse_kinematics(curr_pos, None)

        # 3. Apply
        if success:
            self._robot.apply_action(action)
        else:
            print("Right IK Unsuccessful")

if __name__ == "__main__":
    logic = DualArmKinematics()
    logic._world.reset() 
    
    # Now you can call them separately!
    logic.setup_left_arm()
   #logic.setup_right_arm()

    while simulation_app.is_running():
        logic._world.step(render=True)
    
    simulation_app.close()