
%if 0%{?rhel} == 6
%define cmake_pkg cmake28
%else
%define cmake_pkg cmake
%endif

Name:    smokeqt
Version: 4.14.2
Release: 1%{?dist}
Summary: Bindings for Qt libraries

License: LGPLv2+
URL:     https://projects.kde.org/projects/kde/kdebindings/smoke
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: %{cmake_pkg}
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(qimageblitz)
# qt4-devel
BuildRequires: pkgconfig(QtGui) pkgconfig(QtScript) pkgconfig(QtXml)
BuildRequires: pkgconfig(QtDeclarative) pkgconfig(QtMultimedia)
BuildRequires: pkgconfig(QtWebKit)
BuildRequires: pkgconfig(qwt5-qt4)
BuildRequires: qscintilla-devel >= 2.4
BuildRequires: smokegen-devel >= %{version}

Conflicts: kdebindings < 4.7.0 

%{?_qt4:Requires: qt4%{?_isa} >= %{_qt4_version}}
Requires: smokegen%{?_isa} >= %{version}

%description
This package includes Bindings for Qt libraries.

%package devel
Summary: Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: smokegen-devel 
Conflicts: kdebindings-devel < 4.7.0 
%description devel
%{summary}.

%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{?cmake28}%{!?cmake28:%{?cmake}} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING.LIB
%{_libdir}/libsmokephonon.so.3*
%{_libdir}/libsmokeqimageblitz.so.3*
%{_libdir}/libsmokeqsci.so.3*
%{_libdir}/libsmokeqt3support.so.3*
%{_libdir}/libsmokeqtcore.so.3*
%{_libdir}/libsmokeqtdbus.so.3*
%{_libdir}/libsmokeqtdeclarative.so.3*
%{_libdir}/libsmokeqtgui.so.3*
%{_libdir}/libsmokeqthelp.so.3*
%{_libdir}/libsmokeqtmultimedia.so.3*
%{_libdir}/libsmokeqtnetwork.so.3*
%{_libdir}/libsmokeqtopengl.so.3*
%{_libdir}/libsmokeqtscript.so.3*
%{_libdir}/libsmokeqtsql.so.3*
%{_libdir}/libsmokeqtsvg.so.3*
%{_libdir}/libsmokeqttest.so.3*
%{_libdir}/libsmokeqtuitools.so.3*
%{_libdir}/libsmokeqtwebkit.so.3*
%{_libdir}/libsmokeqtxml.so.3*
%{_libdir}/libsmokeqtxmlpatterns.so.3*
%{_libdir}/libsmokeqwt.so.3*

%files devel
%{_libdir}/libsmoke*.so
%{_includedir}/smoke/*
%{_datadir}/smokegen/*
%{_datadir}/smoke/*


%changelog
* Sat Oct 11 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.2-1
- 4.14.2

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.1-1
- 4.14.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.0-1
- 4.14.0

* Tue Aug 05 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.97-1
- 4.13.97

* Sun Jul 13 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.3-1
- 4.13.3

* Mon Jun 09 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.2-1
- 4.13.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 11 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.1-1
- 4.13.1

* Fri Apr 11 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.0-1
- 4.13.0

* Thu Apr 03 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.97-1
- 4.12.97

* Sat Mar 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.95-1
- 4.12.95

* Tue Mar 18 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.90-1
- 4.12.90

* Sat Mar 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.3-1
- 4.12.3

* Fri Jan 31 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.2-1
- 4.12.2

* Fri Jan 10 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.1-1
- 4.12.1

* Wed Dec 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.12.0-1
- 4.12.0

* Sun Dec 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.97-1
- 4.11.97

* Thu Nov 21 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.95-1
- 4.11.95

* Fri Nov 15 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.90-1
- 4.11.90

* Fri Nov 08 2013 Rex Dieter <rdieter@fedoraproject.org> 4.11.3-2
- rebuild (qscintilla)

* Fri Nov 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.3-1
- 4.11.3

* Sat Sep 28 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-1
- 4.11.2

* Tue Sep 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.1-1
- 4.11.1

* Thu Aug 08 2013 Than Ngo <than@redhat.com> - 4.11.0-1
- 4.11.0

* Thu Jul 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.97-1
- 4.10.97

* Tue Jul 23 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.95-1
- 4.10.95

* Thu Jun 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.90-1
- 4.10.90
- track sonames

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Sat Mar 30 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.1-1
- 4.10.1

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.0-2
- don't override CXXFLAGS (#884836, kde#315772)

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Sat Jan 19 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Mon Dec 17 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-2
- rebuild (qcsintilla)

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.90-1
- 4.9.90

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Sat Oct 20 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.2-2
- rebuild (qwt5)

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Aug 02 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.0-2
- s/qwt/qwt5-qt4/

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.95-1
- 4.8.95

* Sun Jun 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.90-2
- rebuild (smokegen)

* Sat Jun 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Sun Jun 03 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- respin

* Sat May 26 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80
- install to smoke directory

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Sun Jan 22 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.7.97-1
- 4.7.97

* Sat Dec 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.95-2
- rebuild (qsintilla)

* Thu Dec 22 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> - 4.7.90-1
- 4.7.90

* Thu Nov 24 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.80-1
- 4.7.80 (beta 1)

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3
- more pkgconfig-style deps

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Thu Sep 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-3
- drop kde-deps
- update URL
- remove deprecated tags from .spec
- %%doc: AUTHORS COPYING.LIB

* Fri Sep 16 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.1-2
- BR: qt4-webkit-devel

* Tue Sep 06 2011 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Tue Jul 26 2011 Than Ngo <than@redhat.com> - 4.7.0-1
- 4.7.0

* Fri Jul 22 2011 Than Ngo <than@redhat.com> - 4.6.95-1
- 4.7 rc1

* Wed Jul 06 2011 Than Ngo <than@redhat.com> - 4.6.90-1
- first Fedora RPM
