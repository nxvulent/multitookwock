#!/usr/bin/env python3
# SAFE_PLACEHOLDER
"""Token Nuker UI — core-style wrapper (nuker_ui).

Displays a small panel consistent with other tools and exposes the
Token Nuker actions (1-8). Uses the other tool's Helper plugs but
does not change console size or print the original banner art.
"""
import os
import sys
import importlib
from typing import Callable

# import core UI helpers from tools/discord
try:
    from core import _panel, _ask, _pause
except Exception:
    # fallback to simple console if core not importable
    def _panel(title, desc):
        print(f"== {title} ==\n{desc}\n")
    def _ask(prompt):
        return input(f"{prompt}: ").strip()
    def _pause():
        input("Press Enter to continue...")


def _ensure_other_tool_path():
    # other tool folder 'Wockstarz Multi' at repo root
    here = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(here))
    other_tool_dir = os.path.join(repo_root, 'Wockstarz Multi')
    if os.path.isdir(other_tool_dir) and other_tool_dir not in sys.path:
        sys.path.insert(0, other_tool_dir)
    return other_tool_dir if os.path.isdir(other_tool_dir) else None


def import_plugs():
    """Import Token Nuker plug functions from the other tool."""
    other = _ensure_other_tool_path()
    # clear cached imports to get fresh modules in correct context
    for m in ('Helper', 'Helper.Plugs.TokenNukerPlugs'):
        if m in sys.modules:
            del sys.modules[m]

    if not other:
        raise ModuleNotFoundError("other tool folder 'Wockstarz Multi' not found")

    prev_cwd = os.getcwd()
    try:
        os.chdir(other)
        # try default import first
        try:
            helper = importlib.import_module('Helper')
            plugs = importlib.import_module('Helper.Plugs.TokenNukerPlugs')
            return plugs
        except Exception:
            # fallback: load modules directly from filesystem
            import importlib.util
            helper_init = os.path.join(other, 'Helper', '__init__.py')
            plugs_init = os.path.join(other, 'Helper', 'Plugs', 'TokenNukerPlugs', '__init__.py')
            if not os.path.isfile(helper_init):
                raise ModuleNotFoundError(f"Helper __init__.py not found at {helper_init}")
            if not os.path.isfile(plugs_init):
                raise ModuleNotFoundError(f"TokenNukerPlugs __init__.py not found at {plugs_init}")

            # load Helper as module
            spec = importlib.util.spec_from_file_location('Helper', helper_init)
            helper_mod = importlib.util.module_from_spec(spec)
            sys.modules['Helper'] = helper_mod
            spec.loader.exec_module(helper_mod)

            # load TokenNukerPlugs as submodule under Helper.Plugs.TokenNukerPlugs
            spec2 = importlib.util.spec_from_file_location('Helper.Plugs.TokenNukerPlugs', plugs_init)
            plugs_mod = importlib.util.module_from_spec(spec2)
            sys.modules['Helper.Plugs.TokenNukerPlugs'] = plugs_mod
            spec2.loader.exec_module(plugs_mod)
            return plugs_mod
    finally:
        try:
            os.chdir(prev_cwd)
        except Exception:
            pass


def run_action(action: Callable, *args, **kwargs):
    try:
        action(*args, **kwargs)
    except Exception as e:
        print(f"Action error: {e}")


def main():
    _panel('Token Nuker', 'Run token nuker actions (1-8)')
    plugs = None
    try:
        plugs = import_plugs()
    except Exception as e:
        _panel('Error', f'Could not import nuker plugs: {e}')
        _pause()
        return

    # map choices to functions inside the plugs module
    mapping = {
        '1': ('Nuke Token', getattr(plugs, 'Nuke_account', None)),
        '2': ('Leave Servers', getattr(plugs, 'leaveServer', None)),
        '3': ('Delete Friends', getattr(plugs, 'deleteFriends', None)),
        '4': ('Delete Servers', getattr(plugs, 'deleteServers', None)),
        '5': ('Mass DM', getattr(plugs, 'massDM', None)),
        '6': ('Close DMs', getattr(plugs, 'close_all_dms', None)),
        '7': ('Block All Friends', getattr(plugs, 'blockAllFriends', None)),
        '8': ('Fuck account', getattr(plugs, 'fuckAccount', None)),
    }

    while True:
        print("\nOptions:\n")
        for k in sorted(mapping.keys()):
            print(f"  [{k}] {mapping[k][0]}")
        print("  [0] Exit")
        choice = _ask('Choice')
        if choice == '0' or not choice:
            break
        entry = mapping.get(choice)
        if not entry:
            print('Invalid choice')
            continue
        label, func = entry
        if not func:
            print(f"Function for {label} not available")
            continue

        # gather inputs per action
        if choice == '5':
            token = _ask('Discord token')
            msg = _ask('Message')
            run_action(func, token, msg)
        else:
            token = _ask('Discord token')
            run_action(func, token)

        _pause()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
