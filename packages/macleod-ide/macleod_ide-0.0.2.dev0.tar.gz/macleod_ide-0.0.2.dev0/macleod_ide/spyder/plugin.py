# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2023, Reading Club Development
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
macleod_ide Plugin.
"""

# Third-party imports
import qtawesome as qta

# Spyder imports
from spyder.api.plugins import Plugins, SpyderPluginV2
from spyder.api.translations import get_translation
from spyder.utils.icon_manager import ima
from spyder.api.plugin_registration.decorators import on_plugin_available

# Local imports
from macleod_ide.spyder.confpage import macleod_ideConfigPage
from macleod_ide.spyder.container import macleod_ideContainer

_ = get_translation("macleod_ide.spyder")


class macleod_ide(SpyderPluginV2):
    """
    macleod_ide plugin.
    """

    NAME = "macleod_ide"
    REQUIRES = [Plugins.StatusBar, Plugins.Toolbar]
    OPTIONAL = []
    CONTAINER_CLASS = macleod_ideContainer
    CONF_SECTION = NAME
    CONF_WIDGET_CLASS = macleod_ideConfigPage

    # --- Signals

    # --- SpyderPluginV2 API
    # ------------------------------------------------------------------------
    def get_name(self):
        return _("macleod_ide")

    def get_description(self):
        return _("An IDE plugin for the macleod parser")

    def get_icon(self):
        return qta.icon("ei.file-edit", color=ima.MAIN_FG_COLOR)

    def on_initialize(self):
        container = self.get_container()
        print('macleod_ide initialized!')

    @on_plugin_available(plugin=Plugins.StatusBar)
    def on_statusbar_available(self):
        statusbar = self.get_plugin(Plugins.StatusBar)
        if statusbar:
            statusbar.add_status_widget(self.macleod_ide_status)

    @on_plugin_available(plugin=Plugins.Toolbar)
    def on_toolbar_available(self):
        container = self.get_container()
        toolbar = self.get_plugin(Plugins.Toolbar)
        toolbar.add_application_toolbar(container.macleod_ide_toolbar)

    @property
    def macleod_ide_status(self):
        container = self.get_container()
        return container.macleod_ide_status

    def check_compatibility(self):
        valid = True
        message = ""  # Note: Remember to use _("") to localize the string
        return valid, message

    def on_close(self, cancellable=True):
        return True

    # --- Public API
    # ------------------------------------------------------------------------
