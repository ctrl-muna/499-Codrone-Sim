# sdk/client/range_sensor.py

#
# Provides get_front_range() and get_bottom_range() for a connected UserControl
# instance. Subscribes to the distance-sensor topics registered in the active
# robot config (sdk/client/sim_config/robot_quadrotor_fastphysics.jsonc).
#
# Sensor IDs in the robot config:
#   FrontRange  - forward-facing distance sensor (max 50 m)
#   BottomRange - downward-facing distance sensor (max 20 m)
#
# Public API:
#   get_front_range(controller, timeout_s)  -> float | None  (metres)
#   get_bottom_range(controller, timeout_s) -> float | None  (metres)
#
# Both functions return the distance in metres, or None if no reading arrives
# within timeout_s seconds.  Callers can convert to centimetres by multiplying
# by 100.

import asyncio

FRONT_SENSOR_ID = "FrontRange"
BOTTOM_SENSOR_ID = "BottomRange"
SENSOR_TOPIC_KEY = "distance_sensor"


def _subscribe_range(controller, sensor_id):
    """
    Subscribe to a distance-sensor topic on the connected controller.

    Returns a list that will be populated with the latest distance reading
    (in metres) as a single float element once a message arrives.

    Args:
        controller (UserControl): A connected UserControl instance.
        sensor_id  (str):         Sensor ID from the robot config.

    Returns:
        list: Mutable container; result[0] will be set to the distance float.
    """
    result = []

    def _on_reading(_, data):
        # The distance_sensor payload contains a "distance" field in metres.
        distance_m = data.get("distance", None)
        if distance_m is not None and not result:
            result.append(float(distance_m))

    topic = controller.drone.sensors[sensor_id][SENSOR_TOPIC_KEY]
    controller.client.subscribe(topic, _on_reading)
    return result


async def get_front_range(controller, timeout_s=1.0):
    """
    Read the front-facing distance sensor and return the distance in metres.

    Subscribes to the FrontRange sensor topic, waits up to timeout_s seconds
    for the first reading, then returns it.

    Args:
        controller (UserControl): A connected UserControl instance.
        timeout_s  (float):       Maximum seconds to wait for a reading.

    Returns:
        float: Distance in metres, or None if no reading arrived in time.
    """
    result = _subscribe_range(controller, FRONT_SENSOR_ID)
    elapsed = 0.0
    interval = 0.05
    while not result and elapsed < timeout_s:
        await asyncio.sleep(interval)
        elapsed += interval
    return result[0] if result else None


async def get_bottom_range(controller, timeout_s=1.0):
    """
    Read the downward-facing distance sensor and return the distance in metres.

    Subscribes to the BottomRange sensor topic, waits up to timeout_s seconds
    for the first reading, then returns it.

    Args:
        controller (UserControl): A connected UserControl instance.
        timeout_s  (float):       Maximum seconds to wait for a reading.

    Returns:
        float: Distance in metres, or None if no reading arrived in time.
    """
    result = _subscribe_range(controller, BOTTOM_SENSOR_ID)
    elapsed = 0.0
    interval = 0.05
    while not result and elapsed < timeout_s:
        await asyncio.sleep(interval)
        elapsed += interval
    return result[0] if result else None
