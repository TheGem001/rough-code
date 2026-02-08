from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import yt_dlp
import requests

app = FastAPI()

@app.get("/api/download")
async def download_video(url: str):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        # 'cookiefile': 'cookies.txt', # Recommended for bypassing bot detection
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            filename = f"{info.get('title', 'video')}.mp4"

        # Pipe the data stream directly back to the client
        def iter_content():
            with requests.get(video_url, stream=True) as r:
                for chunk in r.iter_content(chunk_size=8192):
                    yield chunk

        return StreamingResponse(
            iter_content(),
            media_type="video/mp4",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))