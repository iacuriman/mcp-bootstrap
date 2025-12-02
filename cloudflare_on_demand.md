# Cloudflare Tunnel - Expose MCP Server

## Install Cloudflare Tunnel

```bash
# macOS
brew install cloudflare/cloudflare/cloudflared

# Or download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
```

## Expose Your Server

**Make sure your MCP server is running first:**
```bash
uvicorn main:app --reload
```

**Then in a NEW terminal:**
```bash
cloudflared tunnel --url http://localhost:8000
```

✅ You'll get a URL like: `https://childrens-detail-highlight-gardening.trycloudflare.com`

## Test Your Public URL

### Test Discovery:
```bash
curl -X POST https://childrens-detail-highlight-gardening.trycloudflare.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "discovery"}'
```

### Test Weather for Murcia:
```bash
curl -X POST https://childrens-detail-highlight-gardening.trycloudflare.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"verb": "execute", "tool_name": "get_weather", "arguments": {"location": "Murcia"}}'
```

Done! 🎉

