Name:           pwsafe
Version:        0.2.0
Release:        18%{?dist}
Summary:        A unix commandline program that manages encrypted password databases

Group:          Applications/Databases
License:        GPLv2+
URL:            http://nsd.dyndns.org/pwsafe/
Source0:        http://nsd.dyndns.org/pwsafe/releases/pwsafe-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0:         pwsafe-0.2.0-paste-gnome-terminal.patch
Patch1:         pwsafe-0.2.0-aarch64.patch

BuildRequires:  readline-devel, ncurses-devel, openssl-devel
BuildRequires:  libXt-devel, libXext-devel, libXau-devel, libXdmcp-devel
BuildRequires:  libSM-devel, libICE-devel, libXmu-devel

%description
pwsafe is a unix commandline program that manages encrypted password databases.
Compatible with CounterPane's PasswordSafe Win32 program versions 2.x and 1.x.

%prep
%setup -q
%patch0 -p0 -b .paste-gnome-terminal
%patch1 -p1 -b .aarch64


%build
%configure \
    --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

# Convert man page to UTF-8
iconv -f iso-8859-1 -t utf8 pwsafe.1 -o pwsafe.1.utf8
mv pwsafe.1.utf8 pwsafe.1
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/pwsafe
%{_mandir}/man1/pwsafe.1.gz


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Dec 21 2013 Ralf Ertzinger <ralf@skytale.net> - 0.2.0-16
- Add patch for aarch64 support

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 07 2011 Ralf Ertzinger <ralf@skytale.net> - 0.2.0-11
- Apply patch from BZ667541

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.2.0-9
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.2.0-6
- rebuild with new openssl

* Fri Aug 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.2.0-5
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.0-4
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Ralf Ertzinger <ralf@skytale.net> 0.2.0-3
- Rebuild against new openssl

* Tue Jul 31 2007 Ralf Ertzinger <ralf@skytale.net> 0.2.0-2
- Enable X11 functionality

* Sun Jul 08 2007 Ralf Ertzinger <ralf@skytale.net> 0.2.0-1
- Initial build for Fedora
