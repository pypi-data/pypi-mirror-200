#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script.

This script executes the unit tests for the package.

"""

from contextlib import redirect_stdout
from os import devnull
from pathlib import Path
from subprocess import DEVNULL, run
from unittest import main, TestCase

from stemplate.core import colors, files
from stemplate.main import date, head


directory = Path(__file__).parent


def runcheck(command):
    """Run a command and check the exit code.

    Parameters
    ----------
    command : str
        Command to be runned.

    Raises
    ------
    CalledProcessError
        If the command exited with an error code.

    """
    run(command, shell=True, check=True, stdout=DEVNULL)


class TestCore(TestCase):

    def test_files_get_content(self):
        content = files.get_beginning(directory/'data.txt', 1)
        self.assertEqual("There is not data here.\n", content)

    def test_files_get_size(self):
        size = files.get_size(directory/'data.txt')
        self.assertEqual(24, size)

    def test_colors_get_code(self):
        code = colors.get_code('red')
        self.assertEqual('\033[31m', code)


class TestMain(TestCase):

    def test_head(self):
        with redirect_stdout(None):
            head.main(file=f'{directory}/data.txt')

    def test_date(self):
        with redirect_stdout(None):
            date.main()


class TestCommandLineInterface(TestCase):

    def test_help(self):
        runcheck("stemplate --help")
        runcheck("stemplate head --help")
        runcheck("stemplate date --help")

    def test_head(self):
        runcheck(f"stemplate head {directory}/data.txt")
        runcheck(f"stemplate -c {directory}/custom.conf head {directory}/data.txt")

    def test_date(self):
        runcheck(f"stemplate date")
        runcheck(f"stemplate -c {directory}/custom.conf date")


if __name__ == '__main__':
    main()
