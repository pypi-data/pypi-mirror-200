"""
config
===============================================================================
"""
import wx.stc as stc
from wbBase.control.textEditControl import PyTextEditConfig
from wbBase.dialog.preferences import PreferencesPageBase


class NameSpaceConfig(PyTextEditConfig):
    def __init__(self):
        PyTextEditConfig.__init__(self)
        self.ShowLineNumbers = False
        self.WrapMode = stc.STC_WRAP_WORD

    def appendProperties(self, page):
        """
        Append properties to PreferencesPage
        """
        self.registerPropertyEditors(page)
        self.appendProperties_main(page)
        self.appendProperties_caret(page)
        self.appendProperties_selection(page)
        # self.appendProperties_indentation(page)
        # self.appendProperties_line_ending(page)
        self.appendProperties_line_warp(page)
        # self.appendProperties_line_numbers(page)
        # self.appendProperties_code_folding(page)
        self.appendProperties_syntax_colour(page)


class NameSpacePreferences(PreferencesPageBase):
    """
    Additional page for the preferences dialog of the
    Workbench application.
    """
    def __init__(self, parent):
        PreferencesPageBase.__init__(self, parent)
        from . import name, namespaceConfig

        self.name = name
        self._config = namespaceConfig
        self.config.appendProperties(self)

    @property
    def config(self):
        return self._config

    def applyValues(self):
        """
        Apply configuration to the namespace panel.
        """
        pane = self.app.TopWindow.panelManager.getPaneByCaption(self.name)
        if pane:
            self.config.getPropertyValues(self)
            win = pane.window
            tree = win.tree
            tree.SetBackgroundColour(self.config.backgroundColour.ChangeLightness(130))
            tree.SetForegroundColour(self.config.foregroundColour)
            self.config.apply(win.text)

    def saveValues(self):
        self.applyValues()
        self.config.save()
