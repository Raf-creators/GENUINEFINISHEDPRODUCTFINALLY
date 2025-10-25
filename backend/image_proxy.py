"""
Image proxy to handle Checkatrade's Google Storage URLs
"""
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/api/proxy-image")
async def proxy_image(url: str):
    """
    Proxy images from external sources to bypass CORS and authentication issues
    """
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.checkatrade.com/',
            })
            
            if response.status_code == 200:
                return StreamingResponse(
                    iter([response.content]),
                    media_type=response.headers.get('content-type', 'image/jpeg')
                )
            else:
                logger.error(f"Failed to fetch image: {response.status_code}")
                raise HTTPException(status_code=404, detail="Image not found")
                
    except Exception as e:
        logger.error(f"Error proxying image: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch image: {str(e)}")
