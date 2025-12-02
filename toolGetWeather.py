from .models import Tool, ToolParameter

def get_warher(location: str) -> str:
    """Get the weather for a given location"""
    return f"The weather in {location} is sunny"

GET_WEATHER_TOOL = Tool(
    name="get_weather",
    description="Get the weather for a given location",
    parameters=[ToolParameter(name="location", type="string")],
)
