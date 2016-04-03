%global commit f5218b7dc06bfe53dac632cb3de3f3679fd33f04
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Name:		flattr-icons
Version:	0
Release:	0.1.20141227git%{shortcommit}%{?dist}
BuildArch:	noarch
Summary:	Icon theme for Linux desktops, inspired by the latest flat design trend.

Group:		User Interface/Desktops
License:	CC BY-NC-SA 4.0

URL:		https://github.com/NitruxSA/flattr-icons

Source0:	https://github.com/NitruxSA/flattr-icons/archive/%{commit}.zip

Requires:	kde-workspace

%description
QtCurve is highly configurable theme engine, aimed at providing a uniform
look across applications. Currently it provides window decorations for kwin,
as well as widget styles for applications based on the Qt5/Qt4/GTK2 toolkits.


%prep
%autosetup -n %{name}-%{commit}


%build

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}%{_datadir}/icons/%{name}
cp -pR * %{buildroot}%{_datadir}/icons/%{name}


%files
%doc CONTRIBUTORS CREDITS LICENSE README.md
%{_datadir}/icons/flattr-icons/


%changelog
* Sat Dec 27 2014 Nux <rpm@li.nux.ro> - 0-0.1-20141227git%{shortcommit}
- build for EL7

* Sun Sep 14 2014 Steven Franzen <sfranzen@fedorapeople.org> - 0-0.1.20140914git%{shortcommit}
- Initial package release
 
