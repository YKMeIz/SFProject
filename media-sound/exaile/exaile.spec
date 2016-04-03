Summary:	A music player
Name:		exaile
Version:	3.4.2
Release:	1%{?dist}
Group:		Applications/Multimedia
License:	GPLv2+
URL:		http://www.exaile.org
Source0:	https://launchpad.net/exaile/3.4.x/3.4.0/+download/%{name}-%{version}.tar.gz
#Patch0:		exaile-3.3.1-makefile.patch
#Patch1:		exaile-3.3.2-udisks.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	pygobject2-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext help2man

Requires:	python-mutagen >= 1.8
Requires:	dbus-python
Requires:	gstreamer-python >= 0.10
Requires:	pygtk2
Requires:	pygobject2
Requires:	python-CDDB
Requires:	udisks2

BuildArch:	noarch

%description
Exaile is a media player aiming to be similar to KDE's AmaroK, but for GTK+.
It incorporates many of the cool things from AmaroK (and other media players)
like automatic fetching of album art, handling of large libraries, lyrics
fetching, artist/album information via the wikipedia, last.fm support, optional
iPod support (assuming you have python-gpod installed).

In addition, Exaile also includes a built in shoutcast directory browser,
tabbed playlists (so you can have more than one playlist open at a time),
blacklisting of tracks (so they don't get scanned into your library),
downloading of guitar tablature from fretplay.com, and submitting played tracks
on your iPod to last.fm

%prep
%setup -q -n %{name}-%{version}
#%patch0 -p0 -b .fix
#%patch1 -p0 -b .udisk

%build
make %{?_smp_mflags}
 
%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_datadir}/appdata/
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
#make install PREFIX=%{_prefix} LIBINSTALLDIR=%{_datadir} DESTDIR=%{buildroot} PYTHON2_CMD=%{_bindir}/python

desktop-file-install --delete-original			\
	--dir=%{buildroot}%{_datadir}/applications	\
	%{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/exaile
/usr/lib/exaile
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/exaile.png
%{_datadir}/exaile/
%{_datadir}/appdata/exaile.appdata.xml
%{_datadir}/dbus-1/services/org.exaile.Exaile.service
%config(noreplace) %{_sysconfdir}/xdg/exaile/
%{_mandir}/man1/exaile*.*

%changelog
* Mon Dec 15 2014 Nux <rpm@li.nux.ro> - 3.4.2-1
- update to 3.4.2

* Mon Sep 08 2014 Nux <rpm@li.nux.ro> - 3.4.0-1
- update to 3.4.0 stable release

* Thu Aug 07 2014 Nux <rpm@li.nux.ro> - 3.4.0-0.1.beta3
- 3.4.0 beta 3

* Fri Feb 21 2014 Deji Akingunola <dakingun@gmail.com> - 3.3.2-1
- Update to 3.3.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 08 2013 Jon Ciesla <limburgher@gmail.com> - 3.3.1-3
- Drop desktop vendor tag.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Deji Akingunola <dakingun@gmail.com> - 3.3.1-1
- Update to 3.3.1

* Mon Sep 24 2012 Deji Akingunola <dakingun@gmail.com> - 3.3.0-1
- Update to 3.3.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Deji Akingunola <dakingun@gmail.com> - 0.3.2.2-2
- Place exaile's private modules in %datadir
- Trim (un-necessary?) requires

* Wed Aug 31 2011 Deji Akingunola <dakingun@gmail.com> - 0.3.2.2-1
- Update to 0.3.2.2
- Drop hal. Apply patch to support udisk from upstream bzr's udisk branch

* Thu Mar 03 2011 Deji Akingunola <dakingun@gmail.com> - 0.3.2.1-1
- Update to 0.3.2.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jun 28 2010 Deji Akingunola <dakingun@gmail.com> - 0.3.2.0-1
- Update to 0.3.2.0

* Wed Jun 09 2010 Deji Akingunola <dakingun@gmail.com> - 0.3.1.2-1
- Update to 0.3.1.2

* Fri Apr 09 2010 Deji Akingunola <dakingun@gmail.com> - 0.3.1.1-1
- Update to 0.3.1.1

* Sat Mar 20 2010 Deji Akingunola <dakingun@gmail.com> - 0.3.1.0-1
- Update to 0.3.1.0

* Wed Nov 25 2009 Deji Akingunola <dakingun@gmail.com> - 0.3.0.2-1
- Update to 0.3.0.2

* Wed Sep 30 2009 Deji Akingunola <dakingun@gmail.com> - 0.3.0.1-1
- Update to 0.3.0.1

* Fri Aug 28 2009 Deji Akingunola <dakingun@gmail.com> - 0.3.0-1
- Update to 0.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.14-2
- Rebuild for Python 2.6

* Thu Oct 09 2008 Deji Akingunola <dakingun@gmail.com> - 0.2.14-1
- Update to 0.2.14

* Fri Jul 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.2.13-3
- fix license tag

* Mon Jul 07 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.2.13-2
- fix conditional comparison
- add sparc64 to 64bit arch check

* Wed Apr 02 2008 Deji Akingunola <dakingun@gmail.com> - 0.2.13-1
- Update to 0.2.13

* Sun Feb 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.2.11.1-2
- Rebuild for gcc43

* Thu Nov 29 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.11.1-1
- Update to 0.2.11.1 that removes bogus cruft from 0.2.11 source tarball
- Rebuild for firefox-2.0.0.10

* Tue Nov 06 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.11-2
- Rebuild for firefox-2.0.0.9

* Mon Oct 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.11-1
- New release

* Tue Sep 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.10-3
- Require pygtk2-libglade (BZ #278471)

* Wed Aug 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.10-2
- Rebuild

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.10-2
- License tag update

* Sat Jun 30 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.10-1
- New release

* Fri Mar 30 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.9-1
- New release

* Tue Jan 09 2007 Deji Akingunola <dakingun@gmail.com> - 0.2.8-1
- New release

* Sat Dec 30 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.7-1
- New release

* Wed Dec 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.6-3
- Rework the python include patch

* Wed Dec 27 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.6-2
- Rewrite the build patch to be more generic

* Tue Dec 26 2006 Deji Akingunola <dakingun@gmail.com> - 0.2.6-1
- First version for Fedora Extras
