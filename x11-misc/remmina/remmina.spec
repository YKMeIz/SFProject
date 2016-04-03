# Review at https://bugzilla.redhat.com/show_bug.cgi?id=553402

Name:           remmina
Version:        1.0.0
Release:        8%{?dist}
Summary:        Remote Desktop Client

Group:          Applications/Internet
License:        GPLv2+ and MIT
URL:            http://remmina.sourceforge.net
Source0:        https://github.com/downloads/FreeRDP/Remmina/Remmina-%{version}.tar.gz
#VCS: git:https://github.com/FreeRDP/Remmina.git

# The following two patches will fix some linking errors
# https://github.com/FreeRDP/Remmina/commit/503a008e
Patch0:         remmina-1.0.0-fix-library-name.patch
# https://github.com/FreeRDP/Remmina/commit/13f20367
Patch1:         remmina-1.0.0-linker-error.patch

# The following 4 patches are needed to add clipboard support (#818155)
# https://github.com/FreeRDP/Remmina/commit/3ebdd6e7
Patch2:         remmina-1.0.0-add-clipboard-support.patch
# https://github.com/FreeRDP/Remmina/commit/97c2af8c
Patch3:         remmina-1.0.0-clipboard-bugfix.patch
# https://github.com/FreeRDP/Remmina/commit/84327f81
Patch4:         remmina-1.0.0-some-more-clipboard-fixes.patch
# https://github.com/FreeRDP/Remmina/commit/c1ef3a16
Patch5:         remmina-1.0.0-disconnect-signal-handler-after-disconnect.patch

# https://github.com/FreeRDP/Remmina/commit/6ee20289
Patch10:        remmina-1.0.0-fix-crashes-in-some-cases.patch
# https://github.com/FreeRDP/Remmina/commit/b2277827
Patch11:        remmina-1.0.0-fix-memory-leak.patch

# Fedora bug:   https://bugzilla.redhat.com/show_bug.cgi?id=953678
# upstream bug: https://github.com/FreeRDP/Remmina/issues/63
# upstream fix: https://github.com/FreeRDP/Remmina/commit/1901a1e9
Patch12:        remmina-1.0.0-fix-typo-when-fitting-window.patch

# Fedora bug:   https://bugzilla.redhat.com/show_bug.cgi?id=834883
# upstream bug: https://github.com/FreeRDP/Remmina/issues/76
# upstream fix: https://github.com/FreeRDP/Remmina/commit/1901a1e9
Patch13:        remmina-1.0.0-trayicon-patch

# Fedora bug:   https://bugzilla.redhat.com/show_bug.cgi?id=830210
# upstream fix: https://github.com/FreeRDP/Remmina/commit/
Patch14:        remmina-1.0.0-fix-scrolling-in-vnc-plugin.patch
# upstream fix: https://github.com/FreeRDP/Remmina/commit/fe1b698e
Patch15:        remmina-1.0.0-Also-handle-GDK_SCROLL_SMOOTH.patch

# upstream bug: https://github.com/FreeRDP/Remmina/issues/77
# upstream fix: https://github.com/FreeRDP/Remmina/commit/bed49ad6
Patch16:        remmina-1.0.0-close-SSH-tunnel-on-disconnect.patch

# Fedora bug:   https://bugzilla.redhat.com/show_bug.cgi?id=864262
# upstream fix: https://github.com/FreeRDP/Remmina/commit/348e01d2
Patch17:        remmina-1.0.0-fix-fullscreen-with-multiple-monitors.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=819976
Patch30:        remmina-1.0.0-dsofix.patch

# From OpenSUSE. All patches are backport from upstream.
# Thanks to Guido Berhoerster <gber at opensuse dot org>
Patch31:        remmina-1.0.0-fix-desktop-file.patch
Patch32:        remmina-1.0.0-fix-install-paths.patch

# From Debian. Thanks to Luca Falavigna <dktrkranz at debian dot org>
Patch35:        remmina-1.0.0-remove-inline-libvncserver.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk3-devel
BuildRequires:  libssh-devel >= 0.4.
BuildRequires:  libgcrypt-devel
BuildRequires:  avahi-ui-devel
BuildRequires:  vte3-devel
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  libxkbfile-devel

BuildRequires:  gnutls-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libvncserver-devel

# We don't ship the remmina-plugins-common package any longer
Provides:       remmina-plugins-common = %{version}
Obsoletes:      remmina-plugins-common < 1.0.0-7

