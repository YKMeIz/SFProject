Summary: PDF rendering library
Name:    poppler
Version: 0.41.0
Release: 1%{?dist}
License: (GPLv2 or GPLv3) and GPLv2+ and LGPLv2+ and MIT
Group:   Development/Libraries
URL:     http://poppler.freedesktop.org/
Source0: http://poppler.freedesktop.org/poppler-%{version}.tar.xz

# https://bugzilla.redhat.com/show_bug.cgi?id=1185007
Patch0:  poppler-0.30.0-rotated-words-selection.patch

## upstreamable patches
# fix configure checks for moc versions
Patch50: poppler-0.24.2-mocversiongrep.patch

Requires: poppler-data >= 0.4.0
BuildRequires: automake libtool
BuildRequires: gettext-devel
BuildRequires: libjpeg-devel
BuildRequires: openjpeg2-devel
BuildRequires: pkgconfig(cairo) >= 1.10.0
BuildRequires: pkgconfig(gobject-introspection-1.0) 
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(QtGui) pkgconfig(QtXml)
BuildRequires: pkgconfig(Qt5Gui) pkgconfig(Qt5Xml)
BuildRequires: pkgconfig(libtiff-4)


%description
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

%package devel
Summary: Libraries and headers for poppler
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
You should install the poppler-devel package if you would like to
compile applications based on poppler.

%package glib
Summary: Glib wrapper for poppler
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description glib
%{summary}.

%package glib-devel
Summary: Development files for glib wrapper
Group: Development/Libraries
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description glib-devel
%{summary}.


%package qt
Summary: Qt4 wrapper for poppler
Group:   System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?_qt4:Requires: qt4%{?_isa} >= %{_qt4_version}}
Obsoletes: poppler-qt4 < 0.16.0-3
Provides:  poppler-qt4 = %{version}-%{release}
%description qt
%{summary}.

%package qt-devel
Summary: Development files for Qt4 wrapper
Group:   Development/Libraries
Requires: %{name}-qt%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes: poppler-qt4-devel < 0.16.0-3
Provides:  poppler-qt4-devel = %{version}-%{release}
Requires: qt4-devel
%description qt-devel
%{summary}.

%package qt5
Summary: Qt5 wrapper for poppler
Group:   System Environment/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%{?_qt5:Requires: qt5-qtbase%{?_isa} >= %{_qt5_version}}
%description qt5
%{summary}.

%package qt5-devel
Summary: Development files for Qt5 wrapper
Group:   Development/Libraries
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel
%description qt5-devel
%{summary}.


%package cpp
Summary: Pure C++ wrapper for poppler
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cpp
%{summary}.

%package cpp-devel
Summary: Development files for C++ wrapper
Group: Development/Libraries
Requires: %{name}-cpp%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

%description cpp-devel
%{summary}.

%package utils
Summary: Command line utilities for converting PDF files
Group: Applications/Text
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} < 11 && 0%{?rhel} < 6
#  last seen in fc8
Provides: pdftohtml = 0.36-11
Obsoletes: pdftohtml < 0.36-11
#  last seen in fc7
Provides: xpdf-utils = 1:3.01-27
Obsoletes: xpdf-utils < 1:3.01-27
# even earlier?
Conflicts: xpdf <= 1:3.01-8
%endif
%description utils
Poppler, a PDF rendering library, is a fork of the xpdf PDF
viewer developed by Derek Noonburg of Glyph and Cog, LLC.

This utils package installs a number of command line tools for
converting PDF files to a number of other formats.

%package demos
Summary: Demos for poppler
Group: Applications/Text
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

%description demos
%{summary}.

%prep
%setup -q
%patch0 -p1 -b .rotated-words-selection

%patch50 -p1 -b .mocversiongrep

# hammer to nuke rpaths, recheck on new releases
autoreconf -i -f


%build

%configure \
  --disable-silent-rules \
  --disable-static \
  --enable-cairo-output \
  --enable-libjpeg \
  --enable-libopenjpeg=openjpeg2 \
  --enable-poppler-qt4 \
  --enable-poppler-qt5 \
  --enable-xpdf-headers \
  --disable-zlib \
  --enable-introspection=yes

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -fv $RPM_BUILD_ROOT%{_libdir}/lib*.la


