%define req_pcap_devel %(eval [ -e /usr/include/pcap.h -o -e /usr/include/pcap/pcap.h ] && echo 0 || echo 1 )

Summary: Knock is a port-knocking server/client
Name: knock
Version: 0.5
Release: 7%{?dist}
License: GPLv2+
Group: System Environment/Daemons
URL: http://www.zeroflux.org/projects/%{name}
Packager: Simon Matter <simon.matter@invoca.ch>
Vendor: Invoca Systems
Distribution: Invoca Linux Server
Source0: http://www.zeroflux.org/proj/knock/files/%{name}-%{version}.tar.gz
Source1: %{name}d.sysconfig
Source2: %{name}d.init
Source3: %{name}d.conf
Patch0: knock-0.5-syslog.patch
Patch1: knock-0.5-limits.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libpcap
%if %{req_pcap_devel}
BuildRequires: libpcap-devel
%endif

%description
Knock is a port-knocking server/client.  Port-knocking is a method where a
server can sniff one of its interfaces for a special "knock" sequence of
port-hits.  When detected, it will run a specified event bound to that port
knock sequence.  These port-hits need not be on open ports, since we use
libpcap to sniff the raw interface traffic. This package contains the
knock client.

%package server
Group: System Environment/Daemons
Summary: Knock is a port-knocking server/client
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
                                                                                                                         
%description server
Knock is a port-knocking server/client.  Port-knocking is a method where a
server can sniff one of its interfaces for a special "knock" sequence of
port-hits.  When detected, it will run a specified event bound to that port
knock sequence.  These port-hits need not be on open ports, since we use
libpcap to sniff the raw interface traffic. This package contains the
knockd server.

%prep
%setup -q
%patch0 -p1 -b .syslog
%patch1 -p1 -b .limits

%build
# this is a problem of RedHat 6.2
export CFLAGS="%{optflags} -I%{_includedir}/pcap"
%{configure}
%{__make}

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%{__make} install DESTDIR=%{buildroot} INSTALL="install -p"
%{__install} -d %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -d %{buildroot}%{_initrddir}

%{__install} -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}d
%{__install} -m 0755 -p %{SOURCE2} %{buildroot}%{_initrddir}/%{name}d
%{__install} -m 0600 -p %{SOURCE3} %{buildroot}%{_sysconfdir}/

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%post server
/sbin/chkconfig --add %{name}d

%preun server
if [ $1 = 0 ]; then
  /sbin/service %{name}d stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del %{name}d
fi

%postun server
if [ "$1" -ge "1" ]; then
  /sbin/service %{name}d condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/%{name}
%{_mandir}/man?/%{name}.*

%files server
%defattr(-,root,root)
%doc README COPYING ChangeLog TODO
%attr(0755,root,root) %{_sbindir}/%{name}d
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}d.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}d
%attr(0755,root,root) %config %{_initrddir}/%{name}d
%{_mandir}/man?/%{name}d.*

%changelog
* Fri Apr 15 2011 Simon Matter <simon.matter@invoca.ch> 0.5-7
- mass rebuild

* Thu Aug 20 2009 Simon Matter <simon.matter@invoca.ch> 0.5-6
- change license tag to GPLv2+
- fix URL's
- fix CFLAGS
- cosmetic spec file changes

* Thu Aug 20 2009 Nik Conwell <nik@bu.edu> - 0.5-5
- Include limits.h in list.h to get to build on Fedora 11.
- Fix from datatek on forums.fedoraforum.org.

* Fri May 25 2007 Simon Matter <simon.matter@invoca.ch> 0.5-4
- autodetect whether libpcap-devel is required
- change to new pre/post-requires style

* Thu Mar 02 2006 Simon Matter <simon.matter@invoca.ch> 0.5-3
- add patch to change syslog facility to authpriv

* Tue Sep 06 2005 Simon Matter <simon.matter@invoca.ch> 0.5-2
- add libpcap to build requirements

* Mon Jul 18 2005 Simon Matter <simon.matter@invoca.ch>
- updated to version 0.5

* Wed Jan 12 2005 Simon Matter <simon.matter@invoca.ch>
- updated to version 0.4

* Wed Sep 15 2004 Simon Matter <simon.matter@invoca.ch>
- updated to version 0.3.1

* Wed Aug 04 2004 Simon Matter <simon.matter@invoca.ch>
- fixed pcap patch
- fixed build issue on Fedora Core

* Wed May 19 2004 Simon Matter <simon.matter@invoca.ch>
- updated to version 0.3

* Fri Apr 16 2004 Simon Matter <simon.matter@invoca.ch>
- updated to version 0.2.1

* Thu Apr 15 2004 Simon Matter <simon.matter@invoca.ch>
- splitted package into client and server part
- fixed build on RedHat 6.2
- updated to version 0.2

* Wed Apr 14 2004 Simon Matter <simon.matter@invoca.ch>
- initial build
