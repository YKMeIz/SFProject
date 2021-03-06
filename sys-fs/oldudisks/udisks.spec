%define glib2_version           2.6.0
%define dbus_version            1.2
%define dbus_glib_version       0.82
%define polkit_version          0.92
%define parted_version          1.8.8
%define udev_version            145
%define mdadm_version           2.6.7
%define device_mapper_version   1.02
%define libatasmart_version     0.12
%define sg3_utils_version       1.27
%define smp_utils_version       0.94
%define systemd_version         185

%define realname udisks

Summary: Storage Management Service
Name: oldudisks
Version: 1.0.4
Release: 14%{?dist}
License: GPLv2+
Group: System Environment/Libraries
URL: http://www.freedesktop.org/wiki/Software/udisks
Source0: http://hal.freedesktop.org/releases/%{realname}-%{version}.tar.gz
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: dbus-devel  >= %{dbus_version}
BuildRequires: dbus-glib-devel >= %{dbus_glib_version}
BuildRequires: polkit-devel >= %{polkit_version}
BuildRequires: parted-devel >= %{parted_version}
BuildRequires: device-mapper-devel >= %{device_mapper_version}
BuildRequires: intltool
BuildRequires: libatasmart-devel >= %{libatasmart_version}
BuildRequires: libgudev1-devel >= %{udev_version}
%if 0%{?fedora} > 17 || 0%{?rhel} > 6
BuildRequires: systemd-devel >= %{systemd_version}
%else
BuildRequires: libudev-devel >= %{udev_version}
%endif
BuildRequires: sg3_utils-devel >= %{sg3_utils_version}
BuildRequires: gtk-doc
# needed to pull in the system bus daemon
Requires: dbus >= %{dbus_version}
# needed to pull in the udev daemon
Requires: udev >= %{udev_version}
# we need at least this version for bugfixes / features etc.
Requires: libatasmart >= %{libatasmart_version}
Requires: mdadm >= %{mdadm_version}
# for smp_rep_manufacturer
Requires: smp_utils >= %{smp_utils_version}
# for mount, umount, mkswap
Requires: util-linux
# for mkfs.ext3, mkfs.ext3, e2label
Requires: e2fsprogs
# for mkfs.xfs, xfs_admin
Requires: xfsprogs
# for mkfs.vfat
Requires: dosfstools
# for mlabel
Requires: mtools
# For ejecting removable disks
Requires: eject
# for mkntfs - no ntfsprogs on ppc, though
%ifnarch ppc ppc64
Requires: ntfsprogs
%endif

# for /proc/self/mountinfo, only available in 2.6.26 or higher
Conflicts: kernel < 2.6.26

# Obsolete and Provide DeviceKit-disks - udisks provides exactly the same
# ABI just with a different name and versioning-scheme
#
Obsoletes: DeviceKit-disks <= 009
Provides: DeviceKit-disks = 010

Patch0: udisks-1.0.4-neuter-stdout-and-stderr.patch
Patch1: fix_bash_completion.patch
Patch2: buffer-overflow.patch

%description
udisks provides a daemon, D-Bus API and command line tools
for managing disks and storage devices.

%package devel
Summary: D-Bus interface definitions for udisks
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

# See comment above
#
Obsoletes: DeviceKit-disks-devel <= 009
Provides: DeviceKit-disks-devel = 010

%description devel
D-Bus interface definitions and documentation for udisks.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .buffer-overflow

