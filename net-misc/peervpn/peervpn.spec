%global _hardened_build 1

%global major 0
%global minor 042

Name:               peervpn
Version:            %{major}.%{minor}
Release:            1%{?dist}
Summary:            A VPN software using full mesh network topology

Group:              Applications/Internet
License:            GPLv3+
URL:                http://www.peervpn.net/
Source0:            http://www.peervpn.net/files/peervpn-%{major}-%{minor}.tar.gz
Source1:            %{name}@.service
Source2:            README.Fedora

BuildRequires:      openssl-devel
BuildRequires:      systemd
# for /usr/sbin/ip
Requires:           iproute
# for /usr/sbin/ifconfig
Requires:           net-tools
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
PeerVPN is software that builds virtual Ethernet networks between multiple
computers. It uses full mesh network topology and can automatically build
tunnels through firewalls and NATs. It supports shared key encryption and
authentication.

%prep
%setup -q -n peervpn-%{major}-%{minor}

%build
make %{?_smp_mflags} \
    CFLAGS="%{?optflags} `pkg-config --cflags libcrypto`" \
    LDFLAGS="%{?__global_ldflags}" \
    LIBS="`pkg-config --libs libcrypto`"

%install
rm -rf %{buildroot}
install -D -m 0755 peervpn %{buildroot}%{_sbindir}/%{name}
install -d -m 0700 %{buildroot}%{_sysconfdir}/%{name}
install -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}@.service
cp %{SOURCE2} .

%post
find %{_sysconfdir}/%{name} -name \*.conf 2>/dev/null | while read conf; do
    conf=${conf#%{_sysconfdir}/%{name}/}; conf=${conf%.conf}
    %systemd_post %{name}@${conf}.service
done

%preun
find %{_sysconfdir}/%{name} -name \*.conf 2>/dev/null | while read conf; do
    conf=${conf#%{_sysconfdir}/%{name}/}; conf=${conf%.conf}
    %systemd_preun %{name}@${conf}.service
done

%postun
find %{_sysconfdir}/%{name} -name \*.conf 2>/dev/null | while read conf; do
    conf=${conf#%{_sysconfdir}/%{name}/}; conf=${conf%.conf}
    %systemd_postun_with_restart %{name}@${conf}.service 
done

%files
%doc license.txt peervpn.conf README.Fedora
%{_sbindir}/%{name}
%{_unitdir}/%{name}@.service
%attr(700,root,root) %config %dir %{_sysconfdir}/%{name}

%changelog
* Tue Feb 10 2015 Nux <rpm@li.nux.ro> - 0.042-1
- Update to 0.042

* Wed Oct 22 2014 Jan Cholasta <jcholast@redhat.com> - 0.040-1
- Updated to 0.040

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.039-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.039-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 31 2014 Jan Cholasta <jcholast@redhat.com> - 0.039-1
- Updated to 0.039.

* Thu Aug 22 2013 Jan Cholasta <jcholast@redhat.com> - 0.036-1
- Updated to 0.036.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.033-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jun 5 2013 Jan Cholasta <jcholast@redhat.com> - 0.033-1
- Updated to 0.033.

* Mon Feb 11 2013 Jan Cholasta <jcholast@redhat.com> - 0.032-1
- Updated to 0.032.

* Mon Dec 10 2012 Jan Cholasta <jcholast@redhat.com> - 0.031-1
- Updated to 0.031.

* Wed Nov 14 2012 Jan Cholasta <jcholast@redhat.com> - 0.029-1
- Updated to 0.029.

* Wed Nov 7 2012 Jan Cholasta <jcholast@redhat.com> - 0.028-1
- Initial package.
