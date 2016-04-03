# norootforbuild

%if 0%{?suse_version} >= 1220
%define xsltpkg libxslt-tools
%else
%define xsltpkg libxslt
%endif

Name:           compton
Version:        0.1.0
Release:        1.1
Summary:        A compositor for X11
License:        MIT
Group:          System/X11/Utilities
Url:            https://github.com/chjj/compton
Source:         compton-%{version}.tar.bz2
BuildRequires:  gcc-c++ make pkgconfig
BuildRequires:  pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xfixes)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libconfig)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  git
BuildRequires:	asciidoc
BuildRequires:	%{xsltpkg}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Prefix:         /usr


%description
Compton was forked from Dana Jansens' fork of xcompmgr and refactored. I fixed whatever bug I found, and added features I wanted. Things seem stable, but don't quote me on it. I will most likely be actively working on this until I get the features I want. This is also a learning experience for me. That is, I'm partially doing this out of a desire to learn Xlib.


%prep
%setup


%build
# Extract the snapshot somewhere...
# Export the COMPTON_VERSION variable (you may also pass it to make directly)
export COMPTON_VERSION=%{version}%
make
make docs


%install
make install DESTDIR=%{buildroot}
# desktop file is broken:
#[   11s] ERROR: No sufficient Category definition: /home/abuild/rpmbuild/BUILDROOT/compton-0.1.0-0.x86_64//usr/share/applications/compton.desktop 
#[   11s] ERROR: Icon file not installed: /home/abuild/rpmbuild/BUILDROOT/compton-0.1.0-0.x86_64//usr/share/applications/compton.desktop (xcompmgr)
#[   11s] WARNING: Empty GenericName: /home/abuild/rpmbuild/BUILDROOT/compton-0.1.0-0.x86_64//usr/share/applications/compton.desktop
rm %{buildroot}/usr/share/applications/compton.desktop



%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_bindir}/compton
%{_bindir}/compton-trans
%{_mandir}/man1/compton.1.gz
%{_mandir}/man1/compton-trans.1.gz


%changelog
* Tue Aug 13 2013 petr@yarpen.cz
- version 0.1.0
* Mon Jan 28 2013 petr@yarpen.cz
- new dependencies: git, dbus-1
- COMPTON_VERSION set for building
* Fri Oct 26 2012 petr@yarpen.cz
- Version bump to 0.0.1
* Mon Oct  1 2012 petr@scribus.info
- Initial package 0.0.0
