%global _hardened_build 1

Summary: Frozen Bubble arcade game
Name: frozen-bubble
Version: 2.2.1
Release: 0.10.beta1%{?dist}
License: GPLv2
Group: Amusements/Games
URL: http://www.frozen-bubble.org/
Source0: http://www.frozen-bubble.org/data/frozen-bubble-%{version}-beta1.tar.bz2
Source1: frozen-bubble.desktop
Source2: fb-server.service
Patch0:  frozen-bubble-2.2.1-setuid.patch
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: glib2-devel
BuildRequires: perl(Alien::SDL) >= 1.413
BuildRequires: perl(autodie)
BuildRequires: perl(ExtUtils::CBuilder)
BuildRequires: perl(File::Slurp)
BuildRequires: perl(File::Spec::Functions)
BuildRequires: perl(IO::File)
BuildRequires: perl(IPC::System::Simple)
BuildRequires: perl(lib)
BuildRequires: perl(Locale::Maketext::Extract)
BuildRequires: perl(Module::Build) >= 0.36
BuildRequires: perl(parent)
BuildRequires: perl(SDL) >= 2.511
BuildRequires: perl(Test::More)
BuildRequires: SDL_mixer-devel
BuildRequires: SDL_Pango-devel
Requires:      perl(SDL) >= 2.511
Requires:      perl(Alien::SDL) >= 1.413
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:      hicolor-icon-theme

%{?perl_default_filter}

%description
Full-featured, colorful animated penguin eye-candy, 100 levels of 1p game, hours
and hours of 2p game, 3 professional quality 20-channels musics, 15 stereo
sound effects, 7 unique graphical transition effects and a level editor.
You need this game.


%package server
Summary: Frozen Bubble network game dedicated server
Group: System Environment/Daemons
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description server
Frozen Bubble network game dedicated server. The server is already included
with the game in order to be launched automatically for LAN games, so you
only need to install this package if you want to run a fully dedicated
Frozen Bubble network game server.


%prep
%setup -q -n %{name}-%{version}-beta1
%patch0 -p1
# Rename this README since the main server README has the same name
%{__mv} server/init/README server/README.init
# Change the example server configuration file to be a working one, which only
# launches a LAN server and doesn't try to register itself on the Internet
%{__sed} -ie "s#^a .*#z\nq\nL#" server/init/fb-server.conf


%build
export LDFLAGS="%{?__global_ldflags}"
export CFLAGS="$RPM_OPT_FLAGS"
%{__perl} Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
sed -i "s|'-Wl,-rpath,/usr/.*',||" _build/build_params
./Build


%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
#%%find_lang %%{name}

# Clean up unneeded files
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

# Desktop file
%{__mkdir_p} %{buildroot}%{_datadir}/applications
desktop-file-install \
    --dir %{buildroot}%{_datadir}/applications \
    %{SOURCE1}

# Icons
%{__install} -D -p -m 0644 share/icons/frozen-bubble-icon-16x16.png \
    %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{__install} -D -p -m 0644 share/icons/frozen-bubble-icon-32x32.png \
    %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{__install} -D -p -m 0644 share/icons/frozen-bubble-icon-48x48.png \
    %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{__install} -D -p -m 0644 share/icons/frozen-bubble-icon-64x64.png \
    %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

# Install server init script and default configuration
%{__install} -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_unitdir}/fb-server.service
%{__install} -D -p -m 0644 server/init/fb-server.conf \
    %{buildroot}%{_sysconfdir}/fb-server.conf


%check
./Build test


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post server
/usr/sbin/useradd -r -s /sbin/nologin -d %{_datadir}/%{name} fbubble \
    &>/dev/null || :
%systemd_post fb-server.service

%preun server
%systemd_preun fb-server.service

%postun server
%systemd_postun_with_restart fb-server.service


