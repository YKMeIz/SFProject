Name:           recordmydesktop
Version:        0.3.8.1
Release:        11%{?dist}
Summary:        Desktop session recorder with audio and video

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://recordmydesktop.sourceforge.net/
Source0:        http://downloads.sourceforge.net/recordmydesktop/%{name}-%{version}.tar.gz
# from gentoo: http://bugs.gentoo.org/attachment.cgi?id=209904
# 2010-01-15: Bug with proposed fix already upstream:
# http://sourceforge.net/tracker/?func=detail&aid=2889699&group_id=172357&atid=861428
Patch0:         recordmydesktop-shmstr.h-to-shmproto.h.patch
# Use default Alsa device instead of hardcoded device:
# https://bugzilla.redhat.com/show_bug.cgi?id=538853
Patch1:         recordmydesktop-ALSA-default.patch
# Use sane theora defaults
# https://bugzilla.redhat.com/show_bug.cgi?id=525155
Patch2:         recordmydesktop-sane-theora-defaults.patch
# Fix jack support detection
# https://bugzilla.redhat.com/show_bug.cgi?id=554292
# Patch by debian
# 2010-01-15: patch submitted upstream:
# https://sourceforge.net/tracker/?func=detail&aid=2894861&group_id=172357&atid=861428
Patch3:         recordmydesktop-fix-configure-ac-jack-support.patch

BuildRequires:  libXdamage-devel, libSM-devel
BuildRequires:  libXext-devel
BuildRequires:  alsa-lib-devel, zlib-devel
BuildRequires:  libtheora-devel, libvorbis-devel, jack-audio-connection-kit-devel
Requires:       jack-audio-connection-kit-example-clients


%description
recordMyDesktop is a desktop session recorder for linux that attempts to be 
easy to use, yet also effective at it's primary task.

As such, the program is separated in two parts; a simple command line tool that
performs the basic tasks of capturing and encoding and an interface that 
exposes the program functionality in a usable way.


%prep
%setup -q
# seems that shmstr.h was renamed to shmproto.h in Fedora 12
%if 0%{?fedora} >= 12
%patch0 -p1 -b .shmstr.h-to-shmproto.h
%endif
%patch1 -p1 -b .ALSA-default
%patch2 -p1 -b .sane-theora-defaults
%patch3 -p1 -b .fix-configure-ac-jack-support

#chmod -x $RPM_BUILD_DIR/%{name}-%{version}/src/load_cache.c \
#         $RPM_BUILD_DIR/%{name}-%{version}/include/rmdtypes.h \
#         $RPM_BUILD_DIR/%{name}-%{version}/src/cache_frame.c

%build
# re-run autoreconf to add support for aarch64
autoreconf -i -f
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"

%files
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{_mandir}/man?/*


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mat Booth <fedora@matbooth.co.uk> - 0.3.8.1-10
- Re-run autoreconf to add support for aarch64, rhbz #926435

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 02 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.3.8.1-5
- update URL

* Fri Jan 15 2010 Till Maas <opensource@till.name> - 0.3.8.1-4
- fix jack support: https://bugzilla.redhat.com/show_bug.cgi?id=554292
- use default Alsa device: https://bugzilla.redhat.com/show_bug.cgi?id=538853
- use sane theora defaults: https://bugzilla.redhat.com/show_bug.cgi?id=525155
- apply patch0 only for F12 and higher

* Fri Jan 15 2010 Till Maas <opensource@till.name> - 0.3.8.1-3
- Fix SF.net Source0 URL
- Fix BTFS bug with patch from gentoo: https://bugzilla.redhat.com/show_bug.cgi?id=538931

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.3.8.1-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.3.7.3-2
- fix license tag

* Wed May 28 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.3.7.3-1
- New upstream release

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.7-3
- Autorebuild for GCC 4.3

* Tue Jan 22 2008 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.7-2
- Add missing jack dependency
* Thu Jan 17 2008 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.7-1
- New upstream release
* Sun Dec 02 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.6-2
- Add jack support
* Sun Oct 21 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.6-1
- New version
- Update URL
* Sat Jun 02 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.4-1
- New version 0.3.4
* Mon Mar 05 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.3.1-3
- chmod +x on source files to make rpmlint happy
* Mon Mar 05 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.3.1-2
- Remove duplicate BR
- Add missing zlib-devel BR
- Preserve timestamps
* Sun Mar 04 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.3.1-1
- Initial build

