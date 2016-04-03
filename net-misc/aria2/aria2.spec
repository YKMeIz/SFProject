%define binname aria2c

Name:           aria2
Version:        1.21.0
Release:        1%{?dist}
Summary:        High speed download utility with resuming and segmented downloading
Group:          Applications/Internet
License:        GPLv2+ with exceptions
URL:            http://aria2.github.io/
Source0:        https://github.com/tatsuhiro-t/%{name}/releases/download/release-%{version}/%{name}-%{version}.tar.xz
BuildRequires:  bison
BuildRequires:  c-ares-devel cppunit-devel
BuildRequires:  gettext gnutls-devel
BuildRequires:  libgcrypt-devel libxml2-devel
BuildRequires:  sqlite-devel
BuildRequires:  gettext
# INFO: temp. workaround will be removed once merged
#BuildRequires:  autoconf gettext-devel automake libtool


%description
aria2 is a download utility with resuming and segmented downloading.
Supported protocols are HTTP/HTTPS/FTP/BitTorrent. It also supports Metalink
version 3.0.

Currently it has following features:
- HTTP/HTTPS GET support
- HTTP Proxy support
- HTTP BASIC authentication support
- HTTP Proxy authentication support
- FTP support(active, passive mode)
- FTP through HTTP proxy(GET command or tunneling)
- Segmented download
- Cookie support
- It can run as a daemon process.
- BitTorrent protocol support with fast extension.
- Selective download in multi-file torrent
- Metalink version 3.0 support(HTTP/FTP/BitTorrent).
- Limiting download/upload speed

%prep
%setup -q

%build
%configure CXX="g++ -std=c++11" \
           --enable-bittorrent \
           --enable-metalink \
           --enable-epoll\
           --disable-rpath \
           --with-gnutls \
           --with-libcares \
           --with-libxml2 \
           --without-openssl \
           --with-libz \
           --with-sqlite3 \
           --enable-gnutls-system-crypto-policy \


V=1 make %{?_smp_mflags}

