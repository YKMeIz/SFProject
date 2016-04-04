
# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

Name:    kate
Summary: Advanced Text Editor
Version: 15.12.3
Release: 2%{?dist}

# kwrite LGPLv2+
# kate: app LGPLv2, plugins, LGPLv2 and LGPLv2+ and GPLv2+
# ktexteditor: LGPLv2
License: LGPLv2 and LGPLv2+ and GPLv2+ 
URL:     https://projects.kde.org/kate
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/kate-%{version}.tar.xz

BuildRequires: extra-cmake-modules
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: pkgconfig(libgit2)
BuildRequires: pkgconfig(x11)
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kdoctools-devel
BuildRequires: kf5-kguiaddons-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kitemmodels-devel
BuildRequires: kf5-kjobwidgets-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-kparts-devel
BuildRequires: kf5-ktexteditor-devel
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: kf5-kxmlgui-devel
BuildRequires: kf5-kservice-devel
BuildRequires: kf5-plasma-devel
BuildRequires: kf5-threadweaver-devel
BuildRequires: kf5-kwallet-devel
BuildRequires: kf5-kcrash-devel
BuildRequires: kf5-kactivities-devel

BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtscript-devel

# not sure if we want -plugins by default, let's play it safe'ish
# and make it optional
Recommends: %{name}-plugins%{?_isa} = %{version}-%{release}

%description
%{summary}.

%package plugins
Summary: Kate plugins
License: LGPLv2
# upgrade path, when -plugins were split
Obsoletes: kate < 14.12.1
Requires: %{name} = %{version}-%{release}
%description plugins
%{summary}.

%package -n kwrite
Summary: Text Editor
License: LGPLv2+
%description -n kwrite
%{summary}.


%prep
%autosetup -n kate-%{version} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.kate.desktop
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.kwrite.desktop


%post
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null || :
fi

%files
%license COPYING.LIB
%doc AUTHORS
%{_kf5_bindir}/kate
%{_kf5_datadir}/applications/org.kde.kate.desktop
%{_kf5_datadir}/appdata/org.kde.kate.appdata.xml
%{_kf5_datadir}/icons/hicolor/*/apps/kate.*
%{_mandir}/man1/kate.1*
%lang(en) %{_kf5_docdir}/HTML/en/kate/
%lang(en) %{_kf5_docdir}/HTML/en/katepart/
#{_kf5_datadir}/kxmlgui5/kate/
%{_kf5_datadir}/plasma/plasmoids/org.kde.plasma.katesessions/
%{_kf5_datadir}/kservices5/plasma-applet-org.kde.plasma.katesessions.desktop
%{_kf5_datadir}/kservices5/plasma-dataengine-katesessions.desktop
%{_kf5_datadir}/plasma/services/org.kde.plasma.katesessions.operations

%files plugins
%{_kf5_qtplugindir}/ktexteditor/katebacktracebrowserplugin.so
%{_kf5_qtplugindir}/ktexteditor/katebuildplugin.so
%{_kf5_qtplugindir}/ktexteditor/katecloseexceptplugin.so
%{_kf5_qtplugindir}/ktexteditor/katectagsplugin.so
%{_kf5_qtplugindir}/ktexteditor/katefilebrowserplugin.so
%{_kf5_qtplugindir}/ktexteditor/katefiletreeplugin.so
%{_kf5_qtplugindir}/ktexteditor/kategdbplugin.so
%{_kf5_qtplugindir}/ktexteditor/katekonsoleplugin.so
%{_kf5_qtplugindir}/ktexteditor/kateopenheaderplugin.so
%{_kf5_qtplugindir}/ktexteditor/kateprojectplugin.so
%{_kf5_qtplugindir}/ktexteditor/katesearchplugin.so
%{_kf5_qtplugindir}/ktexteditor/katesnippetsplugin.so
%{_kf5_qtplugindir}/ktexteditor/katesqlplugin.so
%{_kf5_qtplugindir}/ktexteditor/katesymbolviewerplugin.so
%{_kf5_qtplugindir}/ktexteditor/katexmltoolsplugin.so
%{_kf5_qtplugindir}/ktexteditor/tabswitcherplugin.so
%{_kf5_qtplugindir}/ktexteditor/katereplicodeplugin.so
%{_kf5_qtplugindir}/ktexteditor/kterustcompletionplugin.so
%{_kf5_qtplugindir}/ktexteditor/ktexteditor_lumen.so
%{_kf5_qtplugindir}/ktexteditor/textfilterplugin.so
%{_kf5_qtplugindir}/plasma/dataengine/plasma_engine_katesessions.so
%{_kf5_datadir}/kateproject/
%{_kf5_datadir}/katexmltools/
%{_kf5_datadir}/kxmlgui5/katexmltools/

%post -n kwrite
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :

%posttrans -n kwrite
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null || :

%postun -n kwrite
if [ $1 -eq 0 ] ; then
touch --no-create %{_kf5_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kf5_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null || :
fi

%files -n kwrite
%{_kf5_bindir}/kwrite
%{_kf5_datadir}/applications/org.kde.kwrite.desktop
%{_kf5_datadir}/appdata/org.kde.kwrite.appdata.xml
%{_kf5_datadir}/icons/hicolor/*/apps/kwrite.*
%lang(en) %{_kf5_docdir}/HTML/en/kwrite/


