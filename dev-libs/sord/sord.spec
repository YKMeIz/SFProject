%global maj 0
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:       sord
Version:    0.12.2
Release:    1%{?dist}
Summary:    A lightweight Resource Description Framework (RDF) C library

Group:      System Environment/Libraries
License:    ISC
URL:        http://drobilla.net/software/sord/
Source0:    http://download.drobilla.net/%{name}-%{version}.tar.bz2

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: graphviz
BuildRequires: glib2-devel
BuildRequires: python
BuildRequires: serd-devel >= 0.14.0

%description
%{name} is a lightweight C library for storing Resource Description
Framework (RDF) data in memory. %{name} and parent library serd form 
a lightweight RDF tool-set for resource limited or performance critical 
applications.

%package devel
Summary:    Development libraries and headers for %{name}
Group:      Development/Libraries
Requires:   %{name}%{_isa} = %{version}-%{release}

%description devel
%{name} is a lightweight C library for storing Resource Description
Framework (RDF) data in memory.

This package contains the headers and development libraries for %{name}.

%prep
%setup -q
# we'll run ldconfig, and add our optflags 
sed -i -e "s|bld.add_post_fun(autowaf.run_ldconfig)||" \
       -e "s|cflags          = [ '-DSORD_INTERNAL' ]\
|cflags          = [ '-DSORD_INTERNAL' ] + '%optflags'.split(' ') |" wscript

%build
export CXXFLAGS="%{optflags}"
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
install -pm 644 AUTHORS NEWS README COPYING %{buildroot}%{_pkgdocdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_pkgdocdir}
%exclude %{_pkgdocdir}/%{name}-%{maj}/
%{_libdir}/lib%{name}-%{maj}.so.*
%{_bindir}/sordi
%{_bindir}/sord_validate
%{_mandir}/man1/%{name}*.1*

%files devel
%{_pkgdocdir}/%{name}-%{maj}/
%{_libdir}/lib%{name}-%{maj}.so
%{_libdir}/pkgconfig/%{name}-%{maj}.pc
%{_includedir}/%{name}-%{maj}/
%{_mandir}/man3/%{name}*.3*

%changelog
* Wed Aug 20 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.12.2-1
- Update to 0.12.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.12.0-5
- Rebuild for boost 1.55.0

* Sun Dec 15 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.12.0-4
- Install docs to %%{_pkgdocdir} where available (#994099).
- Move *.1 manpages to main package.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.12.0-2
- Rebuild for boost 1.54.0

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.12.0-1
- New upstream release

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.10.4-2
- Rebuilt for serd

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.10.4-1
- New upstream release

* Tue Jul 24 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.8.0-2
- Remove unwanted man file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.8.0-1
- New upstream release

* Thu Jan 19 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-3
- Correct macros in description, expand summary.

* Mon Jan 16 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-2
- Correct macros in description, expand summary.

* Fri Dec 23 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.5.0-1
- Initial build
