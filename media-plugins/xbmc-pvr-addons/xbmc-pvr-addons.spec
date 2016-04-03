# Upstream xbmc hardcodes a Git hash for OSes that bundle xbmc-pvr-addons. Let's
# try using the same hash that upstream uses for the current XBMC version
# available in RPMFusion. It can be found in the XBMC source tree like so:
#   grep ^VERSION tools/depends/target/xbmc-pvr-addons/Makefile
%global commit be12a8da2072e9c3ddad54892df2f85b759d4e9a
%global short_commit %(c=%{commit}; echo ${c:0:7})
%global commit_date 20140716
%global snapshot_release %{commit_date}git%{short_commit}
# %%global tag 13.0-Gotham

# Minimum supported version of XBMC
%global xbmc_version 13.2-0.3.beta3

Name:           xbmc-pvr-addons
Version:        13.0
Release:        2.%{snapshot_release}%{?dist}
# Release:        1%%{?dist}
Summary:        XBMC PVR add-ons

Group:          Applications/Multimedia
# Entire package is GPLv3 (see COPYING). All the PVR addons are GPLv2+. Portions
# of lib/libhts and lib/cmyth are LGPLv2+. lib/dvblinkremote is MIT
License:        GPLv3 and GPLv2+ and LGPLv2+ and MIT
URL:            https://github.com/opdenkamp/xbmc-pvr-addons
Source0:        https://github.com/opdenkamp/%{name}/archive/%{short_commit}/%{name}-%{short_commit}.tar.gz
# Source0:        https://github.com/opdenkamp/%%{name}/archive/%%{tag}/%%{name}-%%{tag}.tar.gz
# Use system jsoncpp library
Patch0:         %{name}-13.0-use_external_jsoncpp.patch
# Use system rapidxml library
Patch1:         %{name}-13.0-use_external_rapidxml.patch
# Use system tinyxml library
Patch2:         %{name}-13.0-use_external_tinyxml.patch
# Use system tinyxml2 library
Patch3:         %{name}-13.0-use_external_tinyxml2.patch
# Use system XBMC headers
Patch4:         %{name}-13.0-use_external_xbmc.patch
# Use safe format arg to snprintf to fix build on Fedora 21 (see
# https://github.com/opdenkamp/xbmc-pvr-addons/pull/296)
Patch5:         %{name}-13.0-snprintf.patch

BuildRequires:  boost-devel
BuildRequires:  jsoncpp-devel
BuildRequires:  libtool
BuildRequires:  mariadb-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  rapidxml-devel
BuildRequires:  tinyxml-devel
BuildRequires:  tinyxml2-devel
BuildRequires:  vdr-devel
BuildRequires:  xbmc-devel >= %{xbmc_version}
BuildRequires:  zlib-devel

%description
%{summary}.


%package        common
Summary:        Files common to XBMC PVR addons
Group:          Applications/Multimedia
BuildArch:      noarch

%description    common
This package contains files common to XBMC PVR addons.


%package -n     xbmc-pvr-argustv
Summary:        XBMC frontend for the ARGUS TV PVR
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-argustv
ARGUS TV PVR frontend for XBMC. Supports streaming of Live TV & recordings,
listening to radio channels, EPG and schedules.


%package -n     xbmc-pvr-demo
Summary:        Demo PVR Client for XBMC
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-demo
%{summary}.


%package -n     xbmc-pvr-dvblink
Summary:        XBMC PVR Plugin for DVBLink
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-dvblink
PVR Plugin for DVBLink from DvbLogic.com for XBMC; supporting streaming of Live
TV & recordings, EPG, timers.


%package -n     xbmc-pvr-dvbviewer
Summary:        XBMC's frontend for DVBViewer
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-dvbviewer
DVBViewer Recording Service frontend; supporting streaming of LiveTV, timers,
recordings & EPG.


%package -n     xbmc-pvr-hts
Summary:        XBMC's frontend for Tvheadend
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}

Provides:       bundled(sha1-niedermayer)

%description -n xbmc-pvr-hts
Tvheadend frontend; supporting streaming of Live TV & recordings, EPG, timers.


