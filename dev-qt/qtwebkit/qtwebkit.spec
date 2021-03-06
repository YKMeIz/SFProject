
Name: qtwebkit
Summary: Qt WebKit bindings

Version: 2.3.3
Release: 3%{?dist}

License: LGPLv2 with exceptions or GPLv3 with exceptions
URL: http://trac.webkit.org/wiki/QtWebKit
## This was how qtwebkit-2.2 did it (no longer works for 2.3)
# get make-package.py:
# $ git clone git://qt.gitorious.org/qtwebkit/tools.git
# get Qt WebKit source code:
# $ git clone git://gitorious.org/+qtwebkit-developers/webkit/qtwebkit.git
# create a branch from a tag (e.g. qtwebkit-2.2.2):
# $ git checkout -b qtwebkit-2.2.2 qtwebkit-2.2.2
# generate the tarball (requires: bison flex gperf):
# $ make-package.py
# fix/repack the generated tarball:
# $ tar xzf qtwebkit-2.2.2-source.tar.gz
# $ mv qtwebkit-2.2.2-source/include qtwebkit-2.2.2-source/Source/
# $ tar cJf qtwebkit-2.2.2-source.tar.xz qtwebkit-2.2.2-source/
##
# download from
# https://gitorious.org/webkit/qtwebkit-23/archive-tarball/qtwebkit-%{version}
# repack as .xz
Source0:  qtwebkit-%{version}.tar.xz

# search /usr/lib{,64}/mozilla/plugins-wrapped for browser plugins too
Patch1: webkit-qtwebkit-2.2-tp1-pluginpath.patch

# smaller debuginfo s/-g/-g1/ (debian uses -gstabs) to avoid 4gb size limit
Patch3: qtwebkit-2.3-debuginfo.patch

# tweak linker flags to minimize memory usage on "small" platforms
Patch4: qtwebkit-2.3-save_memory.patch

# use SYSTEM_MALLOC on ppc/ppc64, plus some additional minor tweaks (needed only on ppc? -- rex)
Patch10: qtwebkit-ppc.patch

# add missing function Double2Ints(), backport
# rebased for 2.3.1, not sure if this is still needed?  -- rex
Patch11: qtwebkit-23-LLInt-C-Loop-backend-ppc.patch

## upstream patches
Patch102: 0002-Texmap-GTK-The-poster-circle-doesn-t-appear.patch
Patch103: 0003-Qt-Tiled-backing-store-not-clipped-to-frame-or-visib.patch
Patch104: 0004-Qt-Images-scaled-poorly-on-composited-canvas.patch
Patch105: 0005-Port-of-r118587-to-TextBreakIteratorQt.cpp.patch
patch106: 0006-JSC-ARM-traditional-failing-on-Octane-NavierStokes-t.patch
Patch107: 0007-Correct-range-used-for-Emoji-checks.patch
Patch108: 0008-Qt-RepaintRequested-signal-sometimes-not-emitted.patch
Patch109: 0009-TexMap-Remove-ParentChange-in-TextureMapperLayer.patch

BuildRequires: bison
BuildRequires: chrpath
BuildRequires: flex
BuildRequires: gperf
BuildRequires: libicu-devel
BuildRequires: libjpeg-devel
BuildRequires: pkgconfig(gio-2.0) pkgconfig(glib-2.0)
BuildRequires: pkgconfig(fontconfig)
# gstreamer media support
BuildRequires: pkgconfig(gstreamer-0.10) pkgconfig(gstreamer-app-0.10)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libwebp)
BuildRequires: pkgconfig(libxslt)
BuildRequires: pkgconfig(QtCore) pkgconfig(QtNetwork)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xrender)
BuildRequires: perl(version)
BuildRequires: perl(Digest::MD5)
BuildRequires: ruby
%if 0%{?fedora}
# for QtLocation, QtSensors 
BuildRequires: qt-mobility-devel >= 1.2
%endif
Obsoletes: qt-webkit < 1:4.9.0
Provides: qt-webkit = 2:%{version}-%{release}
Provides: qt4-webkit = 2:%{version}-%{release}
Provides: qt4-webkit%{?_isa} = 2:%{version}-%{release}

%{?_qt4_version:Requires: qt4%{?_isa} >= %{_qt4_version}}

%description
%{summary}

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: qt-webkit-devel < 1:4.9.0
Provides:  qt-webkit-devel = 2:%{version}-%{release}
Provides:  qt4-webkit-devel = 2:%{version}-%{release}
Provides:  qt4-webkit-devel%{?_isa} = 2:%{version}-%{release}
%description devel
%{summary}.


%prep
%setup -q -n webkit-qtwebkit-23

