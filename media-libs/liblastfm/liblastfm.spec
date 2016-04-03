
## build/include liblastfm_fingerprint
%define fingerprint 1

# see http://fedoraproject.org/wiki/Packaging:SourceURL#Github
%global commit 0875757fe8c253b67710d6c1f3700ed140a4a7ba
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:	 liblastfm
Summary: Libraries to integrate Last.fm services
Version: 1.0.8
Release: 2%{?dist}

License: GPLv2+
URL:     https://github.com/lastfm/liblastfm
# https://github.com/lastfm/liblastfm/archive/%{version}.tar.gz
#Source0: liblastfm-%{version}.tar.gz
Source0:  https://github.com/lastfm/liblastfm/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz

%if "%{rhel}" == "6"
BuildRequires: cmake28 >= 2.8.6
%global cmake_cmd %{cmake28}
%else
BuildRequires: cmake >= 2.8.6
%global cmake_cmd %{cmake}
%endif
BuildRequires: pkgconfig(QtNetwork) pkgconfig(QtSql) pkgconfig(QtXml)
BuildRequires: ruby

%description
Liblastfm is a collection of libraries to help you integrate Last.fm services
into your rich desktop software.

%if 0%{?fingerprint}
%package fingerprint
Summary: Liblastfm fingerprint library
BuildRequires: fftw3-devel
BuildRequires: pkgconfig(samplerate)
Requires: %{name}%{?_isa} = %{version}-%{release}
%description fingerprint
%{summary}.
%endif

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fingerprint}
Requires: %{name}-fingerprint%{?_isa} = %{version}-%{release}
%endif
%description devel
%{summary}.


%prep
%setup -qn %{name}-%{commit}


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_cmd} \
  -DBUILD_FINGERPRINT:BOOL=%{?fingerprint:ON}%{!?fingerprint:OFF} \
  -DBUILD_WITH_QT4:BOOL=ON \
  ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%check
# TODO: not all tests pass, ping upstream
make test -C %{_target_platform} ||:


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%doc README.md
%{_libdir}/liblastfm.so.1*

%if 0%{?fingerprint}
%post fingerprint -p /sbin/ldconfig
%postun fingerprint -p /sbin/ldconfig

%files fingerprint
%{_libdir}/liblastfm_fingerprint.so.1*
%endif

%files devel
%{_libdir}/liblastfm*.so
%{_includedir}/lastfm/


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Rex Dieter <rdieter@fedoraproject.org> 1.0.8-1
- liblastfm-1.0.8 (#1090909)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Rex Dieter <rdieter@fedoraproject.org> 1.0.7-1
- liblastfm-1.0.7

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Rex Dieter <rdieter@fedoraproject.org> 
- 1.0.3-1
- liblastfm-1.0.3
- include fingerprint support

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Rex Dieter <rdieter@fedoraproject.org> 1.0.1-1
- liblastfm-1.0.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-5
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.3.3-2
- Rebuilt for gcc bug 634757

* Sat Sep 25 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.3-1
- liblastfm-0.3.3
- missing symbols in liblastfm-0.3.2 (#636729)

* Fri Sep 17 2010 Rex Dieter <rdieter@fedoraproject.org> 0.3.2-1
- liblastfm-0.3.2

* Tue Jun 30 2009 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-2
- rpmlint clean(er)
- BR: libsamplerate-devel
- -devel: fix Requires (typo, +%%?_isa)

* Tue Jun 09 2009 Rex Dieter <rdieter@fedoraproject.org> 0.3.0-1
- liblastfm-0.3.0

* Tue May 05 2009 Rex Dieter <rdieter@fedoraproject.org> 0.2.1-1
- liblastfm-0.2.1, first try
