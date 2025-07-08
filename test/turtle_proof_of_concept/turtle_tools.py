# turtle_tools.py
# This file defines the tools the agent can use to control the turtle.

import turtle
from smolagents import tool

# --- Turtle and Screen Setup ---
# We initialize the turtle and screen here so that all tool functions
# can access the same turtle instance.
try:
    screen = turtle.Screen()
    screen.title("Agent-Controlled Turtle")
    t = turtle.Turtle()
    t.shape("turtle") # Give our turtle a nice turtle shape
except turtle.Terminator:
    # This handles re-running the script in some environments (like notebooks)
    # where the turtle screen might not have been properly closed.
    turtle.TurtleScreen._RUNNING = True
    screen = turtle.Screen()
    screen.title("Agent-Controlled Turtle")
    t = turtle.Turtle()
    t.shape("turtle")


# --- Tool Definitions ---
# The @tool decorator makes these Python functions available to the agent.

@tool
def move_forward(distance: int) -> str:
    """
    Moves the turtle forward by a given distance in pixels.

    Args:
        distance (int): The number of pixels to move forward.
    """
    t.forward(distance)
    print(f"Turtle moved forward by {distance} pixels.")
    return f"Moved forward by {distance} pixels."

@tool
def turn(angle: int) -> str:
    """
    Turns the turtle by a given angle in degrees.
    Positive angles for left turns, negative for right turns.

    Args:
        angle (int): The angle in degrees to turn.
    """
    t.left(angle)
    print(f"Turtle turned by {angle} degrees.")
    return f"Turned by {angle} degrees."

@tool
def draw_circle(radius: int) -> str:
    """
    Draws a circle with a given radius.

    Args:
        radius (int): The radius of the circle.
    """
    t.circle(radius)
    print(f"Turtle drew a circle with a radius of {radius}.")
    return f"Drew a circle with a radius of {radius}."

@tool
def change_pen_color(color: str) -> str:
    """
    Changes the pen color for drawing.

    Args:
        color (str): A valid color name (e.g., 'red', 'blue', 'green').
    """
    try:
        t.pencolor(color)
        print(f"Pen color changed to {color}.")
        return f"Pen color changed to {color}."
    except turtle.TurtleGraphicsError:
        error_message = f"Error: '{color}' is not a valid color."
        print(error_message)
        return error_message

@tool
def pen_up() -> str:
    """
    Lifts the turtle's pen, so it does not draw when moving.
    """
    t.penup()
    print("Pen lifted up.")
    return "Pen is now up."

@tool
def pen_down() -> str:
    """
    Lowers the turtle's pen, so it draws when moving.
    """
    t.pendown()
    print("Pen lowered down.")
    return "Pen is now down."
