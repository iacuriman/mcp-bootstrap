from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
import json

from models import ModelContextRequest, ModelContextResponse
from toolGetWeather import GET_WEATHER_TOOL, get_weather

app = FastAPI()

tool_registry = {
    "get_weather": get_weather,
}

# Root endpoint - handle initial connection/discovery
@app.get("/")
async def root():
    """Root endpoint - returns server info"""
    return {
        "name": "mcp-bootstrap",
        "version": "1.0.0",
        "protocol": "mcp",
        "endpoints": {
            "initialize": "/initialize",
            "tools/list": "/tools/list",
            "tools/call": "/tools/call"
        }
    }

@app.post("/")
async def root_post(request: Request):
    """Handle POST to root - might be MCP discovery or JSON-RPC calls"""
    try:
        body = await request.json()
        method = body.get("method")
        
        # Route JSON-RPC requests to appropriate handlers
        if method == "initialize":
            return await mcp_initialize(request)
        elif method == "tools/list":
            return await mcp_tools_list(request)
        elif method == "tools/call":
            return await mcp_tools_call(request)
    except:
        pass
    # Return server info
    return await root()

# MCP Protocol endpoints - JSON-RPC 2.0 format
@app.post("/initialize")
@app.get("/initialize")
async def mcp_initialize(request: Request):
    """MCP initialize endpoint - JSON-RPC 2.0 format"""
    request_id = None
    try:
        body = await request.json()
        request_id = body.get("id") if "id" in body else None
        # Handle JSON-RPC 2.0 format
        if "method" in body and body["method"] == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "mcp-bootstrap",
                        "version": "1.0.0"
                    }
                }
            }
            return JSONResponse(content=response)
    except:
        pass
    
    # Always return JSON-RPC 2.0 format for Groq compatibility
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "mcp-bootstrap",
                "version": "1.0.0"
            }
        }
    }
    return JSONResponse(content=response)

@app.post("/tools/list")
async def mcp_tools_list(request: Request):
    """List available tools - MCP protocol JSON-RPC 2.0"""
    request_id = None
    try:
        body = await request.json()
        request_id = body.get("id") if "id" in body else None
    except:
        pass
    
    # Build tools list
    tools = [
        {
            "name": tool.name,
            "description": tool.description,
            "inputSchema": {
                "type": "object",
                "properties": {
                    param.name: {"type": param.type}
                    for param in tool.parameters
                },
                "required": [param.name for param in tool.parameters]
            }
        }
        for tool in [GET_WEATHER_TOOL]
    ]
    
    # Always return JSON-RPC 2.0 format for Groq compatibility
    response = {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": tools
        }
    }
    return JSONResponse(content=response)

@app.post("/tools/call")
async def mcp_tools_call(request: Request):
    """Call a tool - MCP protocol JSON-RPC 2.0"""
    try:
        body = await request.json()
        request_id = body.get("id") if "id" in body else None
        
        # Handle JSON-RPC 2.0 format
        if "method" in body and body["method"] == "tools/call":
            params = body.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
        else:
            # Direct format
            tool_name = body.get("name")
            arguments = body.get("arguments", {})
        
        if tool_name not in tool_registry:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Tool {tool_name} not found"
                }
            }
        
        try:
            tool_function = tool_registry[tool_name]
            result = tool_function(**arguments)
            
            response = {
                "content": [
                    {
                        "type": "text",
                        "text": str(result)
                    }
                ]
            }
            
            # Always return JSON-RPC 2.0 format for Groq compatibility
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": response
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Error executing tool: {str(e)}"
                }
            }
    except json.JSONDecodeError:
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32700,
                "message": "Parse error"
            }
        }
    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}"
            }
        }

# MCP endpoint - handle both JSON-RPC and legacy format
@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP endpoint - handles JSON-RPC 2.0 and legacy format"""
    try:
        body = await request.json()
        
        # Check if it's JSON-RPC 2.0 format
        if "jsonrpc" in body and "method" in body:
            method = body["method"]
            params = body.get("params", {})
            
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "mcp-bootstrap",
                            "version": "1.0.0"
                        }
                    }
                }
            
            elif method == "tools/list":
                tools = [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                param.name: {"type": param.type}
                                for param in tool.parameters
                            },
                            "required": [param.name for param in tool.parameters]
                        }
                    }
                    for tool in [GET_WEATHER_TOOL]
                ]
                return {
                    "jsonrpc": "2.0",
                    "id": body.get("id"),
                    "result": {
                        "tools": tools
                    }
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                if tool_name not in tool_registry:
                    return {
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "error": {
                            "code": -32601,
                            "message": f"Tool {tool_name} not found"
                        }
                    }
                
                try:
                    tool_function = tool_registry[tool_name]
                    result = tool_function(**arguments)
                    
                    return {
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": str(result)
                                }
                            ]
                        }
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": body.get("id"),
                        "error": {
                            "code": -32603,
                            "message": f"Error executing tool: {str(e)}"
                        }
                    }
        
        # Legacy format (verb-based)
        if "verb" in body:
            if body["verb"] == "discovery":
                return ModelContextResponse(tools=[GET_WEATHER_TOOL])
            elif body["verb"] == "execute":
                tool_name = body.get("tool_name")
                arguments = body.get("arguments", {})
                
                if tool_name not in tool_registry:
                    raise HTTPException(status_code=400, detail=f"Tool {tool_name} not found")
                
                tool_function = tool_registry[tool_name]
                result = tool_function(**arguments)
                return ModelContextResponse(result=result)
            
            raise HTTPException(status_code=400, detail=f"Invalid verb: {body['verb']}")
        
        # If we get here, the format is unknown
        raise HTTPException(status_code=422, detail="Invalid request format")
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Also add endpoints under /mcp/ path for Groq
@app.post("/mcp/initialize")
async def mcp_initialize_alt(request: Request):
    return await mcp_initialize(request)

@app.post("/mcp/tools/list")
async def mcp_tools_list_alt(request: Request):
    return await mcp_tools_list(request)

@app.post("/mcp/tools/call")
async def mcp_tools_call_alt(request: Request):
    return await mcp_tools_call(request)