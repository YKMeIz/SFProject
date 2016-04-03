Name:           tremulous
Version:        1.2.0
Release:        0.12.beta1%{?dist}
Summary:        First Person Shooter game based on the Quake 3 engine
Group:          Amusements/Games
License:        GPLv2+
URL:            http://tremulous.net
# To get the source tarball:
# svn export svn://svn.icculus.org/tremulous/tags/RELEASE_GPP1/ tremulous-1.2.beta1
# rm -rf tremulous-1.2.beta1/src/tools/lcc/
# tar -czf tremulous-1.2.0.beta1.tar.gz tremulous-1.2.beta1
Source0:        tremulous-1.2.0.beta1.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}.png
Patch0:         tremulous-1.2.0-dll-overwrite.patch
Patch1:         tremulous-getstatus-dos.patch
Patch2:         tremulous-aarch64.patch
BuildRequires:  desktop-file-utils SDL-devel openal-soft-devel libvorbis-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libcurl-devel
BuildRequires:  zlib-devel
BuildRequires:  speex-devel
Requires:       tremulous-data = %{version}
Requires:       hicolor-icon-theme opengl-games-utils

%description
Tremulous is a free, open source game that blends a team based FPS with elements
of an RTS. Players can choose from 2 unique races, aliens and humans. 
Players on both teams are able to build working structures in-game like an RTS.
These structures provide many functions, the most important being spawning.
The designated builders must ensure there are spawn structures or other players
 will not be able to rejoin the game after death. Other structures provide 
automated base defense (to some degree), healing functions and much more...

Player advancement is different depending on which team you are on.
As a human, players are rewarded with credits for each alien kill.
These credits may be used to purchase new weapons and upgrades from the Armoury
The alien team advances quite differently. Upon killing a human foe,
the alien is able to evolve into a new class. The more kills gained the more 
powerful the classes available.

The overall objective behind Tremulous is to eliminate the opposing team.
This is achieved by not only killing the opposing players but also 
removing their ability to respawn by destroying their spawn structures.

%prep
%setup -q -n tremulous-1.2.beta1
%patch0 -p1 -b .dll-overwrite
%patch1 -p1 -b .getstatus-dos
%patch2 -p1 -b .aarch64

# Rip out the bundled libraries and use the
# system versions instead
rm -r src/SDL12 src/AL src/libcurl src/libspeex src/libs

%build
# the CROSS_COMPILING=1 is a hack to not build q3cc and qvm files
# since we've stripped out q3cc as this is not Free Software.
make %{?_smp_mflags} \
    OPTIMIZE="$RPM_OPT_FLAGS -fno-strict-aliasing -ffast-math" \
    DEFAULT_BASEDIR=%{_datadir}/%{name} USE_CODEC_VORBIS=1 \
    USE_LOCAL_HEADERS=0 BUILD_GAME_SO=0 GENERATE_DEPENDENCIES=0 \
    CROSS_COMPILING=1 USE_INTERNAL_SPEEX=0 USE_INTERNAL_ZLIB=0

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 build/release-linux-*/tremded.* \
  $RPM_BUILD_ROOT%{_bindir}/tremded
install -m 0755 build/release-linux-*/tremulous.* \
  $RPM_BUILD_ROOT%{_bindir}/%{name}
ln -s opengl-game-wrapper.sh $RPM_BUILD_ROOT%{_bindir}/%{name}-wrapper

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install            \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
install -p -m 644 %{SOURCE2} \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps

%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files
%doc ChangeLog COPYING GPL
%{_bindir}/%{name}*
%{_bindir}/tremded
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png

%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.12.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-0.11.beta1
- Add patch for aarch64 support

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.10.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.9.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.8.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 14 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-0.7.beta1
- Remove vendor tag from desktop file
- spec clean up

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.6.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Jan Kaluza <jkaluza@redhat.com> - 1.2.0-0.5.beta1
- fix #806980 - fixed CVE-2010-5077

* Thu Feb 23 2012 Jan Kaluza <jkaluza@redhat.com> - 1.2.0-0.4.beta1
- fix #796362 - fixed CVE-2011-2764 and CVE-2011-3012

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.3.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 17 2010 Jan Kaluza <jkaluza@redhat.com> - 1.2.0-0.1.beta1
- update to 1.2.0 beta
- fix #602374 - tremulous works on x86_64 now

* Sun Aug 16 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.1.0-10
- Switch to openal-soft

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.1.0-7
- Fix Patch0:/%%patch mismatch.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-6
- Autorebuild for GCC 4.3

* Wed Sep 26 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-5
- Update syslibs patch to make the system libjpeg use tremulous' Malloc and
  Free functions, instead of the libc ones

* Mon Sep 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-4
- Use opengl-games-utils wrapper to show error dialog when DRI is missing

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-3
- Update License tag for new Licensing Guidelines compliance

* Mon Sep  4 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-2
- Various small packaging improvements (see bug 204121)

* Fri Aug 25 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-1
- Initial Fedora packaging (based on work from Matthias and Wart)
