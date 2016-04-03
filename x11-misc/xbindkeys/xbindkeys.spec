Name:           xbindkeys
Version:        1.8.5
Release:        7%{?dist}

Summary:        Binds keys or mouse buttons to shell commands under X
License:        GPLv2+
Group:          User Interface/X
URL:            http://www.nongnu.org/xbindkeys/
Source:         http://www.nongnu.org/xbindkeys/xbindkeys-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  guile-devel
BuildRequires:  libX11-devel
Requires:       tk

%description
xbindkeys is a program that allows you to launch shell commands
with your keyboard or mouse under X. It links commands to keys
or mouse buttons using a simple configuration file, and is
independent of the window manager.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} LDFLAGS="-lpthread"

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS BUGS ChangeLog COPYING INSTALL NEWS README TODO xbindkeysrc*
%attr(0755, root, root) %{_bindir}/xbindkeys*
%attr(0644, root, root) %{_mandir}/man?/*

%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon May 23 2011 Christian Krause <chkr@fedoraproject.org> - 1.8.5-1
- Update to new upstream version 1.8.5
- Drop rpl_malloc patch since it is not needed anymore

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 12 2010 Christian Krause <chkr@fedoraproject.org> - 1.8.3-1
- Update to new upstream version 1.8.3
- Update upstream URLs
- Add example configuration files to %%doc
- Minor spec file cleanup

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.8.2-2
- Autorebuild for GCC 4.3

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.8.2-1
- version 1.8.2
- fix license tag

* Sat Jan 20 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.8.0-1
- version 1.8.0

* Thu Aug 31 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.7.3-4
- rebuild

* Sun Jul 02 2006 Aurelien Bompard <gauret[AT]free.fr> 1.7.3-3
- use LDFLAGS=-lpthread to fix build on FC6

* Sun Jul 02 2006 Aurelien Bompard <gauret[AT]free.fr> 1.7.3-2
- add patch to disable the use of rpl_malloc instead of malloc

* Tue May 30 2006 Aurelien Bompard <gauret[AT]free.fr> 1.7.3-1
- version 1.7.3

* Fri May 12 2006 Aurelien Bompard <gauret[AT]free.fr> 1.7.2-5
- rebuild

* Wed Feb 22 2006 Aurelien Bompard <gauret[AT]free.fr> 1.7.2-4
- fix dependencies for modular Xorg

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 1.7.2-3
- rebuild for FC5

* Sun Jun 12 2005 Aurelien Bompard <gauret[AT]free.fr> 1.7.2-2
- rebuild

* Sun May 08 2005 Aurelien Bompard <gauret[AT]free.fr> 1.7.2-1%{?dist}
- version 1.7.2
- use disttag

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Jan 12 2004 Aurelien Bompard <gauret[AT]free.fr> 1.7.1-0.fdr.1
- adapt to Fedora

* Thu Jan 08 2004 Philippe Brochard <hocwp@free.fr>
- build for 1.7.1

* Fri Nov 15 2002 David Zambonini <dave@alfar.co.uk>
- build for 1.6.3

* Wed Nov 13 2002 David Zambonini <dave@alfar.co.uk>
- second 1.6.2 release - fixed default attributes on docs (oops!)

* Tue Nov 12 2002 David Zambonini <dave@alfar.co.uk>
- build for 1.6.2. wheee

* Tue Nov 12 2002 David Zambonini <dave@alfar.co.uk>
- build for 1.6.1. that was quick

* Sun Nov 10 2002 David Zambonini <dave@alfar.co.uk>
- build for 1.6

* Sat Nov 01 2002 David Zambonini <dave@alfar.co.uk>
- Added additional documents, tweaked description

* Mon Oct 30 2002 David Zambonini <dave@alfar.co.uk>
- Initial revision.

