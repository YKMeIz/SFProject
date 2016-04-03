Name:           megamario
Version:        1.5
Release:        5%{?dist}
Summary:        Well known platform game clone
Group:          Amusements/Games
License:        LGPL+
URL:            http://mmario.sourceforge.net/
Source0:        http://downloads.sourceforge.net/mmario/MegaMario_v1.5_w32_linux.zip
Source1:        %{name}.desktop
Patch0:         megamario-1.5-compile-fix.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  SDL_mixer-devel SDL_image-devel SDL_ttf-devel
BuildRequires:  ImageMagick desktop-file-utils
Requires:       hicolor-icon-theme

%description
MegaMario is a clone of a well know platform game, featuring 25 new levels. In
the game you play Mario and your task is to free his brother Luigi, who was
captured by the evil Bowser.


%prep
%setup -q -c
%patch0 -p1
sed -i 's/\r//' *.txt


%build
make %{?_smp_mflags} PREFIX=%{_prefix} \
  CFLAGS="$RPM_OPT_FLAGS -fsigned-char"
convert -transparent '#FF00FF' data/gfx/characters/small/player1r.PNG \
  %{name}.png


%install
rm -rf $RPM_BUILD_ROOT
make install PREFIX=$RPM_BUILD_ROOT%{_prefix}
# cruft removal
rm $RPM_BUILD_ROOT%{_datadir}/megamario/levels/1/1
rm $RPM_BUILD_ROOT%{_datadir}/megamario/levels/11/maiin
rm $RPM_BUILD_ROOT%{_datadir}/megamario/save.sav
rm $RPM_BUILD_ROOT%{_datadir}/megamario/sfx/jump.gpk
rm $RPM_BUILD_ROOT%{_datadir}/megamario/gfx/tiles/pipes/left/Desktop.ini

# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor dribble           \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps
install -p -m 644 %{name}.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :

%postun
touch --no-create %{_datadir}/icons/hicolor || :
%{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :


%files
%defattr(-,root,root,-)
%doc CONTROLS.txt licence.txt readme.txt fixes_v1.5.txt
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/dribble-%{name}.desktop
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png


%changelog
* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.5-5
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.5-3
- rebuild for new F11 features

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-2
- Release bump for rpmfusion

* Tue Jun  5 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.5-1%{?dist}
- New upstream release 1.5

* Sat Mar 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3-3%{?dist}
- Fixup .desktop file categories for games-menus usage
- No longer use preconverted .png as RH bug 196010 is fixed

* Sun Jul  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3-2%{?dist}
- Use a preconverted .png as icon to work around RH bug 196010

* Thu Jun 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.3-1%{?dist}
- Initial Fedora Extras package
