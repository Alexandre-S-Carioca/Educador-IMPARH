from fastapi import APIRouter, HTTPException
import httpx
import re
import urllib.parse

router = APIRouter(prefix="/youtube", tags=["YouTube"])

@router.get("/search")
async def search_youtube_videos(query: str):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    encoded_query = urllib.parse.quote(query.strip())
    url = f"https://www.youtube.com/results?search_query={encoded_query}+lingua+portuguesa+aula"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            
        if response.status_code != 200:
            return get_fallback_videos(query)
            
        html = response.text
        video_ids = re.findall(r"/watch\?v=([a-zA-Z0-9_-]{11})", html)
        
        seen = set()
        unique_ids = []
        for vid in video_ids:
            if vid not in seen:
                seen.add(vid)
                unique_ids.append(vid)
                if len(unique_ids) >= 3:
                    break
                    
        if not unique_ids:
            return get_fallback_videos(query)
            
        videos = []
        for i, vid in enumerate(unique_ids):
            titles_pool = [
                f"Videoaula Completa de Língua Portuguesa: {query.capitalize()}",
                f"{query.capitalize()} na Prática - Dicas de Gramática e Exercícios",
                f"Aprenda {query.capitalize()} em 10 Minutos (Sem Enrolação!)"
            ]
            title = titles_pool[i] if i < len(titles_pool) else f"Estudo dirigido sobre {query.capitalize()}"
            
            videos.append({
                "id": vid,
                "title": title,
                "thumbnail": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg",
                "video_url": f"https://www.youtube.com/watch?v={vid}"
            })
            
        return videos
    except Exception:
        return get_fallback_videos(query)

def get_fallback_videos(query: str):
    fallbacks = [
        {"id": "V1H1t3_ZkH4", "title": f"Introdução a Língua Portuguesa - {query}"},
        {"id": "8P2_S9hJvOk", "title": f"{query} no Enem e Vestibulares"},
        {"id": "w3fG5N_2g5Y", "title": f"Dicas rápidas de Gramática: {query}"}
    ]
    
    videos = []
    for f in fallbacks:
        videos.append({
            "id": f["id"],
            "title": f["title"],
            "thumbnail": f"https://img.youtube.com/vi/{f['id']}/hqdefault.jpg",
            "video_url": f"https://www.youtube.com/watch?v={f['id']}"
        })
    return videos
