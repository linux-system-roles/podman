# -*- coding: utf-8 -*-

# SPDX-License-Identifier: MIT

DOCUMENTATION = r"""
name: from_ini
short_description: Converts INI text input into a dictionary
version_added: 8.2.0
author: Rich Megginson (@richm)
description:
  - Converts INI text input into a dictionary.
options:
  _input:
    description: A string containing an INI document.
    type: string
    required: true
"""

EXAMPLES = r"""
- name: Slurp an INI file
  ansible.builtin.slurp:
    src: /etc/rhsm/rhsm.conf
  register: rhsm_conf

- name: Display the INI file as dictionary
  ansible.builtin.debug:
    var: rhsm_conf.content | b64decode | community.general.from_ini

- name: Set a new dictionary fact with the contents of the INI file
  ansible.builtin.set_fact:
    rhsm_dict: >-
      {{
          rhsm_conf.content | b64decode | community.general.from_ini
      }}
"""

RETURN = r"""
_value:
  description: A dictionary representing the INI file.
  type: dictionary
"""

from ansible.errors import AnsibleFilterError
from ansible.module_utils.six import string_types


def from_ini(obj):
    """Read the given string as INI file and return a dict"""

    if not isinstance(obj, string_types):
        raise AnsibleFilterError("from_ini requires a str, got %s" % type(obj))

    rv = {}
    section = "DEFAULT"
    for line in obj.split("\n"):
        if len(line) == 0 or line.startswith("#"):
            continue
        if line.startswith("["):
            val = line.replace("[", "").replace("]", "")
            section = val
        else:
            key, val = line.split("=", 1)
            sect_dict = rv.setdefault(section, {})
            cur_val = sect_dict.get(key)
            if cur_val is not None:
                if not isinstance(cur_val, list):
                    cur_val = [cur_val]
                cur_val.append(val)
                sect_dict[key] = cur_val
            else:
                sect_dict[key] = val
    return rv


class FilterModule(object):
    """Query filter"""

    def filters(self):
        return {"podman_from_ini": from_ini}
