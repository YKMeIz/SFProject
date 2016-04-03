%global plugins      animation colorfilter expo ezoom imgjpeg mag mousepoll neg opacify put resizeinfo ring scaleaddon session shift snap staticswitcher text thumbnail titleinfo vpswitch winrules workarounds

%global  basever 0.8.8

Name:    compiz-plugins-main
Version: 0.8.8
Release: 13%{?dist}
Epoch:   1
Summary: Collection of Compiz Fusion plugins for Compiz      
Group:   User Interface/Desktops        
License: GPLv2+       
URL:     http://www.compiz.org             
Source0: http://releases.compiz.org/%{version}/%{name}-%{version}.tar.bz2

Patch0:  compiz-plugins-main_new-mate.patch
# new from debian 
# https://bugs.launchpad.net/bugs/103306
Patch1:  compiz-plugins-main_fix_edges.patch
# https://bugs.launchpad.net/bugs/326995
Patch2:  compiz-plugins-main_expo_reflection_is_unphysical.patch

Patch3:  compiz-plugins-main_incorrect-fsf-address_fix.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=909657
Patch4:  compiz-plugins-main_primary-is-control.patch

Patch5:  compiz-plugins-main_remove_gconf_usage.patch
Patch6:  compiz-plugins-main-aarch64.patch
Patch7:  compiz-plugins-main_automake-1.13.patch

# libdrm is not available on these arches
ExcludeArch:   s390 s390x

BuildRequires: compiz-devel >= %{basever}
BuildRequires: compiz-bcop >= %{basever}
BuildRequires: gettext-devel
BuildRequires: cairo-devel
BuildRequires: pango-devel
BuildRequires: perl(XML::Parser)
BuildRequires: mesa-libGLU-devel
BuildRequires: libXrender-devel
BuildRequires: libjpeg-devel
BuildRequires: intltool
BuildRequires: libtool

Requires: compiz%{?_isa} >= %{basever}

Provides: compiz-plugins-main-mate = %{epoch}:%{version}-%{release}
Obsoletes: compiz-plugins-main-mate < %{epoch}:%{version}-%{release}

%description
The Compiz Fusion Project brings 3D desktop visual effects that improve
usability of the X Window System and provide increased productivity
though plugins and themes contributed by the community giving a
rich desktop experience

%package devel
Group: Development/Libraries
Summary: Development files for Compiz-Fusion
Requires: compiz-devel%{?_isa} >= %{basever}
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: cairo-devel
Requires: pango-devel

%description devel
This package contain development files required for developing other plugins


%prep
%setup -q
%patch0 -p1 -b .mate
%patch1 -p1 -b .edges
%patch2 -p1 -b .expo_reflection
%patch3 -p1 -b .incorrect-fsf-address
%patch4 -p1 -b .primary-is-control
%patch5 -p1 -b .remove_gconf
%patch6 -p1 -b .aarch64
%patch7 -p1 -b .automake
mv images/Gnome/*.png images/Default/
rm -rf images/Gnome
rm -rf images/Mate

autoreconf -f -i


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/compiz/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/compiz/*.a
# remove wall plugin
rm -f $RPM_BUILD_ROOT%{_datadir}/compiz/wall.xml
rm -f $RPM_BUILD_ROOT%{_libdir}/compiz/libwall.so
# remove kdecompat plugin
rm -f $RPM_BUILD_ROOT%{_libdir}/compiz/libkdecompat.so
rm -f $RPM_BUILD_ROOT%{_datadir}/compiz/kdecompat.xml

# remove oxygen images
rm -rf $RPM_BUILD_ROOT%{_datadir}/compiz/Oxygen

%find_lang %{name}



%files -f %{name}.lang
%doc COPYING AUTHORS
%{_libdir}/compiz/*.so
%{_datadir}/compiz/*.xml
%{_datadir}/compiz/filters/
%{_datadir}/compiz/Default/

%files devel
%{_includedir}/compiz/
%{_libdir}/pkgconfig/compiz-*


%changelog
* Wed Mar 18 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-13
- rebuild for f22

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-9
- fix build for aarch64
- fix automake-1.13 build deprecations
- clean up mate patch

* Wed Apr 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-8
- remove gconf usage
- move gnome magnifier image from Mate to Default folder
- rework mate patch

* Sun Feb 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-7
- add compiz-plugins-main_primary-is-control.patch
- this will set all default configurations to pimary key
- fix (#909657)

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1:0.8.8-6
- rebuild due to "jpeg8-ABI" feature drop

* Sat Dec 22 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-5
- disable mateconf schemas and clean spec file
- remove mate subpackage
- remove matecompat icon
- remove icon cache scriptlet

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.8.8-4
- own include dir
- move icons from gnome to mate folder in source
- add requires compiz
- remove oxygen images
- add patches from Jasmine Hassan jasmine.aura@gmail.com
- add icon cache scriplets
- add compiz-plugins-main_incorrect-fsf-address_fix.patch
- add epoch
- add basever

* Sat Sep 29 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-3
- remove kdecompat
- correct plugin %%global
- fix source url

* Wed Sep 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-2
- add source overlay.png and mask.png
- improve spec file
- remove obsolete beryl stuff
- add compiz-plugins-main_mate.patch

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.8.8-1
- build for mate

* Sun May 06 2012 Andrew Wyatt <andrew@fuduntu.org> - 0.8.8-1
- Update to latest stable release

