from typing import Any
from aiohttp import ClientSession
from faunadb.objects import _Expr
from faunadb.errors import FaunaError
from faudantic.json import FaunaJSONEncoder

def to_json(obj: _Expr) -> str:
    return FaunaJSONEncoder().encode(obj)


class AsyncFaunaClient:
    """
    `AsyncFaunaClient`
    Summary:
        Introducing support for coroutines and async/await syntax for FaunaDB python driver.
    Description:
        Using `_Expr` data type as an input for `AsyncFaunaClient.query` method.
        We can build fauna queries using `q` module methods and pass them to `AsyncFaunaClient.query` method
        as an instance of `_Expr` data type to execute them.    
        The `_Expr` object will be serialized with `FaunaJSONEncoder` from json module so the FaunaDB API can understand it.
        The response will be deserialized by the `FaunaModel` class from orm module.
    """
    
    secret: str
    
    def __init__(self, secret: str ):
        self.secret = secret
    
    async def query(self, expr: _Expr) -> Any:
        """
        `AsyncFaunaClient.query`
        Summary:
            Execute a FaunaDB query.
        
        Args:
            expr: A FaunaDB query.
            
        Returns:
            A FaunaDB response.
        """
        
        async with ClientSession() as session:
            async with session.post(
                "https://db.fauna.com",
                data=to_json(expr),
                headers={
                    "Authorization": f"Bearer {self.secret}",
                    "Content-type": "application/json",
                    "Accept": "application/json"
                }) as response:
                try:
                    data = await response.json()
                    return data["resource"]
                except FaunaError as exc:
                    print(exc)
                    return None