%bcond_with	motif
%bcond_with	quicktime

Summary: TV applications for video4linux compliant devices
Name: xawtv
Version: 3.103
Release: 1%{?dist}
Group: Applications/Multimedia
License: GPLv2+
URL: http://git.linuxtv.org/xawtv3.git

Source0: http://linuxtv.org/downloads/xawtv/%{name}-%{version}.tar.bz2
Source1: xawtv.desktop

BuildRequires: mesa-libGL-devel, libXaw-devel, libXext-devel
BuildRequires: libXft-devel, libXinerama-devel
BuildRequires: libXpm-devel, libXrandr-devel, libXt-devel
BuildRequires: libXxf86dga-devel, libXv-devel
#  Note: it compiles with lesstif-devel, but does not work properly.
%{?with_motif:BuildRequires: openmotif-devel}
%{?with_quicktime:BuildRequires: libquicktime-devel}

BuildRequires: ncurses-devel, fileutils, libjpeg-devel, libpng-devel
BuildRequires: alsa-lib-devel
%ifnarch s390 s390x
BuildRequires: libdv-devel
%endif
BuildRequires: zvbi-devel, aalib-devel
BuildRequires: gpm-devel, slang-devel
BuildRequires: desktop-file-utils
BuildRequires: libv4l-devel

Requires: usermode xorg-x11-fonts-misc hicolor-icon-theme

%description
Xawtv is a simple xaw-based TV program which uses the bttv driver or
video4linux. Xawtv contains various command-line utilities for
grabbing images and .avi movies, for tuning in to TV stations, etc.
Xawtv also includes a grabber driver for vic.


%prep
%setup -q


%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-pointer-sign"

%if %{with motif}
export X_LIBS="-L/usr/lib/openmotif"
export X_CFLAGS="-I/usr/include/openmotif"
%endif

%configure \
    %{!?_with_motif: --disable-motif} \
    %{!?_with_quicktime: --disable-quicktime}
make %{?_smp_mflags} verbose=yes


%install
make DESTDIR=$RPM_BUILD_ROOT SUID_ROOT="" install

%if %{without motif}
rm -f $RPM_BUILD_ROOT%{_mandir}/*/motv.*
rm -f $RPM_BUILD_ROOT%{_mandir}/*/mtt.*
%endif
%if %{without quicktime}
rm -f $RPM_BUILD_ROOT%{_bindir}/showqt
%endif

for i in 16x16 32x32 48x48; do
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$i/apps
  install -p -m 0644 contrib/%{name}$i.xpm \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/$i/apps/%{name}.xpm
done

desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
  --vendor fedora \
%endif
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE1}
 

#   v4l-conf  stuff

