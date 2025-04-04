#!/usr/bin/python
# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT
# Copyright: (c) 2025, Red Hat, Inc.
#
"""Convert given python object to TOML string representation."""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: podman_to_toml

short_description: Convert given python object to TOML string representation.

version_added: "2.13.0"

description:
    - "WARNING: Do not use this module directly! It is only for role internal use."
    - Convert given python object to TOML string representation

options:
    data:
        description: Python/Ansible object to convert to TOML
        required: true
        type: dict

author:
    - Rich Megginson (@richm)
"""

EXAMPLES = """
- name: Convert to TOML
  podman_to_toml:
    data: "{{ podman_registries_conf }}"
  register: __podman_to_toml

- name: Write TOML file
  copy:
    content: "{{ header + __podman_to_toml.toml }}
    dest: /path/to/file.conf
"""

RETURN = """
toml:
  description: TOML representation of input data
  returned: always
  type: str
"""

import io
try:
    import pytoml

    HAS_PYTOML = True
except ImportError:
    HAS_PYTOML = False

try:
    import toml

    HAS_TOML = True
except ImportError:
    HAS_TOML = False


from ansible.module_utils.basic import AnsibleModule


def run_module():
    """The entry point of the module."""

    module_args = dict(
        data=dict(type="dict", required=True),
    )

    result = dict(changed=False)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    fp = io.StringIO()
    if HAS_PYTOML:
        pytoml.dump(module.params["data"], fp)
    elif HAS_TOML:
        toml.dump(module.params["data"], fp, toml.TomlEncoder)
    else:
        module.fail_json(msg="No toml python library found")
    result["toml"] = fp.getvalue()
    module.exit_json(**result)


def main():
    """The main function!"""
    run_module()


if __name__ == "__main__":
    main()
