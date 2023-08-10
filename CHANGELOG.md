Changelog
=========

[1.3.2] - 2023-08-10
--------------------

### Bug Fixes

- fix: user secret support (#91)

[1.3.1] - 2023-08-01
--------------------

### Bug Fixes

- fix: require the crun package on EL8 (#88)

[1.3.0] - 2023-07-27
--------------------

### New Features

- feat: allow not pulling images, continue if pull fails (#82)

### Bug Fixes

- fix: support global options in config files (#83)

### Other Changes

- refactor: use getsubids to check subuid and subgid (#86)

[1.2.0] - 2023-07-19
--------------------

### New Features

- feat: add support for quadlet, secrets (#78)

### Bug Fixes

- fix: facts being gathered unnecessarily (#80)

### Other Changes

- ci: Add pull request template and run commitlint on PR title only (#76)
- ci: Rename commitlint to PR title Lint, echo PR titles from env var (#77)
- ci: ansible-lint - ignore var-naming[no-role-prefix] (#79)

[1.1.6] - 2023-05-26
--------------------

### Bug Fixes

- fix: make role work on ansible-core 2.15

### Other Changes

- docs: Consistent contributing.md for all roles - allow role specific contributing.md section
- docs: remove unused Dependencies section in README

[1.1.5] - 2023-04-27
--------------------

### Bug Fixes

- fix: graphroot required in storage.conf on Fedora 37
- fix: Use match instead of in for test for jinja 2.7 support

### Other Changes

- test: use podman pod exists to check if pods absent/stopped
- test: check generated files for ansible_managed, fingerprint
- test: ensure the test works with ANSIBLE_GATHERING=explicit
- ci: Add commitlint GitHub action to ensure conventional commits with feedback

[1.1.4] - 2023-04-13
--------------------

### Other Changes

- ansible-lint - changed_when required even with conditional tasks (#57)

[1.1.3] - 2023-04-06
--------------------

### Other Changes

- Add README-ansible.md to refer Ansible intro page on linux-system-roles.github.io (#54)
- Fingerprint RHEL System Role managed config files (#55)

[1.1.2] - 2023-01-26
--------------------

### New Features

- none

### Bug Fixes

- fix typo in README (#46)

### Other Changes

- none

[1.1.1] - 2023-01-20
--------------------

### New Features

- none

### Bug Fixes

- Ease permissions on kube spec dir and files (#44)

### Other Changes

- Add another example that shows using a Podman volume
- ansible-lint 6.x fixes
- add docs for state parameter (#43)

[1.1.0] - 2022-12-12
--------------------

### New Features


- add checking for subuid, subgid

Ensure that the specified user is present in `/etc/subuid`.
Ensure that the specified group is present in `/etc/subgid`.

### Bug Fixes

- none

### Other Changes

- none

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
