import os
import subprocess


def run_command(command, hide_std=False):
    if hide_std:
        with open(os.devnull, 'w') as dev_null:
            return subprocess.call(command,
                                   shell=True,
                                   stdout=dev_null,
                                   stderr=dev_null)
    return subprocess.call(command, shell=True)
