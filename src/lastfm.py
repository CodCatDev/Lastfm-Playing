import aiohttp
import config
import base64
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
                    is_now_playing = track.get('@attr', {}).get("nowplaying", "false") == "true"
                
                date = ""
                if not is_now_playing:
                    date = track.get('date', {}).get('#text', "Unknown date")

                return {
                    "isNowPlaying":is_now_playing,
                    "artist": artist,
                    "album":album,
                    "title":title,
                    "img": logo,
                    "date": date
                }, True
                
        except Exception as e:
            return f"Unknown error: {e}", False

async def getBase64Image(url: str) -> tuple[str, bool]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return f"download logo unknown error: {response.status}", False
            imageBytes = await response.read()
            contentType = response.headers.get("Content-Type", "image/jpeg")
            
    b64String = base64.b64encode(imageBytes).decode("utf-8")
    return f"data:{contentType};base64,{b64String}", True

async def getPlaceholder() -> str:
    b64str = base64.b64encode(open('icon-placeholder.png', 'rb').read()).decode("utf-8")
    b64 = f"data:image/png;base64,{b64str}"
    return b64