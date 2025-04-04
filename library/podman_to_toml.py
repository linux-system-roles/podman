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
    use_new_formatter:
        description: Use new way to format sub-dict or not
        default: false
        type: bool

author:
    - Rich Megginson (@richm)
"""

EXAMPLES = """
- name: Convert to TOML
  podman_to_toml:
    data: "{{ podman_registries_conf }}"
    use_new_formatter: true
  register: __podman_to_toml

- name: Write TOML file
  copy:
    content: "{{ header + __podman_to_toml.toml }}"
    dest: /path/to/file.conf
"""

RETURN = """
toml:
  description: TOML representation of input data
  returned: always
  type: str
"""

import io
import sys
import datetime
import math

from ansible.module_utils.basic import AnsibleModule

# This part copied from python3-pytoml in el8
# which is also MIT license
if sys.version_info[0] == 3:
    long = int
    unicode = str


def dumps(obj, sort_keys=False):
    fout = io.StringIO()
    dump(obj, fout, sort_keys=sort_keys)
    return fout.getvalue()


_escapes = {'\n': 'n', '\r': 'r', '\\': '\\', '\t': 't', '\b': 'b', '\f': 'f', '"': '"'}


def _escape_string(s):
    res = []
    start = 0

    def flush():
        if start != i:
            res.append(s[start:i])
        return i + 1

    i = 0
    while i < len(s):
        c = s[i]
        if c in '"\\\n\r\t\b\f':
            start = flush()
            res.append('\\' + _escapes[c])
        elif ord(c) < 0x20:
            start = flush()
            res.append('\\u%04x' % ord(c))
        i += 1

    flush()
    return '"' + ''.join(res) + '"'


def _escape_id(s):
    if any(not c.isalnum() and c not in '-_' for c in s):
        return _escape_string(s)
    return s


def _format_list(v):
    return '[{0}]'.format(', '.join(_format_value(obj) for obj in v))


# Formula from:
#   https://docs.python.org/2/library/datetime.html#datetime.timedelta.total_seconds
# Once support for py26 is dropped, this can be replaced by td.total_seconds()
def _total_seconds(td):
    return ((td.microseconds
             + (td.seconds + td.days * 24 * 3600) * 10**6) / 10.0**6)


def _format_value(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int) or isinstance(v, long):
        return unicode(v)
    if isinstance(v, float):
        if math.isnan(v) or math.isinf(v):
            raise ValueError("{0} is not a valid TOML value".format(v))
        else:
            return repr(v)
    elif isinstance(v, unicode) or isinstance(v, bytes):
        return _escape_string(v)
    elif isinstance(v, datetime.datetime):
        offs = v.utcoffset()
        offs = _total_seconds(offs) // 60 if offs is not None else 0

        if offs == 0:
            suffix = 'Z'
        else:
            if offs > 0:
                suffix = '+'
            else:
                suffix = '-'
                offs = -offs
            suffix = '{0}{1:.02}{2:.02}'.format(suffix, offs // 60, offs % 60)

        if v.microsecond:
            return v.strftime('%Y-%m-%dT%H:%M:%S.%f') + suffix
        else:
            return v.strftime('%Y-%m-%dT%H:%M:%S') + suffix
    elif isinstance(v, list):
        return _format_list(v)
    else:
        raise RuntimeError(v)


def dump(obj, fout, sort_keys=False):
    tables = [((), obj, False)]

    while tables:
        name, table, is_array = tables.pop()
        if name:
            section_name = '.'.join(_escape_id(c) for c in name)
            if is_array:
                fout.write('[[{0}]]\n'.format(section_name))
            else:
                fout.write('[{0}]\n'.format(section_name))

        table_keys = sorted(table.keys()) if sort_keys else table.keys()
        new_tables = []
        has_kv = False
        for k in table_keys:
            v = table[k]
            if isinstance(v, dict):
                new_tables.append((name + (k,), v, False))
            elif isinstance(v, list) and v and all(isinstance(o, dict) for o in v):
                new_tables.extend((name + (k,), d, True) for d in v)
            elif v is None:
                # based on mojombo's comment: https://github.com/toml-lang/toml/issues/146#issuecomment-25019344
                fout.write(
                    '#{} = null  # To use: uncomment and replace null with value\n'.format(_escape_id(k)))
                has_kv = True
            else:
                fout.write('{0} = {1}\n'.format(_escape_id(k), _format_value(v)))
                has_kv = True

        tables.extend(reversed(new_tables))

        if (name or has_kv) and tables:
            fout.write('\n')
# This part copied from python3-pytoml in el8


def run_module():
    """The entry point of the module."""

    module_args = dict(
        data=dict(type="dict", required=True),
        use_new_formatter=dict(type="bool", default=False),
    )

    result = dict(changed=False)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    data = module.params["data"]
    if not module.params["use_new_formatter"]:
        for section in list(data):
            if isinstance(data[section], dict):
                for key, value in list(data[section].items()):
                    if isinstance(value, dict):
                        data[section][key] = ["{}={}".format(kk, vv) for kk, vv in value.items()]

    fp = io.StringIO()
    dump(data, fp)
    result["toml"] = fp.getvalue()
    module.exit_json(**result)


def main():
    """The main function!"""
    run_module()


if __name__ == "__main__":
    main()
