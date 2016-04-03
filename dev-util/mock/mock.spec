# next four lines substituted by autoconf
%global major 1
%global minor 2
%global sub 17
%global extralevel %{nil}
%global release_version %{major}.%{minor}.%{sub}%{extralevel}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%if 0%{?fedora} > 21
%global use_python3 1
%global use_python2 0
%else
%global use_python3 0
%global use_python2 1
%endif

%if %{use_python3}
%global python_sitelib %{python3_sitelib}
%else
%global python_sitelib %{python_sitelib}
%endif

# mock group id allocate for Fedora
%global mockgid  135

Summary: Builds packages inside chroots
Name: mock
Version: %{release_version}
Release: 1%{?dist}
License: GPLv2+
Source: https://git.fedorahosted.org/cgit/mock.git/snapshot/%{name}-%{version}.tar.xz
URL: https://fedoraproject.org/wiki/Mock
BuildArch: noarch
%if 0%{?fedora} > 21
Requires: yum >= 3.4.3-505
%else
Requires: yum >= 2.4
%endif
Requires: tar
Requires: pigz
Requires: usermode
Requires: yum-utils
Requires: createrepo_c
%if 0%{?use_python2}
Requires: pyliblzma
%endif
%if 0%{?rhel} != 6 && 0%{?fedora} > 0 && 0%{?fedora} < 24
Requires: systemd
%endif
%if 0%{?fedora} > 23
Requires: systemd-container
%endif
Requires(pre): shadow-utils
Requires(post): coreutils
BuildRequires: autoconf, automake
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: bash-completion
%endif
%if %{use_python3}
Requires: python3
Requires: python3-six
Requires: python3-requests
Requires: rpm-python3
BuildRequires: python3-devel
%else
Requires: python-ctypes
Requires: python-six
Requires: python-requests
Requires: python >= 2.6
BuildRequires: python-devel
%endif
%if 0%{?fedora}
Recommends: dnf
Recommends: dnf-plugins-core
Recommends: btrfs-progs
%endif
%if 0%{?rhel} >= 7
Requires: btrfs-progs
%endif


%description
Mock takes an SRPM and builds it in a chroot.

%package scm
Summary: Mock SCM integration module
Requires: %{name} = %{version}-%{release}
Requires: cvs
Requires: git
Requires: subversion
Requires: tar

%description scm
Mock SCM integration module.

%package lvm
Summary: LVM plugin for mock
Requires: %{name} = %{version}-%{release}
Requires: lvm2

%description lvm
Mock plugin that enables using LVM as a backend and support creating snapshots
of the buildroot.

%prep
%setup -q
%if 0%{?rhel} == 6
sed -i "s|^USE_NSPAWN = True|USE_NSPAWN = False|" py/mockbuild/util.py
%endif
%if %{use_python3}
sed -i 's/AM_PATH_PYTHON/AM_PATH_PYTHON([3])/' configure.ac
for file in py/mock.py py/mockchain.py; do
  sed -i 1"s|#!/usr/bin/python |#!/usr/bin/python3 |" $file
done
%endif

%build
autoreconf -vif
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT/var/lib/mock
mkdir -p $RPM_BUILD_ROOT/var/cache/mock
ln -s consolehelper $RPM_BUILD_ROOT/usr/bin/mock

echo "%defattr(0644, root, mock)" > %{name}.cfgs
find $RPM_BUILD_ROOT%{_sysconfdir}/mock -name "*.cfg" \
    | sed -e "s|^$RPM_BUILD_ROOT|%%config(noreplace) |" >> %{name}.cfgs

# just for %%ghosting purposes
ln -s fedora-rawhide-x86_64.cfg $RPM_BUILD_ROOT%{_sysconfdir}/mock/default.cfg

if [ -d $RPM_BUILD_ROOT%{_datadir}/bash-completion ]; then
    echo %{_datadir}/bash-completion/completions/mock >> %{name}.cfgs
    echo %{_datadir}/bash-completion/completions/mockchain >> %{name}.cfgs
elif [ -d $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d ]; then
    echo %{_sysconfdir}/bash_completion.d/mock >> %{name}.cfgs
fi

%if 0%{?rhel} == 6
    # can be removed when yum-utils >= 1.1.31 lands in el6
    echo "config_opts['plugin_conf']['package_state_enable'] = False" >> $RPM_BUILD_ROOT%{_sysconfdir}/mock/site-defaults.cfg
    echo "config_opts['use_nspawn'] = False" >> $RPM_BUILD_ROOT%{_sysconfdir}/mock/site-defaults.cfg
%endif
%pre

