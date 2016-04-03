Summary: glibc plugin for .local name resolution
Name: nss-mdns
Version: 0.10
Release: 12%{?dist}
License: LGPLv2+
URL: http://0pointer.de/lennart/projects/nss-mdns/
Group: System Environment/Libraries
Source: http://0pointer.de/lennart/projects/nss-mdns/nss-mdns-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: avahi
 
%description
nss-mdns is a plugin for the GNU Name Service Switch (NSS) functionality of
the GNU C Library (glibc) providing host name resolution via Multicast DNS
(aka Zeroconf, aka Apple Rendezvous, aka Apple Bonjour), effectively allowing 
name resolution by common Unix/Linux programs in the ad-hoc mDNS domain .local.

nss-mdns provides client functionality only, which means that you have to
run a mDNS responder daemon separately from nss-mdns if you want to register
the local host name via mDNS (e.g. Avahi).

%prep
%setup -q

%build
%configure --libdir=/%{_lib} --enable-avahi=yes --enable-legacy=no
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# Perl-fu to add mdns4_minimal to the hosts line of /etc/nsswitch.conf
if [ -f /etc/nsswitch.conf ] ; then
	sed -i.bak '
		/^hosts:/ !b
		/\<mdns\(4\|6\)\?\(_minimal\)\?\>/ b
		s/\([[:blank:]]\+\)dns\>/\1mdns4_minimal [NOTFOUND=return] dns/g
		' /etc/nsswitch.conf
fi

%preun
# sed-fu to remove mdns4_minimal from the hosts line of /etc/nsswitch.conf
if [ "$1" -eq 0 -a -f /etc/nsswitch.conf ] ; then
	sed -i.bak '
		/^hosts:/ !b
		s/[[:blank:]]\+mdns\(4\|6\)\?\(_minimal\( \[NOTFOUND=return\]\)\?\)\?//g
	' /etc/nsswitch.conf
fi

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README
/%{_lib}/*

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 30 2008 Stepan Kasal <skasal@redhat.com> - 0.10-6
- use sed instead of perl in %%post and %%preun (#462996),
  fixing two bugs in the scriptlets:
  1) the backup file shall be nsswitch.conf.bak, not nsswitch.confbak
  2) the first element after host: shall be subject to removal, too
- consequently, removed the Requires(..): perl
- removed the reqires for things that are granted
- a better BuildRoot

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.10-5
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.10-4
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.10-3
- Rebuild for selinux ppc32 issue.

* Fri Jun 22 2007 - Lennart Poettering <lpoetter@redhat.com> - 0.10-2
- Fix up post/preun/postun dependencies, add "avahi" to the dependencies, 
  include dist tag in Release field, use _lib directory instead of literal /lib.

* Fri Jun 22 2007 - Lennart Poettering <lpoetter@redhat.com> - 0.10-1
- Update to 0.10, replace perl script by simpler and more robust versions,
  stolen from the Debian package

* Thu Jul 13 2006 - Bastien Nocera <hadess@hadess.net> - 0.8-2
- Make use of Ezio's perl scripts to enable and disable mdns4 lookups
  automatically, patch from Pancrazio `Ezio' de Mauro <pdemauro@redhat.com>

* Tue May 02 2006 - Bastien Nocera <hadess@hadess.net> - 0.8-1
- Update to 0.8, disable legacy lookups so that all lookups are made through
  the Avahi daemon

* Mon Apr 24 2006 - Bastien Nocera <hadess@hadess.net> - 0.7-2
- Fix building on 64-bit platforms

* Tue Dec 13 2005 - Bastien Nocera <hadess@hadess.net> - 0.7-1
- Update to 0.7, fix some rpmlint errors

* Thu Nov 10 2005 - Bastien Nocera <hadess@hadess.net> - 0.6-1
- Update to 0.6

* Tue Dec 07 2004 - Bastien Nocera <hadess@hadess.net> 0.1-1
- Initial package, automatically adds and remove mdns4 as a hosts service

