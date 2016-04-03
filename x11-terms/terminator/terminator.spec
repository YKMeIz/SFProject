%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           terminator
Version:        0.97
Release:        6%{?dist}
Summary:        Store and run multiple GNOME terminals in one window

Group:          User Interface/Desktops
License:        GPLv2
URL:            http://gnometerminator.blogspot.com/p/introduction.html
Source0:        https://launchpad.net/terminator/trunk/%{version}/+download/terminator-%{version}.tar.gz
Patch0:         0000-terminator-fix-desktop-file.patch
Patch1:         0001-terminator-fix-inactive-colour.patch

BuildArch:      noarch
BuildRequires:  python-devel gettext desktop-file-utils intltool
Requires:       vte gnome-python2-gconf GConf2 gtk2 desktop-file-utils
Requires:       gnome-python2-bonobo


%description
Multiple GNOME terminals in one window.  This is a project to produce
an efficient way of filling a large area of screen space with
terminals. This is done by splitting the window into a resizeable
grid of terminals. As such, you can  produce a very flexible
arrangements of terminals for different tasks.


%prep
%setup -q 
sed -i '/#! \?\/usr.*/d' terminatorlib/*.py
%patch0 
%patch1 


%build
%{__python} setup.py build


%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%find_lang %{name}
rm -f %{buildroot}/%{_datadir}/icons/hicolor/icon-theme.cache
rm -f %{buildroot}/%{_datadir}/applications/%{name}.desktop
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications data/%{name}.desktop


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root)
%doc README COPYING ChangeLog
%{_mandir}/man1/%{name}.*
%{_mandir}/man5/%{name}_config.*
%{_bindir}/%{name}
%{_bindir}/remotinator
%{python_sitelib}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}*.png
%{_datadir}/icons/hicolor/*/*/%{name}*.svg
%{_datadir}/icons/hicolor/16x16/status/terminal-bell.png
%{_datadir}/pixmaps/%{name}.png


%post
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor &>/dev/null || :


%postun
gtk-update-icon-cache -qf %{_datadir}/icons/hicolor &>/dev/null || :


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 05 2014 Dominic Hopf <dmaphy@fedoraproject.org> - 0.97-5
- fix the new URL for the website

* Sun Jan 05 2014 Dominic Hopf <dmaphy@fedoraproject.org> - 0.97-4
- update upstream URL to new website (RHBZ#1048553)
- fix bogus date in changelog-warnings

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 0.97-2
- fix an issue when inactive colour is set to 1.0 (RHBZ#968379)

* Fri May 17 2013 Dominic Hopf <dmaphy@fedoraproject.org> - 0.97-1
- New upstream release: Terminator 0.97

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Sep 24 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.96-1
- New upstream release: Terminator 0.96

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 01 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.95-2
- readd dependency for gnome-python2-bonobo 

* Wed Aug 25 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.95-1
- New upstream release: Terminator 0.95

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.94-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 19 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.94-1
- New upstream release: Terminator 0.94

* Thu Apr 15 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.93-1
- New upstream release: Terminator 0.93

* Fri Apr 09 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.92-1
- New upstream release: Terminator 0.92

* Mon Apr 05 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.91-1
- New upstream release: Terminator 0.91

* Wed Mar 10 2010 Steven Fernandez <lonetwin@fedoraproject.org> 0.14-3
- Added patch to fix the traceback reported in bug 567861

* Wed Mar 3 2010 Steven Fernandez <lonetwin@fedoraproject.org> - 0.14-2
- Added dependency for deskbar-applets and gnome-python2-{bonobo,canvas}
  packages (bug 540551 and bug 509461)

* Thu Jan 14 2010 Dominic Hopf <dmaphy@fedoraproject.org> - 0.14-1
- New terminator version 0.14

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Ian Weller <ian@ianweller.org> - 0.13-2
- BuildRequires: intltool

* Thu Jul  2 2009 Ian Weller <ian@ianweller.org> - 0.13-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Ian Weller <ianweller@gmail.com> 0.12-1
- New upstream release
- Upstream fixed desktop file, removing patch0

* Mon Dec 08 2008 Ian Weller <ianweller@gmail.com> 0.11-3
- Patch version in terminatorlib/verison.py to the one we think it is
- Fix License tag
- Update post and postun scripts with one line

* Mon Dec 01 2008 Ian Weller <ianweller@gmail.com> 0.11-2
- Add BuildRequires: gettext
- Fix installation of .desktop file
- terminator-0.11-desktop.patch:
    Remove useless things
    Move to same category as gnome-terminal
- Uses spaces instead of tabs in the specfile because I can't stand tabs

* Mon Dec 01 2008 Ian Weller <ianweller@gmail.com> 0.11-1
- Update upstream
- Fix description to something useful
- Fix group
- Fix some specfile oddities
- Complete/restandardize file list
- Get rid of she-bangs in python_sitelib

* Sat Sep 13 2008 Max Spevack <mspevack AT redhat DOT com> 0.10
- New upstream release.
- Tried to make sure the spec file matches guidelines on Fedora wiki.

* Tue Jul 08 2008 chantra AatT rpm-based DdOoTt org 0.9.fc9.rb
- New upstream release

* Sat May 17 2008 chantra AatT rpm-based DdOoTt org 0.8.1.fc9.rb
- Initial release for Fedora 9.
