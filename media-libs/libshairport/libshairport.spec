%global checkout 20121218git16395d8
Name:           libshairport
Version:        1.2.1
Release:        3.%{checkout}%{?dist}
Summary:        Emulates an AirPort Express
Group:          System Environment/Libraries

License:        MIT
URL:            https://github.com/amejia1/libshairport
Source0:        %{name}-%{version}.%{checkout}.tar.gz
# The source for this package was pulled from upstream's vcs.  Invoke the
# following script while in your SOURCES directory to generate the tarball:
#  sh libshairport-generate-tarball-gz.sh
Source1:        libshairport-generate-tarball-gz.sh
# This patch remove unnecessary libssl link, it has been proposed to upstream (https://github.com/amejia1/libshairport/pull/3)
Patch0:         libshairport-remove-libssl-link.patch

BuildRequires:  libao-devel
BuildRequires:  openssl-devel
BuildRequires:  autoconf automake libtool

%description
This program emulates an AirPort Express for the purpose of
streaming music from iTunes and compatible iPods. It implements
a server for the Apple RAOP protocol. ShairPort does not support
AirPlay v2 (video and photo streaming). It supports multiple
simultaneous streams, if your audio output chain
(as detected by libao) does so.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libao-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}.%{checkout}
%patch0


%build
autoreconf -vif
%configure --disable-static
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc LICENSE README
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libshairport.pc


%changelog
* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.2.1-3.20121218git16395d8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Dec 30 2012 Lorenzo Dalrio <lorenzo.dalrio@gmail.com> - 1.2.1-2.20121218git16395d8
- Modified specfile to meet review requirements

* Tue Dec 18 2012 Lorenzo Dalrio <lorenzo.dalrio@gmail.com> - 1.2.1-1.20121218git16395d8
- Initial release

