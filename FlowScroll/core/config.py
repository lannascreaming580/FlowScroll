import os
import threading
from dataclasses import dataclass
from typing import Tuple

from FlowScroll.constants import (
    CONFIG_VERSION,
    DEFAULT_INERTIA_FRICTION_MS,
    DEFAULT_INERTIA_THRESHOLD,
    WINDOW_INFO_FAILURE_STALE_THRESHOLD,
)

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".FlowScroll_config.json")

BUILTIN_PRESETS = {
    "网页阅读": {
        "sensitivity": 1.5,
        "speed_factor": 3.0,
        "dead_zone": 25.0,
        "overlay_size": 60.0,
        "enable_horizontal": False,
        "minimize_to_tray": True,
        "horizontal_hotkey": "",
        "activation_hotkey_click": "",
        "activation_hotkey_hold": "",
        "activation_mode": 0,
        "activation_compat_mode": False,
        "activation_delay_ms": 0,
        "filter_mode": 0,
        "filter_blacklist": [],
        "filter_whitelist": [],
        "filter_use_regex": False,
        "disable_fullscreen": True,
        "disable_desktop": True,
    },
    "代码办公": {
        "sensitivity": 2.5,
        "speed_factor": 2.5,
        "dead_zone": 15.0,
        "overlay_size": 60.0,
        "enable_horizontal": False,
        "minimize_to_tray": True,
        "horizontal_hotkey": "",
        "activation_hotkey_click": "",
        "activation_hotkey_hold": "",
        "activation_mode": 0,
        "activation_compat_mode": False,
        "activation_delay_ms": 0,
        "filter_mode": 0,
        "filter_blacklist": [],
        "filter_whitelist": [],
        "filter_use_regex": False,
        "disable_fullscreen": True,
        "disable_desktop": True,
    },
    "长文档/表格": {
        "sensitivity": 2.0,
        "speed_factor": 2.0,
        "dead_zone": 20.0,
        "overlay_size": 60.0,
        "enable_horizontal": True,
        "minimize_to_tray": True,
        "horizontal_hotkey": "",
        "activation_hotkey_click": "",
        "activation_hotkey_hold": "",
        "activation_mode": 0,
        "activation_compat_mode": False,
        "activation_delay_ms": 0,
        "filter_mode": 0,
        "filter_blacklist": [],
        "filter_whitelist": [],
        "filter_use_regex": False,
        "disable_fullscreen": True,
        "disable_desktop": True,
    },
    "轻柔/接近触控板": {
        "sensitivity": 1.2,
        "speed_factor": 1.5,
        "dead_zone": 10.0,
        "overlay_size": 60.0,
        "enable_horizontal": False,
        "minimize_to_tray": True,
        "horizontal_hotkey": "",
        "activation_hotkey_click": "",
        "activation_hotkey_hold": "",
        "activation_mode": 0,
        "activation_compat_mode": False,
        "activation_delay_ms": 0,
        "filter_mode": 0,
        "filter_blacklist": [],
        "filter_whitelist": [],
        "filter_use_regex": False,
        "disable_fullscreen": True,
        "disable_desktop": True,
    },
}

DEFAULT_PRESET_NAME = "长文档/表格"


@dataclass
class RuntimeState:
    """运行时状态，不持久化，仅在当前进程生命周期内有效。"""

    active: bool = False
    origin_pos: Tuple[int, int] = (0, 0)
    current_window_name: str = ""
    current_process_name: str = ""
    process_name_status: str = "unknown"
    last_match_target: str = ""
    current_window_class: str = ""
    is_fullscreen: bool = False
    window_info_failure_count: int = 0

    @property
    def window_info_is_stale(self) -> bool:
        return self.window_info_failure_count >= WINDOW_INFO_FAILURE_STALE_THRESHOLD


