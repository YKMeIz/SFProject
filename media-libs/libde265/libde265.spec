Name:		libde265
Summary:	Open H.265 video codec implementation
Version:	0.8
Release:	1%{?dist}
License:	LGPLv3+
Group:		System Environment/Libraries
Source:		https://github.com/strukturag/libde265/releases/download/v%{version}/%{name}-%{version}.tar.gz
URL:		https://github.com/strukturag/libde265
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libswscale)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(QtGui)
BuildRequires:	pkgconfig(sdl)


%description
libde265 is an open source implementation of the H.265 video codec.
It is written from scratch for simplicity and efficiency. Its simple
API makes it easy to integrate it into other software.


%package devel
Group:		Development/Libraries
Summary:	Open H.265 video codec implementation - development files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
libde265 is an open source implementation of the H.265 video codec.
It is written from scratch for simplicity and efficiency. Its simple
API makes it easy to integrate it into other software.

The development headers for compiling programs that use libde265
are provided by this package.


%package examples
License:	GPLv3+
Group:		Applications/Multimedia
Summary:	Open H.265 video codec implementation - examples
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description examples
libde265 is an open source implementation of the H.265 video codec.
It is written from scratch for simplicity and efficiency. Its simple
API makes it easy to integrate it into other software.

Sample applications using libde265 are provided by this package.


%prep
%autosetup

%build
%configure --disable-silent-rules --disable-static --enable-shared
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name '*.a' -exec rm -f {} \;
find %{buildroot} -type f -name '*.la' -exec rm -f {} \;
mv %{buildroot}%{_bindir}/dec265 %{buildroot}%{_bindir}/libde265-dec265
mv %{buildroot}%{_bindir}/sherlock265 %{buildroot}%{_bindir}/libde265-sherlock265

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING
%{_libdir}/*.so.*

%files devel
%doc README.md
%{_includedir}/libde265/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files examples
%doc README.md
%{_bindir}/libde265-dec265
%{_bindir}/libde265-sherlock265

%changelog
* Thu Aug 14 2014 Joachim Bauch <bauch@struktur.de> 0.8-1
- Initial version.
