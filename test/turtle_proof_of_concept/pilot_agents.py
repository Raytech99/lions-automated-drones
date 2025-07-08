# pilot_agents.py (Final Fix: Converted to a synchronous script)

import turtle
from smolagents import CodeAgent
# We need to import the model class to connect to our local server
from smolagents.models import OpenAIServerModel

# Import all the functions we defined as tools.
from turtle_tools import (
    move_forward,
    turn,
    draw_circle,
    change_pen_color,
    pen_up,
    pen_down
)

# --- System Instructions ---
# This version is updated to be extremely specific about the output format.
SYSTEM_INSTRUCTIONS = """
You are an AI assistant that controls a turtle on a screen.
You have access to a set of tools. You MUST call these tools directly by their function name.
You MUST wrap any code you generate in `<code>...</code>` tags.

For example, to move the turtle forward by 100 pixels, your response must look like this:
Thought: I need to move the turtle forward.
<code>
move_forward(100)
</code>
"""

class TurtleAgent:
    def __init__(self):
        """
        Initializes the TurtleAgent, setting up the model and the CodeAgent.
        """
        print("Initializing Turtle Agent...")
        
        # --- Correct Model Configuration ---
        # 1. First, create a model object that points to your local Ollama server.
        ollama_model = OpenAIServerModel(
            model_id="mistral",                         # The model name you use in Ollama
            api_base="http://localhost:11434/v1",       # The full Ollama OpenAI-compatible endpoint
            api_key="ollama"                            # A dummy API key is required
        )

        # 2. Now, create the CodeAgent and pass the configured model object to it.
        self.agent = CodeAgent(
            tools=[
                move_forward,
                turn,
                draw_circle,
                change_pen_color,
                pen_up,
                pen_down
            ],
            model=ollama_model
        )

    def run_prompt(self, prompt: str):
        """
        Runs a single prompt through the agent. This is now a regular function.
        
        Args:
            prompt (str): The user's command for the agent.
        """
        # We combine our instructions with the user's prompt to guide the agent.
        full_prompt = f"{SYSTEM_INSTRUCTIONS}\n\nUser command: {prompt}"
        
        # We add max_steps=1 to force the agent to stop after one action.
        # Note: We are no longer using 'await'.
        print(f"--- Sending prompt to agent (max_steps=1) ---")
        self.agent.run(full_prompt, max_steps=1)
        print("--- Agent finished turn. Waiting for next command. ---")


def main():
    """
    Main function to run the interactive chat loop. This is now a regular function.
    """
    # Create an instance of our new agent class.
    my_turtle_agent = TurtleAgent()

    print("\n--- Turtle Agent is Ready! (Class-based) ---")
    print("A turtle graphics window should have opened.")
    print("Type your commands below and press Enter.")
    print("Type 'quit' or 'exit' to close the program.\n")

    # Interactive Chat Loop
    while True:
        try:
            prompt = input("You: ")
            if prompt.lower() in ["quit", "exit"]:
                print("Exiting...")
                break
            
            # Call the run method on our agent instance.
            my_turtle_agent.run_prompt(prompt)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

    print("\nAll done! Click the turtle window to close it.")
    try:
        turtle.done()
    except turtle.Terminator:
        pass

if __name__ == "__main__":
    # We now call main() directly, without asyncio.
    main()
