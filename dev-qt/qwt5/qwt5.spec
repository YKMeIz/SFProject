
# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Name:    qwt5
Summary: Qt Widgets for Technical Applications
Version: 5.2.2
Release: 26%{?dist}

License: LGPLv2 with exceptions
URL:     http://qwt.sourceforge.net/
Source:  http://downloads.sourceforge.net/qwt/qwt-%{version}.tar.bz2

## upstreamable patches
# use qt_install system paths
Patch50: qwt-5.2.2-qt_install_paths.patch 

BuildRequires: pkgconfig(QtGui) pkgconfig(QtSvg)

%description
The Qwt library contains GUI Components and utility classes which are primarily
useful for programs with a technical background.
Besides a 2D plot widget it provides scales, sliders, dials, compasses,
thermometers, wheels and knobs to control or display values, arrays
or ranges of type double.

%package qt4
Obsoletes: qwt < 5.2.2-20
Summary: Qt Widgets for Technical Applications 
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}
%description qt4 
The Qwt library contains GUI Components and utility classes which are primarily
useful for programs with a technical background.
Besides a 2D plot widget it provides scales, sliders, dials, compasses,
thermometers, wheels and knobs to control or display values, arrays
or ranges of type double.

%package qt4-devel
Summary:  Development files for %{name}
Obsoletes: qwt-devel < 5.2.2-20
Requires: %{name}-qt4%{?_isa} = %{version}-%{release}
%description qt4-devel
%{summary}.

%package doc
Summary: Extra Developer documentation for %{name}
Obsoletes: qwt-doc < 5.2.2-20
BuildArch: noarch
%description doc
%{summary}.



%prep
%setup -q -n qwt-%{version}

%patch50 -p1 -b .qt_install_paths


%build
%{?_qt4_qmake} \
  CONFIG+=QwtSVGItem 

make %{?_smp_mflags}


%install
make install INSTALL_ROOT=%{buildroot}

# hacks for parallel-installability with qwt(6)
mv %{buildroot}%{_qt4_libdir}/libqwt.so \
   %{buildroot}%{_qt4_libdir}/libqwt5-qt4.so
mv %{buildroot}%{_qt4_libdir}/pkgconfig/qwt.pc \
   %{buildroot}%{_qt4_libdir}/pkgconfig/qwt5-qt4.pc
sed -i -e 's|-lqwt|-lqwt5-qt4|g' %{buildroot}%{_qt4_libdir}/pkgconfig/qwt5-qt4.pc

# fixup docs bogosity
mv %{buildroot}%{_qt4_docdir}/html/html \
   %{buildroot}%{_qt4_docdir}/html/qwt5


%post qt4 -p /sbin/ldconfig
%postun qt4 -p /sbin/ldconfig

%files qt4
%doc CHANGES
%doc COPYING
%doc README
%{_qt4_libdir}/libqwt.so.5*
%{?_qt4_plugindir}/designer/libqwt5_designer_plugin.so

%files qt4-devel
%{_mandir}/man3/*
%{_qt4_headerdir}/qwt5-qt4/
%{_qt4_libdir}/libqwt5-qt4.so
%{_qt4_libdir}/pkgconfig/qwt5-qt4.pc

%files doc
# own these to avoid needless dep on qt/qt-doc
%dir %{_qt4_docdir}
%dir %{_qt4_docdir}/html/
%{_qt4_docdir}/html/qwt5/


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 29 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.2.2-24
- cleanup
- rework to avoid CONFIG+=install-qt 

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-21
- don't change soname, just libqwt.so symlink

* Fri Aug 03 2012 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-20
- pkgconfig support
- bump release to -20

* Tue Jul 31 2012 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-5
- make parallel-installable with qwt6

* Tue Jul 31 2012 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-4
- Provides: qwt5-qt4(-devel)
- pkgconfig-style deps

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 07 2011 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-1
- 5.2.2

* Thu Jul 14 2011 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- .spec cosmetics
- use %%_qt4_ macros
- -doc subpkg here (instead of separately built)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr 16 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.1-1
- update to 5.2.1 

* Fri Feb 05 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.0-1
- fix wrong lib names

* Fri Feb 05 2010 Frank Büttner <frank-buettner@gmx.net> - 5.2.0-0
- update to 5.2.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 04 2009 Frank Büttner <frank-buettner@gmx.net> - 5.1.1-2
 - modify path patch

* Sun Jan 04 2009 Frank Büttner <frank-buettner@gmx.net> - 5.1.1-1
 -update to 5.1.1

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.0.2-6
- Autorebuild for GCC 4.3

* Sat Sep 29 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-5
 - add EPEL support

* Sat Sep 29 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-4
- remove parallel build, because it will fail sometimes

* Fri Sep 28 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-3
- fix some errors in the spec file

* Fri Jul 06 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-2
- fix some errors in the spec file

* Mon Jun 11 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.2-1
- update to 5.0.2
- split doc

* Thu May 15 2007 Frank Büttner <frank-buettner@gmx.net> - 5.0.1-1
 - start

