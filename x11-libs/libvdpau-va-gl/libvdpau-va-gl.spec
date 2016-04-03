Name:           libvdpau-va-gl
Version:        0.3.2
Release:        2%{?dist}
Summary:        VDPAU driver with OpenGL/VAAPI back-end

License:        LGPLv3
URL:            https://github.com/i-rinat/libvdpau-va-gl
Source0:        https://github.com/i-rinat/libvdpau-va-gl/archive/v%{version}.tar.gz

#Unlikely to have some meaning outside of intel driver
ExclusiveArch:  i686 x86_64 ia64

BuildRequires:  cmake
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libva-glx)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)

Requires: libva-intel-driver



%description
VDPAU driver with OpenGL/VAAPI back-end.


%prep
%setup -q


%build
mkdir -p build
cd build
%{cmake} \
  -DLIB_INSTALL_DIR=%{_libdir}/vdpau \
   ..

make %{?_smp_mflags}


%install
cd build
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


#This should automatically enable vdpau backend on intel i965
#But xf86-intel doesn't want't to apply
#http://lists.freedesktop.org/archives/intel-gfx/2013-August/031872.html
ln -s libvdpau_va_gl.so.1 $RPM_BUILD_ROOT%{_libdir}/vdpau/libvdpau_i965.so.1


%files
%doc ChangeLog COPYING* README.md
%{_libdir}/vdpau/libvdpau_va_gl.so.1
%exclude %{_libdir}/vdpau/libvdpau_va_gl.so
#Hack - Will be removed
%{_libdir}/vdpau/libvdpau_i965.so.1



%changelog
* Fri Jul 31 2015 Nux <rpm@li.nux.ro> - 0.3.2-2
- rebuild for newer ffmpeg

* Sun Jan 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.3.2-1
- Update to 0.3.2

* Tue Nov 19 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.2.1-1
- Update to 0.2.1

* Thu Jul 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-1
- Initial spec file

