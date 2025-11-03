# 🌌 Space & Astronomy MCP Server

A comprehensive Model Context Protocol (MCP) server that brings the cosmos to your AI! Integrate NASA data, ISS tracking, Mars rover photos, asteroid monitoring, and space launch schedules directly into Claude and other MCP-compatible applications.

## ✨ Features

This server provides 6 powerful tools for space exploration:

### 🔭 NASA APIs
- **`space_get_apod`** - Astronomy Picture of the Day with expert explanations
- **`space_get_mars_photos`** - Photos from Curiosity, Opportunity, Spirit, and Perseverance rovers
- **`space_track_asteroids`** - Near-Earth Object tracking including potentially hazardous asteroids

### 🛰️ Real-Time Tracking
- **`space_track_iss`** - Live International Space Station location, altitude, and velocity

### 🚀 Launch Information
- **`space_get_launches`** - Upcoming rocket launches worldwide from all agencies

### 📊 Response Formats
- **Markdown** - Beautiful, human-readable formatted output (default)
- **JSON** - Structured data for programmatic processing

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Make the server executable:**
```bash
chmod +x space_mcp.py
```

3. **Test the server:**
```bash
python space_mcp.py --help
```

### Configuration for Claude Desktop

Add this to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "space": {
      "command": "python",
      "args": ["/absolute/path/to/space_mcp.py"]
    }
  }
}
```

Replace `/absolute/path/to/` with the actual path to your `space_mcp.py` file.

## 📚 Tool Documentation

### space_get_apod
Get NASA's Astronomy Picture of the Day with scientific explanations.

**Parameters:**
- `date` (optional): Date in YYYY-MM-DD format (defaults to today)
- `response_format` (optional): "markdown" or "json"

**Example prompts:**
- "Show me today's astronomy picture"
- "What was the APOD on June 16, 1995?" (First ever APOD!)
- "Get the astronomy picture from December 25, 2024"

### space_get_mars_photos
Retrieve photos from NASA's Mars rovers.

**Parameters:**
- `rover`: "curiosity", "opportunity", "spirit", or "perseverance"
- `sol` (optional): Martian day number
- `earth_date` (optional): Earth date in YYYY-MM-DD format
- `camera` (optional): Camera filter (FHAZ, RHAZ, MAST, NAVCAM, etc.)
- `limit` (optional): Max photos (1-100, default: 25)
- `response_format` (optional): "markdown" or "json"

**Example prompts:**
- "Show me recent photos from the Curiosity rover"
- "Get Perseverance photos from sol 500"
- "Show me Curiosity's front hazard camera photos from 2024-01-15"
- "Get navigation camera photos from Spirit"

### space_track_asteroids
Track Near-Earth Objects including potentially hazardous asteroids.

**Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD (defaults to today)
- `end_date` (optional): End date in YYYY-MM-DD (defaults to +7 days)
- `limit` (optional): Max asteroids (1-100, default: 20)
- `response_format` (optional): "markdown" or "json"

**Example prompts:**
- "Are there any asteroids passing close to Earth this week?"
- "Show me potentially hazardous asteroids approaching Earth"
- "Track NEOs from December 1-7, 2024"
- "What asteroids are closest to Earth right now?"

### space_track_iss
Get real-time International Space Station location and tracking data.

**Parameters:**
- `response_format` (optional): "markdown" or "json"

**Example prompts:**
- "Where is the ISS right now?"
- "Track the International Space Station"
- "Show me the current ISS location"
- "What's the ISS altitude and velocity?"

### space_get_launches
Get upcoming space launches from around the world.

**Parameters:**
- `limit` (optional): Max launches (1-50, default: 10)
- `search` (optional): Filter by agency, rocket, or mission name
- `response_format` (optional): "markdown" or "json"

**Example prompts:**
- "Show me upcoming SpaceX launches"
- "What are the next rocket launches?"
- "When is the next Falcon 9 launch?"
- "Show me upcoming missions to the ISS"
- "List all launches scheduled this month"

## 💡 Example Conversations

### Educational Exploration
**User:** "Show me today's astronomy picture and tell me about the Curiosity rover's recent photos"

**Claude:** *Retrieves APOD and recent Curiosity photos, providing rich explanations*

### Space Event Planning
**User:** "Are there any SpaceX launches this week that I can watch? Also, when will the ISS pass over my area?"

**Claude:** *Lists upcoming SpaceX launches with webcast info and provides current ISS tracking*

### Asteroid Monitoring
**User:** "Are there any potentially hazardous asteroids approaching Earth? How close and how big are they?"

**Claude:** *Tracks NEOs, shows hazard status, sizes, velocities, and miss distances*

### Mars Research
**User:** "Show me panoramic camera photos from the Spirit rover from its first week on Mars"

**Claude:** *Retrieves Spirit PANCAM photos with mission context*

## 🔧 Technical Details

### API Sources
- **NASA APIs**: Using NASA's official public APIs (APOD, Mars Rovers, NeoWs)
- **ISS Tracking**: wheretheiss.at API for real-time ISS data
- **Launch Data**: The Space Devs Launch Library 2 API

### Rate Limits
- NASA APIs: Uses DEMO_KEY (limited to 30 requests/hour, 50 requests/day)
- ISS Tracking: ~1 request per second
- Launch Library 2: Development API (no authentication required for testing)

### Character Limits
- Responses are limited to 25,000 characters to prevent context window overflow
- Truncation includes helpful guidance on filtering results

### Error Handling
- Graceful handling of API failures with clear error messages
- Timeout protection (30 second timeout)
- Helpful suggestions when no data matches criteria

## 🛠️ Development

### Project Structure
```
space_mcp.py          # Main MCP server implementation
requirements.txt      # Python dependencies
README.md            # This file
evaluations.xml      # Evaluation questions for testing
```

### Code Quality
- ✅ Full type hints throughout
- ✅ Pydantic v2 models for input validation
- ✅ Async/await for all I/O operations
- ✅ Comprehensive docstrings
- ✅ Tool annotations (readOnlyHint, etc.)
- ✅ Character limit protection
- ✅ Error handling with actionable messages

### Testing
Run syntax check:
```bash
python -m py_compile space_mcp.py
```

Test imports:
```bash
python -c "import space_mcp"
```

## 📋 API Keys (Optional)

This server uses NASA's `DEMO_KEY` for basic testing. For production use with higher rate limits:

1. Get a free NASA API key at https://api.nasa.gov/
2. Replace `NASA_DEMO_KEY` in the code with your key
3. Consider implementing authentication for Launch Library 2 API

## 🌟 Use Cases

### Education
- Astronomy lessons with daily space images
- Mars mission tracking and research
- Understanding asteroid threats
- Space station orbital mechanics

### Space Enthusiasts
- Launch countdown tracking
- ISS spotting opportunities
- Mars rover mission following
- NEO close approach monitoring

### Developers
- Building space-themed applications
- Integrating NASA data into projects
- Creating educational tools
- Space event notification systems

## 🤝 Contributing

This MCP server follows best practices from:
- MCP Protocol Specification
- NASA API Guidelines
- FastMCP Python SDK patterns
- Pydantic v2 validation standards

## 📜 License

This server integrates with public APIs:
- NASA APIs are in the public domain
- ISS tracking data is publicly available
- Launch Library 2 is open source

## 🔗 Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [NASA APIs](https://api.nasa.gov/)
- [Launch Library 2](https://thespacedevs.com/llapi)
- [wheretheiss.at](https://wheretheiss.at/)

## 🚀 What's Next?

Potential enhancements:
- Mars weather data integration
- Hubble Space Telescope image searches
- Exoplanet database queries
- Solar system object positions
- Deep space network status
- Earth imagery and EPIC camera data

---

**Made with ❤️ for space exploration and Claude Code!**

Explore the cosmos with Claude! 🌌✨
