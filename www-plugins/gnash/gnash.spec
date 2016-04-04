%filter_provides_in %{python_sitearch}/.*\.so$ 
%filter_setup

Name:           gnash
Version:        0.8.10
Release:        14%{?dist}
Epoch:          1
Summary:        GNU flash movie player

Group:          Applications/Multimedia
License:        GPLv3+
URL:            http://www.gnu.org/software/gnash/
Source0:        ftp://ftp.gnu.org/gnu/%{name}/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  libxml2-devel libpng-devel libjpeg-devel libogg-devel
BuildRequires:  boost-devel curl-devel freetype-devel fontconfig-devel
BuildRequires:  SDL-devel agg-devel
BuildRequires:  kdelibs-devel
BuildRequires:  gtkglext-devel pygtk2-devel
BuildRequires:  docbook2X gettext fop xmltex
BuildRequires:  docbook-utils-pdf
BuildRequires:  gstreamer-devel >= 0.10
BuildRequires:  giflib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  speex-devel gstreamer-plugins-base-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  mysql-devel
BuildRequires:  xulrunner-devel
BuildRequires:  GConf2-devel

BuildRequires:  autoconf automake libtool

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

# Patch0 :      http://www.mail-archive.com/gcc-bugs@gcc.gnu.org/msg338792.html
Patch0:         %{name}-%{version}-add-unistd-header.patch
# Patch1 :      Fix CVE-2012-1175
#               http://git.savannah.gnu.org/cgit/gnash.git/commit/?id=bb4dc77eecb6ed1b967e3ecbce3dac6c5e6f1527
Patch1:         %{name}-%{version}-integer-overflow.patch

Patch2:         %{name}-%{version}-boost-1.50.patch
Patch3:		gnash-0.8.10-includes.patch

%description
Gnash is capable of reading up to SWF v9 files and op-codes, but primarily
supports SWF v7, with better SWF v8 and v9 support under heavy development.
Gnash includes initial parser support for SWF v8 and v9. Not all 
ActionScript 2 classes are implemented yet, but all of the most heavily 
used ones are. Many ActionScript 2 classes are partially implemented; 
there is support for all of the commonly used methods of each
class.

%package plugin
Summary:   Web-client flash movie player plugin 
Requires:  %{name} = %{epoch}:%{version}-%{release}
Requires:  mozilla-filesystem%{?_isa} webclient
Group:     Applications/Internet

%description plugin
The gnash flash movie player plugin for Firefox or Mozilla.

%package klash
Summary:   Konqueror flash movie player plugin
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     Applications/Multimedia

%description klash
The gnash flash movie player plugin for Konqueror.

%package cygnal
Summary:   Streaming media server
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     Applications/Multimedia

%description cygnal
Cygnal is a streaming media server that's Flash aware.

%package devel
Summary:   Gnash header files
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     Development/Libraries

%description devel
Gnash header files can be used to write external Gnash extensions or to embed
the Gnash GTK+ widget into a C/C++ application.

%package -n python-gnash
Summary:   Gnash Python bindings
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     Applications/Multimedia

%description -n python-gnash
Python bindings for the Gnash widget. Can be used to embed Gnash into any PyGTK
application.

%package extension-fileio
Summary:   Fileio extension for Gnash
Group:     Applications/Multimedia
Requires:  %{name} = %{epoch}:%{version}-%{release}

%description extension-fileio
This extension allows SWF files being played within Gnash to have direct access
to the file system. The API is similar to the C library one.

%package extension-lirc
Summary:   LIRC extension for Gnash
Group:     Applications/Multimedia
Requires:  %{name} = %{epoch}:%{version}-%{release}

%description extension-lirc
This extension allows SWF files being played within Gnash to have direct access
to a LIRC based remote control device. The API is similar to the standard
LIRC one.

%package extension-dejagnu
Summary:   DejaGnu extension for Gnash
Group:     Applications/Multimedia
Requires:  %{name} = %{epoch}:%{version}-%{release}

