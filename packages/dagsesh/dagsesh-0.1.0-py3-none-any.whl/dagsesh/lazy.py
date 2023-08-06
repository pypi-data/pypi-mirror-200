"""Delay imports of Python modules and packages.

"""
from typing import Dict, Text
import types
import importlib


class Loader(types.ModuleType):
    """Lazily import a module."""

    def __init__(
        self, local_name: Text, parent_module_globals: Dict, module_name: Text
    ):
        self.__local_name = local_name
        self.__parent_module_globals = parent_module_globals

        super().__init__(module_name)

    @property
    def local_name(self) -> Text:
        """Get the local_name."""
        return self.__local_name

    @property
    def parent_module_globals(self) -> Dict:
        """Get the parent_module_globals."""
        return self.__parent_module_globals

    def _load(self) -> types.ModuleType:
        """Import the target module and insert it into the parent's namespace.

        The method will update this object's dict so that if someone keeps a reference to the
        LazyLoader, lookups are efficient (__getattr__ is only called on lookups that fail).

        Returns:
            Python module.

        """
        module = importlib.import_module(self.__name__)
        self.parent_module_globals[self.local_name] = module

        self.__dict__.update(module.__dict__)

        return module

    def __getattr__(self, item: Text) -> Text:
        module = self._load()

        return getattr(module, item)
