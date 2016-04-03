%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name: devede
Version: 3.23.0
Release: 3%{?dist}
Summary: A program to create video DVDs and CDs (VCD, sVCD or CVD)

License: GPLv3+
URL: http://www.rastersoft.com/programas/devede.html
Source0: http://www.rastersoft.com/descargas/%{name}-%{version}.tar.bz2
# Enable AC3_fix by default
Patch0: %{name}-3.23.0-ac3.patch

BuildArch: noarch

BuildRequires: python >= 2.4
BuildRequires: gettext
BuildRequires: desktop-file-utils
Requires: mplayer
Requires: mencoder
Requires: ffmpeg
Requires: dvdauthor
Requires: vcdimager
Requires: mkisofs
Requires: brasero
Requires: ImageMagick
Requires: python >= 2.4
Requires: pygtk2 >= 2.16
Requires: pygtk2-libglade
Requires: dejavu-sans-fonts
Requires: hicolor-icon-theme


%description
DeVeDe is a program to create video DVDs and CDs (VCD, sVCD or CVD) 
suitable for home players, from any number of video files, in any 
of the formats supported by Mplayer. The big advantage over other 
utilities is that it only needs Mplayer, Mencoder, DVDAuthor, VCDImager 
and MKisofs (well, and Python 2.4, PyGTK and PyGlade), so its 
dependencies are really small.


%prep
%setup -q
%patch0 -p1

# Fix module directory
sed -i 's!/usr/lib/!%{_datadir}/!' devede

# Fix help directory
sed -i 's!/usr/share/doc/devede!%{_pkgdocdir}!' devede

# Remove backup files
find . -name *\~ -exec rm {} \;


%build


%install
rm -rf $RPM_BUILD_ROOT

./install.sh \
  --uninstall=no \
  --targeted=yes \
  --DESTDIR=$RPM_BUILD_ROOT \
  --prefix=%{_prefix} \
  --libdir=%{_datadir} \
  --pkgdocdir=%{_pkgdocdir}

# remove debian files from doc
rm $RPM_BUILD_ROOT%{_pkgdocdir}/{copyright,changelog.Debian}

# replace devedesans.ttf with a symlink to DejaVuSans.ttf
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/devedesans.ttf
ln -s %{_datadir}/fonts/dejavu/DejaVuSans.ttf $RPM_BUILD_ROOT%{_datadir}/%{name}/devedesans.ttf

# rename .desktop file 
desktop-file-install \
  --delete-original \
  --add-category X-OutputGeneration \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

# move icon into %%{_datadir}/icons/hicolor/
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mv $RPM_BUILD_ROOT%{_datadir}/pixmaps/%{name}.svg \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/

%find_lang %{name}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%{_bindir}/%{name}
%{_bindir}/%{name}_debug
%{_bindir}/%{name}-debug
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%doc %{_pkgdocdir}


%changelog
* Tue Aug 13 2013 Andrea Musuruane <musuruan@gmail.com> 3.23.0-3
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Dropped desktop vendor tag
- Used unversioned docdir
- Fixed date in changelog

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.23.0-2
- Rebuilt for x264/FFmpeg

* Sun Oct 28 2012 Andrea Musuruane <musuruan@gmail.com> 3.23.0-1
- Updated to version 3.23.0

* Sun May 27 2012 Andrea Musuruane <musuruan@gmail.com> 3.22.0-1
- Updated to version 3.22.0
- Moved icon in %%{_datadir}/icons/hicolor

* Sat Dec 31 2011 Andrea Musuruane <musuruan@gmail.com> 3.21.0-1
- Updated to version 3.21.0

* Fri Dec 09 2011 Andrea Musuruane <musuruan@gmail.com> 3.20.0-1
- Updated to version 3.20.0
- Added missing brasero dependency

* Sun Nov 27 2011 Andrea Musuruane <musuruan@gmail.com> 3.19.0-1
- Updated to version 3.19.0

* Sat Nov 26 2011 Andrea Musuruane <musuruan@gmail.com> 3.18.0-1
- Updated to version 3.18.0

* Sat Jul 16 2011 Andrea Musuruane <musuruan@gmail.com> 3.17.0-1
- Updated to version 3.17.0

* Sat Jun 04 2011 Andrea Musuruane <musuruan@gmail.com> 3.16.9-2
- Added a patch to use the ac3_fixed codec in new mencoder

* Sat Jul 03 2010 Andrea Musuruane <musuruan@gmail.com> 3.16.9-1
- Updated to version 3.16.9
- Fixed help directory

* Mon Apr 19 2010 Andrea Musuruane <musuruan@gmail.com> 3.16.8-1
- Updated to version 3.16.8

* Sun Apr 18 2010 Andrea Musuruane <musuruan@gmail.com> 3.16.7-1
- Updated to version 3.16.7

