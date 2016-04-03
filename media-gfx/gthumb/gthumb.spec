Summary: Image viewer, editor, organizer
Name: gthumb
Version: 3.2.4
Release: 1%{?dist}
URL: https://wiki.gnome.org/Apps/gthumb
Source0: http://download.gnome.org/sources/gthumb/3.2/%{name}-%{version}.tar.xz
# Change default parameters for image resizing to better values
# (the current default of 640% is misleading)
# https://bugzilla.gnome.org/show_bug.cgi?id=710479
Patch0: gthumb-3.2.4-resize.patch
License: GPLv2+
Group: User Interface/X

BuildRequires: gtk3-devel
BuildRequires: glib2-devel 
BuildRequires: exiv2-devel 
Buildrequires: libopenraw-gnome-devel
BuildRequires: clutter-gtk-devel
BuildRequires: gstreamer1-devel
BuildRequires: gstreamer1-plugins-base-devel
BuildRequires: intltool
BuildRequires: gnome-doc-utils 
BuildRequires: libSM-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: brasero-devel
BuildRequires: libsoup-devel
BuildRequires: gnome-common
BuildRequires: rarian-compat
BuildRequires: librsvg2-devel
BuildRequires: gsettings-desktop-schemas-devel
BuildRequires: itstool
BuildRequires: libwebp-devel
BuildRequires: libsecret-devel
BuildRequires: webkitgtk3-devel
# For Web albums extension
BuildRequires: bison flex

Requires: hicolor-icon-theme

%description
gthumb is an application for viewing, editing, and organizing
collections of images.

%package devel
Summary: Header files needed for developing gthumb extensions
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The gthumb-devel package includes header files for the gthumb
package.

%prep
%setup -q
%patch0 -p1 -b.resize

%build
%configure --enable-libopenraw --disable-static

# drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' -e 's/    if test "$export_dynamic" = yes && test -n "$export_dynamic_flag_spec"; then/      func_append compile_command " -Wl,-O1,--as-needed"\n      func_append finalize_command " -Wl,-O1,--as-needed"\n\0/' libtool

make %{?_smp_mflags}

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT/var/lib/scrollkeeper

%find_lang %{name} --with-gnome

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/gthumb/
%{_datadir}/glib-2.0/schemas/org.gnome.gthumb*
# Co own these directories instead of pulling in GConf
# after all, we are trying to get rid of GConf with these files
%dir %{_datadir}/GConf
%dir %{_datadir}/GConf/gsettings
%{_datadir}/GConf/gsettings/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/gthumb.png
%{_datadir}/icons/hicolor/scalable/apps/gthumb.svg
%{_libdir}/gthumb/
%{_mandir}/man?/gthumb*

