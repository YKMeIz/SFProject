Name:		fuse-s3fs
Version:	0.9
Release:	6%{?dist}
Summary:	FUSE filesystem using Amazon Simple Storage Service as storage
Group:		System Environment/Base
License:	GPLv2
URL:		https://fedorahosted.org/s3fs
Source0:	https://fedorahosted.org/releases/s/3/s3fs/%{name}-%{version}.tbz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	python fuse-python python-boto
BuildArch:	noarch


%description
This package provides a FUSE (Filesystem in User Space) application allowing
for the mounting of Amazon Web Services' S3 storage facilities on a local
system.
WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
This package has undergone some minimal testing and is deemed to be
safe to store data on.  However, this is the first instance in which this
project has been placed into wide circulation.  As such, until this package
develops some extra maturity from more widespread use, it is recommended that
data stored on fuse-s3fs be backed up on other media as well.

%prep
%setup -q

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/share/man/man1

install -m755 -p src/s3fs $RPM_BUILD_ROOT/usr/bin/s3fs
install -m644 -p doc/s3fs.1 $RPM_BUILD_ROOT/usr/share/man/man1/s3fs.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 20 2011 Neil Horman <nhorman@redhat.com> - 0.9-1
- Updated to latest updstream release

* Wed Aug 24 2011 Neil Horman <nhorman@redhat.com> - 0.8-1
- Updated to latest upstream version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.7-4
- Rebuilt with new fuse

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 06 2008 Neil Horman <nhorman@tuxdriver.com> 0.7-1
- Update to upstream (fixing potential zero size file error)

* Fri May 30 2008 Neil Horman <nhorman@tuxdriver.com> 0.6-1
- Updated s3fs to upstream version 0.6

* Fri May 16 2008 Neil Horman <nhorman@tuxdriver.com> 0.5-1
- Updated s3fs to upstream version 0.5

* Thu Apr 24 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-9
- Backport noargs abort patch (bz 443965)

* Sat Apr 05 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-9
- Fix ftruncate to set proper length

* Mon Mar 17 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-8
- Adding -p to install to preserve time stamps
- Adjusted Makefile targets a bit
- Fixed up BuildRequires

* Mon Mar 17 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-7
- Makefile cleanups

* Thu Mar 13 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-6
- Fixing more silly nits 

* Wed Mar 12 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-5
- Further review updates for bz 435155

* Tue Mar 11 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-4
- Fixing spec file problems as per bz 435155

* Tue Mar 11 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-3
- Adding options for key specification and man page cleanups

* Mon Mar 10 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-2
- Bumping rev for spec file rename

* Wed Feb 27 2008 Neil Horman <nhorman@tuxdriver.com> 0.4-1
- Initial build
