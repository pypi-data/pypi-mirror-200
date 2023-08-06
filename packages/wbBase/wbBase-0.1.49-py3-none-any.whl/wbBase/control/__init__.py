"""Collection of various controls used by workbench applications"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import wx

if TYPE_CHECKING:
    from types import ModuleType
    from ..application import App


class PanelMixin:
    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} of "{self.app.AppName}">'

    @property
    def app(self) -> App:
        return wx.GetApp()

    @property
    def plugin(self) -> Optional[ModuleType]:
        plugins = self.app.pluginManager
        for name in plugins:
            plugin = plugins[name]
            if hasattr(plugin, "panels"):
                for cls, info in plugin.panels:
                    if cls == self.__class__:
                        return plugin
        return None

    @property
    def config(self) -> Optional[wx.ConfigBase]:
        if self.plugin:
            cfg = self.app.config
            cfg.SetPath(f"/Plugin/{self.plugin.__name__}/")
            return cfg
        return None
