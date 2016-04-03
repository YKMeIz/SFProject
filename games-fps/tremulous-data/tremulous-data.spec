Name:           tremulous-data
Version:        1.2.0
Release:        0.7.beta1%{?dist}
Summary:        Data files for tremulous the FPS game
Group:          Amusements/Games
License:        CC-BY-SA
URL:            http://tremulous.net
# To get the source tarball:
# wget http://downloads.sourceforge.net/tremulous/tremulous-1.1.0.zip
# unzip tremulous-1.1.0.zip
# wget http://prdownloads.sourceforge.net/tremulous/tremulous-gpp1.zip
# unzip tremulous-gpp1.zip
# cp tremulous/gpp/* tremulous/base/
# mkdir tremulous-data-1.2.0
# cp tremulous/base tremulous-data-1.2.0/
# cp tremulous/C* tremulous-data-1.2.0/
# cp tremulous/manual.pdf tremulous-data-1.2.0/
# tar -czf tremulous-data-1.2.0.tar.gz tremulous-data-1.2.0
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-copyright.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
Data files for tremulous the Quake 3 based FPS game.


%prep
%setup -q
install -p -m 644 %{SOURCE1} fedora-copyright.txt


# %build
# nothing to build data only


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/tremulous/base
install -p -m 0644 base/*.pk3 $RPM_BUILD_ROOT%{_datadir}/tremulous/base/
install -p -m 0644 base/*.cfg $RPM_BUILD_ROOT%{_datadir}/tremulous/base/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CC COPYING fedora-copyright.txt manual.pdf
%{_datadir}/tremulous


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.7.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.6.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.5.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.4.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.3.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 17 2010 Jan Kaluza <jkaluza@redhat.com> - 1.2.0-0.1.beta1
- update to 1.2.0 beta
- fix #602374 - tremulous works on x86_64 now

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ian Weller <ianweller@gmail.com> 1.1.0-5
- Remove Requires on tremulous

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-4
- Update License tag for new Licensing Guidelines compliance

* Tue Sep  5 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-3
- Various small packaging improvements (see bug 204125)

* Mon Sep  4 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-2
- Add fedora-copyright.txt to %doc, which explains and contains the lifting of
  the shaderlab license exception, which makes this package distributable by
  Fedora

* Fri Aug 25 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.1.0-1
- Initial Fedora packaging (based on work from Matthias and Wart)
