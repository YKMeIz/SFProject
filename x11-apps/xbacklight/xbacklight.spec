Name:           xbacklight
Version:        1.2.1
Release:        1%{?dist}
Summary:        Adjust backlight brightness using RandR

%if 0%{?el6}
Group:          User Interface/X Hardware Support
%endif
License:        MIT
URL:            http://xorg.freedesktop.org/releases/individual/app/
Source0:        http://xorg.freedesktop.org/releases/individual/app/xbacklight-%{version}.tar.bz2

BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-atom)
BuildRequires:  pkgconfig(xcb-aux)
BuildRequires:  pkgconfig(xcb-randr)

%description
Xbacklight is used to adjust the backlight brightness where
supported. It finds all outputs on the X server supporting backlight
brightness control and changes them all in the same way.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README
%{_bindir}/xbacklight
%{_datadir}/man/man1/xbacklight.*


%changelog
* Sat Dec  6 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 16 2012 Michel Salim <salimma@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0
- Spec clean-ups

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Michel Salim <salimma@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2

* Mon Jul  5 2010 Michel Salim <salimma@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1-2
- Autorebuild for GCC 4.3

* Sat Jan 26 2008 Michel Salim <michel.sylvan@gmail.com> - 1.1-1
- Initial Fedora package
