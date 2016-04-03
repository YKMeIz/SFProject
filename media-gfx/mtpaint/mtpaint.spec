%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

%global docver 3.40

Summary:       Painting program for creating icons and pixel-based artwork
Name:          mtpaint
Version:       3.40
Release:       15%{?dist}
License:       GPLv3+
Group:         Applications/Multimedia
URL:           http://mtpaint.sourceforge.net/
Source0:       http://downloads.sf.net/%{name}/%{name}-%{version}.tar.bz2
Source1:       http://downloads.sf.net/%{name}/%{name}_handbook-%{docver}.zip
Patch0:        mtpaint-3.40-xdg-open.patch
Patch1:        mtpaint-3.31-png.patch
Patch2:        mtpaint-3.40-strip.patch
Patch3:        mtpaint-3.40-yad.patch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: giflib-devel
BuildRequires: gtk2-devel
BuildRequires: lcms2-devel
BuildRequires: libpng-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: openjpeg-devel
BuildRequires: zlib-devel
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: dos2unix
Requires:      ImageMagick
Requires:      /usr/bin/yad

%description 
mtPaint is a simple painting program designed for creating icons and
pixel-based artwork. It can edit indexed palette or 24 bit RGB images
and offers basic painting and palette manipulation tools. Its main
file format is PNG, although it can also handle JPEG, GIF, TIFF, BMP,
XPM, and XBM files.

%package       handbook
Summary:       Handbook for the mtpaint painting application
Group:         Applications/Multimedia
License:       GFDL
Requires:      %{name} = %{version}-%{release}
BuildArch:     noarch

%description   handbook
Install this package is want to read the handbook for the painting
application mtpaint.

%prep
%setup -q -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1

# We have moved docs
%if 0%{?fedora} >= 20
%{__sed} -i 's,"/usr/doc/mtpaint/index.html","%{_docdir}/%{name}-handbook/index.html",' src/spawn.c
%else
%{__sed} -i 's,"/usr/doc/mtpaint/index.html","%{_docdir}/%{name}-handbook-%{version}/index.html",' src/spawn.c
%endif

