import sys
import os

def resource_path(relative_path):
    """
    获取资源的绝对路径，兼容 Nuitka (Standalone / Onefile) 和 PyInstaller 打包后的路径。
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller
        base_path = sys._MEIPASS
    elif "__compiled__" in globals() or hasattr(sys, 'frozen'):
        # Nuitka 模式下
        # Nuitka 临时解压目录与 __file__ 相关，sys.argv[0] 指向的是外层的原 exe。
        # 我们使用当前 utils.py 所在的目录结构向上回溯到项目根目录（打包后的数据根目录）。
        # FlowScroll/ui/utils.py -> 退 2 层 -> FlowScroll -> 再退1层 -> 根目录
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        except NameError:
            base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    else:
        # 开发源码环境
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
