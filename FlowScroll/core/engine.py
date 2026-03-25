import math
import time
import threading
from FlowScroll.core.config import cfg
from FlowScroll.core.scroller import default_scroll_strategy
from FlowScroll.platform import system_platform


class ScrollEngine(threading.Thread):
    def __init__(self, bridge, mouse_controller):
        super().__init__(daemon=True)
        self.bridge = bridge
        self.mouse_controller = mouse_controller
        self.strategy = default_scroll_strategy

    def run(self):
        platform_multiplier = system_platform.get_scroll_multiplier()

        while True:
            if cfg.active:
                try:
                    curr_x, curr_y = self.mouse_controller.position
                    dx, dy = curr_x - cfg.origin_pos[0], curr_y - cfg.origin_pos[1]

                    if not cfg.enable_horizontal:
                        dx = 0

                    dist = math.hypot(dx, dy)

                    scroll_x, scroll_y = self.strategy.calculate_scroll_speed(
                        dx, dy, dist, cfg, platform_multiplier
                    )

                    if scroll_x != 0 or scroll_y != 0:
                        self.mouse_controller.scroll(scroll_x, scroll_y)

                    time.sleep(0.004)
                except Exception:
                    pass
            else:
                time.sleep(0.05)
