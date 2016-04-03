Name:           ffmpegthumbnailer
Version:        2.0.9
Release:        1%{?dist}
Summary:        Lightweight video thumbnailer that can be used by file managers

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://code.google.com/p/ffmpegthumbnailer/
Source0:        https://bitbucket.org/mtuominen/fedora/src/49e8ed786ec5813f6b0ca53eb96d7e8dceb2e81f/SOURCES/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ffmpeg-devel, libpng-devel, libjpeg-devel
BuildRequires:  chrpath, automake, autoconf, libtool, gcc-c++

%description
This video thumbnailer can be used to create thumbnails for your video files.

%package devel
Summary:        Headers and libraries for building apps that use ffmpegthumbnailer
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This video thumbnailer can be used to create thumbnails for your video files,
development package.

%prep
%setup -q
chmod -x README INSTALL COPYING AUTHORS

%build
./autogen.sh
%configure --enable-png \
           --enable-jpeg \
           --disable-static \
           --enable-gio \
           --enable-thumbnailer

make %{?_smp_mflags}

 
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#chrpath --delete $RPM_BUILD_ROOT%%{_bindir}/ffmpegthumbnailer
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README COPYING AUTHORS
%{_bindir}/ffmpegthumbnailer
%{_libdir}/libffmpegthumbnailer.so.4*
%{_mandir}/man1/ffmpegthumbnailer.1.gz
# gnome thumbnailer registration
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/ffmpegthumbnailer.thumbnailer

%files devel
%defattr(-,root,root,-)
%{_libdir}/libffmpegthumbnailer.so
%{_libdir}/pkgconfig/libffmpegthumbnailer.pc
%{_includedir}/libffmpegthumbnailer/


%changelog
* Thu Apr 09 2015 Magnus Tuominen <magnus.tuominen@gmail.com> - 2.0.9-1
- 2.0.9

* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 2.0.8-11
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.0.8-10
- Rebuilt for FFmpeg 2.4.x

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 2.0.8-9
- Rebuilt for ffmpeg-2.3

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> - 2.0.8-8
- Rebuilt for ffmpeg-2.2

* Wed Nov 27 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-7
- fix compile error

* Wed Oct 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.8-6
- Rebuilt

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.8-5
- Rebuilt for FFmpeg 2.0.x

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.8-4
- Rebuilt for x264/FFmpeg

* Mon Mar 04 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.8-3
- Rebuilt for F-19 Features

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.8-2
- Rebuilt for FFmpeg 1.0

* Wed Aug 29 2012 Magnus Tuominen <magnus.tuominen@gmail.com> - 2.0.8-1
- 2.0.8

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.7-4
- Rebuilt for c++ ABI breakage

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.7-3
- Rebuilt for x264/FFmpeg

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 29 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 2.0.7-1
- new version
- patches merged upstream

* Mon Sep 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.0.6-3
- Rebuilt for FFmpeg-0.8*

* Sun Feb 13 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 2.0.6-2
- patch NULL reference to make rawhide build

* Fri Jan 04 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 2.0.6-1
- version bump
- patch libdl link issue
- add BR: automake and autoconf

* Sun Dec 05 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 2.0.5-1
- version bump
- enable gio-support

* Sat Aug 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0.4-2
- rebuilt

* Wed Aug 18 2010 Magnus Tuominen <magnus.tuominen@gmail.com> 2.0.4-1
- version bump

* Sun May 16 2010 Magnus Tuominen <magnus.tuominen@gmail.com> 2.0.2-1
- version bump

* Sat Apr 19 2010 Magnus Tuominen <magnus.tuominen@gmail.com> 2.0.1-1
- version bump
- libspatch.patch merged upstream, issue 59

* Mon Apr 12 2010 Magnus Tuominen <magnus.tuominen@gmail.com> 2.0.0-3
- drop _kde4_ macros
- moving chmod to %%prep
- moving %%{_includedir}/libffmpegthumbnailer to -devel
- track sonames closer
- license change to GPLv2+
- remove duplicate docs from -devel
- patching libs in pkgconfig%%{name}.pc, thanks to rdieter

* Sun Apr 11 2010 leigh scott <leigh123linux@googlemail.com> 2.0.0-2
- fix rpath
- enable jpeg and png support
- clean up spec file
- remove static libs as they aren't needed
- add docs

* Sat Apr 10 2010 Magnus Tuominen <magnus.tuominen@gmail.com> 2.0.0-1
- initial build
- has to be built with "QA_RPATHS=$[0x0001|0x0010 ]" for now
