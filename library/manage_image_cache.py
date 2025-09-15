#!/usr/bin/python
# Copyright: (c) 2025, Red Hat, Inc.
# SPDX-License-Identifier: MIT
# NOTE: This module was mostly written by claude-4-sonnet in the Cursor IDE

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: manage_image_cache

short_description: Manage physically bound container images for bootc systems

version_added: "1.0.0"

description:
    - This module manages physically bound container images as described in the Fedora bootc documentation.
    - It copies container images to a cache directory using skopeo, similar to how bootc embeds images.
    - Images are stored in the /usr/lib/containers-image-cache directory structure.

options:
    images:
        description:
            - List of container image names to cache
        required: true
        type: list
        elements: str
    username:
        description:
            - Username for registry authentication
        required: false
        type: str
    password:
        description:
            - Password for registry authentication
            - Optional even when username is provided, as some registries allow username-only authentication
        required: false
        type: str
    validate_certs:
        description:
            - Whether to validate TLS certificates when pulling images
        required: false
        type: bool
        default: true
    cache_dir:
        description:
            - Directory where images will be cached
        required: false
        type: str
        default: "/var/lib/lsr_podman_image_cache"
    preserve_digests:
        description:
            - Whether to preserve image digests when copying
        required: false
        type: bool
        default: true
    state:
        description:
            - Whether images should be present or absent in the cache
        required: false
        type: str
        choices: ['present', 'absent']
        default: present

author:
    - Rich Megginson (@richm)
"""

EXAMPLES = r"""
- name: Cache container images for bootc
  manage_image_cache:
    images:
      - "registry.fedoraproject.org/fedora:latest"
      - "docker.io/library/busybox:latest"
      - "quay.io/myorg/myapp:v1.0"
    username: "myuser"
    password: "mypass"
    validate_certs: true

- name: Cache images without certificate validation
  manage_image_cache:
    images:
      - "internal-registry.company.com/app:latest"
    validate_certs: false

- name: Cache images with username-only authentication
  manage_image_cache:
    images:
      - "registry.example.com/private/app:latest"
    username: "myuser"
    # password is optional - some registries allow username-only auth

- name: Remove cached images
  manage_image_cache:
    images:
      - "registry.fedoraproject.org/fedora:latest"
      - "docker.io/library/busybox:latest"
    state: absent
"""

RETURN = r"""
results:
    description: Results for each image
    returned: always
    type: list
    elements: dict
    contains:
        image:
            description: The image name that was processed
            type: str
            returned: always
        changed:
            description: Whether the image was actually copied/updated
            type: bool
            returned: always
        skipped:
            description: Whether the image operation was skipped
            type: bool
            returned: always
        failed:
            description: Whether the image operation failed
            type: bool
            returned: always
        msg:
            description: Human readable message about what happened
            type: str
            returned: always
        cache_path:
            description: Path where the image was cached
            type: str
            returned: when changed is true