%package -n     xbmc-pvr-iptvsimple
Summary:        XBMC PVR addon for IPTV support
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-iptvsimple
IPTV Simple PVR Client support m3u playlists, streaming of Live TV for
multicast/unicast sources, listening to radio channels and EPG.


%package -n     xbmc-pvr-mediaportal-tvserver
Summary:        XBMC frontend for the MediaPortal TV Server (ffmpeg + tsreader version)
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-mediaportal-tvserver
MediaPortal TV Server frontend for XBMC. Supports streaming of Live TV &
recordings, listening to radio channels, EPG and timers. This addon combines the
former ffmpeg and tsreader addons.


%package -n     xbmc-pvr-mythtv-cmyth
Summary:        XBMC frontend for MythTV (using libcmyth)
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-mythtv-cmyth
MythTV frontend (up to MythTV 0.27). Supports streaming of Live TV & recordings,
listening to radio channels, EPG and timers.


%package -n     xbmc-pvr-nextpvr
Summary:        XBMC frontend for the NextPVR
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}

Provides:       bundled(md5-plumb)

%description -n xbmc-pvr-nextpvr
NextPVR frontend for XBMC. Supports streaming of Live TV & recordings, listening
to radio channels and EPG.


%package -n     xbmc-pvr-njoy
Summary:        Njoy N7 PVR Client for XBMC
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-njoy
%{summary}.


%package -n     xbmc-pvr-vdr-vnsi
Summary:        PVR client to connect VDR to XBMC over the VNSI interface
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-vdr-vnsi
VDR frontend for XBMC; supporting streaming of Live TV & recordings, EPG, timers
over the VNSI plugin.

NOTE: this package requires the VNSI plugin (package vdr-vnsiserver on Fedora)
to be installed on the VDR backend.


%package -n     xbmc-pvr-vuplus
Summary:        XBMC's frontend for VU+ / Enigma2 based settop boxes
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-vuplus
VU+ frontend; supporting streaming of Live TV & recordings, EPG, timers.


%package -n     xbmc-pvr-wmc
Summary:        Windows Media Center client for XBMC
Group:          Applications/Multimedia
Requires:       %{name}-common = %{version}-%{release}
Requires:       xbmc >= %{xbmc_version}


%description -n xbmc-pvr-wmc
An XBMC client to interface to Windows Media Center's record and EPG service.


%prep
%setup -q -n %{name}-%{commit}
# %%setup -q -n %%{name}-%%{tag}
%patch0 -p0 -b .use_external_jsoncpp
%patch1 -p0 -b .use_external_rapidxml
%patch2 -p0 -b .use_external_tinyxml
%patch3 -p0 -b .use_external_tinyxml2
%patch4 -p0 -b .use_external_xbmc
%patch5 -p1 -b .snprintf

# Delete bundled libraries jsoncpp, rapidxml, and tinyxml2
rm -r lib/{jsoncpp,rapidxml,tinyxml2}/
# Delete bundled tinyxml, but keep wrapper headers provided by XBMC developers
rm lib/tinyxml/{Makefile.am,readme.txt,tiny*}
# Delete bundled XBMC headers
rm -r xbmc/{*.h,xbmc_stream_utils.hpp}

# Delete empty M3U file provided by the iptvsimple addon (see
# https://github.com/opdenkamp/xbmc-pvr-addons/pull/298)
rm addons/pvr.iptvsimple/addon/iptv.m3u


%build
[ -f configure ] || ./bootstrap
%configure \
  --enable-addons-with-dependencies \
  --libdir=%{_libdir}/xbmc/addons/ \
  --datadir=%{_datadir}/xbmc/addons/
make %{?_smp_mflags}


%install
%make_install

# Fix permissions (see https://github.com/opdenkamp/xbmc-pvr-addons/pull/303)
find $RPM_BUILD_ROOT%{_datadir}/xbmc/addons/ -type f -exec chmod 0644 {} \;