%changelog
* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 15.12.3-2
- Rebuild for libgit2 0.24.0

* Sun Mar 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.3-1
- 15.12.3

* Sun Feb 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.2-1
- 15.12.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Rex Dieter <rdieter@fedoraproject.org> 15.12.1-2
- include kwrite icon in kwrite pkg, %%lang'ify HTML docs

* Mon Jan 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.1-1
- 15.12.1

* Sun Dec 20 2015 Rex Dieter <rdieter@fedoraproject.org> 15.12.0-1
- 15.12.0

* Mon Dec 14 2015 Rex Dieter <rdieter@fedoraproject.org> 15.08.3-3
- setQuitOnLastWindowClosed.patch

* Wed Dec 02 2015 Rex Dieter <rdieter@fedoraproject.org> 15.08.3-2
- Recommends: kate-plugins, update URL

* Wed Dec 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.08.3-1
- 15.08.3

* Tue Sep 29 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.08.1-1
- 15.08.1

* Thu Aug 20 2015 Than Ngo <than@redhat.com> - 15.08.0-1
- 15.08.0

* Fri Jul 31 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 15.04.3-2
- Rebuilt for libgit2-0.23.0 and libgit2-glib-0.23

* Thu Jul 02 2015 Rex Dieter <rdieter@fedoraproject.org> 15.04.3-1
- 15.04.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.04.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.2-1
- 15.04.2

* Mon Jun 01 2015 Rex Dieter <rdieter@fedoraproject.org> 15.04.1-2
- %%{?kf5_kinit_requires}

* Tue May 26 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.1-1
- 15.04.1

* Tue Apr 14 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.0-1
- 15.04.0

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> 14.12.3-1
- kf5 kate-14.12.3, grow -plugins subpkg

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-4
- kwrite: use %%{?kde_runtime_requires}

* Sat Jan 17 2015 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-3
- -part: Provides: kate4-part

* Fri Jan 16 2015 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-2
- kde-applications cleanups

* Sat Nov 08 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.3-1
- 4.14.3

* Sat Oct 11 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.2-1
- 4.14.2

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.1-1
- 4.14.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.0-1
- 4.14.0

* Sun Aug 10 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.97-5
- kwrite needs update-desktop-database scriptlet too

* Sun Aug 10 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.97-4
- fix scriptlets (need update-desktop-database instead of update-mime-database)

