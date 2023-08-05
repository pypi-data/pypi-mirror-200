import logging
import math
from typing import List

import numpy as np
from palaestrai.agent import (
    ActuatorInformation,
    RewardInformation,
    SensorInformation,
)
from palaestrai.types import Box, Discrete

from .reward import Reward

LOG = logging.getLogger(__name__)


def gauss_norm(
    raw_value: float,
    mu: float = 1,
    sigma: float = 0.1,
    c: float = 0.5,
    a: float = -1,
):
    if not isinstance(raw_value, float):
        try:
            raw_value = sum(raw_value)
        except TypeError:
            return 0
    gaus_reward = a * math.exp(-((raw_value - mu) ** 2) / (2 * sigma**2)) - c
    return gaus_reward


class NoExtGridHealthReward(Reward):
    def __init__(self, **params):
        super().__init__(**params)
        self.grid_health_sensor = params.get(
            "grid_health", "Powergrid-0.Grid-0.health"
        )
        self.ext_grid_sensor = params.get(
            "ext_grid", "Powergrid-0.0-ext_grid-0.p_mw"
        )

    def __call__(self, state, *args, **kwargs):

        rewards = []
        for sensor in state:
            if self.grid_health_sensor == sensor.sensor_id:
                system_health_reward = RewardInformation(
                    sensor.sensor_value, Discrete(2), "grid_health_reward"
                )
                rewards.append(system_health_reward)
            elif self.ext_grid_sensor in sensor.sensor_id:
                reward = abs(sensor.sensor_value)
                external_grid_penalty_reward = RewardInformation(
                    reward, Discrete(1000), "external_grid_penalty_reward"
                )
                rewards.append(external_grid_penalty_reward)
        return rewards


class GridHealthReward(Reward):
    def _line_load(self, value):
        if not isinstance(value, int):
            return 0
        if value <= 100:
            return 0
        if value > 100 and value <= 120:
            return value - 100
        if value > 120:
            return np.exp((value - 100) / 10)

    def __call__(
        self, state: List[SensorInformation], *arg, **kwargs
    ) -> List[ActuatorInformation]:

        reward = 0
        for sensor in state:
            if "vm_pu" in sensor.sensor_id:
                reward += (gauss_norm(sensor(), 1, 0.02, 1.0, 2)) * 50
            if "line-" in sensor.sensor_id:
                reward -= self._line_load(sensor())
        final_reward = RewardInformation(
            reward, Box(-np.inf, np.inf, shape=(1,)), "grid_health_reward"
        )
        return [final_reward]


