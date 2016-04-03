Name:		dcadec
Version:	0.2.0
Release:	1%{?dist}
Summary:	dcadec is a free DTS Coherent Acoustics decoder
License:	LGPLv2+
URL:		https://github.com/foo86/dcadec
Source0:	%{name}-%{version}.tar.gz
Group:		Sound

%description
dcadec is a free DTS Coherent Acoustics decoder with support for HD extensions


%package -n	lib%{name}
Summary:	Library files for dcadec
Group:		System/Libraries

%description -n	lib%{name}
%{summary}


%package -n	%{name}-devel
Summary:	Development files for dcadec
Group:		Development/Libraries
Requires: 	lib%{name} = %{version}-%{release}


%description -n	%{name}-devel
%{summary}


%prep
%setup -q


%build
CFLAGS=-fPIC make %{?_smp_mflags}


%install
rm -rf %buildroot
PREFIX=/usr LIBDIR=%{_libdir} CONFIG_SHARED=1 %make_install
cp -a libdcadec/libdcadec.so.0 %{buildroot}%{_libdir}/
chmod +x %{buildroot}%{_libdir}/libdcadec.so.0.1.0


%files
%{_bindir}/dcadec

%files -n lib%{name}
%{_libdir}/libdcadec.so.0
%{_libdir}/libdcadec.so.0.1.0

%files -n %{name}-devel
%{_includedir}/libdcadec
%{_libdir}/libdcadec.so
%{_libdir}/pkgconfig/dcadec.pc

%clean
rm -rf %buildroot

%changelog
* Fri Apr 1 2016 Neil Ge <neil@gyz.io> 0.2.0-1
- update

* Sun Feb 21 2016 bb <bb> 0.1.0-1pclos2016
- import for kodi 16.0