# check for existence of mock group, create it if not found
getent group mock > /dev/null || groupadd -f -g %mockgid -r mock
exit 0

%post

# fix cache permissions from old installs
chmod 2775 %{_localstatedir}/cache/%{name}

if [ -s /etc/os-release ]; then
    # fedora and rhel7
    if grep -Fq Rawhide /etc/os-release; then
        ver=rawhide
    else
        ver=$(source /etc/os-release && echo $VERSION_ID | cut -d. -f1 | grep -o '[0-9]\+')
    fi
else
    # rhel6 or something obsure, use buildtime version
    ver=%{?rhel}%{?fedora}
fi
mock_arch=$(python -c "import rpmUtils.arch; baseArch = rpmUtils.arch.getBaseArch(); print baseArch")
cfg=%{?fedora:fedora}%{?rhel:epel}-$ver-${mock_arch}.cfg
[ -e %{_sysconfdir}/%{name}/$cfg ] || exit -2
if [ "$(readlink %{_sysconfdir}/%{name}/default.cfg)" != "$cfg" ]; then
  ln -s $cfg %{_sysconfdir}/%{name}/default.cfg 2>/dev/null || ln -s -f $cfg %{_sysconfdir}/%{name}/default.cfg.rpmnew
fi
:

%files -f %{name}.cfgs
%defattr(-, root, root)

# executables
%{_bindir}/mock
%{_bindir}/mockchain
%attr(0755, root, root) %{_sbindir}/mock

