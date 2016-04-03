#
# spec file for package jmtpfs
#
# Copyright (c) 2012 Malcolm J Lewis <malcolmlewis@opensuse.org>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:           jmtpfs
Version:        0.5
Release:        1%{?dist}
License:        GPL-3.0
Summary:        FUSE based MTP filesystem
Url:            http://research.jacquette.com/jmtpfs-exchanging-files-between-android-devices-and-linux/
Group:          Productivity/Multimedia/Other
Source0:        http://research.jacquette.com/wp-content/uploads/2012/05/jmtpfs-%{version}.tar.gz
Source1:        51-android.rules
Source2:        jmtpfs.1
#PATCH-FIX-UPSTREAM jmtpfs-fix-compile-errors-and-warnings.patch malcolmlewis@opensuse.org -- Add missing header to build for gcc4.7 and fix constructor initialization order to avoid warnings. Seehttp://research.jacquette.com/jmtpfs-exchanging-files-between-android-devices-and-linux/#comment-58
Patch0:         jmtpfs-fix-compile-errors-and-warnings.patch
BuildRequires:  file-devel
BuildRequires:  fuse-devel
BuildRequires:  gcc-c++
BuildRequires:  libmtp-devel
BuildRequires:  libusbx-devel
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
FUSE and libmtp based filesystem for accessing MTP (Media Transfer Protocol)
devices. It was specifically designed for exchanging files between Linux
systems and newer Android devices that support MTP but not USB Mass Storage.

%prep
%setup -q
#%patch0 -p1

%build
%configure
make %{?_smp_mflags}

%install
%makeinstall
# udev rules (only for non-systemd)
mkdir -p %{buildroot}/lib/udev/rules.d
install -c -m 0644 %{SOURCE1} %{buildroot}/lib/udev/rules.d
mkdir -p %{buildroot}/%{_mandir}/man1/
install -c -m 0644 %{SOURCE2} %{buildroot}/%{_mandir}/man1/

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_bindir}/%{name}
%dir /lib/udev
%dir /lib/udev/rules.d
/lib/udev/rules.d/51-android.rules
%{_mandir}/man1/jmtpfs.1.gz

%changelog
* Fri Sep 25 2015 Nux <rpm@li.nux.ro> - 0.5-1
- update to 0.5
* Tue Sep 18 2012 malcolmlewis@opensuse.org
- Add udev rule for Samsung GT and update man page.
* Mon Aug 27 2012 malcolmlewis@opensuse.org
- Add udev rule, fuse.conf and man page.
* Sat Aug 25 2012 malcolmlewis@opensuse.org
- Initial build.
- Add jmtpfs-fix-compile-errors-and-warnings.patch: Add missing
  header to build for gcc4.7 and fix constructor initialization
  order to avoid warnings.
