# Contributing to the podman Linux System Role

## Where to start

The first place to go is [Contribute](https://linux-system-roles.github.io/contribute.html).
This has all of the common information that all role developers need:

* Role structure and layout
* Development tools - How to run tests and checks
* Ansible recommended practices
* Basic git and github information
* How to create git commits and submit pull requests

**Bugs and needed implementations** are listed on
[Github Issues](https://github.com/linux-system-roles/podman/issues).
Issues labeled with
[**help wanted**](https://github.com/linux-system-roles/podman/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
are likely to be suitable for new contributors!

**Code** is managed on [Github](https://github.com/linux-system-roles/podman), using
[Pull Requests](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests).

## GitHub CI testing using /citest

GitHub CI tests do not run automatically on pull requests. A role repository
maintainer must start them by posting a `/citest` slash command as a pull
request comment.

Run every available CI workflow:

```text
/citest all
```

Run the linting and other lightweight checks:

```text
/citest linters
```

Run the integration tests (QEMU/container and Testing Farm):

```text
/citest integration
```

Run one or more selected workflows by separating their names with spaces:

```text
/citest ansible-lint
/citest ansible-lint markdownlint
```

Post another `/citest` comment at any time to run another selection.

The table below lists each command, the check name shown in the pull request
checks list, and what the test does. Matrix jobs produce one check per
combination; those rows show the check name pattern.

| Command | Check name | Description |
| --- | --- | --- |
| `/citest all` | All checks listed below | Run every CI test available for this role |
| `/citest linters` | Lint and lightweight checks | Run ansible-lint, ansible-test, ansible-managed-var-comment, codespell, markdownlint, pr-title-lint, test_converting_readme, and codeql, python-unit-test, and shellcheck when those workflows exist |
| `/citest integration` | QEMU/container and Testing Farm checks | Run qemu-kvm-integration-tests and tft |
| `/citest ansible-lint` | `Ansible Lint / ansible_lint (<ansible-lint>, <ansible>, <python>) (pull_request)` | Lint Ansible content after converting the role to collection format |
| `/citest ansible-managed-var-comment` | `Check for ansible_managed variable use in comments / ansible_managed_var_comment (pull_request)` | Fail if `ansible_managed` is used in comments |
| `/citest ansible-test` | `Ansible Test / ansible_test (<ansible>, <python>) (pull_request)` | Run ansible-test sanity tests |
| `/citest codespell` | `Codespell / Check for spelling errors (pull_request)` | Check for spelling errors |
| `/citest markdownlint` | `Markdown Lint / markdownlint (pull_request)` | Lint Markdown files |
| `/citest pr-title-lint` | `PR Title Lint / commit-checks` | Check that the pull request title follows the required format |
| `/citest qemu-kvm-integration-tests` | `Test / scenario (<image>, <env>) (pull_request)` | Run role integration tests in QEMU VMs and containers |
| `/citest test_converting_readme` | `Test converting README.md to README.html / test_converting_readme (pull_request)` | Convert README.md to HTML |
| `/citest tft` | `<platform>\|ansible-<version>` | Run integration tests in Testing Farm |
| `/citest woke` | `Woke / Detect non-inclusive language (pull_request)` | Detect non-inclusive language |

## AI Coding Assistants

The `.coderabbit.yaml` configuration file in the repository root contains coding
standards and requirements that can be used by AI coding assistants to help
generate code that follows project conventions.

## Running CI Tests Locally

### Use tox-lsr with qemu

The latest version of tox-lsr supports qemu testing.
<https://github.com/linux-system-roles/tox-lsr#qemu-testing>

**Steps:**

1. If you are using RHEL or CentOS, enable the EPEL repository for your
   platform - <https://docs.fedoraproject.org/en-US/epel/>

2. Use yum or dnf to install `standard-test-roles-inventory-qemu`
   * If for some reason dnf/yum do not work, just download the script from
     <https://pagure.io/standard-test-roles/raw/master/f/inventory/standard-inventory-qcow2> <!--- wokeignore:rule=master -->
     * copy to your `$PATH`, and make sure it is executable

3. Install tox
   * Use yum/dnf to install `python3-tox` - if that does not work, then use
     `pip install --user tox`, then make sure `~/.local/bin` is in your `$PATH`

4. Install tox-lsr <https://github.com/linux-system-roles/tox-lsr#how-to-get-it>

   ```bash
   pip install --user git+https://github.com/linux-system-roles/tox-lsr@main
   ```

5. Download the config file to `~/.config/linux-system-roles.json` from
   <https://github.com/linux-system-roles/linux-system-roles.github.io/blob/main/download/linux-system-roles.json>

6. Assuming you are in a git clone of a role repo which has a tox.ini file -
   you can use e.g.

   ```bash
   tox -e qemu-ansible-core-2-20 -- --image-name centos-9 tests/tests_default.yml
   ```

There are many command line options and environment variables which can be used
to control the behavior, and you can customize the testenv in tox.ini. See
<https://github.com/linux-system-roles/tox-lsr#qemu-testing>

This method supports RHEL also - will download the latest image for a compose,
and will set up the yum repos to point to internal composes.

See <https://linux-system-roles.github.io/contribute.html> for general
development guidelines.
