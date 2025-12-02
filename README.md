cd /Volumes/jetdrive/git/iacuriman/mcp-bootstrap && cat > README.md << 'EOF'
# MCP Bootstrap 🚀

A simple, modular FastAPI server that implements the Model Context Protocol (MCP) for connecting AI models to external tools.

## Quick Start

Get your MCP server running and connected to Groq in 3 simple steps:

### 1️⃣ Start Your MCP Server

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

✅ Your server is now running at `http://localhost:8000`

### 2️⃣ Expose with Cloudflare Tunnel

```bash
# Install cloudflared (if needed)
brew install cloudflare/cloudflare/cloudflared

# Expose your server
cloudflared tunnel --url http://localhost:8000
```

✅ You'll get a public URL like: `https://abc123.trycloudflare.com`

### 3️⃣ Connect to Groq

1. Go to [Groq Playground](https://console.groq.com/playground)
2. Add your MCP server:
   - **Server Name**: `MCP Weather Server`
   - **Server URL**: `https://your-url.trycloudflare.com` (your Cloudflare URL)
3. Select a model with **FUNCTION CALLING / TOOL USE** support
4. Ask: "What's the weather in Murcia, Spain?"

![Groq MCP Setup](docs/groq-1.png)

## Architecture

```
┌─────────────┐
│   Your App  │
│  (FastAPI)  │
└──────┬──────┘
       │
       │ MCP Protocol
       │ (/tools/list, /tools/call)
       │
┌──────▼──────────┐
│ Cloudflare      │
│ Tunnel          │
│ (Public URL)    │
└──────┬──────────┘
       │
       │ HTTPS
       │
┌──────▼──────────┐
│   Groq API      │
│   (LLM)         │
└─────────────────┘
```

## What's Included

- ✅ **Weather Tool** - Real-time weather data via Open-Meteo API
- ✅ **MCP Protocol** - Full JSON-RPC 2.0 implementation
- ✅ **Modular Design** - Easy to add new tools
- ✅ **Groq Compatible** - Works seamlessly with Groq's MCP support

## Adding New Tools

See [docs/aux-add-tool.md](docs/aux-add-tool.md) for a complete guide on adding new tools.

## Documentation

- **[Setup Guide](docs/1-init-readme.md)** - Detailed installation and usage
- **[Tunneling](docs/2-tunneling-cloudflare_on_demand.md)** - Expose your server
- **[Groq Integration](docs/3-use-mcp-with-llm-on-groq.md)** - Connect to Groq

## Requirements

- Python 3.9+
- FastAPI
- Cloudflare Tunnel (for public access)

## License

Open source - feel free to use and modify!

---

**Ready to build?** Start with step 1 above and you'll be running in minutes! 🎉
EOF
