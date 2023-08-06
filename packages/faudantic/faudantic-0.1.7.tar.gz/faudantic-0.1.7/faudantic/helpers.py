from typing import Optional, Dict, Any
from aiohttp import ClientSession

async def fetch(url:str, method:str, headers:Optional[Dict[str,str]]={"Content-Type": "application/json","Accept": "application/json"}, json:Optional[Dict[str,Any]]=None,) -> Dict[str,Any]:
    """Helper function to make requests from a JSON API."""
    if method in ["GET", "DELETE"]:
        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers) as response:
                return await response.json()
    elif method in ["POST", "PUT", "PATCH"]:
        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, json=json) as response:
                return await response.json()
    else:
        raise ValueError(f"Invalid method: {method}")
    
    
async def text(url:str, method:str, headers:Optional[Dict[str,str]]=None, data:Optional[str]=None,) -> str:
    """Helper function to make requests from a text API."""
    if method in ["GET", "DELETE"]:
        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers) as response:
                return await response.text()
    elif method in ["POST", "PUT", "PATCH"]:
        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, data=data) as response:
                return await response.text()
    else:
        raise ValueError(f"Invalid method: {method}")
    
async def blob(url:str, method:str, headers:Optional[Dict[str,str]]=None, data:Optional[bytes]=None,) -> bytes:
    """Helper function to make requests from a binary API."""
    if method in ["GET", "DELETE"]:
        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers) as response:
                return await response.read()
    elif method in ["POST", "PUT", "PATCH"]:
        async with ClientSession() as session:
            async with session.request(method=method, url=url, headers=headers, data=data) as response:
                return await response.read()
    else:
        raise ValueError(f"Invalid method: {method}")