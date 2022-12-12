# podman
![CI Testing](https://github.com/linux-system-roles/podman/workflows/tox/badge.svg)

This role manages `podman` configuration, containers, and systemd services which
run `podman` containers.

## Requirements

The role requires podman version 4.2 or later.

The role requires the following collections:
* `containers.podman`
* `fedora.linux_system_roles` 
Use this to install the collections:
```
ansible-galaxy collection install -vv -r meta/collection-requirements.yml
```

### Users, groups, subuid, subgid

Users and groups specified in `podman_run_as_user`, `podman_run_as_group`, and
specified in a kube spec as `run_as_user` and `run_as_group` have the following
restrictions:
* They must be already present on the system - the role will not create the
  users or groups - the role will exit with an error if a non-existent user or
  group is specified
* They must already exist in `/etc/subuid` and `/etc/subgid` - the role will
  exit with an error if a specified user is not present in `/etc/subuid`, or if
  a specified group is not in `/etc/subgid`

## Role Variables

### podman_kube_specs

This is a `list`.  Each element of the list is a `dict` describing a podman
pod and corresponding systemd unit to manage.  The format of the `dict` is
mostly like the [podman_play
module](https://docs.ansible.com/ansible/latest/collections/containers/podman/podman_play_module.html#ansible-collections-containers-podman-podman-play-module)
except for the following:

* `run_as_user` - Use this to specify a per-pod user.  If you do not
  specify this, then the global default `podman_run_as_user` value will be used.
  Otherwise, `root` will be used.  NOTE: The user must already exist - the role
  will not create.  The user must be present in `/etc/subuid`.
* `run_as_group` - Use this to specify a per-pod group.  If you do not
  specify this, then the global default `podman_run_as_group` value will be
  used.  Otherwise, `root` will be used.  NOTE: The group must already exist -
  the role will not create.  The group must be present in `/etc/subgid`.
* `systemd_unit_scope` - The scope to use for the systemd unit.  If you do not
  specify this, then the global default `podman_systemd_unit_scope` will be
  used.  Otherwise, the scope will be `system` for root containers, and `user`
  for user containers.
* `kube_file_src` - This is the name of a file on the controller node which will
  be copied to `kube_file` on the managed node.  This is a file in Kubernetes
  YAML format.  Do not specify this if you specify `kube_file_content`.
  `kube_file_content` takes precedence over `kube_file_src`.
* `kube_file_content` - This is either a string in Kubernetes YAML format, or a
  `dict` in Kubernetes YAML format.  It will be used as the contents of
  `kube_file` on the managed node.  Do not specify this if you specify
  `kube_file_src`. `kube_file_content` takes precedence over `kube_file_src`.
* `kube_file` - This is the name of a file on the managed node that contains the
  Kubernetes specification of the container/pod.  You typically do not have to specify
  this unless you need to somehow copy this file to the managed node outside of the
  role.  If you specify either `kube_file_src` or `kube_file_content`, you
  do not have to specify this.  It is highly recommended to omit `kube_file` and
  instead specify either `kube_file_src` or `kube_file_content` and let the role
  manage the file path and name.
  * The file basename will be the `metadata.name` value from the K8s yaml, with a
    `.yml` suffix appended to it.
  * The directory will be `/etc/containers/ansible-kubernetes.d` for system services.
  * The directory will be `$HOME/.config/containers/ansible-kubernetes.d` for user services.

For example, if you have
```yaml
    podman_kube_specs:
      - state: started
        kube_file_content:
          apiVersion: v1
          kind: Pod
          metadata:
            name: myappname
```
This will be copied to the file `/etc/containers/ansible-kubernetes.d/myappname.yml` on
the managed node.

### podman_create_host_directories

This is a boolean, default value is `false`.  If `true`, the role will ensure
host directories specified in host mounts in `volumes.hostPath` specifications
in the Kubernetes YAML given in `podman_kube_specs`.  NOTE: Directories must be
specified as absolute paths (for root containers), or paths relative to the home
directory (for non-root containers), in order for the role to manage them.
Anything else will be assumed to be some other sort of volume and will be
ignored. The role will apply its default ownership/permissions to the
directories. If you need to set ownership/permissions, see
`podman_host_directories`.

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
specify per-container username with `run_as_user` in `podman_kube_specs`.  NOTE:
The user must already exist - the role will not create.  The user must be
present in `/etc/subuid`.

### podman_run_as_group

This is the name of the group to use for all rootless containers.  You can also
specify per-container group name with `run_as_group` in `podman_kube_specs`.
NOTE: The group must already exist - the role will not create.  The group must
be present in `/etc/subgid`.

### podman_systemd_unit_scope

This is systemd scope to use by default for all systemd units.  You can also
specify per-container scope with `systemd_unit_scope` in `podman_kube_specs`. By
default, rootless containers will use `user` and root containers will use
`system`.

### podman_containers_conf

These are the containers.conf(5) settings, provided as a `dict`.  These settings
will be provided in a drop-in file in the `containers.conf.d` directory.  If
running as root (see `podman_run_as_user`), the system settings will be managed,
otherwise, the user settings will be managed.  See the man page for the
directory locations.

```yaml
podman_containers_conf:
  containers:
    default_sysctls:
      - net.ipv4.ping_group_range=0 1000
      - user.max_ipc_namespaces=125052
```

### podman_registries_conf

These are the containers-registries.conf(5) settings, provided as a `dict`.
These settings will be provided in a drop-in file in the `registries.conf.d`
directory.  If running as root (see `podman_run_as_user`), the system settings
will be managed, otherwise, the user settings will be managed.  See the man page
for the directory locations.

```yaml
podman_registries_conf:
  aliases:
    myregistry: registry.example.com
```

### podman_storage_conf

These are the containers-storage.conf(5) settings, provided as a `dict`.  If
running as root (see `podman_run_as_user`), the system settings will be managed,
otherwise, the user settings will be managed.  See the man page for the file
locations.

```yaml
podman_storage_conf:
  storage:
    runroot: /var/big/partition/container/storage
```

### podman_policy_json

These are the containers-policy.json(5) settings, provided as a `dict`.  If
running as root (see `podman_run_as_user`), the system settings will be managed,
otherwise, the user settings will be managed.  See the man page for the file
locations.

```yaml
podman_policy_json:
  default:
    type: insecureAcceptAnything
```

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
      - port: 12340/tcp
        state: enabled
    podman_selinux_ports:
      - ports: 8080-8081
        setype: http_port_t
    podman_kube_specs:
      - state: started
        run_as_user: dbuser
        run_as_group: dbgroup
        kube_file_content:
          apiVersion: v1
          kind: Pod
          metadata:
            name: db
          spec:
            containers:
              - name: db
                image: quay.io/db/db:stable
                ports:
                  - containerPort: 1234
                    hostPort: 12340
                volumeMounts:
                  - mountPath: /var/lib/db:Z
                    name: db
            volumes:
              - name: db
                hostPath:
                  path: /var/lib/db
      - state: started
        run_as_user: webapp
        run_as_group: webapp
        kube_file_src: /path/to/webapp.yml
  roles:
    - linux-system-roles.podman
```

## License

MIT.

## Author Information

Based on `podman-container-systemd` by Ilkka Tengvall <ilkka.tengvall@iki.fi>.

Authors: Thom Carlin, Rich Megginson, Adam Miller, Valentin Rothberg
