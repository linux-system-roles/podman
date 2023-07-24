# podman

![CI Testing](https://github.com/linux-system-roles/podman/workflows/tox/badge.svg)

This role manages `podman` configuration, containers, and systemd services which
run `podman` containers.

## Requirements

The role requires podman version 4.2 or later.
The role requires podman version 4.4 or later for quadlet support and secret
support.
The role requires podman version 4.5 or later for support for using healthchecks
(only supported when using quadlet Container types).

### Collection requirements

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

* `state` - default is `created`.  This takes 3 values:
   * `started` - Create the pods and systemd services, and start them running
   * `created` - Create the pods and systemd services, but do not start them
   * `absent` - Remove the pods and systemd services
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
* `activate_systemd_unit` - Whether or not to activate the systemd unit when it
  is created.  If you do not specify this, then the global default
  `podman_activate_systemd_unit` will be used, which is `true` by default.
* `pull_image` - Ensure the image is pulled before use.  If you do not specify
  this, then the global default `podman_pull_image` will be used, which is
  `true` by default.
* `continue_if_pull_fails` - If pulling the image, and the pull fails, do not
  treat this as a fatal error, and continue with the role.  If you do not
  specify this, then the global default `podman_continue_if_pull_fails` will be
  used, which is `false` by default.
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

### podman_quadlet_specs

List of [Quadlet specifications]
(https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)
A quadlet spec is uniquely identified by a name and a type, where type is one of
the types of units like container, kube, network, volume, etc.  You can either
pass in `name` and `type` explicitly, or the `name` and `type` will be derived
from the file name given in `file`, `file_src`, or `template_src`.

By default, the files will be copied to or created in
`/etc/containers/systemd/$name.$type` for root containers, and
`$HOME/.config/containers/systemd/$name.$type` for rootless containers, on the
managed node.  You can provide a different location by using `file`, but then
you will likely need to change the systemd configuration to find the file, which
is not supported by this role.

When a quadlet spec depends on some other file e.g. a `quadlet.kube` that
depends on the `Yaml` file or a `ConfigMap`, then that file must be specified in
the `podman_quadlet_specs` list *before* the file that uses it.  For example, if
you have a file `my-app.kube`:

```ini
[Kube]
ConfigMap=my-app-config.yml
Yaml=my-app.yml
...
```

Then you must specify `my-app-config.yml` and `my-app.yml` before `my-app.kube`:

```yaml
podman_quadlet_specs:
  - file_src: my-app-config.yml
  - file_src: my-app.yml
  - file_src: my-app.kube
```

Most of the parameters for each quadlet spec are the same as for
`podman_kube_spec` above except that the `*kube*` parameters are not supported,
and the following are:

* `name` - The name of the unit.  If not given, it will be derived from `file`,
  `file_src`, or `template_src`.  For example, if you specify
  `file_src: /path/to/my-container.container` then the `name` will
  be `my-container`.
* `type` - The type of unit (container, kube, volume, etc.).  If not given, it
  will be derived from `file`, `file_src`, or `template_src`.  For example, if
  you specify `file_src: /path/to/my-container.container` then the `type` will
  be `container`.  If the derived type is not recognized as a valid quadlet type,
  for example, if you specify `file_src: my-kube.yml`, then it will just be copied
  and not processed as a quadlet spec.
* `file_src` - The name of the file on the control node to copy to the managed
  node to use as the source of the quadlet unit.  If this file is in the quadlet
  unit format and has a valid quadlet unit suffix, it will be used as a quadlet
  unit, otherwise, it will just be copied.
* `file` - The name of the file on the managed node to use as the source of the
  quadlet unit.  If this file is in the quadlet unit format and has a valid
  quadlet unit suffix, it will be used as a quadlet unit, otherwise, it will be
  treated as a regular file.
* `file_content` - The contents of a file to copy to the managed node, in string
  format.  This is useful to pass in short files that can easily be specified
  inline.  You must also specify `name` and `type`.
* `template_src` - The name of the file on the control node which will be
  processed as a Jinja `template` file then copied to the managed node to use as
  the source of the quadlet unit.  If this file is in the quadlet unit format
  and has a valid quadlet unit suffix, it will be used as a quadlet unit,
  otherwise, it will just be copied.  If the file has a `.j2` suffix, that
  suffix will be stripped to determine the quadlet file type.

For example, if you specify:

```yaml
podman_quadlet_specs:
  - template_src: my-app.container.j2
```

Then the local file `templates/my-app.container.j2` will be processed as a Jinja
template file, then copied to `/etc/containers/systemd/my-app.container` as a
quadlet container unit spec on the managed node.

### podman_secrets

This is a list of secret specs in the same format as used by
[podman_secret](https://docs.ansible.com/ansible/latest/collections/containers/podman/podman_secret_module.html#ansible-collections-containers-podman-podman-secret-module)
You are *strongly* encouraged to use Ansible Vault to encrypt the value of the
`data` field.

### podman_create_host_directories

This is a boolean, default value is `false`.  If `true`, the role will ensure
host directories specified in host mounts in `volumes.hostPath` specifications
in the Kubernetes YAML given in `podman_kube_specs`, and from `Volume`
configuration in quadlet Container specification where a host path is specified.
NOTE: Directories must be specified as absolute paths (for root containers), or
paths relative to the home directory (for non-root containers), in order for the
role to manage them. Anything else will be assumed to be some other sort of
volume and will be ignored. The role will apply its default
ownership/permissions to the directories. If you need to set
ownership/permissions, see `podman_host_directories`.

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

### podman_activate_systemd_units

Activate each systemd unit as soon as it is created.  The default is `true`. You
can also do this on a per-unit basis by using `activate_systemd_units` in the
spec for each unit. For example, if you are deploying several specs, and you
only want the last one in the list to activate which will trigger the others to
activate via dependencies, then set `activate_systemd_unit: false` for each one
except the last one uses `activate_systemd_unit: true`.  *NOTE*: quadlet units
are implicitly enabled when created - you cannot currently use
`activate_systemd_unit` to disable those units - you can use
`activate_systemd_unit` to create units stopped or started.

### podman_pull_image

Ensure that each image mentioned in a kube or quadlet spec is present by pulling
the image before it is used.  The default is `true`.  Use `false` if the managed
node already has the correct version, or is not able to pull images.  You can also
specify this on a per-unit basis with `pull_image`.

### podman_continue_if_pull_fails

If the image pull attempt fails, do not treat this as a fatal error, and continue
with the role run.  The default is `false` - a pull attempt failure is a fatal
error.  You can set this on a per-unit basis with `continue_if_pull_fails`.

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

### podman_use_copr (EXPERIMENTAL)

Boolean - default is unset - if you want to enable the copr repo to use the
latest development version of podman, use `podman_use_copr: true`

### podman_fail_if_too_old (EXPERIMENTAL)

Boolean - default is unset - by default, the role will fail with an error if you
are using an older version of podman and try to use a feature only supported by
a newer version.  For example, if you attempt to manage quadlet or secrets with
podman 4.3 or earlier, the role will fail with an error. If you want the role to
be skipped instead, use `podman_fail_if_too_old: false`.

## Variables Exported by the Role

### podman_version

This is the version string of the version used by podman.  You can generally
use this in your templates.  For example, if you want to specify a quadlet
`template_src` for a container, and have it use healthchecks and secrets if
using podman 4.5 or later:

```yaml
podman_quadlet_specs:
  - template_src: my-app.container.j2
podman_secrets:
  - name: my-app-pwd
    data: .....
```

my-app.container.j2:
```ini
[Container]
{% if podman_version is version("4.5", ">=") %}
Secret=my-app-pwd,type=env,target=MYAPP_PASSWORD
HealthCmd=/usr/bin/test -f /path/to/my-app.file
HealthOnFailure=kill
{% else %}
PodmanArgs=--secret=my-app-pwd,type=env,target=MYAPP_PASSWORD
{% endif %}
```

## Example Playbooks

Create rootless container with volume mount:

```yaml
- name: Manage podman containers and services
  hosts: all
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

Create container running as root with Podman volume:

```yaml
- name: Manage podman root containers and services
  hosts: all
  vars:
    podman_firewall:
      - port: 8080/tcp
        state: enabled
    podman_kube_specs:
      - state: started
        kube_file_content:
          apiVersion: v1
          kind: Pod
          metadata:
            name: ubi8-httpd
          spec:
            containers:
              - name: ubi8-httpd
                image: registry.access.redhat.com/ubi8/httpd-24
                ports:
                  - containerPort: 8080
                    hostPort: 8080
                volumeMounts:
                  - mountPath: /var/www/html:Z
                    name: ubi8-html
            volumes:
              - name: ubi8-html
                persistentVolumeClaim:
                  claimName: ubi8-html-volume
  roles:
    - linux-system-roles.podman
```

Create quadlet application with secrets.  Defer starting the application until
all of the units have been created.  Note the order of the files in
`podman_quadlet_specs` are in dependency order.  Using
`podman_create_host_directories: true` will create any host mounted directories
specified by a `Volume=` directive in the container spec.

```yaml
podman_create_host_directories: true
podman_activate_systemd_unit: false
podman_quadlet_specs:
  - name: quadlet-demo
    type: network
    file_content: |
      [Network]
      Subnet=192.168.30.0/24
      Gateway=192.168.30.1
      Label=app=wordpress
  - file_src: quadlet-demo-mysql.volume
  - template_src: quadlet-demo-mysql.container.j2
  - file_src: envoy-proxy-configmap.yml
  - file_src: quadlet-demo.yml
  - file_src: quadlet-demo.kube
    activate_systemd_unit: true
podman_firewall:
  - port: 8000/tcp
    state: enabled
  - port: 9000/tcp
    state: enabled
podman_secrets:
  - name: mysql-root-password-container
    state: present
    skip_existing: true
    data: "{{ root_password_from_vault }}"
  - name: mysql-root-password-kube
    state: present
    skip_existing: true
    data: |
      apiVersion: v1
      data:
        password: "{{ root_password_from_vault | b64encode }}"
      kind: Secret
      metadata:
        name: mysql-root-password-kube
  - name: envoy-certificates
    state: present
    skip_existing: true
    data: |
      apiVersion: v1
      data:
        certificate.key: {{ key_from_vault | b64encode }}
        certificate.pem: {{ cert_from_vault | b64encode }}
      kind: Secret
      metadata:
        name: envoy-certificates
```

## License

MIT.

## Author Information

Based on `podman-container-systemd` by Ilkka Tengvall <ilkka.tengvall@iki.fi>.

Authors: Thom Carlin, Rich Megginson, Adam Miller, Valentin Rothberg
