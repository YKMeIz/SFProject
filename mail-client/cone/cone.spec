%global curses_include_dir  %{_includedir}/ncursesw

Summary:        CONE mail reader
Name:           cone
Version:        0.92
Release:        1%{?dist}
URL:            http://www.courier-mta.org/cone/
Source:         http://downloads.sourceforge.net/project/courier/cone/%{version}/cone-%{version}.tar.bz2
License:        GPLv3

BuildRequires:  aspell-devel
BuildRequires:  libxml2-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel
BuildRequires:  ncurses-devel
BuildRequires:  openldap-devel
BuildRequires:  libidn-devel
BuildRequires:  courier-unicode-devel > 1.2
BuildRequires:  perl
BuildRequires:  openssl-perl
BuildRequires:  gawk
BuildRequires:  procps

Requires(post): perl

%description
CONE is a simple, text-based E-mail reader and writer.

%package devel
Summary:        LibMAIL mail client development library
Provides:       %{name}-static = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package the header files and library files for developing
application using LibMAIL - a high level, C++ OO library for mail clients.

%package doc
Summary:        Documentation for the CONE email client

%description doc
CONE is a simple, text-based E-mail reader and writer.  This package
contains a large amount of documentation for CONE.

%prep
%setup -q

%build
%configure --with-devel --enable-shared CPPFLAGS="$CPPFLAGS -I%{curses_include_dir}"
make %{?_smp_mflags}

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
install -m 0644 sysconftool %{buildroot}%{_datadir}/cone/cone.sysconftool
touch %{buildroot}%{_sysconfdir}/cone

# Remove dupe copies of doc/html from the install tree.
( cd cone/html && \
    find . -type f -exec rm -f %{buildroot}%{_datadir}/cone/{} \; )

%preun
if [ "$1" = 0 ]; then
    mv %{_sysconfdir}/cone %{_sysconfdir}/cone.rpmsave
fi

%pre
if [ "$1" = 1 -a -f %{_sysconfdir}/cone.rpmsave -a ! -f %{_sysconfdir}/cone ]
then
    mv %{_sysconfdir}/cone.rpmsave %{_sysconfdir}/cone
fi

%post
%{__perl} %{_datadir}/cone/cone.sysconftool %{_sysconfdir}/cone.dist > /dev/null

