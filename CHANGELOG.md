Changelog
=========

[1.8.3] - 2025-07-24
--------------------

### Bug Fixes

- fix: do not mix facts with vars (#236)

### Other Changes

- test: add a test for multiple users (#237)

[1.8.2] - 2025-07-09
--------------------

### Other Changes

- ci: bump tox-lsr to 3.8.0; rename qemu/kvm tests (#226)
- ci: Add Fedora 42; use tox-lsr 3.9.0; use lsr-report-errors for qemu tests (#228)
- ci: Add support for bootc end-to-end validation tests (#229)
- ci: Use ansible 2.19 for fedora 42 testing; support python 3.13 (#230)
- refactor: support Ansible 2.19 (#231)

[1.8.1] - 2025-05-05
--------------------

### Other Changes

- ci: bump sclorg/testing-farm-as-github-action from 3 to 4 (#223)
- refactor: fix ansible-test issues - unicode_literals, format string (#224)

[1.8.0] - 2025-04-23
--------------------

### New Features

- feat: support TOML tables by using a real TOML formatter (#218)

### Bug Fixes

- fix: render boolean option values correctly in toml files (#209)
- fix: Do not restart logind unless absolutely necessary (#213)
- fix: Do not change the directory mode for the container parent path (#216)

### Other Changes

- ci: ansible-plugin-scan is disabled for now (#201)
- ci: bump ansible-lint to v25; provide collection requirements for ansible-lint (#204)
- ci: Check spelling with codespell (#205)
- ci: Add test plan that runs CI tests and customize it for each role (#206)
- ci: In test plans, prefix all relate variables with SR_ (#211)
- ci: Fix bug with ARTIFACTS_URL after prefixing with SR_ (#212)
- test: check that boolean values are rendered correctly in TOML (#214)
- ci: several changes related to new qemu test, ansible-lint, python versions, ubuntu versions (#219)
- ci: use tox-lsr 3.6.0; improve qemu test logging (#220)
- ci: skip storage scsi, nvme tests in github qemu ci (#221)

[1.7.2] - 2025-01-09
--------------------

### Bug Fixes

- fix: get user information for secrets (#198)

### Other Changes

- chore: remove debug code (#199)

[1.7.1] - 2024-12-04
--------------------

### Other Changes

- ci: Use Fedora 41, drop Fedora 39 (#193)
- ci: Use Fedora 41, drop Fedora 39 - part two (#194)
- test: enable pod test cleanup (#195)

[1.7.0] - 2024-11-12
--------------------

### New Features

- feat: support for Pod quadlets (#190)

[1.6.5] - 2024-10-30
--------------------

### Bug Fixes

- fix: ignore pod not found errors when removing kube specs (#186)
- fix: make role work on el 8.8 and el 9.2 and podman version less than 4.7.0 (#188)

### Other Changes

- ci: ansible-test action now requires ansible-core version (#182)
- ci: add YAML header to github action workflow files (#183)
- refactor: Use vars/RedHat_N.yml symlink for CentOS, Rocky, Alma wherever possible (#185)
- test: need grubby for el8 testing for ostree (#187)

[1.6.4] - 2024-09-11
--------------------

### Bug Fixes

- fix: Cannot remove volumes from kube yaml - need to convert yaml to list (#180)

[1.6.3] - 2024-09-03
--------------------

### Bug Fixes

- fix: subgid maps user to gids, not group to gids (#178)

### Other Changes

- ci: Add tags to TF workflow, allow more [citest bad] formats (#177)

[1.6.2] - 2024-08-21
--------------------

### Other Changes

- test: fix ostree support (#175)

[1.6.1] - 2024-08-19
--------------------

### Other Changes

- test: skip quadlet tests on non-x86_64 (#173)

[1.6.0] - 2024-08-16
--------------------

### New Features

- feat: Handle reboot for transactional update systems (#170)

### Other Changes

- ci: Add workflow for ci_test bad, use remote fmf plan (#168)
- ci: Fix missing slash in ARTIFACTS_URL (#169)

[1.5.3] - 2024-08-01
--------------------

### Bug Fixes

- fix: Ensure user linger is closed on EL10 (#165)

### Other Changes

- ci: Add tft plan and workflow (#162)
- ci: Update fmf plan to add a separate job to prepare managed nodes (#164)
- ci: bump sclorg/testing-farm-as-github-action from 2 to 3 (#166)

[1.5.2] - 2024-07-23
--------------------

### Bug Fixes

- fix: add support for EL10 (#159)
- fix: proper cleanup for networks; ensure cleanup of resources (#160)

### Other Changes

- ci: ansible-lint action now requires absolute directory (#157)

[1.5.1] - 2024-06-11
--------------------

### Bug Fixes

- fix: grab name of network to remove from quadlet file (#155)

### Other Changes

- ci: use tox-lsr 3.3.0 which uses ansible-test 2.17 (#151)
- ci: tox-lsr 3.4.0 - fix py27 tests; move other checks to py310 (#153)
- ci: Add supported_ansible_also to .ansible-lint (#154)

[1.5.0] - 2024-04-22
--------------------

### New Features

- feat: support registry_username and registry_password (#141)
- feat: support podman_credential_files (#142)
- feat: manage TLS cert/key files for registry connections and validate certs (#146)

### Bug Fixes

- fix: use correct user for cancel linger file name (#138)
- fix: do not use become for changing hostdir ownership, and expose subuid/subgid info (#139)
- fix: make kube cleanup idempotent (#144)

### Other Changes

- test: do not check for root linger (#140)
- chore: change no_log false to true; fix comment (#143)
- chore: use none in jinja code, not null (#145)

[1.4.9] - 2024-04-04
--------------------

### Other Changes

- ci: bump mathieudutour/github-tag-action from 6.1 to 6.2 (#136)

[1.4.8] - 2024-03-14
--------------------

### Bug Fixes

- fix: Add support for --check flag (#134)

### Other Changes

- ci: bump ansible/ansible-lint from 6 to 24 (#132)

[1.4.7] - 2024-02-19
--------------------

### Other Changes

- test: gather facts for quadlet_basic test (#130)

[1.4.6] - 2024-02-08
--------------------

### Bug Fixes

- fix: ensure user linger is enabled and disabled correctly (#127)

### Other Changes

- ci: fix python unit test - copy pytest config to tests/unit (#128)

[1.4.5] - 2024-01-24
--------------------

### Other Changes

- test: allow testing to see if secrets are logged (#125)

[1.4.4] - 2024-01-23
--------------------

### Bug Fixes

- fix: cast secret data to string in order to allow JSON valued strings (#122)

[1.4.3] - 2024-01-16
--------------------

### Bug Fixes

- fix: name of volume quadlet service should be basename-volume.service (#119)

### Other Changes

- ci: support ansible-lint and ansible-test 2.16 (#116)
- ci: Use supported ansible-lint action; run ansible-lint against the collection (#117)

[1.4.2] - 2023-12-12
--------------------

### Bug Fixes

- fix: add no_log: true for tasks that can log secret data (#113)

[1.4.1] - 2023-12-08
--------------------

### Other Changes

- ci: bump actions/github-script from 6 to 7 (#109)
- refactor: get_ostree_data.sh use env shebang - remove from .sanity* (#110)

[1.4.0] - 2023-11-29
--------------------

### New Features

- feat: support for ostree systems (#105)

### Other Changes

- build(deps): bump actions/checkout from 3 to 4 (#97)
- ci: ensure dependabot git commit message conforms to commitlint (#100)
- ci: tox-lsr version 3.1.1 (#104)

[1.3.3] - 2023-09-07
--------------------

### Other Changes

- ci: Add markdownlint, test_converting_readme, and build_docs workflows (#93)

  - markdownlint runs against README.md to avoid any issues with
    converting it to HTML
  - test_converting_readme converts README.md > HTML and uploads this test
    artifact to ensure that conversion works fine
  - build_docs converts README.md > HTML and pushes the result to the
    docs branch to publish dosc to GitHub pages site.
  - Fix markdown issues in README.md
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

- docs: Make badges consistent, run markdownlint on all .md files (#94)

  - Consistently generate badges for GH workflows in README RHELPLAN-146921
  - Run markdownlint on all .md files
  - Add custom-woke-action if not used already
  - Rename woke action to Woke for a pretty badge
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

- ci: Remove badges from README.md prior to converting to HTML (#95)

  - Remove thematic break after badges
  - Remove badges from README.md prior to converting to HTML
  
  Signed-off-by: Sergei Petrosian <spetrosi@redhat.com>

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
