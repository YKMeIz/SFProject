%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%endif

%global mod_name mock

Name:           python-mock
Version:        1.0.1
Release:        4%{?dist}
Summary:        A Python Mocking and Patching Library for Testing

Group:          Development/Libraries
License:        BSD
URL:            http://www.voidspace.org.uk/python/%{mod_name}/
Source0:        http://pypi.python.org/packages/source/m/%{mod_name}/%{mod_name}-%{version}.tar.gz
Source1:        LICENSE.txt

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-unittest2

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif


%description
Mock is a Python module that provides a core mock class. It removes the need
to create a host of stubs throughout your test suite. After performing an
action, you can make assertions about which methods / attributes were used and
arguments they were called with. You can also specify return values and set
needed attributes in the normal way.

%if 0%{?with_python3}
%package -n python3-mock
Summary:        A Python Mocking and Patching Library for Testing
Group:          Development/Libraries

%description -n python3-mock
Mock is a Python module that provides a core mock class. It removes the need
to create a host of stubs throughout your test suite. After performing an
action, you can make assertions about which methods / attributes were used and
arguments they were called with. You can also specify return values and set
needed attributes in the normal way.

%endif


%prep
%setup -q -n %{mod_name}-%{version}
cp -p %{SOURCE1} .

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -ap . %{py3dir}
%endif


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif


#check
#{__python} setup.py test


%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

 
%files
%doc docs/ README.txt PKG-INFO LICENSE.txt
%{python_sitelib}/*.egg-info
%{python_sitelib}/%{mod_name}.py*

%if 0%{?with_python3}
%files -n python3-mock
%doc docs/ README.txt PKG-INFO LICENSE.txt
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{mod_name}.py*
%{python3_sitelib}/__pycache__/%{mod_name}*
%endif


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 1.0.1-3
- rebuild for python 3.4
- disable test suite deps missing

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 11 2013 Luke Macken <lmacken@redhat.com> - 1.0.1-1
- Update to 1.0.1
- Run the test suite
- Add python-unittest2 as a build requirement

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.8.0-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Ralph Bean <rbean@redhat.com> - 0.8.0-2
- Python3 support

* Thu Mar 22 2012 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.8.0-1
- Updated to new version

* Fri Jul 22 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.7.2-1
- Initial RPM release
