from fastapi import FastAPI, HTTPException
app = FastAPI()

@app.post("/mcp")
async def mcp_request_handler(request: Request):
    pass