# python stuff
%{python_sitelib}/*
%exclude %{python_sitelib}/mockbuild/scm.*
%exclude %{python_sitelib}/mockbuild/plugins/lvm_root.*

# config files
%dir  %{_sysconfdir}/%{name}
%ghost %config(noreplace,missingok) %{_sysconfdir}/%{name}/default.cfg
%config(noreplace) %{_sysconfdir}/%{name}/*.ini
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}

# gpg keys
%dir %{_sysconfdir}/pki/mock
%config(noreplace) %{_sysconfdir}/pki/mock/*

# docs
%{_mandir}/man1/mock.1*
%{_mandir}/man1/mockchain.1*
%doc ChangeLog

# cache & build dirs
%defattr(0775, root, mock, 02775)
%dir %{_localstatedir}/cache/mock
%dir %{_localstatedir}/lib/mock

%files scm
%{python_sitelib}/mockbuild/scm.py*

%files lvm
%{python_sitelib}/mockbuild/plugins/lvm_root.*

%changelog
* Fri Mar 11 2016 Miroslav Suchý <msuchy@redhat.com> - 1.2.17-1
- call rpmbuild correctly

* Tue Mar  8 2016 Miroslav Suchý <msuchy@redhat.com> - 1.2.16-1
- remove old %if statements
- systemd-nspawn is now in systemd-container package
- become root user correct way [RHBZ#1312820][RHBZ#1311796]
- remove the sparc config
- Let logging format messages on demand
- tell nspawn which variables it should set [RHBZ#1311796]
- do not call /bin/su and rather utilize --user of systemd-nspawn [RHBZ#1301953]

* Mon Feb 22 2016 Miroslav Suchý <msuchy@redhat.com> - 1.2.15-1
- ccache plugin disabled by default
- F21 configs removed
- F24 configs added
- typo fixed [RHBZ#1285630]
- read user config from ~/.config/mock.cfg too
- disable "local" dnf plugin [RHBZ#1264215]
- when removing buildroot, do that as root [RHBZ#1294979]

* Fri Nov 20 2015 Miroslav Suchý <msuchy@redhat.com> - 1.2.14-1
- after unpacking chroot, change back to $CWD [RHBZ#1281369]
- Fix package manager version handling for CentOS
- use --setopt=deltarpm=false as default value for dnf_common_opts [RHBZ#1281355]
- add arguments, do not over ride previous ones
- Add %%(resultdir) placeholder for sign plugin. [RHBZ#1272123]
- decode shell output when running under Python3 [RHBZ#1267161]
- create tmpfs with unlimited inodes [RHBZ#1266453]
- typo [RHBZ#1241827]
- do not use machinectl --no-legend as it is not el7 compatible [RHBZ#1241827]
- directly tell yum which yum.conf he should use [RHBZ#1264462]

* Wed Sep 16 2015 Miroslav Suchý <msuchy@redhat.com> - 1.2.13-1
- Use 'machinectl terminate' inside orphanskill() when systemd-nspawn used [RHBZ#1171737]
- use quite systemd-nspawn in quite mode [RHBZ#1262889]
- when calling systemd-nspawn become root first [RHBZ#1241827]
- revert F23 configs back to yum
- Give user hint what to do if he miss scm plugin.
- when cleaning up /dev/ do not fail on mountpoins
- warn (but not fail) on RHELs when you try to use DNF
- migrate package_state to use dnf when package_manager is set to dnf
- redownload metadata if they changed on server [RHBZ#1230508]
- provide --scrub=dnf-cache as alias for yum-cache [RHBZ#1241296]
- copy files to correct location [RHBZ#1252088]
- do not install weak deps in chroot [RHBZ#1254634]
- Try to set PTY window size [RHBZ#1155199]
- Set default LVM pool name [RHBZ#1163008]
- better parsing of content-disposition header [RHBZ#1248344]
- backend: Ensure output files are owned by unpriv user with nspawn
- Add "rpmbuild_networking" key (False by default) for nspawn backend
- fdfd464 Update Fedora Wiki URLs
- use yum-deprecated as the yum_command if it exists

* Tue Jul 14 2015 clark Williams <williams@redhat.com> - 1.2.12-1
- from Dennis Gilmore <dennis@ausil.us>:
  - setup support so loopback devices can work [RHBZ#1245401]
- from Miroslav Suchý <msuchy@redhat.com>:
  - clarify path [RHBZ#1228751]
  - document target_arch and legal_host_arches in site-defaults.cfg [RHBZ#1228751]
  - document "yum.conf" in site-defaults.cfg [RHBZ#1228751]
  - correctly specify requires of yum [RHBZ#1244475]
  - bump up releasever in rawhide targets
  - remove EOLed gpg keys
  - add f23 configs
  - removing EOLed f19 and f20 configs

* Tue Jul 14 2015 clark Williams <williams@redhat.com> - 1.2.11-1
- dropped code that does stray mount cleanup of chroot [RHBZ#1208092]
- modified package_manager resolvedep cmd to use repoquery when dnf is installed

* Tue Jun  2 2015 Miroslav Suchý <msuchy@redhat.com> - 1.2.10-1
- do not require pyliblzma if using python3 [RHBZ#1227209]
- add warning to site-defaults.cfg that assumeyes=1 is important [RHBZ#1225004]
- sync comments in site-defaults.cfg with code [RHBZ#1224961]
- check for dangling link of /etc/mtab [RHBZ#1224732]
- Fix --install filename completion

* Wed May 13 2015 Miroslav Suchý <msuchy@redhat.com> - 1.2.9-1
- scm: do not keep copy of environ, this is now handled by uidmanager [RHBZ#1204395]
- Add pm_request plugin
- Drop lvm2-python-libs requires and enable lvm subpackage on el6
- Use lvs instead of lvm python bindings
- Unshare IPC ns only for chroot processes
- Add missing flush in logOutput
- Avoid infinite recursion in selinux plugin

* Wed Apr 29 2015 Miroslav Suchý <msuchy@redhat.com> - 1.2.8-1
- LVM plugin is removed on F22+ due RHBZ 1136366
- allow the chroot's location to be configurable [RHBZ#452730]
- send output of --chroot to log [RHBZ#1214178]
- chroot_scan: implement "only_failed" option [RHBZ#1190763]
- add comment why this previous commit was done [RHBZ#1192128]
- use rpm macros instead of cmd option for --nocheck [RHBZ#1192128]
- plugin options can be string if specified on command line [RHBZ#1193487]
- root_cache: do not assume volatile root with tmpfs [RHBZ#1193487]
- use CONFIG instead of CHROOT in help/man for --root option [RHBZ#1197131]
- more clarification on --dnf-cmd/--yum-cmd [RHBZ#1211621]
- scm correct the logic of exclude_vcs [RHBZ#1204240]
- ignore missing files in ccache [RHBZ#1210569]
- install buildsys-macros in el5 chroot [RHBZ#1213482]
- remove forgotten print statement [RHBZ#1202845]
- add a plugin that calls command (from the host) on the produced rpms.
- save/restore os.environ when dropping/restoring Privs [RHBZ#1204395]
- mock-scm pull tarball name from specfile instead of hardcoding [RHBZ#1204935]
- clarify "--yum-cmd" / "--dnf-cmd" options [RHBZ#1211621]
- return the SRPM name from do_buildsrpm (required for SCM builds) [1190450]
- binding DNF cache directory with yum_cache [RHBZ#1176560]
- suggest user to install dnf-plugins-core [RHBZ#1196248]
- ignore btrfs errors on non-btrfs systems [RHBZ#1205564]
- on F21- use hard deps instead of soft [RHBZ#1198769]
- delete btrfs subvolumes on exit [RHBZ#1205564]
- on python3 convert err from bytes to str [RHBZ#1211199]
- on F22+ use yum-deprecated instead of yum [RHBZ#1211978]
- if mountpoint is inside chroot, remove chroot part [RHBZ#1208299]
- chmod directory only if we really created it [RHBZ#1209532]
- port epel-5 configs to Python 3 [RHBZ#1204662]
- use nosync only for package management and chroot init [RHBZ#1184964]
- missing config file should not be fatal [RHBZ#1195749]
- pass variable "name" [RHBZ#1194171]
- correct chroot_scan configuration sample in site-defaults
- install missing chroot_scan plugin
- avoid creating resultdir as root


* Fri Feb 13 2015 Miroslav Suchý <msuchy@redhat.com> - 1.2.7-1
- add Fedora 22 configs
- rawhide configs use DNF
- touch should not truncate file [RHBZ#1188770]

* Mon Feb  2 2015 Clark Williams <williams@redhat.com> - 1.2.6-1
- fix broken build issue
- From Mikhail Campos Guadamuz <Mikhail_Campos-Guadamuz@epam.com>:
  - use default logging.ini if non-default does not exist [RHBZ#1187727]
- From Michael Simacek <msimacek@redhat.com>:
  - Update manpage regarding multiple arguments
  - Take package arguments in update [RHBZ#1187136]
- From Miroslav Suchý <msuchy@redhat.com>:
  - reset LC before calling lvm commands [RHBZ#1185912]

* Fri Jan 23 2015 Clark Williams <williams@redhat.com> - 1.2.5-1
- mounts: do not mount /dev/shm or /dev/pts if internal setup false
- actually package compress_logs plugin
- use relative imports
- touch /etc/os-release after install @buildsys-build [RHBZ#1183454]
- parse /etc/os-release only if it exists and size is non-zero [RHBZ#1183454]

* Fri Jan 16 2015 Miroslav Suchý <msuchy@redhat.com> - 1.2.4-1
- each user have its own ccache cache [RHBZ#1168116]
- man: write example for --chroot option
- sort options in man page
- sort command in man page
- add Fedora 22 GPG keys
- improve --resultdir part of man page [RHBZ#1181554]
- allow the subsitution of resultdir into the yum.conf block [RHBZ#1125376]
- do no print duplicities in bash completion
- Fixed systemd-nspawn machine name collision [RHBZ#1174286]
- do shell expansion on  --new-chroot --chroot [RHBZ#1174317]
- log executing command after nspawn expansion
- make sure that mockchain generate unique repoid for all repos [RHBZ#1179806]
- workaround old python-six in EL7
- Remove checking for chroot existence in --chroot
- Exclude .bash_history and .bashrc from builddir cleanup
- Ignore broken symlinks in chown_home_dir
- create SCM files as non-privileg user [RHBZ#1178576]
- With --no-clean, delete /builddir except build/SOURCES [RHBZ#1173126]
- Man page formatting improvements
- Move the pool size check to later time when pool already exists
- Always use returnOutput in lvm plugin to get possible error output
- put correct version in man page
- Fix unicode characters in logs on Python 2 [RHBZ#1171707]
- Added new option 'postinstall' [RHBZ#1168911]
- Use keepcache=1 in yum.conf [RHBZ#1169126]
- Warn user when LVM thin pool is filled up [RHBZ#1167761]
- add missing max_metadata_age_days do site-defaults.cfg
- add age_check to site-default.cfg
- compress also logs created by package_state plugin

* Thu Dec  4 2014 Miroslav Suchý <msuchy@redhat.com> - 1.2.3-1
- fixed incorrect command construction in PackageManager:build_invocation [RHBZ#1170230]
- completion: correctly expand --install [RHBZ#1168220]
- copyin: when source is directory, then handle corner cases [RHBZ#1169051]
- increase default for tmpfs to 768
- check if key exist [RHBZ#476837]
- Added tmpfs new option 'keep_mounted' [RHBZ#476837]
- add 2 common tmpfs dirs to find_non_nfs_dir()
- Added new option --symlink-dereference used with --buildsrpm [BZ# 1165242]
- accept None as macro value in config [RHBZ#1165778]
- Don't do yum update when --no-clean specified [RHBZ#1165716]
- do not delete /buildir when --no-clean was set [RHBZ#483486]
- bash completation for --copyin and --sources
- bash_completion.d/mock: fix syntax error
- Correct check for --source cmd option, single file can be used [RHBZ#1165213]
- update BUGS part of man page
- add missing options to man page
