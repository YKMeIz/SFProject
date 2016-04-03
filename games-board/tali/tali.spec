Name:           tali
Version:        3.10.2
Release:        1%{?dist}
Summary:        GNOME Tali game

License:        GPLv2+ and GFDL
URL:            https://live.gnome.org/Tali
Source0:        http://ftp.gnome.org/pub/GNOME/sources/%{name}/3.10/%{name}-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  librsvg2-devel

Obsoletes: gnome-games-extra < 1:3.7.92
Obsoletes: gnome-games-gtali < 1:3.7.92

%description
Sort of poker with dice and less money. An ancient Roman game.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/gtali.desktop

%find_lang %{name} --all-name --with-gnome


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/icons/HighContrast &>/dev/null || :


%postun
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
  touch --no-create %{_datadir}/icons/HighContrast &>/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/HighContrast &> /dev/null || :
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/HighContrast &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :


%files -f %{name}.lang
%doc COPYING
%attr(2551, root, games) %{_bindir}/tali
%{_datadir}/appdata/
%{_datadir}/applications/gtali.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.tali.gschema.xml
%{_datadir}/icons/hicolor/*/apps/tali.*
%{_datadir}/icons/HighContrast/*/apps/tali.png
%{_datadir}/tali
%verify(not md5 size mtime) %config(noreplace) %attr(664, games, games) %{_localstatedir}/games/gtali.*
%{_mandir}/man6/tali.6*


%changelog
* Mon Nov 11 2013 Richard Hughes <rhughes@redhat.com> - 3.10.2-1
- Update to 3.10.2

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92
- Include the appdata file
- Package up the HighContrast icons and add cache scriptlets

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-2
- Obsolete gnome-games-extra (for upgrades from f17)

* Fri Mar 29 2013 Tanner Doshier <doshitan@gmail.com> - 3.8.0-1
- Update to 3.8.0
- Use setgid games

* Fri Mar 22 2013 Tanner Doshier <doshitan@gmail.com> - 3.7.92-1
- Update to 3.7.92
- Use old desktop file name

* Tue Mar 12 2013 Tanner Doshier <doshitan@gmail.com> - 3.7.4-1
- Initial packaging of standalone tali
