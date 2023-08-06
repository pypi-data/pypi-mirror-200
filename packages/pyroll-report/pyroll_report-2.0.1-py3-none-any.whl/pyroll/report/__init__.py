from .report import report
from .pluggy import plugin_manager, hookimpl, hookspec
from .config import Config

from . import hookspecs

plugin_manager.add_hookspecs(hookspecs)

from . import unit_display

import importlib.util

CLI_INSTALLED = bool(importlib.util.find_spec("pyroll.cli"))

if CLI_INSTALLED:
    from . import cli

VERSION = "2.0.1"
