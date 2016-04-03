Summary:      Open Sound Control library
Name:         liblo
Version:      0.27
Release:      5%{?dist}
License:      LGPLv2+
Group:        System Environment/Libraries
URL:          http://liblo.sourceforge.net
Source0:      http://download.sf.net/sourceforge/liblo/liblo-%{version}.tar.gz
# Fix multilib installation issue RHBZ#480403
Patch0:       liblo-no-date-footer.patch
# From upstream trunk. Fixes RHBZ#988421
Patch1:       liblo-7a38f5.patch

BuildRequires: doxygen

%description
liblo is an implementation of the Open Sound Control protocol for
POSIX systems developed by Steve Harris.

%package devel
Summary:  Libraries, includes, etc to develop liblo applications
Group:    Development/Libraries
Requires: liblo%{?_isa} = %{version}-%{release}

%description devel
Libraries, include files, etc you can use to develop liblo 
based Open Sound Control applications.

%prep
%setup -q
%patch0 -p1 -b .nodate
%patch1 -p1 -b .fluidsyntd_dssi

%build
%configure --enable-ipv6 --disable-static
# We don't want rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1

%install
%make_install INSTALL="install -p"

# install man pages by hand
mkdir -p %{buildroot}%{_mandir}/man3/
install -m 0664 doc/man/man3/*.3 %{buildroot}%{_mandir}/man3/

# remove libtool archives
rm -f %{buildroot}%{_libdir}/liblo.la 

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_libdir}/liblo.so.*
%{_bindir}/oscdump
%{_bindir}/oscsend

%files devel
%exclude %{_libdir}/liblo.la
%doc doc/html examples/*.c
%{_libdir}/liblo.so
%{_includedir}/lo
%{_libdir}/pkgconfig/liblo.pc
%{_mandir}/man3/*

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Oct 27 2013 Orcan Ogetbil <oget [dot] fedora [at] gmail [dot] com> - 0.27-3
- Backported bugfix: fluidsynth-dssi dialog does not appear RHBZ#988421

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Orcan Ogetbil <oget [dot] fedora [at] gmail [dot] com> - 0.27-1
- New version

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Orcan Ogetbil <oget [dot] fedora [at] gmail [dot] com> - 0.26-4
- Don't build include the example Makefile*. They cause multilib conflict#480403
- Specfile cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 19 2010 Orcan Ogetbil <oget [dot] fedora [at] gmail [dot] com> - 0.26-1
- New version

* Mon Jul 19 2010 Orcan Ogetbil <oget [dot] fedora [at] gmail [dot] com> - 0.24-6
- Fix multilib installation bug via no_date_footer.html hack RHBZ#480403

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Anthony Green <green@redhat.com> 0.24-4
- Remove latex docs as they bundle a .ttf file which goes against the 
  Fedora guidelines.  HTML docs should be sufficient.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.24-2
- Autorebuild for GCC 4.3

* Fri Oct 19 2007 Anthony Green <green@redhat.com> 0.24-1
- New upstream.
- Enable IPv6 support.

* Fri Oct 19 2007 Anthony Green <green@redhat.com> 0.23-13
- Tweak .html files to remove timestamp (to fix multilib conflict).
- Clarify License tag.

* Thu Feb 22 2007 Anthony Green <green@redhat.com> 0.23-12
- Move devel docs to devel package.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.23-11
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Anthony Green <green@redhat.com> 0.23-10
- Fix release tag.

* Mon Sep 18 2006 Anthony Green <green@redhat.com> 0.23-9.1
- Rebuild.

* Fri Sep  8 2006 Anthony Green <green@redhat.com> 0.23-9
- Add liblo-fix-send.c.patch.

* Mon Sep  4 2006 Anthony Green <green@redhat.com> 0.23-7
- -devel packages with .pc files must now Require pkgconfig.

* Thu May 18 2006 Anthony Green <green@redhat.com> 0.23-6
- Don't install generic INSTALL documentation.

* Sat Apr 29 2006 Anthony Green <green@redhat.com> 0.23-4
- Stop using command macros like __rm, __make, __mkdir and __install.

* Tue Apr 25 2006 Anthony Green <green@redhat.com> 0.23-3
- Don't install empty NEWS file.

* Sat Apr 22 2006 Anthony Green <green@redhat.com> 0.23-2
- Minor spec file improvements.

* Tue Apr 18 2006 Anthony Green <green@redhat.com> 0.23-1
- Update to 0.23. Build for Fedora Extras.

* Wed Mar  2 2005 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.22-1
- updated to 0.22
* Wed Mar  2 2005 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.18-1
- updated to 0.18
* Wed Feb 23 2005 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.17-1
- updated to 0.17
* Mon Jan 24 2005 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.16-1
- updated to 0.16
* Tue Dec 21 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 
- spec file cleanup
* Wed Nov 24 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.15-1
- updated to 0.15, exclude .la file, .a file no longer created by
  default build
* Thu Aug 19 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.9-1
- updated to 0.9
* Mon Aug  9 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.8-1
- updated to 0.8
* Thu Apr 15 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.5-1
- Initial build.

