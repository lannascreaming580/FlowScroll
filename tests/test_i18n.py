import json
from pathlib import Path


def test_locale_keysets_match():
    base = Path(__file__).resolve().parents[1] / "FlowScroll" / "locales"
    zh = json.loads((base / "zh-CN.json").read_text(encoding="utf-8"))
    en = json.loads((base / "en-US.json").read_text(encoding="utf-8"))

    zh_keys = set(zh.keys())
    en_keys = set(en.keys())
    assert zh_keys == en_keys, (
        f"locale key mismatch: only_zh={sorted(zh_keys - en_keys)} "
        f"only_en={sorted(en_keys - zh_keys)}"
    )


def test_language_normalization_and_fallback():
    from FlowScroll.i18n import normalize_language

    assert normalize_language("auto") == "auto"
    assert normalize_language("zh") == "zh-CN"
    assert normalize_language("zh-Hans") == "zh-CN"
    assert normalize_language("en") == "en-US"
    assert normalize_language("EN_us") == "en-US"
    assert normalize_language("unknown") == "auto"


def test_get_system_language_falls_back_to_env(monkeypatch):
    import FlowScroll.i18n as i18n

    monkeypatch.setattr(i18n.locale, "getlocale", lambda *args, **kwargs: (None, None))
    monkeypatch.setenv("LANG", "zh_CN.UTF-8")

    assert i18n.get_system_language() == "zh-CN"
