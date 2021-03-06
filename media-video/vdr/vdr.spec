# TODO, maybe some day:
# - livebuffer patch, http://www.vdr-portal.de/board/thread.php?threadid=37309
# - channelfilter patch, http://www.u32.de/vdr.html#patches
# - more rofa's patches, http://www.saunalahti.fi/~rahrenbe/vdr/patches/
# - pause patch (causes OSD placement issues at least with unrebuilt text2skin)
#   http://www.tolleri.net/vdr/vdr/vdr-1.6.0-2-pause-0.0.1.patch
#   http://thread.gmane.org/gmane.linux.vdr/40188

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global _hardened_build 1
%bcond_without    docs

%global varbase   %{_var}/lib/vdr
%global videodir  %{varbase}/video
%global vardir    %{varbase}/data
%global plugindir %{_libdir}/vdr
%global configdir %{_sysconfdir}/vdr
%global cachedir  %{_var}/cache/vdr
%global rundir    %{_var}/run/vdr
%global vdr_user  vdr
%global vdr_group video
# From APIVERSION in config.h
%global apiver    2.0.0

Name:           vdr
Version:        2.0.5
Release:        1%{?dist}
Summary:        Video Disk Recorder

License:        GPLv2+
URL:            http://www.tvdr.de/
Source0:        ftp://ftp.tvdr.de/vdr/%{name}-%{version}.tar.bz2
Source1:        %{name}.service
Source2:        %{name}.sysconfig
Source3:        %{name}.sudoers
Source4:        %{name}-udev.rules
Source5:        %{name}-reccmds.conf
Source6:        %{name}-commands.conf
Source7:        %{name}-runvdr.sh
Source8:        %{name}-dvbsddevice.conf
Source9:        %{name}-config.sh
Source10:       %{name}-README.package
Source11:       %{name}-skincurses.conf
Source12:       %{name}-dvbhddevice.conf
Source13:       %{name}-timercmds.conf
Source14:       %{name}-shutdown.sh
Source15:       %{name}-moveto.sh
Source16:       %{name}-CHANGES.package.old
Source17:       %{name}.macros
Source18:       http://cdn.debian.net/debian/pool/main/v/vdr/vdr_2.0.3-1.debian.tar.bz2
Source19:       %{name}-check-setup.sh
Source20:       %{name}-rcu.conf
Source21:       %{name}-set-wakeup.sh
Patch0:         %{name}-channel+epg.patch
Patch1:         http://zap.tartarus.org/~ds/debian/dists/stable/main/source/vdr_1.4.5-2.ds.diff.gz
Patch2:         http://www.saunalahti.fi/~rahrenbe/vdr/patches/vdr-2.0.3-vasarajanauloja.patch.gz
# Extracted from http://copperhead.htpc-forum.de/downloads/extensionpatch/extpngvdr1.7.21v1.diff.gz
Patch3:         %{name}-1.7.21-plugin-missing.patch
Patch4:         %{name}-1.7.41-paths.patch
Patch5:         http://toms-cafe.de/vdr/download/vdr-timer-info-0.5-1.7.13.diff
# http://article.gmane.org/gmane.linux.vdr/36097
Patch6:         %{name}-1.5.18-syncearly.patch
Patch7:         http://projects.vdr-developer.org/projects/plg-ttxtsubs/repository/revisions/master/raw/patches/vdr-1.7.40-ttxtsubs.patch
# Extracted from http://copperhead.htpc-forum.de/downloads/extensionpatch/extpngvdr1.7.21v1.diff.gz
# Original at http://toms-cafe.de/vdr/download/vdr-jumpplay-1.0-1.7.6.diff
Patch8:         %{name}-1.7.28-vasarajanauloja-jumpplay.patch
# http://www.udo-richter.de/vdr/patches.en.html#hlcutter
Patch9:         http://www.udo-richter.de/vdr/files/vdr-1.7.29-hlcutter-0.2.3.diff
# http://www.udo-richter.de/vdr/naludump.en.html
Patch10:        http://www.udo-richter.de/vdr/files/vdr-2.1.2-naludump-0.1.diff
# http://article.gmane.org/gmane.linux.vdr/43590
Patch11:        %{name}-2.0.4-mainmenuhooks101.patch
# http://projects.vdr-developer.org/git/vdr-plugin-epgsearch.git/plain/patches/timercmd-0.1_1.7.17.diff
# Modified so that it applies over the timer-info patch
Patch12:        %{name}-1.7.21-timercmd.patch
Patch13:        http://projects.vdr-developer.org/git/vdr-plugin-epgsearch.git/plain/patches/vdr-1.5.17-progressbar-support-0.0.1.diff
# Extracted from http://www.saunalahti.fi/~rahrenbe/vdr/patches/vdr-2.0.5-kamalasamala.patch.gz
Patch14:        %{name}-2.0.5-vasarajanauloja-resetresume.patch
Patch15:        %{name}-1.7.37-fedora-pkgconfig.patch
Patch16:        %{name}-1.7.21-jumpplay-finnish.patch
Patch17:        http://projects.vdr-developer.org/git/vdr-plugin-epgsearch.git/plain/patches/vdr.epgsearch-exttimeredit-0.0.2.diff
Patch18:        %{name}-timer-info-1.7.28.patch

