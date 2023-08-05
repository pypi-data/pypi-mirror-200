"""Lightweight ORM to perform simple CRUD operations on FaunaDB collections and provision indexes
   the fauna query object is available also within the class for further customization
"""
from __future__ import annotations
import asyncio
from os import environ
from typing import List, Optional, Any, Callable, Generator
from pydantic import BaseSettings, BaseConfig, Field
from faunadb import query as q
from faunadb.objects import Query
from faunadb.client import FaunaClient
from faunadb.errors import FaunaError
from faudantic.json import JSONModel
from faudantic.client import AsyncFaunaClient


class Environment(BaseSettings):
    """Environment variables"""

    fauna_secret: str = Field(..., env="FAUNA_SECRET")

    class Config(BaseConfig):
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        if not self.fauna_secret:
            self.fauna_secret = environ["FAUNA_SECRET"]


env = Environment()


class FaunaModel(JSONModel):
    """FaunaDB Model"""

    ref: Optional[str] = Field(
        default=None, description="The document's id got from Ref object"
    )
    ts: Optional[float] = Field(
        default=None, description="The document's timestamp got from FaunaTime object"
    )

    @classmethod
    def client(cls) -> FaunaClient:
        """Return a FaunaClient"""
        return FaunaClient(secret=env.fauna_secret)

    @classmethod
    def q(cls) -> Callable[..., Query]:
        """Return a FaunaDB query"""
        return cls.client().query

    @classmethod
    def provision(cls) -> None:
        """Provision the collection and indexes"""
        _q = cls.q()
        try:
            if not _q(q.exists(q.collection(cls.__name__.lower()))):
                _q(q.create_collection({"name": cls.__name__.lower()}))
                print(f"Created collection {cls.__name__.lower()}")
                _q(
                    q.create_index(
                        {
                            "name": cls.__name__.lower(),
                            "source": q.collection(cls.__name__.lower()),
                        }
                    )
                )
                print(f"Created index {cls.__name__.lower()}")
            for field in cls.__fields__.values():
                if field.field_info.extra.get("unique"):
                    _q(
                        q.create_index(
                            {
                                "name": f"{cls.__name__.lower()}_{field.name}_unique",
                                "source": q.collection(cls.__name__.lower()),
                                "terms": [{"field": ["data", field.name]}],
                                "unique": True,
                            }
                        )
                    )
                    print(
                        f"Created unique index {cls.__name__.lower()}_{field.name}_unique"
                    )
                    continue
                if field.field_info.extra.get("index"):
                    _q(
                        q.create_index(
                            {
                                "name": f"{cls.__name__.lower()}_{field.name}",
                                "source": q.collection(cls.__name__.lower()),
                                "terms": [{"field": ["data", field.name]}],
                            }
                        )
                    )
                    print(f"Created index {cls.__name__.lower()}_{field.name}")
                    continue
        except FaunaError as exc:
            print(exc)

    @classmethod
    def exists(cls, ref: str) -> Optional[bool]:
        """Check if a document exists"""
        try:
            return cls.q()(q.exists(q.ref(q.collection(cls.__name__.lower()), ref)))
        except FaunaError as exc:
            print(exc)
            return None

    @classmethod
    def find_unique(cls, field: str, value: Any) -> Optional[FaunaModel]:
        """Find a document by a unique field"""
        try:
            data = cls.q()(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )
            return cls(**{**data["data"], "ref": data["ref"].id(), "ts": data["ts"]/1000})
        except FaunaError as exc:
            print(exc)
            return None

    @classmethod
    def find_many(cls, field: str, value: Any) -> Generator[FaunaModel, None, None]:
        """Find documents by a field"""
        try:
            _q = cls.q()
            refs = _q(
                q.paginate(q.match(q.index(f"{cls.__name__.lower()}_{field}"), value))
            )["data"]
            for ref in refs:
                data = _q(q.get(ref))
                yield cls(**{**data["data"], "ref": data["ref"].id(), "ts": data["ts"]/1000})
        except FaunaError as exc:
            print(exc)
            return None

    @classmethod
    def find(cls, ref: str) -> Optional[FaunaModel]:
        """Find a document by id"""
        try:
            data = cls.q()(q.get(q.ref(q.collection(cls.__name__.lower()), ref)))
            return cls(**{**data["data"], "ref": data["ref"].id(), "ts": data["ts"]/1000})
        except FaunaError as exc:
            print(exc)
            return None

    @classmethod
    def find_all(cls) -> Generator[FaunaModel, None, None]:
        """Find all documents"""
        try:
            _q = cls.q()
            refs = _q(q.paginate(q.match(q.index(cls.__name__.lower()))))["data"]
            for ref in refs:
                data = _q(q.get(ref))
                yield cls(**{**data["data"], "ref": data["ref"].id(), "ts": data["ts"]/1000})
        except FaunaError as exc:
            print(exc)
            return None

    @classmethod
    def delete_unique(cls, field: str, value: Any) -> bool:
        """Delete a document by a unique field"""
        try:
            _q = cls.q()
            ref = _q(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )
            _q(q.delete(ref))
            return True
        except FaunaError:
            return False

    @classmethod
    def delete(cls, ref: str) -> bool:
        """Delete a document by id"""
        try:
            cls.q()(q.delete(q.ref(q.collection(cls.__name__.lower()), ref)))
            return True
        except FaunaError:
            return False

    def create(self) -> Optional[FaunaModel]:
        """Create a document"""
        try:
            for field in self.__fields__.values():
                if field.field_info.extra.get("unique"):
                    if self.find_unique(field.name, getattr(self, field.name)):
                        raise ValueError(f"{field.name} must be unique")
            data = self.q()(
                q.create(
                    q.collection(self.__class__.__name__.lower()), {"data": self.dict()}
                )
            )
            self.ref = data["ref"].id()
            self.ts = data["ts"] / 1000
            return self

        except FaunaError as exc:
            print(exc)
            return None

    @classmethod
    def update(cls, ref: str, **kwargs) -> Optional[FaunaModel]:
        """Update a document"""
        try:
            data = cls.q()(
                q.update(
                    q.ref(q.collection(cls.__name__.lower()), ref), {"data": kwargs}
                )
            )
            return cls(**{**data["data"], "ref": data["ref"].id(), "ts": data["ts"]/1000})
        except FaunaError as exc:
            print(exc)
            return None

    def upsert(self) -> Optional[FaunaModel]:
        """Upsert a document"""
        try:
            if not self.ref:
                return self.create()
            return self.update(self.ref, **self.dict())
        except FaunaError as exc:
            print(exc)
            return None

    @classmethod
    def query(cls, query: str) -> Generator[FaunaModel, None, None]:
        """Run a query"""
        try:
            refs = cls.q()(q.paginate(q.match(q.query(query))))["data"]
            for ref in refs:
                data = cls.q()(q.get(ref))
                yield cls(**{**data["data"], "ref": data["ref"].id(), "ts": data["ts"]/1000})
        except FaunaError as exc:
            print(exc)
            return None

