Name:           clementine
Version:        1.2.3
Release:        11%{?dist}
Summary:        A music player and library organizer

Group:          Applications/Multimedia
License:        GPLv3+ and GPLv2+
URL:            http://code.google.com/p/clementine-player
Source0:        http://clementine-player.googlecode.com/files/%{name}-%{version}.tar.gz

# fix libmygpo-qt header references
Patch0:         clementine-mygpo.patch
# desktop file fixes:
# * categories (+Audio)
# * non-compliant groups, https://code.google.com/p/clementine-player/issues/detail?id=2690
Patch3:         clementine-desktop.patch
Patch4:         clementine-udisks-headers.patch

# Use bundled sha2 library
# https://github.com/clementine-player/Clementine/issues/4217
Patch5:         clementine-do-not-use-system-sha2.patch
# fix compiler flag handling in gst/moodbar, upstreamable --rex
Patch6:         clementine-moodbar_flags.patch

BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  fftw-devel
BuildRequires:  gettext
BuildConflicts: gmock-devel >= 1.6
%if 0%{?fedora} && 0%{?fedora} < 20
BuildRequires:  gmock-devel
%endif
BuildRequires:  gstreamer-devel
BuildRequires:  gstreamer-plugins-base-devel
BuildRequires:  gtest-devel
BuildRequires:  libcdio-devel
BuildRequires:  libchromaprint-devel
BuildRequires:  libechonest-devel
%ifnarch s390 s390x
BuildRequires:  libgpod-devel
BuildRequires:  libimobiledevice-devel
%endif
BuildRequires:  liblastfm-devel
BuildRequires:  libmtp-devel
BuildRequires:  libmygpo-qt-devel
BuildRequires:  libnotify-devel
BuildRequires:  libplist-devel
BuildRequires:  libprojectM-devel >= 2.0.1-7
BuildRequires:  libqxt-devel
BuildRequires:  libxml2-devel
BuildRequires:  protobuf-devel
BuildRequires:  pkgconfig(qca2)
BuildRequires:  qt4-devel
BuildRequires:  qjson-devel
BuildRequires:  qtiocompressor-devel
BuildRequires:  qtsinglecoreapplication-devel
BuildRequires:  qtsingleapplication-devel >= 2.6.1-2
BuildRequires:  sha2-devel
BuildRequires:  sparsehash-devel
BuildRequires:  sqlite-devel
BuildRequires:  taglib-devel >= 1.8
BuildRequires:  libudisks2-devel
# %%check
BuildRequires:  dbus-x11
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  xorg-x11-xauth

Requires:       hicolor-icon-theme
Requires:       qca-ossl%{?_isa}

%description
Clementine is a multi-platform music player. It is inspired by Amarok 1.4,
focusing on a fast and easy-to-use interface for searching and playing your
music.

%prep
%setup -q
%patch0 -p1 -b .mygpo
%patch3 -p1 -b .desktop
%patch4 -p1 -b .udisks-headers
%patch5 -p1 -b .do-not-use-system-sha2
%patch6 -p1 -b .moodbar_flags

# Remove most 3rdparty libraries
mv 3rdparty/{gmock,qocoa,qsqlite,sha2}/ .
rm -fr 3rdparty/*
mv {gmock,qocoa,qsqlite,sha2}/ 3rdparty/

# Can't run all the unit tests
#   songloader requires internet connection
for test in songloader; do
    sed -i -e "/${test}_test/d" tests/CMakeLists.txt
done


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} \
  -DBUILD_WERROR:BOOL=OFF \
  -DCMAKE_BUILD_TYPE:STRING=Release \
  -DUSE_SYSTEM_QTSINGLEAPPLICATION=1 \
  -DUSE_SYSTEM_PROJECTM=1 \
  -DUSE_SYSTEM_QXT=1 \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install DESTDIR=%{buildroot} -C %{_target_platform}


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/clementine.desktop
pushd %{_target_platform}
# Run a fake X session since some tests check for X, tests still fail sometimes
xvfb-run -a dbus-launch --exit-with-session make test ||:
popd


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
  update-desktop-database &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%files
%doc Changelog COPYING
%{_bindir}/clementine
%{_bindir}/clementine-tagreader
%{_datadir}/applications/clementine.desktop
%{_datadir}/icons/hicolor/*/apps/application-x-clementine.*
%{_datadir}/kde4/services/clementine-feed.protocol
%{_datadir}/kde4/services/clementine-itms.protocol
%{_datadir}/kde4/services/clementine-itpc.protocol
%{_datadir}/kde4/services/clementine-zune.protocol

%changelog
* Wed Jul 15 2015 Jan Grulich <jgrulich@redhat.com> - 1.2.3-10
- Rebuild (qtsingleapplication, qtsinglecoreapplication)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Rex Dieter <rdieter@fedoraproject.org> 1.2.3-8
- fix gst/moodbar compiler flags, simplify qca2 build dep

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> - 1.2.3-7
- Rebuilt for protobuf soname bump

* Mon Apr 27 2015 Jan Grulich <jgrulich@redhat.com> - 1.2.3-6
- Rebuild for protobuf 2.6.1

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.2.3-5
- Rebuild for boost 1.57.0

* Tue Nov 18 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.3-4
- rebuild (libechonest)

* Wed Nov 12 2014 Adrian Reber <adrian@lisas.de> 1.2.3-3
- rebuild (libcdio)

* Wed Nov 05 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.3-2
- rebuild (libechonest)

* Mon Sep 22 2014 Jan Grulich <jgrulich@redhat.com> - 1.2.3-1
- 1.2.3

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 09 2014 Jan Grulich <jgrulich@redhat.com> - 1.2.1-4
- Do not generate namespace headers for udisks

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 1.2.1-2
- Rebuild for boost 1.55.0

