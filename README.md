# Role Name
![CI Testing](https://github.com/linux-system-roles/podman/workflows/tox/badge.svg)

This role manages `podman` configuration, containers, and systemd services which
run `podman` containers.

## Requirements

The role requires `containers.podman` collection.  If you are using
`ansible-core`, you must install this collection.
```
ansible-galaxy collection install -vv -r meta/collection-requirements.yml
```
If you are using Ansible Engine 2.9, or are using an Ansible bundle which
includes these collections/modules, you should have to do nothing.

## Role Variables

### podman_containers

This is a `list`.  Each element of the list is a `dict` describing a podman
container and corresponding systemd unit to manage.  The format of the `dict` is
mostly like the [podman_container
module](https://docs.ansible.com/ansible/latest/collections/containers/podman/podman_container_module.html#ansible-collections-containers-podman-podman-container-module)
except for the following:

* `generate_systemd.container_prefix` is hard-coded to `lsr_container`
* `generate_systemd.separator` is hard-coded to `-`
* `generate_systemd.path` is hard-coded to `/etc/systemd/system` for root
  containers, and `$HOME/.config/systemd/user` for non-root containers

### podman_create_host_directories

This is a boolean, default value is `false`.  If `true`, the role will ensure
host directories specified in host mounts in `volume` and `mount` specifications
for the containers in `podman_containers`.  NOTE: Directories must be specified
as absolute paths (for root containers), or paths relative to the home directory
(for non-root containers), in order for the role to manage them.  Anything else
will be assumed to be some other sort of volume and will be ignored.
The role will apply its default ownership/permissions to the directories. If you
need to set ownership/permissions, see `podman_host_directories`.

### podman_host_directories

This is a `dict`.  When using `podman_create_host_directories`, this tells the
role what permissions/ownership to apply to automatically created host
directories.  Each key is the absolute path of host directory to manage. The
value is in the format of the parameters to the [file
module](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html#ansible-collections-ansible-builtin-file-module).
If you do not specify a value, the role will use its built-in default values. If
you want to specify a value to be used for all host directories, use the special
key `DEFAULT`.

```yaml
podman_host_directories:
  "/var/lib/data":
    owner: dbuser
    group: dbgroup
    mode: "0600"
  DEFAULT:
    owner: root
    group: root
    mode: "0644"
```
The role will use `dbuser:dbgroup` `0600` for `/var/lib/data`, and `root:root`
`0644` for all other host directories created by the role.

A description of all input variables (i.e. variables that are defined in
`defaults/main.yml`) for the role should go here as these form an API of the
role.

### Variables Exported by the Role

None

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  vars:
    podman_foo: foo foo!
    podman_bar: progress bar

  roles:
    - linux-system-roles.podman
```

## License

MIT.

## Author Information

Based on `podman-container-systemd` by Ilkka Tengvall <ilkka.tengvall@iki.fi>.

Authors: Thom Carlin, Valentin Rothberg, Rich Megginson
