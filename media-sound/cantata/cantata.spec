## define build type, uses Qt4 if neither kde or qt5 is defined
%global kde 1
#global qt5 1
#global qt4 1

%if 0%{?fedora} > 17 || 0%{?rhel} > 6
%global udisks2 1
%endif

Name:    cantata
Summary: Music Player Daemon (MPD) graphical client
Version: 1.4.1
Release: 1%{?dist}

License: GPLv2+
URL:     http://code.google.com/p/cantata/
# https://code.google.com/p/cantata/wiki/Downloads
Source0: cantata-%{version}.tar.bz2

## upstreamable patches
# could be made upstreamable with a little more work -- rex
Patch101: cantata-1.4.1-system-qtiocompressor.patch
Patch102: cantata-1.4.1-system-qxt.patch
# fix kde support (kde4_includes)
Patch103: cantata-1.3.3-kde4_includes.patch
# make libsolidlite explicitly static
Patch104: cantata-1.3.4-libsolid_static.patch
# avoid/fix crashes in icons.cpp
Patch105: cantata-1.4.1-icons_crash.patch

BuildRequires: cdparanoia-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: gettext
%if 0%{?kde}
BuildRequires: kdelibs4-devel >= 4.7
%endif
%if 0%{?qt4} || 0%{?kde}
BuildRequires: libqxt-devel
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(QJson)
BuildRequires: pkgconfig(QtDBus) pkgconfig(QtGui) pkgconfig(QtNetwork) pkgconfig(QtXml)
BuildRequires: pkgconfig(QtWebKit)
BuildRequires: qtiocompressor-devel
BuildRequires: qtsingleapplication-devel
%endif
%if 0%{?qt5}
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: pkgconfig(Qt5DBus) pkgconfig(Qt5Gui) pkgconfig(Qt5Network) pkgconfig(Qt5Xml)
BuildRequires: pkgconfig(Qt5WebKit)
%endif
BuildRequires: media-player-info
BuildRequires: pkgconfig(libcddb)
BuildRequires: pkgconfig(libmtp)
BuildRequires: pkgconfig(libmusicbrainz5)
BuildRequires: pkgconfig(phonon)
BuildRequires: pkgconfig(taglib)
BuildRequires: pkgconfig(taglib-extras)
BuildRequires: systemd-devel

Requires: media-player-info
%if 0%{?kde}
# http://bugzilla.redhat.com/1134333
Requires: oxygen-icon-theme 
%endif



%description
Cantata is a graphical client for the music player daemon (MPD).

Features:
* Multiple MPD collections.
* Highly customisable layout.
* Songs grouped by album in play queue.
* Context view to show artist, album, and song information of current track.
* Simple tag editor.
* File organizer - use tags to organize files and folders.
* Ability to calculate ReplyGain tags.
* Dynamic playlists.
* Online services; Jamendo, Magnatune, SoundCloud, and Podcasts.
* Radio stream support - with the ability to search for streams via TuneIn
and ShoutCast.
* USB-Mass-Storage and MTP device support.
* Audio CD ripping and playback.
* Playback of non-MPD songs, via simple in-built HTTP server.
* MPRISv2 DBUS interface.
* Support for KDE global shortcuts (KDE builds), GNOME media keys, and generic
media keys (via Qxt support)
* Ubuntu/ambiance theme integration.


%prep
%setup -q
# No qt5 qjson,qtiocompressor... yet
%if ! 0%{?qt5}
%patch101 -p1 -b .system-qtiocompressor
rm -rfv 3rdparty/{qjson,qtiocompressor}/
sed -i.system-qtiocompressor-headers -e 's|^#include "qtiocompressor/qtiocompressor.h"|#include <QtIOCompressor>|g' \
  context/albumview.cpp \
  context/artistview.cpp \
  context/songview.cpp \
  context/wikipediasettings.cpp \
  models/dirviewmodel.cpp \
  models/musiclibrarymodel.cpp \
  models/musiclibraryitempodcast.cpp \
  models/musiclibraryitemroot.cpp \
  models/streamsmodel.cpp \
  online/onlineservice.cpp \
  scrobbling/scrobbler.cpp \
  streams/tar.cpp 
