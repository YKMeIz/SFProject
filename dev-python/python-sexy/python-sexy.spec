%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define real_name sexy-python
Name:           python-sexy
Version:        0.1.9
Release:        20%{?dist}

Summary:        Python bindings to libsexy

Group:          System Environment/Libraries
# No version specified.
License:        LGPLv2+
URL:            http://www.chipx86.com/wiki/Libsexy
Source0:        http://releases.chipx86.com/libsexy/sexy-python/sexy-python-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libsexy-devel >= 0.1.10
BuildRequires:  python-devel >= 2
BuildRequires:  pygtk2-devel >= 2.8.0
BuildRequires:  libxml2-devel
Requires:  libsexy >= 0.1.10

%description
sexy-python is a set of Python bindings around libsexy.


%prep
%setup -q -n  %{real_name}-%{version}


%build
%configure --enable-docs
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT



%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog NEWS README
%{python_sitearch}/gtk-2.0/sexy.so
%{_datadir}/pygtk/2.0/defs/sexy.defs


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 28 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 0.1.9-13
- revert previous change (unnecessary patch - should be fixed in pygtk2 not python-sexy)

* Wed Jul 28 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.1.9-12
- Fix gdk-pixbuf header location issue on F-14

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.9-11
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Mar 31 2010 Haïkel Guémar <karlthered@gmail.com> - 0.1.9-10
- Rebuilt for F-13

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.9-7
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1.9-6
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.9-5
- Autorebuild for GCC 4.3

* Fri May 04 2007 Haïkel Guémar <karlthered@gmail.com> - 0.1.9-4
- Rebuild on ppc64

* Sat Dec 23 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.1.9-3
- Rebuild with Python 2.5.

* Thu Oct 26 2006 Haïkel Guémar <karlthered@gmail.com> - 0.1.9-2
- fixed requires that asked libsexy-devel instead of libsexy.

* Tue Oct 17 2006 Haïkel Guémar <karlthered@gmail.com> - 0.1.9-1
- updated to 0.1.9, license file issue has been fixed upstream

* Tue Sep 12 2006 Haïkel Guémar <karlthered@gmail.com> - 0.1.8-5
- rebuild for FC6

* Thu Aug 17 2006 Haïkel Guémar <karlthered@gmail.com> - 0.1.8-4
- Added quiet extraction of source tarball, some cleaning to the spec file

* Sun Aug 13 2006 Haïkel Guémar <karlthered@gmail.com> - 0.1.8-3
- fixed some rpmlint issues, add a patch to correct the license file

* Fri May 26 2006 Haïkel Guémar <karlthered@gmail.com> - 0.1.8-2
- Some cleaning to the spec file

* Mon May 22 2006 Karl <karlthered@gmail.com> - 0.1.8-1
- First Packaging