BuildRequires:  libjpeg-devel
BuildRequires:  libcap-devel
BuildRequires:  pkgconfig
BuildRequires:  perl(File::Spec)
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gettext
# systemd >= 186 for scriptlet macros
BuildRequires:  systemd >= 186
%if %{with docs}
BuildRequires:  doxygen
BuildRequires:  graphviz
%endif # docs
# udev >= 136-1 for the audio, cdrom, dialout, and video groups
Requires:       udev >= 136-1
# sudo for the shutdown script, >= 1.7.2p2-3 for sudoers.d functionality
Requires:       sudo >= 1.7.2p2-3
# util-linux >= 2.15 for "rtcwake -m no" timer driven wakeups
Requires:       util-linux >= 2.15
# #863720
Requires:       font(:lang=en)
# shadow-utils >= 4.1.1 for useradd -N
Requires(pre):  shadow-utils >= 2:4.1.1
# systemd >= 189 for RestartPreventExitStatus=
Requires(post): systemd >= 189
Requires(preun): systemd >= 189
Requires(postun): systemd >= 189
Provides:       vdr(abi)%{?_isa} = %{apiver}
Obsoletes:      vdr-subtitles <= 0.5.0
Obsoletes:      vdr-sky < 1.7.11

%description
VDR implements a complete digital set-top-box and video recorder.
It can work with signals received from satellites (DVB-S) as well as
cable (DVB-C) and terrestrial (DVB-T) signals.  At least one DVB card
is required to run VDR.

%package        devel
Summary:        Development files for VDR
Requires:       gettext
Provides:       vdr-devel(api) = %{apiver}

%description    devel
%{summary}.

%package        docs
Summary:        Developer documentation for VDR
BuildArch:      noarch

%description    docs
%{summary}.

%package        dvbhddevice
Summary:        VDR output device plugin for TechnoTrend S2-6400 DVB cards
Requires:       vdr(abi)%{?_isa} = %{apiver}

%description    dvbhddevice
The dvbhddevice plugin implements a VDR output device for the "Full
Featured TechnoTrend S2-6400" DVB cards.

%package        dvbsddevice
Summary:        VDR output device plugin for full featured SD DVB cards
Requires:       vdr(abi)%{?_isa} = %{apiver}
# To get this subpackage pulled in on upgrades
Obsoletes:      vdr < 1.7.11

%description    dvbsddevice
The dvbsddevice plugin implements the output device for the "Full
Featured" DVB cards based on the TechnoTrend/Fujitsu-Siemens design.

%package        rcu
Summary:        VDR remote control unit plugin
Requires:       vdr(abi)%{?_isa} = %{apiver}
# To get this subpackage pulled in on upgrades
Obsoletes:      vdr < 1.7.25

%description    rcu
The rcu plugin implements a remote control unit for VDR.

%package        skincurses
Summary:        Shell window skin plugin for VDR
BuildRequires:  ncurses-devel
Requires:       vdr(abi)%{?_isa} = %{apiver}

%description    skincurses
The skincurses plugin implements a VDR skin that works in a shell
window, using only plain text output.


