Name:           gstreamer1-libav
Version:        1.0.6
Release:        1%{?dist}
Summary:        GStreamer 1.0 libav-based plug-ins
Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gst-libav/gst-libav-%{version}.tar.xz
# We drop in a newer libav to get all the security bugfixes from there!
Source1:        http://libav.org/releases/libav-0.8.6.tar.xz
Patch0:         gst-ffmpeg-0.10.12-ChangeLog-UTF-8.patch
Patch1:         gst-libav-configure-set-the-assembler.patch
BuildRequires:  gstreamer1-devel >= 1.0.0
BuildRequires:  gstreamer1-plugins-base-devel >= 1.0.0
BuildRequires:  orc-devel bzip2-devel zlib-devel
%ifarch %{ix86} x86_64
BuildRequires:  yasm
%endif

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

This package provides libav-based GStreamer plug-ins.


%prep
%setup -q -n gst-libav-%{version} -a 1
%patch0 -p1
%patch1 -p1
chmod +x configure
rm -r gst-libs/ext/libav
mv libav-0.8.6 gst-libs/ext/libav


%build
# Note no --with-system-ffmpeg *for now*, as gst-ffmpeg wants libav-0.8,
# and the system ffmpeg is 0.11, which is more or less libav-0.9
%configure --disable-dependency-tracking --disable-static \
  --with-package-name="gst-libav 1.0 rpmfusion rpm" \
  --with-package-origin="http://rpmfusion.org/" \
  --with-libav-extra-configure="--enable-runtime-cpudetect --arch=%{_target_cpu} --optflags=\\\"\\\$RPM_OPT_FLAGS\\\""
make %{?_smp_mflags} V=1


%install
make install V=1 DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.la


%files
%doc AUTHORS COPYING.LIB ChangeLog NEWS README TODO
%{_libdir}/gstreamer-1.0/libgstlibav.so
%{_libdir}/gstreamer-1.0/libgstavscale.so


%changelog
* Mon Mar 25 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.6-1
- Rebase to 1.0.6
- Upgrade the buildin libav to 0.8.6 to get all the security fixes from
  upstream libav

* Sun Mar 10 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-2
- Add a patch from upstream git to fix h264 decoding artifacts (rf#2710)
- Add a patch from upstream libav to fix miscompilation with gcc-4.8
  (rf#2710, gnome#695166, libav#388)

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-1
- Rebase to 1.0.5 (rf#2688)
- Upgrade the buildin libav to 0.8.5 to get all the security fixes from
  upstream libav

* Sat Nov  3 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-2
- Build included libav with the default RPM_OPT_FLAGS (rf#2560, rf#2472)

* Sun Oct 28 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-1
- Rebase to 1.0.2
- Included libav copy updated to 0.8.4
- Change the license to LGPLv2+, as the GPL only postproc plugin is no longer
  included
- Replace references to ffmpeg with libav (rf#2472)
- Add COPYING.LIB to %%doc (rf#2472)
- Run make with V=1 (rf#2472)

* Sun Sep 23 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.99-1
- New upstream release 0.11.99

* Sun Sep  9 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.93-1
- First version of gstreamer1-libav for rpmfusion
