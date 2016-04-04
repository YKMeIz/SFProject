Name:          rtorrent
# OpenSSL exception, see README
License:       GPLv2+ with exceptions
Group:         Applications/Internet
Version:       0.9.6
Release:       2%{?dist}
Summary:       BitTorrent client based on libtorrent 
URL:           http://rtorrent.rakshasa.no/
Source0:       http://libtorrent.rakshasa.no/downloads/rtorrent-%{version}.tar.gz
# see comments at patch below
Patch0:        rtorrent-0.9.3-makefile-am.patch
Patch1:        rtorrent-0.9.3-makefile-in.patch
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: curl-devel
BuildRequires: libstdc++-devel
BuildRequires: libsigc++20-devel
BuildRequires: libtorrent-devel >= 0.13.6
BuildRequires: ncurses-devel
BuildRequires: pkgconfig
BuildRequires: xmlrpc-c-devel

%description
A BitTorrent client using libtorrent, which on high-bandwidth connections is 
able to seed at 3 times the speed of the official client. Using
ncurses its ideal for use with screen or dtach. It supports 
saving of sessions and allows the user to add and remove torrents and scanning
of directories for torrent files to seed and/or download.

%prep
%setup -q
# http://libtorrent.rakshasa.no/ticket/2326
# http://libtorrent.rakshasa.no/ticket/2327
%patch0  -b .xmlrpcFTBFS1
%patch1  -b .xmlrpcFTBFS2

%build
%configure --with-xmlrpc-c
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# manually install the man page to correct location for this release
# install -p -m 0644 -D ./doc/rtorrent.1 $RPM_BUILD_ROOT/%{_mandir}/man1/rtorrent.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README doc/rtorrent.rc
%{_bindir}/rtorrent

%changelog
* Tue Sep 22 2015 Conrad Meyer <cemeyer@uw.edu> - 0.9.6-2
- Add explicit BR on libtorrent 0.13.6

* Sat Sep 19 2015 Conrad Meyer <cemeyer@uw.edu> - 0.9.6-1
- Bump to latest upstream release
- Drop now-broken AArch64 patch

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.4-4
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.4-1
- Update to latest upstream release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Mar 24 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.3-5
- Add patch for ARM 64 build support
- https://bugzilla.redhat.com/show_bug.cgi?id=926462

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.3-3
- Remove traces of man page from spec.

* Thu Oct 25 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.3-2
- Upstream removed man page. Removing from files

* Thu Oct 25 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.3-1
- Update to latest upstream release (#869534)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.2-1
- Update to 0.9.2

* Tue Apr 03 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.1-2
- Update patch

* Tue Apr 03 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.1-1
- Update to latest upstream release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Conrad Meyer <konrad@tylerc.org> - 0.9.0-1
- bump to latest upstream

* Sat Jul 2 2011 Conrad Meyer <konrad@tylerc.org> - 0.8.9-1
- bump to latest upstream

* Thu May 26 2011 Conrad Meyer <konrad@tylerc.org> - 0.8.8-1
- bump to latest upstream

* Sat Mar 5 2011 Conrad Meyer <konrad@tylerc.org> - 0.8.7-6
- Fix bad usage of ncurses

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Conrad Meyer <konrad@tylerc.org> - 0.8.7-4
- Adopt insecure SSL patch (as commandline option) (#669251)

* Thu Oct 28 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8.7-3
- manually install the man page to correct location

* Wed Oct 27 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8.7-2
- updated FTBFS patch for new version

* Wed Oct 27 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8.7-1
- Update to latest upstream release
- #646981

* Fri Oct 15 2010 Michel Salim <salimma@fedoraproject.org> - 0.8.6-4
- document fallocate option (# 466548)
- send patches upstream, link to bug reports in spec file

* Sun Feb 14 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8.6-3
- fix FTBFS

* Sun Feb 14 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.8.6-2
- add patch to add libxmlrpc for FTBFS fix 
- # 564688

* Tue Dec 15 2009 Conrad Meyer <konrad@tylerc.org> - 0.8.6-1
- Bump version.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 3 2009 Conrad Meyer <konrad@tylerc.org> - 0.8.5-1
- Bump version.

* Mon May 11 2009 Conrad Meyer <konrad@tylerc.org> - 0.8.4-4
- Use normal Fedora build flags.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 2 2008 Conrad Meyer <konrad@tylerc.org> - 0.8.4-2
- Add --with-xmlrpc-c to configure.

* Wed Nov 26 2008 Conrad Meyer <konrad@tylerc.org> - 0.8.4-1
- Bump to 0.8.4.

* Tue Nov 18 2008 Conrad Meyer <konrad@tylerc.org> - 0.8.3-1
- Bump version.

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.7.8-4
- fix license tag

* Sat Apr  5 2008 Christopher Aillon <caillon@redhat.com> - 0.7.8-3
- Fix build against newer sigc++
- Fix build against GCC 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.7.8-2
- Autorebuild for GCC 4.3

* Tue Sep 18 2007 Marek Mahut <mmahut fedoraproject.org> - 0.7.8-1
- New upstream release

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.7.4-3
- Rebuild for selinux ppc32 issue.

* Thu Jun 28 2007 Chris Chabot <chabotc@xs4all.nl> - 0.7.4-2
- Fixed BR

* Thu Jun 28 2007 Chris Chabot <chabotc@xs4all.nl> - 0.7.4-1
- New upstream release

* Sun Nov 26 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.4-1
- New upstream version
- Compile with -Os to work around a gcc 4.1 incompatibility

* Mon Nov 06 2006 Jindrich Novy <jnovy@redhat.com> - 0.6.2-5
- rebuild against new curl

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-4
- re-tag

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-3
- re-tag

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.2-2
- New upstream version

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.0-2
- FC6 rebuild

* Sun Aug 13 2006 Chris Chabot <chabotc@xs4all.nl> - 0.6.0-1
- Upgrade to 0.6.0

* Sat Jun 17 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.5.3-1
- Upgrade to new upstream version 0.5.3
- And changed libtorrent dependency to >= 0.9.3

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-3
- Added ncurses-devel to buildrequirements

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-2
- Improved summary & description
- Removed explicit requires, leaving to rpm
- Changed mode of rtorrent.rc.example to 644

* Wed Jan 11 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.4.2-1
- Initial version
