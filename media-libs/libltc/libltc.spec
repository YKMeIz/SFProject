Name:       libltc
Version:    1.1.4
Release:    3%{?dist}
Summary:    Linear/Longitudinal Time Code (LTC) Library

Group:      System Environment/Libraries
License:    LGPLv3+
URL:        http://x42.github.io/libltc/
Source0:    https://github.com/x42/%{name}/releases/download/v%{version}/libltc-%{version}.tar.gz
# Don't timestamp built HTML documentation, probably Fedora specific
Patch0:     libltc-1.1.2-multilib.patch

BuildRequires:  doxygen

%description
Linear (or Longitudinal) Timecode (LTC) is an encoding of time code data as a
Manchester-Biphase encoded audio signal. The audio signal is commonly recorded
on a VTR track or other storage media.

libltc provides functionality to encode and decode LTC from/to time code,
including SMPTE date support.

%package devel
Summary:    Development files for libltc
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package contains the libraries and header files needed for
developing with libltc.

%prep
%setup -q
%patch0 -p1 -b .multilib

%build
%configure
make %{?_smp_mflags} all dox

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/libltc.{a,la}

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING README.md
%{_libdir}/libltc.so.*

%files devel
%doc doc/html
%{_libdir}/libltc.so
%{_includedir}/ltc.h
%{_libdir}/pkgconfig/ltc.pc
%{_mandir}/man3/ltc.h.3*

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Nils Philippsen <nils@tiptoe.de> - 1.1.4-1
- version 1.1.4

* Sat Nov 09 2013 Nils Philippsen <nils@tiptoe.de> - 1.1.3-1
- version 1.1.3

* Sat Nov 09 2013 Nils Philippsen <nils@tiptoe.de> - 1.1.2-2
- upstream distributes official tarballs now

* Mon Oct 28 2013 Nils Philippsen <nils@tiptoe.de> - 1.1.2-1
- version 1.1.2
- use github auto-generated tarball
- build HTML development documentation

* Tue Oct 22 2013 Nils Philippsen <nils@tiptoe.de> - 1.1.1-1
- initial release