# Delete useless files (see
# https://github.com/opdenkamp/xbmc-pvr-addons/pull/301)
rm $RPM_BUILD_ROOT%{_datadir}/xbmc/addons/*/*.in


%files common
# TODO: add ChangeLog and NEWS if non-empty
%doc AUTHORS COPYING README


%files -n xbmc-pvr-argustv
%doc addons/pvr.argustv/addon/changelog.txt
%{_libdir}/xbmc/addons/pvr.argustv/
%{_datadir}/xbmc/addons/pvr.argustv/


%files -n xbmc-pvr-demo
%{_libdir}/xbmc/addons/pvr.demo/
%{_datadir}/xbmc/addons/pvr.demo/


%files -n xbmc-pvr-dvblink
%doc addons/pvr.dvblink/addon/changelog.txt
%{_libdir}/xbmc/addons/pvr.dvblink/
%{_datadir}/xbmc/addons/pvr.dvblink/


%files -n xbmc-pvr-dvbviewer
%doc addons/pvr.dvbviewer/addon/changelog.txt
%{_libdir}/xbmc/addons/pvr.dvbviewer/
%{_datadir}/xbmc/addons/pvr.dvbviewer/


%files -n xbmc-pvr-hts
%doc addons/pvr.hts/addon/changelog.txt
%{_libdir}/xbmc/addons/pvr.hts/
%{_datadir}/xbmc/addons/pvr.hts/


%files -n xbmc-pvr-iptvsimple
%doc addons/pvr.iptvsimple/addon/changelog.txt
%{_libdir}/xbmc/addons/pvr.iptvsimple/
%{_datadir}/xbmc/addons/pvr.iptvsimple/


%files -n xbmc-pvr-mediaportal-tvserver
%doc addons/pvr.mediaportal.tvserver/{addon/changelog.txt,addon/LICENSE.txt,src/README}
%{_libdir}/xbmc/addons/pvr.mediaportal.tvserver/
%{_datadir}/xbmc/addons/pvr.mediaportal.tvserver/


%files -n xbmc-pvr-mythtv-cmyth
%doc addons/pvr.mythtv.cmyth/addon/changelog.txt
%{_libdir}/xbmc/addons/pvr.mythtv.cmyth/
%{_datadir}/xbmc/addons/pvr.mythtv.cmyth/


%files -n xbmc-pvr-nextpvr
%doc addons/pvr.nextpvr/addon/changelog.txt
%{_libdir}/xbmc/addons/pvr.nextpvr/
%{_datadir}/xbmc/addons/pvr.nextpvr/


%files -n xbmc-pvr-njoy
%{_libdir}/xbmc/addons/pvr.njoy/
%{_datadir}/xbmc/addons/pvr.njoy/


%files -n xbmc-pvr-vdr-vnsi
%{_libdir}/xbmc/addons/pvr.vdr.vnsi/
%{_datadir}/xbmc/addons/pvr.vdr.vnsi/


%files -n xbmc-pvr-vuplus
%doc addons/pvr.vuplus/addon/changelog.txt
%{_libdir}/xbmc/addons/pvr.vuplus/
%{_datadir}/xbmc/addons/pvr.vuplus/


%files -n xbmc-pvr-wmc
%{_libdir}/xbmc/addons/pvr.wmc/
%{_datadir}/xbmc/addons/pvr.wmc/


%changelog
* Wed Aug 06 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 13.0-2.20140716gitbe12a8d
- Sync with XBMC 13.2 beta3
- Use bundled (and heavily patched!) version of dvblinkremote library
- Use system tinyxml2 library to build dvblinkremote instead of bundled one


* Tue May 13 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 13.0-1
- Update to 13.0
- Drop empty M3U file provided by the iptvsimple addon
- Add upstream report links for each packaging issue in comments
- Add common subpackage for common license/documentation files
- Add missing license GPLv3
- Drop vdr-vnsiserver subpackage (now a separate project, packaged in Fedora)

* Fri May 09 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 13.0-0.4.Gotham_rc1
- Fix build on Fedora 21 (thanks to Ken Dreyer)
- Fix license tag
- Spec cleanup
- Add Provides for bundled implementations of MD5 and SHA1 (copylibs)

* Fri May 02 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 13.0-0.3.Gotham_rc1
- Sync with XBMC Gotham_rc1

* Mon Mar 24 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 13.0-0.2.20140314git1d9e336
- Sync with XBMC Gotham_beta2
- Drop embedded dvblinkremote and tinyxml2 libraries
- Add new dvblink and wmc subpackages

* Tue Feb 11 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 13.0-0.1.20130907git18597fd
- Initial RPM release
