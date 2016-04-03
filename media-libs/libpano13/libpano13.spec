Summary: Library for manipulating panoramic images
Name: libpano13
Version: 2.9.19
Release: 1%{?dist}
License: GPLv2+
URL: http://panotools.sourceforge.net/
Group: Development/Libraries
Source: http://downloads.sourceforge.net/panotools/%{name}-%{version}.tar.gz
BuildRequires: libjpeg-devel, libtiff-devel, libpng-devel, zlib-devel
BuildRequires: cmake
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Helmut Dersch's Panorama Tools library.  Provides very high quality
manipulation, correction and stitching of panoramic photographs.

Due to patent restrictions, this library has a maximum fisheye field-of-view
restriction of 179 degrees to prevent stitching of hemispherical photographs.

%package tools
Summary: Tools that use the libpano13 library
Group: Applications/Multimedia
Requires: %{name} = %{version}-%{release}

%description tools
PTcrop, create cropped TIFF files from uncropped TIFF
PTuncrop, create uncropped TIFF files from cropped TIFF
PTtiffdump
PTinfo
PToptimizer, a command-line interface for control-point optimisation
PTblender, match colour histograms of overlapping TIFF files
PTtiff2psd, convert TIFF files to PSD
panoinfo, a tool for querying pano13 library capabilities
PTmasker 
PTmender, remaps photos between projections
PTroller, merges multiple TIFF with alpha masks to a single TIFF

%package devel
Summary: Development tools for programs which will use the libpano13 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libjpeg-devel, libtiff-devel, libpng-devel, zlib-devel

%description devel
The libpano13-devel package includes the header files necessary for developing
programs which will manipulate panoramas using the libpano13 library.

%prep
%setup -q

%build
%cmake . -DSUPPORT_JAVA_PROGRAMS=0
make VERBOSE=1 %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm %{buildroot}/%{_libdir}/libpano13.a
rm -rf %{buildroot}/usr/share/pano13

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root,-)
%doc AUTHORS ChangeLog COPYING NEWS README README.linux
%{_libdir}/libpano13.so.3*

%files tools
%defattr(-, root, root,-)
%doc doc/Optimize.txt doc/stitch.txt doc/PTblender.readme doc/PTmender.readme
%{_bindir}/PTcrop
%{_bindir}/PTtiffdump
%{_bindir}/PTinfo
%{_bindir}/PToptimizer
%{_bindir}/PTblender
%{_bindir}/PTtiff2psd
%{_bindir}/panoinfo
%{_bindir}/PTmasker
%{_bindir}/PTmender
%{_bindir}/PTroller
%{_bindir}/PTuncrop
%{_mandir}/man1/*.1.gz

%files devel
%defattr(-, root, root,-)
%doc COPYING
%{_includedir}/pano13
%{_libdir}/libpano13.so
%{_libdir}/pkgconfig/libpano13.pc

%changelog
* Thu Oct 16 2014 Bruno Postle <bruno@postle.net> - 2.9.19-1
- Upstream release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.18-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Bruno Postle <bruno@postle.net> - 2.9.18-10
- Drop PTAInterpolate since it required java

* Wed Jun 04 2014 Bruno Postle <bruno@postle.net> - 2.9.18-9
- Drop java support since libgcj-devel no longer in fedora

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.9.18-6
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.9.18-5
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.9.18-2
- Rebuild for new libpng

* Tue May 03 2011 Bruno Postle 2.9.18-1
- new upstream release

* Sat Sep 11 2010 Terry Duell 2.9.17-1
- New upstream release with soname increment

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild


* Tue May 26 2009 Bruno Postle <bruno@postle.net> - 2.9.14-1
- New upstream release with soname increment.
- Maximum fisheye field of view has increased to 179 degrees.
- Obsoletes libpano12-devel and libpano12-tools.
- New man pages and PTAinterpolate tool.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jun 13 2008 Bruno Postle <bruno@postle.net> - 2.9.12-7
- Bad URL report, use sourceforge tar.gz rather than slightly different tar.bz2.
  It seems that there have been two 2.9.12 releases with the old bz2 file being deleted.
  Diffing trees reveals just a couple of bugfixes in the newer gz version.

* Thu May 29 2008 Bruno Postle <bruno@postle.net> - 2.9.12-6
- bumping to fix broken shipped binaries on F-9

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.9.12-5
- Autorebuild for GCC 4.3

* Sun Sep 30 2007 Bruno Postle <bruno@postle.net> 2.9.12-4
- add _smp_mflags, change defattr

* Sun Jul 01 2007 Bruno Postle <bruno@postle.net> 2.9.12-3
- upstream release

* Sat Jan 27 2007 Bruno Postle <bruno@postle.net> 2.9.12-1
- adapted from libpano12 package