%check
# verify pkg-config sanity/version
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion poppler)" = "%{version}"
test "$(pkg-config --modversion poppler-cairo)" = "%{version}"
test "$(pkg-config --modversion poppler-cpp)" = "%{version}"
test "$(pkg-config --modversion poppler-glib)" = "%{version}"
test "$(pkg-config --modversion poppler-qt4)" = "%{version}"
test "$(pkg-config --modversion poppler-qt5)" = "%{version}"
test "$(pkg-config --modversion poppler-splash)" = "%{version}"


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post glib -p /sbin/ldconfig

%postun glib -p /sbin/ldconfig

%post qt -p /sbin/ldconfig

%postun qt -p /sbin/ldconfig

%post qt5 -p /sbin/ldconfig

%postun qt5 -p /sbin/ldconfig

%post cpp -p /sbin/ldconfig

%postun cpp -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libpoppler.so.58*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler.pc
%{_libdir}/pkgconfig/poppler-splash.pc
%{_libdir}/libpoppler.so
%dir %{_includedir}/poppler/
# xpdf headers
%{_includedir}/poppler/*.h
%{_includedir}/poppler/fofi/
%{_includedir}/poppler/goo/
%{_includedir}/poppler/splash/
%{_datadir}/gtk-doc/

%files glib
%defattr(-,root,root,-)
%{_libdir}/libpoppler-glib.so.8*
%{_libdir}/girepository-1.0/Poppler-0.18.typelib

%files glib-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler-glib.pc
%{_libdir}/pkgconfig/poppler-cairo.pc
%{_libdir}/libpoppler-glib.so
%{_datadir}/gir-1.0/Poppler-0.18.gir
%{_includedir}/poppler/glib/

%files qt
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt4.so.4*

%files qt-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt4.so
%{_libdir}/pkgconfig/poppler-qt4.pc
%{_includedir}/poppler/qt4/

%files qt5
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt5.so.1*

%files qt5-devel
%defattr(-,root,root,-)
%{_libdir}/libpoppler-qt5.so
%{_libdir}/pkgconfig/poppler-qt5.pc
%{_includedir}/poppler/qt5/

%files cpp
%defattr(-,root,root,-)
%{_libdir}/libpoppler-cpp.so.0*

%files cpp-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/poppler-cpp.pc
%{_libdir}/libpoppler-cpp.so
%{_includedir}/poppler/cpp

%files utils
%defattr(-,root,root,-)
%{_bindir}/pdf*
%{_mandir}/man1/*

%files demos
%defattr(-,root,root,-)
%{_bindir}/poppler-glib-demo


%changelog
* Fri Feb 26 2016 Marek Kasik <mkasik@redhat.com> - 0.41.0-1
- Update to 0.41.0
- Resolves: #1309145

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Marek Kasik <mkasik@redhat.com> - 0.40.0-1
- Update to 0.40.0
- Resolves: #1251781

* Wed Jul 22 2015 Marek Kasik <mkasik@redhat.com> - 0.34.0-1
- Update to 0.34.0
- Resolves: #1241305

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun  5 2015 Marek Kasik <mkasik@redhat.com> - 0.33.0-1
- Update to 0.33.0
- Resolves: #1190427

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.30.0-5
- Rebuilt for GCC 5 C++11 ABI change

* Thu Mar 26 2015 Marek Kasik <mkasik@redhat.com> - 0.30.0-4
- Respect orientation when selecting words
- Resolves: #1185007

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.30.0-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Jan 23 2015 Marek Kasik <mkasik@redhat.com> - 0.30.0-2
- Use libopenjpeg2 instead of libopenjpeg

* Fri Jan 23 2015 Marek Kasik <mkasik@redhat.com> - 0.30.0-1
- Update to 0.30.0
- Resolves: #1171056

* Tue Jan 20 2015 Marek Kasik <mkasik@redhat.com> - 0.28.1-3
- Revert previous commit (It needs poppler-0.30.0)

* Tue Jan 20 2015 Marek Kasik <mkasik@redhat.com> - 0.28.1-2
- Use libopenjpeg2 instead of libopenjpeg

* Fri Nov 14 2014 Marek Kasik <mkasik@redhat.com> - 0.28.1-1
- Update to 0.28.1
- Resolves: #1147443

* Wed Aug 27 2014 Marek Kasik <mkasik@redhat.com> - 0.26.4-1
- Update to 0.26.4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Marek Kasik <mkasik@redhat.com> - 0.26.3-1
- Update to 0.26.3

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.26.2-2
- Rebuilt for gobject-introspection 1.41.4

* Fri Jun 27 2014 Marek Kasik <mkasik@redhat.com> - 0.26.2-1
- Update to 0.26.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Marek Kasik <mkasik@redhat.com> - 0.26.0-1
- Update to 0.26.0

* Fri Jan  3 2014 Marek Kasik <mkasik@redhat.com> - 0.24.3-3
- Use correct format string
- Resolves: #1048202

* Mon Nov 11 2013 Rex Dieter <rdieter@fedoraproject.org> 0.24.3-2
- rebuild (qt5 qreal/arm)

* Tue Oct 29 2013 Marek Kasik <mkasik@redhat.com> - 0.24.3-1
- Update to 0.24.3
- Resolves: #1023712

* Fri Oct 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.24.2-4
- fix mocversiongrep configure checks (so Qt 5.2 works)
- %%configure --disable-silent-rules

* Fri Oct 18 2013 Rex Dieter <rdieter@fedoraproject.org> 0.24.2-3
- undo ExcludeArch: ppc ppc64 (qt5-qtbase-5.1.1-6+ fixed)

* Thu Oct 17 2013 Rex Dieter <rdieter@fedoraproject.org> 0.24.2-2
- -qt5: ExcludeArch: ppc ppc64 (f20, hopefully temporary)

* Mon Sep 30 2013 Marek Kasik <mkasik@redhat.com> - 0.24.2-1
- Update to 0.24.2

* Mon Sep 30 2013 Marek Kasik <mkasik@redhat.com> - 0.24.1-2
- Don't convert pdftohtml.1 to UTF-8, it is already UTF-8

* Tue Aug 27 2013 Marek Kasik <mkasik@redhat.com> - 0.24.1-1
- Update to 0.24.1

* Tue Aug 20 2013 Marek Kasik <mkasik@redhat.com> - 0.24.0-2
- Fix Qt5 requirements

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 0.24.0-1
- Update to 0.24.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Marek Kasik <mkasik@redhat.com> 0.22.5-1
- Update to 0.22.5

* Thu Jun 20 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-5
- Switch from LCMS to LCMS2
- Resolves: #975465

* Wed Jun  5 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-4
- Fix changelog dates

* Fri Apr 12 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-3
- Enable generating of TIFF files by pdftoppm

* Thu Apr 11 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-2
- Fix man pages of pdftops and pdfseparate

* Wed Feb 27 2013 Marek Kasik <mkasik@redhat.com> 0.22.1-1
- Update to 0.22.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Rex Dieter <rdieter@fedoraproject.org> 0.22.0-2
- -demos: omit extraneous (and broken) dep

* Fri Jan 18 2013 Marek Kasik <mkasik@redhat.com> 0.22.0-1
- Update to 0.22.0

* Tue Nov 13 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-9
- Move poppler-glib-demo to new sub-package demos
- Resolves: #872338

* Mon Nov 12 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-8
- Add references to corresponding bugs for poppler-0.20.3-5.patch

* Tue Nov  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-7
- Add missing hunk to patch poppler-0.20.3-5.patch

* Tue Nov  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-6
- Backport most of the changes from poppler-0.20.3 - poppler-0.20.5
-   (those which doesn't change API or ABI and are important)
- See poppler-0.20.3-5.patch for detailed list of included commits

* Wed Oct 31 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-5
- Remove unused patch

* Wed Oct 31 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-4
- Update License field

* Mon Aug  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-3
- Fix conversion to ps when having multiple strips

* Mon Aug  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-2
- Make sure xScale and yScale are always initialized
- Resolves: #840515

* Mon Aug  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.2-1
- Update to 0.20.2

* Mon Aug  6 2012 Marek Kasik <mkasik@redhat.com> 0.20.1-3
- Try empty string instead of NULL as password if needed
- Resolves: #845578

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  2 2012 Marek Kasik <mkasik@redhat.com> 0.20.1-1
- Update to 0.20.1

* Mon Jun 25 2012 Nils Philippsen <nils@redhat.com>
- license is "GPLv2 or GPLv3" from poppler-0.20.0 on (based off xpdf-3.03)

* Wed May 16 2012 Marek Kasik <mkasik@redhat.com> 0.20.0-1
- Update to 0.20.0

* Fri May  4 2012 Marek Kasik <mkasik@redhat.com> 0.18.4-3
- Backport of a patch which sets mask matrix before drawing an image with a mask
- Resolves: #817378

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.4-2
- Rebuilt for c++ ABI breakage

* Sat Feb 18 2012 Rex Dieter <rdieter@fedoraproject.org> 0.18.4-1
- 0.18.4

* Thu Feb 09 2012 Rex Dieter <rdieter@fedoraproject.org> 0.18.3-3
- rebuild (openjpeg)

* Tue Jan 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.18.3-2
- -devel: don't own all headers

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 0.18.3-1
- 0.18.3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Marek Kasik <mkasik@redhat.com> - 0.18.2-1
- Update to 0.18.2
- Remove upstreamed patches

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 0.18.1-3
- Rebuild for new libpng

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> 0.18.1-2
- poppler-glib.pc pkgconfig file broken (#749898)
- %%check: verify pkgconfig sanity

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> 0.18.1-1
- Update to 0.18.1
- pkgconfig-style deps
- tighten deps with %%_isa

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 0.18.0-2
- rebuild 

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 0.18.0-1
- Update to 0.18.0

* Mon Sep 26 2011 Marek Kasik <mkasik@redhat.com> - 0.17.3-2
- Don't include pdfextract and pdfmerge in resulting packages for now
- since they conflict with packages pdfmerge and mupdf (#740906)

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 0.17.3-1
- Update to 0.17.3

* Wed Aug 17 2011 Marek Kasik <mkasik@redhat.com> - 0.17.0-2
- Fix a problem with freeing of memory in PreScanOutputDev (#730941)

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 0.17.0-1
- Update to 0.17.0

* Thu Jun 30 2011 Rex Dieter <rdieter@fedoraproject.org> 0.16.7-1
- 0.16.7

* Wed Jun 22 2011 Marek Kasik <mkasik@redhat.com> - 0.16.6-2
- Drop dependency on gtk-doc (#604412)

* Thu Jun  2 2011 Marek Kasik <mkasik@redhat.com> - 0.16.6-1
- Update to 0.16.6

* Thu May  5 2011 Marek Kasik <mkasik@redhat.com> - 0.16.5-1
- Update to 0.16.5

* Thu Mar 31 2011 Marek Kasik <mkasik@redhat.com> - 0.16.4-1
- Update to 0.16.4

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.16.3-2
- Update to 0.16.3

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 0.16.3-1
- Update to 0.16.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Marek Kasik <mkasik@redhat.com> - 0.16.2-1
- Update to 0.16.2

* Tue Jan 18 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.16.0-3
- drop qt3 bindings
- rename -qt4 -> -qt

* Wed Jan 12 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.16.0-2
- rebuild (openjpeg)

* Mon Dec 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.16.0-1
- 0.16.0

* Fri Dec 10 2010 Marek Kasik <mkasik@redhat.com> - 0.15.3-1
- Update to 0.15.3

* Mon Nov  1 2010 Marek Kasik <mkasik@redhat.com> - 0.15.1-1
- Update to 0.15.1
- Remove CVE-2010-3702, 3703 and 3704 patches (they are already in 0.15.1)

* Thu Oct  7 2010 Marek Kasik <mkasik@redhat.com> - 0.15.0-5
- Add poppler-0.15.0-CVE-2010-3702.patch
    (Properly initialize parser)
- Add poppler-0.15.0-CVE-2010-3703.patch
    (Properly initialize stack)
- Add poppler-0.15.0-CVE-2010-3704.patch
    (Fix crash in broken pdf (code < 0))
- Resolves: #639861

* Wed Sep 29 2010 jkeating - 0.15.0-4
- Rebuilt for gcc bug 634757

* Mon Sep 27 2010 Marek Kasik <mkasik@redhat.com> - 0.15.0-3
- Remove explicit requirement of gobject-introspection

* Fri Sep 24 2010 Marek Kasik <mkasik@redhat.com> - 0.15.0-2
- Move requirement of gobject-introspection to glib sub-package

* Fri Sep 24 2010 Marek Kasik <mkasik@redhat.com> - 0.15.0-1
- Update to 0.15.0
- Enable introspection

* Sat Sep 11 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.14.3-1
- Update to 0.14.3

* Thu Aug 19 2010 Marek Kasik <mkasik@redhat.com> - 0.14.2-1
- Update to 0.14.2
- Remove poppler-0.12.1-objstream.patch

* Fri Jul 16 2010 Marek Kasik <mkasik@redhat.com> - 0.14.1-1
- Update to 0.14.1
- Don't apply poppler-0.12.1-objstream.patch, it is not needed anymore

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.14.0-1
- Update to 0.14.0

* Wed May 26 2010 Marek Kasik <mkasik@redhat.com> - 0.13.4-1
- poppler-0.13.4

* Mon May  3 2010 Marek Kasik <mkasik@redhat.com> - 0.13.3-2
- Update "sources" file
- Add BuildRequires "gettext-devel"

* Fri Apr 30 2010 Marek Kasik <mkasik@redhat.com> - 0.13.3-1
- poppler-0.13.3

* Thu Mar  4 2010 Marek Kasik <mkasik@redhat.com> - 0.12.4-2
- Fix showing of radio buttons (#480868)

* Thu Feb 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.4-1
- popper-0.12.4

* Tue Feb 16 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-9
- Fix downscaling of rotated pages (#563353)

* Thu Jan 28 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-8
- Get current FcConfig before using it (#533992)

* Sun Jan 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-7
- use alternative/upstream downscale patch (#556549, fdo#5589)

* Wed Jan 20 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-6
- Add dependency on poppler-data (#553991)

* Tue Jan 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-5
- cairo backend, scale images correctly (#556549, fdo#5589)

* Fri Jan 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-4
- Sanitize versioned Obsoletes/Provides

* Fri Jan 15 2010 Marek Kasik <mkasik@redhat.com> - 0.12.3-3
- Correct permissions of goo/GooTimer.h
- Convert pdftohtml.1 to utf8
- Make the pdftohtml's Provides/Obsoletes versioned

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.12.3-1
- poppler-0.12.3

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.2-1
- poppler-0.12.2

* Sun Oct 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.1-3
- CVE-2009-3607 poppler: create_surface_from_thumbnail_data
  integer overflow (#526924)

* Mon Oct 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.1-1
- poppler-0.12.1
- deprecate xpdf/pdftohtml Conflicts/Obsoletes

* Wed Sep 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0

* Tue Aug 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.3-1
- Update to 0.11.3

* Mon Aug  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.1-2
- omit poppler-data (#507675)

* Tue Jun 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.1-1
- poppler-0.11.1

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-6
- reduce lib deps in qt/qt4 pkg-config support

* Sat Jun 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-5
- --enable-libjpeg
- (explicitly) --disable-zlib

* Fri Jun 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-3
- --enable-libopenjpeg, --disable-zlib

* Sun May 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.11.0-2
- update changelog
- track sonames

* Tue May 19 2009 Bastien Nocera <bnocera@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Thu Mar 12 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.5-1
- Update to 0.10.5

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.4-1
- Update to 0.10.4

* Tue Jan 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.10.3-2
- add needed scriptlets
- nuke rpaths

* Tue Jan 13 2009 Matthias Clasen <mclasen@redhat.com> - 0.10.3-1
- Update to 0.10.3

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.10.2-1
- Update to 0.10.2

* Tue Nov 11 2008 Matthias Clasen <mclasen@redhat.com> - 0.10.1-1
- Update to 0.10.1 and  -data 0.2.1

* Tue Sep 16 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.8.7-2
- cleanup qt3 hack
- %%description cosmetics

* Sun Sep  7 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.7-1
- Update to 0.8.7

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.6-1
- Update to 0.8.6

* Tue Aug 05 2008 Colin Walters <walters@redhat.com> - 0.8.5-1
- Update to 0.8.5

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Mon Apr 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Sun Apr 06 2008 Adam Jackson <ajax@redhat.com> 0.8.0-3
- poppler-0.8.0-ocg-crash.patch: Fix a crash when no optional content
  groups are defined.
- Mangle configure to account for the new directory for qt3 libs.
- Fix grammar in %%description.

* Tue Apr 01 2008 Rex Dieter <rdieter@fedoraproject.org> - 0.8.0-2
- -qt-devel: Requires: qt3-devel

* Sun Mar 30 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Sun Mar 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Wed Mar 12 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Thu Feb 28 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Thu Feb 21 2008 Matthias Clasen <mclasen@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.4-4
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Jindrich Novy <jnovy@redhat.com> - 0.6.4-3
- apply ObjStream patch (#433090)

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.4-2
- Add some required inter-subpackge deps

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.4-1
- Update to 0.6.4
- Split off poppler-glib

* Sun Dec  2 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-3
- Fix the qt3 checks some more

* Wed Nov 28 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-2
- package xpdf headers in poppler-devel (Jindrich Novy)
- Fix qt3 detection (Denis Leroy)

* Thu Nov 22 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Thu Oct 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 0.6-2
- include qt4 wrapper

* Tue Sep  4 2007 Kristian Høgsberg <krh@redhat.com> - 0.6-1
- Update to 0.6

* Wed Aug 15 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.91-2
- Remove debug spew

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.91-1
- Update to 0.5.91

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.9-2
- Update the license field

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.5.9-1
- Update to 0.5.9

* Thu Mar  1 2007 Bill Nottingham <notting@redhat.com> - 0.5.4-7
- fix it so the qt pkgconfig/.so aren't in the main poppler-devel

* Fri Dec 15 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-5
- Include epoch in the Provides/Obsoletes for xpdf-utils

* Wed Dec 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-4
- Add Provides/Obsoletes for xpdf-utils (#219033)

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> - 0.5.4-3
- drop hard-wired: Req: gtk2
- --disable-static
- enable qt wrapper
- -devel: Requires: pkgconfig

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 0.5.4-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.4-1.fc6
- Rebase to 0.5.4, drop poppler-0.5.3-libs.patch, fixes #205813,
  #205549, #200613, #172137, #172138, #161293 and more.

* Wed Sep 13 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.3-3.fc6
- Move .so to -devel (#203637).

* Mon Aug 14 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.3-2.fc6
- link against fontconfig (see bug 202256)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.3-1.1
- rebuild

* Wed May 31 2006 Kristian Høgsberg <krh@redhat.com> 0.5.3-1
- Update to 0.5.3.

* Mon May 22 2006 Kristian Høgsberg <krh@redhat.com> 0.5.2-1
- Update to 0.5.2.

* Wed Mar  1 2006 Kristian Høgsberg <krh@redhat.com> 0.5.1-2
- Rebuild the get rid of old soname dependency.

* Tue Feb 28 2006 Kristian Høgsberg <krh@redhat.com> 0.5.1-1
- Update to version 0.5.1.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.5.0-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.5.0-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.com> - 0.5.0-4
- change xpdf conflict version to be <= instead of <

* Wed Jan 18 2006 Ray Strode <rstrode@redhat.com> - 0.5.0-3
- update conflicts: xpdf line to be versioned

* Wed Jan 11 2006 Kristian Høgsberg <krh@redhat.com> - 0.5.0-2.0
- Update to 0.5.0 and add poppler-utils subpackage.
- Flesh out poppler-utils subpackage.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Sep  4 2005 Kristian Høgsberg <krh@redhat.com> - 0.4.2-1
- Update to 0.4.2 and disable splash backend so we don't build it.

* Fri Aug 26 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.4.1-2
- Rebuild

* Fri Aug 26 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Wed Aug 17 2005 Kristian Høgsberg <krh@redhat.com> - 0.4.0-2
- Bump release and rebuild.

* Wed Aug 17 2005 Marco Pesenti gritti <mpg@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Mon Aug 15 2005 Kristian Høgsberg <krh@redhat.com> - 0.3.3-2
- Rebuild to pick up new cairo soname.

* Mon Jun 20 2005 Kristian Høgsberg <krh@redhat.com> - 0.3.3-1
- Update to 0.3.3 and change to build cairo backend.

* Sun May 22 2005 Marco Pesenti gritti <mpg@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Sat May  7 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.1
- Update to 0.3.1

* Sat Apr 23 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.3.0
- Update to 0.3.0

* Wed Apr 13 2005 Florian La Roche <laroche@redhat.com>
- remove empty post/postun scripts

* Wed Apr  6 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.2.0-1
- Update to 0.2.0

* Sat Mar 12 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.2-1
- Update to 0.1.2
- Use tar.gz because there are not bz of poppler

* Wed Mar  2 2005 Marco Pesenti Gritti <mpg@redhat.com> - 0.1.1-1
- Initial build