%prep
%setup -q -a 18
%patch0 -p1
%patch1 -p1
# sort_options would be nice, but it conflicts with channel+epg which is nicer
#patch -F 0 -i debian/patches/02_sort_options.dpatch
# TODO: does not apply since 1.7.24
#patch -F 0 -i debian/patches/06_recording_scan_speedup.dpatch
patch -F 2 -i debian/patches/07_blockify_define.dpatch
# TODO: does not apply
#patch -F 0 -i debian/patches/10_livelock.dpatch
patch -F 0 -i debian/patches/12_osdbase-maxitems.patch
%patch2 -p1
%patch3 -p1
sed \
    -e 's|__CACHEDIR__|%{cachedir}|'   \
    -e 's|__CONFIGDIR__|%{configdir}|' \
    -e 's|__PLUGINDIR__|%{plugindir}|' \
    -e 's|__VARDIR__|%{vardir}|'       \
    -e 's|__VIDEODIR__|%{videodir}|'   \
    %{PATCH4} | %{__patch} -p1
%patch5 -p1 -F 2
# TODO: does not apply
#patch6 -p0
%patch7 -p1
#TODO: patch8 -p1
#TODO: patch9 -p1 -F 2
%patch10 -p1
%patch11 -p1
%patch12 -p1
# TODO: does not apply
#patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
# TODO: build failure
#patch17 -p0 -F 3
%patch18 -p1

for f in CONTRIBUTORS HISTORY UPDATE-1.4.0 README.timer-info \
    PLUGINS/src/dvbhddevice/HISTORY; do
    iconv -f iso-8859-1 -t utf-8 -o $f.utf8 $f && mv $f.utf8 $f
done

cp -p %{SOURCE5} reccmds.conf
cp -p %{SOURCE13} timercmds.conf
cp -p %{SOURCE6} commands.conf
# Unfortunately these can't have comments in them, so ship 'em empty.
cat /dev/null > channels.conf
cat /dev/null > remote.conf
cat /dev/null > setup.conf
cat /dev/null > timers.conf

install -pm 644 %{SOURCE10} README.package
install -pm 644 %{SOURCE16} CHANGES.package.old

# Would like to do "files {channels,setup,timers}.conf" from config dir
# only, but rename() in cSafeFile barks "device or resource busy", cf.
# http://lists.suse.com/archive/suse-programming-e/2003-Mar/0051.html
cat << EOF > %{name}.rwtab
dirs    %{cachedir}
files   %{configdir}
files   %{vardir}
EOF

# Disable some graphs that end up too big to be useful.
for g in COLLABORATION INCLUDE INCLUDED_BY ; do
    sed -i -e 's/^\(\s*'$g'_GRAPH\s*=\s*\).*/\1NO/' Doxyfile
done


%build

cat << EOF > Make.config
CC           = %{__cc}
CXX          = %{__cxx}

CFLAGS       = \$(shell pkg-config vdr --variable=cflags)
CXXFLAGS     = \$(shell pkg-config vdr --variable=cxxflags)
LDFLAGS      = $RPM_LD_FLAGS

PREFIX       = %{_prefix}
MANDIR       = \$(shell pkg-config vdr --variable=mandir)
BINDIR       = \$(shell pkg-config vdr --variable=bindir)

LOCDIR       = \$(shell pkg-config vdr --variable=locdir)
PLUGINLIBDIR = \$(shell pkg-config vdr --variable=libdir)
VIDEODIR     = \$(shell pkg-config vdr --variable=videodir)
CONFDIR      = \$(shell pkg-config vdr --variable=configdir)
CACHEDIR     = \$(shell pkg-config vdr --variable=cachedir)
RESDIR       = \$(shell pkg-config vdr --variable=resdir)
INCDIR       = %{_includedir}
LIBDIR       = \$(PLUGINLIBDIR)

PLGCFG       = \$(LIBDIR)/plugins.mk
LIRC_DEVICE  = %{_localstatedir}/run/lirc/lircd
VDR_USER     = \$(shell pkg-config vdr --variable=user)
EOF

cat << EOF > plugins.mk
LDFLAGS = $RPM_LD_FLAGS
EOF

cp plugins.mk bundled-plugins.mk
cat << EOF >> bundled-plugins.mk
CFLAGS += -I$PWD/include
CXXFLAGS += -I$PWD/include
EOF

cflags="${RPM_OPT_FLAGS/-O2/-O3} -fPIC" # see HISTORY for 1.7.17 for -O3

