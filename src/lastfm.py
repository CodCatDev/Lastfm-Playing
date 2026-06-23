import aiohttp
import asyncio
import config
from typing import Any

async def getRecentTrack(username: str) -> tuple[Any, bool]:
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "user.getrecenttracks",
        "user": username,
        "api_key": config.API_KEY,
        "format": "json",
        "limit": 1
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as resp:
                if resp.status != 200:
                    return f"audioscrobbler error: {resp.status}", False
                
                data = await resp.json()
                
                if "error" in data:
                    return f"lastfm error: {data.get('message')}", False
                
                tracks = data.get("recenttracks", {}).get("track")
                if not tracks:
                    return "Nothing listen", True
                
                if isinstance(tracks, dict):
                    tracks = [tracks]
                
                track = tracks[0]
                artist = track.get("artist", {}).get("#text", "Unknown Artist")
                title = track.get("name", "Unknown Track")
                album = track.get("album", {}).get("#text", "")
                logoList = track.get('image', [])
                logo = ""
                for lg in logoList:
                    if lg.get('size', "") == "extralarge":
                        logo = lg.get('#text', "")
                
                is_now_playing = False
                if "@attr" in track and "nowplaying" in track["@attr"]:
                    is_now_playing = track["@attr"]["nowplaying"] == "true"
    
                return {
                    "isNowPlaying":is_now_playing,
                    "artist": artist,
                    "album":album,
                    "title":title,
                    "img": logo
                }, True
                
        except Exception as e:
            return f"Unknown error: {e}", False