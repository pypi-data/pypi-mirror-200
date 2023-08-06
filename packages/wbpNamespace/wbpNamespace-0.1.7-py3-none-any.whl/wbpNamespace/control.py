"""
control
===============================================================================
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import wx
from wbBase.control.filling import Filling

if TYPE_CHECKING:
    from .config import NameSpaceConfig


class NameSpace(Filling):
    def __init__(
        self,
        parent: wx.Window,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.SP_LIVE_UPDATE
        | wx.SP_NOBORDER
        | wx.SP_NO_XP_THEME
        | wx.NO_BORDER,
    ):
        super().__init__(
            parent,
            id,
            pos,
            size,
            style,
            name="NameSpace",
            rootObject=None,
            rootLabel="NameSpace",
            rootIsNamespace=True,
            static=False,
        )
        self.config.load()

    @property
    def config(self) -> NameSpaceConfig:
        """
        Configuration of the namespace panel.
        """
        from . import namespaceConfig

        return namespaceConfig
