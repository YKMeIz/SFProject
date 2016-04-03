Name:           tarsnap
Version:        1.0.35
Release:        1%{?dist}
Summary:        Online encrypted backup service (client)

Group:          Applications/Archiving
# The following files are BSD licensed:
#  - libarchive/*
#  - lib/crypto/crypto_aesctr.*
#  - lib/crypto/crypto_scrypt.*
#  - lib/crypto/sha256.*
#  - lib/util/memlimit.*
#  - lib/util/readpass.*
#  - lib/util/sysendian.h
#  - lib/scryptenc/*
#  - tar/config_freebsd.h
#  - tar/siginfo.c
#  - tar/subst.c
# Portions of the following files are BSD licensed
# (the original BSD licensed code is in libarchive):
#  - tar/bsdtar*
#  - tar/cmdline.c
#  - tar/matching.c
#  - tar/read.c
#  - tar/tree.*
#  - tar/util.c
#  - tar/write.c
# The following file is in the public domain:
#  - tar/getdate.c
License:        Tarsnap License and BSD and Public Domain
URL:            https://www.tarsnap.com/
Source0:        https://www.tarsnap.com/download/%{name}-autoconf-%{version}.tgz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  xz-devel
BuildRequires:  e2fsprogs-devel

Provides:       bundled(libarchive) = 2.7.0

%description
Tarsnap is an online encrypted backup service.  It presents a tar-like
command-line interface, but stores data online rather than locally;
using ideas taken from the author's FreeBSD Update and Portsnap
utilities, it maximizes performance by recognizing duplicate data and
only storing it once, and cryptographically encrypts and signs archives
using locally-held keys in order to guarantee that nobody without access
to the key file (including the author) can read or modify archives.


%prep
%setup -q -n %{name}-autoconf-%{version}


%build
%configure
%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING
%config %{_sysconfdir}/tarsnap.conf.sample
%{_bindir}/tarsnap*
%{_mandir}/man*/tarsnap*

%changelog
* Thu Aug 14 2014 Nux <rpm@li.nux.ro> - 1.0.35-1
- update to 1.0.35

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.32-2
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jun 24 2012 Ricky Zhou <ricky@fedoraproject.org> - 1.0.32-1
- Upstream released a new version.

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Ricky Zhou <ricky@fedoraproject.org> - 1.0.31-1
- Upstream released a new version.

* Wed Aug 25 2011 Ricky Zhou <ricky@fedoraproject.org> - 1.0.30-1
- Upstream released a new version.

* Tue Feb 08 2011 Ricky Zhou <ricky@fedoraproject.org> - 1.0.29-1
- Upstream released a new version.

* Tue Jan 18 2011 Ricky Zhou <ricky@fedoraproject.org> - 1.0.28-1
- Upstream released a new version.
- Fixes critical security bug in data encryption code.

* Fri Dec 04 2010 Ricky Zhou <ricky@fedoraproject.org> - 1.0.27-1
- Initial package.