* Sat Mar 20 2010 Andrea Musuruane <musuruan@gmail.com> 3.16.6-1
- Updated to version 3.16.6

* Sat Mar 13 2010 Andrea Musuruane <musuruan@gmail.com> 3.16.5-1
- Updated to version 3.16.5

* Thu Feb 25 2010 Andrea Musuruane <musuruan@gmail.com> 3.16.4-1
- Updated to version 3.16.4

* Sun Feb 21 2010 Andrea Musuruane <musuruan@gmail.com> 3.16.2-1
- Updated to version 3.16.2
- Fixed description

* Sat Feb 13 2010 Andrea Musuruane <musuruan@gmail.com> 3.16.0-1
- Updated to version 3.16.0

* Wed Dec 02 2009 Andrea Musuruane <musuruan@gmail.com> 3.15.2-1
- Updated to version 3.15.2
- Updated desktop file categories as required by Fedora Studio

* Sun Nov 29 2009 Andrea Musuruane <musuruan@gmail.com> 3.15.0-1
- Updated to version 3.15
- Now it requires gtk >= 2.16
- Updated icon cache scriptlets

* Sat Oct 31 2009 Andrea Musuruane <musuruan@gmail.com> 3.12c-4
- Fixed font Requires on Fedora 11 and higher (BZ #891)
- Fixed Summary

* Mon Apr 06 2009 Andrea Musuruane <musuruan@gmail.com> 3.12c-3
- Fixed greek translation (BZ #494)

* Sat Mar 28 2009 Andrea Musuruane <musuruan@gmail.com> 3.12c-2
- Fix font Requires: dejavu-fonts-compat

* Wed Jan 28 2009 Andrea Musuruane <musuruan@gmail.com> 3.12c-1
- Updated to version 3.12c

* Sun Jan 25 2009 Andrea Musuruane <musuruan@gmail.com> 3.12-1
- Updated to version 3.12

* Wed Jan 14 2009 Andrea Musuruane <musuruan@gmail.com> 3.11b-4
- Used DejaVuSans.ttf instead of devedesans.ttf
- Changed libdir to %%{_datadir} like other python packages
- Improved macro usage

* Sat Dec 20 2008 Andrea Musuruane <musuruan@gmail.com> 3.11b-3
- Rebuilt for python 2.6

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.11b-2
- rebuilt

* Wed Aug 27 2008 Andrea Musuruane <musuruan@gmail.com> 3.11b-1
- Updated to version 3.11b.

* Mon Aug 25 2008 Andrea Musuruane <musuruan@gmail.com> 3.11-1
- Updated to version 3.11.

* Tue Aug 19 2008 Andrea Musuruane <musuruan@gmail.com> 3.10-1
- Updated to version 3.10.

* Sat Jun 28 2008 Andrea Musuruane <musuruan@gmail.com> 3.9-1
- Updated to version 3.9.

* Mon May 26 2008 Andrea Musuruane <musuruan@gmail.com> 3.8c-1
- Updated to version 3.8c.

* Sat Apr 19 2008 Andrea Musuruane <musuruan@gmail.com> 3.7-1
- Updated to version 3.7.

* Wed Dec 12 2007 Andrea Musuruane <musuruan@gmail.com> 3.6-1
- Updated to version 3.6.

* Sun Dec 9 2007 Andrea Musuruane <musuruan@gmail.com> 3.5-1
- Updated to version 3.5.

* Sat Nov 24 2007 Andrea Musuruane <musuruan@gmail.com> 3.4-1
- Updated to version 3.4.

* Fri Oct 26 2007 Andrea Musuruane <musuruan@gmail.com> 3.3-1
- Updated to version 3.3.

* Tue Sep 18 2007 Andrea Musuruane <musuruan@gmail.com> 3.2-1
- Updated to version 3.2.
- License changed to GPLv3 or later.
- Updated icon cache scriptlets to be compliant to new guidelines.

* Sat Aug 25 2007 Andrea Musuruane <musuruan@gmail.com> 3.01-3
- Changed license due to new guidelines.

* Sun Jul 08 2007 Andrea Musuruane <musuruan@gmail.com> 3.01-2
- Removed %%{?dist} tag from changelog.

* Sat Jul 07 2007 Andrea Musuruane <musuruan@gmail.com> 3.01-1
- Updated to version 3.01.
- Cosmetical changes.

* Sun Jun 24 2007 Andrea Musuruane <musuruan@gmail.com> 3.0-1
- Updated to version 3.0.
- Updated icon cache scriptlets to be compliant to new guidelines.
- Minor fixes to desktop file.

* Fri Apr 20 2007 Andrea Musuruane <musuruan@gmail.com> 2.13-1
- Updated to version 2.13.

* Thu Mar 01 2007 Andrea Musuruane <musuruan@gmail.com> 2.12-1
- First release for Livna.