%files
%doc AUTHORS COPYING Changes HISTORY README
%{_bindir}/%{name}*
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Games/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man[13]/*

%files server
%doc COPYING server/AUTHORS server/README*
%config(noreplace) %{_sysconfdir}/fb-server.conf
%{_unitdir}/fb-server.service
%{_bindir}/fb-server


%changelog
* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.2.1-0.10.beta1
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-0.9.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-0.8.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-0.7.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 2.2.1-0.6.beta1
- Perl 5.18 rebuild

* Fri May 17 2013 Hans de Goede <hdegoede@redhat.com> - 2.2.1-0.5.beta1
- Fix hardened build (rhbz#955273)
- Remove rpath

* Wed Mar  6 2013 Hans de Goede <hdegoede@redhat.com> - 2.2.1-0.4.beta1
- Fix FTBFS (rhbz#914013)
- Use new systemd macros for scripts (rhbz#850120)
- Drop sysv -> systemd conversion scripts

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-0.3.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.2.1-0.1.beta1
- Updated to 2.2.1-beta1

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.2.0-13
- Perl 5.16 rebuild

* Fri Apr 13 2012 Jon Ciesla <limburgher@gmail.com> - 2.2.0-12
- Add hardened build.

* Wed Mar 14 2012 Jon Ciesla <limburgher@gmail.com> - 2.2.0-11
- Migrate to systemd, BZ 767621.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.2.0-9
- Perl mass rebuild
- change perl-SDL to correct perl(SDL)

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.2.0-8
- Perl 5.14 mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.2.0-6
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.2.0-5
- rebuild against perl 5.10.1

* Tue Dec  1 2009 Hans de Goede <hdegoede@redhat.com> 2.2.0-4
- Do not remove server user (#542423), per:
  http://fedoraproject.org/wiki/Packaging/UsersAndGroups

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 26 2009 Nils Philippsen <nils@redhat.com> 2.2.0-1
- Update to 2.2.0 (#479431)

* Sun Jul  6 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 2.1.0-9
- Fix audio on bigendian archs (bz 454109), patch by Ian Chapman

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.0-8
- rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.0-7
- Autorebuild for GCC 4.3

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.0-6
- rebuild for new perl

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 2.1.0-5
- Rebuild for new BuildID feature.

* Sun Aug  5 2007 Matthias Saou <http://freshrpms.net/> 2.1.0-4
- Update License field.

* Fri Jun 22 2007 Matthias Saou <http://freshrpms.net/> 2.1.0-3
- Fix build with perl-devel split (ExtUtils/MakeMaker.pm build requirement).
- Cosmetic changes to the spec file.
- Change fbubble user's home from / to %%{_datadir}/%%{name}.
- Remove the desktop file's "fedora" prefix.
- Remove executable bit from the man pages.

* Wed Nov 29 2006 Matthias Saou <http://freshrpms.net/> 2.1.0-2
- Silence useradd call so there is no output upon update (#217902).

* Wed Nov 29 2006 Matthias Saou <http://freshrpms.net/> 2.1.0-1
- Update to 2.1.0 (fixes #216248).

* Fri Oct 27 2006 Matthias Saou <http://freshrpms.net/> 2.0.0-1
- Update to 2.0.0.
- Add new SDL_Pango dependency.
- New server standalone sub-package for the dedicated server.

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.0-10
- FE6 Rebuild

* Wed Aug 23 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.0-9
- Filter out the autogenerated Provides for our private perl modules and also
  filter out the matching AutoRequires to still get an installable package

* Sun Aug 20 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.0-8
- Apply patch from Wart (wart@kobold.org) to move private perl stuff to
  %%{_libdir}/%%{_name}
- Drop unnescesarry perl BR (already implied by perl-SDL).
- Fix inconsistent use of $RPM_BUILD_ROOT vs ${RPM_BUILD_ROOT} (only use the
  former)

* Tue Aug 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.0-7
- Update to work with new perl-SDL-2.1.3 see BZ 202437

* Mon Aug 14 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.0.0-6
- Submit to Fedora Extras since perl-SDL is in FE now, so frozen-bubble can
  move to FE too
- Cleanup BR's a bit to match FE-guidelines
- Install all sizes icons into /usr/share/icons, instead of just the biggest
  one into /usr/share/pixmaps
- Add scriptlets to update icon cache

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Tue Nov 16 2004 Thorsten Leemmhuis <fedora [AT] leemhuis [DOT] info> - 0:1.0.0-0.lvn.5
- Update to new Debian patch

* Sat Jul  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0.0-0.lvn.4
- Apply patch from Debian to make fb work with perl-SDL >= 1.20.3.
- Install Perl modules into vendor install dirs, require (:MODULE_COMPAT_*).
- Fix Source0 URL.
- Remove unneeded files.
- Fix file permissions.
- s/fedora/livna/ in desktop entry, other small improvements.

* Fri Jun 27 2003 Phillip Compton <pcompton at proteinmedia dot com> 0:1.0.0-0.fdr.3
- Removed BuildConflicts.
- Added Epochs to BuildReqs.
- Split Desktop entry into seperate file.

* Sun Jun 22 2003 Phillip Compton <pcompton at proteinmedia dot com> 0:1.0.0-0.fdr.2
- Fixed file permissions.
- Added in suggested fixes from Adrian Reber.

* Tue May 27 2003 Phillip Compton <pcompton at proteinmedia dot com> 0:1.0.0-0.fdr.1
- Fedorafied.

* Tue Apr  1 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Replace the __find_requires with AutoReq: as it works better.
- Remove .xvpics from installed files.

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.

* Tue Feb 18 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Added missing man pages, thanke to Michal Ambroz.

* Mon Feb 17 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.0.0.

* Mon Oct 28 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 8.0 (at last!).
- New menu entry.

* Thu Feb  7 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 0.9.3.

* Thu Feb  7 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Spec file modifications for a Red Hat Linux release.

* Wed Feb  6 2002 Guillaume Cottenceau <gc@mandrakesoft.com> 0.9.1-1mdk
- first mdk rpm

