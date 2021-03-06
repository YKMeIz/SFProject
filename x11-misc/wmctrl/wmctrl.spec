Name:           wmctrl
Version:        1.07
Release:        15%{?dist}
Summary:        Command line tool to interact with an X Window Manager

Group:          User Interface/X
License:        GPLv2+
URL:            http://sweb.cz/tripie/utils/wmctrl
Source0:        http://sweb.cz/tripie/utils/wmctrl/dist/%{name}-%{version}.tar.gz
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libXmu-devel
BuildRequires:  glib2-devel
Patch0:         http://ftp.de.debian.org/debian/pool/main/w/wmctrl/wmctrl_1.07-6.diff.gz
Patch1:         wmctrl-sticky-workspace.patch

%description
The wmctrl program is a UNIX/Linux command line tool to interact with an
EWMH/NetWM compatible X Window Manager. The tool provides command line access
to almost all the features defined in the EWMH specification. It can be used,
for example, to obtain information about the window manager, to get a detailed
list of desktops and managed windows, to switch and resize desktops, to make
windows full-screen, always-above or sticky, and to activate, close, move,
resize, maximize and minimize them. The command line access to these window
management functions makes it easy to automate and execute them from any
application that is able to run a command in response to an event.


%prep
%setup -q
%patch0 -p1
%patch1 -p1


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%doc AUTHORS COPYING README
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 24 2012 Jens Petersen <petersen@redhat.com> - 1.07-12
- add patch to allow stick to all workspaces from Jeff Bastien (#524023)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec  1 2011 Jens Petersen <petersen@redhat.com> - 1.07-10
- drop INSTALL and ChangeLog from doc files

* Thu Sep 29 2011 Jens Petersen <petersen@redhat.com> - 1.07-9
- revive orphaned package (#742166)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 28 2008 Patrice Dumas <pertusus@free.fr> - 1.07-5
- apply debian patcheset, to fix #426383

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.07-4
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.07-3
- Autorebuild for GCC 4.3

* Wed Oct 04 2006 Michael Rice <errr[AT]errr-online.com> - 1.07-2
- Fix Summary per rpmlint warning
- Fix description per rpmlint warning
- Remove unneeded line from setup
- Remove NEWS from docs since it was empty
- Reformat Changlelog entrys in spec file due to bad formatting
- Changed Group to User Interface/X

* Wed Sep 27 2006 Michael Rice <errr[AT]errr-online.com> - 1.07-1
- Initial RPM release
