"""Wock-Multi entry point."""
import os
import sys

_wock = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _wock not in sys.path:
    sys.path.insert(0, _wock)

from colorama import init
init(autoreset=True)

from lib import constants as C
from lib.boot import boot
from lib.config import get_settings
from lib.deps import check_deps
from lib.remote import show_announcement_block, sync as remote_sync
from lib.updater import handle_update_gate
from lib.router import MasterRouter
from lib.setup import run_setup_wizard
from lib.wock_common import cls, console, error_box


def run_wock():
    check_deps(auto_install=True)
    s = get_settings()
    C.apply_theme(C._THEME_ALIASES.get(s.get("theme", "red"), s.get("theme", "red")))

    if os.name == "nt":
        import ctypes
        os.system(f"title Wock-Multi — {s.username}")
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )

    remote_sync()
    if handle_update_gate():
        main_py = os.path.join(C.wock_DIR, "main.py")
        os.execv(sys.executable, [sys.executable, "-u", main_py])

    run_setup_wizard()
    s = get_settings()
    boot(skip_anim=bool(s.get("skip_boot")))
    show_announcement_block()
    cls()
    MasterRouter().start()


if __name__ == "__main__":
    try:
        run_wock()
    except KeyboardInterrupt:
        console.print(f"\n[{C.C_DIM}]  ○ Arrêt propre.[/]")
        sys.exit(0)
    except Exception as e:
        cls()
        error_box("Crash fatal", "Wock-Multi", f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
