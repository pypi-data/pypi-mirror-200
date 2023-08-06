"""
wbpNamespace
===============================================================================

Tree view to inspect the namespace of the application
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import wx
from wx import aui

from .config import NameSpaceConfig, NameSpacePreferences
from .control import NameSpace

if TYPE_CHECKING:
    from wbBase.application import App

__version__ = "0.1.7"

name = "Namespace"

namespaceConfig = NameSpaceConfig()

nameSpaceInfo = aui.AuiPaneInfo()
nameSpaceInfo.Name(name)
nameSpaceInfo.Caption(name)
nameSpaceInfo.MaximizeButton(True)
nameSpaceInfo.MinimizeButton(True)
nameSpaceInfo.CloseButton(False)
nameSpaceInfo.Right()
nameSpaceInfo.Dock()
nameSpaceInfo.Hide()
nameSpaceInfo.Resizable()
nameSpaceInfo.MinSize(150, 100)
nameSpaceInfo.BestSize(250, 200)
nameSpaceInfo.Icon(wx.ArtProvider.GetBitmap("NAMESPACE", wx.ART_FRAME_ICON))


panels = [(NameSpace, nameSpaceInfo)]
preferencepages = [NameSpacePreferences]


def loadConfig(app: App):
    namespaceConfig.load()