%description extension-dejagnu
This extension allows SWF files to have a simple unit testing API. The API
is similar to the DejaGnu unit testing one.

%package extension-mysql
Summary:   MySQL extension for Gnash
Group:     Applications/Multimedia
Requires:  %{name} = %{epoch}:%{version}-%{release}

%description extension-mysql
This extension allows SWF files being played within Gnash to have direct access
to a MySQL database. The API is similar to the standard MySQL one.

%prep
%setup -q
%patch0 -p1 -b .unistd-header
%patch1 -p1 -b .integer-overflow
%patch2 -p1 -b .boost150
%patch3 -p0 -b .includes
autoreconf -if

%build
%configure --disable-static --with-npapi-plugindir=%{_libdir}/mozilla/plugins \
  --enable-docbook --disable-ghelp --enable-media=GST \
  --disable-dependency-tracking --disable-rpath \
  --disable-testsuite \
  --without-swfdec-testsuite \
  --without-ming \
  --enable-cygnal \
  --enable-python \
  --enable-gui=gtk,kde4,sdl,fb \
  --enable-renderer=all \
  --with-plugins-install=system \
  --enable-doublebuf \
  --disable-jemalloc \
  --enable-extensions=fileio,lirc,dejagnu,mysql \
  --htmldir=%{_datadir}/gnash/html

make %{?_smp_mflags}

%install
make install install-plugins \
 DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -rf '{}' \;
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %{name}


%post 
/sbin/install-info %{_infodir}/gnash_ref.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/gnash_user.info %{_infodir}/dir || :

update-desktop-database &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%post klash
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/gnash_ref.info %{_infodir}/dir || :
    /sbin/install-info --delete %{_infodir}/gnash_user.info %{_infodir}/dir || :
fi

