Name:           wmweather+
Version:        2.15
Release:        2%{?dist}
Summary:        Weather status dockapp

Group:          User Interface/X
License:        GPLv2+
URL:            http://sourceforge.net/projects/wmweatherplus/
Source0:        http://dl.sf.net/wmweatherplus/%{name}-%{version}.tar.gz
Patch1:         wmweather+-Makefile.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequireS:  libXpm-devel
BuildRequires:  WINGs-devel
BuildRequires:  pcre-devel
BuildRequires:  w3c-libwww-devel
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  autoconf automake

%description
wmweather+ will download the National Weather Serivce METAR bulletins; AVN,
ETA, and MRF forecasts; and any weather map for display in a WindowMaker
dockapp. Think wmweather with a smaller font, forecasts, a weather map, and a
sky condition display.

%prep
%setup -q
%patch1

autoreconf -fv

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING README
%{_bindir}/wmweather+
%{_mandir}/man1/*

%changelog
* Wed Oct 15 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.15-2
- run autoreconf before configure for aclocal

* Tue Oct 14 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.15-1
- version upgrade

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.11-5
- Rebuild against PCRE 8.30
- wraster headers moved from WindowMaker-devel to WINGs-devel

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Mar 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.11-2
- add libcurl to BR

* Sun Mar 28 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.11-1
- fix FTBFS #564623
- version upgrade

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.9-12
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 2.9-9
- rebuild with new openssl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.9-8
- Autorebuild for GCC 4.3

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 2.9-7
- Rebuilt for gcc43

* Wed Dec 05 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.9-6
- bump

* Thu Aug 23 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.9-5
- new license tag
- rebuild for buildid

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9-4
- FE6 rebuild

* Thu Sep 15 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9-2
- add dist tag
- don't doc ChangeLog

* Fri Jun 03 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9-1
- Initial Release
