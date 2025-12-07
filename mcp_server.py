#!/usr/bin/env python3
"""
Conference Assistant MCP Server
Exposes tools for accessing conference and session data from Django ORM
"""

import os
import django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async

# Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firstProject.settings")
django.setup()

# Import Django models after setup
from ConferenceApp.models import Conference
from SessionApp.models import Session

# Create an MCP server
mcp = FastMCP("Conference Assistant")

# ============================================================================
# TOOL 1: List all available conferences
# ============================================================================
@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""
    @sync_to_async
    def _get_conferences():
        """Internal synchronous function to fetch conferences from database."""
        return list(Conference.objects.all())
    
    conferences = await _get_conferences()
    
    if not conferences:
        return "No conferences found."
    
    return "\n".join([
        f"- {c.name} ({c.start_date} to {c.end_date})"
        for c in conferences
    ])

# ============================================================================
# TOOL 2: Get details of a specific conference by name
# ============================================================================
@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Get details of a specific conference by name."""
    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
    
    conference = await _get_conference()
    
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    
    if not conference:
        return f"Conference '{name}' not found."
    
    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )

# ============================================================================
# TOOL 3: List sessions for a specific conference
# ============================================================================
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """List sessions for a specific conference."""
    @sync_to_async
    def _get_sessions():
        try:
            conference = Conference.objects.get(name__icontains=conference_name)
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None
    
    result, conference = await _get_sessions()
    
    if result == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."
    
    if conference is None:
        return f"Conference '{conference_name}' not found."
    
    sessions = result
    
    if not sessions:
        return f"No sessions found for conference '{conference.name}'."
    
    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n"
            f"  Topic: {s.topic}"
        )
    
    return "\n".join(session_list)

# ============================================================================
# TOOL 4: Get session details by title
# ============================================================================
@mcp.tool()
async def get_session_details(title: str) -> str:
    """Get detailed information about a specific session by title."""
    @sync_to_async
    def _get_session():
        try:
            return Session.objects.get(title__icontains=title)
        except Session.DoesNotExist:
            return None
        except Session.MultipleObjectsReturned:
            return "MULTIPLE"
    
    session = await _get_session()
    
    if session == "MULTIPLE":
        return f"Multiple sessions found matching '{title}'. Please be more specific."
    
    if not session:
        return f"Session '{title}' not found."
    
    conference = session.conference
    return (
        f"Title: {session.title}\n"
        f"Conference: {conference.name}\n"
        f"Topic: {session.topic}\n"
        f"Start Time: {session.start_time}\n"
        f"End Time: {session.end_time}\n"
        f"Room: {session.room}\n"
        f"Description: {session.description if hasattr(session, 'description') else 'N/A'}"
    )

# ============================================================================
# TOOL 5: Search conferences by theme
# ============================================================================
@mcp.tool()
async def search_conferences_by_theme(theme: str) -> str:
    """Search for conferences by theme."""
    @sync_to_async
    def _search_by_theme():
        return list(Conference.objects.filter(theme__icontains=theme))
    
    conferences = await _search_by_theme()
    
    if not conferences:
        return f"No conferences found with theme matching '{theme}'."
    
    return "\n".join([
        f"- {c.name} (Theme: {c.get_theme_display()}) - {c.location}\n"
        f"  Dates: {c.start_date} to {c.end_date}"
        for c in conferences
    ])

# ============================================================================
# TOOL 6: Filter conferences by date range (Custom Business Logic)
# ============================================================================
@mcp.tool()
async def filter_conferences_by_date_range(start_date: str, end_date: str) -> str:
    """
    Filter conferences by date range.
    Find conferences that overlap with or occur within the specified date range.
    Format dates as: YYYY-MM-DD (e.g., 2025-01-15)
    """
    from datetime import datetime
    
    @sync_to_async
    def _filter_by_date():
        try:
            # Parse input dates
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            
            # Validate date range
            if start > end:
                return "INVALID", None
            
            # Query conferences that overlap with the date range
            # A conference overlaps if: conference.start_date <= range.end_date AND conference.end_date >= range.start_date
            conferences = Conference.objects.filter(
                start_date__lte=end,
                end_date__gte=start
            ).order_by('start_date')
            
            return "OK", list(conferences)
        except ValueError:
            return "FORMAT_ERROR", None
    
    status, conferences = await _filter_by_date()
    
    if status == "FORMAT_ERROR":
        return f"Invalid date format. Please use YYYY-MM-DD format (e.g., 2025-01-15)."
    
    if status == "INVALID":
        return f"Invalid date range. Start date must be before or equal to end date."
    
    if not conferences:
        return f"No conferences found between {start_date} and {end_date}."
    
    result = f"Conferences between {start_date} and {end_date}:\n"
    result += "=" * 80 + "\n"
    
    for c in conferences:
        result += (
            f"\n• {c.name}\n"
            f"  Location: {c.location}\n"
            f"  Dates: {c.start_date} to {c.end_date}\n"
            f"  Theme: {c.get_theme_display()}\n"
            f"  Sessions: {c.sessions.count()}\n"
        )
    
    return result

# ============================================================================
# TOOL 7: Find upcoming conferences (Custom Business Logic)
# ============================================================================
@mcp.tool()
async def get_upcoming_conferences(days_ahead: int = 30) -> str:
    """
    Get upcoming conferences within the next N days.
    Default: next 30 days.
    """
    from datetime import datetime, timedelta
    
    @sync_to_async
    def _get_upcoming():
        today = datetime.now().date()
        future_date = today + timedelta(days=days_ahead)
        
        return list(Conference.objects.filter(
            start_date__gte=today,
            start_date__lte=future_date
        ).order_by('start_date'))
    
    conferences = await _get_upcoming()
    
    if not conferences:
        return f"No upcoming conferences in the next {days_ahead} days."
    
    result = f"Upcoming conferences (next {days_ahead} days):\n"
    result += "=" * 80 + "\n"
    
    for c in conferences:
        days_until = (c.start_date - datetime.now().date()).days
        result += (
            f"\n• {c.name}\n"
            f"  Location: {c.location}\n"
            f"  Starts in: {days_until} days ({c.start_date})\n"
            f"  Theme: {c.get_theme_display()}\n"
            f"  Total Sessions: {c.sessions.count()}\n"
        )
    
    return result

# ============================================================================
# TOOL 8: Get conference statistics (Custom Business Logic)
# ============================================================================
@mcp.tool()
async def get_conference_statistics() -> str:
    """
    Get comprehensive statistics about all conferences and sessions.
    Includes: total count, average sessions per conference, etc.
    """
    @sync_to_async
    def _get_stats():
        conferences = Conference.objects.all()
        sessions = Session.objects.all()
        
        total_conferences = conferences.count()
        total_sessions = sessions.count()
        
        if total_conferences == 0:
            return None
        
        avg_sessions = total_sessions / total_conferences
        
        # Get theme distribution
        theme_dist = {}
        for c in conferences:
            theme = c.get_theme_display()
            theme_dist[theme] = theme_dist.get(theme, 0) + 1
        
        # Get location distribution
        location_dist = {}
        for c in conferences:
            location = c.location
            location_dist[location] = location_dist.get(location, 0) + 1
        
        return {
            'total_conferences': total_conferences,
            'total_sessions': total_sessions,
            'avg_sessions_per_conference': avg_sessions,
            'theme_distribution': theme_dist,
            'location_distribution': location_dist
        }
    
    stats = await _get_stats()
    
    if stats is None:
        return "No conference data available."
    
    result = "Conference Statistics:\n"
    result += "=" * 80 + "\n"
    result += f"\nTotal Conferences: {stats['total_conferences']}\n"
    result += f"Total Sessions: {stats['total_sessions']}\n"
    result += f"Average Sessions per Conference: {stats['avg_sessions_per_conference']:.2f}\n"
    
    result += "\nTheme Distribution:\n"
    for theme, count in stats['theme_distribution'].items():
        result += f"  • {theme}: {count} conference(s)\n"
    
    result += "\nLocation Distribution:\n"
    for location, count in stats['location_distribution'].items():
        result += f"  • {location}: {count} conference(s)\n"
    
    return result

# ============================================================================
# RESOURCE: All conferences data
# ============================================================================
@mcp.resource("conferences://all")
def get_all_conferences_resource() -> str:
    """Expose all conference data as a resource."""
    @sync_to_async
    def _fetch_all():
        conferences = Conference.objects.all()
        result = "All Conferences:\n" + "=" * 80 + "\n"
        for c in conferences:
            result += (
                f"\nName: {c.name}\n"
                f"Theme: {c.get_theme_display()}\n"
                f"Location: {c.location}\n"
                f"Dates: {c.start_date} to {c.end_date}\n"
                f"Description: {c.description}\n"
            )
        return result
    
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(_fetch_all())

# ============================================================================
# Launcher
# ============================================================================
if __name__ == "__main__":
    mcp.run(transport="stdio")
