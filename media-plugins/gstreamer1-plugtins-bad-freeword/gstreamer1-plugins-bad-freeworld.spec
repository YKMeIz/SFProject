# which plugins to actually build and install
%global gstdirs gst/dvbsuboverlay gst/dvdspu gst/siren
%global extdirs ext/dts ext/faad ext/libmms ext/mimic ext/mpeg2enc ext/mpg123 ext/mplex ext/rtmp ext/voamrwbenc

Summary:        GStreamer 1.0 streaming media framework "bad" plug-ins
Name:           gstreamer1-plugins-bad-freeworld
Version:        1.0.6
Release:        1%{?dist}
License:        LGPLv2+
Group:          Applications/Multimedia
URL:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz
BuildRequires:  gstreamer1-devel >= 1.0.0
BuildRequires:  gstreamer1-plugins-base-devel >= 1.0.0
BuildRequires:  check
BuildRequires:  gettext-devel
BuildRequires:  libXt-devel
BuildRequires:  gtk-doc
BuildRequires:  orc-devel
BuildRequires:  libdca-devel
BuildRequires:  faad2-devel
BuildRequires:  libmms-devel
BuildRequires:  mjpegtools-devel >= 2.0.0
BuildRequires:  twolame-devel
BuildRequires:  libmimic-devel
BuildRequires:  librtmp-devel
BuildRequires:  vo-amrwbenc-devel
#BuildRequires:  vo-aacenc-devel
BuildRequires:  libmpg123-devel
BuildRequires: libusbx-devel

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that have licensing issues, aren't tested
well enough, or the code is not of good enough quality.


%prep
%setup -q -n gst-plugins-bad-%{version}


%build
# Note we don't bother with disabling everything which is in Fedora, that
# is unmaintainable, instead we selectively run make in subdirs
%configure \
    --with-package-name="gst-plugins-bad 1.0 rpmfusion rpm" \
    --with-package-origin="http://rpmfusion.org/" \
    --enable-debug --disable-static --enable-experimental
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
for i in %{gstdirs} %{extdirs}; do
    pushd $i
    make %{?_smp_mflags} V=2
    popd
done


%install
for i in %{gstdirs} %{extdirs}; do
    pushd $i
    make install V=2 DESTDIR=$RPM_BUILD_ROOT
    popd
done
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/*.la


%files
%doc AUTHORS COPYING.LIB NEWS README RELEASE
# Take the whole dir for proper dir ownership (shared with other plugin pkgs)
%{_datadir}/gstreamer-1.0

# Plugins without external dependencies
%{_libdir}/gstreamer-1.0/libgstdvbsuboverlay.so
%{_libdir}/gstreamer-1.0/libgstdvdspu.so
%{_libdir}/gstreamer-1.0/libgstsiren.so

# Plugins with external dependencies
%{_libdir}/gstreamer-1.0/libgstdtsdec.so
%{_libdir}/gstreamer-1.0/libgstfaad.so
%{_libdir}/gstreamer-1.0/libgstmms.so
%{_libdir}/gstreamer-1.0/libgstmimic.so
%{_libdir}/gstreamer-1.0/libgstmpeg2enc.so
%{_libdir}/gstreamer-1.0/libgstmpg123.so
%{_libdir}/gstreamer-1.0/libgstmplex.so
%{_libdir}/gstreamer-1.0/libgstrtmp.so
#%%{_libdir}/gstreamer-1.0/libgstvoaacenc.so
%{_libdir}/gstreamer-1.0/libgstvoamrwbenc.so


%changelog
* Mon Mar 25 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.6-1
- New upstream release 1.0.6

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-1
- New upstream release 1.0.5
- Drop no longer needed PyXML BuildRequires (rf#2572)

* Sat Nov  3 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-2
- Include some more files in %%doc (rf#2473)

* Sun Oct 28 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-1
- New upstream release 1.0.2

* Sun Sep 23 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.99-1
- New upstream release 0.11.99
- Use global rather then define (rf#2473)
- Disable vo-aacenc plugin for now (rf#1742)
- Enable siren plugin now that it has been ported to the 1.0 API

* Sun Sep  9 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.93-1
- First version of gstreamer1-plugins-ugly for rpmfusion
