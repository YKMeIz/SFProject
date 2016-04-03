Name:           oggvideotools
Version:        0.8
Release:        16%{?dist}
Summary:        Toolbox for manipulating Ogg video files

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://dev.streamnik.de/oggvideotools.html

Source0:        http://downloads.sourceforge.net/project/oggvideotools/oggvideotools/oggvideotools-0.7b/%{name}-%{version}.tar.gz
Patch0:         oggvideotools-fixbuild.patch

BuildRequires:  pkgconfig
BuildRequires:  libogg-devel libvorbis-devel libtheora-devel SDL-devel
BuildRequires:	gd-devel

%description
A toolbox for manipulating Ogg video files, which usually consist of a
video stream (Theora) and an audio stream (Vorbis). It includes a
number of handy command line tools for manipulating these video files,
such as for splitting the different streams.

%prep
%setup -q
%patch0 -p1 -b .fixbuild

%build
autoreconf -vif #BZ926266 - add support for aarch64
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
chmod 644 docs/DocuOggVideoTools.pdf ChangeLog scripts/*


%files
%defattr(-,root,root,-)
%doc COPYING README ChangeLog docs/DocuOggVideoTools.pdf scripts/*
%{_bindir}/*
%{_mandir}/man1/ogg*

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 0.8-13
- rebuild for new GD 2.1.0

* Mon May 13 2013 Adam Miller <maxamillion@fedoraproject.org> - 0.8-12
- BZ 926266 - add aarch64 support

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 0.8-10
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.8-9
- rebuild against new libjpeg

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul  8 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.8-7
- Fix FTBFS

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-6
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.8-4
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 23 2010 Adam Miller <maxamillion@fedoraproject.org> - 0.8-2
- Added man pages

* Mon May 23 2010 Adam Miller <maxmaillion@fedoraproject.org> - 0.8-1
- Upgrade to latest upstream (0.8)

* Mon Aug 10 2009 Adam Miller <maxamillion [AT] gmail.com> - 0.7b-3
- Fixed source0 as per https://www.redhat.com/archives/fedora-devel-list/2009-August/msg00591.html

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 29 2009 Adam Miller <maxamillion [AT] gmail.com> - 0.7b-1
- New release upstream, previous patches are included and no longer needed

* Mon May 18 2009 Adam Miller <maxamillion [AT] gmail.com> - 0.7a-4
- Patch from upstream applied for segfault in oggStream due to big packets

* Fri May 15 2009 Adam Miller <maxamillion [AT] gmail.com> - 0.7a-3
- Patched a bug in oggSlideshow no showing help menu if no args passed

* Fri May 15 2009 Adam Miller <maxamillion [AT] gmail.com> - 0.7a-2
- Added gd-devel to requires as there was an issue with dependencies of:
	oggSlideshow, oggResize, and oggThumb

* Wed Apr 15 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.7a-1
- update to 0.7a
  dropped upstreamed cstring patch
  added oggResize
  bugfix for wrong size in oggThumb, which causes a green border
  minor bugfixes:
  - random number generator is always initialized with a random seed
  - command line options harmonized (e.g. -s is always size)
  handling for corrupt End-Of-Stream markers
  added sample scripts for easy creation of thumbnails and slideshows with sound
  dokumentation update

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan  9 2009 Matt Domsch <mdomsch@fedoraproject.org> - 0.6-1
- update to 0.6
  added oggSlideshow, oggThumb
  handling for huge files > 4GB implemented
  packet order with oggCut has been fixed and cleaned up
  ogg type in BOS packet is completely analysed
  added support for kate-streams (done by ogg.k.ogg.k)

* Tue Aug 12 2008 Matt Domsch <mdomsch@fedoraproject.org> - 0.5-1
- Fedora patches applied upstream
- improved documentation

* Thu Jul 24 2008 Matt Domsch <mdomsch@fedoraproject.org> - 0.4-1
- initial build
