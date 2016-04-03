Name:           devilspie
Version:        0.22
Release:        13%{?dist}
Summary:        A window-matching utility

Group:          User Interface/X
License:        GPLv2+
URL:            http://www.burtonini.com/blog/computers/devilspie
Source0:        http://www.burtonini.com/computing/%{name}-%{version}.tar.gz
Patch0:         devilspie-0.22-dsofix.patch
Patch1:         devilspie-0.20.2-manpage.patch
# from https://bugzilla.gnome.org/show_bug.cgi?id=636890
Patch2:         devilspie-0.22-gtk-2.22.1.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libwnck-devel
BuildRequires:  libpng-devel
BuildRequires:  libxml2-devel
BuildRequires:  gettext
BuildRequires:  perl(XML::Parser)

%description
A window-matching utility, inspired by Sawfish's "Matched Windows" option and
the lack such functionality in Metacity. Devil's Pie can be configured to
detect windows as they are created, and match the window to a set of rules. If
the window matches the rules, it can perform a series of actions on that
window. 

%prep
%setup -q

%patch0 -p1 -b .dsofix
%patch1 -p1 -b .manpage
%patch2 -p0 -b .gtk-2.22.1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ChangeLog README AUTHORS NEWS COPYING TODO
%{_bindir}/devilspie
%{_mandir}/man1/devilspie.1.gz

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.22-7
- Rebuild for new libpng

* Wed Feb 09 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.22-6
- Fix for GTK >= 2.22.1 (bugzilla.gnome.org #636890)

* Thu Feb 25 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.22-5
- Add patch to fix DSO linking (#564707)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 09 2008 Sebastian Vahl <fedora@deadbabylon.de> 0.22-2
- rebuild for new gcc-4.3

* Thu Dec 13 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.22-1
- new upstream version: 0.22

* Mon Nov 12 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.21-1
- new upstream version: 0.21

* Mon Sep 17 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.20.2-5
- Fix some minor issue in manpage (#293731)

* Tue Aug 28 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.20.2-4
- Change License to GPLv2+

* Tue Jun 06 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.20.2-3
- rebuild against new libwnck (again)

* Tue Jun 05 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.20.2-2
- rebuild against new libwnck

* Mon Jan 29 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.20.2-1
- New upstream version: 0.20.2

* Fri Jan 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 0.20.1-1
- New upstream version: 0.20.1

* Sat Dec 02 2006 Sebastian Vahl <fedora@deadbabylon.de> 0.19-2
- Removed gob2 from BR (not needed any more)
- Replaced perl-XML-Parser with perl(XML::Parser) in BR

* Fri Dec 01 2006 Sebastian Vahl <fedora@deadbabylon.de> 0.19-1
- New upstream version: 0.19

* Wed Oct 25 2006 Sebastian Vahl <fedora@deadbabylon.de> 0.18-1
- New upstream version: 0.18

* Wed Aug 23 2006 Sebastian Vahl <fedora@deadbabylon.de> 0.17.1-2
- removed redundant dependencies: atk-devel gtk2-devel pango-devel
- shorten summary and description
- fixed rpmlint in spec error: mixed-use-of-spaces-and-tabs

* Wed Mar 08 2006 Sebastian Vahl <fedora@deadbabylon.de> 0.17.1-1
- New upstream version: 0.17.1

* Mon Jan 09 2006 Sebastian Vahl <fedora@deadbabylon.de> 0.16-1
- New upstream version: 0.16

* Mon Jul 18 2005 Menno Smits <menno@freshfoo.com> 0.10-1
- initial package for Fedora Extras
