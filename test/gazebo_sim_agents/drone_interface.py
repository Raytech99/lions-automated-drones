# drone_interface.py
# This class handles all low-level communication with the drone using MAVSDK.

import asyncio
from mavsdk import System

class DroneInterface:
    """A wrapper class for MAVSDK to simplify drone control."""
    def __init__(self):
        self.drone = System()
        self.is_connected = False

    async def connect(self):
        """
        Connects to the simulated drone.
        """
        print("--- Connecting to drone...")
        await self.drone.connect(system_address="udp://:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("--- Drone connected!")
                self.is_connected = True
                return True
        return False

    async def arm(self):
        """
        Arms the drone.
        """
        if not self.is_connected:
            print("--- Drone not connected. Cannot arm.")
            return False
        print("--- Arming drone...")
        await self.drone.action.arm()
        return True

    async def takeoff(self):
        """
        Takes off to a default altitude.
        """
        if not self.is_connected:
            print("--- Drone not connected. Cannot take off.")
            return False
        print("--- Taking off...")
        await self.drone.action.takeoff()
        await asyncio.sleep(5) # Wait for takeoff to complete
        return True

    async def land(self):
        """
        Lands the drone.
        """
        if not self.is_connected:
            print("--- Drone not connected. Cannot land.")
            return False
        print("--- Landing...")
        await self.drone.action.land()
        return True

    async def goto_location(self, latitude_deg, longitude_deg, altitude_m, yaw_deg):
        """
        Commands the drone to fly to a specific GPS location.

        Args:
            latitude_deg (float): Target latitude.
            longitude_deg (float): Target longitude.
            altitude_m (float): Target altitude in meters.
            yaw_deg (float): Target yaw angle in degrees.
        """
        if not self.is_connected:
            print("--- Drone not connected. Cannot go to location.")
            return False
        print(f"--- Flying to {latitude_deg}, {longitude_deg} at {altitude_m}m...")
        await self.drone.action.goto_location(latitude_deg, longitude_deg, altitude_m, yaw_deg)
        return True

    async def get_telemetry(self):
        """
        Gets the current telemetry data from the drone.

        Returns:
            A dictionary with telemetry data or None if not available.
        """
        if not self.is_connected:
            print("--- Drone not connected. Cannot get telemetry.")
            return None
            
        try:
            # Get the first available telemetry data
            position = await anext(self.drone.telemetry.position())
            heading = await anext(self.drone.telemetry.heading())
            is_in_air = await anext(self.drone.telemetry.in_air())

            telemetry_data = {
                "latitude_deg": position.latitude_deg,
                "longitude_deg": position.longitude_deg,
                "absolute_altitude_m": position.absolute_altitude_m,
                "relative_altitude_m": position.relative_altitude_m,
                "heading_deg": heading.heading_deg,
                "is_in_air": is_in_air
            }
            return telemetry_data
        except Exception as e:
            print(f"--- Error getting telemetry: {e}")
            return None

# Helper to fix a common issue with anext in some environments
async def anext(ait):
    return await ait.__anext__()
