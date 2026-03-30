import os
import shlex
import sys

from FlowScroll.platform import OS_NAME, system_platform


class AutoStartManager:
    """璺ㄥ钩鍙板紑鏈鸿嚜鍚姩绠＄悊灏佽銆?"""

    def __init__(self) -> None:
        self.app_name: str = "FlowScroll"
        if getattr(sys, "frozen", False):
            self.app_path: str = os.path.abspath(sys.executable)
        else:
            script_path = os.path.abspath(sys.argv[0])
            self.app_path = self._build_source_launch_command(script_path)

    @staticmethod
    def _build_source_launch_command(script_path: str) -> str:
        python_path = os.path.abspath(sys.executable)
        if OS_NAME == "Windows":
            return f'"{python_path}" "{script_path}"'
        return f"{shlex.quote(python_path)} {shlex.quote(script_path)}"

    def is_autorun(self) -> bool:
        return system_platform.is_autostart_enabled(self.app_name, self.app_path)

    def set_autorun(self, enable: bool) -> bool:
        return system_platform.set_autostart(self.app_name, self.app_path, enable)
