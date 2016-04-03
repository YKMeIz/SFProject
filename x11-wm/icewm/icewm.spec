Name:		icewm
Version:	1.3.8
Release:	4%{?dist}
Summary:	Light and configurable window manager
Group:		User Interface/Desktops
License:	LGPLv2+
URL:		http://www.icewm.org
Source0:	http://heanet.dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:	http://lostclus.linux.kiev.ua/scripts/icewm-xdg-menu
Source2:	icewm.desktop
Source3:	icewm-startup
Source4:	clearlooks-v3.tgz

BuildRequires:	giflib-devel
BuildRequires:	libXinerama-devel
BuildRequires:	imlib-devel
BuildRequires:	xorg-x11-proto-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libXft-devel
BuildRequires:	libICE-devel
BuildRequires:	gettext
BuildRequires:	gnome-desktop-devel
BuildRequires:	fribidi-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	popt-devel
BuildRequires:	autoconf
BuildRequires:	automake

Requires:	gnome-icon-theme
Requires:	alsa-utils
Requires:	xdg-utils
Requires:	xterm

Patch1:		icewm-1.3.8-menu.patch
Patch2:		icewm-toolbar.patch
Patch3:		icewm-keys.patch
Patch4:		icewm-1.3.8-fribidi.patch
Patch5:		icewm-1.3.7-dso.patch
Patch6:		icewm-defaults.patch
Patch7:		icewm-1.3.7-menuiconsize.patch
Patch8:		icewm-1.3.8-deprecated.patch


%description
IceWM is a window manager for the X Window System (freedesktop, XFree86).
The goal of IceWM is speed, simplicity, and not getting in the user's way.


%package	gnome
Summary:	GNOME menu support for IceWM window manager
Group:		User Interface/Desktops
Requires:	gnome-menus
Requires:	icewm = %{version}-%{release}


%description	gnome
IceWM-gnome adds gnome-menu support for the IceWM window manager.


%package	xdgmenu
BuildArch:	noarch
License:	Public Domain
Summary:	Automatically generate the main IceWM menu
Group:		User Interface/Desktops
Requires:	pyxdg
Requires:	icewm = %{version}-%{release}


%description	xdgmenu
IceWM-xdgmenu generates static IceWM menu files from the existing
freedesktop.org .desktop files. Files are re-generated each time the
user logs-in.


%package	clearlooks
BuildArch:	noarch
Summary:	Clearlooks like theme for IceWM
Group:		User Interface/Desktops
Requires:	ImageMagick
Requires:	icewm = %{version}-%{release}
Requires:	fedora-logos


%description	clearlooks
An IceWM theme that mimics the GNOME ClearLooks theme used by
older Fedora releases and RHEL.


%prep
%setup -q
%patch1 -p0 -b .menu
%patch2 -p1 -b .toolbar
%patch3 -p1 -b .keys
%patch4 -p0 -b .fribidi
%patch5 -p0 -b .dso
%patch6 -p0 -b .defaults
%patch7 -p1 -b .menuiconsize
%patch8 -p0 -b .deprecated


%build
autoreconf -vif
%configure --prefix=/usr \
	--enable-gradients \
	--enable-antialiasing \
	--enable-i18n \
	--enable-menus-gnome2 \
	--with-cfgdir=%{_sysconfdir}/icewm
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -p"

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -p -m 644 doc/icewm.1.man $RPM_BUILD_ROOT/%{_mandir}/man1/icewm.1

mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{_bindir}
install -p -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{_bindir}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icewm/
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/icewm/startup

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/xsessions/
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/xsessions/

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icewm/themes
tar -C $RPM_BUILD_ROOT%{_datadir}/icewm/themes -xzf %{SOURCE4}

echo "Theme=\"clearlooks/default.theme\"" > $RPM_BUILD_ROOT%{_datadir}/icewm/theme

%find_lang %{name}


%post clearlooks
[ -d /usr/share/icewm/themes/clearlooks ] && [ -x /usr/bin/convert ] &&	\
	[ -f /usr/share/icons/hicolor/24x24/apps/fedora-logo-icon.png ] && \
		convert /usr/share/icons/hicolor/24x24/apps/fedora-logo-icon.png \
				/usr/share/icewm/themes/clearlooks/taskbar/linux.xpm || echo -n


