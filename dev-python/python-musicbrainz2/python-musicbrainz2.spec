%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           python-musicbrainz2
Version:        0.7.0
Release:        9%{?dist}
Summary:        Library which provides access to the MusicBrainz Database

Group:          Development/Languages
License:        BSD
URL:            http://musicbrainz.org/doc/PythonMusicBrainz2
Source0:        http://users.musicbrainz.org/~matt/python-musicbrainz2-%{version}.tar.gz

Patch3:	        0003-Support-both-the-0.2.x-and-the-0.1.x-versions-of-the.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-setuptools

Requires:       libdiscid

%description
The package python-musicbrainz2 is a client library written in python,
which provides easy object oriented access to the MusicBrainz Database
using the XMLWebService. It has been written from scratch and uses a
different model than PythonMusicbrainz, the first generation python
bindings.

%prep
%setup0 -q
%patch3 -p1

%build
CFLAGS="%{optflags}" %{__python} -c 'import setuptools; execfile("setup.py")' build

%install
rm -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot}
 
%clean
rm -rf %{buildroot}

%check
CFLAGS="%{optflags}" %{__python} setup.py test

%files
%defattr(-,root,root,-)
%doc AUTHORS.txt CHANGES.txt COPYING.txt INSTALL.txt README.txt
%{_bindir}/mb-submit-disc
%{python_sitelib}/*

%changelog
* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 0.7.0-9
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jan  6 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.7.0-1
- Update to 0.7.0
- Drop upstreamed patches
- Switch to using global instead of define

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-3
- Rebuild for Python 2.6

* Fri Aug  1 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6.0-2
- Add some patches from upstream SVN
- Clean up cruft for compatibility with previous releases of Fedora.
- Add a patch that lets either version 0.2.x or 0.1.x of libdiscid be used.

* Fri Aug  1 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.6.0-1
- Update to 0.6.0

* Fri Jan  4 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.5.0-2
- Update to build/package egg info files.

* Fri Nov 16 2007 Alex Lancaster <alexlan@fedoraproject.org> - 0.5.0-1
- Update to latest upstream: 0.5.0
- Requires: libdiscid to get DiscID support (#248308)

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.1-1
- Update to 0.4.1

* Tue Dec 12 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.0-3
- Don't require python-ctypes in development as it's included in the
  main Python package

* Fri Dec  8 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.0-2
- Bump release for rebuild with Python 2.5.

* Tue Nov 14 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.4.0-1
- Update to 0.4.0.

* Wed Aug 16 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.3.1-2
- Add Requires for python-ctypes and libmusicbrainz.
- Add check section.

* Sun Aug 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.3.1-1
- First version for Fedora Extras

