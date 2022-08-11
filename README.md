# Role Name
![CI Testing](https://github.com/linux-system-roles/podman/workflows/tox/badge.svg)

This role manages `podman` configuration, containers, and systemd services which
run `podman` containers.

## Requirements

The role requires the following collections:
* `containers.podman`
* `fedora.linux_system_roles` 
Use this to install the collections:
```
ansible-galaxy collection install -vv -r meta/collection-requirements.yml
```

## Role Variables

### podman_containers

This is a `list`.  Each element of the list is a `dict` describing a podman
container and corresponding systemd unit to manage.  The format of the `dict` is
mostly like the [podman_container
module](https://docs.ansible.com/ansible/latest/collections/containers/podman/podman_container_module.html#ansible-collections-containers-podman-podman-container-module)
except for the following:

* `generate_systemd` - If you specify a value of `true`, then the role will
  create a systemd unit to run the container using the role default variables.
  Or, you can specify a `dict` in the `podman_container` module format.
* `generate_systemd.container_prefix` is hard-coded to `lsr_container`
* `generate_systemd.separator` is hard-coded to `-`
* `generate_systemd.path` is hard-coded to `/etc/systemd/system` for root
  containers, and `$HOME/.config/systemd/user` for non-root containers
* `run_as_user` - Use this to specify a per-container user.  If you do not
  specify this, then the global default `podman_run_as_user` value will be used.
  Otherwise, `root` will be used.  NOTE: The user must already exist - the role
  will not create.
* `run_as_group` - Use this to specify a per-container group.  If you do not
  specify this, then the global default `podman_run_as_group` value will be
  used.  Otherwise, `root` will be used.  NOTE: The group must already exist -
  the role will not create.
* `systemd_unit_scope` - The scope to use for the systemd unit.  If you do not
  specify this, then the global default `podman_systemd_unit_scope` will be
  used.  Otherwise, the scope will be `system` for root containers, and `user`
  for user containers.

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

### podman_firewall

This is a `list` of `dict` in the same format as used by the
`fedora.linux_system_roles.firewall` role.  Use this to specify ports that you
want the role to manage in the firewall.

```yaml
podman_firewall:
  - port: 8080/tcp
```

### podman_selinux_ports

This is a `list` of `dict` in the same format as used by the
`fedora.linux_system_roles.selinux` role.  Use this if you want the role to
manage the SELinux policy for ports used by the role.

```yaml
podman_selinux_ports:
  - ports: 8080
    protocol: tcp
    setype: http_port_t
```

### podman_run_as_user

This is the name of the user to use for all rootless containers.  You can also
specify per-container username with `run_as_user` in `podman_containers`.  NOTE:
  The user must already exist - the role will not create.

### podman_run_as_group

This is the name of the group to use for all rootless containers.  You can also
specify per-container group name with `run_as_group` in `podman_containers`.
  NOTE: The group must already exist - the role will not create.

### podman_systemd_unit_scope

This is systemd scope to use by default for all systemd units.  You can also
specify per-container scope with `systemd_unit_scope` in `podman_containers`. By
default, rootless containers will use `user` and root containers will use
`system`.

## Variables Exported by the Role

None

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  vars:
    podman_create_host_directories: true
    podman_firewall:
      - port: 8080-8081/tcp
        state: enabled
    podman_selinux_ports:
      - ports: 8080-8081
        setype: http_port_t
    podman_containers:
      - name: my_user_service
        image: quay.io/a_service/an_image:v4.1
        rm: true
        tty: true
        volume:
          - /var/lib/my_service:/var/www:Z
        publish:
          - "8080:80"
        generate_systemd: true
        command: /bin/busybox-extras httpd -f -p 80
        workdir: /var/www
        run_as_user: dbuser
        run_as_group: dbgroup
        labels:
          io.containers.autoupdate: registry
      - name: my_system_service
        image: quay.io/another_service/an_image:v4.2
        rm: true
        tty: true
        volume:
          - /var/lib/my_service:/var/www:Z
        publish:
          - "8081:80"
        generate_systemd:
          restart_policy: always
        command: /bin/busybox-extras httpd -f -p 80
        workdir: /var/www
        labels:
          io.containers.autoupdate: registry
```

## License

MIT.

## Author Information

Based on `podman-container-systemd` by Ilkka Tengvall <ilkka.tengvall@iki.fi>.

Authors: Adam Miller, Thom Carlin, Valentin Rothberg, Rich Megginson
