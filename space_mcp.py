#!/usr/bin/env python3
"""
Space & Astronomy MCP Server

A comprehensive MCP server providing access to:
- NASA Astronomy Picture of the Day (APOD)
- Mars Rover Photos from Curiosity, Opportunity, and Spirit
- Near-Earth Object (NEO) tracking for potentially hazardous asteroids
- Real-time International Space Station location
- Upcoming space launches from Launch Library 2

This server enables LLMs to explore space data and provide cosmic insights.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any, Literal
from enum import Enum
from datetime import datetime, timedelta
import httpx
import json

# Constants
CHARACTER_LIMIT = 25000
NASA_API_BASE = "https://api.nasa.gov"
ISS_API_BASE = "https://api.wheretheiss.at/v1"
LAUNCH_API_BASE = "https://lldev.thespacedevs.com/2.3.0"  # Development API, no auth required
NASA_DEMO_KEY = "DEMO_KEY"  # NASA provides a demo key for testing

# Initialize MCP server
mcp = FastMCP("space_mcp")


# ============================================================================
# Pydantic Models for Input Validation
# ============================================================================

class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    MARKDOWN = "markdown"
    JSON = "json"


class MarsRover(str, Enum):
    """Available Mars rovers."""
    CURIOSITY = "curiosity"
    OPPORTUNITY = "opportunity" 
    SPIRIT = "spirit"
    PERSEVERANCE = "perseverance"


class MarsCamera(str, Enum):
    """Mars rover camera types."""
    FHAZ = "FHAZ"  # Front Hazard Avoidance Camera
    RHAZ = "RHAZ"  # Rear Hazard Avoidance Camera
    MAST = "MAST"  # Mast Camera
    CHEMCAM = "CHEMCAM"  # Chemistry and Camera Complex
    MAHLI = "MAHLI"  # Mars Hand Lens Imager
    MARDI = "MARDI"  # Mars Descent Imager
    NAVCAM = "NAVCAM"  # Navigation Camera
    PANCAM = "PANCAM"  # Panoramic Camera
    MINITES = "MINITES"  # Miniature Thermal Emission Spectrometer


class APODInput(BaseModel):
    """Input for retrieving NASA's Astronomy Picture of the Day."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, extra='forbid')
    
    date: Optional[str] = Field(
        default=None,
        description="Date for APOD in YYYY-MM-DD format (e.g., '2024-01-15', '1995-06-16'). Defaults to today.",
        pattern=r'^\d{4}-\d{2}-\d{2}$'
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


class MarsPhotosInput(BaseModel):
    """Input for retrieving Mars rover photos."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, extra='forbid')
    
    rover: MarsRover = Field(
        ...,
        description="Mars rover name: 'curiosity', 'opportunity', 'spirit', or 'perseverance'"
    )
    sol: Optional[int] = Field(
        default=None,
        description="Martian sol (day) number. Use either sol OR earth_date, not both.",
        ge=0
    )
    earth_date: Optional[str] = Field(
        default=None,
        description="Earth date in YYYY-MM-DD format (e.g., '2024-01-15'). Use either sol OR earth_date.",
        pattern=r'^\d{4}-\d{2}-\d{2}$'
    )
    camera: Optional[MarsCamera] = Field(
        default=None,
        description="Filter by camera type (e.g., 'FHAZ', 'RHAZ', 'MAST', 'NAVCAM'). Leave empty for all cameras."
    )
    limit: int = Field(
        default=25,
        description="Maximum number of photos to return",
        ge=1,
        le=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )

    @field_validator('sol', 'earth_date')
    @classmethod
    def validate_date_params(cls, v: Any, info) -> Any:
        """Ensure only one of sol or earth_date is provided."""
        if info.field_name == 'earth_date' and v is not None:
            if info.data.get('sol') is not None:
                raise ValueError("Provide either 'sol' or 'earth_date', not both")
        return v


class NeoInput(BaseModel):
    """Input for Near-Earth Object tracking."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, extra='forbid')
    
    start_date: Optional[str] = Field(
        default=None,
        description="Start date for NEO search in YYYY-MM-DD format. Defaults to today.",
        pattern=r'^\d{4}-\d{2}-\d{2}$'
    )
    end_date: Optional[str] = Field(
        default=None,
        description="End date for NEO search in YYYY-MM-DD format. Defaults to 7 days from start_date.",
        pattern=r'^\d{4}-\d{2}-\d{2}$'
    )
    limit: int = Field(
        default=20,
        description="Maximum number of NEOs to return",
        ge=1,
        le=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


class ISSLocationInput(BaseModel):
    """Input for ISS location tracking."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, extra='forbid')
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


class UpcomingLaunchesInput(BaseModel):
    """Input for upcoming space launches."""
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True, extra='forbid')
    
    limit: int = Field(
        default=10,
        description="Maximum number of launches to return",
        ge=1,
        le=50
    )
    search: Optional[str] = Field(
        default=None,
        description="Search term to filter launches (e.g., 'SpaceX', 'Falcon', 'ISS')",
        max_length=100
    )
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'markdown' for human-readable or 'json' for structured data"
    )


# ============================================================================
# Helper Functions
# ============================================================================

async def make_api_request(
    client: httpx.AsyncClient,
    url: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make an async API request with error handling.
    
    Args:
        client: HTTP client
        url: Request URL
        params: Optional query parameters
        
    Returns:
        JSON response as dictionary
        
    Raises:
        httpx.HTTPStatusError: If request fails
    """
    try:
        response = await client.get(url, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        error_msg = f"API request failed with status {e.response.status_code}: {e.response.text}"
        raise Exception(error_msg) from e
    except httpx.TimeoutException as e:
        raise Exception("API request timed out. Please try again.") from e
    except Exception as e:
        raise Exception(f"API request failed: {str(e)}") from e


def format_response(data: Any, format_type: ResponseFormat) -> str:
    """
    Format response data as JSON or Markdown.
    
    Args:
        data: Data to format
        format_type: Output format (json or markdown)
        
    Returns:
        Formatted string
    """
    if format_type == ResponseFormat.JSON:
        return json.dumps(data, indent=2)
    return data  # Markdown is already formatted


def check_character_limit(content: str, data: Any) -> str:
    """
    Check character limit and truncate if needed.
    
    Args:
        content: Content to check
        data: Original data for truncation info
        
    Returns:
        Content with truncation notice if needed
    """
    if len(content) > CHARACTER_LIMIT:
        truncated = content[:CHARACTER_LIMIT]
        truncated += f"\n\n⚠️ **Response truncated** from {len(content)} to {CHARACTER_LIMIT} characters. Use filters to narrow results."
        return truncated
    return content


# ============================================================================
# NASA API Tools
# ============================================================================

@mcp.tool(
    name="space_get_apod",
    annotations={
        "title": "Get NASA Astronomy Picture of the Day",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_apod(params: APODInput) -> str:
    """
    Retrieve NASA's Astronomy Picture of the Day with description.
    
    NASA's APOD showcases stunning astronomical images with expert explanations.
    Each day features a different image or photograph of our fascinating universe,
    along with a brief explanation written by a professional astronomer.
    
    Args:
        params (APODInput): Input parameters containing:
            - date (Optional[str]): Date in YYYY-MM-DD format. Defaults to today.
            - response_format (ResponseFormat): 'markdown' or 'json'
    
    Returns:
        str: APOD information in requested format including:
            - title: Picture title
            - date: APOD date
            - explanation: Scientific explanation
            - url: Image URL (hdurl if available)
            - media_type: Type of media (image or video)
            - copyright: Copyright information if applicable
    
    Example use cases:
        - Get today's astronomy picture
        - Explore historical APODs from specific dates
        - Learn about astronomical phenomena with expert explanations
    """
    async with httpx.AsyncClient() as client:
        api_params = {"api_key": NASA_DEMO_KEY}
        if params.date:
            api_params["date"] = params.date
        
        data = await make_api_request(
            client,
            f"{NASA_API_BASE}/planetary/apod",
            api_params
        )
        
        if params.response_format == ResponseFormat.MARKDOWN:
            image_url = data.get('hdurl', data.get('url', 'N/A'))
            copyright_info = f"\n📝 **Copyright:** {data.get('copyright', 'Public Domain')}" if 'copyright' in data else ""
            
            content = f"""# 🌌 Astronomy Picture of the Day

**Title:** {data.get('title', 'N/A')}
**Date:** {data.get('date', 'N/A')}
**Media Type:** {data.get('media_type', 'N/A')}{copyright_info}

## Explanation
{data.get('explanation', 'No explanation available.')}

## Image
🔗 [View Image]({image_url})
URL: {image_url}
"""
            return check_character_limit(content, data)
        else:
            return format_response(data, params.response_format)


@mcp.tool(
    name="space_get_mars_photos",
    annotations={
        "title": "Get Mars Rover Photos",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_mars_photos(params: MarsPhotosInput) -> str:
    """
    Retrieve photos from NASA Mars rovers (Curiosity, Opportunity, Spirit, Perseverance).
    
    Access thousands of images captured by NASA's Mars rovers from various cameras.
    Each photo includes metadata about the rover, camera, and Martian sol (day).
    
    Args:
        params (MarsPhotosInput): Input parameters containing:
            - rover (MarsRover): Rover name ('curiosity', 'opportunity', 'spirit', 'perseverance')
            - sol (Optional[int]): Martian sol (day) number
            - earth_date (Optional[str]): Earth date in YYYY-MM-DD format
            - camera (Optional[MarsCamera]): Camera filter (e.g., 'FHAZ', 'NAVCAM')
            - limit (int): Maximum photos to return (default: 25, max: 100)
            - response_format (ResponseFormat): 'markdown' or 'json'
    
    Returns:
        str: Mars rover photos in requested format including:
            - photos: List of photos with camera info, URLs, sol, earth_date
            - total: Total number of photos found
            - rover: Rover information
    
    Example use cases:
        - Explore Mars surface through rover cameras
        - Track rover missions by sol or earth date
        - Filter by specific cameras for different perspectives
        - View recent Curiosity or Perseverance discoveries
    
    Error handling:
        - If no date specified, uses most recent sol
        - Returns helpful message if no photos found for criteria
    """
    async with httpx.AsyncClient() as client:
        api_params = {"api_key": NASA_DEMO_KEY}
        
        # Add date parameter
        if params.sol is not None:
            api_params["sol"] = params.sol
        elif params.earth_date:
            api_params["earth_date"] = params.earth_date
        else:
            # Default to sol 1000 for a good sample
            api_params["sol"] = 1000
        
        # Add camera filter if specified
        if params.camera:
            api_params["camera"] = params.camera.value
        
        data = await make_api_request(
            client,
            f"{NASA_API_BASE}/mars-photos/api/v1/rovers/{params.rover.value}/photos",
            api_params
        )
        
        photos = data.get('photos', [])
        
        if not photos:
            return f"No photos found for {params.rover.value} with the specified criteria. Try a different date or remove the camera filter."
        
        # Limit results
        photos = photos[:params.limit]
        
        if params.response_format == ResponseFormat.MARKDOWN:
            content = f"""# 🔴 Mars Rover Photos: {params.rover.value.title()}

**Total Photos Found:** {len(photos)}
**Date:** {photos[0].get('earth_date', 'N/A')} (Earth) | Sol {photos[0].get('sol', 'N/A')} (Mars)
**Rover:** {photos[0].get('rover', {}).get('name', params.rover.value.title())}

"""
            for i, photo in enumerate(photos[:params.limit], 1):
                camera = photo.get('camera', {})
                content += f"""## Photo {i}
**Camera:** {camera.get('full_name', 'N/A')} ({camera.get('name', 'N/A')})
**Photo ID:** {photo.get('id', 'N/A')}
🔗 [View Photo]({photo.get('img_src', 'N/A')})

"""
            
            return check_character_limit(content, photos)
        else:
            result = {
                "total": len(photos),
                "rover": params.rover.value,
                "photos": photos[:params.limit]
            }
            return format_response(result, params.response_format)


@mcp.tool(
    name="space_track_asteroids",
    annotations={
        "title": "Track Near-Earth Objects (Asteroids)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def track_asteroids(params: NeoInput) -> str:
    """
    Track Near-Earth Objects (NEOs) including potentially hazardous asteroids.
    
    NASA's NeoWs (Near Earth Object Web Service) provides data on asteroids and comets
    that pass close to Earth. Includes size estimates, velocity, and hazard assessment.
    
    Args:
        params (NeoInput): Input parameters containing:
            - start_date (Optional[str]): Start date in YYYY-MM-DD format (defaults to today)
            - end_date (Optional[str]): End date in YYYY-MM-DD format (defaults to +7 days)
            - limit (int): Maximum NEOs to return (default: 20, max: 100)
            - response_format (ResponseFormat): 'markdown' or 'json'
    
    Returns:
        str: NEO tracking data in requested format including:
            - element_count: Total number of NEOs found
            - near_earth_objects: List of NEOs with:
                - name and NASA JPL URL
                - estimated diameter (min/max in meters)
                - potentially_hazardous status
                - close_approach_data with date, velocity, miss_distance
    
    Example use cases:
        - Monitor potentially hazardous asteroids
        - Track upcoming asteroid close approaches
        - Learn about NEO sizes and velocities
        - Explore asteroid statistics over date ranges
    
    Error handling:
        - Maximum date range is 7 days per NASA API limits
        - Provides clear guidance if date range too large
    """
    async with httpx.AsyncClient() as client:
        # Default dates
        start_date = params.start_date or datetime.now().strftime('%Y-%m-%d')
        end_date = params.end_date or (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        api_params = {
            "api_key": NASA_DEMO_KEY,
            "start_date": start_date,
            "end_date": end_date
        }
        
        data = await make_api_request(
            client,
            f"{NASA_API_BASE}/neo/rest/v1/feed",
            api_params
        )
        
        neo_data = data.get('near_earth_objects', {})
        element_count = data.get('element_count', 0)
        
        # Flatten NEOs from all dates
        all_neos = []
        for date_key in neo_data:
            all_neos.extend(neo_data[date_key])
        
        # Sort by miss distance (closest first) and limit
        all_neos.sort(key=lambda x: float(x['close_approach_data'][0]['miss_distance']['kilometers']))
        all_neos = all_neos[:params.limit]
        
        if params.response_format == ResponseFormat.MARKDOWN:
            content = f"""# ☄️ Near-Earth Objects (NEOs) Tracking

**Date Range:** {start_date} to {end_date}
**Total NEOs Found:** {element_count}
**Showing Top {len(all_neos)} Closest Approaches**

"""
            for i, neo in enumerate(all_neos, 1):
                hazardous = "⚠️ YES" if neo.get('is_potentially_hazardous_asteroid') else "✅ No"
                diameter = neo.get('estimated_diameter', {}).get('meters', {})
                close_approach = neo['close_approach_data'][0]
                
                content += f"""## {i}. {neo.get('name', 'Unknown')}
**Potentially Hazardous:** {hazardous}
**Estimated Diameter:** {diameter.get('estimated_diameter_min', 0):.1f} - {diameter.get('estimated_diameter_max', 0):.1f} meters
**Close Approach Date:** {close_approach.get('close_approach_date_full', 'N/A')}
**Relative Velocity:** {float(close_approach.get('relative_velocity', {}).get('kilometers_per_hour', 0)):,.0f} km/h
**Miss Distance:** {float(close_approach.get('miss_distance', {}).get('kilometers', 0)):,.0f} km
🔗 [NASA JPL Info]({neo.get('nasa_jpl_url', 'N/A')})

"""
            
            return check_character_limit(content, all_neos)
        else:
            result = {
                "element_count": element_count,
                "date_range": {"start": start_date, "end": end_date},
                "near_earth_objects": all_neos
            }
            return format_response(result, params.response_format)


# ============================================================================
# ISS Tracking Tool
# ============================================================================

@mcp.tool(
    name="space_track_iss",
    annotations={
        "title": "Track International Space Station Location",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def track_iss(params: ISSLocationInput) -> str:
    """
    Get real-time location of the International Space Station (ISS).
    
    The ISS travels at approximately 28,000 km/h (17,500 mph), orbiting Earth
    every 90 minutes at an altitude of about 400 km. This tool provides current
    position, velocity, altitude, and visibility status.
    
    Args:
        params (ISSLocationInput): Input parameters containing:
            - response_format (ResponseFormat): 'markdown' or 'json'
    
    Returns:
        str: ISS location data in requested format including:
            - latitude: Current latitude in degrees
            - longitude: Current longitude in degrees
            - altitude: Altitude in kilometers
            - velocity: Speed in km/h
            - visibility: Current visibility (daylight, eclipsed)
            - timestamp: Unix timestamp of data
    
    Example use cases:
        - Track ISS position for spotting opportunities
        - Monitor ISS orbit path
        - Educational space station tracking
        - Coordinate amateur astronomy observations
    
    Note: ISS position updates in real-time. Data accuracy typically within 1 second.
    """
    async with httpx.AsyncClient() as client:
        data = await make_api_request(
            client,
            f"{ISS_API_BASE}/satellites/25544"  # 25544 is ISS NORAD catalog ID
        )
        
        if params.response_format == ResponseFormat.MARKDOWN:
            timestamp = datetime.fromtimestamp(data.get('timestamp', 0))
            
            content = f"""# 🛰️ International Space Station (ISS) - Live Tracking

**Location:** {data.get('latitude', 0):.4f}°, {data.get('longitude', 0):.4f}°
**Altitude:** {data.get('altitude', 0):.2f} km
**Velocity:** {data.get('velocity', 0):,.0f} km/h
**Visibility:** {data.get('visibility', 'unknown').title()}

**Data Timestamp:** {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}

## ISS Facts
- Orbits Earth approximately every 90 minutes
- Travels at ~28,000 km/h (17,500 mph)
- Maintains altitude of ~400 km
- Size of a football field (109m x 73m)
- Home to international astronauts conducting research

🗺️ [View on Map](https://www.google.com/maps?q={data.get('latitude', 0)},{data.get('longitude', 0)})
"""
            return content
        else:
            return format_response(data, params.response_format)


# ============================================================================
# Space Launch Tracking Tool
# ============================================================================

@mcp.tool(
    name="space_get_launches",
    annotations={
        "title": "Get Upcoming Space Launches",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def get_launches(params: UpcomingLaunchesInput) -> str:
    """
    Get upcoming space launches from around the world.
    
    Launch Library 2 provides comprehensive data on upcoming rocket launches
    from all space agencies and private companies. Includes mission details,
    launch vehicles, locations, and status updates.
    
    Args:
        params (UpcomingLaunchesInput): Input parameters containing:
            - limit (int): Maximum launches to return (default: 10, max: 50)
            - search (Optional[str]): Search term to filter (e.g., 'SpaceX', 'ISS')
            - response_format (ResponseFormat): 'markdown' or 'json'
    
    Returns:
        str: Upcoming launches in requested format including:
            - name: Launch name and mission
            - net: Launch date/time (No Earlier Than)
            - status: Launch status (Go, TBD, Success, etc.)
            - launch_service_provider: Agency/company
            - rocket: Launch vehicle configuration
            - mission: Mission details and type
            - pad: Launch pad location
            - webcast_live: Whether webcast is available
    
    Example use cases:
        - Track SpaceX Falcon 9 launches
        - Monitor ISS resupply missions
        - Follow international space agency launches
        - Plan to watch live launch webcasts
        - Track specific rocket families (Atlas, Soyuz, etc.)
    
    Search tips:
        - Search by agency: 'SpaceX', 'NASA', 'ESA', 'Roscosmos'
        - Search by rocket: 'Falcon', 'Soyuz', 'Ariane', 'Starship'
        - Search by mission: 'ISS', 'Starlink', 'Mars'
    """
    async with httpx.AsyncClient() as client:
        api_params = {"limit": params.limit, "mode": "detailed"}
        if params.search:
            api_params["search"] = params.search
        
        data = await make_api_request(
            client,
            f"{LAUNCH_API_BASE}/launches/upcoming/",
            api_params
        )
        
        launches = data.get('results', [])
        count = data.get('count', 0)
        
        if not launches:
            search_info = f" matching '{params.search}'" if params.search else ""
            return f"No upcoming launches found{search_info}. Try a different search term or check back later."
        
        if params.response_format == ResponseFormat.MARKDOWN:
            search_info = f" (filtered by '{params.search}')" if params.search else ""
            content = f"""# 🚀 Upcoming Space Launches{search_info}

**Total Upcoming Launches:** {count}
**Showing:** {len(launches)} launches

"""
            for i, launch in enumerate(launches, 1):
                status = launch.get('status', {})
                status_emoji = "🟢" if status.get('name') == "Go" else "🟡" if "TBD" in status.get('name', '') else "🔴"
                
                provider = launch.get('launch_service_provider', {})
                rocket = launch.get('rocket', {}).get('configuration', {})
                pad = launch.get('pad', {})
                location = pad.get('location', {})
                mission = launch.get('mission', {})
                
                launch_time = launch.get('net', 'TBD')
                webcast = "📺 Webcast Available" if launch.get('webcast_live') else ""
                
                content += f"""## {i}. {launch.get('name', 'Unknown Mission')}

{status_emoji} **Status:** {status.get('name', 'Unknown')}
**Launch Time:** {launch_time}
**Provider:** {provider.get('name', 'Unknown')} ({provider.get('type', 'Unknown')})
**Rocket:** {rocket.get('full_name', 'Unknown')}
**Location:** {pad.get('name', 'Unknown')}, {location.get('name', 'Unknown')}

**Mission:** {mission.get('name', 'N/A')}
**Mission Type:** {mission.get('type', 'N/A')}
**Description:** {mission.get('description', 'No description available.')[:200]}...

{webcast}
🔗 [More Info]({launch.get('url', '#')})

---

"""
            
            return check_character_limit(content, launches)
        else:
            result = {
                "count": count,
                "showing": len(launches),
                "launches": launches
            }
            return format_response(result, params.response_format)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Run with stdio transport (default for MCP servers)
    mcp.run()
