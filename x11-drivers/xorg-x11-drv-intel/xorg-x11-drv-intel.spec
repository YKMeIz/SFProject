%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers
%define gputoolsver 1.9
%define gitdate 20160119
%define gitrev .%{gitdate}

%undefine _hardened_build

%if 0%{?rhel} == 7
%define rhel7 1
%endif
%if 0%{?rhel} == 6
%define rhel6 1
%endif

%if 0%{?rhel7} || 0%{?fedora} > 17
%define prime 1
%endif

%if 0%{?rhel7} || 0%{?fedora} > 20
%define kmsonly 1
%else
%ifnarch %{ix86}
%define kmsonly 1
%endif
%endif

Summary:   Xorg X11 Intel video driver
Name:      xorg-x11-drv-intel
Version:   2.99.917
Release:   22%{?gitrev}%{?dist}
URL:       http://www.x.org
License:   MIT
Group:     User Interface/X Hardware Support

%if 0%{?gitdate}
Source0:    xf86-video-intel-%{gitdate}.tar.bz2
%else
Source0:    http://xorg.freedesktop.org/archive/individual/driver/xf86-video-intel-%{version}.tar.bz2 
%endif
Source1:    make-intel-gpu-tools-snapshot.sh
Source3:    http://xorg.freedesktop.org/archive/individual/app/intel-gpu-tools-%{gputoolsver}.tar.bz2
Source4:    make-git-snapshot.sh

Patch0:	    intel-gcc-pr65873.patch
Patch1:	    igt-stat.patch
Patch2:     0001-sna-Let-modestting-glamor-handle-gen9.patch

ExclusiveArch: %{ix86} x86_64 ia64

BuildRequires: autoconf automake libtool
BuildRequires: flex bison
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: libX11-devel
BuildRequires: libXcursor-devel
BuildRequires: libXdamage-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXtst-devel
BuildRequires: libXvMC-devel
BuildRequires: libXfont-devel
BuildRequires: mesa-libGL-devel >= 6.5-9
BuildRequires: libdrm-devel >= 2.4.25
BuildRequires: kernel-headers >= 2.6.32.3
BuildRequires: libudev-devel
BuildRequires: libxcb-devel >= 1.5 
BuildRequires: xcb-util-devel
BuildRequires: cairo-devel
BuildRequires: python
BuildRequires: libXScrnSaver-devel
BuildRequires: libXext-devel
BuildRequires: pixman-devel

Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
Requires: polkit

%description 
X.Org X11 Intel video driver.

%package devel
Summary:   Xorg X11 Intel video driver development package
Group:     Development/System
Requires:  %{name} = %{version}-%{release}
Provides:  xorg-x11-drv-intel-devel = %{version}-%{release}

%description devel
X.Org X11 Intel video driver development package.

%package -n intel-gpu-tools
Summary:    Debugging tools for Intel graphics chips
Group:	    Development/Tools

%description -n intel-gpu-tools
Debugging tools for Intel graphics chips

%if 0%{?gitdate}
%define dirsuffix %{gitdate}
%else
%define dirsuffix %{version}
%endif

%prep
%setup -q -n xf86-video-intel-%{?gitdate:%{gitdate}}%{!?gitdate:%{dirsuffix}} -b3
%patch0 -p1 -b .gcc
%patch2 -p1

pushd ../intel-gpu-tools-%{gputoolsver}
%patch1 -p1 -b .stat
popd

%build
autoreconf -f -i -v
%configure %{?kmsonly:--enable-kms-only} --with-default-dri=3 --enable-tools
make %{?_smp_mflags} V=1

pushd ../intel-gpu-tools-%{gputoolsver}
# this is missing from the tarbal, having it empty is ok
touch lib/check-ndebug.h
mkdir -p m4
autoreconf -f -i -v
# --disable-dumper: quick_dump is both not recommended for packaging yet,
# and requires python3 to build; i'd like to keep this spec valid for rhel6
# for at least a bit longer
%configure %{!?prime:--disable-nouveau} --disable-dumper
# some of the sources are in utf-8 and pre-preprocessed by python
export LANG=en_US.UTF-8
make %{?_smp_mflags}
popd

%install
%make_install

pushd ../intel-gpu-tools-%{gputoolsver}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_bindir}/eudb
popd

find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

