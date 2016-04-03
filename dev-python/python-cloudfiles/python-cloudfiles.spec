
# FIX ME: Need to add code for building python26-cloudfiles.  Pending:
#
# https://bugzilla.redhat.com/show_bug.cgi?id=678690
# 

%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Name:       python-cloudfiles        
Version:    1.7.10
Release:    5%{?dist}
Summary:    Python language bindings for Rackspace CloudFiles API

Group:      Development/Libraries           
License:    MIT    
URL:        https://github.com/rackspace/python-cloudfiles

Source0:    http://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz 
BuildArch:  noarch
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  python-setuptools, python-nose 
Requires:       python2

%description
Python language bindings for Rackspace CloudFiles API

%prep
%setup -q 

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 \
    --skip-build \
    --root %{buildroot}

%check
nosetests

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
#%%doc ChangeLog COPYING
%{python_sitelib}/cloudfiles/
%{python_sitelib}/python_cloudfiles-*-py*.egg-info/

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 BJ Dierkes <wdierkes@rackspace.com> - 1.7.10-1
- Latest sources from upstream, rebuild for F18.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 BJ Dierkes <wdierkes@rackspace.com> - 1.7.9.3-1
- Latest sources from upstream, rebuild for F17.

* Wed Apr 20 2011 BJ Dierkes <wdierkes@rackspace.com> - 1.7.9.1-1
- Latest sources from upstream.  

* Tue Feb 15 2011 BJ Dierkes <wdierkes@rackspace.com> - 1.7.8-1
- Latest sources.
- Use PyPi as upstream Source0

* Mon Jan 31 2011 BJ Dierkes <wdierkes@rackspace.com> - 1.7.7-1
- Latest sources.
- Removed Patch0: broken_tests.patch (applied upstream).

* Tue Jan 25 2011 BJ Dierkes <wdierkes@rackspace.com> - 1.7.6.1-1
- Latest sources
- Fixed Source0 to a usable URL
- BR: python-nose, and run nosetests in %%check
- Added Patch0: broken_tests.patch.  Resolves GH#23
  https://github.com/rackspace/python-cloudfiles/issues#issue/23

* Mon Jan 17 2011 BJ Dierkes <wdierkes@rackspace.com> - 1.7.5-1
- Initial spec build