make vdr.pc BINDIR=%{_bindir} MANDIR=%{_mandir} CONFDIR=%{configdir} \
    VIDEODIR=%{videodir} CACHEDIR=%{cachedir} RESDIR=%{_datadir}/vdr \
    LIBDIR=%{plugindir} LOCDIR=%{_datadir}/locale RUNDIR=%{rundir} \
    VARDIR=%{vardir} VDR_USER=%{vdr_user} VDR_GROUP=%{vdr_group} \
    LDFLAGS="$RPM_LD_FLAGS" CFLAGS="$cflags" \
    CXXFLAGS="$cflags -Werror=overloaded-virtual -Wno-parentheses"

PKG_CONFIG_PATH="$PWD:$PKG_CONFIG_PATH" \
make %{?_smp_mflags} vdr include-dir i18n

for plugin in dvbhddevice dvbsddevice rcu skincurses ; do
    make %{?_smp_mflags} -C PLUGINS/src/$plugin VDRDIR=$PWD \
        PLGCFG=$PWD/bundled-plugins.mk all
done

%if %{with docs}
make %{?_smp_mflags} srcdoc
%endif # docs


%install

# Not using the install-pc target to preserve our already good vdr.pc
install -Dpm 644 vdr.pc $RPM_BUILD_ROOT%{_libdir}/pkgconfig/vdr.pc

PKG_CONFIG_PATH="$RPM_BUILD_ROOT%{_libdir}/pkgconfig:$PKG_CONFIG_PATH" \
make install-bin install-dirs install-conf install-doc install-i18n \
    install-includes DESTDIR=$RPM_BUILD_ROOT

install -pm 755 epg2html $RPM_BUILD_ROOT%{_bindir}
install -dm 755 $RPM_BUILD_ROOT%{_sbindir}
mv $RPM_BUILD_ROOT%{_bindir}/vdr $RPM_BUILD_ROOT%{_sbindir}

install -dm 755 $RPM_BUILD_ROOT%{configdir}/plugins

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d

install -dm 755 $RPM_BUILD_ROOT%{vardir}/themes
touch $RPM_BUILD_ROOT%{vardir}/themes/{classic,sttng}-default.theme

install -pm 755 %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/runvdr
sed -i \
    -e 's|/usr/sbin/|%{_sbindir}/|'                    \
    -e 's|/etc/sysconfig/|%{_sysconfdir}/sysconfig/|g' \
    -e 's|/usr/lib/vdr\b|%{plugindir}|'                \
    -e 's|VDR_PLUGIN_VERSION|%{apiver}|'               \
    $RPM_BUILD_ROOT%{_sbindir}/runvdr

install -Dm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr
sed -i \
    -e 's|/usr/lib/vdr/|%{plugindir}/|' \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr

touch $RPM_BUILD_ROOT%{videodir}/.update

install -dm 755 $RPM_BUILD_ROOT%{plugindir}/bin

install -m 755 %{SOURCE14} $RPM_BUILD_ROOT%{plugindir}/bin/%{name}-shutdown.sh
sed -i \
    -e 's|/etc/sysconfig/|%{_sysconfdir}/sysconfig/|' \
    -e 's|/var/run/vdr/|%{rundir}/|'                  \
    $RPM_BUILD_ROOT%{plugindir}/bin/%{name}-shutdown.sh

install -m 755 %{SOURCE15} $RPM_BUILD_ROOT%{plugindir}/bin/%{name}-moveto.sh
sed -i \
    -e 's|/var/lib/vdr/video|%{videodir}|' \
    -e 's|/etc/vdr/|%{configdir}/|'        \
    $RPM_BUILD_ROOT%{plugindir}/bin/%{name}-moveto.sh

install -m 755 %{SOURCE19} $RPM_BUILD_ROOT%{plugindir}/bin/%{name}-check-setup
sed -i \
    -e 's|/etc/vdr/|%{configdir}/|' \
    -e 's|VDR_USER|%{vdr_user}|'    \
    -e 's|VDR_GROUP|%{vdr_group}|'  \
    $RPM_BUILD_ROOT%{plugindir}/bin/%{name}-check-setup

install -m 755 %{SOURCE21} $RPM_BUILD_ROOT%{plugindir}/bin/%{name}-set-wakeup
sed -i \
    -e 's|/usr/sbin/|%{_sbindir}/|'  \
    -e 's|/var/run/vdr/|%{rundir}/|' \
    $RPM_BUILD_ROOT%{plugindir}/bin/%{name}-set-wakeup

