Name:           libdvdnav
Version:        5.0.3
Release:        3%{?dist}
Summary:        A library for reading DVD video discs based on Ogle code
License:        GPLv2+
URL:            http://dvdnav.mplayerhq.hu/

Source0:        https://download.videolan.org/pub/videolan/%{name}/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  libdvdread-devel >= 5.0.2

%description
%{name} provides a simple library for reading DVD video discs. The code is
based on Ogle and used in, among others, the Xine dvdnav plug-in.

%package        devel
Summary:        Development files for libdvdnav
Requires:       %{name} = %{version}-%{release}
Requires:       libdvdread-devel >= 5.0.2
Requires:       pkgconfig

%description    devel
%{name}-devel contains the files necessary to build packages that use the
%{name} library.

%prep
%setup -q

%build
%configure --disable-static

make %{?_smp_mflags}
pushd doc
doxygen doxy.conf
popd

%install
%make_install
rm -fr %{buildroot}%{_docdir}/%{name}
find %{buildroot} -name "*.la" -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog README
%{_libdir}/%{name}.so.*

%files devel
%doc doc/html/*
%{_libdir}/%{name}.so
%{_includedir}/dvdnav
%{_libdir}/pkgconfig/dvdnav.pc

%changelog
* Wed Dec 30 2015 Simone Caronni <negativo17@gmail.com> - 5.0.3-3
- Make the package build also on RHEL/CentOS 7.
- Add license macro.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 07 2015 Dominik Mierzejewski <rpm[AT]greysector.net> 5.0.3-1
- update to 5.0.3
- drop obsolete patches
- BR libdvdread 5.0.2

* Fri Oct 03 2014 Dominik Mierzejewski <rpm[AT]greysector.net> 5.0.1-2.20140901gite225924
- backport patches upstream git master to fix several known bugs
  (LP #1236939, #570790)

* Sat Sep 20 2014 Dominik Mierzejewski <rpm[AT]greysector.net> 5.0.1-1
- update to 5.0.1
- drop obsolete patches

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 09 2014 Dominik Mierzejewski <rpm[AT]greysector.net> 4.2.1-3
- drop obsolete patch
- fix FTBFS (rhbz#1106007)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 19 2013 Dominik Mierzejewski <rpm[AT]greysector.net> 4.2.1-1
- update to 4.2.1
- drop obsolete/redundant specfile elements
- add upstream URL

* Tue Sep 10 2013 Dominik Mierzejewski <rpm[AT]greysector.net> 4.2.0-6
- fix segfault when cell is empty, patch by Simo Sorce, bug #902037

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 09 2011 Dominik Mierzejewski <rpm[AT]greysector.net> 4.2.0-1
- update to 4.2.0

* Mon Apr 11 2011 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.4-0.3.svn1226
- update to SVN r1226

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.4-0.2.svn1184
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 26 2009 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.4-0.1.svn1184
- fix multilib conflict, based on a patch by Rex Dieter (rhbz#477684)
- update to SVN r1184
- move TODO to devel docs

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 09 2008 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.3-1
- update to 4.1.3 final

* Sun Aug 31 2008 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.3-0.4.rc1
- update to 4.1.3rc1
- require libdvdread with fixed API

* Fri Jul 25 2008 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.3-0.3
- add missing file to -devel

* Thu Jul 17 2008 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.3-0.2
- update to current SVN
- use new external libdvdread

* Fri Jun 06 2008 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.3-0.1
- update to current SVN (pre-4.1.3)
- macroize
- re-enable parallel make

* Sun Apr 13 2008 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.2-1
- update to 4.1.2
- drop obsolete patches (merged upstream)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.1.1-6
- Autorebuild for GCC 4.3

* Sun Jan 27 2008 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.1-5
- fix missing <inttypes.h> include (bug 428910)

* Sun Jan 06 2008 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.1-4
- make sure -devel requires our version of libdvdread-devel

* Thu Nov 22 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.1-3
- fix build with internal libdvdread

* Wed Nov 21 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.1-2
- use upstream non-autotools buildsystem
- build with external libdvdread for older releases
- fix version.h
- fix soname
- fix lib paths on 64bit

* Thu Nov 01 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 4.1.1-1
- switch to new upstream
- libdvdread comes from here now
- apply dvdread udf-related fixes from upstream SVN

* Sun Aug 19 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 0.1.10-4.20070819
- update to current snapshot
- specfile cleanups

* Thu May 03 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 0.1.10-3.20070503
- update to current snapshot from new upstream
- clean up some specfile cruft
- disable static libs
- drop unnecessary explicit dependency on libdvdread

* Mon Mar 13 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0.1.10-2
- Drop Epoch completely

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop Epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Wed Oct 13 2004 Ville Skytt?? <ville.skytta at iki.fi> - 0:0.1.10-0.lvn.1
- Update to 0.1.10.
- Disable dependency tracking to speed up the build.

* Wed Jun 25 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:0.1.9-0.fdr.2: incorporated bugzilla suggestions, new release

* Thu May 29 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:0.1.9-0.fdr.1: initial RPM release
