Name:          libtorrent
License:       GPLv2+
Group:         System Environment/Libraries
Version:       0.13.3
Release:       5%{?dist}
Summary:       BitTorrent library with a focus on high performance & good code
URL:           http://libtorrent.rakshasa.no/
Source0:       http://libtorrent.rakshasa.no/downloads/libtorrent-%{version}.tar.gz
Patch0:        libtorrent-aarch64.patch 
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig
BuildRequires: openssl-devel
BuildRequires: libsigc++20-devel

%description
LibTorrent is a BitTorrent library written in C++ for *nix, with a focus 
on high performance and good code. The library differentiates itself 
from other implementations by transfering directly from file pages to 
the network stack. On high-bandwidth connections it is able to seed at 
3 times the speed of the official client.

%package devel
Summary: Libtorrent development environment
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header and library definition files for developing applications                                               
with the libtorrent libraries.

%prep
%setup -q
%patch0 -p1 -b arch64

%build
%configure --with-posix-fallocate
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING INSTALL README
%{_libdir}/libtorrent.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/libtorrent.pc
%{_includedir}/torrent
%{_libdir}/*.so

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.13.3-4
- Bad patch name. Paste error

* Sat Mar 23 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.13.3-3
- Add patch to support ARM 64 support

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.13.3-1
- Update to latest upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.13.2-1
- Update to 0.13.2

* Tue Apr 03 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.13.1-1
- Update to 0.13.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 18 2011 Conrad Meyer <konrad@tylerc.org> - 0.13.0-1
- Bump to latest upstream release

* Sat Jul 2 2011 Conrad Meyer <konrad@tylerc.org> - 0.12.9-1
- Bump to latest upstream release

* Thu May 26 2011 Conrad Meyer <konrad@tylerc.org> - 0.12.8-1
- Bump to latest upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 27 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.12.7-1
- update to latest upstream release

* Fri Oct 15 2010 Michel Salim <salimma@fedoraproject.org> - 0.12.6-2
- Compile with support for pre-allocating files (# 466548)

* Tue Dec 15 2009 Conrad Meyer <konrad@tylerc.org> - 0.12.6-1
- Bump version.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.12.5-3
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 3 2009 Conrad Meyer <konrad@tylerc.org> - 0.12.5-1
- Bump version.

* Fri Feb 27 2009 Conrad Meyer <konrad@tylerc.org> - 0.12.4-4
- Fix FTBFS.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.12.4-2
- rebuild with new openssl

* Wed Nov 26 2008 Conrad Meyer <konrad@tylerc.org> - 0.12.4-1
- Bump to 0.12.4.

* Tue Nov 18 2008 Conrad Meyer <konrad@tylerc.org> - 0.12.3-1
- Bump to 0.12.3.

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.11.8-5
- fix license tag

* Sat Apr  5 2008 Christopher Aillon <caillon@redhat.com> - 0.11.8-4
- Add missing #includes so this compiles against GCC 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.11.8-3
- Autorebuild for GCC 4.3

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.11.8-2
- Rebuild for deps

* Tue Sep 18 2007 Marek Mahut <mmahut at fedoraproject dot org> - 0.11.8-1
- New upstream version

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.11.4-2
- Rebuild for selinux ppc32 issue.

* Thu Jun 28 2007 Chris Chabot <chabotc@xs4all.nl> - 0.11.4-1
- New upstream version

* Sun Nov 26 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.4-1
- New upstream version
- Compile with -Os to work around a gcc 4.1 incompatibility

* Mon Oct 02 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.2-3
- Bump EVR to fix broken upgrade path (BZ #208985)

* Fri Sep 29 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.2-1
- New upstream release

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-3
- FC6 rebuild, re-tag

* Mon Sep 11 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-2
- FC6 rebuild

* Sun Aug 13 2006 Chris Chabot <chabotc@xs4all.nl> - 0.10.0-1
- Upgrade to 0.10.0

* Sat Jun 17 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.9.3-1
- Upgrade to new upstream version 0.9.3

* Sat Jan 14 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.8.2-2
- Improved general summary & devel package description 
- Simplified devel package includedir files section
- Removed openssl as requires, its implied by .so dependency
- Correct devel package Group

* Wed Jan 11 2006 - Chris Chabot <chabotc@xs4all.nl> - 0.8.2-1
- Initial version
