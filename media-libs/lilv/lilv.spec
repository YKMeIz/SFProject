%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global maj 0

Name:       lilv
Version:    0.20.0
Release:    2%{?dist}
Summary:    An LV2 Resource Description Framework Library

Group:      System Environment/Libraries
License:    MIT
URL:        http://drobilla.net/software/lilv/
Source0:    http://download.drobilla.net/%{name}-%{version}.tar.bz2
Patch1:     lilv-0.16.0-gcc.patch
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  sord-devel >= 0.12.0
BuildRequires:  sratom-devel >= 0.4.4
BuildRequires:  lv2-devel >= 1.8.0
BuildRequires:  python2-devel
BuildRequires:  swig
BuildRequires:  numpy

%filter_setup

%description
%{name} is a library to make the use of LV2 plugins as simple as possible 
for applications. Lilv is the successor to SLV2, rewritten to be significantly 
faster and have minimal dependencies. 

%package devel
Summary:    Development libraries and headers for %{name}
Group:      Development/Libraries
Requires:   %{name}%{_isa} = %{version}-%{release}

%description devel
%{name} is a lightweight C library for Resource Description Syntax which 
supports reading and writing Turtle and NTriples.

This package contains the headers and development libraries for %{name}.

%package -n python-%{name}
Summary:    Python bindings for %{name}
Group:      Development/Libraries
Requires:   %{name}%{_isa} = %{version}-%{release}

%description -n python-%{name} 
%{name} is a lightweight C library for Resource Description Syntax which 
supports reading and writing Turtle and NTriples.

This package contains the python libraries for %{name}.

%prep
%setup -q 
%patch1 -p1 
# we'll run ld config
sed -i -e 's|bld.add_post_fun(autowaf.run_ldconfig)||' wscript
# for packagers sake, build the tests with debug symbols
sed -i -e "s|'-ftest-coverage'\]|\
 '-ftest-coverage' \] + '%{optflags}'.split(' ')|" wscript

%build
export CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
./waf configure -v --prefix=%{_prefix}\
 --libdir=%{_libdir} --configdir=%{_sysconfdir} --mandir=%{_mandir}\
 --docdir=%{_pkgdocdir}\
 --docs --test --dyn-manifest --bindings 
./waf -v build %{?_smp_mflags}

%install
./waf -v install --destdir=%{buildroot} 
chmod +x %{buildroot}%{_libdir}/lib%{name}-0.so.*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%check
./build/test/lilv_test

%files
%doc AUTHORS NEWS README COPYING
%exclude %{_pkgdocdir}/%{name}-%{maj}/
%{_libdir}/lib%{name}-%{maj}.so.*
%{_bindir}/lilv-bench
%{_bindir}/lv2info
%{_bindir}/lv2ls
%{_bindir}/lv2bench
%dir %{_sysconfdir}/bash_completion.d/
%{_sysconfdir}/bash_completion.d/lilv
%{_mandir}/man1/*

%files devel
%{_libdir}/lib%{name}-%{maj}.so
%{_libdir}/pkgconfig/%{name}-%{maj}.pc
%{_includedir}/%{name}-%{maj}/
%{_pkgdocdir}/%{name}-%{maj}/
%{_mandir}/man3/*

%files -n python-%{name}
%{python_sitelib}/%{name}.*
%{python_sitearch}/_%{name}.so

%changelog
* Sat Aug 23 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.20.0-2
- Build against new version of sratom / sord

* Wed Aug 20 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.20.0-1
- Update to 0.20.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 11 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.18.0-2
- Add numpy BR

* Fri Jan 10 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.18.0-1
- New upstream release

* Thu Nov 28 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.16.0-3
- Install docs to (main, not devel) %%{_pkgdocdir} where available (#993969).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.16.0-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.14.4-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 05 2012 Karsten Hopp <karsten@redhat.com> 0.14.2-3
- bump release and rebuild, lilv was missing some deps on PPC*

* Sat May 12 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.2-2
- Corrected waf configure
 
* Sat May 12 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.2-1
- New upstream 0.14.2
 
* Sat May 12 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.0-2
- Add python binding BR
 
* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.0-1
- New upstream release 0.14.0
 
* Wed Feb 29 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-3
- Remove redundant build requires, merge python bindings
- Move man3 pages to devel package
- Apply patch to correct scale points iteration in test suite

* Sun Feb 26 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-2
- Add python bindings, and missing build requires
- Move man pages to main package

* Fri Dec 23 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-1
- Initial build
