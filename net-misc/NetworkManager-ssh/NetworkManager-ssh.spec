%global commit 46247c270d55309087be926386af7fc569039fe0
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global checkout 20140209git%{shortcommit}

Summary: NetworkManager VPN plugin for SSH
Name: NetworkManager-ssh
Version: 0.9.2
Release: 0.2.%{checkout}%{?dist}
License: GPLv2+
URL: https://github.com/danfruehauf/NetworkManager-ssh
Group: System Environment/Base
Source0: https://github.com/danfruehauf/NetworkManager-ssh/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

BuildRequires: autoconf
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: glib2-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: libtool intltool gettext
Requires: gtk3
Requires: dbus
Requires: NetworkManager
Requires: openssh-clients
Requires: shared-mime-info
Requires: gnome-keyring
Requires: sshpass

%global _privatelibs libnm-ssh-properties[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

%description
This package contains software for integrating VPN capabilities with
the OpenSSH server with NetworkManager.

%package -n NetworkManager-ssh-gnome
Summary: NetworkManager VPN plugin for SSH - GNOME files
Group: System Environment/Base
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: nm-connection-editor

%description -n NetworkManager-ssh-gnome
This package contains software for integrating VPN capabilities with
the OpenSSH server with NetworkManager (GNOME files).

%prep
%setup -q -n %{name}-%{commit}

%build
if [ ! -f configure ]; then
  autoreconf -fvi
fi
CFLAGS="$RPM_OPT_FLAGS -Wno-deprecated-declarations" \
	%configure --disable-static --disable-dependency-tracking --enable-more-warnings=yes --with-gtkver=3
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" install

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}

%files -f %{name}.lang
%doc COPYING AUTHORS README ChangeLog
%{_sysconfdir}/dbus-1/system.d/nm-ssh-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-ssh-service.name
%{_libexecdir}/nm-ssh-service
%{_libexecdir}/nm-ssh-auth-dialog

%files -n NetworkManager-ssh-gnome
%doc COPYING AUTHORS README ChangeLog
%{_libdir}/NetworkManager/lib*.so*
%dir %{_datadir}/gnome-vpn-properties/ssh
%{_datadir}/gnome-vpn-properties/ssh/nm-ssh-dialog.ui

%changelog
* Sun Feb 09 2014 Dan Fruehauf <malkodan@gmail.com> - 0.9.2-0.2.20140209git46247c2
- Fixed upstream #25 (Fedora #1056810) - Bad strcmp usage
- Fixed upstream #27 (Fedora #1061365, #1058028) - sshpass via fd

* Sun Aug 11 2013 Dan Fruehauf <malkodan@gmail.com> - 0.9.1-0.5.20130706git6bf4649
- Added $RPM_OPT_FLAGS to CFLAGS

* Mon Aug 05 2013 Dan Fruehauf <malkodan@gmail.com> - 0.9.1-0.4.20130706git6bf4649
- Remove deprecated warning

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-0.3.20130706git6bf4649
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Dan Fruehauf <malkodan@gmail.com> - 0.9.1-0.2.20130706git6bf4649
- Depends on sshpass

* Sat Jul 06 2013 Dan Fruehauf <malkodan@gmail.com> - 0.9.1-0.1.20130706git6bf4649
- Support for password and plain key authentication 

* Tue Jun 25 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.4-0.1.20130625git241fee0
- Can choose to not set VPN as default route

* Fri Apr 19 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.3-0.8.20130419git3d5321b
- DBUS and NetworkManager files in /etc are no longer config files
- Other refactoring to conform with other NetworkManager VPN plugins

* Fri Apr 05 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.3-0.7.20130405git6ba59c4
- Added sub package for NetworkManager-ssh-gnome

* Tue Apr 02 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.3-0.6.20130402git6ba59c4
- Fixed dependencies (openssh-clients
- Added private libs

* Sat Mar 30 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.3-0.5.20130330git9afb20
- Removed macros from changelog

* Thu Mar 28 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.3-0.4.20130328gita2add30
- Fixed more issues in spec to conform with Fedora Packaging standards

* Tue Mar 26 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.3-0.3.20130326git7549f1d
- More changes to conform with Fedora packaging standards

* Fri Mar 22 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.3-0.2.20130322git8767415
- Changes to conform with Fedora packaging standards

* Wed Mar 20 2013 Dan Fruehauf <malkodan@gmail.com> - 0.0.3-0.1.20130320gitcf6c00f
- Initial spec release
