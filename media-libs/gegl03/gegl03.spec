%global apiver 0.3

Name:           gegl03
Version:        0.3.2
Release:        1%{?dist}
Summary:        Graph based image processing framework

# The binary is under the GPL, while the libs are under LGPL.
# We only install the libs, which makes the license:
License:        LGPLv3+
URL:            http://www.gegl.org/
Source0:        http://download.gimp.org/pub/gegl/%{apiver}/gegl-%{version}.tar.bz2

BuildRequires:  asciidoc
BuildRequires:  enscript
BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  graphviz
BuildRequires:  intltool
BuildRequires:  libspiro-devel
BuildRequires:  perl
BuildRequires:  ruby
BuildRequires:  SDL-devel
BuildRequires:  suitesparse-devel
BuildRequires:  vala-tools

BuildRequires:  pkgconfig(babl) >= 0.1.14
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(exiv2)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.18.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.36.0
BuildRequires:  pkgconfig(jasper) >= 1.900.1
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(lcms2) >= 2.2
BuildRequires:  pkgconfig(lensfun) >= 0.2.5
BuildRequires:  pkgconfig(libraw) >= 0.15.4
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0) >= 2.14.0
BuildRequires:  pkgconfig(libv4l2) >= 1.0.1
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(lua) >= 5.1.0
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pygobject-3.0) >= 3.2
BuildRequires:  pkgconfig(vapigen) >= 0.20.0
BuildRequires:  pkgconfig(libtiff-4) >= 4.0.0

# operations/common/magick-load.c has a fallback image loader which uses /usr/bin/convert
Requires:       /usr/bin/convert

%description
GEGL (Generic Graphics Library) is a graph based image processing framework.
GEGLs original design was made to scratch GIMP's itches for a new
compositing and processing core. This core is being designed to have
minimal dependencies and a simple well defined API.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name} API version 0.3.


%prep
%setup -q -n gegl-%{version}


%build
%configure --disable-static
make %{?_smp_mflags}


%install
%make_install

# Remove .la files
find $RPM_BUILD_ROOT -name '*.la' -delete

# Remove unversioned binaries that would make gegl-0.2 and gegl-0.3
# parallel installations conflict
rm -rf $RPM_BUILD_ROOT%{_bindir}

# Remove API documentation that is currently broken
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%find_lang gegl-%{apiver}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f gegl-%{apiver}.lang
%license COPYING.LESSER
%{_libdir}/gegl-%{apiver}/
%{_libdir}/libgegl-%{apiver}.so.*
# FIXME: gegl-npd and gegl-sc should be versioned as well
%{_libdir}/libgegl-npd-%{apiver}.so
%{_libdir}/libgegl-sc-%{apiver}.so
%{_libdir}/girepository-1.0/Gegl-%{apiver}.typelib

%files devel
%{_includedir}/gegl-%{apiver}/
%{_libdir}/libgegl-%{apiver}.so
%{_libdir}/pkgconfig/gegl-%{apiver}.pc
%{_libdir}/pkgconfig/gegl-sc-%{apiver}.pc
%{_datadir}/gir-1.0/Gegl-%{apiver}.gir
%{_datadir}/vala/vapi/gegl-%{apiver}.deps
%{_datadir}/vala/vapi/gegl-%{apiver}.vapi


%changelog
* Tue Nov 24 2015 Nils Philippsen <nils@redhat.com> - 0.3.2-1
- version 0.3.2
- versionize build requirements
- add missing libtiff build requirement

* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.3.0-5
- rebuild (exiv2)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Nils Philippsen <nils@redhat.com> - 0.3.0-3
- rebuild for suitesparse-4.4.4

* Thu Jun 04 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.3.0-2
- Restore %%{?dist}

* Wed Jun 03 2015 Debarshi Ray <rishi@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.0-0.4.gitc9bbc81
- Rebuilt for GCC 5 C++11 ABI change

* Fri Mar 13 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.0-0.3.gitc9bbc81
- Package review fixes (#1201469)
- Fix grammar errors in package description
- Add a runtime dep on /usr/bin/convert

* Fri Mar 13 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.0-0.2.gitc9bbc81
- Update to latest git master, fixing the build on arm

* Wed Mar 04 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.0-0.1.git06aea8e
- Initial Fedora packaging