%postun
update-desktop-database &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun klash
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README AUTHORS COPYING NEWS 
%config(noreplace) %{_sysconfdir}/gnashpluginrc
%config(noreplace) %{_sysconfdir}/gnashrc
%{_bindir}/fb-gnash
%{_bindir}/gtk-gnash
%{_bindir}/gnash-gtk-launcher
%{_bindir}/rtmpget
%{_bindir}/sdl-gnash
%{_bindir}/gnash
%{_bindir}/gprocessor
%{_bindir}/findmicrophones
%{_bindir}/findwebcams
%dir %{_libdir}/gnash
%{_libdir}/gnash/*.so*
%{_mandir}/man1/gnash.1*
%{_mandir}/man1/gprocessor.1*
%{_mandir}/man1/findmicrophones.1*
%{_mandir}/man1/findwebcams.1*
%{_mandir}/man1/gtk-gnash.1*
%{_mandir}/man1/gnash-gtk-launcher.1*
%{_mandir}/man1/fb-gnash.1*
%{_mandir}/man1/sdl-gnash.1*
%{_mandir}/man1/rtmpget.1*
%{_infodir}/gnash*
%{_datadir}/gnash/
%{_datadir}/icons/hicolor/32x32/apps/gnash.xpm
%{_datadir}/applications/gnash.desktop

%files plugin
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/mozilla/plugins/libgnashplugin.so

%files klash
%defattr(-,root,root,-)
%doc COPYING
%{_datadir}/applications/klash.desktop
%{_bindir}/gnash-qt-launcher
%{_kde4_bindir}/qt4-gnash
%{_kde4_libdir}/kde4/libklashpart.so
%{_kde4_appsdir}/klash/
%{_kde4_datadir}/kde4/services/klash_part.desktop
%{_datadir}/icons/hicolor/32x32/apps/klash.xpm
%{_mandir}/man1/qt4-gnash.1*
%{_mandir}/man1/gnash-qt-launcher.1*

%files cygnal
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/cygnalrc
%{_bindir}/cygnal
%{_bindir}/flvdumper
%{_bindir}/soldumper
%{_mandir}/man1/cygnal.1*
%{_mandir}/man1/flvdumper.1*
%{_mandir}/man1/soldumper.1*
%dir %{_libdir}/cygnal
%{_libdir}/cygnal/plugins/*.so*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%{_includedir}/gnash/
%{_libdir}/pkgconfig/gnash.pc

%files -n python-gnash
%defattr(-,root,root,-)
%doc COPYING
%{python_sitearch}/gtk-2.0/gnash.so

%files extension-fileio
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/gnash/plugins/fileio.so

%files extension-lirc
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/gnash/plugins/lirc.so

%files extension-dejagnu
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/gnash/plugins/dejagnu.so

%files extension-mysql
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/gnash/plugins/mysql.so

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1:0.8.10-12
- Rebuild for boost 1.55.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 Petr Machata <pmachata@redhat.com> - 1:0.8.10-10
- Rebuild for boost 1.54.0
- Boost doesn't use tagged sonames anymore, drop the -mt suffix
  from gnash-0.8.10-boost-1.50.patch

* Mon Jun 10 2013 Jon Ciesla <limburgher@gmail.com> - 1:0.8.10-9
- agg rebuild.
- Patch for explicit includes.

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:0.8.10-8
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1:0.8.10-7
- Rebuild for Boost-1.53.0

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1:0.8.10-6
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1:0.8.10-5
- rebuild against new libjpeg

* Mon Aug 13 2012 Daniel Drake <dsd@laptop.org> - 1:0.8.10-4
- Rebuilt for Boost-1.50

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 15 2012 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:0.8.10-2
- Fix CVE-2012-1175 ( rhbz #803443 #803444 )

* Mon Feb 27 2012 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:0.8.10-1
- Update to 0.8.10
- Drop patches backported from upstream

* Thu Jan 26 2012 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:0.8.9-9
- Add unistd.h header ( http://www.mail-archive.com/gcc-bugs@gcc.gnu.org/msg338792.html )
- Backport patch from upstream that replaces xulrunner-headers patch 
  ( http://git.savannah.gnu.org/gitweb/?p=gnash.git;a=commit;h=35dde18 )

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Daniel Drake <dsd@laptop.org> - 1:0.8.9-7
- Add patch to fix compile with new xulrunner

* Mon Nov 21 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1:0.8.9-6
- Rebuild for boost 1.48

* Tue Jul 26 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1:0.8.9-5
- Rebuild for boost 1.47

* Mon Apr 18 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:0.8.9-4
- Fix rhbz #691370

* Sat Apr 09 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:0.8.9-3
- Fix rhbz #692779

* Wed Mar 30 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:0.8.9-2
- Fix rhbz #691699

* Fri Mar 18 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:0.8.9-1
- Update to 0.8.9 final

* Sat Mar 12 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:0.8.9-0.1.20110312git
- Switch to 0.8.9 branch
- Spec cleanup
- Add extensions
- Enable testsuite

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.8.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.8-4
- backport 2 upstream commits to make it work with libcurl >= 7.21.x (#639737)

* Sat Oct 02 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.8-3
- fix FTBFS (#631181) (fix by Hicham Haouari)

* Fri Aug 27 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.8-2
- fix the check for the docbook2X tools being in Perl

* Wed Aug 25 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.8-1.1
- rebuild for the official release of Boost 1.44.0 (silent ABI change)

* Mon Aug 23 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.8-1
- update to 0.8.8 (#626352, #574100, #606170)
- update file list (patch by Jeff Smith)

* Thu Jul 29 2010 Bill Nottingham <notting@redhat.com> - 1:0.8.7-5
- Rebuilt for boost-1.44, again

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 1:0.8.7-4
- Rebuilt for boost-1.44

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1:0.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 08 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.7-2
- -plugin: avoid file (directory) dependency (#601942)

* Sat Feb 27 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.7-1
- update to 0.8.7 (#568971)
- make scrollkeeper a conditional (still disabled as it's not working)
- drop gnash-0.8.3-manual.patch, should no longer be needed
- drop gnash-0.8.6-python-install-dir.patch, fixed upstream

* Fri Feb 12 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-13
- delete bundled libltdl stuff to make sure it's not used

* Thu Feb 11 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-12
- don't build libltdlc.a

* Thu Feb 11 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-11
- --without-included-ltdl (CVE-2009-3736)

* Fri Jan 22 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-10
- Rebuild for new Boost (1.41.0)

* Sat Jan 02 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-9
- Add missing Epoch to Requires

* Sat Jan 02 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1:0.8.6-8
- Install icon to the correct place (#551621)

* Wed Dec 30 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-7
- One more try at using the correct dir

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-6
- Patch was reversed

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-5
- Patch Makefile.in, not Makefile.am

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-4
- Pick up python modules from the right dir

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-3
- Install python modules in the right dir

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-2
- Add cygnal plugins

* Tue Dec 29 2009 Tomeu Vizoso <tomeu@sugarlabs.org> - 1:0.8.6-1
- Update to 0.8.6, increase epoch.

* Thu Sep 10 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.8.20090910bzr11506
- update to HEAD

* Thu Sep 10 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.7.20090910bzr11505
- update to HEAD

* Mon Aug 10 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.0-0.6.20090809bzr11401
- don't package headers in -widget, only in -devel (no duplicate files)
- own %%{_includedir}/gnash/ in -devel
- add missing %%defattr for -devel and -widget
- make -devel and -widget require the main package (with exact VR)
- fix -devel group and description
- rename gnash-widget to python-gnash as per the naming guidelines

* Sun Aug 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.9.0-0.5.20090809bzr11401
- use %%{_includedir}, not %%{_prefix}/include

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.4.20090809bzr11401
- Install the python module in the sitearch dir

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.3.20090809bzr11401
- One more 64bit fix

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.3.20090809bzr11400
- Fix the packaging in 64bits

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.2.20090809bzr11400
- upload the .swf file

* Sun Aug 09 2009 Tomeu Vizoso <tomeu@sugarlabs.org> 0.9.0-0.1.20090809bzr11400
- merge upstream changes into the spec

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 22 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.5-4
- rebuild for new Boost

* Fri Mar 06 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.5-3
- explicitly link the KlashPart against the libraries it uses

* Fri Mar 06 2009 Jaroslav Reznik <jreznik@redhat.com> 0.8.5-2
- add missing speex-devel and gstreamer-plugins-base-devel BR
 
* Fri Mar 06 2009 Jaroslav Reznik <jreznik@redhat.com> 0.8.5-1
- update to 0.8.5
- remove use_kde3_executable_hack
- remove autoreconf

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 0.8.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.4-6
- rebuild for new boost

* Thu Nov 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.4-5
- add missing portions of KDE 4 port from upstream kde4 branch

* Thu Nov 13 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.4-4
- add 3 more patches from bero to fix the KDE 4 viewer executable
- disable use_kde3_executable hack

* Sun Oct 19 2008 Patrice Dumas <pertusus@free.fr> 0.8.4-3
- add a desktop file

* Sat Oct 18 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.4-2
- update KDE 4 patch (undo the backporting and use original patch)
- patch to make autoreconf work
- add missing BR giflib-devel, gettext
- omit unrecognized --with-qtdir

* Sat Oct 18 2008 Patrice Dumas <pertusus@free.fr> 0.8.4-1
- update to 0.8.4

* Sat Oct  4 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.3-6
- use the KDE 3 executable with the KDE 4 KPart for now (making this conditional
  so it can easily be disabled or removed once the KDE 4 executable is fixed)

* Sat Oct  4 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.3-5
- register KComponentData properly in KDE 4 KPart

* Fri Oct  3 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.8.3-4
- KDE 4 port of klash by Benjamin Wolsey and Bernhard Rosenkränzer

* Fri Aug 29 2008 Michael Schwendt <mschwendt@fedoraproject.org> 0.8.3-3
- include %%_libdir/gnash directory

* Wed Jun 25 2008 Patrice Dumas <pertusus@free.fr> 0.8.3-2
- add glib in the link, thanks Daniel Drake (#452767)

* Sun Jun 22 2008 Patrice Dumas <pertusus@free.fr> 0.8.3-1
- update to 0.8.3

* Wed Apr  9 2008 Patrice Dumas <pertusus@free.fr> 0.8.2-3
- ship libklashpart (#441601)

* Mon Mar 10 2008 Patrice Dumas <pertusus@free.fr> 0.8.2-2
- don't ship libltdl.so.3 (#436725)

* Fri Mar  7 2008 Patrice Dumas <pertusus@free.fr> 0.8.2-1
- update to 0.8.2

* Sat Oct 27 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-6
- add patch from Martin Stransky to fix wrapped plugin #281061

* Thu Sep 20 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-5
- info files are empty, don't install them

* Thu Sep 20 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-4
- omf/scrollkeeper doc is broken, remove it

* Fri Sep  7 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-3
- better documentation generation

* Wed Sep  5 2007 Patrice Dumas <pertusus@free.fr> 0.8.1-2
- update to 0.8.1
- agg is now the default renderer

* Fri Aug  3 2007 Patrice Dumas <pertusus@free.fr> 0.8.0-2
- rebuild for boost soname change

* Sun Jun 17 2007 Patrice Dumas <pertusus@free.fr> 0.8.0-1
- update to 0.8.0

* Wed May  9 2007 Patrice Dumas <pertusus@free.fr> 0.7.2-2
- fix CVE-2007-2500 (fix 239213)

* Mon Nov  6 2006 Patrice Dumas <pertusus@free.fr> 0.7.2-1
- update for 0.7.2 release.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.7.1-9
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Patrice Dumas <pertusus@free.fr> 0.7.1-8
- plugin requires %%{_libdir}/mozilla/plugins. Fix (incompletly and 
  temporarily, but there is no better solution yet) #207613

* Sun Aug 27 2006 Patrice Dumas <pertusus@free.fr> - 0.7.1-7
- add defattr for klash
- add warnings in the description about stability

* Mon Aug 21 2006 Patrice Dumas <pertusus@free.fr> - 0.7.1-6
- remove superfluous buildrequires autoconf
- rename last patch to gnash-plugin-tempfile-dir.patch
- add README.fedora to plugin to explain tmpdirs

* Wed Aug 16 2006 Jens Petersen <petersen@redhat.com> - 0.7.1-5
- source qt.sh and configure --with-qtdir (Dominik Mierzejewski)
- add plugin-tempfile-dir.patch for plugin to use a safe tempdir

* Fri Jul 28 2006 Jens Petersen <petersen@redhat.com> - 0.7.1-4
- buildrequire autotools (Michael Knox)

* Fri Jun  2 2006 Patrice Dumas <pertusus@free.fr> - 0.7.1-3
- add gnash-continue_on_info_install_error.patch to avoid
- buildrequire libXmu-devel

* Wed May 17 2006 Jens Petersen <petersen@redhat.com> - 0.7.1-2
- configure with --disable-rpath
- buildrequire docbook2X
- remove devel files

* Sun May  7 2006 Jens Petersen <petersen@redhat.com> - 0.7.1-1
- update to 0.7.1 alpha release

* Sat Apr  22 2006 Rob Savoye <rob@welcomehome.org> - 0.7-1
- install the info file. Various tweaks for my system based on
Patrice's latest patch,

* Fri Feb  3 2006 Patrice Dumas <dumas@centre-cired.fr> - 0.7-1
- initial packaging
