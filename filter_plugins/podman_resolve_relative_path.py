# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Red Hat, Inc.
# SPDX-License-Identifier: MIT
"""Resolve a relative path the way Quadlet does."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os


def podman_resolve_relative_path(path, base):
    """Resolve path against base if path starts with '.'.

    Quadlet resolves a source that starts with '.' relative to the directory
    of the unit file, using filepath.Join, which cleans the result lexically
    ('.' and '..' components are removed, symlinks are not resolved).
    os.path.normpath does the same. Other paths are returned unchanged.
    """
    if path.startswith("."):
        return os.path.normpath(os.path.join(base, path))
    return path


class FilterModule(object):
    def filters(self):
        return {
            "podman_resolve_relative_path": podman_resolve_relative_path,
        }
