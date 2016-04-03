# Based on Tom Callaway's <spot@fedoraproject.org> work
# Based on Johnny Hughes's <johnny@centos.org> work
# To get the source code tarballs see:
#
# https://github.com/zcbenz/chromium-source-tarball


%define chromium_path /opt/chromium

Name:		chromium
Version:	49.0.2623.110
Release:	1%{?dist}
Summary:	A WebKit powered web browser

License:	BSD and LGPLv2+
Group:		Applications/Internet

Patch0:		gtk2fix.patch
Patch1:		chrometypesbug.patch
Patch2:		ppapifix.patch
Patch3:		chromiumlibssclfix.patch
Patch4:		capfix.patch
Patch5:         capfix43.patch
Patch6:         chromium-43.0.2357.65-capture_v4l2.patch
Patch7:         542819fix.patch

Source0:	https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%{version}.tar.xz
Source1:	chromium-devel.desktop

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gcc-c++, bison, flex, gtk2-devel, atk-devel
BuildRequires:	nss-devel >= 3.12.3
BuildRequires:	pciutils-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	gnome-keyring-devel
BuildRequires:	cups-devel
BuildRequires:	libudev-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	libXdamage-devel
BuildRequires:  redhat-lsb-core
BuildRequires:	libXScrnSaver-devel
BuildRequires:	glibc-devel
BuildRequires:  libffi-devel
BuildRequires:	libXtst-devel
BuildRequires:	fontconfig-devel, GConf2-devel, dbus-devel
BuildRequires:	glib2-devel
BuildRequires:	gperf
BuildRequires:  glibc-headers
BuildRequires:	alsa-lib-devel
BuildRequires:	libusb-devel, expat-devel
BuildRequires:	desktop-file-utils
BuildRequires:  git
BuildRequires:  pkgconfig
BuildRequires:  python
BuildRequires:  libdrm-devel
BuildRequires:  libexif-devel
BuildRequires:  libcap-devel
BuildRequires:  openssl-devel

%if 0%{?fedora:1} || 0%{?rhel} >= 7
BuildRequires:  systemd-devel
%endif


%if 0%{?rhel} == 6
BuildRequires:  devtoolset-2-binutils
BuildRequires:  devtoolset-2-gcc-c++
BuildRequires:  devtoolset-2-gcc
BuildRequires:  python27
BuildRequires:  chromiumlibs
BuildRequires:  chromiumlibs-runtime
BuildRequires:  chromiumlibs-glib2
BuildRequires:  chromiumlibs-glib2-devel

Requires:       chromiumlibs
Requires:       chromiumlibs-runtime
Requires:       chromiumlibs-glib2
%endif



ExclusiveArch:	%{ix86} arm x86_64

%description
Chromium is an open-source web browser, powered by WebKit.
Upstream to Google Chrome.

%prep
%setup -q -n chromium-%{version}

# These patches and workarounds only required under RHEL 6.
%if 0%{?rhel} == 6
%if "%{?version:%{version}}%{!?version:0}" < "41.0.2267.0"
%patch0 -p1 -b .gtk2fix
%endif
%if "%{?version:%{version}}%{!?version:0}" < "43.0.2327.5"
%if "%{?version:%{version}}%{!?version:0}" >= "42.0.2292.0"
%patch4 -p1 -b .capfix
%endif
%endif
%if "%{?version:%{version}}%{!?version:0}" >= "43.0.2327.5"
#%patch5 -p1 -b .capfix43
%patch6 -p1 -b .capfix43a
%endif

%if "%{?version:%{version}}%{!?version:0}" < "42.0.2305.3"
%patch1 -p1 -b .typesbug
%endif


. /opt/rh/devtoolset-2/enable
. /opt/rh/python27/enable
. /opt/rh/chromiumlibs/enable
%endif

%patch7 -p1 -b .542819fix


# Unfortunately, the ninja package from fedora DOES NOT work. And "make" is 
# depriciated for chromium. (it doesn't work any longer) So we have to actually
# get the depot tools from google with git I'm afraid...

git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

export PATH="${PATH}:$(pwd)/depot_tools"

# Please note: If you intend to build this package outside of NCSU, please
# get your own chromium "api keys" as explained here:
# http://www.chromium.org/developers/how-tos/api-keys

#%ifarch x86_64
#build/linux/sysroot_scripts/install-sysroot.py --running-as-hook
#%else
#build/linux/sysroot_scripts/install-sysroot.py --arch i386
#%endif


build/gyp_chromium -f ninja \
	--depth . \
%ifarch x86_64
	-Dtarget_arch=x64 \
	-Dsystem_libdir=lib64 \
