# 🌌 Space & Astronomy MCP Server

<div align="center">

[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)](https://modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![NASA](https://img.shields.io/badge/NASA-APIs-red.svg)](https://api.nasa.gov/)

**Bring the cosmos to your AI! A production-quality MCP server integrating NASA, ISS tracking, and space launch data.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Reference](#-api-reference) • [Examples](#-examples)

</div>

---

## 📖 Overview

The **Space & Astronomy MCP Server** is a comprehensive Model Context Protocol (MCP) server that provides AI assistants like Claude with direct access to NASA's space data, real-time ISS tracking, Mars rover photos, asteroid monitoring, and global rocket launch schedules.

Built following MCP best practices, this server enables AI to explore the cosmos, answer astronomy questions, track space events, and provide educational content about space exploration—all through a clean, well-documented API.

### 🎯 What is MCP?

The [Model Context Protocol](https://modelcontextprotocol.io/) is an open standard that enables AI assistants to securely connect to external data sources and tools. This server implements MCP to give AI models access to space exploration data.

---

## ✨ Features

### 🔭 **NASA Data Integration**
- **Astronomy Picture of the Day (APOD)**
  - Access 30 years of stunning astronomical images
  - Expert scientific explanations
  - HD image URLs and metadata
  
- **Mars Rover Photos**
  - Photos from Curiosity, Perseverance, Opportunity, and Spirit
  - 9 different camera types (FHAZ, RHAZ, MAST, NAVCAM, etc.)
  - Search by Martian sol or Earth date
  - Over 1 million images available

- **Near-Earth Object (NEO) Tracking**
  - Monitor potentially hazardous asteroids
  - Size estimates and velocity data
  - Close approach dates and miss distances
  - NASA JPL database integration

### 🛰️ **Real-Time Space Tracking**
- **International Space Station Location**
  - Live position updates (latitude, longitude, altitude)
  - Current velocity (~28,000 km/h)
  - Visibility status (daylight/eclipsed)
  - Orbital data with 1-second accuracy

### 🚀 **Launch Information**
- **Global Rocket Launch Tracking**
  - Upcoming launches from all space agencies
  - SpaceX, NASA, ESA, Roscosmos, and more
  - Mission details and rocket specifications
  - Launch windows and webcast availability
  - Real-time status updates

### 🎨 **Flexible Response Formats**
- **Markdown** - Beautiful, human-readable formatting (default)
- **JSON** - Structured data for programmatic processing
- Smart truncation with guidance for large datasets
- Pagination support for extensive results

---

## 🚀 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager
- An Anthropic API key (for Claude integration)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/space-mcp-server.git
cd space-mcp-server
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `mcp>=1.0.0` - Model Context Protocol SDK
- `httpx>=0.27.0` - Async HTTP client
- `pydantic>=2.0.0` - Data validation

### Step 3: Verify Installation

```bash
python space_mcp.py --help
```

You should see the MCP server help information.

---

## ⚙️ Configuration

### For Claude Desktop

Add the server to your Claude Desktop configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

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

**Important:** Replace `/absolute/path/to/` with the actual path to your `space_mcp.py` file.

### For Other MCP Clients

This server uses the **stdio transport** by default, making it compatible with any MCP client. Configure your client to run:

```bash
python /path/to/space_mcp.py
```

---

## 💻 Usage

Once configured, you can interact with the server through your MCP client (e.g., Claude Desktop).

### Example Prompts

#### Astronomy Picture of the Day
```
"Show me today's astronomy picture"
"What was the APOD on June 16, 1995?"
"Get the astronomy picture from my birthday"
```

#### Mars Rover Photos
```
"Show me recent photos from the Curiosity rover"
"Get Perseverance photos from sol 500"
"Show me Spirit's navigation camera photos from 2005"
"Display Curiosity's front hazard camera images"
```

#### Asteroid Tracking
```
"Are there any dangerous asteroids approaching Earth?"
"Show me potentially hazardous NEOs this week"
"Track asteroids passing close to Earth"
"What's the largest asteroid approaching us?"
```

#### ISS Tracking
```
"Where is the ISS right now?"
"Track the International Space Station"
"Show me the current ISS location and velocity"
"When will the ISS pass over my location?"
```

#### Launch Tracking
```
"Show me upcoming SpaceX launches"
"What are the next rocket launches?"
"When is the next Falcon 9 launch?"
"List all launches scheduled this month"
"Show me ISS resupply missions"
```

---

## 📚 API Reference

### Tool: `space_get_apod`

Get NASA's Astronomy Picture of the Day.

**Parameters:**
- `date` (optional): Date in YYYY-MM-DD format (defaults to today)
- `response_format` (optional): "markdown" or "json" (default: "markdown")

**Returns:** APOD information including title, date, explanation, image URL, and copyright info.

**Example:**
```python
{
  "date": "2024-01-15",
  "response_format": "markdown"
}
```

---

### Tool: `space_get_mars_photos`

Retrieve photos from NASA Mars rovers.

**Parameters:**
- `rover` (required): "curiosity", "opportunity", "spirit", or "perseverance"
- `sol` (optional): Martian day number
- `earth_date` (optional): Earth date in YYYY-MM-DD format
- `camera` (optional): Camera filter (FHAZ, RHAZ, MAST, NAVCAM, PANCAM, etc.)
- `limit` (optional): Max photos (1-100, default: 25)
- `response_format` (optional): "markdown" or "json" (default: "markdown")

**Note:** Use either `sol` OR `earth_date`, not both.

**Returns:** Mars rover photos with camera info, URLs, sol, and earth_date.

**Example:**
```python
{
  "rover": "curiosity",
  "sol": 1000,
  "camera": "NAVCAM",
  "limit": 10,
  "response_format": "markdown"
}
```

---

### Tool: `space_track_asteroids`

Track Near-Earth Objects including potentially hazardous asteroids.

**Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format (defaults to today)
- `end_date` (optional): End date in YYYY-MM-DD format (defaults to +7 days)
- `limit` (optional): Max asteroids (1-100, default: 20)
- `response_format` (optional): "markdown" or "json" (default: "markdown")

**Returns:** NEO tracking data including name, size, velocity, close approach date, miss distance, and hazard status.

**Example:**
```python
{
  "start_date": "2024-12-01",
  "end_date": "2024-12-07",
  "limit": 10,
  "response_format": "json"
}
```

---

### Tool: `space_track_iss`

Get real-time International Space Station location.

**Parameters:**
- `response_format` (optional): "markdown" or "json" (default: "markdown")

**Returns:** ISS location data including latitude, longitude, altitude, velocity, and visibility status.

**Example:**
```python
{
  "response_format": "markdown"
}
```

---

### Tool: `space_get_launches`

Get upcoming space launches from around the world.

**Parameters:**
- `limit` (optional): Max launches (1-50, default: 10)
- `search` (optional): Search term to filter launches (e.g., "SpaceX", "Falcon", "ISS")
- `response_format` (optional): "markdown" or "json" (default: "markdown")

**Returns:** Upcoming launches with name, time, status, agency, rocket, mission details, and location.

**Example:**
```python
{
  "limit": 5,
  "search": "SpaceX",
  "response_format": "markdown"
}
```

---

## 🎯 Examples

### Example 1: Educational Astronomy Lesson

**Prompt:**
> "Show me today's astronomy picture and explain what makes this phenomenon special."

**Response:**
```markdown
# 🌌 Astronomy Picture of the Day

**Title:** The Horsehead Nebula in Infrared
**Date:** 2024-11-03
**Media Type:** image

## Explanation
The Horsehead Nebula is one of the most identifiable nebulae in the sky...
[Scientific explanation continues]

## Image
🔗 [View Image](https://apod.nasa.gov/apod/image/2411/horsehead_webb_4096.jpg)
```

---

### Example 2: Mars Rover Mission Tracking

**Prompt:**
> "Show me photos from Curiosity's mast camera on sol 1000. What did it see?"

**Response:**
```markdown
# 🔴 Mars Rover Photos: Curiosity

**Total Photos Found:** 145
**Date:** 2015-05-31 (Earth) | Sol 1000 (Mars)
**Rover:** Curiosity

## Photo 1
**Camera:** Mast Camera (MAST)
**Photo ID:** 102693
🔗 [View Photo](https://mars.nasa.gov/msl-raw-images/...)

## Photo 2
**Camera:** Mast Camera (MAST)
**Photo ID:** 102694
🔗 [View Photo](https://mars.nasa.gov/msl-raw-images/...)
```

---

### Example 3: Asteroid Hazard Assessment

**Prompt:**
> "Are there any potentially hazardous asteroids approaching Earth this week? How close will they get?"

**Response:**
```markdown
# ☄️ Near-Earth Objects (NEOs) Tracking

**Date Range:** 2024-11-03 to 2024-11-10
**Total NEOs Found:** 48
**Showing Top 5 Closest Approaches**

## 1. (2024 UT3)
**Potentially Hazardous:** ⚠️ YES
**Estimated Diameter:** 320.5 - 716.8 meters
**Close Approach Date:** 2024-11-05 14:23:00 UTC
**Relative Velocity:** 54,231 km/h
**Miss Distance:** 4,231,847 km
🔗 [NASA JPL Info](https://ssd.jpl.nasa.gov/...)
```

---

### Example 4: ISS Spotting

**Prompt:**
> "Where is the ISS right now? Can I see it from the ground?"

**Response:**
```markdown
# 🛰️ International Space Station (ISS) - Live Tracking

**Location:** 41.2345°, -74.3456°
**Altitude:** 418.32 km
**Velocity:** 27,584 km/h
**Visibility:** Daylight

**Data Timestamp:** 2024-11-03 19:45:23 UTC

## ISS Facts
- Orbits Earth approximately every 90 minutes
- Travels at ~28,000 km/h (17,500 mph)
- Maintains altitude of ~400 km
- Size of a football field (109m x 73m)

🗺️ [View on Map](https://www.google.com/maps?q=41.2345,-74.3456)
```

---

### Example 5: Launch Countdown

**Prompt:**
> "When is the next SpaceX Falcon 9 launch? Can I watch it online?"

**Response:**
```markdown
# 🚀 Upcoming Space Launches (filtered by 'SpaceX Falcon')

**Total Upcoming Launches:** 127
**Showing:** 3 launches

## 1. Falcon 9 Block 5 | Starlink Group 6-42

🟢 **Status:** Go
**Launch Time:** 2024-11-05T03:15:00Z
**Provider:** SpaceX (Commercial)
**Rocket:** Falcon 9 Block 5
**Location:** Space Launch Complex 40, Cape Canaveral SFS, FL, USA

**Mission:** Starlink Group 6-42
**Mission Type:** Communications
**Description:** A batch of 23 satellites for Starlink mega-constellation...

📺 Webcast Available
🔗 [More Info](https://ll.thespacedevs.com/2.0.0/launch/...)
```

---

## 🏗️ Architecture

### Design Principles

This server follows MCP best practices and agent-centric design:

1. **Workflow-Focused Tools** - Complete tasks, not just API wrappers
2. **Context-Efficient Responses** - High-signal information, optimized for LLM context windows
3. **Actionable Error Messages** - Guide users to correct usage patterns
4. **Natural Task Names** - Intuitive tool naming with `space_` prefix
5. **Composable Functions** - Shared utilities for DRY code

### Code Quality

- ✅ **Full type hints** throughout (Python 3.10+ typing)
- ✅ **Pydantic v2** models for bulletproof input validation
- ✅ **Async/await** patterns for all I/O operations
- ✅ **Comprehensive docstrings** with examples
- ✅ **Tool annotations** (readOnlyHint, destructiveHint, etc.)
- ✅ **Character limits** (25,000 chars) to prevent overflow
- ✅ **Error handling** with timeout protection

### API Sources

| API | Purpose | Documentation |
|-----|---------|---------------|
| NASA APOD | Astronomy pictures | [api.nasa.gov](https://api.nasa.gov/) |
| NASA Mars Rovers | Mars photos | [api.nasa.gov](https://api.nasa.gov/) |
| NASA NeoWs | Asteroid tracking | [api.nasa.gov](https://api.nasa.gov/) |
| wheretheiss.at | ISS tracking | [wheretheiss.at](https://wheretheiss.at/) |
| Launch Library 2 | Space launches | [thespacedevs.com](https://thespacedevs.com/) |

---

## 🧪 Testing

### Run Syntax Check

```bash
python -m py_compile space_mcp.py
```

### Run Evaluations

The server includes 10 comprehensive evaluation questions:

```bash
# Install evaluation dependencies
pip install anthropic mcp

# Set your API key
export ANTHROPIC_API_KEY=your_api_key_here

# Run evaluations (requires evaluation script)
python scripts/evaluation.py \
  -t stdio \
  -c python \
  -a space_mcp.py \
  evaluations.xml
```

### Manual Testing

Test individual tools with MCP Inspector or Claude Desktop:

```
"Test the APOD tool with June 16, 1995"
"Get Curiosity photos from sol 1"
"Track ISS location"
```

---

## 📊 Performance

- **Response Time:** <2 seconds for most queries
- **Character Limit:** 25,000 characters (prevents context overflow)
- **Pagination:** Supports large result sets
- **Timeout Protection:** 30-second maximum per request
- **Async Operations:** Non-blocking I/O for optimal performance

### Rate Limits

- **NASA APIs:** Using DEMO_KEY (30 requests/hour, 50/day)
  - Get a free NASA API key at [api.nasa.gov](https://api.nasa.gov/) for higher limits
- **ISS Tracking:** ~1 request per second
- **Launch Library 2:** Development API (no authentication required)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. **Report Bugs** - Open an issue with details and reproduction steps
2. **Suggest Features** - Propose new space data sources or tools
3. **Improve Documentation** - Fix typos, add examples, clarify instructions
4. **Submit Code** - Fix bugs, add features, optimize performance

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/space-mcp-server.git
cd space-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Run tests
python -m pytest tests/
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write comprehensive docstrings
- Add unit tests for new features
- Ensure async/await patterns for I/O operations

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🗺️ Roadmap

### Planned Features

- [ ] Mars weather data from InSight lander
- [ ] Hubble Space Telescope image searches
- [ ] Exoplanet database queries (NASA Exoplanet Archive)
- [ ] Solar system object positions
- [ ] Earth imagery from EPIC camera
- [ ] Solar flare and space weather alerts
- [ ] Spacecraft trajectory data
- [ ] Deep Space Network status
- [ ] Satellite tracking (beyond ISS)
- [ ] Historical mission archives

### Completed ✅

- [x] NASA APOD integration
- [x] Mars rover photo access
- [x] NEO asteroid tracking
- [x] Real-time ISS location
- [x] Global launch tracking
- [x] Markdown and JSON formats
- [x] Comprehensive documentation
- [x] Evaluation framework

---

## 🐛 Troubleshooting

### Common Issues

**Server won't start:**
```bash
# Check Python version (requires 3.10+)
python --version

# Verify dependencies
pip install -r requirements.txt

# Check for syntax errors
python -m py_compile space_mcp.py
```

**No results from tools:**
```bash
# NASA API issues - try with a different date
# ISS API - check internet connection
# Launch API - verify API is accessible
```

**Character limit warnings:**
```
# Reduce the limit parameter
# Add more specific filters
# Use JSON format for compact data
```

### Getting Help

- **Issues:** [GitHub Issues](https://github.com/yourusername/space-mcp-server/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/space-mcp-server/discussions)
- **MCP Documentation:** [modelcontextprotocol.io](https://modelcontextprotocol.io/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party APIs

This server integrates with public APIs:
- **NASA APIs** - Public domain (U.S. Government work)
- **wheretheiss.at** - Freely available ISS tracking data
- **Launch Library 2** - Open source space launch database

---

## 🙏 Acknowledgments

- **NASA** for providing free, public APIs and inspiring space exploration
- **The Space Devs** for maintaining Launch Library 2
- **Bill Shupp** for the wheretheiss.at ISS tracking API
- **Anthropic** for the Model Context Protocol specification
- **Claude** for assistance in building this server with the mcp-builder skill
- The entire **space exploration community** for making data accessible

---

## 🌟 Show Your Support

If you find this project useful, please consider:

- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 🤝 Contributing code
- 📢 Sharing with others

---

## 📞 Contact

- **Author:** Your Name
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **Email:** your.email@example.com
- **Twitter:** [@yourhandle](https://twitter.com/yourhandle)

---

## 🔗 Links

- [MCP Specification](https://modelcontextprotocol.io/)
- [NASA APIs](https://api.nasa.gov/)
- [Launch Library 2](https://thespacedevs.com/llapi)
- [wheretheiss.at API](https://wheretheiss.at/w/developer)
- [FastMCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Anthropic Claude](https://www.anthropic.com/claude)

---

<div align="center">

**Made with ❤️ for space exploration and AI**

🌌 **Explore the cosmos with Claude!** ✨

[⬆ Back to Top](#-space--astronomy-mcp-server)

</div>
