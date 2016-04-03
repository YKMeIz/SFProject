Name:          rapidxml
Version:       1.13
Release:       3%{?dist}
Summary:       Fast XML parser
License:       Boost or MIT
URL:           http://rapidxml.sourceforge.net/
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}-with-tests.zip
Patch0:        %{name}-declarations.patch
BuildArch:     noarch
BuildRequires:  dos2unix

%description
RapidXml is an attempt to create the fastest XML parser possible, while
retaining usability, portability and reasonable W3C compatibility. It is an
in-situ parser written in modern C++, with parsing speed approaching that of
strlen function executed on the same data.

%package devel
Summary:       Fast XML parser
Provides:      %{name}-static = %{version}-%{release}

%description devel
RapidXml is an attempt to create the fastest XML parser possible, while
retaining usability, portability and reasonable W3C compatibility. It is an
in-situ parser written in modern C++, with parsing speed approaching that of
strlen function executed on the same data.

%prep
%setup -qn %{name}-%{version}-with-tests
%patch0 -p1

dos2unix license.txt

# Rename it to .h (but keep .hpp for tests)
sed -i 's/.hpp/.h/g' manual.html
for HPP in *.hpp; do
  cp -p $HPP ${HPP%hpp}h
  sed -i 's/.hpp/.h/g' ${HPP%hpp}h
done

%build
cd tests
# -jX is useless here
make build-g++-debug
cd -

%install
for H in *.h; do
  install -Dpm0644 $H %{buildroot}%{_includedir}/$H
done

%check
cd tests
# -jX is useless here
make run-g++-debug
cd -

%files devel
%doc license.txt manual.html
%{_includedir}/*

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr 20 2013 Miro Hrončok <mhroncok@redhat.com> - 1.13-2
- devel subpackage now provides -static.

* Sat Feb 02 2013 Miro Hrončok <mhroncok@redhat.com> - 1.13-1
- Initial release
