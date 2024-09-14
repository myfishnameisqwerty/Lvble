from abc import ABC, abstractmethod
import importlib
from typing import Type

import aiohttp
from utils import snake_to_camel


class RentPortal(ABC):
    @abstractmethod
    def __init__(self, user_name: str, user_password: str) -> None: ...

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self.start_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    @abstractmethod
    async def start_session(self): ...

    @abstractmethod
    async def get_data(self): ...


class RentPortalFactory:
    @staticmethod
    def create_portal(tenant_portal: str, username: str, password: str) -> RentPortal:
        try:
            module_name = f"portals.{tenant_portal}"
            module = importlib.import_module(module_name)

            class_name = snake_to_camel(tenant_portal)
            portal_class: Type[RentPortal] = getattr(module, class_name)

            if not issubclass(portal_class, RentPortal):
                raise TypeError(f"{class_name} is not a subclass of RentPortal")

            return portal_class(username, password)

        except ModuleNotFoundError:
            raise ValueError(f"Module '{module_name}' not found.")
        except AttributeError:
            raise ValueError(
                f"Class '{class_name}' not found in the module '{module_name}'."
            )
        except Exception as e:
            raise RuntimeError(f"An error occurred while creating the portal: {e}")