%files devel
%defattr(-,root,root,-)
%{_includedir}/gthumb-3.2/
%{_libdir}/pkgconfig/gthumb-3.2.pc
%{_datadir}/aclocal/*

%changelog
* Tue Oct 15 2013 Christian Krause <chkr@fedoraproject.org> - 3.2.4-1
- New upstream release 3.2.4 (rhbz#1019097, rhbz#1018895)
- Drop upstreamed patches
- Add patch for better default parameters (rhbz#1006245)

* Sat Aug 24 2013 Christian Krause <chkr@fedoraproject.org> - 3.2.3-5
- Added upstream patch to fix a crash in the find-duplicates
  extension (rhbz#1000559)

* Mon Aug 19 2013 Christian Krause <chkr@fedoraproject.org> - 3.2.3-4
- Added upstream patch to fix a crash in gthumb's file manager
  (rhbz#995551)
- Added a patch to fix a crash when using the Audio/Video
  extension (rhbz#995724)

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.2.3-3
- Rebuilt for cogl 1.15.4 soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Christian Krause <chkr@fedoraproject.org> - 3.2.3-1
- New upstream release 3.2.3 (rhbz#952572)
- Fix some "bogus dates" in %%changelog (reported by rpmlint)

* Mon May 13 2013 Christian Krause <chkr@fedoraproject.org> - 3.2.2-1
- New upstream release 3.2.2

* Thu May 02 2013 Christian Krause <chkr@fedoraproject.org> - 3.2.1-1
- New upstream release 3.2.1 (rhbz#952572)

* Fri Mar 29 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.2.0-2
- Fix building with gstreamer support.
- Enable web services, webp, and libsecret support.

* Thu Mar 28 2013 Christian Krause <chkr@fedoraproject.org> - 3.2.0-1
- New upstream release 3.2.0 (rhbz#860359)
- Remove unused patches
- Minor cleanup

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.2-6
- Rebuild for new cogl

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 3.0.2-5
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 3.0.2-4
- rebuild against new libjpeg

* Thu Sep  6 2012 Hans de Goede <hdegoede@redhat.com> - 3.0.2-3
- Really rebuild for new cogl (buildroot override was missing)

* Tue Sep  4 2012 Hans de Goede <hdegoede@redhat.com> - 3.0.2-1
- New upstream release 3.0.2 (rhbz#849882)
- Rebuild for new cogl (rhbz#825507)
- Drop the obsolete unique BR (rhbz#852407)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Christian Krause <chkr@fedoraproject.org> - 3.0.1-1
- Update to 3.0.1 (#821670)

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 3.0.0-2
- rebuild (exiv2)

* Sun Apr 29 2012 Christian Krause <chkr@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0 (#802954)
- Remove unused patches

* Tue Mar 27 2012 Christian Krause <chkr@fedoraproject.org> - 2.14.3-1
- Update to 2.14.3

* Sun Jan 29 2012 Christian Krause <chkr@fedoraproject.org> - 2.14.2-1
- Update to 2.14.2 (#784234)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jan 01 2012 Christian Krause <chkr@fedoraproject.org> - 2.14.1-1
- Update to 2.14.1 (#760061)

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.14.0-2
- Rebuild for new libpng

* Thu Oct 27 2011 Christian Krause <chkr@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0 (#683408)

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.13.91-4
- rebuild (exiv2)

* Fri Oct 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.13.91-3
- and again

* Fri Oct 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.13.91-2
- Rebuild for new clutter-gtk010

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Wed May 04 2011 Christian Krause <chkr@fedoraproject.org> - 2.12.3-2
- Build against clutter-gtk010 until gthumb is ported to GTK3

* Sat Apr 23 2011 Christian Krause <chkr@fedoraproject.org> - 2.12.3-1
- Update to 2.12.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Christian Krause <chkr@fedoraproject.org> - 2.12.2-1
- Update to 2.12.2 (#669612)
- Drop 4 upstreamed patch

* Sun Jan 02 2011 Christian Krause <chkr@fedoraproject.org> - 2.12.1-3
- Rebuilt against new exiv2
- Added upstream patch for changed API in exiv2-0.21

* Tue Dec 14 2010 Christian Krause <chkr@fedoraproject.org> - 2.12.1-2
- Temporarily disable usage of brasero to avoid mixed linkage of
  GTK+-2.x and GTK+-3.x (#662793)

* Wed Nov 17 2010 Christian Krause <chkr@fedoraproject.org> - 2.12.1-1
- Update to 2.12.1 (#654748)
- Add 3 upstream patches (to fix bgo: #635475 and two other minor bugs)

* Wed Oct 06 2010 Christian Krause <chkr@fedoraproject.org> - 2.12.0-1
- Update to 2.12.0

* Fri Sep 24 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.11.91-3
- Merge-review cleanup (#225867)

* Thu Sep 02 2010 Christian Krause <chkr@fedoraproject.org> - 2.11.91-2
- Rebuild against new clutter

* Tue Aug 31 2010 Christian Krause <chkr@fedoraproject.org> - 2.11.91-1
- Update to 2.11.91 (#628892)
- Drop upstreamed patch

* Sun Aug 22 2010 Christian Krause <chkr@fedoraproject.org> - 2.11.90-3
- Fix compilation against new libbrasero-burn

* Sun Aug 22 2010 Christian Krause <chkr@fedoraproject.org> - 2.11.90-2
- Spec file cleanup
- Add BR for Web albums extension (#620707)

* Tue Aug 17 2010 Matthias Clasen <mclasen@redhat.com> 2.11.90-1
- Update to 2.11.90

* Fri Aug  6 2010 Matthias Clasen <mclasen@redhat.com> 2.11.6-1
- Update to 2.11.6

* Tue Jul 20 2010 Bastien Nocera <bnocera@redhat.com> 2.11.5-2
- Force compile against newer brasero-media

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.5-1
- Update to 2.11.5

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.4-1
- Update to 2.11.4

* Fri Jun 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.3-3
- Rebuild against new brasero

* Mon May 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.11.3-2 
- rebuild (exiv2)

* Thu Apr 15 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.11.3-1
- Update to 2.11.3

* Mon Apr 12 2010 Hans de Goede <hdegoede@redhat.com> - 2.11.2-2
- Don't ship our own gthumb-importer.desktop and gthumb-importer script, the
  gvfs unmounting these were created for, is unwanted now that gthumb itself
  uses gvfs. The gvfs unmounting now actually stops non mass storage cameras
  (ptp or proprietary protocols) from working (related #533691)

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.2-1
- Update to 2.11.2

* Mon Feb  8 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.11.1-5
- Fix extension linking with --as-needed (#562243)

* Wed Feb  3 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.11.1-4
- Enable clutter and gstreamer integration

* Wed Jan  6 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.1-3
- Use my CFLAGS, dammit

* Wed Jan  6 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.1-2
- Fix up some spec file issues

* Mon Jan  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to 2.11.1

* Mon Aug  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.10.11-6
- Drop unneeded direct deps

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.10.11-4
- Rebuild to shrink GConf schemas

* Fri Apr 10 2009 Matthias Clasen <mclasen@redhat.com> - 2.10.11-3
- Fix directory ownership

* Fri Mar 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.10.11-2
- Fix the photo import location (#492179)

* Fri Feb 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.10.11-1
- Update to 2.10.11

* Thu Feb 26 2009 Matthias Clasen <mclasen@redhat.com> - 2.10.10-5
- Make it build

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 23 2008 Matthias Clasen  <mclasen@redhat.com> - 2.10.10-3
- Avoid tons of GTK+ warnings

* Mon Sep 22 2008 Matthias Clasen  <mclasen@redhat.com> - 2.10.10-1
- Update to 2.10.10

* Tue Aug  5 2008 Matthias Clasen  <mclasen@redhat.com> - 2.10.9-1
- Update to 2.10.9

* Fri Jul 18 2008 Matthias Clasen  <mclasen@redhat.com> - 2.10.8-4
- Try to fix a crash (#453181)

* Fri May  2 2008 David Zeuthen <davidz@redhat.com> - 2.10.8-3
- Drop x-content patch and provide gthumb-importer and a desktop
  file for it (#444635)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.10.8-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.10.8-1
- Update to 2.10.8

* Fri Jan 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.10.7-2
- Add content-type support

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.7-1
- Update to 2.10.7 (bug fixes)

* Tue Oct  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.6-2
- Fix rotation of images with # in their name (#248708)

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.6-1
- Update to 2.10.6

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.10.5-5
- Rebuild for selinux ppc32 issue.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 2.10.5-4
- Rebuild for PPC toolchain bug

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.5-3
- Update the license field
- Use %%find_lang for help files

* Fri Jul  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.5-2
- Fix a directory ownership issue

* Wed Jun 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.5-1
- Update to 2.10.5

* Tue Jun 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.4-1
- Update to 2.10.4

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.3-1
- Update to 2.10.3
- Drop upstreamed patch

* Wed May  9 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.2-3
- Add dependency on libopenraw-gnome (#236184)

* Thu May  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.2-2
- Add dependency on libiptcdata (#127690)

* Fri Apr 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.2-1
- Update to 2.10.2
- 
* Mon Apr  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.0-3
- Use the PICTURES user dir as default location for photo import

* Fri Mar 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.0-2
- Remove a no-longer needed patch (#233350)

* Tue Mar 20 2007 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1
- Update to 2.10.0

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.9.3-1
- Update to 2.9.3

* Wed Feb 21 2007 Matthias Clasen <mclasen@redhat.com> - 2.9.2-1
- Update to 2.9.2
- Move libgthumb.so out of libdir

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.9.1-1
- Update to 2.9.1

* Sun Oct 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.9-1
- Update to 2.7.9

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.8-4
- fix up requires (#202549)

* Thu Sep  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.8-3
- fix directory ownership issues (#205682)

* Mon Aug  7 2006 Jindrich Novy <jnovy@redhat.com> - 2.7.8-2.fc6
- fix URL in Source0

* Wed Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.8-1.fc6
- Update to 2.7.8
- Fix some documentation inaccuracies (#175165)

* Fri Jul 14 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.7-4
- Don't BR gphoto2-devel on s390

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.7.7-3
- rebuild
- Don't get gphoto2 on s390(x)

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.7-2  
- Update to 2.7.7  

* Thu Apr 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.6-2  
- Update to 2.7.6  

* Fri Mar 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.5.1-2
- Update to 2.7.5.1

* Mon Mar 20 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.5-1
- Update to 2.7.5

* Thu Mar  2 2006 Ray Strode <rstrode@redhat.com> - 2.7.3-2
- Make saving work again (bug 183141)

* Wed Feb 15 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.3-1
- Update to 2.7.3
- BuildRequire libgphoto2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.7.2-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.7.2-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Ray Strode <rstrode@redhat.com> - 2.7.2-2
- drop redhat-menus buildrequires
- use make install DESTDIR instead %%makeinstall

* Wed Jan  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.7.2-1
- Update to 2.7.2
- Drop upstreamed patches

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 2.7.1-1.1
- rebuilt

* Sun Nov 13 2005 Matthias Clasen <mclasen@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Wed Oct 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.8-2
- Use GTK+ stock icons where available

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.8-1
- Update to 2.6.8

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.7-1
- Update to 2.6.7

* Thu Aug 18 2005 John (J5) Palmieri <johnp@redhat.com> - 2.6.2-2
- Bump and rebuild for cairo ABI changes

* Fri Jul 15 2005 Matthias Clasen <mclasen@redhat.com> - 2.6.6-1
- Newer upstream version

* Mon May 16 2005 John (J5) Palmieri <johnp@redhat.com> - 2.6.5-1
- Minor updated that fixes a couple of bugs and adds some translations

* Mon Mar 28 2005 Matthias Clasen <mclasen@redhat.com> 
- Rebuild against newer libexif

* Wed Mar 16 2005 John (J5) Palmieri <johnp@redhat.com> - 2.6.4-1
- Update to upstream version 2.6.4

* Thu Mar  3 2005 Marco Pesenti Gritti <mpg@redhat.com> 2.6.3-2
- Rebuild

* Mon Jan 31 2005 Matthias Clasen <mclasen@redhat.com> 2.6.3
- Update to 2.6.3

* Tue Nov  9 2004 Marco Pesenti Gritti <mpg@redhat.com> 2.6.0.1-2
- Use upstream desktop file, it has translations and mime

* Sun Oct 31 2004 Christopher Aillon <caillon@redhat.com> 2.6.0.1-1
- Update to 2.6.0.1

* Thu Sep 30 2004 Christopher Aillon <caillon@redhat.com> 2.4.2-3
- PreReq desktop-file-utils >= 0.9

* Wed Sep 29 2004 Ray Strode <rstrode@redhat.com> 2.4.2-2
- Move gthumb.desktop to redhat-menus (#131726)
- Require recent desktop-file-utils
- Call update-desktop-database from %%postun

* Mon Sep 13 2004 Christopher Aillon <caillon@redhat.com> 2.4.2-1
  - gthumb.desktop: Add supported mime types (#131740)
  - gthumb.spec: Run update-desktop-database (#131740)
  - Update to 2.4.2

* Mon Aug 23 2004 Christopher Aillon <caillon@redhat.com> 2.4.1-2
- Only use catalog view if the directory has an image file present (alexl)

* Wed Aug 11 2004 Christopher Aillon <caillon@redhat.com> 2.4.1-1
- Update to 2.4.1

* Tue Jun 29 2004 Christopher Aillon <caillon@redhat.com> 2.4.0-1
- Update to 2.4.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Warren Togami <wtogami@redhat.com> 2.3.2-2
- #111001 BR: libgnomeui-devel gettext libpng-devel
  BR or missing features: gphoto2-devel libjpeg-devel libtiff-devel

* Fri Apr  2 2004 Mark McLoughlin <markmc@redhat.com> 2.3.2-1
- Update to 2.3.2

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.3.1-1
- update to 2.3.1

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec 22 2003 Matt Wilson <msw@redhat.com> 2.2.0-1
- 2.2.0

* Wed Jul  9 2003 Havoc Pennington <hp@redhat.com> 2.0.2-1
- 2.0.2
- buildreq libgnomeprint

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 2.0.1-1
- 2.0.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Havoc Pennington <hp@redhat.com>
- 1.108
- disable schema install during makeinstall

* Thu Jan 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- require scrollkeeper

* Mon Dec 16 2002 Havoc Pennington <hp@redhat.com>
- rebuild

* Thu Dec 12 2002 Havoc Pennington <hp@redhat.com>
- Initial build.