# libXvMC opens the versioned file name, these are useless
rm -f $RPM_BUILD_ROOT%{_libdir}/libI*XvMC.so


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{driverdir}/intel_drv.so
%if !%{?kmsonly}
%{_libdir}/libI810XvMC.so.1*
%endif
%{_libdir}/libIntelXvMC.so.1*
%{_libexecdir}/xf86-video-intel-backlight-helper
%{_datadir}/polkit-1/actions/org.x.xf86-video-intel.backlight-helper.policy
%{_mandir}/man4/i*

%files devel
%{_bindir}/intel-gen4asm
%{_bindir}/intel-gen4disasm
%{_libdir}/pkgconfig/intel-gen4asm.pc

%files -n intel-gpu-tools
%doc COPYING
%{_bindir}/gem_userptr_benchmark
%{_bindir}/intel*
%{_datadir}/gtk-doc
%{_mandir}/man1/intel_*.1*

%changelog
* Mon Mar 07 2016 Hans de Goede <hdegoede@redhat.com> - 2.99.917-22.20160119
- xorg-x11-drv-intel hardly has any accel on skylake and newer, so make
  Xorg fallback to modesetting + glamor by returning FALSE from probe
- Using glamor also gives us proper Xvideo support on skylake (rhbz#1305369)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.99.917-21.20160119
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Kevin Fenzi <kevin@scrye.com> - 2.99.917-20-20160119
- Update to 20160119 snapshot

* Sun Dec 06 2015 Adel Gadllah <adel.gadllah@gmail.com> - 2.99.917-19.20151109
- Update to 20151206 snapshot

* Tue Nov 17 2015 Adel Gadllah <adel.gadllah@gmail.com> - 2.99.917-18.20151109
- Reenable DRI3 - we ship xserver 1.18 now

* Mon Nov 09 2015 Kevin Fenzi <kevin@scrye.com> - 2.99.917-17.20151109
- Update to 20151109 snapshot

* Wed Sep 16 2015 Dave Airlie <airlied@redhat.com> - 2.99.917-16.20150729
- 1.18 ABI rebuild

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> 2.99.917-15.20150729
- update to upstream git snapshot for ABI

* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 2.99.917-14.20150615
- 1.15 ABI rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.917-13.20150615
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Dave Airlie <airlied@redhat.com> 2.99.917-12
- you guessed it, git snap of the day
- this should bring some PRIME corruption fixes.

* Wed Jun 03 2015 Adam Jackson <ajax@redhat.com> 2.99.917-11
- Today's git snap

* Tue May 26 2015 Dave Airlie <airlied@redhat.com> 2.99.917-10
- update git snap
- fixes uninitialised properties crash

* Wed May 20 2015 Adam Jackson <ajax@redhat.com> 2.99.917-9
- Today's git snap
- Don't force the default to DRI3, use upstream's preference
- Fix build failure due to GCC PR65873

* Mon Mar 02 2015 Dave Airlie <airlied@redhat.com> 2.99.917-8
- this time for sure, now less hardended.

* Mon Mar 02 2015 Dave Airlie <airlied@redhat.com> 2.99.917-7
- remove cement, X.org drivers aren't hard enough.

* Thu Feb 26 2015 Hans de Goede <hdegoede@redhat.com> - 2.99.917-6
- Really really build intel-virtual-output (rhbz#1195962)

* Thu Feb 26 2015 Hans de Goede <hdegoede@redhat.com> - 2.99.917-5
- Add more missing BuildRequires so that intel-virtual-output really gets
  build (rhbz#1195962)

* Thu Feb 26 2015 Hans de Goede <hdegoede@redhat.com> - 2.99.917-4
- Add missing BuildRequires libXext-devel so that intel-virtual-output gets
  build (rhbz#1195962)

* Wed Feb 11 2015 Hans de Goede <hdegoede@redhat.com> - 2.99.917-3
- Git snapshot of the day to bring in various DPMS and other fixes
- Update gpu-tools to 1.9
- Xserver 1.17 ABI rebuild

* Wed Dec 24 2014 Adel Gadllah <adel.gadllah@gmail.com> 2.99.917-2
- Enable DRI3

* Mon Dec 22 2014 Kevin Fenzi <kevin@scrye.com> 2.99.917-1
- Update to 2.99.917

* Mon Nov 17 2014 Adam Jackson <ajax@redhat.com> 2.99.916-3
- Today's git snapshot

* Thu Sep 11 2014 Dave Airlie <airlied@redhat.com> 2.99.916-2
- backport some SNA and MST fixes.

* Wed Sep 10 2014 Dave Airlie <airlied@redhat.com> 2.99.916-1
- Rebase to 2.99.916

* Wed Sep 03 2014 Dave Airlie <airlied@redhat.com> 2.99.914-4
- Add UXA MST support as a fallback

* Tue Sep 02 2014 Adel Gadllah <adel.gadllah@gmail.com> - 2.99.914-3
- Backport fix for sna to fix broken shadow rendering in gtk

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.914-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 28 2014 Hans de Goede <hdegoede@redhat.com> - 2.99.914-1
- Rebase to 2.99.914

* Tue Jul 22 2014 Adel Gadllah <adel.gadllah@gmail.com> - 2.99.912-6
- Apply fix for sna render corruption due to missing fencing, FDO #81551

* Fri Jul 11 2014 Hans de Goede <hdegoede@redhat.com> - 2.99.912-5
- Fix a security issue in the backlight helper (CVE-2014-4910)

* Tue Jul  1 2014 Hans de Goede <hdegoede@redhat.com> - 2.99.912-4
- Re-enable DRI3 support (the latest mesa fixes the gnome-shell hang)

* Wed Jun 18 2014 Hans de Goede <hdegoede@redhat.com> - 2.99.912-3
- xserver 1.15.99.903 ABI rebuild

* Thu Jun 12 2014 Hans de Goede <hdegoede@redhat.com> - 2.99.912-2
- DRI3 support causes gnome-shell to hang, disable for now

* Wed Jun 11 2014 Hans de Goede <hdegoede@redhat.com> - 2.99.912-1
- Rebase to 2.99.912
- Rebuild for xserver 1.15.99.903
- Update intel-gpu-tools to 1.7 release

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.911-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 2.99.911-2
- xserver 1.15.99-20140428 git snapshot ABI rebuild
- Add 2 patches from upstream to not close server-fds of udl devices

* Thu Apr 17 2014 Hans de Goede <hdegoede@redhat.com> - 2.99.911-1
- Rebase to 2.99.911
- Rebuild for xserver 1.15.99.902

* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 2.21.15-13
- 1.15 ABI rebuild

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.21.15-12
- Call ldconfig in %%post* scriptlets.

* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 2.21.15-11
- 1.15RC4 ABI rebuild

* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 2.21.15-10
- 1.15RC2 ABI rebuild

* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 2.21.15-9
- 1.15RC1 ABI rebuild

* Mon Oct 28 2013 Adam Jackson <ajax@redhat.com> - 2.21.15-8
- Don't patch in xwayland in RHEL

* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 2.21.15-7
- ABI rebuild

* Thu Oct 24 2013 Adam Jackson <ajax@redhat.com> 2.21.15-6
- Disable UMS support in F21+

* Thu Oct 24 2013 Adam Jackson <ajax@redhat.com> 2.21.15-5
- xserver 1.15 API compat

* Wed Oct 02 2013 Adam Jackson <ajax@redhat.com> 2.21.15-4
- Default to uxa again

* Mon Sep 23 2013 Adam Jackson <ajax@redhat.com> 2.21.15-2
- Change xwayland requires to be explicitly versioned

* Mon Sep 23 2013 Adam Jackson <ajax@redhat.com> 2.21.15-1
- intel 2.21.15
- xwayland support

* Tue Aug 06 2013 Dave Airlie <airlied@redhat.com> 2.21.14-1
- intel 2.21.24
- add fix to make build - re-enable autoreconf

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Adam Jackson <ajax@redhat.com> 2.21.12-1
- intel 2.21.12

* Tue Jun 11 2013 Adam Jackson <ajax@redhat.com> 2.21.9-1
- intel 2.21.9
- New i-g-t snapshot
- Drop useless symlinks from -devel
- Repurpose -devel for intel-gen4{,dis}asm
- Default to SNA in F20+

* Tue May 28 2013 Adam Jackson <ajax@redhat.com> 2.21.8-1
- intel 2.21.8

* Fri Apr 12 2013 Dave Airlie <airlied@redhat.com> 2.21.6-1
- intel 2.21.6

* Thu Mar 21 2013 Adam Jackson <ajax@redhat.com> 2.21.5-1
- intel 2.21.5

* Mon Mar 11 2013 Adam Jackson <ajax@redhat.com> 2.21.4-1
- intel 2.21.4

* Thu Mar 07 2013 Adam Jackson <ajax@redhat.com> 2.21.3-1
- intel 2.21.3

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.21.2-4
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.21.2-3
- ABI rebuild

* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 2.21.2-2
- ABI rebuild

* Tue Feb 12 2013 Adam Jackson <ajax@redhat.com> 2.21.2-1
- intel 2.21.2
- New i-g-t snapshot
- Pre-F16 changelog trim

* Wed Jan 16 2013 Adam Jackson <ajax@redhat.com> 2.20.18-2
- Compensate for rawhide's aclocal breaking in a newly stupid way

* Wed Jan 16 2013 Adam Jackson <ajax@redhat.com> 2.20.18-1
- intel 2.20.18

* Tue Jan 08 2013 Dave Airlie <airlied@redhat.com> 2.20.17-2
- Fix damage issue for reverse prime work

* Fri Jan 04 2013 Adam Jackson <ajax@redhat.com> 2.20.17-1
- intel 2.20.17

* Wed Jan 02 2013 Dave Airlie <airlied@redhat.com> 2.20.16-2
- Fix uxa bug that trips up ilk on 3.7 kernels

* Mon Dec 17 2012 Adam Jackson <ajax@redhat.com> 2.20.16-1
- intel 2.20.16

* Wed Nov 28 2012 Adam Jackson <ajax@redhat.com> 2.20.14-1
- intel 2.20.14

* Mon Oct 22 2012 Adam Jackson <ajax@redhat.com> 2.20.12-1
- intel 2.20.12

* Fri Oct 19 2012 Adam Jackson <ajax@redhat.com> 2.20.10-2
- Today's i-g-t
- Don't bother building the nouveau bits of i-g-t on OSes without an X
  server with prime support.

* Mon Oct 15 2012 Dave Airlie <airlied@redhat.com> 2.20.10-1
- intel 2.20.10

* Fri Oct 05 2012 Adam Jackson <ajax@redhat.com> 2.20.9-1
- intel 2.20.9
- Today's intel-gpu-tools snapshot

* Fri Sep 21 2012 Adam Jackson <ajax@redhat.com> 2.20.8-1
- intel 2.20.8

* Mon Sep 10 2012 Adam Jackson <ajax@redhat.com> 2.20.7-1
- intel 2.20.7

* Fri Sep 07 2012 Dave Airlie <airlied@redhat.com> 2.20.6-2
- latest upstream git snapshot with prime + fixes

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 2.20.6-2
- Only bother to build UMS (read: i810) support on 32-bit.  If you've
  managed to build a machine with an i810 GPU but a 64-bit CPU, please
  don't have done that.

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 2.20.6-1
- intel 2.20.6 (#853783)

* Thu Aug 30 2012 Adam Jackson <ajax@redhat.com> 2.20.5-2
- Don't package I810XvMC when not building legacy i810

* Mon Aug 27 2012 Adam Jackson <ajax@redhat.com> 2.20.5-1
- intel 2.20.5

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 2.20.4-3
- Rebuild for new xcb-util soname

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 2.20.4-2
- Backport some patches to avoid binding to non-i915.ko-driven Intel GPUs,
  like Cedarview and friends (#849475)

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 2.20.4-1
- intel 2.20.4

* Thu Aug 16 2012 Dave Airlie <airlied@redhat.com> 2.20.3-3
- fix vmap flush to correct upstream version in prime patch

* Thu Aug 16 2012 Dave Airlie <airlied@redhat.com> 2.20.3-2
- snapshot upstream + add prime support for now

* Wed Aug 15 2012 Adam Jackson <ajax@redhat.com> 2.20.3-1
- intel 2.20.3

* Wed Aug 01 2012 Adam Jackson <ajax@redhat.com> 2.20.2-1
- intel 2.20.2
- Only disable UMS in RHEL7, since i810 exists in RHEL6

* Mon Jul 23 2012 Adam Jackson <ajax@redhat.com> 2.20.1-1
- intel 2.20.1

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.20.0-2.20120718
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 2.20.0-1.20120718
- todays git snapshot

* Tue Jun 12 2012 Dave Airlie <airlied@redhat.com> 2.19.0-5.20120612
- today's git snapshot
- resurrect copy-fb

* Tue May 29 2012 Adam Jackson <ajax@redhat.com> 2.19.0-4.20120529
- Today's git snapshot
- Enable SNA (default is still UXA, use Option "AccelMethod" to switch)
- build-fix.patch: Fix build with Fedora's default cflags

* Tue May 29 2012 Adam Jackson <ajax@redhat.com> 2.19.0-3
- Don't autoreconf the driver, fixes build on F16.

* Mon May 21 2012 Adam Jackson <ajax@redhat.com> 2.19.0-2
- Disable UMS support in RHEL.
- Trim some Requires that haven't been needed since F15.

* Thu May 03 2012 Adam Jackson <ajax@redhat.com> 2.19.0-1
- intel 2.19.0