install -Dm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service
sed -i \
    -e 's|/usr/lib/vdr/|%{plugindir}/|'        \
    -e 's|/usr/sbin/|%{_sbindir}/|'            \
    -e 's|/usr/share/doc/vdr/|%{_pkgdocdir}/|' \
    $RPM_BUILD_ROOT%{_unitdir}/%{name}.service

install -Dpm 440 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.d/vdr

touch $RPM_BUILD_ROOT%{cachedir}/epg.data
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/vdr/{logos,plugins}
install -dm 755 $RPM_BUILD_ROOT%{rundir}
touch $RPM_BUILD_ROOT%{rundir}/next-timer
install -dm 755 $RPM_BUILD_ROOT%{vardir}

install -Dm 644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/51-%{name}.rules
sed -i \
    -e 's/VDR_GROUP/%{vdr_group}/' \
    $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/*-%{name}.rules

install -Dpm 644 %{name}.rwtab $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/%{name}

install -dm 755 $RPM_BUILD_ROOT%{_pkgdocdir}
install -pm 644 CHANGES.package.old CONTRIBUTORS COPYING HISTORY* INSTALL \
    MANUAL PLUGINS.html README* UPDATE-?.?.0 $RPM_BUILD_ROOT%{_pkgdocdir}
%if %{with docs}
cp -pR srcdoc/html $RPM_BUILD_ROOT%{_pkgdocdir}
%endif

# devel

abs2rel() { perl -MFile::Spec -e 'print File::Spec->abs2rel(@ARGV)' "$@" ; }

install -pm 755 %{SOURCE9} $RPM_BUILD_ROOT%{_bindir}/vdr-config
install -pm 755 newplugin $RPM_BUILD_ROOT%{_bindir}/vdr-newplugin
install -pm 644 Make.{config,global} plugins.mk $RPM_BUILD_ROOT%{_libdir}/vdr
ln -s $(abs2rel %{_includedir}/vdr/config.h %{_libdir}/vdr) \
    $RPM_BUILD_ROOT%{_libdir}/vdr
macrodir=%{_sysconfdir}/rpm
[ -d %{_rpmconfigdir}/macros.d ] && macrodir=%{_rpmconfigdir}/macros.d
install -Dpm 644 %{SOURCE17} $RPM_BUILD_ROOT$macrodir/macros.vdr
echo $macrodir/macros.vdr > %{name}-devel.files

# i18n

%find_lang %{name}
sed -i -e '1i%%defattr(-,root,root,-)' %{name}.lang

install -dm 755 $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d
echo "d %{rundir} 0755 %{vdr_user} root -" \
    > $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/%{name}.conf
echo "%{_prefix}/lib/tmpfiles.d/%{name}.conf" \
    >> %{name}.lang

# plugins

%make_install -C PLUGINS/src/dvbhddevice
install -pm 644 %{SOURCE12} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/dvbhddevice.conf
%find_lang %{name}-dvbhddevice

%make_install -C PLUGINS/src/dvbsddevice
install -pm 644 %{SOURCE8} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/dvbsddevice.conf

%make_install -C PLUGINS/src/rcu
install -pm 644 %{SOURCE20} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/rcu.conf

%make_install -C PLUGINS/src/skincurses
install -pm 644 %{SOURCE11} \
    $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/vdr-plugins.d/skincurses.conf
%find_lang %{name}-skincurses


%check
export PKG_CONFIG_PATH=$RPM_BUILD_ROOT%{_libdir}/pkgconfig
if [ "$(pkg-config vdr --variable=apiversion)" != "%{apiver}" ] ; then
    echo "ERROR: API version mismatch in vdr.pc / package / config.h" ; exit 1
fi


%pre
getent passwd %{vdr_user} >/dev/null || \
useradd -r -g %{vdr_group} -d %{vardir} -s /sbin/nologin -M -N \
    -G audio,cdrom,dialout -c "Video Disk Recorder" %{vdr_user} || :

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files -f %{name}.lang
%{_pkgdocdir}
%exclude %{_pkgdocdir}/PLUGINS.html
%if %{with docs}
%exclude %{_pkgdocdir}/html/
%endif
%config(noreplace) %{_sysconfdir}/sudoers.d/vdr
%config(noreplace) %{_sysconfdir}/sysconfig/vdr
%config(noreplace) %{_sysconfdir}/udev/rules.d/*-%{name}.rules
%config(noreplace) %{_sysconfdir}/rwtab.d/%{name}
%config %dir %{_sysconfdir}/sysconfig/vdr-plugins.d/
%{_bindir}/epg2html
%{_bindir}/svdrpsend
%{_sbindir}/runvdr
%{_sbindir}/vdr
%{_unitdir}/%{name}.service
%dir %{plugindir}/
%dir %{plugindir}/bin/
%{plugindir}/bin/%{name}-check-setup
%{plugindir}/bin/%{name}-moveto.sh
%{plugindir}/bin/%{name}-set-wakeup
%{plugindir}/bin/%{name}-shutdown.sh
%{_datadir}/vdr/
%{_mandir}/man1/svdrpsend.1*
%{_mandir}/man1/vdr.1*
%{_mandir}/man5/vdr.5*
%dir %{varbase}/
%defattr(-,%{vdr_user},%{vdr_group},-)
# TODO: tighten ownerships to root:root for some files in %%{configdir}
%config(noreplace) %{configdir}/*.conf
%dir %{videodir}/
%ghost %{videodir}/.update
%ghost %{vardir}/themes/*.theme
%ghost %{cachedir}/epg.data
%defattr(-,%{vdr_user},root,-)
%dir %{configdir}/
%dir %{configdir}/plugins/
%dir %{rundir}/
%ghost %{rundir}/next-timer
%dir %{vardir}/
%dir %{vardir}/themes/
%dir %{cachedir}/

%files devel -f %{name}-devel.files
%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING
%if ! %{with docs}
%{_pkgdocdir}/PLUGINS.html
%endif # docs
%{_bindir}/vdr-config
%{_bindir}/vdr-newplugin
%{_includedir}/libsi/
%{_includedir}/vdr/
%{_libdir}/pkgconfig/vdr.pc
%dir %{_libdir}/vdr/
%{_libdir}/vdr/Make.config
%{_libdir}/vdr/Make.global
%{_libdir}/vdr/config.h
%{_libdir}/vdr/plugins.mk

%if %{with docs}
%files docs
%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING
%{_pkgdocdir}/PLUGINS.html
%{_pkgdocdir}/html/
%endif

%files dvbhddevice -f %{name}-dvbhddevice.lang
%doc PLUGINS/src/dvbhddevice/COPYING PLUGINS/src/dvbhddevice/HISTORY
%doc PLUGINS/src/dvbhddevice/README
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/dvbhddevice.conf
%{plugindir}/libvdr-dvbhddevice.so.%{apiver}

%files dvbsddevice
%doc PLUGINS/src/dvbsddevice/COPYING PLUGINS/src/dvbsddevice/HISTORY
%doc PLUGINS/src/dvbsddevice/README
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/dvbsddevice.conf
%{plugindir}/libvdr-dvbsddevice.so.%{apiver}

%files rcu
%doc PLUGINS/src/rcu/COPYING PLUGINS/src/rcu/HISTORY PLUGINS/src/rcu/README
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/rcu.conf
%{plugindir}/libvdr-rcu.so.%{apiver}

%files skincurses -f %{name}-skincurses.lang
%doc PLUGINS/src/skincurses/COPYING PLUGINS/src/skincurses/HISTORY
%doc PLUGINS/src/skincurses/README
%config(noreplace) %{_sysconfdir}/sysconfig/vdr-plugins.d/skincurses.conf
%{plugindir}/libvdr-skincurses.so.%{apiver}


%changelog
* Tue Jan  7 2014 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.5-1
- Update to 2.0.5, starting after lirc.service is no longer needed.
- Remove restart logic from runvdr, handle it with systemd instead.
- Drop DVB reloading logic due to the above change.
- Use stdout/err for script log messages and let systemd route them.
- Get locale settings from /etc/locale.conf, not /etc/sysconfig/i18n.
- Use systemd macros in scriptlets (#850358).

* Wed Dec 11 2013 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.4-2
- Use main package's doc dir in -devel and -docs.
- Use upstream copy of NALU dump patch.

* Wed Oct 23 2013 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.4-1
- Update to 2.0.4.

* Mon Sep  2 2013 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.3-1
- Update to 2.0.3.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2.0.2-4
- Perl 5.18 rebuild

* Fri Jul 26 2013 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.2-3
- Honor %%{_pkgdocdir} where available.

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.0.2-2
- Perl 5.18 rebuild

* Mon May 20 2013 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.2-1
- Update to 2.0.2.

* Sat Apr 13 2013 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.1-1
- Update to 2.0.1.

* Sun Apr  7 2013 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.0-2
- Update vasarajanauloja patch to 2.0.0.
- Apply upstream cDevice::keepTracks init patch.

* Sun Mar 31 2013 Ville Skytt?? <ville.skytta@iki.fi> - 2.0.0-1
- Update to 2.0.0.
- Move pre-1.7 changelog entries to CHANGES.package.old.

* Sat Mar 23 2013 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.42-2
- Fix API version.

* Sat Mar 23 2013 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.42-1
- Update to 1.7.42.

* Sat Mar 16 2013 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.41-1
- Update to 1.7.41.
- Move macros.vdr to %%{_rpmconfigdir}/macros.d where applicable.

* Wed Mar 13 2013 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.40-1
- Update to 1.7.40.

* Sun Mar  3 2013 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.39-2
- Move tmpfiles.d snippet to %%{_prefix}/lib/tmpfiles.d, make it more friendly
  to plugin specific subdirs.

* Sun Mar  3 2013 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.39-1
- Update to 1.7.39.
- Apply Udo Richter's NALU dump patch.

* Mon Feb 18 2013 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.38-1
- Update to 1.7.38; hard link cutter and jumpplay are temporarily not included,
  and some variables in *.pc and macros have changed.
- Drop no longer needed sysv-to-systemd migration scriptlets.
- Drop After=syslog.target from systemd unit file.
- Drop deprecated %%{_isa}-less vdr(abi) provision.
- Misc specfile cleanups.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 1.7.31-4
- rebuild due to "jpeg8-ABI" feature drop

* Sat Dec 22 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.31-3
- Fix build with DVB API 5.8 (upstream).
- Do not mark recordings as new when removing marks at EOF (Rolf Ahrenberg).
- Require font(:lang=en) [#863720].

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.7.31-2
- rebuild against new libjpeg

* Tue Oct  2 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.31-1
- Update to 1.7.31.

* Thu Sep 13 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.30-1
- Update to 1.7.30.
- Add Documentation entries to systemd service.

* Wed Jul 18 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.29-1
- Update to 1.7.29.

* Wed Jun 27 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.28-1
- Update to 1.7.28.
- Add softhdddevice to sysconfig's VDR_PLUGIN_ORDER.

* Mon Apr 23 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.27-2
- Build with hardening flags on.
- Update hlcutter patch to 0.2.3.
- Patch to build libhdffcmd with our CFLAGS.
- Sync CXXFLAGS in Make.config with upstream.

* Mon Mar 26 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.27-1
- Update to 1.7.27, re-enable legacy receiver code for now.

* Sun Mar 18 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.26-2
- Apply Rolf Ahrenberg's subtitles fix.

* Sun Mar 11 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.26-1
- Update to 1.7.26.

* Tue Mar  6 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.25-1
- Update to 1.7.25; RCU functionality split into -rcu plugin subpackage.

* Tue Feb 21 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.24-3
- Apply upstream dvbplayer 50fps reload patch.

* Tue Feb 21 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.24-2
- Revert only problematic dvbplayer changes to 1.7.23, thanks to Udo Richter.

* Mon Feb 20 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.24-1
- Update to 1.7.24 sans dvbplayer changes that broke some output plugins.

* Sun Jan 15 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.23-1
- Update to 1.7.23.
- Migrate to systemd.
- runvdr cleanups.

* Wed Jan  4 2012 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.22-2
- Fix build with g++ 4.7.0.
- Turn on teletext subtitles by default for 1.6.x backwards compat.

* Sun Dec  4 2011 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.22-1
- Update to 1.7.22.
- Build docs by default.

* Thu Nov 17 2011 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.21-2
- Update liemikuutio patch to 1.33.

* Sun Nov  6 2011 Ville Skytt?? <ville.skytta@iki.fi> - 1.7.21-1
- Update to 1.7.21.
- Clean up specfile constructs no longer needed with Fedora or EL6+.
