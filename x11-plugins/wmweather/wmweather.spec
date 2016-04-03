Name:           wmweather
Version:        2.4.5
Release:        4%{?dist}
Summary:        Applet which shows local weather conditions
Summary(de):    Applet, welches die lokalen Wetterbedingungen anzeigt

Group:          User Interface/X
License:        GPLv2+
URL:            http://people.debian.org/~godisch/wmweather/
Source0:        http://ftp.de.debian.org/debian/pool/main/w/wmweather/%{name}_%{version}.orig.tar.gz

BuildRequires:  curl-devel
BuildRequires:  libXext-devel
BuildRequires:  libXpm-devel
Requires:       xorg-x11-fonts-misc

%description
wmWeather is a dockapp that displays the local weather conditions, using the
values provided from some weather services.

%description -l de
wmWeather ist ein Dockapp, welches die lokalen Wetterdedingungen anzeigt, unter
Verwendung der Werte von verschiedenen Wetterdiensten.

%prep
%setup -q

%build
cd src
%configure --without-xmessage

%install
cd src
make install DESTDIR=%{buildroot} %{?_smp_mflags}


%files
%doc CHANGES COPYING README src/wmweather.conf
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%exclude %{_bindir}/wmWeather
%exclude %{_mandir}/man1/wmWeather.1.*

%changelog
* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 11 2011 Mario Blättermann <mariobl@fedoraproject.org> 2.4.5-2
- Added Group

* Sun Jul 31 2011 Mario Blättermann <mariobl@fedoraproject.org> 2.4.5-1
- Initial package
