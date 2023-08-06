# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2023, Reading Club Development
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
macleod_ide Main Widget.
"""



# Spyder imports
from spyder.api.config.decorators import on_conf_change
from spyder.api.translations import get_translation
from spyder.api.widgets.toolbars import ApplicationToolbar
from spyder.api.widgets.status import BaseTimerStatus
from spyder.utils.icon_manager import ima

# Third party imports
import qtawesome as qta

# Localization
_ = get_translation("macleod_ide.spyder")

class MacleodIdeStatus(BaseTimerStatus):
    """Status bar widget to display the pomodoro timer"""

    ID = "macleod_ide_status"
    CONF_SECTION = "macleod_ide"

    def __init__(self, parent):
        super().__init__(parent)
        self.value = ""

    def get_tooltip(self):
        """Override api method."""
        return "macleod ide"

    def get_icon(self):
        return qta.icon("ei.file-edit", color=ima.MAIN_FG_COLOR)

class MacleodIdeToolbar(ApplicationToolbar):
    """ Toolbar to add buttons to macleod ide """

    ID = 'macleod_ide_toolbar'
