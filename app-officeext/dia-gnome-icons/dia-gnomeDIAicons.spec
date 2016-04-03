%define	_datadir /usr/share/dia 

Name:           dia-gnomeDIAicons
Version:        0.1
Release:        5%{?dist}
Summary:        Beautiful icon set for dia diagram editor

License:        GPL+
#URL:            http://gnomediaicons.sourceforge.net/files/rib-network-v0.1.tar.gz
URL:            http://gnomediaicons.sourceforge.net
Source0:        %{name}-%{version}.tar.gz

BuildArch:          noarch
BuildRequires:  dia
Requires:       dia

%description
A collection of gnome network icons adapted to Dia

%prep
%setup -q -c diaicons
chmod 0644 shapes/RIB-Network/*

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -d -m 0755 %{buildroot}%{_datadir}/
%{__cp} -av * %{buildroot}%{_datadir}/

%clean
%{__rm} -rf %{buildroot}

%files
%doc
%{_datadir}/shapes/*
%{_datadir}/sheets/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