%{__chmod} 0755 %{name}_handbook-%{docver}/docs/{en_GB,img,files,cs}
dos2unix -k %{name}_handbook-%{docver}/docs/index.html
dos2unix -k %{name}_handbook-%{docver}/docs/{en_GB,cs}/*.html

%build
# This is not a "normal" configure
export CFLAGS="%{optflags}"
export LDFLAGS="%{?__global_ldflags}"
./configure \
    --prefix=%{_prefix} \
    --docdir=%{_pkgdocdir} \
    cflags asneeded intl man thread gtk2 GIF tiff jpeg jp2 imagick lcms2
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install MT_PREFIX=%{buildroot}%{_prefix}            \
                  MT_MAN_DEST=%{buildroot}%{_mandir}          \
                  MT_LANG_DEST=%{buildroot}%{_datadir}/locale \
                  MT_DATAROOT=%{buildroot}%{_datadir}         \
                  BIN_INSTALL=%{buildroot}%{_bindir}

desktop-file-install --delete-original         \
%if 0%{?fedora} && 0%{?fedora} < 19
    --vendor fedora                            \
%endif
    --dir %{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x %{_bindir}/update-desktop-database ] ; then
  %{_bindir}/update-desktop-database &> /dev/null
fi
exit 0

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
if [ -x %{_bindir}/update-desktop-database ] ; then
  %{_bindir}/update-desktop-database &> /dev/null
fi
exit 0

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-, root, root, -)
%doc COPYING NEWS README
%{_mandir}/man1/%{name}*
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/%{name}.png

%files handbook
%defattr(-, root, root, -)
%doc %{name}_handbook-%{docver}/COPYING %{name}_handbook-%{docver}/docs/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Terje Rosten <terje.rosten@ntnu.no> - 3.40-14
- New doc location

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 10 2013 Terje Rosten <terje.rosten@ntnu.no> - 3.40-12
- Print with yad

* Mon May 27 2013 Terje Rosten <terje.rosten@ntnu.no> - 3.40-11
- Add req. on kprinter (bz #964588)

* Thu Feb 14 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.40-10
- remove --vendor flag from desktop-file-install https://fedorahosted.org/fesco/ticket/1077

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 3.40-8
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 3.40-7
- rebuild against new libjpeg

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.40-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Terje Rosten <terje.rosten@ntnu.no> - 3.40-5
- Rebuilt for new libtiff

* Sun Feb 12 2012 Terje Rosten <terje.rosten@ntnu.no> - 3.40-4
- Rebuilt for new openjpeg

* Sun Feb 05 2012 Terje Rosten <terje.rosten@ntnu.no> - 3.40-3
- Fix ld flags

* Sun Feb 05 2012 Terje Rosten <terje.rosten@ntnu.no> - 3.40-2
- Don't strip bins (bz #787462)

* Sun Jan 29 2012 Terje Rosten <terje.rosten@ntnu.no> - 3.40-1
- Update to 3.40

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 07 2011 Terje Rosten <terje.rosten@ntnu.no> - 3.31-6
- Add png patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 11 2010 Terje Rosten <terje.rosten@ntnu.no> - 3.31-4
- Add DSO patch

* Wed Aug 19 2009 Christoph Wickert <cwickert@fedoraproject.org> - 3.31-3
- Update to 3.31
- Make handbook package noarch
- New gtk-update-icon-cache scriptlets

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 15 2008 Terje Rosten <terje.rosten@ntnu.no> - 3.21-1
- 3.21
- add %%defattr on handbook

* Sat Feb  9 2008 Terje Rosten <terje.rosten@ntnu.no> - 3.20-3
- Rebuild

* Wed Jan 23 2008 Terje Rosten <terje.rosten@ntnu.no> - 3.20-2
- Unzip by %%setup
- Simplify %%post/postun
- Added COPYING to handbook

* Sat Dec 29 2007 Terje Rosten <terje.rosten@ntnu.no> - 3.20-1
- 3.20
- include patch now upstream
- handbook patch now upstream

* Wed Dec 19 2007 Terje Rosten <terje.rosten@ntnu.no> - 3.20-0.1.rc2
- 3.20RC2
- disable openjpeg support
- icon and desktop file now upstream

* Sun Dec 16 2007 Terje Rosten <terje.rosten@ntnu.no> - 3.19-1
- upgrade to 3.19
- misc fixes to be rpmlint clean
- fix debuginfo package
- handle translations
- fix license
- compile with correct flags
- add patch to compile
- add handbook subpackage (and fix app to find docs)
- add xdg-open patch
- dont' use %%makeinstall
- add icon and mimetypes to desktop file

* Mon Apr 16 2007 Dries Verachtert <dries@ulyssis.org> - 3.11-1 - 5280/dries
- Updated to release 3.11.

* Sun Nov 12 2006 Dries Verachtert <dries@ulyssis.org> - 3.02-1
- Updated to release 3.02.

* Mon Aug 07 2006 Dries Verachtert <dries@ulyssis.org> - 3.01-1
- Updated to release 3.01.

* Wed May 31 2006 Dries Verachtert <dries@ulyssis.org> - 2.31-1
- Updated to release 2.31.

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 2.30-1.2
- Rebuild for Fedora Core 5.

* Wed Mar 01 2006 Dries Verachtert <dries@ulyssis.org> - 2.30-1
- Updated to release 2.30.

* Sun Jan 01 2006 Dries Verachtert <dries@ulyssis.org> - 2.20-1
- Updated to release 2.20.

* Mon Nov 21 2005 Dries Verachtert <dries@ulyssis.org> - 2.10-1
- Updated to release 2.10.

* Sat Sep 24 2005 Dries Verachtert <dries@ulyssis.org> - 2.03-1
- Updated to release 2.03.

* Tue Sep 20 2005 Dries Verachtert <dries@ulyssis.org> - 2.02-1
- Initial package.