# Remmina used to be called grdc
Provides:       grdc = %{version}
Obsoletes:      grdc < 0.6.1

# Remmina has a generic trayicon now
Provides:       gnome-applet-remmina = %{version}
Provides:       xfce4-remmina-plugin = %{version}
Obsoletes:      gnome-applet-remmina <= 0.7.3
Obsoletes:      xfce4-remmina-plugin <= 0.7.3


%description
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

Remmina supports multiple network protocols in an integrated and consistent
user interface. Currently RDP, VNC, XDMCP and SSH are supported.

Please don't forget to install the plugins for the protocols you want to use.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains header files for developing plugins for 
%{name}.


%package        plugins-gnome
Summary:        GNOME keyring integration for Remmina Remote Desktop Client
BuildRequires:  libgnome-keyring-devel
Group:          Applications/System
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libgnome-keyring

%description    plugins-gnome
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the plugin with GNOME keyring support for the Remmina
remote desktop client.


%package        plugins-nx
Summary:        NX plugin for Remmina Remote Desktop Client
Group:          Applications/System
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       nx

%description    plugins-nx
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the NX plugin for the Remmina remote desktop client.


%package        plugins-rdp
Summary:        RDP plugin for Remmina Remote Desktop Client
Group:          Applications/System
BuildRequires:  freerdp-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       freerdp

%description    plugins-rdp
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the Remote Desktop Protocol (RDP) plugin for the Remmina
remote desktop client.


%package        plugins-telepathy
Summary:        Telepathy plugin for Remmina Remote Desktop Client
Group:          Applications/System
BuildRequires:  telepathy-glib-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    plugins-telepathy
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the Telepathy plugin for the Remmina remote desktop 
client.


%package        plugins-vnc
Summary:        VNC plugin for Remmina Remote Desktop Client
Group:          Applications/System
BuildRequires:  gnutls-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libvncserver-devel
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    plugins-vnc
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the VNC plugin for the Remmina remote desktop 
client.


%package        plugins-xdmcp
Summary:        XDMCP plugin for Remmina Remote Desktop Client
Group:          Applications/System
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       xorg-x11-server-Xephyr

%description    plugins-xdmcp
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the XDMCP plugin for the Remmina remote desktop 
client.


%prep
%setup -qn FreeRDP-Remmina-356c033

%patch0 -p1 -b .fix-library-name
%patch1 -p1 -b .linker-error

%patch2 -p1 -b .add-clipboard-support
%patch3 -p1 -b .clipboard-bugfix
%patch4 -p1 -b .some-more-clipboard-fixes
%patch5 -p1 -b .disconnect-signal-handler

%patch10 -p1 -b .fix-crashes-in-some-cases
%patch11 -p1 -b .fix-memory-leak

%patch12 -p1 -b .fitting-window

%patch13 -p1 -b .trayicon

%patch14 -p1 -b .vnc-scrolling

%patch15 -p1 -b .GDK_SCROLL_SMOOTH

%patch16 -p1 -b .ssh-disconnect

%patch17 -p1 -b .multiple-monitors

%patch30 -p0 -b .dsofix
%patch31 -p1 -b .desktop-file
%patch32 -p1 -b .install-paths


%patch35 -p1 -b .libvncserver


%build
mkdir -p build
pushd build

CFLAGS="%{optflags} -DLIBVNCSERVER_WITH_CLIENT_TLS=1"
LDFLAGS="-Wl,-z,relro -Wl,--no-as-needed"

%cmake \
    -DWITH_PTHREAD=ON \
    -DWITH_GCRYPT=ON \
    -DWITH_LIBSSH=ON \
    -DWITH_VTE=ON \
    -DWITH_GETTEXT=ON \
    -DWITH_LIBSSH=ON \
    -DWITH_FREERDP=ON \
    -DWITH_TELEPATHY=ON \
    -DWITH_ZLIB=ON \
    -DWITH_GETTEXT=ON \
    -DWITH_AVAHI=ON \
    -DWITH_APPINDICATOR=OFF \
    -LIBVNCSERVER_INCLUDE_DIRS=%{_includedir} \
    -DLIBVNCSERVER_WITH_CLIENT_TLS=1 \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    ..

make %{?_smp_mflags}
popd

%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C build