mkdir -p $RPM_BUILD_ROOT%{_sbindir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/pam.d \
	$RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps \

cat >v4l-conf.pam <<!
#%%PAM-1.0
auth		sufficient	pam_rootok.so
auth		required	pam_console.so
account		required	pam_permit.so
session		required	pam_permit.so
session		optional	pam_xauth.so
!
install -m 0644 v4l-conf.pam $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/v4l-conf

cat >v4l-conf.apps <<!
SESSION=true
USER=root
PROGRAM=%{_sbindir}/v4l-conf
!
install -p -m 0644 v4l-conf.apps $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/v4l-conf

mv $RPM_BUILD_ROOT%{_bindir}/v4l-conf $RPM_BUILD_ROOT%{_sbindir}/
ln -s consolehelper $RPM_BUILD_ROOT%{_bindir}/v4l-conf


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%config(noreplace) %{_sysconfdir}/pam.d/v4l-conf
%config(noreplace) %{_sysconfdir}/security/console.apps/v4l-conf
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/xawtv
%{_datadir}/xawtv
%{_datadir}/X11/app-defaults/*
%{_datadir}/icons/hicolor/*/apps/%{name}.xpm
%{_datadir}/applications/*
%{_mandir}/man?/*
%lang(es) %{_mandir}/es/*/*
%lang(fr) %{_mandir}/fr/*/*
%doc COPYING README TODO contrib/frequencies*
%if %{with motif}
%lang(de) %{_datadir}/X11/de_DE.UTF-8/app-defaults/*
%lang(fr) %{_datadir}/X11/fr_FR.UTF-8/app-defaults/*
%lang(fr) %{_datadir}/X11/it_IT.UTF-8/app-defaults/*
%endif


%changelog
* Tue Apr  2 2013 Hans de Goede <hdegoede@redhat.com> 3.103-1
- New upstream version 3.103

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 3.101-7
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077
- Cleanup spec as per recently changed packaging guidelines

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 3.101-6
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 3.101-5
- rebuild against new libjpeg

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.101-2
- Rebuild for new libpng

* Sun Jul  3 2011 Mauro Carvalho Chehab <mchehab@redhat.com> - 3.101-1
- update to Xawtv version 3.101: Adds support for alsa streams

* Wed Mar  2 2011 Mauro Carvalho Chehab <mchehab@redhat.com> - 3.100-1
- update to Xawtv version 3.100. Fixes control handling on xawtv.

* Thu Feb 17 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.99.rc6-1
- update to Xawtv version 3.99.rc6

* Thu Feb  3 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.99.rc4-1
- update to Xawtv version 3.99.rc4

* Wed Feb  2 2011 Mauro Carvalho Chehab <mchehab@redhat.com> 3.99.rc3-1
- Update to Xawtv version 3.99.rc3
- Upstream applied some patches from Debian and from Fedora, making
  compilation more portable along different distros. It also incudes
  a couple minor fixes.

* Tue Feb  1 2011 Mauro Carvalho Chehab <mchehab@redhat.com> 3.99.rc2-1
- Update to Xawtv version 3.99.rc2
- All other patches from Fedora are now upstream

* Thu Jan 28 2011 Mauro Carvalho Chehab <mchehab@redhat.com> 3.99.rc1-1
- Update to Xawtv version 3.99.rc1
- Applied some fixes upstream fixing radio application and also some
  improvements from other patches that were found on Fedora.

* Thu Jan 27 2011 Mauro Carvalho Chehab <mchehab@redhat.com> 3.98-1
- Update to Xawtv version 3.98
- Removes V4L1 support and adds some new stuff

* Wed Nov 17 2010 Hans de Goede <hdegoede@redhat.com> 3.95-14
- Protect the exit code from being called twice. This fixes a double
  free error when the user tries to exit twice when xawtv is stuck (#608344)

* Fri Mar 12 2010 Hans de Goede <hdegoede@redhat.com> 3.95-13
- Fix xawtv not starting due to it not finding its fonts

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.95-12.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 07 2009 Karsten Hopp <karsten@redhat.com> 3.95-11.1
- we have no libdv on mainframe, don't require that on s390(x)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.95-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.95-10
- fix some typos in manuals  (patch7, derived from Debian)
- fix recording from oss  (patch8, derived from Debian)
- allow scantv to use another card's input  (patch9, derived from Debian)
- some v4l2 code fixes (patch10, Hans de Goede <j.w.r.degoede@hhs.nl>)
- skip dga automatically when not available (patch11, Hans de Goede)
- specifying of bpl pitch for v4l-conf (patch12, Hans de Goede)
- drop drv0-v4l2-old.so driver (assume not needed anyway now)
- optional (default yes) build with libv4l wrapper library
  (patch100, Hans de Goede <j.w.r.degoede@hhs.nl>)

* Mon Jul 21 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.95-9
- rebuild for new gpm
- update strip patch

* Tue Feb 19 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.95-8
- add gpm-devel and slang-devel to BuildRequires
- rebuild for GCC 4.3

* Thu Aug 30 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.95-7
- add patch for "open(2) call now is a macro" issue (#265081).

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.95-6
- Rebuild for selinux ppc32 issue.

* Fri Aug 17 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- Change License tag to GPLv2+

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 3.95-5
- rebuild for toolchain bug

* Tue Jul 24 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.95-4
- don't assume v4l-conf as system config util (#249130)

* Tue Jun 26 2007 Dmitry Butskoy <Dmitry@Butskoy.name>
- drop X-Fedora category from desktop file

* Mon Jun 25 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.95-3
- add patch for use getpagesize() instead of a kernel headers macro

* Thu Jun 21 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.95-1
- spec file cleanup
- accepted for Fedora (review by Jason Tibbitts <tibbs@math.uh.edu>)

* Thu Mar  1 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 3.95-0
- upgrade to 3.95
- adapt for Fedora Extras, spec file cleanups
- add UTF-8 support for console apps
- drop tv-fonts package (you can use zvbi-fonts package for that purpose),
  bitstream-vera is now a default for "big" fullscreen-mode fonts.
- add desktop entry and icons
- add ALEVTD_REGION environment to change default teletext's region


* Tue Oct 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add BuildReq for fontconfig-devel and freetype-devel, these seem
  to get picked up

* Mon Sep 01 2003 Than Ngo <than@redhat.com> 3.88-5
- Added missing BuildRequires for libpng-devel (bug #103447)

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 3.88-4
- fixed permission problem (bug #90921)

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 3.88-3
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  6 2003 Than Ngo <than@redhat.com> 3.88-1
- 3.88

* Thu Mar  3 2003 Than Ngo <than@redhat.com> 3.85-1
- 3.85, (#85557, #81588, #74684, #61717)
- own /usr/lib/xawtv, (bug #73981)
- dependency on libjpeg-devel, (bug #48925)
- include alevtd daemon (bug #53878)
- create default configuration by install (bug #73270) 

* Sun Feb 10 2003 Than Ngo <than@redhat.com> 3.81-6
- install correct pam file, #83820

* Mon Jan 27 2003 Than Ngo <than@redhat.com> 3.81-5
- fix #81791

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan 21 2003 Than Ngo <than@redhat.com> 3.81-3
- fix #81851

* Mon Dec 16 2002 Than Ngo <than@redhat.com> 3.81-2
- rebuild

* Fri Dec 13 2002 Than Ngo <than@redhat.com> 3.81-1
- update 3.81
- move bitmap fonts to bitmap-fonts package

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com> 3.78-2
- adjust PAM configuration to not use absolute paths so that the right module
  set gets used for the current arch on multilib systems

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 3.78-1
- 3.78

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Than Ngo <than@redhat.com> 3.74-3
- Don't forcibly strip binaries

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Harald Hoyer <harald@redhat.de>
- 3.74

* Sun Apr 07 2002 han Ngo <than@redhat.com> 3.73-3
- remove motv manpage (#62771)

* Tue Apr  2 2002 Than Ngo <than@redhat.com> 3.73-2
- get rid of openmotif

* Sun Mar 24 2002 Than Ngo <than@redhat.com> 3.73-1
- update
- fix bug #61719

* Fri Mar 22 2002 Tim Powers <timp@redhat.com>
- rebuilt motv against new openmotif-2.2.2

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 3.72-1
- update to 3.72

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.71-1
- 3.71

* Fri Jan 18 2002 Than Ngo <than@redhat.com> 3.68-1
- update to 3.68
- enable XFree extensions
- fix Url
- add missing plugins

* Wed Dec  5 2001 Than Ngo <than@redhat.com> 3.65-1
- update to 3.65
- fix build on ia64

* Wed Nov 14 2001 Than Ngo <than@redhat.com> 3.64-1
- update to 3.64

* Mon Sep 17 2001 Than Ngo <than@redhat.com> 3.62-1
- update to 3.62 (bug #53711 #52847)

* Tue Aug 28 2001 Than Ngo <than@redhat.com> 3.54-5
- fix spec file bug (Bug #52675)

* Fri Aug 10 2001 Than Ngo <than@redhat.com> 3.54-4
- add requires usermode (bug #51474)

* Sun Aug  5 2001 Nalin Dahyabhai <nalin@redhat.com> 3.54-3
- tweak PAM setup so that v4l-conf can access the display properly

* Tue Jul 10 2001 Elliot Lee <sopwith@redhat.com> 3.54-2
- Rebuild to remove libXv/libXxf86dga deps

* Mon Jul 02 2001 Than Ngo <than@redhat.com>
- update to 3.54

* Fri Jun 22 2001 Than Ngo <than@redhat.com>
- update to 3.53
- add buildprereq
- remove some uneeeded patches

* Tue Jun 19 2001 Karsten Hopp <karsten@redhat.de>
- excludearch s390 s390x

* Wed Jun 13 2001 Than Ngo <than@redhat.com>
- update to 3.51

* Thu Jun 07 2001 Than Ngo <than@redhat.com>
- update to 3.50

* Thu May 31 2001 Than Ngo <than@redhat.com>
- udate to 3.49

* Tue May 22 2001 Than Ngo <than@redhat.com>
- update to 3.48

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- built for the distro

* Wed May 18 2001 Karsten Hopp <karsten@redhat.de>
- make xawtv work with kernel-2.4

* Wed May 16 2001 Than Ngo <than@redhat.com>
- update to 3.47

* Mon May 07 2001 Than Ngo <than@redhat.com>
- update to 3.45
- add missing fonts

* Tue Feb 13 2001 Than Ngo <than@redhat.com>
- update to 3.34
- use consolehelper for v4l-conf
- add excludearch sparc, bdftopcf is broken on sparc

* Wed Jan 24 2001 Than Ngo <than@redhat.com>
- updated to 3.30
- use /dev/video0 instead /dev/video (bug #24871)
- fixed dependencies (Bug #24881)
 
* Sun Nov 19 2000 Than Ngo <than@redhat.com>
- update to 3.24
- add missing tools (rootv,scantv)
- add missing prereq on xset and mkfontdir

* Fri Nov 3 2000 Than Ngo <than@redhat.com>
- update to 3.23

* Wed Aug 23 2000 Tim Powers <timp@redhat.com>
- rebuilt against new XFree86 to fix DGA problems

* Mon Aug 21 2000 Than Ngo <than@redhat.com>
- update to 3.18 (Bugfix release)
- option -nodga to disable DGA (Bug #16577, #15702)
- compress fonts with gzip

* Mon Aug 07 2000 Tim Powers <timp@redhat.com>
- fixed bug #15435

* Mon Aug 07 2000 Than Ngo <than@redhat.de>
- rebuilt against the new DGA
- fixed in post and postun, so that it does not
  emits to console (Bug #15436)


* Sat Jul 29 2000 Than Ngo <than@redhat.de>
- update to 3.17

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- FHS fixes

* Mon Jul 03 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun May 28 2000 Ngo Than <than@redhat.de>
- update to 3.14 for 7.0
- put man page in correct place
- add webcam
- bzip2 source
- cleanup specfile

* Wed Jan 19 2000 Preston Brown <pbrown@redhat.com>
- font fix (#8610) in post and postun
- add missing files in bin

* Sun Jan 16 2000 Preston Brown <pbrown@redhat.com>
- whoops! 3.07 already bugfix release

* Fri Jan 14 2000 Ngo Than <than@redhat.de>
- updated to 3.06

* Mon Jul 26 1999 Tim Powers <timp@redhat.com>
- updated to 2.46
- built for 6.1

* Wed Apr 28 1999 Preston Brown <pbrown@redhat.com>
- initial build for Powertools 6.0