%patch1 -p1 -b .pluginpath
%patch3 -p1 -b .debuginfo
%patch4 -p1 -b .save_memory
# all big-endian arches require the Double2Ints fix
%ifarch ppc ppc64 s390 s390x
%patch10 -p1 -b .system-malloc
%patch11 -p1 -b .Double2Ints
%endif
%patch102 -p1 -b .0002
%patch103 -p1 -b .0003
%patch104 -p1 -b .0004
%patch105 -p1 -b .0005
%patch106 -p1 -b .0006
%patch107 -p1 -b .0007
%patch108 -p1 -b .0008
%patch109 -p1 -b .0009



%build 

PATH=%{_qt4_bindir}:$PATH; export PATH
QMAKEPATH=`pwd`/Tools/qmake; export QMAKEPATH
QTDIR=%{_qt4_prefix}; export QTDIR

mkdir -p %{_target_platform}
pushd    %{_target_platform}
WEBKITOUTPUTDIR=`pwd`; export WEBKITOUTPUTDIR
../Tools/Scripts/build-webkit \
  --qt \
  --no-webkit2 \
  --release \
  --qmakearg="CONFIG+=production_build DEFINES+=HAVE_LIBWEBP=1" \
  --makeargs=%{?_smp_mflags} \
  --system-malloc
popd

%ifarch %{ix86}
# build safe(r) non-sse2-enabled version
mkdir -p %{_target_platform}-no_sse2
pushd    %{_target_platform}-no_sse2
WEBKITOUTPUTDIR=`pwd`; export WEBKITOUTPUTDIR
../Tools/Scripts/build-webkit \
  --qt \
  --no-webkit2 \
  --release \
  --qmakearg="CONFIG+=production_build DEFINES+=HAVE_LIBWEBP=1" \
  --makeargs=%{?_smp_mflags} \
  --system-malloc \
  --no-force-sse2
popd
%endif

  
%install
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}/Release

%ifarch %{ix86}
mkdir -p %{buildroot}%{_qt4_libdir}/sse2/
mv %{buildroot}%{_qt4_libdir}/libQtWebKit.so.4* %{buildroot}%{_qt4_libdir}/sse2/
make install INSTALL_ROOT=%{buildroot} -C %{_target_platform}-no_sse2/Release
%endif

## HACK alert
chrpath --list   %{buildroot}%{_qt4_libdir}/libQtWebKit.so.4.10.? ||:
chrpath --delete %{buildroot}%{_qt4_libdir}/libQtWebKit.so.4.10.? ||:

## pkgconfig love
# drop Libs.private, it contains buildroot references, and
# we don't support static linking libQtWebKit anyway
pushd %{buildroot}%{_libdir}/pkgconfig
grep -v "^Libs.private:" QtWebKit.pc > QtWebKit.pc.new && \
mv QtWebKit.pc.new QtWebKit.pc
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_qt4_libdir}/libQtWebKit.so.4*
%ifarch %{ix86}
%{_qt4_libdir}/sse2/libQtWebKit.so.4*
%endif
%if 0%{?_qt4_importdir:1}
%{_qt4_importdir}/QtWebKit/
%endif

%files devel
%{_qt4_datadir}/mkspecs/modules/qt_webkit.pri
%{_qt4_headerdir}/QtWebKit/
%{_qt4_libdir}/libQtWebKit.prl
%{_qt4_libdir}/libQtWebKit.so
%{_libdir}/pkgconfig/QtWebKit.pc


%changelog
* Wed Dec 11 2013 Rex Dieter <rdieter@fedoraproject.org> - 2.3.3-3
- support out-of-source-tree build
- %%ix86: build both no-sse2 and sse2 versions

* Mon Dec 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-2
- build-webkit --system-malloc (unconditionally, WAS only ppc)

* Thu Oct 03 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.3-1
- qtwebkit-2.3.3
- include some post 2.3.3 commits/fixes

