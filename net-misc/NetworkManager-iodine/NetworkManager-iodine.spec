Summary: NetworkManager VPN plugin for iodine
Name: NetworkManager-iodine
Version: 0.0.4
Release: 2%{?dist}
License: GPLv2+
URL: https://honk.sigxcpu.org/piki/projects/network-manager-iodine
Group: System Environment/Base
Source0: https://git.gnome.org/browse/network-manager-iodine/snapshot/network-manager-iodine-0.0.4.tar.gz

# Avoid AC_PROG_LIBTOOL deprecated macro
# Upstream bug: https://bugzilla.gnome.org/show_bug.cgi?id=720453
Patch0: lt_init.patch

BuildRequires: autoconf
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: libtool intltool gettext
Requires: shared-mime-info
Requires: iodine-client

%global _privatelibs libnm-iodine-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the iodine server and NetworkManager.

%package -n NetworkManager-iodine-gnome
Summary: NetworkManager VPN plugin for iodine - GNOME files
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: nm-connection-editor

%description -n NetworkManager-iodine-gnome
This package contains software for integrating VPN capabilities with
the iodine server and NetworkManager (GNOME files).

%prep
%setup -q -n network-manager-iodine-%{version}

%patch0 -p1 -b .lt_init

%build
if [ ! -f configure ]; then
  ./autogen.sh
fi
CFLAGS="$RPM_OPT_FLAGS -Wno-deprecated-declarations" \
	%configure --disable-static --disable-dependency-tracking --enable-more-warnings=yes --with-gtkver=3
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" install

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS
%{_sysconfdir}/dbus-1/system.d/nm-iodine-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-iodine-service.name
%{_libexecdir}/nm-iodine-service
%{_libexecdir}/nm-iodine-auth-dialog

%files -n NetworkManager-iodine-gnome
%doc COPYING AUTHORS
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/iodine
%{_datadir}/gnome-vpn-properties/iodine/nm-iodine-dialog.ui

%changelog
* Sat Dec 14 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.4-2
- Removed auto required packages

* Fri Dec 13 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.4-1
- Changes for review

* Tue Dec 10 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.4-0.1.20131210gita2a90c6
- Initial spec release
