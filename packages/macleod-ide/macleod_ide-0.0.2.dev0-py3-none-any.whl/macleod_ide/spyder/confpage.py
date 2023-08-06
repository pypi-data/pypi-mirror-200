# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2023, Reading Club Development
#
# Licensed under the terms of the GNU General Public License v3
# ----------------------------------------------------------------------------
"""
macleod_ide Preferences Page.
"""
from spyder.api.preferences import PluginConfigPage
from spyder.api.translations import get_translation

_ = get_translation("macleod_ide.spyder")


class macleod_ideConfigPage(PluginConfigPage):

    # --- PluginConfigPage API
    # ------------------------------------------------------------------------
    def setup_page(self):
        pass
