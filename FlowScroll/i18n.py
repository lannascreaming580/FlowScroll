import json
import locale
from pathlib import Path

from FlowScroll.core.config import STATE_LOCK, cfg

SUPPORTED_LANGUAGES = ("zh-CN", "en-US")
DEFAULT_LANGUAGE = "en-US"
AUTO_LANGUAGE = "auto"

_ALIASES = {
    "zh": "zh-CN",
    "zh_cn": "zh-CN",
    "zh-cn": "zh-CN",
    "zh_hans": "zh-CN",
    "zh-hans": "zh-CN",
    "en": "en-US",
    "en_us": "en-US",
    "en-us": "en-US",
}

_cache = {}


def _normalize_tag(tag: str) -> str:
    token = (tag or "").strip().lower().replace("-", "_")
    if not token:
        return ""
    if token in _ALIASES:
        return _ALIASES[token]
    if token.startswith("zh"):
        return "zh-CN"
    if token.startswith("en"):
        return "en-US"
    return ""


def normalize_language(value: str) -> str:
    token = (value or "").strip()
    if not token or token.lower() == AUTO_LANGUAGE:
        return AUTO_LANGUAGE
    normalized = _normalize_tag(token)
    if normalized in SUPPORTED_LANGUAGES:
        return normalized
    return AUTO_LANGUAGE


def get_system_language() -> str:
    candidates = []
    try:
        current_locale = locale.getlocale()[0]
        if current_locale:
            candidates.append(current_locale)
    except Exception:
        pass

    try:
        default_locale = locale.getdefaultlocale()[0]  # noqa: UP017
        if default_locale:
            candidates.append(default_locale)
    except Exception:
        pass

    for item in candidates:
        normalized = _normalize_tag(item)
        if normalized in SUPPORTED_LANGUAGES:
            return normalized

    return DEFAULT_LANGUAGE


def get_active_language() -> str:
    with STATE_LOCK:
        config_language = normalize_language(getattr(cfg, "ui_language", AUTO_LANGUAGE))
    if config_language == AUTO_LANGUAGE:
        return get_system_language()
    return config_language


def set_ui_language(value: str) -> str:
    normalized = normalize_language(value)
    with STATE_LOCK:
        cfg.ui_language = normalized
    return normalized


def _load_locale(lang: str) -> dict:
    locale_path = Path(__file__).resolve().parent / "locales" / f"{lang}.json"
    if not locale_path.exists():
        return {}
    try:
        return json.loads(locale_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _get_dict(lang: str) -> dict:
    if lang not in _cache:
        _cache[lang] = _load_locale(lang)
    return _cache.get(lang, {})


def tr(key: str, **kwargs) -> str:
    active = get_active_language()
    active_dict = _get_dict(active)
    fallback_dict = _get_dict(DEFAULT_LANGUAGE)
    value = active_dict.get(key)
    if value is None:
        value = fallback_dict.get(key, key)
    if kwargs:
        try:
            return str(value).format(**kwargs)
        except Exception:
            return str(value)
    return str(value)