%files
%license COPYING COPYING.GPL
%doc ChangeLog README NEWS AUTHORS INSTALL
%attr(644,root,root) %{_sysconfdir}/cone.dist
%ghost %verify(user group mode) %attr(644,root,root) %{_sysconfdir}/cone
%{_bindir}/*
%{_libexecdir}/cone
%{_datadir}/cone
%{_mandir}/man1/*

%files devel
%{_libdir}/*.a
%{_mandir}/man[35]/*
%{_includedir}/libmail

%files doc
%doc cone/html

%changelog
* Sun Feb 14 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.92-1
- Update to 0.92.
- Cleanup spec.
- Remove cone-0.84-build.patch (Unused).

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.91.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.91.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Sun Mar 22 2015 Mosaab Alzoubi <moceap@hotmail.com> - 0.91.1-1
- Update to 0.91.1
- Clean Spec up
- Remove old tags
- Remove old %%clean
- Remove un-neede sig file
- Use best way of sourceforge sources
- Split old one-line BRs
- Add New BRs
- Use %%make_install
- Add %%license macro
- Update %%doc line
- Fix dates on %%changelog
- Remove old patch

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.84-8
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-5
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 0.84-3
- Add %%?_isa to -devel base package dep to meet guidelines.
- Fix FTBFS (#716041).
- Add -static Provides to -devel package (#609603).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Steven Pritchard <steve@kspei.com> 0.84-1
- Update to 0.84.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.78-3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 13 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.78-1
- Update to 0.78 (resolves BZ#496421, BZ#426952).
- Dropped cone-gcc44.patch (merged upstream).

* Sun Apr 19 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.75-5
- Updated cone-gcc44.patch according to upstream wishes.

* Sat Apr 18 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.75-4
- Fix FTBFS: added cone-gcc44.patch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> 0.75-2
- rebuild with new openssl

* Thu Jul 10 2008 Steven Pritchard <steve@kspei.com> 0.75-1
- Update to 0.75.

* Sat Mar 29 2008 Christopher Aillon <caillon@redhat.com> - 0.74-3
- Add compilation patch for GCC 4.3; add proper C++ #includes

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.74-2
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Steven Pritchard <steve@kspei.com> 0.74-1
- Update to 0.74.
- Update License (now GPLv3).

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.71-5
- BR gawk.
- and procps.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.71-3
- Rebuild for selinux ppc32 issue.

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 0.71-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Steven Pritchard <steve@kspei.com> 0.71-1
- Update to 0.71.

* Mon Apr 09 2007 Steven Pritchard <steve@kspei.com> 0.69-1
- Update to 0.69.

* Mon Aug 28 2006 Steven Pritchard <steve@kspei.com> 0.68-2
- Rebuild.

* Tue Aug 01 2006 Steven Pritchard <steve@kspei.com> 0.68-1
- Update to 0.68.
- Drop cone-0.66.20060203-compile.patch.

* Sat Feb 04 2006 Steven Pritchard <steve@kspei.com> 0.66.20060203-1
- Update to 0.66.20060203 (development snapshot, needed to fix compilation
  with g++ 4.1)
- Patch a few more g++ 4.1 issues

* Thu Feb 02 2006 Steven Pritchard <steve@kspei.com> 0.66-1
- Update to 0.66
- Spec cleanup (reformatting)

* Mon Nov 14 2005 Steven Pritchard <steve@kspei.com> 0.65-3
- Disabling static library creation breaks the build

* Mon Nov 14 2005 Steven Pritchard <steve@kspei.com> 0.65-2
- Rebuild

* Thu Aug 04 2005 Steven Pritchard <steve@kspei.com> 0.65-1
- Update to 0.65

* Thu Jun  2 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.64-5
- disable explicit gcc-c++/libstdc++-devel BR and bump for another
  rebuild attempt

* Sat May 28 2005 Steven Pritchard <steve@kspei.com> 0.64-4
- rebuild

* Thu May 26 2005 Jeremy Katz <katzj@redhat.com> - 0.64-3
- rebuild on all arches

* Thu Apr 7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.64-2
- rebuilt

* Wed Mar 02 2005 Steven Pritchard <steve@kspei.com> 0.64-1
- Update to 0.64

* Wed Feb 23 2005 Steven Pritchard <steve@kspei.com> 0.63-1
- Update to 0.63
- Include signature file with the source rpm
- Drop GCC 3.4 patch (already included upstream)

* Fri Nov 12 2004 Michael Schwendt <mschwendt[AT]users.sf.net> 0.60-2
- Fix addressbookget.C for GCC 3.4.

* Thu Jul 15 2004 Steven Pritchard <steve@kspei.com> 0:0.60-0.fdr.1
- Update to 0.60
- Re-enable sysconftool
- Eliminate duplicate html documentation
- Other minor changes from upstream spec
- Add explicit Epoch to make rpmlint happier
- Split html documentation into separate -doc subpackage

* Wed Apr 14 2004 Steven Pritchard <steve@kspei.com> 0.58-0.fdr.1
- Remove html docs from %doc.  They're all in /usr/share/cone already.

* Tue Apr 13 2004 Steven Pritchard <steve@kspei.com> 0.58-0.fdr.0
- Update to 0.58
- More spec cleanup (s/BuildPreReq/BuildRequires/, -devel Requires
  version-release, generate the config file in install instead of
  post).  Suggestions from Warren Togami.
- Enable SMP builds
- Use RPM_OPT_FLAGS

* Tue Apr 06 2004 Steven Pritchard <steve@kspei.com> 0.57.20040327-0.fdr.1
- Spec cleanup

* Sun Apr 04 2004 Steven Pritchard <steve@kspei.com> 0.57.20040327-0.fdr.0
- Recompile for FC1 using the spec included with the source

* Mon Sep  1 2003 Mr. Sam <sam@email-scan.com>
- Fix for Red Hat 9+

* Sat Jul 26 2003 Mr. Sam 0.52
- Use wide-char compatible ncurses in current RH Beta.

* Wed Mar  5 2003 Mr. Sam <mrsam@courier-mta.com>
- Initial build.
