# coding: utf-8
from __future__ import annotations
import sys
import argparse
from typing import Tuple
import psutil
from ..utils.sys_info import SysInfo
from ..utils.question import query_yes_no


def _get_lo_process_names() -> Tuple[str, ...]:
    platform = SysInfo.get_platform()
    if platform == SysInfo.PlatformEnum.WINDOWS:
        return ("soffice.bin", "soffice.exe")
    else:
        return ("soffice.bin", "soffice")


def is_lo_process_running() -> bool:
    names = _get_lo_process_names()
    result = False
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() in names:
            result = True
            break
    return result


def kill_lo_process() -> bool:
    names = _get_lo_process_names()
    result = False
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() in names:
            result = True
            proc.kill()
    return result


def _args_main(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-r', '--running',
        help=f"Gets if soffice process is running",
        action='store_true',
        dest='running',
        default=False
    )
    parser.add_argument(
        '-k', '--kill',
        help="Kills soffice process if it is running",
        action='store_true',
        dest='kill',
        default=False
    )


def main() -> int:
    parser = argparse.ArgumentParser(description='main')
    _args_main(parser)

    if len(sys.argv) <= 1:
        parser.print_help()
        print("Other Commands, loapi, lodoc, loguide")
        return 0
    args = parser.parse_args()

    if bool(args.running) and bool(args.kill):
        parser.error(
            '--kill or --running options are not allowed to be combined.')

    if bool(args.running):
        print(f"Process running: {is_lo_process_running()}")
        return

    if bool(args.kill):
        if is_lo_process_running():
            if query_yes_no(f"Are you sure you want LibreOffice process'?", 'no'):
                print(f"Process killed: {kill_lo_process()}")
            else:
                print('User canceled')
        else:
            print('Nothing to kill')
    else:
        print('Nothing to kill')
    return 0
