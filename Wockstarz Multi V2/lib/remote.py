"""Remote — Discord, site GitHub, alertes MAJ (manifest GitHub)."""
import json
import os
import sys
import time
import urllib.error
import urllib.request

from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich import box

from . import constants as C
from .config import get_settings
from .wock_common import ansi_hex, cls, console, error_box, pause, success_box

# Héberge Wock/config/remote-manifest.json sur GitHub (branche main)
REMOTE_URL = os.environ.get(
    "Wock_REMOTE_URL",
    "https://raw.githubusercontent.com/verareal1231-lgtm/wock/refs/heads/main/remote-manifest.json",
)
LOCAL_MANIFEST = os.path.join(C.CONFIG_DIR, "remote-manifest.json")
CACHE_PATH = os.path.join(C.DATA_DIR, "remote-cache.json")

_manifest = {}
_loaded = False


def _ensure_dirs():
    os.makedirs(C.CONFIG_DIR, exist_ok=True)
    os.makedirs(C.DATA_DIR, exist_ok=True)


def _load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save_cache(data):
    _ensure_dirs()
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _rev_num(manifest):
    try:
        return int(str((manifest or {}).get("config_rev", "0")))
    except ValueError:
        return 0


def _fetch_url(url, timeout=8):
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}t={int(time.time())}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": f"Wock-Tools/{C.VERSION}", "Cache-Control": "no-cache"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _default_manifest():
    if os.path.isfile(LOCAL_MANIFEST):
        try:
            return _load_json(LOCAL_MANIFEST)
        except Exception:
            pass
    return {"config_rev": "0", "latest_version": C.VERSION, "links": {}}


def get_manifest():
    global _manifest, _loaded
    if not _loaded:
        _manifest = _default_manifest()
        if os.path.isfile(CACHE_PATH):
            try:
                _manifest = _load_json(CACHE_PATH)
            except Exception:
                pass
        _loaded = True
    return _manifest


def config_rev():
    return str(get_manifest().get("config_rev", "0"))


def apply_overrides(manifest=None):
    """Applique Discord + GitHub (site) + changelog."""
    m = manifest or get_manifest()
    links = m.get("links") or {}
    if links.get("discord"):
        C.DISCORD = str(links["discord"]).strip()
    if links.get("github"):
        C.GITHUB = str(links["github"]).strip()
    if links.get("shop"):
        C.SHOP = str(links["shop"]).strip()
    if m.get("changelog"):
        C.CHANGELOG = str(m["changelog"])


def sync(force=False):
    """[SAFE] Remote sync neutralized - no phone-home"""
    global _manifest, _loaded
    if not _loaded:
        _manifest = _default_manifest()
        _loaded = True
    return True, "local"


def sync_or_fail(force=False):
    """[SAFE] Stub"""
    return sync(force)


def has_pending_update():
    s = get_settings()
    return config_rev() != str(s.get("last_seen_config_rev", ""))


def mark_seen():
    s = get_settings()
    s.set("last_seen_config_rev", config_rev())
    s.save()


def version_update_available():
    m = get_manifest()
    latest = str(m.get("latest_version", C.VERSION))
    if latest == C.VERSION:
        return False
    try:
        from packaging.version import parse as vparse
        return vparse(latest) > vparse(C.VERSION)
    except Exception:
        return latest != C.VERSION


def status_badge():
    if version_update_available():
        return "MAJ"
    if has_pending_update():
        return "NEW"
    return ""


def show_announcement_block():
    """[SAFE] Blocked"""
    return
    # ORIGINAL BODY OMITTED
    from .updater import version_prompt_was_shown

    link_pending = has_pending_update()
    version_pending = version_update_available() and not version_prompt_was_shown()
    if not link_pending and not version_pending:
        return
    s = get_settings()
    fr = s.lang == "fr"
    m = get_manifest()
    ann = m.get("announcement") or {}
    title = ann.get("title_fr" if fr else "title_en") or ("Mise à jour" if fr else "Update")
    body = ann.get("body_fr" if fr else "body_en") or ann.get("body_en") or ""
    extra = []
    if version_pending:
        latest = m.get("latest_version", "?")
        dl = m.get("download_url", C.GITHUB)
        if fr:
            extra.append(f"Nouvelle version [bold {C.C_GOLD}]{latest}[/] (tu as {C.VERSION}).")
        else:
            extra.append(f"New version [bold {C.C_GOLD}]{latest}[/] (you have {C.VERSION}).")
        extra.append(f"Télécharge : [{C.C_DIM}]{dl}[/]")
    if C.DISCORD or C.GITHUB or C.SHOP:
        extra.append(f"Discord : [{C.C_GOLD2}]{C.DISCORD}[/]")
        extra.append(f"Shop    : [{C.C_GOLD2}]{C.SHOP}[/]")
        extra.append(f"Site    : [{C.C_GOLD2}]{C.GITHUB}[/]")
    cls()
    console.print(Panel(
        Align.center(Text.from_markup(
            f"[bold {C.C_NEON}]{title}[/]\n\n{body}"
            + ("\n\n" + "\n".join(extra) if extra else "")
        )),
        title=f"[bold {C.C_GOLD}]Wock — LIENS & MAJ[/]",
        border_style=C.C_GOLD,
        box=box.DOUBLE,
        padding=(1, 2),
    ))
    msg = (
        f"{ansi_hex(C.C_MID)}  ► Entrée pour continuer… \033[0m"
        if fr else f"{ansi_hex(C.C_MID)}  ► Press Enter to continue… \033[0m"
    )
    input(msg)
    mark_seen()
    cls()


def tool_remote_sync():
    """[SAFE] Stub"""
    from .wock_common import pause, cls
    cls()
    print("[Remote sync disabled for safety]")
    pause()
