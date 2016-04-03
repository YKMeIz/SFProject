# first two digits of version
%global release_version %%(echo %{version} | awk -F. '{print $1"."$2}')

Name:           gnome-nettool
Version:        3.8.1
Release:        5%{?dist}
Summary:        Network information tool for GNOME

License:        GPLv2+ and GFDL
URL:            http://projects.gnome.org/gnome-network/
Source0:        http://download.gnome.org/sources/gnome-nettool/%{release_version}/gnome-nettool-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  libgtop2-devel

Requires:       bind-utils
Requires:       coreutils
Requires:       iputils
Requires:       net-tools
Requires:       nmap
Requires:       traceroute
Requires:       whois

%description
GNOME Nettool is a front-end to various networking command-line
tools, like ping, netstat, ifconfig, whois, traceroute, finger.


%prep
%setup -q


%build
%configure --disable-compile-warnings
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang gnome-nettool --with-gnome


%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/gnome-nettool.desktop


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f gnome-nettool.lang
%doc AUTHORS COPYING NEWS README
%{_bindir}/gnome-nettool
%{_datadir}/applications/gnome-nettool.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.gnome-nettool.gschema.xml
%{_datadir}/gnome-nettool/
%{_datadir}/icons/hicolor/*/apps/gnome-nettool.png
%{_datadir}/icons/hicolor/scalable/apps/gnome-nettool.svg


%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 3.8.1-3
- Rebuilt for libgtop2 soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Thu May 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.2.0-3
- Depend on package names instead of executables

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.2.0-2
- Use %%global instead of %%define (#812674)

* Fri Apr 13 2012 Kalev Lember <kalevlember@gmail.com> - 3.2.0-1
- Update to 3.2.0, spec file clean up for re-review (#812674)

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-4
- Rebuild gainst newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-2
- Rebuild against newer gtk

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-1
- Update to 2.91.5

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.2-2
- Rebuild against newer gtk3

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Thu Aug 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Fri Dec  4 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.3-2
- Update to 2.25.3

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-3
- Tweak description

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-2
- Update to 2.22.1

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.22.0-2
- fix license tag

* Tue Mar 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 18 2008 Christopher Aillon <caillon@redhat.com> - 2.20.0-3
- Rebuild to celebrate my birthday (and GCC 4.3)

* Thu Oct 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-2
- Rebuild

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 2.19.90-2
- Rebuild for build ID

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Wed Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.4-1
- Update to 2.17.4

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-1.fc6
- Update to 2.16.0

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.0-1.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 2.15.0-1
- Update to 2.15.0

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 2.13.90-4
- Add missing BuildRequires

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> 2.13.90-3
- Add BuildRequires for perl-XML-Parser

* Wed Mar 01 2006 Karsten Hopp <karsten@redhat.de> 2.13.90-2
- BuildRequires: desktop-file-utils for desktop-file-install

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.90

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 17 2005 Ray Strode <rstrode@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0

* Wed Mar  2 2005 Mark McLoughlin <markmc@redhat.com> 0.99.3-3
- Rebuild with gcc4

* Tue Sep 21 2004 Mark McLoughlin <markmc@redhat.com> 0.99.3-2
- Move to the System Tools menu from the Internet menu - bug #131619

* Tue Aug 31 2004 Mark McLoughlin <markmc@redhat.com> 0.99.3-1
- Update to 0.99.3

* Fri Aug 27 2004 Mark McLoughlin <markmc@redhat.com> 0.99.2-1
- Initial build
