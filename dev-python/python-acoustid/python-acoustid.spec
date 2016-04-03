%global oname   pyacoustid

Summary:        Python bindings for Chromaprint acoustic fingerprinting and the Acoustid API
Name:           python-acoustid
Version:        0.7
Release:        6%{?dist}
License:        MIT
URL:            http://pypi.python.org/pypi/pyacoustid
Source0:        http://pypi.python.org/packages/source/p/pyacoustid/pyacoustid-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Requires:       libchromaprint
Requires:       python-audioread

%description
Chromaprint and its associated Acoustid Web service make up a
high-quality, open-source acoustic fingerprinting system. This package
provides Python bindings for both the fingerprinting algorithm
library, which is written in C but portable, and the Web service,
which provides fingerprint look ups.

%prep
%setup -q -n %{oname}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc README.rst aidmatch.py
%{python_sitelib}/acoustid.py*
%{python_sitelib}/chromaprint.py*
%{python_sitelib}/pyacoustid-%{version}-*.egg-info/


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 16 2012 Terje Røsten <terje.rosten@ntnu.no> - 0.7-3
- Fix req.

* Mon Aug 27 2012 Terje Røsten <terje.rosten@ntnu.no> - 0.7-2
- Convert spec to utf-8
- Fix spelling

* Fri Aug 24 2012 Terje Røsten <terje.rosten@ntnu.no> - 0.7-1
- initial package
