%global git_user bwalex
%global git_project tc-play
#%global git_date 20130629
#%global git_hash b44b1fa

Name:           tcplay
Version:        2.0
#Release:       0.2.%{git_date}git%{git_hash}%{?dist}
Release:        6%{?dist}
Summary:        Utility to create/open/map TrueCrypt-compatible volumes
Group:          Applications/System
License:        BSD
URL:            https://github.com/%{git_user}/%{git_project}
#Source0:       https://github.com/%{git_user}/%{git_project}/tarball/%{git_hash}/%{git_project}-%{git_hash}.tar.gz
Source0:        https://github.com/%{git_user}/%{git_project}/archive/v%{version}.tar.gz


BuildRequires:  cmake
BuildRequires:  device-mapper-devel libgcrypt-devel libuuid-devel
BuildRequires:  openssl-devel

%description
The tcplay utility provides full support for creating and opening/mapping
TrueCrypt-compatible volumes.

%package        lib
Summary:        Library to create/open/map TrueCrypt-compatible volumes
Group:          System Environment/Libraries

%description    lib
The libtcplay library provides an API for creating and opening/mapping
TrueCrypt-compatible volumes.

%post lib -p /sbin/ldconfig
%postun lib -p /sbin/ldconfig

%package        devel
Summary:        Development files for libtcplay
Group:          Development/Libraries
Requires:       %{name}-lib%{?_isa} = %{version}-%{release}

%description    devel
Files necessary to develop applications that use the libtcplay.

%prep
#%setup -q -n %{git_user}-%{git_project}-%{git_hash}
%setup -q -n %{git_project}-%{version}

%build
%{cmake}
make %{?_smp_mflags} CFLAGS="%{optflags}"

%install
install -d -m 755 %{buildroot}%{_bindir}
install -p -m 755 %{name} %{buildroot}%{_bindir}

install -d -m 755 %{buildroot}%{_mandir}/man8
install -p -m 644 %{name}.8 %{buildroot}%{_mandir}/man8

install -d -m 755 %{buildroot}%{_libdir}
install -p -m 755 libtcplay.so.2.0 %{buildroot}%{_libdir}
ln -s libtcplay.so.2.0 %{buildroot}%{_libdir}/libtcplay.so.2
ln -s libtcplay.so.2.0 %{buildroot}%{_libdir}/libtcplay.so

install -d -m 755 %{buildroot}%{_includedir}
install -p -m 644 tcplay_api.h %{buildroot}%{_includedir}

%files
%doc README.md LICENSE CHANGELOG
%{_bindir}/%{name}
%{_mandir}/man8/%{name}.8*

%files lib
%doc README.md LICENSE CHANGELOG
%{_libdir}/libtcplay.so.2.0
%{_libdir}/libtcplay.so.2

%files devel
%{_includedir}/tcplay_api.h
%{_libdir}/libtcplay.so

%changelog
* Fri Feb 06 2015 Nux <rpm@li.nux.ro> - 2.0-6
- removed rhel cmake28 conditionals, not needed on EL7

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Eric Smith <brouhaha@fedoraproject.org> - 2.0-3
- Fix dependency on lib subpackage (typo).

* Sat Apr 19 2014 Eric Smith <brouhaha@fedoraproject.org> - 2.0-2
- Package libtcplay.

* Sun Apr 06 2014 Eric Smith <brouhaha@fedoraproject.org> - 2.0-1
- Updated to latest upstream release.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-0.2.20130629gitb44b1fa
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Eric Smith <brouhaha@fedoraproject.org> - 1.1-0.1.20130629gitb44b1fa
- Updated to latest upstream snapshot.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-0.7.20111007git97ed5f9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-0.6.20111007git97ed5f9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-0.5.20111007git97ed5f9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 08 2011 Eric Smith <eric@brouhaha.com> - 0.9-0.4.20111007git97ed5f9
- Removed more outdated items from spec, not intending to support RHEL5 or
  earlier.

* Thu Oct 06 2011 Eric Smith <eric@brouhaha.com> - 0.9-0.3.20111007git97ed5f9
- updated to new upstream snapshot

* Thu Oct 06 2011 Eric Smith <eric@brouhaha.com> - 0.9-0.2.20111004git59c6097
- updated based on package review comments, bug 743497

* Tue Oct 04 2011 Eric Smith <eric@brouhaha.com> - 0.9-0.1.20111004git59c6097
- initial version
