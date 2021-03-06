%global nm_version          1:0.9.2
%global dbus_version        1.1
%global gtk3_version        3.0
%global ppp_version         %(rpm -q ppp --queryformat '%{VERSION}')
%global shared_mime_version 0.16-3

Summary:   NetworkManager VPN plugin for l2tp
Name:      NetworkManager-l2tp
Version:   0.9.8.6
Release:   2%{?dist}
# The most of code uses GPLv2+ license.
# Only vpn-password-dialog has LGPLv2+.
License:   GPLv2+ and LGPLv2+
URL:       https://launchpad.net/~seriy-pr/+archive/network-manager-l2tp
Source:    https://github.com/seriyps/NetworkManager-l2tp/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: libtool
BuildRequires: gtk3-devel             >= %{gtk3_version}
BuildRequires: dbus-devel             >= %{dbus_version}
BuildRequires: dbus-glib-devel        >= 0.74
BuildRequires: NetworkManager-devel   >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: libgnome-keyring-devel
BuildRequires: intltool gettext
BuildRequires: ppp-devel

# nm-connection-editor was a part of NetworkManager-gnome but since F18 it splits
%if 0%{?fedora} > 17 || 0%{rhel} >= 7
Requires: nm-connection-editor
%else
Requires: NetworkManager-gnome
%endif
Requires: dbus             >= %{dbus_version}
Requires: NetworkManager   >= %{nm_version}
Requires: ppp              = %{ppp_version}
Requires: shared-mime-info >= %{shared_mime_version}
Requires: pptp
Requires: gnome-keyring
Requires: xl2tpd
Requires: openswan

%filter_provides_in %{_libdir}/pppd/%{ppp_version}/nm-l2tp-pppd-plugin.so
%filter_provides_in %{_libdir}/NetworkManager/lib*.so

%description
This package contains software for integrating L2TP VPN support with
the NetworkManager and the GNOME desktop.

%prep
%setup -q

%build
./autogen.sh
%configure \
    --disable-static \
    --enable-more-warnings=yes \
    --with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version}

make %{?_smp_mflags}

%install

make install DESTDIR=%{buildroot} INSTALL="/usr/bin/install -p"

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

rm -f %{buildroot}%{_libdir}/pppd/%{ppp_version}/nm-l2tp-pppd-plugin.la
rm -f %{buildroot}%{_libdir}/pppd/%{ppp_version}/nm-l2tp-pppd-plugin.a

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/nm-l2tp-service.conf
# Content must not be changed
%config %{_sysconfdir}/NetworkManager/VPN/nm-l2tp-service.name
%{_libdir}/NetworkManager/lib*.so
%{_libdir}/pppd/2.*/nm-l2tp-pppd-plugin.so
%{_libexecdir}/nm-l2tp-auth-dialog
%{_libexecdir}/nm-l2tp-service
%{_datadir}/gnome-vpn-properties/l2tp

%changelog
* Fri Apr 11 2014 Ivan Romanov <drizt@land.ru> - 0.9.8.6-2
- use ppp of any version
- dropped Groups tag

* Thu Feb 27 2014 Ivan Romanov <drizt@land.ru> - 0.9.8.6-1
- updated to 0.9.8.6

* Sun Jan 19 2014 Ivan Romanov <drizt@land.ru> - 0.9.8.5-1
- updated to 0.9.8.5
- dropped patches, went to upstream

* Mon Sep 23 2013 Ivan Romanov <drizt@land.ru> - 0.9.8-4
- added NetworkManager-l2tp-Check-var-run-pluto-ipsec-info patch (#887674)

* Mon Sep 23 2013 Ivan Romanov <drizt@land.ru> - 0.9.8-3
- added NetworkManager-l2tp-noccp-pppd-option patch (#887674)

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr  1 2013 Ivan Romanov <drizt@land.ru> - 0.9.8-1
- a new upstream version

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 25 2012 Ivan Romanov <drizt@land.ru> - 0.9.6-5
- openswan is requires

* Tue Dec 25 2012 Ivan Romanov <drizt@land.ru> - 0.9.6-4
- added openswan to BR

* Sat Dec 15 2012 Ivan Romanov <drizt@land.ru> - 0.9.6-3
- fix F17 dependency error (rh #886773)
- added licensies explanations

* Mon Nov 26 2012 Ivan Romanov <drizt@land.ru> - 0.9.6-2
- corrected License tag. Added LGPLv2+
- use only %%{buildroot}
- use %%config for configuration files
- removed unused scriptlets
- cleaned .spec file
- preserve timestamps when installing
- filtered provides for plugins
- droped zero-length changelog
- use %%global instead of %%define

* Mon Nov 19 2012 Ivan Romanov  <drizt@land.ru> - 0.9.6-1
- initial version based on NetworkManager-pptp 1:0.9.3.997-3