%files -f %{name}.lang
%doc AUTHORS BUGS CHANGES COPYING README README.wm-session TODO doc/*.html
%exclude %{_datadir}/icewm/startup
%exclude %{_datadir}/icewm/themes/clearlooks
%{_datadir}/icewm
%{_datadir}/xsessions/icewm.desktop
%{_mandir}/man1/icewm.1*
%{_bindir}/icewm-set-gnomewm
%{_bindir}/icewmbg
%{_bindir}/icehelp
%{_bindir}/icesh
%{_bindir}/icewm
%{_bindir}/icewm-session
%{_bindir}/icewmhint
%{_bindir}/icewmtray


%files gnome
%{_bindir}/icewm-menu-gnome2


%files xdgmenu
%{_bindir}/icewm-xdg-menu*
%{_datadir}/icewm/startup


%files clearlooks
%{_datadir}/icewm/themes/clearlooks-2px
%{_datadir}/icewm/themes/clearlooks
%{_datadir}/icewm/theme


%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.3.8-3
- Fix FTBFS on new architectures (aarch64/ppc64le)
- Cleanup and modernise spec

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 16 2013 Gilboa Davara <gilboad [AT] gmail.com> - 1.3.8-1
- 1.3.38.
- Clearlooks_v3: clearlooks_2px added. Should solve #981758 and #960663.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 09 2013 Gilboa Davara <gilboad [AT] gmail.com> - 1.3.7-9
- Fix #925574 by calling autoconf. (Temporary solution, pending upsteam fix).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 6 2012 Gilboa Davara <gilboad[AT]gmail.com> - 1.3.7-7
- Updated clearlooks package (#811331).
- (Blunder alert) Finally pushes gnome-icon-theme change to stable.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Gilboa Davara <gilboad[AT]gmail.com> - 1.3.7-5
- Bluecurve is still used for menu generation.
- "Rebuild program menu" menu entry added.

* Sun Jun 10 2012 Gilboa Davara <gilboad[AT]gmail.com> - 1.3.7-4
- Emacs replaced fixes (BZ #805939, Ported Debian fix).
- Use gnome-icon-theme instead of bluecurve (BZ #811335).
- Gcc 4.7 compile fix.
- spec cleanup.

* Sun Mar 4 2012 Gilboa Davara <gilboad[AT]gmail.com> - 1.3.7-3
- Fix missing bluecurve-icon-theme in EL-6.
- Start menu icon should now be generated correctly on both Fedora and EPEL.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Gilboa Davara <gilboad[AT]gmail.com> - 1.3.7-1
- Switch to 1.3.7 tree.
- Fixes bugs: #694532, #689804, #696291, #694622, #716218, #754124.
- Add Marcus Moeller's menu icon size and wmclient patches.
- Missing license information for icewm-xdg-menu.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.37-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 22 2010 Gilboa Davara <gilboad[AT]gmail.com> - 1.2.37-7
- Fix missing backspace.
- Fix duplicate clearlooks theme. (#545268)

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.2.37-6
- Rebuild for libgnome-desktop soname bump
- Fix mixed use of tabs and spaces

* Thu Sep 24 2009 Gilboa Davara <gilboad[AT]gmail.com> - 1.2.37-5
- Patch in missing fribidi support. (#515134)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Gilboa Davara <gilboad[AT]gmail.com> - 1.2.37-1
- 1.2.37.
- Fix missing directory ownership. (#483346)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 6 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.36-3
- pkg-config --cflags gnome-desktop-2.0 doesn't implicitly include
  libgnomeui-2.0 anymore, so add it in explicitly

* Mon Jan 5 2009 Gilboa Davara <gilboad[AT]gmail.com> - 1.2.36-2
- Missing BR libgnomeui-devel. (devel)
- Missing BR gnome-vfs2-devel. (devel)

* Thu Jan 24 2008 <gilboad[AT]gmail.com> - 1.2.35-3
- Fix broken -devel BR (truetype).

* Sat Jan 19 2008 <gilboad[AT]gmail.com> - 1.2.35-2
- Disable xorg-x11-fonts-truetype in -devel.

* Mon Jan 14 2008 <gilboad[AT]gmail.com> - 1.2.35-1
- 1.2.35.
- Missing BR: xorg-x11-fonts-truetype. (#351811)

* Tue Oct 09 2007 <gilboad[AT]gmail.com> - 1.2.32-5
- EL-5 support.
- Missing BR - libgif-devel.
- Devel: Replace redhat-artwork with bluecurve-icon-theme.

* Sun Sep 02 2007 <gilboad[AT]gmail.com> - 1.2.32-4
- Fix mangled if/else. (Again...)

* Sat Sep 01 2007 <gilboad[AT]gmail.com> - 1.2.32-3
- Fix missing BR: libXinerama-devel.
- Fix broken source file.

* Mon Aug 27 2007 <gilboad[AT]gmail.com> - 1.2.32-2
- Fix bad %%{_fedora} if/else.

* Sun Aug 26 2007 <gilboad[AT]gmail.com> - 1.2.32-1
- Fixed license tag.
- Fixed F8 BR - popt-devel.
- Remove APMstatus fix.
- 1.2.32

* Mon Apr 09 2007 <gilboad[AT]gmail.com> - 1.2.30-13
- APMStatus crash fix. (Icewm #1696182)

* Sat Feb 10 2007 <gilboad[AT]gmail.com> - 1.2.30-12
- Add missing dot in the -gnome sub-package description.
- Replace REQ icewm (in both -gnome and -xdgmenu) with icewm-x.x.x.
- Fix -xdgmenu file list and %%install section.
- Preserve the source time-stamp.

* Sun Feb 04 2007 <gilboad[AT]gmail.com> - 1.2.30-11
- Remove .Xdefaults fix from startup. (reported upstream).
- Replace buildroot with RPM_BUILD_ROOT.

* Sun Jan 28 2007 <gilboad[AT]gmail.com> - 1.2.30-10
- Missing REQ: icewm (both -gnome and -xdgmenu)
- Updated menu.in patch.
- Updated startup script. (-xdgmenu)
- Updated icewm-xdg-menu script. (-xdgmenu)

* Thu Jan 25 2007 <gilboad[AT]gmail.com> - 1.2.30-9
- Remove redundant icewm-xdg-menu* %%file entry.
- Change sub-package name to xdgmenu.
- Move icewm-xdg-menu to xdgmenu sub-package.
- Removed the icewm-generate-menu script.

* Sat Jan 20 2007 <gilboad[AT]gmail.com> - 1.2.30-8
- Fix source1 URL. (2nd is a winner)
- Fix -gnome summery.
- New sub-package: icewm-xdg-menu
- ALPHA: icewm-generate-menu script added to use icewm-xdg-menu to generate static menus.

* Sat Jan 20 2007 <gilboad[AT]gmail.com> - 1.2.30-7
- Fix source1 URL.
- Fix xdg-menu* owner.
- Replace default terminal icon to reduce dep-chain.
- Fix icewm-gnome description.
- Replace install with %%{_install}
- Push -gnome's BR to main package.
- Change hard-coded sysconf path.

* Thu Jan 18 2007 <gilboad[AT]gmail.com> - 1.2.30-6
- Change license back to LGPL.
- Change summery.
- New sub-package: -gnome. (GNOME menu support.)
- Missing REQ: xterm.
- Missing REQ: htmlview.
- Remove redundant %%_sysconf section.
- Remove redundant redhat-xxx icons.
- New REQ: redhat-artwork. (icons)
- Better man pages handling.
- Customize keys to better match fedora.
- New REQ: eject. (keys)
- New REQ: alsautils. (keys)

* Wed Jan 17 2007 <gilboad[AT]gmail.com> - 1.2.30-5
- Fix Source0 URL.
- Replace cp with install.
- Do not gzip the man page, just copy it.
- Use htmlview instead of firefox.
- Use BlueCurve icons instead of the mozilla ones.
- Re-fix lang support.
- Return the default configuration files to %%_datadir
- Add gdm session support.
- Remove gnome-menus from default menu - replace it with pyxdg/icewm-xdg-menu.

* Tue Jan 16 2007 <gilboad[AT]gmail.com> - 1.2.30-4
- Fix man page name.
- Remove missing menu items.
- Convert GNOME-menu patch to configure.in patch.
- Push default configuration into /etc/icewm
- Remove the default KDE support. (At least for now)
- Require firefox (default browser in Fedora).
- Add missing firefox icon. (No source - manual convert)
- Add missing gnome-menus. (required for GNOME2 menus)
- Fix missing gettext BR.
- Fix missing lang support.

* Sat Jan 13 2007 <gilboad[AT]gmail.com> - 1.2.30-3
- Fix wrong license. (Was LGPL, should be GPL.)

* Thu Jan 11 2007 <gilboad[AT]gmail.com> - 1.2.30-2
- Manually add missing man page.

* Thu Jan 11 2007 <gilboad[AT]gmail.com> - 1.2.30-1
- Initial release.

