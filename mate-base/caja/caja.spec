# Conditional for release and snapshot builds. Uncomment for release-builds.
%global rel_build 1

# This is needed, because src-url contains branched part of versioning-scheme.
%global branch 1.12

# Settings used for build from snapshots.
%{!?rel_build:%global commit ee0a62c8759040d84055425954de1f860bac8652}
%{!?rel_build:%global commit_date 20140223}
%{!?rel_build:%global shortcommit %(c=%{commit};echo ${c:0:7})}
%{!?rel_build:%global git_ver git%{commit_date}-%{shortcommit}}
%{!?rel_build:%global git_rel .git%{commit_date}.%{shortcommit}}
%{!?rel_build:%global git_tar %{name}-%{version}-%{git_ver}.tar.xz}

Name:        caja
Summary:     File manager for MATE
Version:     %{branch}.7
%if 0%{?rel_build}
Release:     1%{?dist}
%else
Release:     0.1%{?git_rel}%{?dist}
%endif
License:     GPLv2+ and LGPLv2+
Group:       User Interface/Desktops
URL:         http://mate-desktop.org

# for downloading the tarball use 'spectool -g -R caja.spec'
# Source for release-builds.
%{?rel_build:Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz}
# Source for snapshot-builds.
%{!?rel_build:Source0:    http://git.mate-desktop.org/%{name}/snapshot/%{name}-%{commit}.tar.xz#/%{git_tar}}

Patch0:         caja_add-xfce-to-desktop-file.patch

BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  exempi-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  cairo-gobject-devel
BuildRequires:  libexif-devel
BuildRequires:  libselinux-devel
BuildRequires:  libSM-devel
BuildRequires:  libxml2-devel
BuildRequires:  mate-common
BuildRequires:  mate-desktop-devel
BuildRequires:  pangox-compat-devel
BuildRequires:  startup-notification-devel
BuildRequires:  unique-devel

Requires:   gamin
Requires:   filesystem
Requires:   redhat-menus
Requires:   gvfs

# the main binary links against libcaja-extension.so
# don't depend on soname, rather on exact version
Requires:       %{name}-extensions%{?_isa} = %{version}-%{release}

# needed for using mate-text-editor as stanalone in another DE
Requires:       %{name}-schemas%{?_isa} = %{version}-%{release}

%description
Caja (mate-file-manager) is the file manager and graphical shell
for the MATE desktop,
that makes it easy to manage your files and the rest of your system.
It allows to browse directories on local and remote file systems, preview
files and launch applications associated with them.
It is also responsible for handling the icons on the MATE desktop.

%package extensions
Summary:  Caja extensions library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description extensions
This package provides the libraries used by caja extensions.

# needed for using mate-text-editor (pluma) as stanalone in another DE
%package schemas
Summary:  Caja schemas
License:  LGPLv2+

%description schemas
This package provides the gsettings schemas for caja.

%package devel
Summary:  Support for developing Caja extensions
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides libraries and header files needed
for developing caja extensions.

%prep
%setup -q%{!?rel_build:n %{name}-%{commit}}

%patch0 -p1 -b .add-xfce-to-desktop-file

%if 0%{?rel_build}
#NOCONFIGURE=1 ./autogen.sh
%else # 0%{?rel_build}
# for snapshots
# needed for git snapshots
NOCONFIGURE=1 ./autogen.sh
%endif # 0%{?rel_build}

%build
%configure \
        --disable-static \
        --enable-unique \
        --disable-schemas-compile \
        --with-x \
        --with-gtk=2.0 \
        --disable-update-mimedb

#drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags} V=1

%install
%{make_install}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/.icon-theme.cache

mkdir -p $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0

desktop-file-install                              \
    --delete-original                             \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
$RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# remove needless gsettings convert file
rm -f  $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/caja.convert

# Avoid prelink to mess with caja - rhbz (#1228874)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d
cat << EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/caja.conf
-b %{_libdir}/caja/
-b %{_libdir}/libcaja-extension.so.*
-b %{_libexecdir}/caja-convert-metadata
-b %{_bindir}/caja
-b %{_bindir}/caja-autorun-software
-b %{_bindir}/caja-connect-server
-b %{_bindir}/caja-file-management-properties
EOF

%find_lang %{name} --with-gnome --all-name


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
  /bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
  /usr/bin/update-desktop-database &> /dev/null || :
  /usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%post extensions -p /sbin/ldconfig

%postun extensions -p /sbin/ldconfig

%postun schemas
if [ $1 -eq 0 ]; then
  /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans schemas
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :


%files
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_bindir}/*
%{_datadir}/caja
%{_libdir}/caja/
%{_sysconfdir}/prelink.conf.d/caja.conf
%{_datadir}/pixmaps/caja/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/caja.*
%{_datadir}/icons/hicolor/*/emblems/emblem-note.png
%{_mandir}/man1/*
%{_libexecdir}/caja-convert-metadata
%{_datadir}/appdata/caja.appdata.xml
%{_datadir}/mime/packages/caja.xml
%{_datadir}/dbus-1/services/org.mate.freedesktop.FileManager1.service

%files extensions
%{_libdir}/libcaja-extension.so.*
%{_libdir}/girepository-1.0/*.typelib

%files schemas -f %{name}.lang
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

%files devel
%{_includedir}/caja/
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir
%{_datadir}/gtk-doc/html/libcaja-extension


%changelog
* Wed Mar 30 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.7-1
- update to 1.12.7 release
- fix long out standing fg color issue with dark themes

* Fri Feb 19 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.4-1
- update to 1.12.4 release
- add missing BR cairo-gobject-devel

* Sun Dec 27 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.2-2
- try fix rhbz (#1291540)

* Sun Dec 27 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.2-1
- update to 1.12.2 release

* Fri Sep 25 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.4-1
- update to 1.10.4 release

* Tue Jul 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.3-1
- update to 1.10.3 release

* Sat Jul 18 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-1
- update to 1.10.2 release
- remove upstreamed patches

* Mon Sep 29 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.2-1
- update to 1.8.2 release
- removed upstreamed caja_font-color-desktop.patch

* Sun Sep 14 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1 release
- remove upstreamed patches
- remove non needed obsoletes for epel7
- use '--with-gnome --all-name' for find language

* Sat Mar 22 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- fix for x-caja-window issue, end of a long story
- remove consolekit usage
- don't use caja-autostart script anymore

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0
- Turn autoreconf bit back on. This is still needed for rpath issue.

* Sun Feb 23 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.91-0.1.git20140223.ee0a62
- update to latest git snapshot from 2014.02.23
- remove debuging patch, fix rhbz (#1067234)
- move autoreconf to the right place
- remove delay from caja-autostart for testing proposal
- remove non existent COPYING-DOCS
- disable gtk-docs for dit snapshot builds

* Wed Feb 12 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-2
- Add autoreconf -fi to fix rpath issues.

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Tue Jan 14 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1
- remove glib-2.39 fix, already fixed in upstream
- use gtk-docs for release build

* Tue Dec 17 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.6.git20131201.0ef48fa
- fix build against new glib2-39.2, 'g_memmove' is removed
- https://git.gnome.org/browse/glib/commit/?id=6e4a7fca431f53fdfd89afbe956212229cf52200

* Tue Dec 17 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.5.git20131201.0ef48fa
- new patch for x-caja-window issue, it surpress creating x-caja-desktop-windows
- rename patches
- fix provides
- use modern 'make install' macro
- make Maintainers life easier and use better git snapshot usage, Thanks to Bj??rn Esser

* Sun Dec 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.4.git0ef48fab
- add mimeinfo rpm scriplets again

* Sun Dec 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.3.git0ef48fab
- fix usage of %%{buildroot}
- use desktop-database rpm scriptlet instead of mimeinfo scriptlet

* Sat Dec 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.2.git0ef48fab
- fix all the macro-in-comment warnings
- add ldconfig scriptlets for the extension subpackage
- add versioned provides for the obsoleted packages
- remove licence tags from subpackages
- remove group tags from subpackages
- fix permission for caja-autostart script

* Thu Dec 05 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.git0ef48fab
- rename mate-file-manager to caja for f21
- use latest git snapshot, 2013.12.05

* Thu Dec 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Oct 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.7.gitbf47018
- add add autostart script to desktop file

* Thu Oct 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.6.gitbf47018
- add a 3 secs delay for caja autostart and restart if killed

* Mon Oct 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.5.gitbf47018
- add new caja-sidebar design for f20

* Mon Oct 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.4.gitbf47018
- allow dropping files to bookmarks
- fix https://github.com/mate-desktop/mate-file-manager/issues/122

* Sun Oct 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.3.gitbf47018
- fix caja crash if closing properties windows on dropbox folder

* Sun Sep 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.2.git73cc7e9
- update latest git snapshot
- fix rhbz (#1005660)
- change open folders in spatial-mode
- fix spatial mode crash and shift+double click
- https://github.com/mate-desktop/mate-file-manager/issues/120
- https://github.com/mate-desktop/mate-file-manager/issues/161
- fixed thumbnail frame not being displayed for some files
- https://github.com/mate-desktop/mate-file-manager/issues/135

* Wed Sep 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.1.git6278dcb
- update latest git snapshot
- fix rhbz (959444)
- remove upstreamed mate-file-manager_fix_privat-icons-dir.patch

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-3
- move gsettings schemas to -schemas subpackage, to fix #959607
- move locale to -schemas subpackage
- remove runtime require hicolor-icon-theme

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-1
- update to new upstream release
- remove in release included mate-file-manager_fix-radio-buttons.patch
- add  upstream mate-file-manager_fix_privat-icons-dir.patch
- remove needless runtime require gsettings-desktop-schemas
- remove runtime require mate-icon-theme

* Mon Jul 01 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-9
- set autostart to false in caja-autostart, fix rhbz #969663
- and #978598

* Sun Jun 30 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-8
- add mate-file-manager_fix-radio-buttons.patch to fix rhbz #964357
- clean up BR's
- add runtime require hicolor-icon-theme
- revert 1.6.1-7 changes

* Thu Jun 20 2013 Dan Mashal <dan.mashal@fedoraproejct.org> - 1.6.1-7
- Try caja without the autostart file (886029)

* Sat Jun 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-6
- remove gsettings convert file

* Thu Jun 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-5
- add AutostartCondition to caja-autostart.desktop

* Wed May 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-4
- workaround for x-caja-desktop window issue
- add caja-autostart desktopfile to /etc/xdg/autostart

* Wed May 15 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-3
- Fix previous commit

* Tue May 14 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-2
- Own libdir/caja (961992)

* Thu Apr 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release.

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Mar 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
- Update to latest upstream release

* Sat Mar 02 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-1
- Update to latest upstream release
- Add upstream patch

* Mon Dec 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 release
- Drop all patches
- Update configure flags
- Clean up spec file

* Sun Nov 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-2
- upload source again as upstream switched it
- specfile cleanup

* Fri Nov 23 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1 release
- drop upstream commits patch and other merged patch
- change source url and fix packagename in %%prep to suit

* Thu Nov 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-6
- update commits patch

* Tue Nov 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-5
- add git commits rollup patch, hopefully it fixes rhbz 868472
- drop merged patch

* Mon Nov 19 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-4
- This change was reverted

* Sun Nov 11 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-3
- add patch to call gdk_pixbuf_loader_close() earlier (#558267)
- fix mistake in scriptlets

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-2
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- add schema scriptlets and remove mateconf scriptlets
- drop un-needed requires and build requires and change style
- make directory for extensions and move to main package
- drop all patches not needed for building for now
- clean up spec file

* Thu Oct 18 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-12
- fix mate-doc xml error (patch out reference to non-existent caja-extension-i18n.xml)
- verbose build

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-11
- Drop caja_remove_mate-bg-crossfade patch as it was causing crash

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-10
- add patch to try and fix crash

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-9
- revert last commit "add autostart file for caja desktop"
- add no session delay patch

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-8
- add autostart file for caja desktop
- add build requires libxml2-devel

* Mon Aug 20 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-7
- remove obsoleting stuff

* Thu Aug 16 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-6
- drop needless ldconfig scriptlet on main pkg

* Mon Aug 13 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-5
- fix desktop file handle
- fix obsolete caja from external repo

* Sun Aug 12 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-4
- correct %%build section
- correct rpm scriplets
- correct %%prep section
- change .*z to .* in %%file section
- correct obsoletes
- some other fixes

* Sun Aug 12 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-3
- obsoleting caja from external repo
- remove unecessary build requires

* Tue Aug 07 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-2
- initial package for fedora

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- mate-file-manager.spec based on nautilus-2.32.0-1.fc14 spec

