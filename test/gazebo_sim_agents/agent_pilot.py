# agent_pilot.py
# The main script that runs the agent and its tools to control the simulated drone.

import asyncio
import threading
from smolagents import CodeAgent
from smolagents.models import OpenAIServerModel
from smolagents.tools import tool

from drone_interface import DroneInterface

# --- Create a single instance of our drone interface ---
drone_ctrl = DroneInterface()

# --- Dedicated asyncio thread setup ---
def run_async_loop(loop):
    """Function to run the asyncio event loop in a background thread."""
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop = asyncio.new_event_loop()
async_thread = threading.Thread(target=run_async_loop, args=(loop,), daemon=True)
async_thread.start()


# --- NEW, MORE RESTRICTIVE SYSTEM INSTRUCTIONS ---
SYSTEM_INSTRUCTIONS = """
You are an expert drone pilot AI. Your goal is to respond to the user's command by generating a SINGLE line of Python code to call the appropriate tool.
You MUST NOT generate more than one line of code.
You MUST NOT generate any 'if' statements, loops, or other complex logic.
You MUST wrap your single line of code in `<code>...</code>` tags.

Correct example for the command "take off":
Thought: The user wants to take off. I will use the arm_and_takeoff tool.
<code>
print(arm_and_takeoff())
</code>
"""

# --- Tool Definitions ---
# These are SYNCHRONOUS, but submit their async logic to the background thread.
def run_async_tool(coro):
    """Helper function to run a coroutine on the background loop and get the result."""
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result()

@tool
def connect_to_drone() -> str:
    """Connects to the drone simulator. Call this first."""
    return run_async_tool(drone_ctrl.connect())

@tool
def arm_and_takeoff() -> str:
    """Arms the drone and then immediately commands it to take off. This is the standard procedure."""
    print("--- Arming and Taking Off ---")
    # We now run the two async functions sequentially inside the tool
    is_armed = run_async_tool(drone_ctrl.arm())
    if not is_armed:
        return "Arming failed. Cannot take off."
    
    is_airborne = run_async_tool(drone_ctrl.takeoff())
    return "Takeoff sequence initiated successfully." if is_airborne else "Takeoff failed after arming."


@tool
def land_drone() -> str:
    """Commands the drone to land."""
    return run_async_tool(drone_ctrl.land())

@tool
def get_drone_telemetry() -> str:
    """Gets the current position, altitude, and heading of the drone."""
    data = run_async_tool(drone_ctrl.get_telemetry())
    return str(data) if data else "Could not retrieve telemetry."


class DronePilotAgent:
    def __init__(self):
        print("--- Initializing Drone Pilot Agent...")
        ollama_model = OpenAIServerModel(
            model_id="mistral",
            api_base="http://192.168.64.1:11434/v1",
            api_key="ollama"
        )
        # --- UPDATED TOOL LIST ---
        self.agent = CodeAgent(
            tools=[
                connect_to_drone,
                arm_and_takeoff, # Replaced arm_drone and takeoff_drone
                land_drone,
                get_drone_telemetry
            ],
            model=ollama_model
        )

    def run_prompt(self, prompt: str):
        full_prompt = f"{SYSTEM_INSTRUCTIONS}\n\nUser command: {prompt}"
        print(f"--- Sending prompt to agent ---")
        self.agent.run(full_prompt, max_steps=1)
        print("--- Agent finished turn. Waiting for next command. ---")

def main():
    pilot = DronePilotAgent()
    print("\n--- Drone Pilot Agent is Ready! ---")
    print("Ensure the Gazebo simulation is running in a separate terminal.")
    print("Your new command sequence is: 'connect to the drone', then 'take off'.")
    print("Type 'quit' or 'exit' to close.\n")

    try:
        while True:
            try:
                prompt = input("You: ")
                if prompt.lower() in ["quit", "exit"]:
                    break
                pilot.run_prompt(prompt)
            except (KeyboardInterrupt, EOFError):
                break
    finally:
        print("\n--- Shutting down agent and closing event loop. ---")
        loop.call_soon_threadsafe(loop.stop)
        async_thread.join()

if __name__ == "__main__":
    main()