* Thu Sep 12 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.2-3
- SIGSEGV - ~NonSharedCharacterBreakIterator (#1006539, webkit#101337)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.2-1
- qtwebkit-2.3.2

* Thu Apr 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 2.3.1-1
- qtwebkit-2.3.1
- -devel: drop explicit Requires: qt4-devel (let pkgconfig deps do it)

* Mon Mar 25 2013 Dan Hor??k <dan[at]danny.cz> 2.3.0-2
- use ppc fixes also on s390

* Fri Mar 15 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3.0-1
- 2.3.0 (final)
- enable libwebp support
- .spec cleanup

* Sat Mar 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3-0.6.rc1
- should use libxml and libxslt (#919778)

* Sat Mar 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3-0.5.rc1
- qt_webkit_version.pri is missing in 2.3-rc1 package (#919477)

* Tue Mar 05 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3-0.4.rc1
- 2.3-rc1

* Tue Mar 05 2013 Than Ngo <than@redhat.com> - 2.3-0.3.beta2
- add missing function Double2Ints() on ppc, backport

* Mon Feb 25 2013 Than Ngo <than@redhat.com> - 2.3-0.2.beta2
- fix 64k page issue on ppc/ppc64
- set -g1 on ppc/ppc64 to reduce archive size

* Thu Feb 21 2013 Rex Dieter <rdieter@fedoraproject.org> 2.3-0.1.beta2
- qtwebkit-2.3-beta2

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-8
- fix rpath (#902571)

* Tue Jan 15 2013 Than Ngo <than@redhat.com> - 2.2.2-7
- use SYSTEM_MALLOC on ppc/ppc64

* Fri Jan 11 2013 Than Ngo <than@redhat.com> 2.2.2-6
- bz#893447, fix 64k pagesize issue

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-5
- segfault in requiresLineBox at rendering/RenderBlockLineLayout.cpp (#891464)

* Mon Dec 24 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-4
- switch to upstream versions of some patches

* Tue Nov 13 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-3
- Certain SVG content freezes QtWebKit (webkit#97258)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.2-1
- qtwebkit-2.2.2

* Fri May 11 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.1-6
- can't render Complex Text Layout (Hindi, Arabic) (#761337)

* Fri May 11 2012 Rex Dieter <rdieter@fedoraproject.org> 2.2.1-5
- respin tarball using upstream make-package.py tool

* Tue Jan 24 2012 Than Ngo <than@redhat.com> - 2.2.1-4
- gcc doesn't support flag -fuse-ld=gold yet
- fix build failure with gcc-4.7 

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Than Ngo <than@redhat.com> - 2.2.1-2
- backport the correct patch from trunk to fix glib-2.31 issue

* Mon Dec 19 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.1-1
- qtwebkit-2.2.1
- add explicit BR: pkgconfig(xext) pkgconfig(xrender)

* Sun Nov 27 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-3
- add explicit BR: libjpeg-devel libpng-devel

* Fri Nov 18 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-2
- fix FTBFS against newer glib

* Thu Sep 29 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-1
- qtwebkit-2.2.0 (final)
- more pkgconfig-style deps

* Wed Sep 14 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2.0-0.1.rc1
- qtwebkit-2.2.0-rc1

* Tue Sep 06 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-16.week35
- qtwebkit-2.2-week35 snapshot

* Thu Sep 01 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-15.week34
- qtwebkit-2.2-week34 snapshot

* Sat Aug 27 2011 Than Ngo <than@redhat.com> - 2.2-14.week32
- drop conditional

* Thu Aug 18 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-13.week32
- qtwebkit-2.2-week32 snapshot

* Wed Aug 10 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-12.week31
- BR: gstreamer-devel bits

* Tue Aug 09 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-11.week31
- qtwebkit-2.2-week31 snapshot

* Sat Jul 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-10.week28
- rebuild

* Wed Jul 20 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-9.week28
- qtwebkit-2.2-week28 snapshot

* Wed Jul 20 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-8.20110621
- rebuild (qt48)

* Wed Jun 22 2011 Dan Hor??k <dan[at]danny.cz> 2.2-7.20110621
- bump release for the s390 build fix

* Tue Jun 21 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-6.20110621
- 20110621 snapshot
- s390: respin javascriptcore_debuginfo.patch to omit -g from CXXFLAGS too

* Fri Jun 03 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-5.20110603
- 20110603 snapshot
- drop unused/deprecated phonon/gstreamer support snippets
- add minimal qt4 dep

* Tue May 24 2011 Than Ngo <than@redhat.com> - 2.2-4.20110513
- fix for qt-4.6.x
- add condition for rhel
- enable shared for qtwebkit build

* Thu May 19 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-3.20110513
- bump up Obsoletes: qt-webkit a bit, to be on the safe side

* Fri May 13 2011 Rex Dieter <rdieter@fedoraproject.org> 2.2-2.20110513
- 20110513 qtwebkit-2.2 branch snapshot
- cleanup deps
- drop -Werror

* Thu May 12 2011 Than Ngo <than@redhat.com> - 2.2-1
- 2.2-tp1
- gstreamer is now default, drop unneeded phonon patch

* Fri Apr 22 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-4
- javascriptcore -debuginfo too (#667175)

* Fri Apr 22 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-3
- Provides: qt(4)-webkit(-devel) = 2:%%version...

* Thu Apr 21 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-2
- -devel: Conflicts: qt-devel < 1:4.7.2-9 (qt_webkit_version.pri)
- drop old/deprecated Obsoletes/Provides: WebKit-qt
- use modified, less gigantic tarball
- patch to use phonon instead of QtMultimediaKit
- patch pluginpath for /usr/lib{,64}/mozilla/plugins-wrapped

* Tue Apr 19 2011 Rex Dieter <rdieter@fedoraproject.org> 2.1-1
- 2.1

* Mon Nov 08 2010 Than Ngo <than@redhat.com> - 2.0-2
- fix webkit to export symbol correctly

* Tue Nov 02 2010 Rex Dieter <rdieter@fedoraproject.org> 2.0-1
- 2.0 (as released with qt-4.7.0)

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> 2.0-0.1.week32
- first try, borrowing a lot from debian/kubuntu packaging
