# core/update_checker.py
import json
import ssl
import urllib.request

from core.version import APP_VERSION, REPO_OWNER, REPO_NAME

GITHUB_API_LATEST = "https://api.github.com/repos/{owner}/{repo}/releases/latest"


class UpdateInfo:
    def __init__(self, current, latest, url, has_update):
        self.current = current
        self.latest = latest
        self.url = url
        self.has_update = has_update


def normalize_version(v: str):
    v = v.lstrip("vV").strip()
    parts = []
    for part in v.split("."):
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def fetch_latest_release():
    url = GITHUB_API_LATEST.format(owner=REPO_OWNER, repo=REPO_NAME)
    req = urllib.request.Request(url, headers={"User-Agent": "QuizApp-Updater"})

    ctx = ssl.create_default_context()

    with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
        data = json.load(resp)

    tag = data.get("tag_name") or data.get("name") or APP_VERSION
    html_url = data.get("html_url") or ""
    has_update = normalize_version(tag) > normalize_version(APP_VERSION)
    return UpdateInfo(APP_VERSION, tag, html_url, has_update)