%install
%make_install
%find_lang %{name}
rm -f $RPM_BUILD_ROOT%{_datadir}/locale/locale.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING README 
%{_bindir}/%{binname}
%{_mandir}/man1/aria2c.1.gz
%{_mandir}/*/man1/aria2c.1.gz

%changelog
* Thu Mar 17 2016 Athmane Madjoudj <athmane@fedoraproject.org> 1.21.0-1
- Update to 1.21.0
- Remove upstreamed patch

* Tue Feb 16 2016 Athmane Madjoudj <athmane@fedoraproject.org> 1.20.0-1
- Update to 1.20.0
- Rebase Use system wide crypto policies patch
- Fix configure options

* Sun Feb 14 2016 Athmane Madjoudj <athmane@fedoraproject.org> 1.19.3-4
- Use current ISO C++ name

* Sat Feb 13 2016 Athmane Madjoudj <athmane@fedoraproject.org> 1.19.3-3
- Fix build issue with GCC 6.0 (RHBZ #1307327)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Athmane Madjoudj <athmane@fedoraproject.org> 1.19.3-1
- Update to 1.19.3
- Fix Source and URL since upsteam moved to Github
- Rebase Use system wide crypto policies patch

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 24 2015 Athmane Madjoudj <athmane@fedoraproject.org> 1.19.0-1
- Update to 1.19.0

* Mon May 04 2015 Kalev Lember <kalevlember@gmail.com> - 1.18.10-4
- Rebuilt for nettle soname bump

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.18.10-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Athmane Madjoudj <athmane@fedoraproject.org> 1.18.10-2
- Add a patch to use system-wide crypto-policies (RHBZ #1179277)

* Fri Feb 27 2015 Athmane Madjoudj <athmane@fedoraproject.org> 1.18.10-1
- Update to 1.18.10 (RHBZ #1123979)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 13 2014 Rahul Sundaram <sundaram@fedoraproject.org> - 1.18.6-1
- update to 1.18.6

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 30 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.18.2-1
- upstream release 1.18.2 (rhbz#967784)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 02 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.17.0-1
- update to 1.17.0
- drop upstream build patch
- switch to verbose make
- switch to make_install macro

* Wed Mar  6 2013 Tomáš Mráz <tmraz@redhat.com> - 1.16.1-2
- rebuilt with new gnutls

* Fri Jan 25 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 1.16.1-1
- upstream release 1.16.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 21 2012 Tom Callaway <spot@fedoraproject.org> - 1.14.2-1
- update to 1.14.2
- fix compile issues with gcc 4.7

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.0-3
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.14.0-1
- update to 1.14.0
- https://github.com/tatsuhiro-t/aria2/blob/3dc6d2ff6df5a33f6abf47b4e792ea7dd578cf9a/NEWS

* Mon Aug 15 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.12.1-1
- https://github.com/tatsuhiro-t/aria2/commit/bd3956293995bcbbb76e6c8686b4ac8dfd3c9ed4#NEWS
- Additional man page

* Sun May 22 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.11.2-1
- https://github.com/tatsuhiro-t/aria2/commit/f6625f8dc5557e77fcace9bedaf1815c5eaf763f#NEWS
- Drop defattr since it is set by default in recent rpm

* Sun Apr 10 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.11.1-1
- https://github.com/tatsuhiro-t/aria2/blob/8d8fb31a45f66a29c78911293a60a00ac4903795/NEWS

* Tue Feb 22 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.10.9-1
- https://github.com/tatsuhiro-t/aria2/blob/6af3cd82b36190b12102bf3fbc5c07cc494627ad/NEWS

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.10.8-1
- https://github.com/tatsuhiro-t/aria2/blob/6af3cd82b36190b12102bf3fbc5c07cc494627ad/NEWS

* Sat Nov 27 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.10.6-1
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=2479

* Fri Jul 30 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.10.0-1
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=2279
- Dropped clean section

* Tue Jun 08 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.9.4-1
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=2133

* Sat Mar 20 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.9.0-1
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1990 

* Tue Feb 16 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 1.8.2-1
- Several bug fixes
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1860

* Mon Dec 28 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.8.0-1
- Many new features including XML RPC improvements and other bug fixes
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1778
 
* Mon Dec 07 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.7.1-1
- Option --bt-prioritize-piece=tail will work again
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1721

* Wed Nov 04 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.6.3-1
- Minor bug fixes
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1616

* Sat Oct 10 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.6.2-1
- Minor bug fixes and switch XZ compressed source 
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1586

* Thu Oct 08 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.6.1-1
- Fixes memory leak in HTTP/FTP downloads and other minor bug fixes
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1569

* Wed Sep 23 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.6.0-1
- Minor bug fixes
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1544

* Mon Aug 24 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5.2-1
- Minor bug fixes
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1504

* Mon Jul 27 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5.1-2
- update source

* Mon Jul 27 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5.1-1
- Minor bug fixes
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1494
- Fixed the license tag

* Sun Jul 26 2009 Rahul Sundaram <sundaram@fedoraproject.org> - 1.5.0-1
- Mostly minor bug fixes 
- WEB-Seeding support for multi-file torrent
- http://aria2.svn.sourceforge.net/viewvc/aria2/trunk/NEWS?revision=1476

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Robert Scheck <robert@fedoraproject.org> - 1.3.1-1
- Upgrade to 1.3.1

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 05 2008 Michał Bentkowski <mr.ecik at gmail.com> - 1.0.1-2
- New version, 1.0.1
- Forgot to add changelog in last release...

* Tue Jun 24 2008 Tomas Mraz <tmraz@redhat.com> - 0.12.0-5
- rebuild with new gnutls

* Fri Feb 22 2008 Michał Bentkowski <mr.ecik at gmail.com> - 0.12.0-4
- Add patch

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.12.0-3
- Autorebuild for GCC 4.3

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 0.12.0-2
- Get rid of odd locale.alias

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 0.12.0-1
- 0.12.0

* Thu Sep 20 2007 Michał Bentkowski <mr.ecik at gmail.com> - 0.11.3-1
- 0.11.3

* Fri Aug 24 2007 Michał Bentkowski <mr.ecik at gmail.com> - 0.11.2-1
- 0.11.2
- Fix License tag

* Mon Jul 09 2007 Michał Bentkowski <mr.ecik at gmail.com> - 0.11.1-1
- Update to 0.11.1

* Sat Apr 28 2007 Michał Bentkowski <mr.ecik at gmail.com> - 0.10.2+1-1
- Update to 0.10.2+1

* Tue Feb 20 2007 Michał Bentkowski <mr.ecik at gmail.com> - 0.10.1-1
- Update to 0.10.1

* Sun Dec 31 2006 Michał Bentkowski <mr.ecik at gmail.com> - 0.9.0-2
- Small fix in Summary

* Sat Dec 30 2006 Michał Bentkowski <mr.ecik at gmail.com> - 0.9.0-1
- Initial release
