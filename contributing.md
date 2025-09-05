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
   tox -e qemu-ansible-core-2.14 -- --image-name centos-9 tests/tests_default.yml
   ```

There are many command line options and environment variables which can be used
to control the behavior, and you can customize the testenv in tox.ini. See
<https://github.com/linux-system-roles/tox-lsr#qemu-testing>

This method supports RHEL also - will download the latest image for a compose,
and will set up the yum repos to point to internal composes.

See <https://linux-system-roles.github.io/contribute.html> for general
development guidelines.
