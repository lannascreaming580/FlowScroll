from FlowScroll.core.config import STATE_LOCK, cfg, runtime
from FlowScroll.platform import OS_NAME


def is_current_app_allowed() -> bool:
    """统一应用过滤逻辑，判断当前前台应用是否允许启用滚动增强。"""
    with STATE_LOCK:
        disable_fullscreen = cfg.disable_fullscreen
        is_fullscreen = runtime.is_fullscreen
        disable_desktop = cfg.disable_desktop
        current_window_class = runtime.current_window_class
        filter_mode = cfg.filter_mode
        process_name = runtime.current_process_name.strip().lower()
        window_name = runtime.current_window_name.strip().lower()
        process_name_status = runtime.process_name_status
        filter_blacklist = list(cfg.filter_blacklist)
        filter_whitelist = list(cfg.filter_whitelist)

    match_target = process_name if process_name_status == "available" else window_name

    if disable_fullscreen and is_fullscreen:
        return False

    # Windows 桌面与壁纸窗口不参与滚动增强。
    if disable_desktop and OS_NAME == "Windows":
        if current_window_class in ("Progman", "WorkerW"):
            return False

    if filter_mode == 0:
        return True

    # 黑名单模式
    if filter_mode == 1:
        for keyword in filter_blacklist:
            if keyword.lower() in match_target:
                return False
        return True

    # 白名单模式
    if filter_mode == 2:
        for keyword in filter_whitelist:
            if keyword.lower() in match_target:
                return True
        return False

    return True
