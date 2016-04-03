%global	urlver		3.4
%global	mainver	3.4.1

%global	core_least_ver	3.4.1

%global	ruby_vendorlib	%(ruby -rrbconfig -e "puts RbConfig::CONFIG['vendorlibdir']")

%global	build_unstable	1

Name:			cairo-dock-plug-ins
Version:		%{mainver}
Release:		4%{?dist}
Summary:		Plug-ins files for Cairo-Dock

License:		GPLv3+
URL:			http://glx-dock.org/
#Source0:		http://launchpad.net/cairo-dock-plug-ins/%%{urlver}/%%{mainver}/+download/cairo-dock-plugins-%%{mainver}.tar.gz
# Some contents removed: see https://bugzilla.redhat.com/show_bug.cgi?id=1178912
Source0:		cairo-dock-plugins-fedora-%{version}.tar.gz
# Source0 is created from Source1
Source1:		cairo-dock-plug-ins-create-fedora-tarball.sh
# demo_ruby: fix traceback when changing themes
Patch1:		cairo-dock-plugins-3.4.1-0001-demo_ruby-fix-traceback-when-changing-themes.patch
# Default to xdg-screensaver for lock_screen
Patch2:		cairo-dock-plugins-3.4.1-0002-Default-to-xdg-screensaver-for-lock_screen.patch
Patch3:		cairo-dock-plugins-3.4.1-0003-lock-screen.sh-used-xdg-screensaver-if-available.patch

BuildRequires:	cmake
BuildRequires:	gettext

BuildRequires:	pkgconfig(gldi) = %{core_least_ver}
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)

# Plug-ins
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(gnome-vfs-2.0)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(libgnome-menu-3.0)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libical)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libxklavier)
# BuildRequires:	pkgconfig(thunar-vfs-1)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	pkgconfig(vte-2.90)
BuildRequires:	pkgconfig(webkitgtk-3.0)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(zeitgeist-1.0)

BuildRequires:	libetpan-devel
BuildRequires:	lm_sensors-devel

# Bindings
BuildRequires:	python2-devel
BuildRequires:	python3-devel
BuildRequires:	ruby-devel
BuildRequires:	vala

Requires:	%{name}-base%{?_isa} = %{version}-%{release}
# Explicitly write below
Requires:	%{name}-dbus%{?_isa} = %{version}-%{release}
# cairo-dock-launcher-API-daemon is written in python,
# so for now make this depending on python
Requires:	cairo-dock-python2 = %{version}-%{release}
# Require xdg-utils for logout by default
Requires:	xdg-utils

%description
This package is a meta package for Cairo-Dock plugins.

%package	base
Summary:	Base files for Cairo-Dock plugins
Requires:	cairo-dock-core%{?_isa} = %{core_least_ver}
Requires:	%{name}-common = %{version}-%{release}

%description	base
This package contains plug-ins files for Cairo-Dock.


%package	common
Summary:	Common files for Cairo-Dock plugins
BuildArch:	noarch

%description	common
This file contains common files for Cairo-Dock plugins.

%package	dbus
Summary:	Plug-ins files for Cairo-Dock related to Dbus
Requires:	cairo-dock-core%{?_isa} >= %{core_least_ver}
Requires:	%{name}-common = %{version}-%{release}

%description	dbus
This package contains plug-ins files for Cairo-Dock related
to Dbus.

%package	xfce
Summary:	Plug-ins files for Cairo-Dock related to Xfce
Requires:	cairo-dock-core%{?_isa} >= %{core_least_ver}
Requires:	%{name}-common = %{version}-%{release}

%description	xfce
This package contains plug-ins files for Cairo-Dock related
to Xfce.

%package	kde
Summary:	Plug-ins files for Cairo-Dock related to KDE
Requires:	cairo-dock-core%{?_isa} >= %{core_least_ver}
Requires:	%{name}-common = %{version}-%{release}

%description	kde
This package contains plug-ins files for Cairo-Dock related
to KDE.

%package	webkit
Summary:	Plug-ins files for Cairo-Dock related to WebKit
Requires:	cairo-dock-core%{?_isa} >= %{core_least_ver}
Requires:	%{name}-common = %{version}-%{release}

%description	webkit
This package contains plug-ins files for Cairo-Dock related
to WebKit.

%package	unstable
Summary:	Unstable plug-ins not installed by default
Requires:	cairo-dock-core%{?_isa} >= %{core_least_ver}
Requires:	%{name}-common = %{version}-%{release}

%description	unstable
This package contains unstable and experimental
plug-ins not installed by default.

%package	-n cairo-dock-python2
Summary:	Python2 binding for Cairo-Dock
Requires:	cairo-dock-core >= %{core_least_ver}
Requires:	%{name}-dbus = %{version}-%{release}
Requires:	pygobject2
Requires:	dbus-python
Obsoletes:	cairo-dock-python < 3.4.0-8.99
Provides:	cairo-dock-python = %{version}-%{release}
BuildArch:	noarch