class AsyncFaunaModel(JSONModel):
    """FaunaDB Model"""
    ref: Optional[str] = None
    ts: Optional[int] = None
    
    @classmethod
    def client(cls) -> AsyncFaunaClient:
        """Return a FaunaClient"""
        return AsyncFaunaClient(secret=env.fauna_secret)

    @classmethod
    def q(cls):
        """Return a FaunaDB query"""
        return cls.client().query

    @classmethod
    async def provision(cls) -> None:
        """Provision the collection and indexes"""
        _q = cls.q()
        try:
            if not await _q(q.exists(q.collection(cls.__name__.lower()))):
                await _q(q.create_collection({"name": cls.__name__.lower()}))
                print(f"Created collection {cls.__name__.lower()}")
                await _q(
                    q.create_index(
                        {
                            "name": cls.__name__.lower(),
                            "source": q.collection(cls.__name__.lower()),
                        }
                    )
                )
                print(f"Created index {cls.__name__.lower()}")
            for field in cls.__fields__.values():
                if field.field_info.extra.get("unique"):
                    await _q(
                        q.create_index(
                            {
                                "name": f"{cls.__name__.lower()}_{field.name}_unique",
                                "source": q.collection(cls.__name__.lower()),
                                "terms": [{"field": ["data", field.name]}],
                                "unique": True,
                            }
                        )
                    )
                    print(
                        f"Created unique index {cls.__name__.lower()}_{field.name}_unique"
                    )
                    continue
                if field.field_info.extra.get("index"):
                    await _q(
                        q.create_index(
                            {
                                "name": f"{cls.__name__.lower()}_{field.name}",
                                "source": q.collection(cls.__name__.lower()),
                                "terms": [{"field": ["data", field.name]}],
                            }
                        )
                    )
                    print(f"Created index {cls.__name__.lower()}_{field.name}")
                    continue
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None

    @classmethod
    async def exists(cls, ref: str) -> Optional[bool]:
        """Check if a document exists"""
        try:
            return await cls.q()(q.exists(q.ref(q.collection(cls.__name__.lower()), ref)))
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None

    @classmethod
    async def find_unique(cls, field: str, value: Any) -> Optional[AsyncFaunaModel]:
        """Find a document by a unique field"""
        try:
            data = await cls.q()(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )
            return cls(**{**data["data"], "ref": data["ref"]["@ref"]["id"], "ts": data["ts"]/1000})
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None

    @classmethod
    async def find_many(cls, field: str, value: Any) -> Optional[List[AsyncFaunaModel]]:
        """Find documents by a field"""
        try:
            _q = cls.q()
            refs = (await _q(
                q.paginate(q.match(q.index(f"{cls.__name__.lower()}_{field}"), value))
            ))["data"]
            data = await asyncio.gather(*[_q(q.get(q.ref(q.collection(cls.__name__.lower()), ref['@ref']['id']))) for ref in refs])
            return [
                cls(**{**d["data"], "ref": d["ref"]["@ref"]["id"], "ts": d["ts"]/1000}) for d in data
            ]   
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None

    @classmethod
    async def find(cls, ref: str) -> Optional[AsyncFaunaModel]:
        """Find a document by id"""
        try:
            data = await cls.q()(q.get(q.ref(q.collection(cls.__name__.lower()), ref)))
            return cls(**{**data["data"], "ref": data["ref"]["@ref"]["id"], "ts": data["ts"]/1000})
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None

    @classmethod
    async def find_all(cls) -> Optional[List[AsyncFaunaModel]]:
        """Find all documents"""
        try:
            _q = cls.q()
            refs = (await _q(q.paginate(q.match(q.index(cls.__name__.lower())))))["data"]
            data = await asyncio.gather(*[_q(q.get(q.ref(q.collection(cls.__name__.lower()), ref['@ref']['id']))) for ref in refs])
            return [
                cls(**{**d["data"], "ref": d["ref"]["@ref"]["id"], "ts": d["ts"]/1000}) for d in data
            ]

        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None


    @classmethod
    async def delete_unique(cls, field: str, value: Any) -> bool:
        """Delete a document by a unique field"""
        try:
            _q = cls.q()
            ref = await _q(
                q.get(q.match(q.index(f"{cls.__name__.lower()}_{field}_unique"), value))
            )
            await _q(q.delete(ref))
            return True
        except (FaunaError, KeyError, IndexError, Exception) as exc:
            print(exc)
            return False
    @classmethod
    async def delete(cls, ref: str) -> bool:
        """Delete a document by id"""
        try:
            await cls.q()(q.delete(q.ref(q.collection(cls.__name__.lower()), ref)))
            return True
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return False

            return False

    async def create(self) -> Optional[AsyncFaunaModel]:
        """Create a document"""
        try:
            for field in self.__fields__.values():
                if field.field_info.extra.get("unique"):
                    instance = await self.find_unique(field.name, self.dict()[field.name])
                    if instance:
                        return instance
            data = await self.q()(
                q.create(
                    q.collection(self.__class__.__name__.lower()), {"data": self.dict()}
                ))
            return self.__class__(**{**data["data"], "ref": data["ref"]["@ref"]["id"], "ts": data["ts"]/1000})
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None

        
    @classmethod
    async def update(cls, ref: str, **kwargs) -> Optional[AsyncFaunaModel]:
        """Update a document"""
        try:
            data = await cls.q()(
                q.update(
                    q.ref(q.collection(cls.__name__.lower()), ref), {"data": kwargs}
                )
            )
            return cls(**{**data["data"], "ref": data["ref"]["@ref"]["id"], "ts": data["ts"]/1000})
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None


    async def upsert(self) -> Optional[AsyncFaunaModel]:
        """Upsert a document"""
        try:
            if not self.ref:
                return await self.create()
            return await self.update(self.ref, **self.dict())
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None


    @classmethod
    async def query(cls, query: str) -> Optional[List[AsyncFaunaModel]]:
        """Run a query"""
        try:
            refs = (await cls.q()(q.paginate(q.match(q.query(query)))))["data"]
            data = await asyncio.gather(*[cls.q()(q.get(ref)) for ref in refs])
            return [
                cls(**{**d["data"], "ref": d["ref"]["@ref"]["id"], "ts": d["ts"]/1000}) for d in data
            ]
        
        except (FaunaError, KeyError, IndexError, ValueError, EOFError, ModuleNotFoundError,TypeError,Exception) as exc:
            print(exc)
            return None