"""

import os
import hashlib
import shutil
from ansible.module_utils.basic import AnsibleModule


def run_skopeo_copy(
    module,
    src_image,
    dest_dir,
    username=None,
    password=None,
    validate_certs=True,
    preserve_digests=True,
):
    """Run skopeo copy command to cache an image"""

    cmd = ["skopeo", "copy"]

    if preserve_digests:
        cmd.append("--preserve-digests")

    # Add credentials if provided
    if username:
        if password:
            cmd.extend(["--src-creds", f"{username}:{password}"])
        else:
            cmd.extend(["--src-creds", username])

    # Add certificate validation option
    if validate_certs is not None:
        if validate_certs:
            cmd.append("--src-tls-verify=true")
        else:
            cmd.append("--src-tls-verify=false")

    # Add source and destination
    cmd.extend([f"docker://{src_image}", f"dir:{dest_dir}"])

    rc, stdout, stderr = module.run_command(cmd)

    if rc == 0:
        return True, stdout, None
    else:
        return False, stdout, stderr


def get_image_cache_path(cache_dir, image_name):
    """Generate a cache path for an image based on its name hash"""
    # Create a hash of the image name to use as directory name
    image_hash = hashlib.sha256(image_name.encode()).hexdigest()[:16]
    return os.path.join(cache_dir, image_hash)


def is_image_cached(cache_path):
    """Check if an image is already cached"""
    manifest_path = os.path.join(cache_path, "manifest.json")
    return (
        os.path.exists(cache_path)
        and os.path.isdir(cache_path)
        and os.path.exists(manifest_path)
    )


def has_mapping_entry(mapping_file, mapping_entry):
    with open(mapping_file, "r") as ff:
        file_lines = [line.strip() for line in ff.readlines()]
        return mapping_entry.strip() in file_lines


MAPPING_HEADER = "# Ansible Managed - DO NOT EDIT\n# system_role:podman\n"


def update_mapping_file(cache_dir, image_name, image_sha):
    """Update the mapping file with image name to SHA mapping"""
    mapping_file = os.path.join(cache_dir, "mapping.txt")
    mapping_entry = f"{image_name},{image_sha}\n"

    try:
        # Check if mapping already exists
        if os.path.exists(mapping_file) and has_mapping_entry(
            mapping_file, mapping_entry
        ):
            return True, None

        # If file doesn't exist, create it with header
        if not os.path.exists(mapping_file):
            with open(mapping_file, "w") as ff:
                ff.write(MAPPING_HEADER)

        # Append new mapping
        with open(mapping_file, "a") as ff:
            ff.write(mapping_entry)
        return True, None
    except Exception as e:
        return False, str(e)


def remove_from_mapping_file(cache_dir, image_name, image_sha):
    """Remove the mapping from the mapping file"""
    mapping_file = os.path.join(cache_dir, "mapping.txt")
    mapping_entry = f"{image_name},{image_sha}"

    try:
        if not os.path.exists(mapping_file):
            return True, None

        # Read all lines and filter out the one to remove
        with open(mapping_file, "r") as ff:
            lines = [line for line in ff.readlines() if line.strip() != mapping_entry]

        # Write back the content minus the mapping entry
        with open(mapping_file, "w") as ff:
            ff.writelines(lines)

        return True, None
    except Exception as e:
        return False, str(e)


def remove_cached_image(cache_path):
    """Remove a cached image directory"""
    try:
        if os.path.exists(cache_path) and os.path.isdir(cache_path):
            shutil.rmtree(cache_path)
            return True, None
        else:
            return True, "Directory does not exist"
    except Exception as e:
        return False, str(e)


def run_module():
    module_args = dict(
        images=dict(type="list", elements="str", required=True),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
        validate_certs=dict(type="bool", required=False, default=True),
        cache_dir=dict(
            type="str", required=False, default="/var/lib/lsr_podman_image_cache"
        ),
        preserve_digests=dict(type="bool", required=False, default=True),
        state=dict(
            type="str", required=False, default="present", choices=["present", "absent"]
        ),
    )

    result = dict(changed=False, results=[])

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    images = module.params["images"]
    username = module.params["username"]
    password = module.params["password"]
    validate_certs = module.params["validate_certs"]
    cache_dir = module.params["cache_dir"]
    preserve_digests = module.params["preserve_digests"]
    state = module.params["state"]

    overall_changed = False
    overall_failed = False

    for image in images:
        image_result = {
            "image": image,
            "changed": False,
            "skipped": False,
            "failed": False,
            "msg": "",
        }

        try:
            cache_path = get_image_cache_path(cache_dir, image)
            image_sha = os.path.basename(cache_path)  # Extract SHA from cache path

            if state == "present":
                # Check if image is already cached
                if is_image_cached(cache_path):
                    image_result["skipped"] = True
                    image_result["msg"] = (
                        f"Image {image} already cached at {cache_path}"
                    )
                else:
                    if module.check_mode:
                        image_result["changed"] = True
                        image_result["msg"] = (
                            f"Would cache image {image} to {cache_path}"
                        )
                    else:
                        # Copy image to cache
                        success, stdout, stderr = run_skopeo_copy(
                            module,
                            image,
                            cache_path,
                            username,
                            password,
                            validate_certs,
                            preserve_digests,
                        )
                        image_result["stdout"] = stdout
                        if success:
                            image_result["changed"] = True
                            image_result["cache_path"] = cache_path
                            image_result["msg"] = (
                                f"Successfully cached image {image} to {cache_path}"
                            )
                            overall_changed = True

                            # Update mapping file with image name and SHA
                            mapping_success, mapping_error = update_mapping_file(
                                cache_dir, image, image_sha
                            )
                            if not mapping_success:
                                module.warn(
                                    f"Failed to update mapping file: {mapping_error}"
                                )
                        else:
                            image_result["failed"] = True
                            error_msg = f"Failed to cache image {image}"
                            if stderr:
                                error_msg += f": {stderr}"
                            image_result["msg"] = error_msg
                            overall_failed = True
            elif state == "absent":
                # Check if image is cached and remove it
                if is_image_cached(cache_path):
                    if module.check_mode:
                        image_result["changed"] = True
                        image_result["msg"] = (
                            f"Would remove cached image {image} from {cache_path}"
                        )
                    else:
                        # Remove cached image
                        remove_success, remove_error = remove_cached_image(cache_path)

                        if remove_success:
                            image_result["changed"] = True
                            image_result["msg"] = (
                                f"Successfully removed cached image {image} from {cache_path}"
                            )
                            overall_changed = True

                            # Remove from mapping file using image name and SHA
                            mapping_success, mapping_error = remove_from_mapping_file(
                                cache_dir, image, image_sha
                            )
                            if not mapping_success:
                                module.warn(
                                    f"Failed to update mapping file: {mapping_error}"
                                )
                        else:
                            image_result["failed"] = True
                            image_result["msg"] = (
                                f"Failed to remove cached image {image}: {remove_error}"
                            )
                            overall_failed = True
                else:
                    image_result["skipped"] = True
                    image_result["msg"] = f"Image {image} not cached at {cache_path}"

        except Exception as e:
            image_result["failed"] = True
            image_result["msg"] = f"Error processing image {image}: {str(e)}"
            overall_failed = True
        result["results"].append(image_result)

    result["changed"] = overall_changed
    result["failed"] = overall_failed
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
