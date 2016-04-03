%global with_python3 1

%global oname   audioread

Summary:        Multi-library, cross-platform audio decoding in Python
Name:           python-audioread
Version:        1.0.1
Release:        3%{?dist}
License:        MIT
URL:            http://pypi.python.org/pypi/audioread/
Source0:        http://pypi.python.org/packages/source/a/audioread/audioread-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python-tools
%endif
Requires:       gstreamer-python

%description
Decode audio files using whichever backend is available. Among
currently supports backends are 
 o Gstreamer via gstreamer-python 
 o The standard library wave and aifc modules (for WAV and AIFF files)

%if 0%{?with_python3}
%package -n     python3-audioread
Summary:        Multi-library, cross-platform audio decoding in Python
#Requires:      gstreamer-python
%description -n python3-audioread
Decode audio files using whichever backend is available. Among
currently supports backends are 
 o Gstreamer via gstreamer-python 
 o The standard library wave and aifc modules (for WAV and AIFF files)
%endif # if with_python3

%prep
%setup -q -n %{oname}-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python2} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
2to3 --write --nobackups .
%{__python3} setup.py build
%endif

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
%endif

%files
%doc README.rst decode.py
%{python2_sitelib}/audioread/
%{python2_sitelib}/audioread-%{version}-*.egg-info

%if 0%{?with_python3}
%files -n python3-audioread
%doc README.rst decode.py
%{python3_sitelib}/audioread/
%{python3_sitelib}/audioread-%{version}-*.egg-info
%endif

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Nov 18 2013 Terje Røsten <terje.rosten@ntnu.no> - 1.0.1-1
- 1.0.1
- Python 3 support

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 24 2012 Terje Røsten <terje.rosten@ntnu.no> - 0.6-1
- initial package