desktop-file-install --vendor="" --delete-original \
    --add-category="RemoteAccess" \
    --remove-category="X-GNOME-NetworkSettings" \
    --remove-key="Actions" \
    --dir %{buildroot}%{_datadir}/applications \
    %{buildroot}/%{_datadir}/applications/%{name}.desktop

%find_lang %{name}
%find_lang %{name}-plugins


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-nx
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-rdp
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-vnc
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%post plugins-xdmcp
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-nx
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-rdp
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-vnc
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun plugins-xdmcp
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-nx
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-rdp
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-vnc
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%posttrans plugins-xdmcp
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang -f %{name}-plugins.lang
%defattr(-,root,root,-)
# FIXME: Add NEWS if not empty
%doc remmina/AUTHORS remmina/ChangeLog remmina/COPYING README 
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.*
%dir %{_libdir}/remmina/
%dir %{_libdir}/remmina/plugins/

%files devel
%defattr(-,root,root,-)
%doc
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc

%files plugins-gnome
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugins-gnome.so

%files plugins-nx
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-nx.so
%{_datadir}/icons/hicolor/*/emblems/remmina-nx.png

%files plugins-rdp
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-rdp.so
%{_datadir}/icons/hicolor/*/emblems/remmina-rdp-ssh.png
%{_datadir}/icons/hicolor/*/emblems/remmina-rdp.png

%files plugins-telepathy
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-telepathy.so
#%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Remmina.service
#%{_datadir}/telepathy/clients/Remmina.client

%files plugins-vnc
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-vnc.so
%{_datadir}/icons/hicolor/*/emblems/remmina-vnc-ssh.png
%{_datadir}/icons/hicolor/*/emblems/remmina-vnc.png

%files plugins-xdmcp
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-xdmcp.so
%{_datadir}/icons/hicolor/*/emblems/remmina-xdmcp-ssh.png
%{_datadir}/icons/hicolor/*/emblems/remmina-xdmcp.png


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-7
- Fix scrolling in VNC (#830210)
- Handle GDK_SCROLL_SMOOTH in VNC and RDP
- Bring back the --icon/-i autostart option (#834883)
- Fix fullscreen with multiple monitors (#864262)
- Resize window to fit remote resolution (#953678)
- Enable TLS-support in VNC plugin
- Close SSH tunnels on disconnect (https://github.com/FreeRDP/Remmina/issues/77)
- Patch out copy of libvncserver shipped in source tarball
- Update icon cache also for plugins
- Drop the remmina-plugins-common package
- Drop Provides/Obsoletes for grdc
- Spec file clean-up

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-4
- Fix DSO linking against gnutls (#819976)

* Sun Jun 03 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-3
- Fix crash introduced by clipboard support (#827756)

* Fri Jun 01 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-2
- Add clipboard support (#818155)
- Fix a memory leak and a crash

* Sun Apr 22 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0
- Plugins are now part of this package (again)
- Fix two linker errors
- Add VCS key

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.9.3-4
- Rebuild for new libpng

* Sat Mar 05 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.3-3
- Fix obsoletes for for gnome-applet-remmina and xfce4-remmina-plugin

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.3-1
- Update to 0.9.3

* Sun Nov 28 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.3-1
- Update to 0.8.3
- Plugins are in remmina-plugins now

* Sat Nov 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.7.5-3
- Enable 32-bit color depth (#656120)

* Mon Jul 19 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.7.5-2
- Fix menu entry (#616115)

* Wed May 05 2010 Damien Durand <splinux@fedoraproject.org> - 0.7.5-1
- Upstream release, 0.7.5
- Remove the old "DSO" patch

* Tue Mar 16 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.7.4-2
- Add patch to fix DSO issue

* Sat Feb 27 2010 Damien Durand <splinux@fedoraproject.org> 0.7.4-1
- Update to 0.7.4
- Fix License tag

* Sun Feb 14 2010 Damien Durand <splinux@fedoraproject.org> 0.7.3-1
- Upstream release
- Add rdesktop, xorg-x11-server-Xephyr in Requires
- Add grdc in Provides/Obsoletes
- Add --enable-vnc=dl in %%configure
- Remove unneeded README.LibVNCServer
- Fix "icons/hicolor" path

* Thu Jan 07 2010 Damien Durand <splinux@fedoraproject.org> 0.7.2-2
- Fix Summary
- Split BuildRequires

* Thu Jan 07 2010 Damien Durand <splinux@fedoraproject.org> 0.7.2-1
- Initial release
