%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define major_version 0.14

Name:           pygoocanvas
Version:        0.14.1
Release:        9%{?dist}
Summary:        GooCanvas python bindings

Group:          Development/Languages
License:        LGPLv2+
URL:            http://live.gnome.org/PyGoocanvas
Source0:        ftp://ftp.gnome.org/pub/GNOME/sources/pygoocanvas/%{name}/%{major_version}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel, pkgconfig, pygobject2-devel
BuildRequires:  pycairo-devel >= 1.8.4, pygtk2-devel >= 2.10.0
BuildRequires:  goocanvas-devel >= %{major_version}, gtk2-devel
BuildRequires:  libxslt, docbook-style-xsl

Requires:       goocanvas >= %{major_version}

%description
GooCanvas python bindings.


%prep
%setup -q

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
 
# remove libtool droppings
rm -f $RPM_BUILD_ROOT/%{python_sitearch}/*\.la

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{python_sitearch}/*

%package devel
Group:          Development/Languages
Summary:        GooCanvas python bindings development files
Requires:       goocanvas >= %{major_version}, %{name} = %{version}-%{release}, pkgconfig

%description devel
GooCanvas python bindings development files.

%files devel
%defattr(-,root,root,-)
%doc docs demo
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gtk-doc/html/%{name}

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.14.1-5
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Apr 24 2010 Haïkel guémar <hguemar@fedoraproject.org> - 0.15.1-2
- Rebuilt against newer goocanvas
- Add documentation and demo into *-devel sub-package

* Sun Nov 22 2009 Bernard Johnson <bjohnson@symetrix.com> - 0.14.1-1
- v 0.14.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Bernard Johnson <bjohnson@symetrix.com> - 0.14.0-2
- add patch to fix upstream API breakage (bz #511658)

* Thu Jun 25 2009 Denis Leroy <denis@poolshark.org> - 0.14.0-1
- Update to upstream 0.14.0, as part of general goocanvas update

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Denis Leroy <denis@poolshark.org> - 0.13.1-1
- Update to 0.13.1
- Updated URLs to gnome.org

* Sun Dec 21 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.10.0-4
- break into main and -devel packages

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.10.0-3
- Rebuild for Python 2.6

* Wed Jul 02 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.10.0-2
- package package config file (.pc) into package (don't want separate devel)

* Sun Jun 29 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.10.0-1
- v 0.10.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.0-3
- Autorebuild for GCC 4.3

* Sun Aug 19 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.9.0-2
- use macro for version
`
* Sun Aug 19 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.9.0-1
- 0.9.0
- update license tag to LGPLv2+

* Fri May 04 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.6.0-2
- enable docbook build

* Mon Mar 19 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.6.0-1
- initial release
