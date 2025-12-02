from fastapi import FastAPI, HTTPException

from models import ModelContextRequest, ModelContextResponse
app = FastAPI()

@app.post("/mcp")
async def mcp_request_handler(request: Request):
    if request.verb == "discovery":
        return ModelContextResponse(tools=[GET_WEATHER_TOOL])
    
    pass