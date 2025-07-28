# Copyright (C) Shigeyuki <http://patreon.com/Shigeyuki>
# License: GNU AGPL version 3 or later <http://www.gnu.org/licenses/agpl.html>｣

from aqt import QDockWidget, QWidget, mw
from ..PixelArtsPathManager import path_manager

def update_progress_height(*args, **kwargs):
    from ..card_count_progress import (popup_timer_progress,
                                        popup_timer_progress_2)
    p = path_manager

    pop1 = None
    if popup_timer_progress is not None:
        pop1 = popup_timer_progress

    pop2 = None
    if popup_timer_progress_2 is not None:
        pop2 = popup_timer_progress_2

    config = mw.addonManager.getConfig(__name__)
    p.scale_to_Height = max(config["Character_Size"], 0)

    def adjust_height(pop, height):
        if pop is None:
            return

        height = max(height, 0)
        if (pop is not None
            and pop.adjust_widget_height is not None
            and isinstance(pop.adjust_widget_height, QWidget)
            and pop.adjust_dock_height is not None
            and isinstance(pop.adjust_dock_height, QDockWidget)):
                pop.setFixedHeight(max(height, 0))
                pop.setMinimumSize(0, 0)
                pop.adjust_widget_height.setFixedHeight(max(height, 0))
                pop.adjust_dock_height.setFixedHeight(max(height, 0))

    pop_objects = []
    height_keys = []
    if pop1 is not None:
        pop_objects.append(pop1)
        height_keys.append("height1")
    if pop2 is not None:
        pop_objects.append(pop2)
        height_keys.append("height2")

    heights = []
    for pop, key in zip(pop_objects, height_keys):
        # height = max(round(config[key] * p.scale_to_Height, 1), 0)
        if p.scale_to_Height:
            height = max(round(config[key] * p.scale_to_Height, 1), 0)
        else:
            height = 0
        adjust_height(pop, height)
        heights.append(height)

    config['total_top_dock_heigh'] = sum(heights)
    mw.addonManager.writeConfig(__name__, config)
    mw.web.setFocus()

