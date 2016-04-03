Name:           simple-scan
Version:        3.10.0
Release:        1%{?dist}
Summary:        Simple scanning utility

Group:          Applications/Multimedia
License:        GPLv3+
URL:            https://launchpad.net/simple-scan
Source0:        https://launchpad.net/simple-scan/3.10/%{version}/+download/simple-scan-%{version}.tar.xz

BuildRequires: intltool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: vala
BuildRequires: gtk3-devel
BuildRequires: libgudev1-devel
BuildRequires: colord-devel
BuildRequires: sane-backends-devel
BuildRequires: sqlite-devel
BuildRequires: itstool

Requires: gnome-icon-theme
Requires: xdg-utils
Requires: yelp

%description
Simple Scan is an easy-to-use application, designed to let users connect their
scanner and quickly have the image/document in an appropriate format.

%prep
%setup -q

%build

%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name} --with-man --with-gnome

%postun
if [ $1 -eq 0 ]; then
  glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc COPYING NEWS README.md
%{_mandir}/man1/simple-scan.1.gz
%{_bindir}/simple-scan
%{_datadir}/appdata/
%{_datadir}/applications/simple-scan.desktop
%{_datadir}/simple-scan/
%{_datadir}/glib-2.0/schemas/org.gnome.SimpleScan.gschema.xml

%changelog
* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0
- Include the appdata file

* Sun Aug 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Tue Jul 30 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-2
- Rebuild for colord soname bump

* Wed Mar 27 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 3.6.0-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 3.6.0-2
- rebuild against new libjpeg

* Wed Sep 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 11 2012 Matthias Clasen <mclasen@redhat.com> - 3.4.1-1
- Update to 3.4.1
- Fixes 820971

* Wed Mar 28 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Richard Hughes <rhughes@redhat.com> - 3.3.92-1
- Update to 3.3.92

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Fri Sep 30 2011 Kalev Lember <kalevlember@gmail.com> - 3.2.0-2
- Fix postun scriplet syntax error

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 2.32.0.2-1
- Update to 2.32.0.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.32.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0.1-1
- Update to 2.32.0.1

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Tue Aug 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90.2-1
- Update to 2.31.90.2

* Mon Aug 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90.1-1
- Update to 2.31.90.1
- Use GConf macros

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-1
- Update to 2.31.5

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.4-1
- Update to 2.31.4

* Mon Jun  7 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-1
- Update to 2.31.3

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.1-1
- Update to 2.31.1

* Mon Mar 17 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.9.9-1
- https://launchpad.net/simple-scan/trunk/0.9.9

* Mon Mar 08 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.9.5-2
- Organize and comment patch dependencies and link to upstream bug report 
- add requires on yelp and add gconf schema scriptlets 

* Fri Mar 05 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.9.5-1
- initial build
