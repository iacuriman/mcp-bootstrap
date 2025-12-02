# Adding a New Tool - Step by Step Guide

This guide explains how to add a new tool to the MCP Bootstrap application. The architecture is designed to be modular, making it easy to add new functionality.

## Overview

Each tool consists of:
1. **A Python function** that implements the tool's logic
2. **A Tool definition** that describes the tool's name, description, and parameters
3. **Registration** in the main application

## Step-by-Step Instructions

### Step 1: Create a New Tool File

Create a new Python file in the project root with a descriptive name, following the pattern `tool<Name>.py`.

**Example:** For a calculator tool, create `toolCalculator.py`

```python
from models import Tool, ToolParameter

def calculate(operation: str, a: float, b: float) -> str:
    """Perform a basic calculation"""
    try:
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return "Error: Division by zero"
            result = a / b
        else:
            return f"Error: Unknown operation '{operation}'. Use: add, subtract, multiply, divide"
        
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

CALCULATOR_TOOL = Tool(
    name="calculate",
    description="Perform basic mathematical calculations (add, subtract, multiply, divide)",
    parameters=[
        ToolParameter(name="operation", type="string"),
        ToolParameter(name="a", type="number"),
        ToolParameter(name="b", type="number"),
    ],
)
```

### Step 2: Import the Tool in main.py

Open `main.py` and add the import statement at the top:

```python
from toolCalculator import CALCULATOR_TOOL, calculate
```

**Note:** If you have multiple tools, you can import them all:

```python
from models import ModelContextRequest, ModelContextResponse
from toolGetWeather import GET_WEATHER_TOOL, get_weather
from toolCalculator import CALCULATOR_TOOL, calculate
```

### Step 3: Register the Tool Function

Add your tool function to the `tool_registry` dictionary in `main.py`:

```python
tool_registry = {
    "get_weather": get_weather,
    "calculate": calculate,  # Add your new tool here
}
```

### Step 4: Register the Tool Definition

Update the discovery response to include your tool's definition. Modify the `discovery` branch in the handler:

```python
@app.post("/mcp", response_model=ModelContextResponse)
async def mcp_request_handler(request: ModelContextRequest):
    if request.verb == "discovery":
        return ModelContextResponse(tools=[GET_WEATHER_TOOL, CALCULATOR_TOOL])  # Add your tool here
    # ... rest of the code
```

## Complete Example

Here's what your `main.py` should look like after adding a calculator tool:

```python
from fastapi import FastAPI, HTTPException

from models import ModelContextRequest, ModelContextResponse
from toolGetWeather import GET_WEATHER_TOOL, get_weather
from toolCalculator import CALCULATOR_TOOL, calculate

app = FastAPI()

tool_registry = {
    "get_weather": get_weather,
    "calculate": calculate,
}

@app.post("/mcp", response_model=ModelContextResponse)
async def mcp_request_handler(request: ModelContextRequest):
    if request.verb == "discovery":
        return ModelContextResponse(tools=[GET_WEATHER_TOOL, CALCULATOR_TOOL])
    elif request.verb == "execute":
        try:
            tool_function = tool_registry.get(request.tool_name)
            arguments = request.arguments or {}
            result = tool_function(**arguments)
            return ModelContextResponse(result=result)

        except KeyError:
            raise HTTPException(status_code=400, detail=f"Tool {request.tool_name} not found")

    raise HTTPException(status_code=400, detail=f"Invalid verb: {request.verb}")
```

## Testing Your New Tool

### 1. Test Discovery

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "discovery"}'
```

You should see your new tool in the response.

### 2. Test Execution

```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "execute", "tool_name": "calculate", "arguments": {"operation": "add", "a": 10, "b": 5}}'
```

## Tool Function Guidelines

### Function Signature

Your tool function should:
- Accept parameters that match the `ToolParameter` definitions
- Return a string (or any JSON-serializable value)
- Handle errors gracefully

### Parameter Types

Supported parameter types in `ToolParameter`:
- `"string"` - Text values
- `"number"` - Numeric values (integers or floats)
- `"boolean"` - True/false values
- `"array"` - Lists of values
- `"object"` - Nested objects

### Error Handling

Always include error handling in your tool functions:

```python
def my_tool(param1: str, param2: int) -> str:
    """My tool description"""
    try:
        # Your tool logic here
        result = do_something(param1, param2)
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

## Advanced Examples

### Example 1: Tool with Multiple Parameters

```python
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""
    # Implementation here
    return f"Email sent to {to}"

EMAIL_TOOL = Tool(
    name="send_email",
    description="Send an email to a recipient",
    parameters=[
        ToolParameter(name="to", type="string"),
        ToolParameter(name="subject", type="string"),
        ToolParameter(name="body", type="string"),
    ],
)
```

### Example 2: Tool Using External APIs

```python
import requests

def get_stock_price(symbol: str) -> str:
    """Get current stock price"""
    try:
        # Example API call (replace with actual API)
        response = requests.get(f"https://api.example.com/stock/{symbol}")
        data = response.json()
        return f"Stock {symbol}: ${data['price']}"
    except Exception as e:
        return f"Error: {str(e)}"

STOCK_TOOL = Tool(
    name="get_stock_price",
    description="Get the current stock price for a symbol",
    parameters=[ToolParameter(name="symbol", type="string")],
)
```

### Example 3: Tool with Optional Parameters

```python
def search(query: str, limit: int = 10) -> str:
    """Search with optional limit"""
    # limit has a default value, so it's optional
    results = perform_search(query, limit)
    return f"Found {len(results)} results"

SEARCH_TOOL = Tool(
    name="search",
    description="Search with optional result limit",
    parameters=[
        ToolParameter(name="query", type="string"),
        ToolParameter(name="limit", type="number"),  # Optional in function, but still defined
    ],
)
```

## Best Practices

1. **Naming Convention**: Use descriptive names for tool files (`tool<Name>.py`) and functions
2. **Documentation**: Always include docstrings in your tool functions
3. **Error Handling**: Always wrap your logic in try-except blocks
4. **Type Hints**: Use Python type hints for better code clarity
5. **Parameter Validation**: Validate inputs in your tool functions
6. **Return Values**: Return meaningful, user-friendly messages

## Troubleshooting

### Tool Not Appearing in Discovery

- Check that you imported the tool definition in `main.py`
- Verify the tool is included in the `tools` list in the discovery response
- Restart the server if auto-reload didn't work

### Tool Execution Fails

- Check that the function name matches the tool name in the registry
- Verify parameter names match between the Tool definition and function signature
- Check the server logs for error messages
- Ensure your function handles all edge cases

### Import Errors

- Make sure your tool file is in the project root directory
- Verify the import statement matches the filename
- Check that all dependencies are installed

## Next Steps

Once you've added your tool:
1. Test it thoroughly with various inputs
2. Update the main README if your tool is a core feature
3. Consider adding unit tests for your tool function
4. Document any special requirements or API keys needed

## Summary Checklist

- [ ] Create `tool<Name>.py` file with function and Tool definition
- [ ] Import tool in `main.py`
- [ ] Add function to `tool_registry` dictionary
- [ ] Add Tool definition to discovery response
- [ ] Test discovery endpoint
- [ ] Test execution endpoint
- [ ] Handle errors appropriately
- [ ] Document any special requirements

That's it! Your new tool is now integrated into the MCP Bootstrap application.

