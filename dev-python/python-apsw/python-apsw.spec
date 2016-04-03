%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%else
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif

%global sqlite_version 3.7.15.2
%global uprel 1
%global pkg_version %{sqlite_version}-r%{uprel}

%filter_provides_in %{python_sitearch}/.*\.so$ 
%if 0%{?with_python3}
%filter_provides_in %{python3_sitearch}/.*\.so$ 
%endif # if with_python3
%filter_setup

Name:               python-apsw
Version:            %{sqlite_version}.r%{uprel}
Release:            1%{?dist}
Summary:            Another Python SQLite Wrapper
Source:             http://apsw.googlecode.com/files/apsw-%{pkg_version}.zip
URL:                http://code.google.com/p/apsw/
Group:              Development/Libraries
License:            zlib

Requires:           sqlite >= %{sqlite_version}

BuildRequires:      sqlite-devel >= %{sqlite_version}
BuildRequires:      python2-devel
%if 0%{?with_python3}
BuildRequires:      python3-devel
%endif # if with_python3



%description
APSW is a Python wrapper for the SQLite embedded relational database
engine. In contrast to other wrappers such as pysqlite it focuses on
being a minimal layer over SQLite attempting just to translate the
complete SQLite API into Python.
%if 0%{?with_python3}
%package -n python3-apsw
Summary:            Another Python SQLite Wrapper Python 3 packages
Group:              Development/Libraries

%description -n python3-apsw
APSW is a Python 3 wrapper for the SQLite embedded relational database
engine. In contrast to other wrappers such as pysqlite it focuses on
being a minimal layer over SQLite attempting just to translate the
complete SQLite API into Python 3.
%endif # with_python3



%prep
%setup -q -n "apsw-%{pkg_version}"
rm doc/.buildinfo

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3
find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'


%build

CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
CFLAGS="$RPM_OPT_FLAGS" %{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --root %{buildroot}
popd
%endif # with_python3

%{__python} setup.py install --root %{buildroot}

%files
%doc doc/*
%{python_sitearch}/*

%if 0%{?with_python3}
%files -n python3-apsw
%doc doc/*
%{python3_sitearch}/*
%endif # with_python3

%changelog
* Fri Feb 15 2013 Marcel Wysocki <maci@satgnu.net> - 3.7.15.2.r1-1
- update to 3.7.15.2-r1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.11.r1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Marcel Wysocki <maci@satgnu.net> 3.7.11.r1-8
- initial python3 build

* Tue Oct 30 2012 Marcel Wysocki <maci@satgnu.net> 3.7.11.r1-7
- use python2-devel BR instead of python-devel

* Mon Oct 29 2012 Marcel Wysocki <maci@satgnu.net> 3.7.11.r1-6
- removed -doc package, not really needed

* Sun Oct 28 2012 Marcel Wysocki <maci@satgnu.net> 3.7.11.r1-5
- fixed changelog rpmlint error

* Sat Oct 27 2012 Marcel Wysocki <maci@satgnu.net> 3.7.11.r1-4
- use global instead of define macro
- filter private-shared-object-provides 
- removed python from requires

* Tue Oct 23 2012 Marcel Wysocki <maci@satgnu.net> 3.7.11.r1-3
- don't use rm macro
- remove doc/.buildinfo
- add missing dependencies

* Fri Oct 05 2012 Marcel Wysocki <maci@satgnu.net> 3.7.11.r1-2
- add missing builddep

* Thu Oct 04 2012 Marcel Wysocki <maci@satgnu.net> 3.7.11.r1-1
- fedora port
- update to 3.7.11-r1

* Wed Nov 30 2011 Dmitry Mikhirev <dmikhirev@mandriva.org> 3.7.7.1.r1-1
+ Revision: 735584
- imported package python-apsw

