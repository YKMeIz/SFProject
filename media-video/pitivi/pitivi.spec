%global major 0.94
%global minor 2

Name:		pitivi
Version:	%{major}
Release:	4%{?dist}
Summary:	Non-linear video editor
Group:		Applications/Multimedia
License:	LGPLv2+
URL:		http://www.pitivi.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pitivi/%{major}/pitivi-%{version}.tar.xz
#Patch0:		pitivi-0.15.0-ignore-unknown-stream-types.patch
BuildRequires:	intltool >= 0.35.0
BuildRequires:	python3
BuildRequires:	desktop-file-utils
BuildRequires:	gnome-doc-utils >= 0.18.0
BuildRequires:	itstool
#BuildRequires:	libappstream-glib
BuildRequires:	python3-cairo-devel

Requires:	gstreamer1
Requires:	gnonlin >= 1.4.0
Requires:	gstreamer1-plugins-good
Requires:	python3-gstreamer1
Requires:	gst-editing-services
Requires:	pygtk2 >= 2.17.0
Requires:	python-setuptools
Requires:	hicolor-icon-theme
Requires:	pyxdg
Requires:	frei0r-plugins
Requires:	python3-numpy
Requires:	yelp
Requires:	pycairo >= 1.0.0
Requires:	libnotify
Requires:	python3-canberra
Requires:	gobject-introspection
Requires:	pygobject3
Requires:	clutter-gtk
Requires:	clutter-gst2

#BuildArch:	noarch

%description
Pitivi is an application using the GStreamer multimedia framework to
manipulate a large set of multimedia sources.

At this level of development it can be compared to a classic video editing
program. 

%prep
%setup -q

#%patch0 -p0 -b .unknown_types

%build
%configure --libdir=%{_datadir}

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
desktop-file-edit --add-category "Video" $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

find $RPM_BUILD_ROOT -name '*.a' | xargs rm -f

mkdir -p $RPM_BUILD_ROOT%{python3_sitearch}/pitivi
mv $RPM_BUILD_ROOT%{_datadir}/pitivi/python/pitivi $RPM_BUILD_ROOT%{python3_sitearch}/
rmdir $RPM_BUILD_ROOT%{_datadir}/pitivi/python


%find_lang %{name}