# https://bugzilla.redhat.com/show_bug.cgi?id=673544#c15
rm -f src/*-glue.h tools/*-glue.h

%build
%configure --enable-gtk-doc
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# for now, include a compat symlink for the command-line tool
# and man page
ln -s udisks $RPM_BUILD_ROOT%{_bindir}/devkit-disks
ln -s udisks.1 $RPM_BUILD_ROOT%{_datadir}/man/man1/devkit-disks.1

# TODO: should be fixed upstream
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/udisks-bash-completion.sh
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mv $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/udisks-bash-completion.sh \
    $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d

%find_lang %{realname}

%files -f %{realname}.lang
%defattr(-,root,root,-)

%doc README AUTHORS NEWS COPYING HACKING doc/TODO

%{_sysconfdir}/avahi/services/udisks.service
%{_sysconfdir}/bash_completion.d/
%{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules

/lib/udev/udisks-part-id
/lib/udev/udisks-dm-export
/lib/udev/udisks-probe-ata-smart
/lib/udev/udisks-probe-sas-expander
/sbin/umount.udisks

%{_bindir}/*
%{_libexecdir}/*

%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%{_datadir}/polkit-1/actions/*.policy

%{_datadir}/dbus-1/system-services/*.service

%attr(0700,root,root) %dir %{_localstatedir}/lib/udisks

%files devel
%defattr(-,root,root,-)

%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/pkgconfig/udisks.pc
%{_datadir}/gtk-doc

# Note: please don't forget the %{?dist} in the changelog. Thanks
%changelog
* Mon Aug 25 2014 Nux <rpm@li.nux.ro> - 1.0.14-14
- attempting to reintroduce package as oldudisks so udisks2 doesn't obsolete it

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.0.4-13
- fix CVE-2014-0004

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 26 2013 Ville Skytt?? <ville.skytta@iki.fi> - 1.0.4-11
- Move bash completion to %%{_sysconfdir}/bash_completion.d (#584569).

* Sun Feb 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> 1.0.4-10
- Fix bash completion as per RHBZ 584569

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 05 2012 Adam Jackson <ajax@redhat.com> 1.0.4-7%{?dist}
- Rebuild for new libudev
- Conditional BuildReqs for {libudev,systemd}-devel

* Sat Apr 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.4-6
- Add dependency on eject - fixes RHBZ 810882

* Thu Mar 15 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-5
- rebuild (parted)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 David Zeuthen <davidz@redhat.com> - 1.0.4-2%{?dist}
- Add patch to neuter the annoying systemd behavior where stdout/stderr
  is sent to the system logs (#743344)

* Fri Aug 26 2011 David Zeuthen <davidz@redhat.com> - 1.0.4-1%{?dist}
- Update to release 1.0.4 and update BR + files to reflect that lvm2 is no
  longer enabled given recommendations from upstream (lvm2 support in
  udisks never worked well and caused a lot more problems than it solved)
- Remove /etc/tmpfiles.d/udisks.conf hack since this is now created on demand

* Thu Aug 25 2011 David Zeuthen <davidz@redhat.com> - 1.0.3-3%{?dist}
- Use tmpfiles.d for /var/run dir (#733161)

* Mon Jul 18 2011 Dan Hor??k <dan@danny.cz> - 1.0.3-2%{?dist}
- rebuilt for sg3_utils 1.31

* Mon Jul 11 2011 David Zeuthen <davidz@redhat.com> - 1.0.3-1%{?dist}
- Update to 1.0.3

* Sat Apr  9 2011 Christopher Aillon <caillon@redhat.com> 1.0.2-4%{?dist}
- Bump release to match what's in Fedora 14

* Thu Apr  7 2011 Matthias Clasen <mclasen@redhat.com> 1.0.2-1%{?dist}
- Update to 1.0.2
- Nuke generated D-Bus code to force regeneration and avoid potential
  dbus-glib bug. Credit goes to Tom???? Trnka <tomastrnka@gmx.com> for
  figuring this out (#673544 comment 15)

* Fri Jan 28 2011 Matthias Clasen <mclasen@redhat.com> - 1.0.1-7%{?dist}
- %%ghost /var/run content (#656709)

* Tue Jan 25 2011 Matthias Clasen <mclasen@redhat.com> - 1.0.1-6%{?dist}
- BR gtk-doc

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 1.0.1-5%{?dist}
- Co-own /usr/share/gtk-doc (#604420)
- Some other packaging cleanups

* Wed May 19 2010 David Zeuthen <davidz@redhat.com> - 1.0.1-4%{?dist}
- Actually make udisks work with latest liblvm2app

* Wed May 05 2010 Adam Tkac <atkac redhat com> - 1.0.1-3%{?dist}
- rebuilt against new lvm2 libraries

* Tue Apr 13 2010 Dan Hor????k <dan@danny.cz> - 1.0.1-2%{?dist}
- rebuilt for sg3_utils 1.29

* Fri Apr 09 2010 David Zeuthen <davidz@redhat.com> - 1.0.1-1%{?dist}
- Update to release 1.0.1 (CVE-2010-1149 ,fdo #27494)

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-2%{?dist}
- Bump release and rebuild so we link to the new libparted.

* Mon Mar 15 2010 David Zeuthen <davidz@redhat.com> - 1.0.0-1%{?dist}
- Update to release 1.0.0

* Tue Feb 23 2010 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20100223.1%{?dist}
- Update to new git snapshot

* Tue Feb 16 2010 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20100215.3%{?dist}
- Require lvm2-libs >= 2.02.61 to get the right ABI for liblvm2app

* Tue Feb 16 2010 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20100215.2%{?dist}
- Update for new liblvm2app library

* Mon Feb 15 2010 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20100215.1%{?dist}
- Update to git snapshot

* Fri Jan 15 2010 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20100115.2%{?dist}
- Rebuild

* Fri Jan 15 2010 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20100115.1%{?dist}
- New git snapshot with LVM support

* Tue Jan 12 2010 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20091202.3%{?dist}
- Rebuild for new libparted

* Mon Dec 07 2009 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20091202.2%{?dist}
- Rebuild

* Fri Dec 04 2009 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20091202.1%{?dist}
- Updated for package review (#543608)

* Wed Dec 02 2009 David Zeuthen <davidz@redhat.com> - 1.0.0-0.git20091202%{?dist}
- Git snapshot for upcoming 1.0.0 release