%description	-n cairo-dock-python2
This package contains Python2 binding files for Cairo-Dock

%package	-n cairo-dock-python3
Summary:	Python3 binding for Cairo-Dock
Requires:	cairo-dock-core >= %{core_least_ver}
Requires:	%{name}-dbus = %{version}-%{release}
Requires:	pygobject3
Requires:	python3-dbus
BuildArch:	noarch

%description	-n cairo-dock-python3
This package contains Python3 binding files for Cairo-Dock

%package	-n cairo-dock-ruby
Summary:	Ruby binding for Cairo-Dock
Requires:	cairo-dock-core >= %{core_least_ver}
Requires:	%{name}-common = %{version}-%{release}
Requires:	ruby(release)
Requires:	rubygem(ruby-dbus)
Requires:	rubygem(parseconfig)
BuildArch:	noarch

%description	-n cairo-dock-ruby
This package contains Ruby binding files for Cairo-Dock

%package	-n cairo-dock-vala
Summary:	Vala binding for Cairo-Dock
Requires:	cairo-dock-core%{?_isa} >= %{core_least_ver}
Requires:	%{name}-common = %{version}-%{release}
Requires:	vala

%description	-n cairo-dock-vala
This package contains Vala binding files for Cairo-Dock

%package	-n cairo-dock-vala-devel
Summary:	Development files for Vala binding for Cairo-Dock
Requires:	cairo-dock-vala%{?_isa} = %{version}-%{release}
Requires:	%{name}-dbus%{?isa} = %{version}-%{release}

%description	-n cairo-dock-vala-devel
This package contains development files for Vala
binding for Cairo-Dock.

%prep
%setup -q -n cairo-dock-plugins-%{mainver}
%patch1 -p1
%patch2 -p1
%patch3 -p1

## permission
# %%_fixperms cannot fix permissions completely here
for dir in */
do
	find $dir -type f | xargs chmod 0644
done
chmod 0644 [A-Z]* copyright
chmod 0755 */

# cmake issue
sed -i.debuglevel \
	-e '\@add_definitions@s|-O3|-O2|' \
	CMakeLists.txt
sed -i.stat \
	-e 's|\${MSGFMT_EXECUTABLE}|\${MSGFMT_EXECUTABLE} --statistics|' \
	po/CMakeLists.txt

## source code fix
## Bindings
# Ruby
sed -i.site \
	-e "s|CONFIG\['rubylibdir'\]|CONFIG['vendorlibdir']|" \
	CMakeLists.txt
# ????
sed -i.installdir \
	-e '\@REGEX REPLACE.*RUBY@d' \
	-e '\@set.*RUBY_LIB_DIR.*CMAKE_INSTALL_PREFIX.*RUBY_LIB_DIR_INSTALL@d' \
	CMakeLists.txt

%build
rm -f CMakeCache.txt
%cmake \
%if 0%{?build_unstable} >= 1
	-Denable-disks=TRUE \
	-Denable-doncky=TRUE \
	-Denable-global-menu=TRUE \
	-Denable-network-monitor=TRUE \
%if 0
	-Denable-scooby-do=TRUE \
%endif
%endif

make %{?_smp_mflags}

%install
%make_install \
	INSTALL="install -p"

# Collect documents
rm -rf documents licenses documents-dbus
mkdir documents licenses documents-dbus
cp -a \
	ChangeLog \
	documents
mkdir documents-dbus/Dbus
cp -a Dbus/demos \
	documents-dbus/Dbus/
cp -a \
	LGPL-2 \
	LICENSE \
	copyright \
	licenses/

# Just to suppress rpmlint...
pushd $RPM_BUILD_ROOT

for f in \
	`find . -name \*.conf`
do
	sed -i -e '1i\ ' $f
done

set +x
for f in \
	.%{_datadir}/cairo-dock/plug-ins/*/* \
	$(find . -name \*.rb)
do
	if head -n 1 $f 2>/dev/null | grep -q /bin/ ; then 
		set -x
		chmod 0755 $f
		set +x
	fi
done

# Modify CDApplet.h not to contain %%buildroot strings
sed -i .%{_datadir}/cairo-dock/plug-ins/Dbus/CDApplet.h \
	-e '\@def@s|__.*\(DBUS_INTERFACES_VALA_SRC_CDAPPLET_H__\)|__\1|'

popd

%find_lang cairo-dock-plugins

%post -n cairo-dock-vala -p /sbin/ldconfig
%postun -n cairo-dock-vala -p /sbin/ldconfig

%files	common
%license	licenses/*

%files
# This is a metapackage

%files	base -f cairo-dock-plugins.lang
%doc	documents/*

%{_libdir}/cairo-dock/*
%{_datadir}/cairo-dock/plug-ins/*
%{_datadir}/cairo-dock/gauges/*/

