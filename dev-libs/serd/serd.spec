%global maj 0
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           serd
Version:        0.20.0
Release:        1%{?dist}
Summary:        A lightweight C library for RDF syntax

Group:          System Environment/Libraries
License:        ISC
URL:            http://drobilla.net/software/serd/
Source0:        http://download.drobilla.net/%{name}-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  glib2-devel
BuildRequires:  python

%description
%{name} is a lightweight C library for RDF syntax which supports reading and 
writing Turtle and NTriples.

Serd is not intended to be a swiss-army knife of RDF syntax, but rather is 
suited to resource limited or performance critical applications (e.g. 
converting many gigabytes of NTriples to Turtle), or situations where a 
simple reader/writer with minimal dependencies is ideal (e.g. in LV2 
implementations or embedded applications).is a library to make the use of 
LV2 plugins as simple as possible for applications. 

%package devel
Summary:        Development libraries and headers for %{name}
Group:          Development/Libraries
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
%{name} is a lightweight C library for RDF syntax which supports reading and 
writing Turtle and NTriples.

This package contains the headers and development libraries for %{name}.

%prep
%setup -q
# we'll run ldconfig
sed -i -e 's|bld.add_post_fun(autowaf.run_ldconfig)||' wscript

%build
export CFLAGS="%{optflags}"
./waf configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --datadir=%{_datadir} \
    --docdir=%{_pkgdocdir} \
    --test \
    --docs 
./waf build -v %{?_smp_mflags}

%install
DESTDIR=%{buildroot} ./waf install
chmod +x %{buildroot}%{_libdir}/lib%{name}-%{maj}.so.*
install -pm 644 AUTHORS COPYING NEWS README %{buildroot}%{_pkgdocdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%dir %{_pkgdocdir}/
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/COPYING
%{_pkgdocdir}/NEWS
%{_pkgdocdir}/README
%{_libdir}/lib%{name}-%{maj}.so.*
%{_bindir}/serdi
%{_mandir}/man1/serdi.1*

%files devel
%{_libdir}/lib%{name}-%{maj}*.so
%{_libdir}/pkgconfig/%{name}*.pc
%{_includedir}/%{name}-%{maj}/
%{_pkgdocdir}/%{name}-%{maj}/
%{_mandir}/man3/*.3*

%changelog
* Wed Aug 20 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.20.0-1
- Update to 0.20.0

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 14 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.18.2-3
- Install docs to %%{_pkgdocdir} where available (#994091).

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.18.2-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.18.0-1
- New upstream release

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.14.0-1
- New upstream release. 

* Sat Jan 14 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-3
- Move man1 file, furtherqualify wildcards. 

* Sat Jan 14 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-2
- License to ISC, remove tabs

* Fri Dec 23 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-1
- Initial build
