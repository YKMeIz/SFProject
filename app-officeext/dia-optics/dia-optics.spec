%global dia_datadir %{_datadir}/dia
%global shapes Optics

Name:           dia-optics
Version:        0.1
Release:        7%{?dist}
Summary:        Dia Optics shapes

Group:          Applications/Engineering
License:        GPLv2+
URL:            http://dia-installer.de/shapes/optics/index_en.html
Source0:        http://dia-installer.de/shapes/optics/optics.zip
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       dia
BuildArch:      noarch

%description
The following shapes are included in the package:
 * Polarisation Controller
 * Directional Coupler
 * Tuneable Coupler
 * DFB Laser
 * Long Fibre
 * Detector
 * Osilloscope
 * Spectrum Analyser
 * Optical Isolator
 * EDFA
 * Variable Attenuator
 * MZ Modulator
 * Phase Modulator
 * Sine Wave Source
 * Square Wave Source
 * Long Period Grating
 * Light Beam
 * Wave

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

* Sun Oct 3 2010 Thibault North <tnorth@fedoraproject.org> - 0.1-1
- init fedora package
