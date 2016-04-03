Name:		fsarchiver
Version:	0.6.19
Release:	3%{?dist}
Summary:	Safe and flexible file-system backup/deployment tool

Group:		Applications/Archiving
License:	GPLv2
URL:		http://www.fsarchiver.org
Source0:  	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz      
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	e2fsprogs-devel => 1.41.4
BuildRequires:	libuuid-devel
BuildRequires:	libblkid-devel
BuildRequires:	e2fsprogs
BuildRequires:	libattr-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
BuildRequires:	lzo-devel
BuildRequires:	xz-devel

%description
FSArchiver is a system tool that allows you to save the contents of a 
file-system to a compressed archive file. The file-system can be restored 
on a partition which has a different size and it can be restored on a 
different file-system. Unlike tar/dar, FSArchiver also creates the 
file-system when it extracts the data to partitions. Everything is 
checksummed in the archive in order to protect the data. If the archive 
is corrupt, you just lose the current file, not the whole archive.

%prep
%setup -q

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
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}*
%doc COPYING README THANKS NEWS

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 01 2014 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.19-1
- Update to 0.6.19
- Fixes regression introduced in 0.6.18

* Sat Feb 15 2014 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.18-1
- Update to 0.6.18
- Fixes RH#925370

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 27 2013 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.17-1
- Update to 0.6.17

* Fri Feb 08 2013 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.16-1
- Update to 0.6.16

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.15-1
- Update to 0.6.15

* Fri Mar 09 2012 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.13-1
- Update to 0.6.13

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 12 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.11-1
- Update to 0.6.11

* Sat May 15 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.10-1
- Update to 0.6.10

* Sat May 08 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.9-1
- Update to 0.6.9

* Sat Feb 20 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.8-1
- Update to 0.6.8

* Fri Feb 12 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.7-3
- Fix build

* Tue Feb 09 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.7-2
- Fix build

* Tue Feb 09 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.7-1
- Update to 0.6.7

* Fri Jan 08 2010 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.5-1
- Update to 0.6.5

* Mon Dec 28 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.3-1
- Update to 0.6.3

* Tue Dec 22 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.2-1
- Update to 0.6.2
- Apply fix as requested by upstream

* Sat Oct 10 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Sun Sep 27 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.6.0-1
- Update to 0.6.0
- Fixes licensing issue (no longer links against openssl)

* Thu Sep 03 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.9-1
- Update to 0.5.9

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.8-5
- rebuilt with new openssl

* Mon Aug 17 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.8-4
- Enable XZ support

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.8-2
- BR libblkid-devel

* Sun Jul 12 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.8-1
- Update to 0.5.8

* Tue May 19 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.6-1
- Update to 0.5.6

* Tue May 19 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.5-2
- BR e2fsprogs

* Tue May 19 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.5-1
- Update to 0.5.5

* Fri May 01 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.5.2-1
- Update to 0.5.2

* Sat Mar 28 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.4.6-1
- Update to 0.4.6

* Sun Mar 22 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.4.5-1
- Update to 0.4.5

* Sat Mar 07 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.4.4-2
- Fix file section
- Fix changelog

* Sat Mar 07 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.4.4-1
- Update to 0.4.4

* Sat Feb 28 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.4.3-1
- 0.4.3
- Drop build patch, no longer needed

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.4.1-2
- Fix description

* Thu Feb 12 2009 Adel Gadllah <adel.gadllah@gmail.com> - 0.4.1-1
- Initial package
