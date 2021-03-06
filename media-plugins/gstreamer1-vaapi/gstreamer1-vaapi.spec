Name:           gstreamer1-vaapi
Version:        0.6.1
Release:        1%{?dist}
Summary:        GStreamer plugins to use VA API video acceleration

License:        LGPLv2+
URL:            https://github.com/01org/gstreamer-vaapi
Source0:        http://www.freedesktop.org/software/vaapi/releases/gstreamer-vaapi/gstreamer-vaapi-%{version}.tar.bz2

BuildRequires:  glib2-devel >= 2.28
BuildRequires:  gstreamer1-devel >= 1.0.0
BuildRequires:  gstreamer1-plugins-base-devel >= 1.0.0
BuildRequires:  gstreamer1-plugins-bad-free-devel >= 1.0.0
BuildRequires:  libva-devel >= 1.1.0
BuildRequires:  libdrm-devel
BuildRequires:  libudev-devel
BuildRequires:  libGL-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  libvpx-devel
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)

%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client) >= 1
BuildRequires:  pkgconfig(wayland-scanner) >= 1
BuildRequires:  pkgconfig(wayland-server) >= 1
%endif

# We can't provide encoders or decoders unless we know what VA-API drivers
# are on the system. Just filter them out, so they're not suggested by
# PackageKit et al.
%global __provides_exclude gstreamer1\\(decoder|gstreamer1\\(encoder

%description

A collection of GStreamer plugins to let you make use of VA API video
acceleration from GStreamer applications.

Includes elements for video decoding, display, encoding and post-processing
using VA API (subject to hardware limitations).

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?isa} = %{version}-%{release}
Requires:       pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n gstreamer-vaapi-%{version}

%build

# Fix for https://bugzilla.gnome.org/show_bug.cgi?id=723748
chmod -x ./tests/test-filter.c ./gst-libs/gst/vaapi/gstvaapifilter.c ./gst-libs/gst/vaapi/gstvaapifilter.h

# Wayland support in libva isn't present - gstreamer-vaapi can't support Wayland without it
# https://bugzilla.redhat.com/show_bug.cgi?id=1051862
%configure \
           --enable-static=no \
           %{?_without_wayland:--disable-wayland} \
           --disable-builtin-libvpx

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%make_install

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB NEWS README
%{_libdir}/*.so.*
%{_libdir}/gstreamer-1.0/*.so

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING.LIB NEWS README
%{_includedir}/gstreamer-1.0/gst/vaapi
%{_libdir}/*.so
%{_libdir}/pkgconfig/gstreamer-vaapi*.pc

%changelog
* Wed Sep 30 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.6.1-1
- Update to 0.6.1

* Sat Jul 18 2015 Francesco Frassinelli <fraph24@gmail.com> - 0.6.0-1
- Update to 0.6.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr  7 2015 Simon Farnsworth <simon.farnsworth@onelan.co.uk> - 0.5.10-3
- Update URL to follow project after gitorious shutdown

* Sun Feb 15 2015 Simon Farnsworth <simon.farnsworth@onelan.co.uk> - 0.5.10-2
- Fix FTBFS on s390x due to header file not matching implementation

* Tue Feb  3 2015 Simon Farnsworth <simon@farnz.org.uk> - 0.5.10-1
- Update to 0.5.10 release
- Filter out encoder and decoder Provides

* Tue Nov 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.5.9-3
- Rebuilt for vaapi 0.36

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug  1 2014 Simon Farnsworth <simon.farnsworth@onelan.co.uk> - 0.5.9-1
- Update to 0.5.9 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr  9 2014 Simon Farnsworth <simon.farnsworth@onelan.co.uk> - 0.5.8-4
- Provide Wayland support now that libva includes it

* Fri Feb  7 2014 Simon Farnsworth <simon@farnz.org.uk> - 0.5.8-3
- Fix typo in spec file - Patch1 and %patch0 don't go together

* Fri Feb  7 2014 Simon Farnsworth <simon@farnz.org.uk> - 0.5.8-2
- Fix vaapipostproc crash in live pipelines

* Wed Feb  5 2014 Simon Farnsworth <simon@farnz.org.uk> - 0.5.8-1
- initial release