%check
#appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/appdata/%{name}.appdata.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    touch --no-create %{_datadir}/mime/packages &> /dev/null || :
    update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README RELEASE
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/mime/packages/%{name}.xml
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/help/*
%{_datadir}/appdata/pitivi.appdata.xml
%{python3_sitearch}/pitivi/

%changelog
* Wed Nov 26 2014 Jon Ciesla <limburgher@gmail.com> - 0.94-4
- Move arch-specific Python module to the proper place, BZ 1167119.

* Mon Nov 10 2014 Debarshi Ray <rishi@fedoraproject.org> - 0.94-3
- Require python3-canberra and python3-gstreamer, instead of their python2
  counterparts.

* Fri Nov 07 2014 Jon Ciesla <limburgher@gmail.com> - 0.94-2
- Requires fixes.

* Tue Nov 04 2014 Jon Ciesla <limburgher@gmail.com> - 0.94-1
- 0.94, BZ 1160285.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.93-6
- update mime scriptlet
- %%check: validate .desktop/appdata

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 05 2014 Jon Ciesla <limburgher@gmail.com> - 0.93-4
- Require clutter-gst2, BZ 1093933.

* Wed Apr 02 2014 Jon Ciesla <limburgher@gmail.com> - 0.93-3
- Updated GES Requires to reflect reality.

* Fri Mar 28 2014 Jon Ciesla <limburgher@gmail.com> - 0.93-2
- Updated gnonlin Requires to reflect reality.

* Fri Mar 21 2014 Jon Ciesla <limburgher@gmail.com> - 0.93-1
- New upstream to support latest GES.

* Fri Mar 07 2014 Jon Ciesla <limburgher@gmail.com> - 0.92-2
- Drop unneeded Requires pygoocanvas and python-zope-interface,
- added gobject-introspection, pygobject3, BZ 1059916.
- added clutter-gtk, BZ 1073726.

* Fri Dec 06 2013 Jon Ciesla <limburgher@gmail.com> - 0.92-1
- Latest upstream, BZ 1013686.

* Fri Oct 11 2013 Jon Ciesla <limburgher@gmail.com> - 0.91-1
- Latest upstream, BZ 1013686.

* Tue Sep 03 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.2-5
- Add Video category to .desktop file.
- Date fix.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 03 2012 Jon Ciesla <limburgher@gmail.com> - 0.15.2-1
- New upstream, BZ 818690, regression fix.

* Mon Apr 09 2012 Jon Ciesla <limburgher@gmail.com> - 0.15.1-1
- New upstream, BZ 810765, multiple bugfixes.

* Tue Mar 27 2012 Jon Ciesla <limburgher@gmail.com> - 0.15.0-3
- Patch for unknown stream types, BZ 723653.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.15.0-1
- Update to 0.15.0
- Drop previously backported patches
- Disable tests since most of them require gtk

* Sun Sep 11 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.14.2-1
- Update to 0.14.2

* Thu Jun 30 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.14.0-3
- Do not allow presets to have the same name, fixes rhbz #717328

* Sun Jun 12 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.14.0-2
- Allow using "Default" as preset name, fixes rhbz #712700
- Lower pygtk2 min version to 2.17.0 so that we can push 0.14.0 to f14

* Thu Jun 02 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.14.0-1
- Update to 0.14
- Drop backported patches
- Remove BuildRoot tag and clean section
- Add patch to make sure welcome dialog apprears after the UI is loaded
- Fix license in some files headers

* Wed Dec 15 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.13.5-4
- Initialize pending new_segment to none, fixes rhbz #653062

* Wed Dec 08 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.13.5-3
- Add buildroot tag
- Clean buildroot in %%install section
- Add patch from lp #640630 to fix rhbz #654119
- Add man page
- Add %%check section
- Add pygobject2, gstreamer-python, gnonlin and gstreamer-plugins-good
  to BR so that we can run %%check

* Tue Dec 07 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 0.13.5-2
- Add scriptlet to update icon cache (rhbz #625580)

* Wed Sep 22 2010 Chen Lei <supercyper@163.com> - 0.13.5-1
- Update to 0.13.5

* Wed Aug 11 2010 David Malcolm <dmalcolm@redhat.com> - 0.13.4-3
- recompiling .py files against Python 2.7 (rhbz#623347)

* Mon Mar 15 2010 Benjamin Otte <otte@redhat.com> - 0.13.4-2
- Make sure Pitivi has an icon in the menu.

* Wed Mar 10 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.4-1.1
- Upload new tarball :)

* Wed Mar 10 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.4-1
- Update to 0.13.4

* Tue Mar  9 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.3.2-0.1
- Update to 0.13.3.2

* Fri Dec 11 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.3-3.3.837f0d73
- Make sure we have the correct source uploaded.

* Thu Dec 10 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.3-3.2.837f0d73
- Update to git master to see if this fixes anyone's problems
- Call update-desktop-database/update-mime-database in post/postun

* Thu Dec  3 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.3-3
- Add Req on python-setuptools for BZ#540192

* Wed Sep 23 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.13.3-2
- Update desktop file according to F-12 FedoraStudio feature

* Mon Sep 14 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.3-1
- 0.13.3 Release : ... we shall never (sur)render
-
- The PiTiVi team is proud to announce the second release in the
- unstable 0.13 PiTiVi series.
-
- Due to its dependency on GStreamer, The PiTiVi team strongly
- recommends users have all official latest gstreamer libraries and
- plugins installed for the best user experience.
-
- Title is from a quote by Winston Churchill “We shall defend our
- island, whatever the cost may be, we shall fight on the beaches, we
- shall fight on the landing grounds, we shall fight in the fields and
- in the streets, we shall fight in the hills; we shall never
- surrender.”
-
- Features of this release
-
-    * Fix rendering failures
-    * UI beautifications
-    * Switch to themeable ruler
-    * Speed optimisations
-    * Show the project name in the window title 

* Sat Aug 29 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.2.2-0.1
- Update to prerelease for 0.13.3
- Streamline BuildRequires

* Fri Aug 14 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.2-2
- Bump required version of gstreamer-python

* Thu Aug 13 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.2-1
- Update to 0.13.2 "Jailbreak (out of Deadlock City)"
- 
- The PiTiVi team is proud to announce the second release in the
- unstable 0.13 PiTiVi series.
- 
- Due to its dependency on GStreamer, The PiTiVi team strongly
- recommends users have all official latest gstreamer libraries and
- plugins installed for the best user experience.
- 
- Features of this release
- 
-    * Undo/Redo support
-    * Audio mixing
-    * Ripple/Roll edit
-    * misc fixes everywhere 

* Wed Aug 12 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1.3-1
- Update to latest prerelease.

* Mon Jul 27 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1.2-1
- Update to prerelease

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.1-1
- 0.13.1 Release "L'Aquila Immota Manet : The eagle remains unmoved"
- ------------------------------------------------------------------
- 
- The PiTiVi team is proud to announce the first release in the unstable 0.13
- PiTiVi series.
- 
- This release is in memory of those who have lost their lives, friends,
- houses in the April 6th 2009 earthquake in l'Aquila, Italy.
- 
- Due to its dependency on GStreamer, The PiTiVi team strongly
- recommends users have all official latest gstreamer libraries and
- plugins installed for the best user experience.
- 
- 
- * Features of this release
- 
-  * core rewrite
-  * multi-layered timeline
-  * trimming features
-  * audio waveforms and video thumbnails in timeline
-  * picture support
-  * New project file format support

* Thu May 21 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.13.0.2-1
- Upgrade to 0.13.1 prerelease

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.3-2
- Add patch from Denis Leroy to fix running with Python 2.6

* Mon Dec 15 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.3-1
- Update to 0.11.3

* Thu Dec  4 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.2.2-2
- Upload the sources

* Thu Dec  4 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.2.2-1
- Update to 0.11.2.2

* Sat Nov 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.2-2
- Rebuild for Python 2.6

* Wed Oct 15 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.2-1
- Update to 0.11.2

* Mon Oct 13 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.1.4-1
- Update to 0.11.1.4

* Mon Jan 14 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.1-2
- Add requirement for python-setuptools. (BZ#426855)

* Sat Dec  8 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.1-1
- Update to 0.11.1

* Sun Nov 11 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-2
- Add missing BR

* Wed Oct 17 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.11.0-1
- Update to 0.11.0

* Wed Jun 27 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.3-2
- Add versioned requires for gnonlin. (BZ#245981)

* Fri Jun 22 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.3-1
- Update to 0.10.3

* Mon May 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.2.2-3
- BR gettext

* Mon May 28 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.10.2.2-2
- BR perl(XML::Parser)