* Fri Aug 08 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.97-3
- re-enable -pate (hopefully pykde4 is fixed for real this time)

* Fri Aug 08 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.97-2
- disable -pate, FTBFS against latest pykde4 (dont know exactly why yet...)

* Tue Aug 05 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.97-1
- 4.13.97

* Mon Jul 14 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.3-1
- 4.13.3

* Mon Jun 30 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.2-2
- BR: qtwebkit ...

* Mon Jun 09 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.2-1
- 4.13.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.1-1
- 4.13.1

* Sat Apr 12 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.0-1
- 4.13.0

* Fri Apr 04 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.97-1
- 4.12.97

* Sat Mar 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.95-1
- 4.12.95

* Wed Mar 19 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.90-1
- 4.12.90

* Fri Mar 07 2014 Rex Dieter <rdieter@fedoraproject.org> 4.12.3-2
- implement upstreamable PYTHON_LIBRARY_REALPATH fix (#1050944)

* Sat Mar 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.3-1
- 4.12.3

* Fri Jan 31 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.2-1
- 4.12.2

* Fri Jan 10 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.1-1
- 4.12.1

* Fri Jan 10 2014 Rex Dieter <rdieter@fedoraproject.org> 4.12.0-2
- workaround libpython dlopen failure (#1050944)

* Thu Dec 19 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.12.0-1
- 4.12.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 4.11.97-2
- (re)enable pate, add dependencies (#1028819)

* Sun Dec 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.97-1
- 4.11.97

* Thu Nov 21 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.95-1
- 4.11.95

* Sat Nov 16 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.90-1
- 4.11.90, omit -pate (bootstrap)

* Sat Nov 02 2013 Rex Dieter <rdieter@fedoraproject.org> 4.11.3-2
- kate: pate(python) plugins not built/packaged (#922280)

* Sat Nov 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.3-1
- 4.11.3

* Wed Oct 02 2013 Rex Dieter <rdieter@fedoraproject.org> 4.11.2-2
- respin tarball

* Sat Sep 28 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-1
- 4.11.2

* Tue Sep 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.1-1
- 4.11.1

* Thu Aug 08 2013 Than Ngo <than@redhat.com> - 4.11.0-1
- 4.11.0

* Thu Jul 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.97-1
- 4.10.97

* Tue Jul 23 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.95-1
- 4.10.95

* Thu Jun 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.90-1
- 4.10.90

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Thu Apr 04 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.2-2
- -libs: Obsoletes: kdesdk-libs (instead of Conflicts)

* Sun Mar 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Tue Mar 19 2013 Than Ngo <than@redhat.com> - 4.10.1-3
- backport to fix python indentation mode

* Tue Mar 19 2013 Than Ngo <than@redhat.com> - 4.10.1-2
- Fix documentation multilib conflict in index.cache

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.1-1
- 4.10.1

* Fri Feb 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Sun Jan 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-2
- kate has a file conflict with kdelibs3 (#883529)

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-1
- 4.9.90 (4.10 beta2)

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.95-1
- 4.8.95

* Sat Jun 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Fri Jun 01 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-2
- respin

* Sat May 26 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.80-1
- 4.8.80

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.3-2
- s/kdebase-runtime/kde-runtime/

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Radek Novacek <rnovacek@redhat.com> - 4.8.1-1
- 4.8.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for c++ ABI breakage

* Fri Jan 20 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.0-1
- 4.8.0

* Wed Jan 04 2012 Radek Novacek <rnovacek@redhat.com> - 4.7.97-1
- 4.7.97

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- 4.7.90

* Thu Nov 24 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.80-1
- 4.7.80 (beta 1)

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 07 2011 Than Ngo <than@redhat.com> - 4.7.1-1
- 4.7.1

* Thu Jul 28 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.0-2
- -part: move %%_kde4_appsdir/katepart/ here

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.0-1
- 4.7.0

* Mon Jul 18 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6.95-1
- first try

