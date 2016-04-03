%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Name:   arandr
Version:        0.1.7.1
Release:        4%{?dist}
Summary:        Simple GTK+ XRandR GUI

Group:  Applications/System
License:        GPLv3
URL:    http://christian.amsuess.com/tools/arandr/
Source0:        http://christian.amsuess.com/tools/arandr/files/%{name}-%{version}.tar.gz
Patch0:         0001-Make-ARandR-appear-in-XFCE-Settings-Manager.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  python
BuildRequires:  python-docutils
BuildRequires:  gettext
BuildRequires:  python-setuptools
BuildRequires:  desktop-file-utils
Requires:       python
Requires:       pygtk2
Requires:       xorg-x11-server-utils

%description
ARandR is designed to provide a simple visual front end for XRandR 1.2/1.3.
Relative monitor positions are shown graphically and can be changed in a
drag-and-drop way.

%prep
%setup -q
%patch0 -p1


%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --root=%{buildroot}
desktop-file-validate %{buildroot}/%{_datadir}/applications/arandr.desktop
%find_lang %{name}


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README TODO ChangeLog NEWS COPYING
%{_bindir}/arandr
%{_bindir}/unxrandr
%{python_sitelib}/screenlayout/
%{python_sitelib}/arandr-%{version}-py*.egg-info
%{_mandir}/man1/arandr.1.gz
%{_mandir}/man1/unxrandr.1.gz
%{_datadir}/applications/arandr.desktop


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 14 2013 Maros Zatko <mzatko@fedoraproject.org> - 0.1.7.1-3
- Add patch for ARandR to be in XFCE Settings Manager

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Maros Zatko <mzatko@fedoraproject.org> - 0.1.7-1
- new version (1.7.1)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Maros Zatko <mzatko@fedoraproject.org> - 0.1.6-1
- new version (1.6)

* Mon Oct 03 2011 Maros Zatko <mzatko@fedoraproject.org> - 0.1.4-4
- fixed tab indentation
- changed py2.7 -> py*

* Mon Sep 19 2011 Maros Zatko <mzatko@fedoraproject.org> - 0.1.4-3
- RPM_BUILD_ROOT replaced by macro
- doc files are handled completely by doc macro

* Sat Sep 17 2011 Maros Zatko <mzatko@fedoraproject.org> - 0.1.4-2
- tabs replaced by spaces
- COPYING, README, ChangeLog, NEWS and TODO doc entry
- fixed date in previous changelog entry
- desktop files installed according to guidelines

* Thu Sep 15 2011 Maros Zatko <mzatko@fedoraproject.org> - 0.1.4-1
- Initial package
