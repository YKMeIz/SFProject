Name: system-switch-displaymanager
Summary: A display manager switcher for GDM, KDM, XDM, WDM and LightDM
Version: 1.3
Release: 4%{?dist}
URL: http://fedoraproject.org/wiki/switch-displaymanager
Source: %{name}-%{version}.tar.xz
License: GPLv2+
Group: User Interface/Desktops
Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: noarch
Requires: polkit
BuildRequires: intltool
BuildRequires: gettext
BuildRequires: desktop-file-utils

%description
The Display Manager Switcher is a tool which enables users to easily switch
between various deskplay managers that they have installed. The tool includes
support for GDM, KDM, XDM and WDM.

Install system-switch-displaymanager if you need a tool for switching between
display managers.

%package gnome
Group: User Interface/Desktops
Summary: A graphical interface for the Display Manager Switcher
Requires: %{name} = %{version}-%{release} python pygtk2

%description gnome
The system-switch-displaymanager-gnome package provides the GNOME graphical user
interface for the Display Manager Switcher.

%prep

%setup -q -n %{name}-%{version}

%build
make

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

%find_lang %{name} || true

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING
%dir %{_datadir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/polkit-1/actions/*
%{_datadir}/%{name}/%{name}-helper
%{_mandir}/man1/*

%files gnome -f %{name}.lang
%defattr(-,root,root)
%{_datadir}/%{name}/pixmaps
%{_datadir}/%{name}/*.glade
%{_datadir}/%{name}/*.py*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/*/*.png

%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Than Ngo <than@redhat.com> - 1.3-1
- fix bz#866721, bz#873899
- polkit support
- systemd support

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 1.2-6
- recompiling .py files against Python 2.7 (rhbz#623408)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.2-3
- Rebuild for Python 2.6

* Sat Oct 04 2008 Than Ngo <than@redhat.com> 1.2-2
- add %%dist

* Wed Sep 24 2008 Than Ngo <than@redhat.com> 1.2-1
- 1.2
- WDM setting issue
- add missing icons for WDM/XDM

* Thu Sep 11 2008 Than Ngo <than@redhat.com> 1.1-1
- rename to system-switch-displaymanager

* Fri Aug 15 2008 Than Ngo <than@redhat.com> 1.0-1
- 1.0
