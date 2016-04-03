Name:           netactview
Version:        0.6.2
Release:        1%{?dist}
Summary:        Graphical network connections viewer for Linux

Group:          Applications/Internet
License:        GPLv2+
URL:            http://netactview.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  gettext
BuildRequires:  desktop-file-utils 
BuildRequires:  gtk+-devel
BuildRequires:  libglade2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgtop2-devel
BuildRequires:  intltool
BuildRequires:  perl-XML-Parser
BuildRequires:  glib-devel
BuildRequires:  pkgconfig

%description
Netactview is a graphical network connections viewer for Linux, similar in
functionality with Netstat. It includes features like process information,
host name retrieval, automatic refresh and sorting. It has a fully featured
GTK 2 graphical interface.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%{make_install}

desktop-file-install                            \
  --set-icon=netactview                         \
  --remove-category=Application                 \
  --delete-original                             \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  $RPM_BUILD_ROOT%{_datadir}/applications/netactview.desktop

%find_lang %{name}

%files -f %{name}.lang
%doc README COPYING AUTHORS NEWS ChangeLog
%{_bindir}/netactview
%{_datadir}/netactview/
%{_datadir}/pixmaps/netactview.png
%{_datadir}/applications/netactview.desktop
%{_mandir}/man1/netactview.1.*

%changelog
* Thu May 01 2014 Leigh Scott <leigh123linux@googlemail.com> - 0.6.2-1
- update to 0.6.2

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 0.6.1-8
- Rebuilt for libgtop2 soname bump

* Tue Oct 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-7
- clean up spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-5
- Patch for autoconf changes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-3
- spec file clean up

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 28 2012 Leigh Scott <leigh123linux@googlemail.com> - 0.6.1-1
- update to 0.6.1
- add Br libgtop2-devel

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.6-3
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 leigh scott <leigh123linux@googlemail.com> - 0.6-1
- update to 0.6

* Fri Jan 08 2010 Leigh Scott <leigh123linux@googlemail.com> - 0.5.1-1
- update to 0.5.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

*Thu Feb 19  2009 leigh scott  <leigh123linux@googlemail.com> 0.4.1-3
- add find_lang

*Sun Feb 15  2009 leigh scott  <leigh123@linux.net> 0.4.1-2
- Review changes.
- fix permissions on debug. 
- fix desktop file (remove Application).

*Sat Jan 3  2009 leigh scott  <leigh123@linux.net> 0.4.1-1
- update to 0.4.1 
- fix desktop file.
- fix permissions on ChangeLog AUTHORS README COPYING NEWS.

*Sat Sep 13  2008 leigh scott  <leigh123@linux.net> 0.3.1-1
- first build

