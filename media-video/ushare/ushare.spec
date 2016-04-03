Summary: UPnP (TM) A/V & DLNA Media Server
Name: ushare
Version: 1.1a
Release: 12%{?dist}
License: LGPLv2+
Group: Applications/Multimedia
URL: http://ushare.geexbox.org/

Source: http://ushare.geexbox.org/releases/%{name}-%{version}.tar.bz2
Source1:ushare.init
Patch0: ushare-conf.patch
Patch1: ushare-error.patch
Patch2: 101-ushare-upnp-build-fix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libupnp-devel, pkgconfig
Requires: /usr/sbin/alternatives
Requires(pre): fedora-usermgmt
Requires(post): /sbin/chkconfig, /usr/sbin/alternatives
Requires(preun): /sbin/service, /sbin/chkconfig, /usr/sbin/alternatives
Requires(postun): /sbin/service

%description
uShare is a UPnP (TM) A/V & DLNA Media Server. It implements the server 
component that provides UPnP media devices with information on 
available multimedia files. uShare uses the built-in http server 
of libupnp to stream the files to clients.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
iconv -f ISO_8859-1 -t UTF-8 AUTHORS --output AUTHORS.utf8
cp -af AUTHORS.utf8 AUTHORS

%build
export CFLAGS="$RPM_OPT_FLAGS"
./configure --prefix=%{_prefix} --localedir=%{_datadir}/locale --sysconfdir=%{_sysconfdir} --disable-dlna --enable-debug
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%makeinstall DESTDIR=%{buildroot}
%{__rm} -rf   %{buildroot}%{_sysconfdir}/init.d
%{__install} -m 0755 -D %{SOURCE1} %{buildroot}%{_initrddir}/ushare
%{__mkdir_p} %{buildroot}%{_var}/lib/ushare
%{__mv} %{buildroot}%{_bindir}/ushare %{buildroot}%{_bindir}/ushare-fedora
%find_lang %{name}

%clean
rm -rf %{buildroot}

%pre
%{_sbindir}/fedora-useradd 21 -s /sbin/nologin -M -r -d %{_var}/lib/ushare \
    -c "ushare service account" ushare &>/dev/null || :

%post
/sbin/chkconfig --add ushare
alternatives --install %{_bindir}/ushare ushare %{_bindir}/ushare-fedora 10

%preun
if [ $1 -eq 0 ]; then
    /sbin/service ushare stop &>/dev/null || :
    /sbin/chkconfig --del ushare
alternatives --remove ushare %{_bindir}/ushare-fedora
fi

%postun
if [ $1 -ge 1 ]; then
	/sbin/service ushare condrestart &>/dev/null || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/ushare-fedora
%config(noreplace) %{_sysconfdir}/ushare.conf
%{_initrddir}/ushare
%attr(770,ushare,ushare) %dir %{_var}/lib/ushare/

%changelog
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1a-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Matěj Cepl <mcepl@redhat.com> - 1.1a-11
- Fix Summary (fix #593471)

* Sat Jul 30 2011 Matěj Cepl <mcepl@redhat.com> - 1.1a-9
- Rebuilt against new libraries.

* Wed Jul 06 2011 Adam Jackson <ajax@redhat.com> 1.1a-8
- 101-ushare-upnp-build-fix.patch: Fix build against newer libupnp (#715648)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1a-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1a-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Dave Jones <davej@redhat.com>
- Don't trash the ircd pid file when shutting down ushare.

* Sun Mar 09 2008 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.1a-4
- BZ 436605 & 436607

* Fri Jan 25 2008 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.1a-3
- Correct some spec error

* Tue Dec 25 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.1a-2
- Introduce use of alternatives

* Thu Dec 06 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.1a-1
- Update to 1.1a

* Wed Dec 05 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.1-1
- Update to 1.1

* Sun Nov 18 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.0-4
- Rebuild for new libupnp.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.0-2
- Rebuild for selinux ppc32 issue.

* Fri Jul 06 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 1.0-1
- Update to 1.0

* Tue Jun 26 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.10-4
- Rebuild

* Sat May 05 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.10-3
- Rebuild for libupnp-1.6.0

* Sat May 05 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.10-2
- Rebuild

* Mon Feb 26 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.10-1
- Update to 0.9.10

* Sun Feb 25 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.9-1
- Update to 0.9.9

* Sat Feb 17 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.8-2
- Rebuild for libupnp 1.4.2

* Wed Dec 13 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.8-1
- Update to 0.9.8

* Thu Jun 29 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.7-2
- Add pkgconfig to buildrequires

* Sun Mar 12 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.7-1
- Update to 0.9.7

* Tue Feb 14 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.6-1
- Update to 0.9.6

* Tue Feb 14 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.5-6
- Rebuild for FC5

* Fri Feb 10 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 0.9.5-5
- Rebuild for FC5

* Tue Dec 27 2005 Eric Tanguy 0.9.5-4
- Use %%find_lang macro instead of %%{_datadir}/locale/*

* Tue Dec 27 2005 Eric Tanguy 0.9.5-3
- Drop "Requires: libupnp"
- replace %%{_sysconfdir}/ushare.conf by %%config(noreplace) %%{_sysconfdir}/ushare.conf

* Tue Dec 27 2005 Eric Tanguy 0.9.5-2
- add patch for buffer

* Tue Dec 27 2005 Eric Tanguy 0.9.5-1
- First build
