Changelog
=========

[1.0.1] - 2022-11-17
--------------------

### New Features

- none

### Bug Fixes

- ensure role works with podman 4.3
- ensure role works with ansible-core 2.14
- ensure role passes ansible-lint 6.x

### Other Changes

- fix role name

[1.0.0] - 2022-11-01
--------------------

### New Features

- Manage podman containers using the `podman kube play` Kubernetes YAML
  file interface - `podman_kube_spec` - system and user

- Automatically create host volume directories based on specifying host
  mounted volumes in the K8s YAML spec

- Use `podman_host_directories` to provide detailed ownership, permissions,
  SELinux policy, etc. for host directories created by the role

- Use `podman_firewall` to manage firewalld properties of ports specified
  in `podman_kube_spec`

- Use `podman_selinux_ports` to manage SELinux policy for ports specified
  in `podman_kube_spec`

- Manage config files using `podman_containers_conf`, `podman_registries_conf`,
  `podman_storage_conf`, and `podman_policy_json`

### Bug Fixes

- none

### Other Changes

- none
