# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Red Hat, Inc.
# SPDX-License-Identifier: MIT
"""Resolve a relative path the way Quadlet does."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os

from ansible.module_utils.six import string_types


def _resolve(path, base):
    if path.startswith("."):
        return os.path.normpath(os.path.join(base, path))
    return path


def podman_resolve_relative_path(paths, base):
    """Resolve paths that start with '.' against base.

    Quadlet resolves a source that starts with '.' relative to the directory
    of the unit file, using filepath.Join, which cleans the result lexically
    ('.' and '..' components are removed, symlinks are not resolved).
    os.path.normpath does the same. Other paths are returned unchanged.
    Accepts a single path or a list of paths.
    """
    if isinstance(paths, string_types):
        return _resolve(paths, base)
    return [_resolve(path, base) for path in paths]


class FilterModule(object):
    def filters(self):
        return {
            "podman_resolve_relative_path": podman_resolve_relative_path,
        }
