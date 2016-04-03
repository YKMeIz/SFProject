Name:          simple-mtpfs
Version:       0.2
Release:       3%{?dist}
Summary:       Fuse-based MTP driver
License:       GPLv2+
URL:           https://github.com/phatina/simple-mtpfs
Source0:       http://phatina.fedorapeople.org/releases/simple-mtpfs/%{name}-%{version}.tar.gz

BuildRequires: fuse-devel >= 2.7.3
BuildRequires: libmtp-devel

%description
SIMPLE-MTPFS (Simple Media Transfer Protocol FileSystem) is a file system for
Linux (and other operating systems with a FUSE implementation, such as Mac OS X
or FreeBSD) capable of operating on files on MTP devices attached via USB to
local machine. On the local computer where the SIMPLE-MTPFS is mounted, the
implementation makes use of the FUSE (Filesystem in Userspace) kernel module.
The practical effect of this is that the end user can seamlessly interact with
MTP device files.

%prep
%setup -q -n %{name}-%{version}

%build
%configure --with-tmpdir=/var/tmp
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc COPYING README.md
%{_bindir}/simple-mtpfs
%{_mandir}/man1/simple-mtpfs.1.gz

%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 06 2013 Peter Hatina <phatina@redhat.com> - 0.2-1
- upgrade to v0.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Peter Hatina <phatina@redhat.com> - 0.1-5
- changed license to GPLv2

* Sun Oct 07 2012 Peter Hatina <phatina@redhat.com> - 0.1-4
- removed defattr

* Sat Oct 06 2012 Peter Hatina <phatina@redhat.com> - 0.1-3
- removed gcc dependency

* Fri Oct 05 2012 Peter Hatina <phatina@redhat.com> - 0.1-2
- removed autoconf dependency

* Wed Oct 03 2012 Peter Hatina <phatina@redhat.com> - 0.1-1
- initial import
