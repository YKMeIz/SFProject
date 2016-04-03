%global dia_datadir %{_datadir}/dia
%global shapes electronic

Name:           dia-%{shapes}
Version:        0.1
Release:        7%{?dist}
Summary:        Dia Digital IC logic shapes

Group:          Applications/Engineering
License:        GPLv2+
URL:            http://dia-installer.de/shapes/electronic/index_en.html
Source0:        http://dia-installer.de/shapes/electronic/electronic.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       dia
BuildArch:      noarch

%description
The following shapes are included in the package:
 * Antenna
 * Bell
 * Button
 * Capacitor
 * Electrolytic capacitor
 * Crystal
 * Di-Gate
 * Diac
 * Engine
 * Headphone
 * Inverse diode
 * Schottky diode
 * Tunnel diode
 * Zenner diode
 * Inductor
 * LED display
 * Microphone
 * Photo-emiting part
 * Photosensitive part
 * Potenciometer
 * Ground
 * Contact
 * Contact Pair
 * IN Port
 * OUT Port
 * IN/OUT Port
 * Voltmeter
 * Ampermeter
 * Source or Meter
 * Current source
 * Substitute linearised source
 * Voltage source
 * Alternating voltage source
 * Direct voltage source
 * Bipolar transistor NPN
 * Bipolar transistor NPN
 * Bipolar transistor PNP
 * Bipolar transistor PNP
 * JFE transitor - N
 * JFE transistor - P
 * MISFE conducting transistor - N
 * MISFE conducting transistor - P
 * MISFE inducting transistor - N
 * MISFE inducting transistor - P
 * Single ..... transistor
 * Triac
 * Diode tyristor, blocking
 * Triode tyristor, blocking
 * Vacuum diode
 * Vacuum pentode
 * Vacuum triode
 * Linear variable part
 * Nonlinear variable part
 * Varicap

%prep
%setup -q -c


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{dia_datadir}/sheets
cp -p sheets/%{shapes}.sheet %{buildroot}%{dia_datadir}/sheets
cp -pr shapes %{buildroot}%{dia_datadir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING
%{dia_datadir}/sheets/%{shapes}.sheet
%{dia_datadir}/shapes/%{shapes}/

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 15 2009 Chitlesh Goorah <chitlesh [AT] fedoraproject DOT org> 0.1-1
- init fedora package
