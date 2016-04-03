%global commit 498bc5bcdd305e04721f94a04b9f26a7da72673f
%global short_commit %(c=%{commit}; echo ${c:0:7})
%global commit_date 20150921

%global _hardened_build 1

Name:           shairplay
Version:        0.9.0
Release:        3.%{commit_date}git%{short_commit}%{?dist}
Summary:        Apple AirPlay and RAOP protocol server

Group:          Applications/Multimedia
License:        MIT and BSD and LGPLv2+
URL:            https://github.com/juhovh/shairplay/
Source0:        https://github.com/juhovh/%{name}/archive/%{short_commit}/%{name}-%{short_commit}.tar.gz
# Shairplay service file, taken from Arch Linux (see
# https://projects.archlinux.org/svntogit/community.git/tree/trunk/shairplay.service?h=packages/shairplay)
Source1:        %{name}.service
Source2:        airtv.desktop
Source3:        airtv.appdata.xml
# Fix dns_sd library load
Patch0:         %{name}-0.9.0-dns_sd.patch
# Load airport.key from /etc/ instead of the current directory
Patch1:         %{name}-0.9.0-key_path.patch
# Fix AirTV build
Patch2:         %{name}-0.9.0-AirTV_build.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  libtool
BuildRequires:  phonon-devel
BuildRequires:  pkgconfig(ao)
BuildRequires:  qt4-devel
BuildRequires:  systemd
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       avahi%{?_isa}
Requires:       avahi-compat-libdns_sd%{?_isa}
Requires(pre):  shadow-utils
Requires(post): systemd
Requires(preun):systemd
Requires(postun):systemd

%description
Free portable AirPlay server implementation similar to ShairPort. Currently only
AirPort Express emulation is supported.


%package libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description libs
The %{name}-libs package contains the runtime shared libraries for %{name}.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       libao-devel%{?_isa}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.


%package -n airtv
Summary:        Qt GUI to start a RAOP server
Group:          Applications/Multimedia
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       avahi-compat-libdns_sd%{?_isa}

%description -n airtv
AirTV Qt is a GUI to start a RAOP server. Once started, AirTV will add an icon
to the system tray using which you can stop the server.


%prep
%setup -q -n %{name}-%{commit}
%patch0 -p0 -b .dns_sd
%patch1 -p0 -b .key_path
%patch2 -p0 -b .AirTV_build


%build
[ -f configure ] || ./autogen.sh
%configure \
    --disable-static
# Remove Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

# Build AirTV
cd AirTV-Qt/
%{_qt4_qmake}
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name "*.la" -delete

install -Dpm 0644 airport.key $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/airport.key

install -Dpm 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/%{name}.service

# Install AirTV
pushd AirTV-Qt/
install -Dpm 0755 AirTV $RPM_BUILD_ROOT%{_bindir}/AirTV
desktop-file-install \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications/ \
    %{SOURCE2}
install -Dpm 0644 images/airtv.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/airtv.svg
install -Dpm 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/appdata/airtv.appdata.xml


%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/airtv.desktop
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/appdata/airtv.appdata.xml


%post
%systemd_post %{name}.service

%post libs -p /sbin/ldconfig

%post -n airtv
/bin/touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null || :


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service

%postun libs -p /sbin/ldconfig

%postun -n airtv
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor/ &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :
fi


%posttrans -n airtv
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :


%files
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/airport.key


%files libs
%license LICENSE
%{_libdir}/*.so.*


%files devel
%{_includedir}/*
%{_libdir}/*.so


%files -n airtv
%{_bindir}/AirTV
%{_datadir}/applications/airtv.desktop
%{_datadir}/icons/hicolor/*/apps/airtv.*
%{_datadir}/appdata/airtv.appdata.xml


%changelog
* Wed Sep 30 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.9.0-3.20150921git498bc5b
- Update to latest snapshot
- Add missing runtime dependency on Avahi
- Add AppData file for AirTV

* Mon Aug 17 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.9.0-2.20150508git0f41ade
- Enable shairplay server build
- Enable AirTV GUI build

* Wed Jul 15 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.9.0-1.20150508git0f41ade
- Initial RPM release