%endif
%patch102 -p1 -b .system-qxt
rm -rfv 3rdparty/{qtsingleapplication,qxt}/
sed -i.system-qxt-headers -e 's|^#include "qxt/qxtglobalshortcut.h"|#include <QxtGlobalShortcut>|g' \
  gui/qxtmediakeys.cpp
%patch103 -p1 -b .kde4_includes
%patch104 -p1 -b .libsolid_static
%patch105 -p1 -b .icons_crash


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
PATH="%{_qt4_bindir}:$PATH" ; export PATH ;
CXXFLAGS="%{optflags} -I/usr/include/QtSolutions" # see bug 1077936
%{cmake} \
  -DENABLE_KDE:BOOL=%{?kde:ON}%{!?kde:OFF} \
  -DENABLE_QT5:BOOL=%{?qt5:ON}%{!?qt5:OFF} \
  -DENABLE_FFMPEG:BOOL=OFF \
  -DENABLE_MPG123:BOOL=OFF \
  %{?udisks2:-DENABLE_UDISKS2:BOOL=ON} \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-qt --with-kde --all-name


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{?kde:kde4/}cantata.desktop 


%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%files -f %{name}.lang
%doc AUTHORS ChangeLog LICENSE README TODO
%{_bindir}/cantata
# libexecdir type stuff
%{_prefix}/lib/cantata/
%{_datadir}/applications/%{?kde:kde4/}cantata.desktop
%{_datadir}/icons/hicolor/*/*/*
%dir %{_datadir}/cantata/
%{_datadir}/cantata/config
%{_datadir}/cantata/icons/
%{_datadir}/cantata/mpd/
%{_datadir}/cantata/scripts/
%{_datadir}/cantata/themes/
%if 0%{?kde}
%dir %{_kde4_appsdir}/solid/
%dir %{_kde4_appsdir}/solid/actions/
%{_kde4_appsdir}/solid/actions/cantata-play-audiocd.desktop
%else
%dir %{_datadir}/cantata/translations/
%endif


%changelog
* Wed Aug 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.4.1-1
- cantata-1.4.1 (#1082278)
- missing dependency oxygen theme (#1134333)
- re-enable kde build

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 09 2014 Rex Dieter <rdieter@fedoraproject.org> 1.3.4-2
- make libsolidlite convenience lib explicitly static

* Sat Jun 07 2014 Rex Dieter <rdieter@fedoraproject.org> - 1.3.4-1
- cantata-1.3.4
- disable kde integration (for now, FTBFS)
- revert whitespace changes
- restore cmake types for build options
- use system libqxt
- ready Qt5-enabled build (not used yet)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-2
- Use system qtiocompressor instead of bundled one

* Mon Jan 06 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.2-1
- cantata-1.2.2 (#1048750)

* Thu Dec 26 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-1
- cantata-1.2.1 (#1034054)

* Tue Dec 17 2013 Rex Dieter <rdieter@fedoraproject.org> 1.2.0-1
- cantata-1.2.0

* Tue Dec 17 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.3-1
- cantata-1.1.3 

* Wed Aug 14 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-1
- cantata-1.1.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.9.2-2
- Perl 5.18 rebuild

* Mon Jan 28 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2

* Sat Jan 05 2013 Rex Dieter <rdieter@fedoraproject.org> 0.9.1-1
- cantata-0.9.1

* Wed Nov 28 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.3.1-2
- patch s|^#!/usr/bin/env perl|#!/usr/bin/perl|

* Tue Sep 25 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.3.1-1
- cantata-0.8.3.1
- run desktop-file-validate
- add icon scriptlets
- drop Requires: mpd
- %%doc LICENSE AUTHORS ChangeLog README TODO
- omit and explicitly disable ffmpeg, mpg123 support

* Thu Aug 02 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.2-1
- first try

