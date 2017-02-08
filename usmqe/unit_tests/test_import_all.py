# -*- coding: utf8 -*-
"""
Very basic check of all usmqe modules. We try to just import every module
inside usmqe module, which would fail on a syntax error if the module is not
compatible.
"""

import importlib
import pkgutil

import pytest


def list_submodules(module_path, module_prefix):
    """
    For given module, return list of full module path names for all submodules
    recursively.
    """
    return [name for _, name, _ in
            pkgutil.walk_packages(path=[module_path], prefix=module_prefix)]


# parametrize makes this case run for every submodule in webstr module
@pytest.mark.parametrize("module", list_submodules("../usmqe", "usmqe."))
def test_import(module):
    """
    Just try to import given module.
    """
    try:
        importlib.import_module(module)
    # TODO: FIXME Remove try except block when webstr will be public
    except ImportError as exc:
        if 'webstr' not in str(exc):
            raise exc
