%global commit0 9f4a84d73fb73d430f07a80cea3688c424439f6a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global realname mfx_dispatch

Name:           libmfx
Version:        0.0.0
Release:        3.%{?shortcommit0}%{?dist}
Summary:        Intel media sdk dispatcher

License:        Intel
URL:            https://github.com/lu-zero/%{realname}
Source0:        https://github.com/lu-zero/%{realname}/archive/%{commit0}.tar.gz#/%{realname}-%{shortcommit0}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libva-devel

%description
Intel Media SDK dispatcher.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qn %{realname}-%{commit0}

%build
autoreconf -vif
%configure \
    --disable-static \
    --enable-shared \
    --with-libva_drm \
    --with-libva_x11
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Thu Feb 04 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-3.9f4a84d
- Update to latest snapshot.
- Update description.

* Sun Dec 13 2015 Simone Caronni <negativo17@gmail.com> - 0.0.0-2.8220f46
- Fix build requirements.

* Fri Nov 27 2015 Simone Caronni <negativo17@gmail.com> 0.0.0-1.8220f46
- First build.
