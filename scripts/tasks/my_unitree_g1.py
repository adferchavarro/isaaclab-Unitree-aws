
from isaaclab.envs import RLTask
import torch
import math

class MyUnitreeG1(RLTask):
    def __init__(self, cfg, sim_device, graphics_device_id, headless):
        super().__init__(cfg, sim_device, graphics_device_id, headless)

        # Cargar URDF del G1
        self.robot = self.scene.add_articulation(
            "unitree_g1",
            urdf_file="/workspace/assets/unitree/g1/urdf/g1.urdf"
        )

        # Objetivo inicial: posición de pie
        self.target_pose_standing = {
            "joint_hip_left": 0.0,
            "joint_knee_left": 0.0,
            "joint_ankle_left": 0.0,
            "joint_hip_right": 0.0,
            "joint_knee_right": 0.0,
            "joint_ankle_right": 0.0
        }

        self.reset()

    def get_observations(self):
        obs = torch.cat([
            self.robot.get_joint_positions(),
            self.robot.get_joint_velocities(),
            self.robot.get_root_state()
        ], dim=-1)
        return obs

    def get_rewards(self):
        # Recompensa por estar erguido
        torso_height = self.robot.get_link_world_poses("torso_link")[0][2]
        height_reward = torch.clamp(torso_height - 0.9, min=0.0, max=1.0)

        # Penalización por caerse
        fall_penalty = torch.where(torso_height < 0.4, -1.0, 0.0)

        # Recompensa por equilibrio en un pie
        foot_contact = self.robot.get_link_contact_forces(["foot_left", "foot_right"])
        balance_reward = 0.0
        if foot_contact[0].norm() > 0 and foot_contact[1].norm() == 0:
            balance_reward = 1.0

        reward = height_reward + balance_reward + fall_penalty
        return reward

    def reset(self):
        self.robot.set_joint_positions(torch.zeros(self.robot.num_dofs))
        self.robot.set_joint_velocities(torch.zeros(self.robot.num_dofs))