class GlobalConfig:
    """
    持久化用户配置。
    运行时状态已拆分到 RuntimeState。
    """

    def __init__(self):
        self.config_version = CONFIG_VERSION

        defaults = BUILTIN_PRESETS[DEFAULT_PRESET_NAME]
        self.dead_zone = defaults["dead_zone"]
        self.sensitivity = defaults["sensitivity"]
        self.speed_factor = defaults["speed_factor"]
        self.overlay_size = defaults["overlay_size"]
        self.enable_horizontal = defaults["enable_horizontal"]
        self.minimize_to_tray = defaults["minimize_to_tray"]

        self.horizontal_hotkey = ""
        self.activation_hotkey_click = ""
        self.activation_hotkey_hold = ""

        self.reverse_y = False
        self.reverse_x = False

        self.hide_overlay = False  # 是否隐藏准星

        self.activation_mode = 0  # 0=点击中键启用/关闭, 1=长按中键时启用
        self.activation_compat_mode = False
        self.activation_delay_ms = 0
        self.ui_language = "auto"
        self.filter_mode = 0
        self.filter_blacklist = []
        self.filter_whitelist = []
        self.filter_use_regex = False
        self.disable_fullscreen = True
        self.disable_desktop = True

        self.enable_inertia = False
        self.inertia_friction_ms = DEFAULT_INERTIA_FRICTION_MS
        self.inertia_threshold = DEFAULT_INERTIA_THRESHOLD

        self.webdav_url = ""
        self.webdav_username = ""

    def to_dict(self):
        return {
            "config_version": self.config_version,
            "sensitivity": self.sensitivity,
            "speed_factor": self.speed_factor,
            "dead_zone": self.dead_zone,
            "overlay_size": self.overlay_size,
            "enable_horizontal": self.enable_horizontal,
            "minimize_to_tray": self.minimize_to_tray,
            "horizontal_hotkey": self.horizontal_hotkey,
            "activation_hotkey_click": self.activation_hotkey_click,
            "activation_hotkey_hold": self.activation_hotkey_hold,
            "reverse_y": self.reverse_y,
            "reverse_x": self.reverse_x,
            "hide_overlay": self.hide_overlay,
            "filter_mode": self.filter_mode,
            "filter_blacklist": self.filter_blacklist,
            "filter_whitelist": self.filter_whitelist,
            "filter_use_regex": self.filter_use_regex,
            "filter_list": self._get_active_filter_list(),
            "disable_fullscreen": self.disable_fullscreen,
            "disable_desktop": self.disable_desktop,
            "activation_mode": self.activation_mode,
            "activation_compat_mode": self.activation_compat_mode,
            "activation_delay_ms": self.activation_delay_ms,
            "ui_language": self.ui_language,
            "enable_inertia": self.enable_inertia,
            "inertia_friction_ms": self.inertia_friction_ms,
            "inertia_threshold": self.inertia_threshold,
        }

    def to_webdav_dict(self) -> dict:
        return {
            "url": self.webdav_url,
            "username": self.webdav_username,
        }

    def to_dict_for_sync(self) -> dict:
        """生成用于 WebDAV 同步的配置字典，不包含 WebDAV 凭据。"""
        return {
            "config_version": self.config_version,
            "sensitivity": self.sensitivity,
            "speed_factor": self.speed_factor,
            "dead_zone": self.dead_zone,
            "overlay_size": self.overlay_size,
            "enable_horizontal": self.enable_horizontal,
            "minimize_to_tray": self.minimize_to_tray,
            "horizontal_hotkey": self.horizontal_hotkey,
            "activation_hotkey_click": self.activation_hotkey_click,
            "activation_hotkey_hold": self.activation_hotkey_hold,
            "reverse_y": self.reverse_y,
            "reverse_x": self.reverse_x,
            "hide_overlay": self.hide_overlay,
            "filter_mode": self.filter_mode,
            "filter_blacklist": self.filter_blacklist,
            "filter_whitelist": self.filter_whitelist,
            "filter_use_regex": self.filter_use_regex,
            "filter_list": self._get_active_filter_list(),
            "disable_fullscreen": self.disable_fullscreen,
            "disable_desktop": self.disable_desktop,
            "activation_mode": self.activation_mode,
            "activation_compat_mode": self.activation_compat_mode,
            "activation_delay_ms": self.activation_delay_ms,
            "ui_language": self.ui_language,
            "enable_inertia": self.enable_inertia,
            "inertia_friction_ms": self.inertia_friction_ms,
            "inertia_threshold": self.inertia_threshold,
        }

    def from_dict(self, data):
        self.sensitivity = data.get("sensitivity", 2.0)
        self.speed_factor = data.get("speed_factor", 2.0)
        self.dead_zone = data.get("dead_zone", 20.0)
        self.overlay_size = data.get("overlay_size", 60.0)
        self.enable_horizontal = data.get("enable_horizontal", True)
        self.minimize_to_tray = data.get("minimize_to_tray", True)
        self.horizontal_hotkey = data.get("horizontal_hotkey", "")
        self.activation_hotkey_click = data.get("activation_hotkey_click", "")
        self.activation_hotkey_hold = data.get("activation_hotkey_hold", "")
        self.reverse_y = data.get("reverse_y", False)
        self.reverse_x = data.get("reverse_x", False)
        self.hide_overlay = data.get("hide_overlay", False)
        self.filter_mode = data.get("filter_mode", 0)
        legacy_list = data.get("filter_list", [])
        self.filter_blacklist = data.get("filter_blacklist")
        self.filter_whitelist = data.get("filter_whitelist")

        if self.filter_blacklist is None:
            if self.filter_mode in (0, 1):
                self.filter_blacklist = legacy_list
            else:
                self.filter_blacklist = []
        if self.filter_whitelist is None:
            if self.filter_mode in (0, 2):
                self.filter_whitelist = legacy_list
            else:
                self.filter_whitelist = []

        self.filter_blacklist = [
            str(v).strip() for v in self.filter_blacklist if str(v).strip()
        ]
        self.filter_whitelist = [
            str(v).strip() for v in self.filter_whitelist if str(v).strip()
        ]
        self.filter_use_regex = data.get("filter_use_regex", False)
        self.disable_fullscreen = data.get("disable_fullscreen", True)
        self.disable_desktop = data.get("disable_desktop", True)
        self.activation_mode = data.get("activation_mode", 0)
        self.activation_compat_mode = data.get("activation_compat_mode", False)
        self.activation_delay_ms = int(data.get("activation_delay_ms", 0))
        self.ui_language = data.get("ui_language", "auto")
        self.enable_inertia = data.get("enable_inertia", False)
        self.inertia_friction_ms = data.get("inertia_friction_ms", 500)
        self.inertia_threshold = data.get("inertia_threshold", 80.0)

    def from_webdav_dict(self, data):
        if not isinstance(data, dict):
            self.webdav_url = ""
            self.webdav_username = ""
            return
        self.webdav_url = str(data.get("url", "")).strip()
        self.webdav_username = str(data.get("username", "")).strip()

    def _get_active_filter_list(self):
        if self.filter_mode == 1:
            return list(self.filter_blacklist)
        if self.filter_mode == 2:
            return list(self.filter_whitelist)
        return []


cfg = GlobalConfig()
runtime = RuntimeState()
STATE_LOCK = threading.RLock()