%exclude	%{_libdir}/cairo-dock/*weblet*
%exclude	%{_libdir}/cairo-dock/*xfce*
%exclude	%{_libdir}/cairo-dock/*kde*
%exclude	%{_libdir}/cairo-dock/*Dbus*
%exclude	%{_datadir}/cairo-dock/plug-ins/*weblet*
%exclude	%{_datadir}/cairo-dock/plug-ins/*xfce*
%exclude	%{_datadir}/cairo-dock/plug-ins/*kde*
%exclude	%{_datadir}/cairo-dock/plug-ins/Dbus/
%if 0%{?build_unstable} >= 1
%exclude	%{_libdir}/cairo-dock/appmenu-registrar
%exclude	%{_libdir}/cairo-dock/libcd-Global-Menu.so
%exclude	%{_libdir}/cairo-dock/libcd-disks.so
%exclude	%{_libdir}/cairo-dock/libcd-doncky.so
%exclude	%{_libdir}/cairo-dock/libcd-network-monitor.so
#%%exclude	%%{_libdir}/cairo-dock/libcd-scooby-do.so
%exclude	%{_datadir}/cairo-dock/plug-ins/Disks/
%exclude	%{_datadir}/cairo-dock/plug-ins/Doncky/
%exclude	%{_datadir}/cairo-dock/plug-ins/Global-Menu/
%exclude	%{_datadir}/cairo-dock/plug-ins/Network-Monitor/
#%%exclude	%%{_datadir}/cairo-dock/plug-ins/Scooby-Do/
%endif
# Vala
%exclude	%{_datadir}/cairo-dock/plug-ins/Dbus/CDApplet.h

%if 0%{?build_unstable} >= 1
%files	unstable
%{_libdir}/cairo-dock/appmenu-registrar
%{_libdir}/cairo-dock/libcd-Global-Menu.so
%{_libdir}/cairo-dock/libcd-disks.so
%{_libdir}/cairo-dock/libcd-doncky.so
%{_libdir}/cairo-dock/libcd-network-monitor.so
#%%{_libdir}/cairo-dock/libcd-scooby-do.so
%{_datadir}/cairo-dock/plug-ins/Disks/
%{_datadir}/cairo-dock/plug-ins/Doncky/
%{_datadir}/cairo-dock/plug-ins/Global-Menu/
%{_datadir}/cairo-dock/plug-ins/Network-Monitor/
#%%{_datadir}/cairo-dock/plug-ins/Scooby-Do/
%endif

%files	dbus
%doc	documents-dbus/*
%{_libdir}/cairo-dock/*Dbus*
%{_datadir}/cairo-dock/plug-ins/Dbus/
# The following is for cairo-dock-vala-devel
%exclude	%{_datadir}/cairo-dock/plug-ins/Dbus/CDApplet.h

%files	xfce
%{_libdir}/cairo-dock/*xfce*
%{_datadir}/cairo-dock/plug-ins/*xfce*

%files	kde
%{_libdir}/cairo-dock/*kde*
%{_datadir}/cairo-dock/plug-ins/*kde*

%files	webkit
%{_libdir}/cairo-dock/*weblet*
%{_datadir}/cairo-dock/plug-ins/*weblet*

%files	-n cairo-dock-python2
%{python2_sitelib}/CairoDock.py*
%{python2_sitelib}/CDApplet.py*
%{python2_sitelib}/CDBashApplet.py*
%{python2_sitelib}/*.egg-info

%files	-n cairo-dock-python3
%{python3_sitelib}/CairoDock.py*
%{python3_sitelib}/CDApplet.py*
%{python3_sitelib}/CDBashApplet.py*
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/__pycache__/

%files	-n cairo-dock-ruby
%{ruby_vendorlib}/CDApplet.rb

%files -n cairo-dock-vala
%{_libdir}/libCDApplet.so.1*
%{_datadir}/vala/vapi/CDApplet.*

%files -n cairo-dock-vala-devel
%{_libdir}/libCDApplet.so
%{_libdir}/pkgconfig/CDApplet.pc
%{_datadir}/cairo-dock/plug-ins/Dbus/CDApplet.h

%changelog
* Wed Dec 02 2015 Nux <rpm@li.nux.ro> - 3.4.1-3
- rebuild with newer ical from CentOS 7.2

* Wed Mar 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-3
- Require xdg-utils by default for logout

* Wed Mar 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-2
- Default to xdg-screensaver for lock_screen
- Restrict the dependency for core package

* Thu Mar 13 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-1
- 3.4.1
- demo_ruby: fix traceback when changing themes

* Sat Feb 28 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-14
- Bump release

* Wed Feb 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-13
- Cosmetic changes

* Wed Feb 11 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-12
- Split out Dbus subpackage, modify internal dependency
- Make some packages noarch

* Fri Jan 23 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-11
- Another may-be-problematic contents removed (bug 1178912)
- Make sure that licenses files are always installed

* Thu Jan 22 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-10
- Some may-be-problematic contents removed (bug 1178912)

* Fri Jan 02 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-9
- Initial package