class ExtendedGridHealthReward(Reward):
    def __call__(
        self, state: List[SensorInformation], *args, **kwargs
    ) -> List[RewardInformation]:
        voltages = np.sort(
            np.array([s() for s in state if "vm_pu" in s.sensor_id]),
            axis=None,
        )
        voltage_rewards = [
            RewardInformation(
                voltages[0],
                Box(0.8, 1.2, shape=(1,)),
                reward_id="vm_pu-min",
            ),
            RewardInformation(
                voltages[-1],
                Box(0.8, 1.2, shape=(1,)),
                reward_id="vm_pu-max",
            ),
            RewardInformation(
                voltages[len(voltages) // 2],
                Box(0.8, 1.2, shape=(1,)),
                reward_id="vm_pu-median",
            ),
            RewardInformation(
                voltages.mean(),
                Box(0.8, 1.2, shape=(1,)),
                reward_id="vm_pu-mean",
            ),
            RewardInformation(
                voltages.std(),
                Box(0.8, 1.2, shape=(1,)),
                reward_id="vm_pu-std",
            ),
        ]

        lineloads = np.sort(
            np.array(
                [s() for s in state if ".loading_percent" in s.sensor_id]
            ),
            axis=None,
        )
        lineload_rewards = [
            RewardInformation(
                lineloads[0],
                Box(0.0, 100.0, shape=(1,)),
                reward_id="lineload-min",
            ),
            RewardInformation(
                lineloads[-1],
                Box(0.0, 100.0, shape=(1,)),
                reward_id="lineload-max",
            ),
            RewardInformation(
                lineloads[len(lineloads) // 2],
                Box(0.0, 100.0, shape=(1,)),
                reward_id="lineload-median",
            ),
            RewardInformation(
                lineloads.mean(),
                Box(0.0, 100.0, shape=(1,)),
                reward_id="lineload-mean",
            ),
            RewardInformation(
                lineloads.std(),
                Box(0.0, 100.0, shape=(1,)),
                reward_id="lineload-std",
            ),
        ]

        return voltage_rewards + lineload_rewards


class AllesDestroyAllPire2RewardIchWeissNicht(Reward):
    """This is a reward for classic ARL.

    Despite its unique name, this is a serious reward for the use
    with a constrainted power grid model from MIDAS.

    It checks all available power grid sensors and creates a score
    based on the *Technische Anschlussregeln Mittelspannung* (TAR-MS).

    Every component in a healthy state gives one point while each
    component that is out of its usual operation state gives ten minus
    points.

    Additionally, this reward includes everything from the
    :class:`ExtendedGridHealthReward` and can be used instead of that
    reward.

    """

    def __init__(
        self,
        reward_value: int = 1,
        small_penalty_value: int = 10,
        large_penalty_value: int = 100,
    ):
        self._reward_value: int = reward_value
        self._small_penalty_value: int = small_penalty_value
        self._large_penalty_value: int = large_penalty_value

    def __call__(
        self, state: List[SensorInformation], *args, **kwargs
    ) -> List[RewardInformation]:

        points = 0
        min_reward = 0
        max_reward = 0
        for s in state:
            if "Powergrid" not in s.sensor_id:
                continue

            if "in_service" in s.sensor_id:
                min_reward -= self._large_penalty_value
                max_reward += self._reward_value
                if s():
                    points += self._reward_value
                else:
                    points -= self._large_penalty_value

            if "loading_percent" in s.sensor_id:
                min_reward -= self._large_penalty_value
                max_reward += self._reward_value
                if s() < 95:
                    points += self._reward_value
                elif s() < 100:
                    points -= self._reward_value
                else:
                    points -= self._large_penalty_value

            if "vm_pu" in s.sensor_id:
                min_reward -= self._large_penalty_value
                max_reward += self._reward_value
                if 0.95 <= s() <= 1.05:
                    points += self._reward_value
                elif 0.9 <= s() <= 1.1:
                    points -= self._small_penalty_value
                else:
                    points -= self._large_penalty_value

        extgrid_rew = ExtendedGridHealthReward()
        rewards = extgrid_rew(state)

        rewards.append(
            RewardInformation(
                points,
                Box(min_reward, max_reward, (1,), np.int64),
                reward_id="ErikaReward",
            )
        )
        LOG.info(
            f"Reward ({self.__class__}) gives {points} points (RewardSpace=["
            f"{min_reward}, {max_reward}])"
        )
        return rewards


class RetroPsiReward(Reward):
    def __call__(
        self, state: List[SensorInformation], *args, **kwargs
    ) -> List[RewardInformation]:

        erika_rew = AllesDestroyAllPire2RewardIchWeissNicht()
        rewards = erika_rew(state)

        renewable_energy: float = 0.0
        fossil_energy: float = 0.0
        storage_usage: float = 0.0
        ext_grid_active_usage: float = 0.0
        ext_grid_reactive_usage: float = 0.0
        agent_bids: dict = {}

        for sensor in state:
            if (
                "Photovoltaic" in sensor.sensor_id
                or "Biogas" in sensor.sensor_id
            ) and "p_mw" in sensor.sensor_id:
                renewable_energy += sensor.sensor_value

            if "Diesel" in sensor.sensor_id and "p_mw" in sensor.sensor_id:
                fossil_energy += sensor.sensor_value

            if "Battery" in sensor.sensor_id and "p_mw" in sensor.sensor_id:
                storage_usage += sensor.sensor_value

            if "ext_grid" in sensor.sensor_id:
                if "p_mw" in sensor.sensor_id:
                    ext_grid_active_usage += sensor.sensor_value
                if "q_mvar" in sensor.sensor_id:
                    ext_grid_reactive_usage += sensor.sensor_value
            if "MarketAgentModel" in sensor.sensor_id:
                _, eid, attr = sensor.sensor_id.split(".")
                agent_bids.setdefault(eid, {})
                if "price" in attr:
                    agent_bids[eid]["price"] = sensor.sensor_value
                if "amount" in attr:
                    agent_bids[eid]["amount"] = sensor.sensor_value

        for eid, offer in agent_bids.items():
            rewards.append(
                RewardInformation(
                    offer["price"] * offer["amount"],
                    Box(-100, 100, (1,), np.double),
                    f"profit_{eid}",
                )
            )
            print(rewards[-1])

        # rewards.append(RewardInformation(sensor.sensor_value, Box(-100, 100, (1,), np.double), f"profit_{sensor.sensor_id.split('.')[1]}"))

        rewards.append(
            RewardInformation(
                renewable_energy,
                Box(0, 1000, (1,), np.float32),
                "renewable_energy",
            )
        )
        rewards.append(
            RewardInformation(
                fossil_energy, Box(0, 1000, (1,), np.float32), "fossil_energy"
            )
        )
        rewards.append(
            RewardInformation(
                ext_grid_active_usage,
                Box(-1000, 1000, (1,), np.float32),
                "ext_grid_active_usage",
            )
        )
        rewards.append(
            RewardInformation(
                ext_grid_reactive_usage,
                Box(-1000, 1000, (1,), np.float32),
                "ext_grid_reactive_usage",
            )
        )
        rewards.append(
            RewardInformation(
                storage_usage,
                Box(-1000, 1000, (1,), np.double),
                "storage_usage",
            )
        )

        return rewards
