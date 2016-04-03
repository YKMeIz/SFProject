
Name:           kdenlive
Version:        0.9.10
Release:        1%{?dist}
Summary:        Non-linear video editor
License:        GPLv2+
URL:            http://www.kdenlive.org
Source0:        http://download.kde.org/stable/kdenlive/%{version}/src/kdenlive-%{version}.tar.bz2

BuildRequires:  desktop-file-utils 
BuildRequires:  gettext
BuildRequires:  kdelibs4-devel
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(mlt++) >= 0.8.8
%global mlt_version %(pkg-config --modversion mlt++ 2>/dev/null || echo 0.8.8)
BuildRequires:  pkgconfig(QJson)
BuildRequires:  pkgconfig(QtOpenGL) pkgconfig(QtScript)

Requires:       dvdauthor
Requires:       dvgrab
Requires:       ffmpeg
Requires:       kde-runtime%{?_kde4_version: >= %{_kde4_version}}
Requires:       mlt%{?_isa} >= %{mlt_version}
Requires:       recordmydesktop

%description
Kdenlive is an intuitive and powerful multi-track video editor, including most
recent video technologies.


%prep
%setup -q

# MLT's binary melt renamed at Fedora, so we must rename it in Kdenlive, too
sed -i 's|/bin/melt|/bin/mlt-melt|' src/mainwindow.cpp
sed -i 's|findExe("melt")|findExe("mlt-melt")|' src/mainwindow.cpp


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-kde


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/%{name}.desktop


%post
touch --no-create %{_kde4_iconsdir}/hicolor &>/dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_kde4_datadir}/icons/hicolor &>/dev/null || :
  touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
  update-desktop-database &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kde4_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_kde4_bindir}/*
%{_kde4_datadir}/applications/kde4/%{name}.desktop
%{_kde4_libdir}/kde4/*.so
%{_kde4_datadir}/config.kcfg/*
%{_kde4_configdir}/*
%{_kde4_datadir}/mime/packages/*
%{_kde4_appsdir}/%{name}/
%{_kde4_datadir}/kde4/services/westleypreview.desktop
# menu/pixmaps is deprecated/legacy stuff, could likely omit from packaging -- Rex
%{_kde4_datadir}/menu/%{name}
%{_kde4_datadir}/pixmaps/%{name}.xpm
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_mandir}/man1/*.gz


%changelog
* Mon Dec 22 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.10-1
- 0.9.10

* Wed Aug 06 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.8-2
- optimize mime scriptlets

* Wed May 14 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.8-1
- 0.9.8

* Mon Apr 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.9.6-4
- Rebuilt for rfbz#3209

* Wed Oct 09 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.6-3
- rebuilt for mlt

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.6-2
- Rebuilt for x264/FFmpeg

* Sun Apr 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.6-1
- 0.9.6

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.9.4-2
- Mass rebuilt for Fedora 19 Features

* Tue Jan 29 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.4-1
- 0.9.4

* Tue Jun 19 2012 Richard Shaw <hobbes1069@gmail.com> - 0.9.2-2
- Rebuild for updated mlt.

* Thu May 31 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Tue May 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9-1
- 0.9
- pkgconfig-style deps

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.2.1-3
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.8.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 10 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2.1-1
- 0.8.2.1

* Tue Nov 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-2
- rebuild

* Fri Nov 11 2011 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-1
- 0.8.2
- tighten mlt deps

* Thu Jul 21 2011 Ryan Rix <ry@n.rix.si> 0.8-1
- New version
- Add patch to fix FTBFS

* Fri Apr 15 2011 Rex Dieter <rdieter@fedoraproject.org> 0.7.8-2
- update scriptlets, %%_kde4_... macros/best-practices
- +Requires: kdebase-runtime (versioned)
- fix ftbfs

* Thu Apr 07 2011 Ryan Rix <ry@n.rix.si> - 0.7.8-1
- new version

* Mon Mar 01 2010 Zarko <zarko.pintar@gmail.com> - 0.7.7.1-1
- new version

* Thu Feb 18 2010 Zarko <zarko.pintar@gmail.com> - 0.7.7-1
- new version

* Mon Sep 07 2009 Zarko <zarko.pintar@gmail.com> - 0.7.5-1
- new version

* Sat May 30 2009 Zarko <zarko.pintar@gmail.com> - 0.7.4-2
- added updating of mime database
- changed dir of .desktop file

* Fri May 22 2009 Zarko <zarko.pintar@gmail.com> - 0.7.4-1
- new release
- spec cleaning

* Thu Apr 16 2009 Zarko <zarko.pintar@gmail.com> - 0.7.3-2
- some clearing
- added doc files

* Wed Apr 15 2009 Zarko <zarko.pintar@gmail.com> - 0.7.3-1
- new release

* Sun Apr 12 2009 Zarko <zarko.pintar@gmail.com> - 0.7.2.1-2
- spec convert to kde4 macros

* Mon Mar 16 2009 Zarko <zarko.pintar@gmail.com> - 0.7.2.1-1
- update to 0.7.2.1
- spec cleaned
- Resolve RPATHs

* Sun Nov 16 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.7-1
- update to 0.7

* Wed Nov  5 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.7-0.1.20081104svn2622
- update to last svn revision

* Tue Nov  4 2008 Arkady L. Shane <ashejn@yandex-team.ru> - 0.7-0.beta1
- clean up spec

* Fri Oct 17 2008 jeff <moe@blagblagblag.org> - 0.7-1.beta1
- Add URL
- Full URL for Source:
- Remove all Requires:
- Update BuildRoot
- Remove Packager: Brixton Linux Action Group
- Add BuildRequires: ffmpeg-devel kdebindings-devel soprano-devel
- Update %%files
- %%doc with only effects/README
- GPLv2+
- Add lang files

* Tue Jul  8 2008 jeff <moe@blagblagblag.org> - 0.6-1.svn2298.0blag.f9
- Update to KDE4 branch
  https://kdenlive.svn.sourceforge.net/svnroot/kdenlive/branches/KDE4

* Tue Jul  8 2008 jeff <moe@blagblagblag.org> - 0.6-1.svn2298.0blag.f9
- Update to svn r2298
- New Requires
- kdenlive-svn-r2298-renderer-CMakeLists.patch 

* Sun Nov 11 2007 jeff <moe@blagblagblag.org> - 0.5-1blag.f7
- Update to 0.5 final

* Tue Apr 17 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070417.0blag.fc6
- svn to 20070417

* Fri Apr  6 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070406.0blag.fc6
- svn to 20070406

* Tue Apr  3 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070403.0blag.fc6
- svn to 20070403

* Thu Mar 22 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070322.0blag.fc6
- svn to 20070322

* Thu Mar 15 2007 jeff <moe@blagblagblag.org> - 0.5-0svn20070316.0blag.fc6
- BLAG'd

* Sun Apr 27 2003 Jason Wood <jasonwood@blueyonder.co.uk> 0.2.2-1mdk
- First stab at an RPM package.
- This is taken from kdenlive-0.2.2 source package.
