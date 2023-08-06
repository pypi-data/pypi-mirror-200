"""The Aviary class, the core of how PyFlyt handles UAVs in the PyBullet simulation environment."""
from __future__ import annotations

import time
from itertools import repeat
from typing import Sequence

import numpy as np
import pybullet as p
import pybullet_data
from pybullet_utils import bullet_client

from .abstractions import DroneClass
from .drones import FixedWing, QuadX, Rocket

DroneIndex = int


class Aviary(bullet_client.BulletClient):
    """Aviary class, the core of how PyFlyt handles UAVs in the PyBullet simulation environment."""

    def __init__(
        self,
        start_pos: np.ndarray,
        start_orn: np.ndarray,
        drone_type: str | Sequence[str],
        drone_type_mappings: None | dict[str, DroneClass] = None,
        render: bool = False,
        physics_hz: int = 240,
        worldScale: float = 1.0,
        drone_options: dict | Sequence[dict] = {},
        seed: None | int = None,
    ):
        """Initializes a PyBullet environment that hosts UAVs and other entities.

        The Aviary class itself inherits from a BulletClient, so any function that a PyBullet client has, this class will have.
        The Aviary also handles dealing with physics and control looprates, as well as automatic construction of several default UAVs and their corresponding cameras.

        Args:
            start_pos (np.ndarray): start_pos
            start_orn (np.ndarray): start_orn
            drone_type (str | Sequence[str]): drone_types
            drone_type_mappings (None | dict[str, DroneClass]): string to mapping of custom drone classes
            render (bool): render
            physics_hz (int): physics_hz
            worldScale (float): worldScale
            drone_options (dict | Sequence[dict]): drone_options
            seed (None | int): seed
        """
        super().__init__(p.GUI if render else p.DIRECT)
        print("\033[A                             \033[A")

        # check for starting position and orientation shapes
        assert (
            len(start_pos.shape) == 2
        ), f"start_pos must be shape (n, 3), currently {start_pos.shape}."
        assert (
            start_pos.shape[-1] == 3
        ), f"start_pos must be shape (n, 3), currently {start_pos.shape}."
        assert (
            start_orn.shape == start_pos.shape
        ), f"start_orn must be same shape as start_pos, currently {start_orn.shape}."

        # check to ensure drone type has same number as drones if is list/tuple
        if isinstance(drone_type, (tuple, list)):
            assert (
                len(drone_type) == start_pos.shape[0]
            ), f"If multiple `drone_types` are used, must have same number of `drone_types` ({len(drone_type)}) as number of drones ({start_pos.shape[0]})."
        # check to ensure drone type has same number as drones if is list/tuple
        if isinstance(drone_options, (tuple, list)):
            assert (
                len(drone_options) == start_pos.shape[0]
            ), f"If multiple `drone_options` ({len(drone_options)}) are used, must have same number of `drone_options` as number of drones ({start_pos.shape[0]})."

        # constants
        self.num_drones = start_pos.shape[0]
        self.start_pos = start_pos
        self.start_orn = start_orn

        # do not change because pybullet doesn't like it
        # default physics looprate is 240 Hz
        self.physics_hz = physics_hz
        self.physics_period = 1.0 / physics_hz

        # mapping of drone type string to the constructors
        self.drone_type_mappings = dict()
        self.drone_type_mappings["quadx"] = QuadX
        self.drone_type_mappings["fixedwing"] = FixedWing
        self.drone_type_mappings["rocket"] = Rocket
        if drone_type_mappings is not None:
            self.drone_type_mappings = {
                **self.drone_type_mappings,
                **drone_type_mappings,
            }

        # store all drone types
        if isinstance(drone_type, (tuple, list)):
            assert all(
                dt in self.drone_type_mappings for dt in drone_type
            ), f"One of types in `drone_type` {drone_type} is not amongst known types {self.drone_type_mappings.keys()}."
            self.drone_type = drone_type
        else:
            assert (
                drone_type in self.drone_type_mappings
            ), f"Can't find `drone_type` {drone_type} amongst known types {self.drone_type_mappings.keys()}."
            self.drone_type = repeat(drone_type)

        # store the drone options
        if isinstance(drone_options, (tuple, list)):
            self.drone_options = drone_options
        else:
            self.drone_options = repeat(drone_options)

        # set the world scale and directories
        self.worldScale = worldScale
        self.setAdditionalSearchPath(pybullet_data.getDataPath())

        # render
        self.render = render
        self.rtf_debug_line = self.addUserDebugText(
            text="RTF here", textPosition=[0, 0, 0], textColorRGB=[1, 0, 0]
        )

        self.reset(seed)

    def reset(self, seed: None | int = None):
        """Resets the simulation.

        Args:
            seed (None | int): seed
        """
        self.resetSimulation()
        self.setGravity(0, 0, -9.81)
        self.steps = 0

        # reset the camera position to a sane place
        self.resetDebugVisualizerCamera(
            cameraDistance=5,
            cameraYaw=30,
            cameraPitch=-30,
            cameraTargetPosition=[0, 0, 1],
        )

        # define new RNG
        self.np_random = np.random.RandomState(seed=seed)

        # construct the world
        self.planeId = self.loadURDF(
            "plane.urdf", useFixedBase=True, globalScaling=self.worldScale
        )

        # spawn drones
        self.drones: list[DroneClass] = []
        for start_pos, start_orn, drone_type, drone_options in zip(
            self.start_pos,
            self.start_orn,
            self.drone_type,
            self.drone_options,
        ):
            self.drones.append(
                self.drone_type_mappings[drone_type](
                    self,
                    start_pos=start_pos,
                    start_orn=start_orn,
                    physics_hz=self.physics_hz,
                    np_random=self.np_random,
                    **drone_options,
                )
            )

        # constants for tracking how many times to step depending on control hz
        all_control_hz = [1.0 / drone.control_period for drone in self.drones]
        self.updates_per_step = int(self.physics_hz / np.min(all_control_hz))
        self.update_period = 1.0 / np.min(all_control_hz)
        self.now = time.time()

        # arm everything
        self.register_all_new_bodies()
        self.set_armed(True)

    def register_all_new_bodies(self):
        """Registers all new bodies in the environment to be able to handle collisions later.

        Call this when there is an update in the number of bodies in the environment.
        """
        # collision array
        self.collision_array = np.zeros(
            (self.getNumBodies(), self.getNumBodies()), dtype=bool
        )

    def state(self, index: DroneIndex) -> np.ndarray:
        """Returns the state for the indexed drone.

        Args:
            index (DRONE_INDEX): index

        Returns:
            np.ndarray: state
        """
        return self.drones[index].state

    def aux_state(self, index: DroneIndex) -> np.ndarray:
        """Returns the auxiliary state for the indexed drone.

        Args:
            index (DRONE_INDEX): index

        Returns:
            np.ndarray: auxiliary state
        """
        return self.drones[index].aux_state

    @property
    def all_states(self) -> list[np.ndarray]:
        """Returns a list of states for all drones in the environment.

        This function is not very optimized, if you want the state of a single drone, do `state(i)`.

        Returns:
            np.ndarray: list of states
        """
        states = []
        for drone in self.drones:
            states.append(drone.state)

        return states

    @property
    def all_aux_states(self) -> list[np.ndarray]:
        """Returns a list of auxiliary states for all drones in the environment.

        This function is not very optimized, if you want the aux state of a single drone, do `aux_state(i)`.

        Returns:
            np.ndarray: list of auxiliary states
        """
        aux_states = []
        for drone in self.drones:
            aux_states.append(drone.aux_state)

        return aux_states

    def print_all_bodies(self):
        """Debugging function used to print out all bodies in the environment along with their IDs."""
        bodies = dict()
        for i in range(self.getNumBodies()):
            bodies[i] = self.getBodyInfo(i)[-1].decode("UTF-8")

        from pprint import pprint

        pprint(bodies)

    def set_armed(self, settings: int | bool | list[int | bool]):
        """Sets the arming state of each drone in the environment.

        Args:
            settings (int | bool | list[int | bool]): arm setting
        """
        if isinstance(settings, list):
            assert len(settings) == len(
                self.drones
            ), f"Expected {len(self.drones)} settings, got {len(settings)}."
            self.armed_drones = [
                drone for (drone, arm) in zip(self.drones, settings) if arm
            ]
        else:
            self.armed_drones = [drone for drone in self.drones] if settings else []

    def set_mode(self, flight_modes: int | list[int]):
        """Sets the flight mode of each drone in the environment.

        Args:
            flight_modes (int | list[int]): flight mode
        """
        if isinstance(flight_modes, list):
            assert len(flight_modes) == len(
                self.drones
            ), f"Expected {len(self.drones)} flight_modes, got {len(flight_modes)}."
            for drone, mode in zip(self.drones, flight_modes):
                drone.set_mode(mode)
        else:
            for drone in self.drones:
                drone.set_mode(flight_modes)

    def set_setpoint(self, index: DroneIndex, setpoint: np.ndarray):
        """Sets the setpoint of one drone in the environment.

        Args:
            index (DRONE_INDEX): index
            setpoint (np.ndarray): setpoint
        """
        self.drones[index].setpoint = setpoint

    def set_all_setpoints(self, setpoints: np.ndarray):
        """Sets the setpoints of each drone in the environment.

        Args:
            setpoints (np.ndarray): list of setpoints
        """
        for i, drone in enumerate(self.drones):
            drone.setpoint = setpoints[i]

    def step(self):
        """Steps the environment, this automatically handles physics and control looprates, one step is equivalent to one control loop step."""
        # compute rtf if we're rendering
        if self.render:
            elapsed = time.time() - self.now
            self.now = time.time()

            # sleep to maintain real time factor
            time.sleep(max(0, self.update_period - elapsed))

            # calculate real time factor
            RTF = self.update_period / (elapsed + 1e-6)

            # handle case where sometimes elapsed becomes 0
            if elapsed != 0.0:
                self.rtf_debug_line = self.addUserDebugText(
                    text=f"RTF: {str(RTF)[:7]}",
                    textPosition=[0, 0, 0],
                    textColorRGB=[1, 0, 0],
                    replaceItemUniqueId=self.rtf_debug_line,
                )

        # reset collisions
        self.collision_array &= False

        # step the environment enough times for one control loop of the slowest controller
        physics_steps = 1
        while physics_steps <= self.updates_per_step:
            # update onboard avionics conditionally
            [
                drone.update_avionics()
                for drone in self.armed_drones
                if physics_steps % drone.physics_control_ratio == 0
            ]

            # compute physics
            [drone.update_physics() for drone in self.armed_drones]

            # advance pybullet
            self.stepSimulation()

            # splice out collisions
            for collision in self.getContactPoints():
                self.collision_array[collision[1], collision[2]] = True
                self.collision_array[collision[2], collision[1]] = True

            physics_steps += 1

        self.steps += 1