* Fri Jan 03 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-1
- 1.2.1

* Tue Dec 17 2013 Adrian Reber <adrian@lisas.de> 1.1.1-10
- rebuild (libcdio)

* Wed Sep 04 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-9
- fix .desktop categories (+Audio)
- clementine - excessive debug output (#1001595)
- drop Requires: libtaginfo (not needed or used afaict)
- drop Requires: libprojectM, qtsingleapplication
- allow bundled gmock(1.5), not compat with 1.6 (yet)
- restore parallel builds

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 1.1.1-7
- Rebuild for boost 1.54.0

* Tue Jun 11 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-6
- BR: taglib-devel >= 1.8

* Wed May 29 2013 Luis Bazan <lbazan@fedoraproject.org> 1.1.1-5
- rebuild (libtaginfo)

* Wed May 22 2013 Rex Dieter <rdieter@fedoraproject.org> 1.1.1-4
- rebuild (libechonest)

* Tue Apr 23 2013 Tom Callaway <spot@fedoraproject.org> - 1.1.1-3
- fix compile against new libimobiledevice

* Wed Mar 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.1-2
- Rebuild for new libimobiledevice

* Sun Feb 24 2013 Orion Poplawski <orion@cora.nwra.com> - 1.1.1-1
- Update to 1.1.1
- Rebase desktop patch
- Drop system-sha2, fresh-start, fix-albumcoverfetch-crash, imobiledevice, and
  liblastfm1-compatibility patches fixed upstream
- Add mygpo patch to use system mygpo-qt library
- Use bundled qocoa library for now
- Add BR on fftw-devel and sparsehash-devel
- Drop BR on notification-daemon, not used and being dropped from Fedora

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 13 2013 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-15
- -DBUILD_WERROR=OFF

* Mon Jan 07 2013 Adrian Reber <adrian@lisas.de> 1.0.1-14
- rebuild (libcdio)

* Sat Nov 24 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-13
- rebuild (qjson)

* Sat Jul 28 2012 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> 1.0.1-12
- Rebuild on F-18 against new boost

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-11
- rebuild (libechonest)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-9
- Disable plasmarunner plugin as it was unstable. Upstream removed it from trunk

* Tue Jul 03 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-8
- liblastfm1 compatibility fix

* Tue Jul 03 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-7
- rebuild (liblastfm)

* Tue Jun 05 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-6
- Add Requires: qca-ossl RHBZ#826723

* Sat Apr 21 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-5
- Rebuild for new libimobiledevice and usbmuxd one more time on F-18

* Thu Apr 12 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.1-4
- Rebuild for new libimobiledevice and usbmuxd

* Sun Feb 26 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-3
- Fix a possible crash when an album cover search times out RHBZ#797451

* Tue Feb 07 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-2
- Re-add the fresh start patch. Looks like it didn't make it to 1.0.1
- Include plasma addon only in F-17+

* Thu Feb 02 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.0.1-1
- New upstream release RHBZ#772175

* Thu Jan 12 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-6
- Fix startup on a fresh install RHBZ#773547
- Some specfile clean-ups

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 10 2012 Rex Dieter <rdieter@fedoraproject.org> 0.7.1-4.1
- rebuild (libechonest)

* Tue Nov 29 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-4
- Lastfm login fix RHBZ#757280
- Patches for building against newer glibmm24 and glib2

* Mon Oct 10 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-3
- Rebuild for libechonest soname bump.

* Sat Jun 11 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-2
- Rebuild due to libmtp soname bump. Was this announced?

* Thu Mar 31 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7.1-1
- New upstream release
- Drop upstreamed patch

* Thu Mar 31 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7-2
- gcc-4.6 fix

* Wed Mar 30 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.7-1
- New upstream version
- Drop all upstreamed patches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6-2
- Rebuilt against new libimobiledevice on F-15

* Thu Dec 23 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.6-1
- New upstream version

* Thu Oct 14 2010 Dan Horák <dan[at]danny.cz> - 0.5.3-2
- Update BRs for s390(x)

* Wed Sep 29 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5.3-1
- New upstream version

* Sun Sep 26 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5.2-1
- New upstream version

* Wed Sep 22 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5.1-1
- New upstream version
- Drop all upstreamed patches

* Sun Aug 08 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-9
- Only create the OpenGL graphics context when you first open the visualisations
  window. Fixes RHBZ#621913

* Fri Aug 06 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-8
- Enforce Fedora compilation flags

* Thu Aug 05 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-7
- Fix crash on lastfm tree RHBZ#618474

* Tue Jul 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-6
- Rebuild against new boost on F-14

* Fri Jul 23 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-5
- Add missing scriptlets

* Wed Jul 21 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-4
- Use: make VERBOSE=1
- License is GPLv3+ and GPLv2+
- Put BRs in alphabetical order
- Remove redundant BRs: glew-devel, xine-lib-devel, and
  the extra libprojectM-devel
- Add R: hicolor-icon-theme

* Sun Jul 18 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-3
- Better qxt split patch

* Sat Jul 17 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-2
- Fix font paths issue, which caused a segfault on visualizations

* Sat Jul 17 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.4.2-1
- Version 0.4.2

* Fri May 07 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.3-1
- Version 0.3

* Sat Apr 17 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.2-2
- Patch out the external libraries
- Build the libclementine_lib into the final executable

* Sat Mar 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.2-1
- Fedorized the upstream specfile

* Mon Mar 22 2010 David Sansome <me@davidsansome.com> - 0.2
- Version 0.2

* Sun Feb 21 2010 David Sansome <me@davidsansome.com> - 0.1-5
- Various last-minute bugfixes

* Sun Jan 17 2010 David Sansome <me@davidsansome.com> - 0.1-1
- Initial package
