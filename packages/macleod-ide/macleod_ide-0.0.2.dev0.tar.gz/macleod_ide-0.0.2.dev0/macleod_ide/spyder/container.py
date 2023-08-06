# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2023, Reading Club Development
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
macleod_ide Main Container.
"""

# Third party imports
import qtawesome as qta
from qtpy.QtWidgets import QToolButton

# Spyder imports
from spyder.api.config.decorators import on_conf_change
from spyder.api.translations import get_translation
from spyder.api.widgets.main_container import PluginMainContainer
from spyder.utils.icon_manager import ima

# Local imports
from macleod_ide.spyder.widgets import(
    MacleodIdeStatus,
    MacleodIdeToolbar,
) 

from macleod_ide.spyder.api import (
    MacleodToolbarActions, 
    MacleodToolbarSections,
    MacleodMenuSections,
)

_ = get_translation("macleod_ide.spyder")


class macleod_ideContainer(PluginMainContainer):

    # Signals

    # --- PluginMainContainer API
    # ------------------------------------------------------------------------
    def setup(self):
        # Widgets
        title = _("Macleod IDE Toolbar")
        self.macleod_ide_status = MacleodIdeStatus(self)
        self.macleod_ide_toolbar = MacleodIdeToolbar(self, title)

        # Actions
        edit_file_action = self.create_action(
            MacleodToolbarActions.Edit,
            text = _("Edit"),
            tip = _("Edit file"),
            icon = qta.icon("ei.livejournal", color=ima.MAIN_FG_COLOR),
            triggered = self.edit_file,
        )

        parse_file_action = self.create_action(
        MacleodToolbarActions.Parse,
        text = _("Parse"),
        tip = _("Parse file"),
        icon=qta.icon("ei.book", color=ima.MAIN_FG_COLOR),
        triggered = self.parse_file,
        ) 
        
        translate_file_action = self.create_action(
        MacleodToolbarActions.Translate,
        text = _("Translate"),
        tip = _("Translate file"),
        icon=qta.icon("ei.random", color=ima.MAIN_FG_COLOR),
        triggered = self.translate_file,
        ) 


        # Menu
        self.macleod_ide_menu = self.create_menu(
            "macleod_ide_menu",
            text = _("Macleod IDE"),
            icon=qta.icon("ei.file-edit", color = ima.MAIN_FG_COLOR),
        )

        # Add actions to the menu
        for action in [edit_file_action, parse_file_action,translate_file_action]:
            self.add_item_to_menu(
            action, 
            self.macleod_ide_menu,
            section = MacleodMenuSections.Main,
            )
        self.macleod_ide_button = self.create_toolbutton(
            "macleod_ide_button",
            text=_("Macleod IDE"),
            icon = qta.icon("ei.file-edit", color = ima.MAIN_FG_COLOR),
        )

        self.macleod_ide_button.setMenu(self.macleod_ide_menu)
        self.macleod_ide_button.setPopupMode(QToolButton.InstantPopup)

        # Add menu to toolbar
        self.add_item_to_toolbar(
            self.macleod_ide_button, 
            self.macleod_ide_toolbar,
            section = MacleodToolbarSections.Controls,
            )

    def update_actions(self):
        pass

    # --- Public API
    # ------------------------------------------------------------------------
    def edit_file(self):
        """ Edit the file """
        pass

    def parse_file(self):
        """ Parse the file """
        pass

    def translate_file(self):
        """ Translate the file """
        pass