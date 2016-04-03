%global maj 0
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:       suil
Version:    0.8.2
Release:    2%{?dist}
Summary:    A lightweight C library for loading and wrapping LV2 plugin UIs

Group:      System Environment/Libraries
License:    MIT 
URL:        http://drobilla.net/software/suil/
Source0:    http://download.drobilla.net/%{name}-%{version}.tar.bz2

BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  python
BuildRequires:  lv2-devel
# we need to track changess to these toolkits manually due to the 
# requires filtering below
BuildRequires:  gtk2-devel
BuildRequires:  qt4-devel

# lets not unecessarily pull in toolkits dependancies. They will be provided by 
# the host and or the plugin
%filter_from_requires /.*libatk.*/d
%filter_from_requires /.*libcairo.*/d
%filter_from_requires /.*libfont.*/d
%filter_from_requires /.*libfree.*/d
%filter_from_requires /.*libg.*/d
%filter_from_requires /.*libpango.*/d
%filter_from_requires /.*libQt.*/d
%filter_from_requires /.*libX*/d
%filter_setup

%description
%{name} makes it possible to load a UI of any toolkit in a host using any other 
toolkit (assuming the toolkits are both supported by %{name}). Hosts do not need
to build against or link to foreign toolkit libraries to use UIs written with 
that toolkit (%{name} performs its magic at runtime using dynamically 
loaded modules). 

%package devel
Summary:    Development libraries and headers for %{name}
Group:      Development/Libraries
Requires:   %{name}%{_isa} = %{version}-%{release}

%description devel
This package contains the headers and development libraries for %{name}.

%prep
%setup -q
# we'll run ldconfig, and add our optflags 
sed -i -e "s|bld.add_post_fun(autowaf.run_ldconfig)||" wscript

%build
export CXXFLAGS="%{optflags}"
./waf configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --docdir=%{_pkgdocdir} \
    --docs 
./waf build -v %{?_smp_mflags}

%install
DESTDIR=%{buildroot} ./waf install
chmod +x %{buildroot}%{_libdir}/lib%{name}-0.so.*
install -pm 644 AUTHORS COPYING NEWS README %{buildroot}%{_pkgdocdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_pkgdocdir}
%exclude %{_pkgdocdir}/%{name}-%{maj}
%dir %{_libdir}/suil-%{maj}
%{_libdir}/lib%{name}-*.so.*
%{_libdir}/suil-%{maj}/libsuil_gtk2_in_qt4.so
%{_libdir}/suil-%{maj}/libsuil_qt4_in_gtk2.so
%{_libdir}/suil-%{maj}/libsuil_x11_in_qt4.so
%{_libdir}/suil-%{maj}/libsuil_x11_in_gtk2.so

%files devel
%{_libdir}/lib%{name}-%{maj}.so
%{_libdir}/pkgconfig/%{name}-%{maj}.pc
%{_includedir}/%{name}-%{maj}/
%{_pkgdocdir}/%{name}-%{maj}
%{_mandir}/man3/%{name}.3.gz

%changelog
* Wed Aug 20 2014 Kevin Fenzi <kevin@scrye.com> - 0.8.2-2
- Rebuild for rpm bug 1131892

* Wed Aug 20 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.8.2-1
- Update to 0.8.2

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 11 2014 Brendan Jones <brendan.jones.it@gmail.com> 0.8.0-1
- Update to 0.8.0

* Mon Dec 16 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.6.16-2
- Install docs to %%{_pkgdocdir} where available (#994119).

* Mon Sep 23 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.6.16-1
- Update to 0.6.16 (minor Qt fix, NULL extension data)

* Sun Aug 25 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.6.14-1
- Update to version 0.6.14

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.6.12-1
- New upstream release

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 12 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.6.10-1
- New upstream

* Sat Dec 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.6.6-1
- New upstream

* Tue Jul 24 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.6.0-4
- Remove unwanted man file generated from doxygen

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.6.0-2
- New upstream release

* Sat Apr 07 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.4.4-6
- Add filter_from_requires macro to remove unwanted Gtk/Qt dependancies

* Fri Mar 30 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.4.4-5
- License change to MIT, adjust descriptions

* Wed Feb 22 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.4.4-4
- Split into Qt and GTK packages

* Mon Feb 06 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.4.4-3
- Correct directory ownsership and runtime library placement

* Wed Jan 25 2012 Brendan Jones <brendan.jones.it@gmail.com> - 0.4.4-2
- Correct build requires

* Fri Dec 23 2011 Brendan Jones <brendan.jones.it@gmail.com> - 0.4.4-1
- Initial build
