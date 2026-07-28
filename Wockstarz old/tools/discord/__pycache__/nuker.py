#!/usr/bin/env python3
# SAFE_PLACEHOLDER
"""Standalone wrapper to run the Token Nuker from the Wockstarz Multi tool.

This script adds the other tool's root folder to sys.path and switches cwd so
the Helper package (and its TokenNuker plugs) can be imported and executed
standalone from this project.
"""
import os
import sys
import importlib


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    # repo root is two levels up from tools/discord
    repo_root = os.path.dirname(os.path.dirname(here))
    # the other tool lives in a sibling folder named 'Wockstarz Multi'
    other_tool_dir = os.path.join(repo_root, 'Wockstarz Multi')

    prev_cwd = os.getcwd()
    prev_sys_path = list(sys.path)
    try:
        # prefer running inside the other tool dir so Helper imports resolve
        if os.path.isdir(other_tool_dir):
            target_dir = other_tool_dir
        else:
            # fallback to current tools/discord folder
            target_dir = here

        os.chdir(target_dir)
        if target_dir not in sys.path:
            sys.path.insert(0, target_dir)

        # clear cached Helper imports
        for m in ('Helper', 'tools.discord.Helper'):
            if m in sys.modules:
                del sys.modules[m]

        # import Helper from the other tool and run Token_nuker
        try:
            Helper = importlib.import_module('Helper')
        except Exception:
            # as a fallback try to import Token_Nuker directly from package path
            from Helper.Funcs2.Token_Nuker import Token_nuker as _tn
            _tn()
            return

        Token_nuker = getattr(Helper, 'Token_nuker', None)
        if not Token_nuker:
            # try nested module
            from Helper.Funcs2.Token_Nuker import Token_nuker as _tn
            Token_nuker = _tn

        Token_nuker()
    finally:
        try:
            os.chdir(prev_cwd)
        except Exception:
            pass
        sys.path[:] = prev_sys_path


if __name__ == '__main__':
    try:
        main()
    except Exception:
        import traceback
        print('Token Nuker crashed:')
        traceback.print_exc()
