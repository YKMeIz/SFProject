%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-CDDB
Version:        1.4
Release:        12%{?dist}
Summary:        CDDB and FreeDB audio CD track info access in Python

Group:          Development/Languages
License:        GPLv2+
URL:            http://cddb-py.sourceforge.net/
Source0:        http://dl.sourceforge.net/sourceforge/cddb-py/CDDB-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel

%description
This is actually a set of three modules to access the CDDB and FreeDB
online databases of audio CD track titles and information. It includes
a C extension module to fetch track lengths under Linux, FreeBSD,
OpenBSD, Mac OS X, Solaris, and Win32, which is easily ported to other
operating systems.

%prep
%setup -q -n CDDB-%{version}
%{__sed} -e '/^#!/,1d' < CDDB.py > CDDB.py.tmp
mv CDDB.py.tmp CDDB.py
%{__sed} -e '/^#!/,1d' < DiscID.py > DiscID.py.tmp
mv DiscID.py.tmp DiscID.py

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
 
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING README
%{python_sitearch}/*

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.4-4
- Rebuild for Python 2.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4-2
- Bump release and rebuild.
- Update license tag.

* Mon Dec 11 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4-1
- First version for Fedora Extras

