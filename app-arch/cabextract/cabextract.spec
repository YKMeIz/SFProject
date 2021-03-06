Name:           cabextract
Version:        1.4
Release:        5%{?dist}
Summary:        Utility for extracting cabinet (.cab) archives

Group:          Applications/Archiving
License:        GPLv2+
URL:            http://www.cabextract.org.uk/
Source:         http://www.cabextract.org.uk/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libmspack-devel


%description
cabextract is a program which can extract files from cabinet (.cab)
archives.


%prep
%setup -q


%build
%configure --with-external-libmspack

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/cabextract
%{_mandir}/man1/cabextract.1*


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 16 2011 Dan Horák <dan[at]danny.cz> - 1.4-1
- updated to 1.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.3-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Dan Horák <dan[at]danny.cz> - 1.3-1
- updated to 1.3
- built with system copy of libmspack (CVE-2010-2800 CVE-2010-2801)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Patrice Dumas <pertusus@free.fr> - 1.2-1
- update to 1.2

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1-8
- respin (gcc43)
- cosmetics

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.1-7
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.1-6
- License: GPLv2+

* Tue Aug 29 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1-5
- Rebuild.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.1-4
- Rebuild.

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.1-3
- Fix FC4 build.

* Wed Nov 10 2004 Matthias Saou <http://freshrpms.net/> 1.1-2
- Update to 1.1.
- Bump release to provide Extras upgrade path.

* Sat Mar 27 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:1.0-0.fdr.1
- Updated to 1.0.
- Added COPYING and TODO to documentation.
- Converted spec file to UTF-8.

* Sat May 31 2003 Warren Togami <warren@togami.com> 0:0.6-0.fdr.2
- Remove redundant %%doc

* Thu May 29 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> 0:0.6-0.fdr.1
- Initial Fedora RPM release.
