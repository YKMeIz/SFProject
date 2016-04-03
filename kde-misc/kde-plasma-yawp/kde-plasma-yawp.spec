Name:           kde-plasma-yawp
Version:        0.4.5
Release:        3%{?dist}
Summary:        Yet Another Weather Plasmoid
Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.kde-look.org/content/show.php?content=94106
Source0:        http://downloads.sourceforge.net/yawp/yawp-%{version}.tar.bz2

BuildRequires:  gettext
BuildRequires:  kdebase-workspace-devel
BuildRequires:  kdelibs4-devel
BuildRequires:  kdeplasma-addons-devel

# minimal runtime deps
%{?_kde4_version:Requires: kdelibs4%{?_isa} >= %{_kde4_version}}
%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}


%description
This colorful plasmoid shows weather maps, reports and forecasts.


%prep
%setup -q -n yawp-%{version}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang plasma_applet_yawp


%files -f plasma_applet_yawp.lang
%doc CHANGELOG COPYRIGHT LICENSE* README TODO
%{_kde4_libdir}/kde4/plasma_applet_yawp.so
%{_kde4_libdir}/kde4/ion_accuweather.so
%{_kde4_libdir}/kde4/ion_wunderground.so
%{_kde4_datadir}/kde4/services/plasma-applet-yawp.desktop
%{_kde4_datadir}/kde4/services/ion-accuweather.desktop
%{_kde4_datadir}/kde4/services/ion-wunderground.desktop
%{_kde4_appsdir}/desktoptheme/default/widgets/*.svg


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.5-1
- update to 0.4.5

* Thu Mar 21 2013 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.4-3
- fix systemtray crash

* Tue Mar 19 2013 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.4-2
- fix widget geometry

* Sun Mar 17 2013 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.4-1
- update to 0.4.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.3-1
- update to 0.4.3

* Wed Jan  4 2012 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.2-1
- update to 0.4.2

* Sat Dec  3 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.1-1
- update to 0.4.1

* Thu Nov 17 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.0-5
- fix geometry settings (#754407)

* Sun Nov 13 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.0-2
- fix unowned dir

* Sun Nov 13 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.4.0-1
- update to 0.4.0

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Alexey Kurov <nucleo@fedoraproject.org> - 0.3.6-1
- update to 0.3.6
- drop 0.3.5 patches

* Wed Nov 24 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.5-6
- Fix build against KDE4.6

* Tue Nov 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.3.5-5
- rebuild

* Sun Nov 07 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.5-4
- Rebuild due to soname bump in libweather_ion.so from kdebase-workspace-libs

* Tue Oct 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.3.5-3
- minimal qt4 runtime dep too

* Mon Oct 11 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.5-2
- Fix crash when built against KDE 4.5.1 RHBZ#641971

* Fri Oct 08 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.5-1
- update to 0.3.5

* Sun Oct 03 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.4-4
- better patch for KDE4.5

* Sun Oct 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.3.4-2
- add minimum kde runtime dep

* Tue Sep 07 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.4-2
- patch for KDE4.5

* Sat Jul 10 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.4-1
- new version

* Tue Jun 15 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.3-1
- new version

* Tue Dec 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.3.2-2
- rebuild against kde-4.4beta1 (#549620)

* Sun Dec 06 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.2-1
- Update to new upstream version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 06 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.2.3-1
- Initial build
