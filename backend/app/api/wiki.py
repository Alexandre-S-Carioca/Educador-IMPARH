from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/wiki", tags=["Wikipedia"])

@router.get("/summary")
async def get_wiki_summary(query: str):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    url = "https://pt.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "format": "json",
        "titles": query.strip()
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            
        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="Failed to fetch from Wikipedia API")
            
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        if not pages:
            return {"query": query, "summary": None, "url": None}
            
        # Pega a primeira página do resultado
        page_id = list(pages.keys())[0]
        
        if page_id == "-1":
            # Tentar uma busca aproximada para obter o título correto
            search_params = {
                "action": "opensearch",
                "limit": 1,
                "namespace": 0,
                "format": "json",
                "search": query.strip()
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                search_resp = await client.get(url, params=search_params)
            if search_resp.status_code == 200:
                search_data = search_resp.json()
                if len(search_data) >= 2 and search_data[1]:
                    # Refaz com o título sugerido
                    suggested_title = search_data[1][0]
                    params["titles"] = suggested_title
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        response = await client.get(url, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        pages = data.get("query", {}).get("pages", {})
                        page_id = list(pages.keys())[0]
        
        if page_id == "-1":
            return {"query": query, "summary": None, "url": None}
            
        page = pages[page_id]
        extract = page.get("extract", "")
        title = page.get("title", "")
        
        wiki_url = f"https://pt.wikipedia.org/wiki/{title.replace(' ', '_')}"
        
        return {
            "query": query,
            "title": title,
            "summary": extract if extract.strip() else None,
            "url": wiki_url
        }
    except Exception as e:
        return {"query": query, "summary": None, "url": None, "error": str(e)}
