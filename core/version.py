# core/version.py
import requests

APP_VERSION = "__APP_VERSION__"   # заполняется из тега GitHub
REPO_OWNER = "DexMP"
REPO_NAME = "quiz_game"


def get_latest_version() -> str | None:
    """
    Возвращает версию последнего релиза на GitHub (tag_name или name) либо None при ошибке.
    """
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        tag = (data.get("tag_name") or data.get("name") or "").strip()
        tag = tag.lstrip("vV")
        return tag or None
    except Exception:
        return None


def is_update_available() -> bool:
    """
    True, если опубликован релиз с версией, отличной от APP_VERSION.
    Для твоего кейса достаточно сравнения строк; при желании можно прикрутить semver. [web:134][web:145]
    """
    latest = get_latest_version()
    if not latest:
        return False
    current = (APP_VERSION or "").lstrip("vV")
    return latest != current