%endif
	-Dgoogle_api_key="AIzaSyA9CVqG-viO0VB3n-ajb9fJe1XP6epQ_fE" \
	-Dgoogle_default_client_id="444223224839-qsmp17h726v5846fnmhttreqgr73p8lb.apps.googleusercontent.com" \
	-Dgoogle_default_client_secret="HS7YJpEhkTEIntt4kM4fDrHw" \
	-Ddisable_glibc=1 \
	-Ddisable_nacl=1 \
	-Ddisable_sse2=1 \
	-Dlinux_link_gnome_keyring=0 \
	-Dlinux_link_gsettings=1 \
	-Dlinux_link_libpci=1 \
	-Dlinux_link_libgps=0 \
	-Dlinux_sandbox_path=%{chromium_path}/chrome-sandbox \
	-Dlinux_sandbox_chrome_path=%{chromium_path}/chrome \
	-Dlinux_strip_binary=1 \
	-Dlinux_use_gold_binary=0 \
	-Dlinux_use_gold_flags=0 \
	-Dlinux_use_libgps=0 \
	-Dmedia_use_libvpx=1 \
	-Dno_strict_aliasing=1 \
	-Dproprietary_codecs=1 \
	-Dremove_webcore_debug_symbols=1 \
	-Duse_gconf=0 \
	-Duse_gnome_keyring=0 \
	-Duse_pulseaudio=1 \
	-Dffmpeg_branding=Chromium \
	-Dlogging_like_official_build=1 \
	-Duse_system_harfbuzz=0 \
	-Ddisable_fatal_linker_warnings=1 \
	-Dclang=0 \
	-Dfieldtrial_testing_like_official_build=1 \
	-Duse_sysroot=0 \
	-Dwerror=

mkdir -p out/Release

%build

# These workarounds only required under RHEL 6.
%if 0%{?rhel} == 6
. /opt/rh/devtoolset-2/enable
. /opt/rh/python27/enable
. /opt/rh/chromiumlibs/enable
%endif


export PATH="${PATH}:$(pwd)/depot_tools"
ninja -v -j4 -C out/Release chrome chrome_sandbox


# RPM can't use patch macro in a build section? WTF rpm developers?...
# Fix wrapper on all platforms to use /opt/chromium/PepperFlash/libpepflashplayer.so
# but only if it exists...
echo "Patch #2:"
patch -p0 -s < %{PATCH2}

%if 0%{?rhel} == 6
# Fix wrapper to use "chromiumlibs" scl if on RHEL 6 system. (Needs newer glib2)
echo "Patch #3:"
patch -p0 -s < %{PATCH3}
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromium_path}
ln -s %{chromium_path}/chrome-wrapper %{buildroot}%{_bindir}/chromium-browser
mkdir -p %{buildroot}%{_mandir}/man1/

pushd out/Release
cp -a *.pak locales resources %{buildroot}%{chromium_path}
cp -a chrome %{buildroot}%{chromium_path}/chrome
cp -a chrome-wrapper %{buildroot}%{chromium_path}/chrome-wrapper
cp -a chrome_sandbox %{buildroot}%{chromium_path}/chrome-sandbox
cp -a chrome.1 %{buildroot}%{_mandir}/man1/chromium-browser.1
mkdir -p %{buildroot}%{chromium_path}/plugins/
#cp -a libffmpegsumo.so %{buildroot}%{chromium_path}
cp -a icudtl.dat %{buildroot}%{chromium_path}

%if "%{?version:%{version}}%{!?version:0}" < "42.0.2298.0"
cp -a libpdf.so %{buildroot}%{chromium_path}
%endif

cp -a libyuv.a %{buildroot}%{chromium_path}
# For backwards compatibility...
cp -a product_logo_48.png %{buildroot}%{chromium_path}

#https://code.google.com/p/chromium/issues/detail?id=421063
#https://code.google.com/p/chromium/issues/detail?id=437136
%if "%{?version:%{version}}%{!?version:0}" >= "41.0.2236.0"
cp -a natives_blob.bin %{buildroot}%{chromium_path}
cp -a snapshot_blob.bin %{buildroot}%{chromium_path}
%endif

popd

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/256x256/apps
cp -a chrome/app/theme/chromium/product_logo_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/chromium-browser.png

mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%{_bindir}/chromium-browser
%dir /%{chromium_path}
/%{chromium_path}/*.pak

%attr(4755, root, root) /%{chromium_path}/chrome-sandbox

#/%{chromium_path}/libffmpegsumo.so
/%{chromium_path}/icudtl.dat
/%{chromium_path}/libyuv.a
/%{chromium_path}/product_logo_48.png
/%{chromium_path}/locales/
/%{chromium_path}/plugins/
/%{chromium_path}/resources/
/%{chromium_path}/chrome
/%{chromium_path}/chrome-wrapper
%{_mandir}/man1/chromium-browser.*
%{_datadir}/icons/hicolor/256x256/apps/chromium-browser.png
%{_datadir}/applications/*.desktop
%if "%{?version:%{version}}%{!?version:0}" >= "41.0.2236.0"
/%{chromium_path}/natives_blob.bin
/%{chromium_path}/snapshot_blob.bin
%endif
%if "%{?version:%{version}}%{!?version:0}" < "42.0.2298.0"
/%{chromium_path}/libpdf.so
%endif

%changelog
* Mon Mar 28 2016 Gary Gatling <gsgatlin@ncsu.edu> 49.0.2623.110-1
- Update to new version.

* Thu Mar 24 2016 Gary Gatling <gsgatlin@ncsu.edu> 49.0.2623.108-1
- Update to new version.

* Tue Mar 8 2016 Gary Gatling <gsgatlin@ncsu.edu> 49.0.2623.87-1
- Update to new version.

* Thu Mar 3 2016 Gary Gatling <gsgatlin@ncsu.edu> 49.0.2623.75-1
- Update to new version.

* Thu Feb 18 2016 Gary Gatling <gsgatlin@ncsu.edu> 48.0.2564.116-1
- Update to new version.

* Mon Feb 15 2016 Gary Gatling <gsgatlin@ncsu.edu> 48.0.2564.109-1
- Update to new version.

* Thu Feb 04 2016 Gary Gatling <gsgatlin@ncsu.edu> 48.0.2564.103-1
- Update to new version.

* Thu Jan 28 2016 Gary Gatling <gsgatlin@ncsu.edu> 48.0.2564.97-1
- Update to new version.

* Thu Jan 21 2016 Gary Gatling <gsgatlin@ncsu.edu> 48.0.2564.82-1
- Update to new version.

* Thu Jan 14 2016 Gary Gatling <gsgatlin@ncsu.edu> 47.0.2526.111-1
- Update to new version.

* Wed Dec 16 2015 Gary Gatling <gsgatlin@ncsu.edu> 47.0.2526.106-1
- Update to new version.

* Wed Dec 9 2015 Gary Gatling <gsgatlin@ncsu.edu> 47.0.2526.80-1
- Update to new version.

* Tue Dec 1 2015 Gary Gatling <gsgatlin@ncsu.edu> 47.0.2526.73-1
- Update to new version.

* Wed Nov 11 2015 Gary Gatling <gsgatlin@ncsu.edu> 46.0.2490.86-1
- Update to new version.

* Thu Oct 22 2015 Gary Gatling <gsgatlin@ncsu.edu> 46.0.2490.80-1
- Update to new version.

* Tue Oct 13 2015 Gary Gatling <gsgatlin@ncsu.edu> 46.0.2490.71-1
- Update to new version.
- add patch for bug 542819

* Fri Sep 25 2015 Gary Gatling <gsgatlin@ncsu.edu> 45.0.2454.101-1
- Update to new version.

* Thu Sep 24 2015 Gary Gatling <gsgatlin@ncsu.edu> 45.0.2454.99-1
- Update to new version.

* Tue Sep 15 2015 Gary Gatling <gsgatlin@ncsu.edu> 45.0.2454.93-1
- Update to new version.

* Wed Sep 2 2015 Gary Gatling <gsgatlin@ncsu.edu> 45.0.2454.85-1
- Update to new version.

* Thu Aug 20 2015 Gary Gatling <gsgatlin@ncsu.edu> 44.0.2403.157-1
- Update to new version.

* Tue Aug 4 2015 Gary Gatling <gsgatlin@ncsu.edu> 44.0.2403.155-1
- Update to new version.

* Tue Aug 4 2015 Gary Gatling <gsgatlin@ncsu.edu> 44.0.2403.130-1
- Update to new version.

* Tue Jul 28 2015 Gary Gatling <gsgatlin@ncsu.edu> 44.0.2403.125-1
- Update to new version.

* Tue Jul 28 2015 Gary Gatling <gsgatlin@ncsu.edu> 44.0.2403.107-1
- Update to new version.

* Tue Jul 21 2015 Gary Gatling <gsgatlin@ncsu.edu> 44.0.2403.89-1
- Update to new version.

* Tue Jul 14 2015 Gary Gatling <gsgatlin@ncsu.edu> 43.0.2357.134-1
- Update to new version.

* Tue Jun 23 2015 Gary Gatling <gsgatlin@ncsu.edu> 43.0.2357.132-1
- Update to new version.

* Tue Jun 23 2015 Gary Gatling <gsgatlin@ncsu.edu> 43.0.2357.130-1
- Update to new version.

* Thu Jun 18 2015 Gary Gatling <gsgatlin@ncsu.edu> 43.0.2357.125-1
- Update to new version.

* Wed Jun 10 2015 Gary Gatling <gsgatlin@ncsu.edu> 43.0.2357.124-1
- Update to new version.

* Mon Jun 8 2015 Gary Gatling <gsgatlin@ncsu.edu> 43.0.2357.81-3
- Add gcc51fix.

* Mon Jun 1 2015 Gary Gatling <gsgatlin@ncsu.edu> 43.0.2357.81-2
- Update to new version.
- We can no longer build for RHEL 6 due to kernel being too old.
  Any patches to work around this problem are welcome.

* Tue May 19 2015 Gary Gatling <gsgatlin@ncsu.edu> 43.0.2357.65-1
- Update to new version.

* Tue May 12 2015 Gary Gatling <gsgatlin@ncsu.edu> 42.0.2311.152-1
- Update to new version.

* Wed Apr 29 2015 Gary Gatling <gsgatlin@ncsu.edu> 42.0.2311.135-1
- Update to new version.

* Tue Apr 14 2015 Gary Gatling <gsgatlin@ncsu.edu> 42.0.2311.90-1
- Update to new version.

* Thu Apr 2 2015 Gary Gatling <gsgatlin@ncsu.edu> 41.0.2272.118-1
- Update to new version.

* Thu Mar 12 2015 Gary Gatling <gsgatlin@ncsu.edu> 41.0.2272.101-1
- Update to new version.
- Add capfix43 patch for version 43+ and RHEL 6.

* Wed Mar 11 2015 Gary Gatling <gsgatlin@ncsu.edu> 41.0.2272.89-1
- Update to new version.

* Wed Mar 4 2015 Gary Gatling <gsgatlin@ncsu.edu> 41.0.2272.76-1
- Update to new version.

* Thu Feb 19 2015 Gary Gatling <gsgatlin@ncsu.edu> 40.0.2214.115-1
- Update to new version.
- Conditionally remove libpdf.so from files section.
- Conditionally remove chrometypesbug.patch

* Sat Feb 07 2015 Gary Gatling <gsgatlin@ncsu.edu> 40.0.2214.111-1
- Update to new version.

* Wed Feb 04 2015 Gary Gatling <gsgatlin@ncsu.edu> 40.0.2214.95-1
- Update to new version.
- Add back in capfix.patch for future version...

* Fri Jan 30 2015 Gary Gatling <gsgatlin@ncsu.edu> 40.0.2214.94-1
- Update to new version.

* Tue Jan 27 2015 Gary Gatling <gsgatlin@ncsu.edu> 40.0.2214.93-1
- Update to new version.

* Thu Jan 22 2015 Gary Gatling <gsgatlin@ncsu.edu> 40.0.2214.91-1
- Update to new version.
- Remove capfix.patch (Fixed in chromium > 41.0.2272.12)

* Thu Jan 15 2015 Gary Gatling <gsgatlin@ncsu.edu> 39.0.2171.99-1
- Update to new version.
- Fix issues with RHEL 6 and chromium > 41.0.2267.0 (capfix.patch)

* Thu Dec 11 2014 Gary Gatling <gsgatlin@ncsu.edu> 39.0.2171.95-1
- Update to new version.
- Fix issues #437136 and #421063 in chromium newer then 41.0.2236.0.
  https://code.google.com/p/chromium/issues/detail?id=437136
  https://code.google.com/p/chromium/issues/detail?id=421063

* Wed Nov 26 2014 Gary Gatling <gsgatlin@ncsu.edu> 39.0.2171.71-1
- Update to new version.

* Wed Nov 19 2014 Gary Gatling <gsgatlin@ncsu.edu> 39.0.2171.65-1
- Update to new version.

* Wed Nov 12 2014 Gary Gatling <gsgatlin@ncsu.edu> 38.0.2125.122-1
- Update to new version.

* Mon Oct 27 2014 Gary Gatling <gsgatlin@ncsu.edu> 38.0.2125.111-1
- Update to new version.

* Tue Oct 14 2014 Gary Gatling <gsgatlin@ncsu.edu> 38.0.2125.104-1
- Update to new version.

* Tue Oct 7 2014 Gary Gatling <gsgatlin@ncsu.edu> 38.0.2125.101-1
- Update to new version.

* Sun Sep 14 2014 Gary Gatling <gsgatlin@ncsu.edu> 37.0.2062.120-2
- Redo chromiumlibssclfix.patch for RHEL 6 boxes.

* Sat Sep 13 2014 Gary Gatling <gsgatlin@ncsu.edu> 37.0.2062.120-1
- Re-work / Redo this package for my users and newer chromium.

