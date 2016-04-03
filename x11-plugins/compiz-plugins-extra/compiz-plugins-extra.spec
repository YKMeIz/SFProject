%global plugins     3d addhelper animationaddon bench bicubic crashhandler cubeaddon extrawm fadedesktop firepaint gears grid group loginout maximumize mblur notification reflex scalefilter shelf showdesktop showmouse splash trailfocus wallpaper widget

%global  basever 0.8.8

Name:    compiz-plugins-extra
Version: 0.8.8
Release: 14%{?dist}
Epoch:   1
Summary: Additional Compiz Fusion plugins for Compiz

Group:   User Interface/Desktops
License: GPLv2+ and MIT
URL:     http://www.compiz.org
Source0: http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2
Patch0:  compiz-plugins-extra_new-mate.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=909657
Patch1:  compiz-plugins-extra_primary-is-control.patch

Patch2:  compiz-plugins-extra_remove_gconf_usage.patch

Patch3:  compiz-plugins-extra_libnotify.patch
Patch4:  compiz-plugins-extra-aarch64.patch
Patch5:  compiz-plugins-extra_automake-1.13.patch

# libdrm is not available on these arches
ExcludeArch: s390 s390x

BuildRequires: compiz-plugins-main-devel >= %{basever}
BuildRequires: compiz-bcop >= %{basever}
BuildRequires: gettext-devel
BuildRequires: perl(XML::Parser)
BuildRequires: mesa-libGLU-devel
BuildRequires: libXrender-devel
BuildRequires: libnotify-devel
BuildRequires: libjpeg-devel
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: gtk2-devel

Requires: compiz-plugins-main%{?_isa} >= %{basever}

Provides: compiz-fusion-extra%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: compiz-fusion-extra%{?_isa} < %{epoch}:%{version}-%{release}

%description
The Compiz Fusion Project brings 3D desktop visual effects that improve
usability of the X Window System and provide increased productivity
though plugins and themes contributed by the community giving a
rich desktop experience.
This package contains additional plugins from the Compiz Fusion Project

%package devel
Group: Development/Libraries
Summary: Development files for Compiz-Fusion
Requires: compiz-plugins-main-devel%{?_isa} >= %{basever}
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Provides: compiz-fusion-extra-devel%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes: compiz-fusion-extra-devel%{?_isa} < %{epoch}:%{version}-%{release}

%description devel
This package contain development files required for developing other plugins


%prep
%setup -q
%patch0 -p1 -b .mate
%patch1 -p1 -b .primary-is-control
%patch2 -p1 -b .gconf
%patch3 -p1 -b .libnotify
%patch4 -p1 -b .aarch64
%patch5 -p1 -b .automake

autoreconf -f -i

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc COPYING AUTHORS
%{_libdir}/compiz/*.so
%{_datadir}/compiz/*.xml
%{_datadir}/compiz/*.png

%files devel
%{_includedir}/compiz/
%{_libdir}/pkgconfig/compiz-*


%changelog
* Wed Mar 18 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-14
- rebuild for f22

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-10
- fix build for aarch64
- add autoreconf command + necessary BR
- fix automake-1.13 build deprecations
- add BR gtk2-devel

* Sun Feb 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-9
- rework mate patch
- remove gconf usage
- switch to libnotify

* Sun Feb 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-8
- add compiz_primary-is-control.patch
- this will set all default configurations to pimary key
- fix (#909657)

* Sun Jan 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-7
- obsolete compiz-fusion-extra

* Sat Jan 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-6
- add ldconfig scriplets
- trailing whitespace from the Summary,Group,License and URL lines

* Sat Dec 22 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-5
- disable mateconf schemas
- remove rpm scriptlet
- remove mate subpackage
- remove copying part from mate patch

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-4
- build for fedora
- rename patch
- own include dir
- fix license information
- add basever

* Sat Sep 29 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-3
- add Epoch tag
- improve spec file

* Wed Sep 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-2
- add compiz-plugins-extra_mate.patch
- improve spec file

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-1
- build for mate

