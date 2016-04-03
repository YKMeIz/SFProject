Summary: A library implementing algorithms related to the Unicode Standard
Name: courier-unicode
Version: 1.4
Release: 1%{?dist}
License: GPLv3
Group: System Environment/Libraries
URL: http://www.courier-mta.org/unicode/
Source0: http://sourceforge.net/projects/courier/files/%{name}/%{version}/courier-unicode-%{version}.tar.bz2
Source1: http://sourceforge.net/projects/courier/files/%{name}/%{version}/courier-unicode-%{version}.tar.bz2.sig
Source2: pubkey.maildrop

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: gnupg

%description
This library implements several algorithms related to the Unicode Standard:

* Look up uppercase, lowercase, and titlecase equivalents of a unicode character.
* Implementation of grapheme and work breaking rules.
* Implementation of line breaking rules.

Several ancillary functions, like looking up the unicode character that
corresponds to some HTML 4.0 entity (such as “&amp;”, for example), and
determining the normal width or a double-width status of a unicode character.
Also, an adaptation of the iconv(3) API for this unicode library.

This library also implements C++ bindings for these algorithms.
The current release of the Courier Unicode library is based on the Unicode 6.3.0 standard.

%package devel
Summary: Development tools for programs which will use the libcourier-unicode library
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The courier-unicode-devel package includes the header files and documentation
necessary for developing programs which will use the libcourier-unicode library.

%prep
%setup -q
gpg --import %{SOURCE2}
gpg --verify %{SOURCE1} %{SOURCE0}

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
%makeinstall

# We don't ship .la files.
rm %{buildroot}%{_libdir}/*.la

%check
%{__make} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%doc README ChangeLog AUTHORS
%{_libdir}/libcourier-unicode.so.3
%{_libdir}/libcourier-unicode.so.3.0.0

%files devel
%{_includedir}/courier-unicode.h
%{_includedir}/courier-unicode-categories-tab.h
%{_includedir}/courier-unicode-script-tab.h
%{_libdir}/libcourier-unicode.so
%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
* Thu Feb 04 2016 Brian C. Lane <bcl@redhat.com> 1.4-1
- Upstream v1.4
  Note that the library name changed to libcourier-unicode

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.1-4
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 18 2015 Brian C. Lane <bcl@redhat.com> 1.1-3
- Update with suggestions from the review
- Run make check

* Tue Feb 17 2015 Brian C. Lane <bcl@redhat.com> 1.1-2
- Changed package name to courier-unicode

* Wed Jan 28 2015 Brian C. Lane <bcl@redhat.com> 1.1-1
- Initial build
