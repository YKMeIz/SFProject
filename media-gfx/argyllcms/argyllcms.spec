Name:    argyllcms
Version: 1.3.5
Release: 7%{?dist}
Summary: ICC compatible color management system
Group:   User Interface/X
License: GPLv3 and MIT
URL:     http://gitorious.org/hargyllcms
Source0: http://people.freedesktop.org/~hughsient/releases/hargyllcms-%{version}.tar.xz

# Pending upstream review
Patch1:    0001-Add-an-experimental-ColorHug-sensor-driver.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: libtiff-devel
BuildRequires: libusb1-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libXinerama-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: libXrandr-devel
Requires: udev

%description
The Argyll color management system supports accurate ICC profile creation for
acquisition devices, CMYK printers, film recorders and calibration and profiling
of displays.

Spectral sample data is supported, allowing a selection of illuminants observer
types, and paper fluorescent whitener additive compensation. Profiles can also
incorporate source specific gamut mappings for perceptual and saturation
intents. Gamut mapping and profile linking uses the CIECAM02 appearance model,
a unique gamut mapping algorithm, and a wide selection of rendering intents. It
also includes code for the fastest portable 8 bit raster color conversion
engine available anywhere, as well as support for fast, fully accurate 16 bit
conversion. Device color gamuts can also be viewed and compared using a VRML
viewer.

%package doc
Summary: Argyll CMS documentation
Group:   User Interface/X
# Does not really make sense without Argyll CMS itself
Requires: %{name} = %{version}-%{release}

%description doc
The Argyll color management system supports accurate ICC profile creation for
acquisition devices, CMYK printers, film recorders and calibration and profiling
of displays.

This package contains the Argyll color management system documentation.

%prep
%setup -q -n hargyllcms-%{version}
%patch1 -p1 -b .add-colorhug-sensor
autoreconf
automake
libtoolize --force

# we're not allowed to refer to acquisition devices as scanners
./legal.sh

%build
%configure --disable-static
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# We don't want other programs to use these
rm -f $RPM_BUILD_ROOT%{_libdir}/libargyll*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libargyll*.so

%files
%defattr(0644,root,root,0755)
%doc *.txt

%attr(0755,root,root) %{_bindir}/*
%{_datadir}/color/argyll
%{_datadir}/color/argyll/ref
/lib/udev/rules.d/55-Argyll.rules
%{_libdir}/libargyll*.so.*

%exclude %{_datadir}/doc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files doc
%defattr(0644,root,root,0755)
%doc doc/*.html doc/*.jpg

%changelog
* Tue Feb 07 2012 Richard Hughes <rhughes@redhat.com> - 1.3.5-7
- Ship a shared library to reduce the installed package size from
  27.7Mb to 3.2Mb by removing 46 instances of static linking.

* Thu Jan 26 2012 Richard Hughes <rhughes@redhat.com> - 1.3.5-6
- Fix the ColorHug patch to not time out with firmware >= 1.1.1 and to
  correctly report negative numbers.
- Re-libtoolize to fix compile failure on rawhide.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec 11 2011 Richard Hughes <rhughes@redhat.com> - 1.3.5-4
- Build and install ccxxmake, iccdump and icclu.

* Fri Dec 02 2011 Richard Hughes <rhughes@redhat.com> - 1.3.5-3
- Add an experimental ColorHug sensor driver.

* Thu Dec 01 2011 Richard Hughes <rhughes@redhat.com> - 1.3.5-2
- Upstream bundles yajl 1.0.0 and it's impossible to easily switch to
  the system version now Fedora has switched to libyajl.so.2
- Disable the ucmm functionality as it's not even used in Fedora.

* Thu Dec 01 2011 Richard Hughes <rhughes@redhat.com> - 1.3.5-1
- Update to 1.3.5

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.2.20100201git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 01 2010 Richard Hughes <rhughes@redhat.com> - 1.1.0-0.1-20100201git
- Update to 1.1.0
- Switch to using the hargyllcms friendly fork sources as upstream refuses
  to switch away from jam, or stop bundling other projects (yajl) and
  libraries (libusb, libtiff).
- Switch primarily motivated by the fragility of the automake patch, and that
  the original patch will not cleanly apply to the new sources without
  essentially rewriting it. The old patch also compiles a few of the source
  object files 3 or 4 times and links different versions internally with
  different binaries.

* Mon Feb 01 2010 Richard Hughes <rhughes@redhat.com> - 1.0.4-5
- Backport the 55-Argyll.rules files from hargyllcms as the upstream Argyll file
  is insecure.
- Resolves #560050

* Mon Nov 09 2009 Adam Jackson <ajax@redhat.com> 1.0.4-4
- argyllcms-1.0.4-dispwin-randr-fix.patch: Fix dispwin to not look at
  outputs with no CRTC (which is not the same thing as outputs with no
  connection) (#498931)

* Fri Oct 30 2009 Richard Hughes <rhughes@redhat.com> - 1.0.4-3
- Install the udev rules file so users can get the correct device
  permissions on F12 and above which does not use HAL policy files.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Jon Ciesla <limb@jcomserv.net> - 1.0.4-1
- New upstream, incorporating ICC fixes.

* Thu Apr 16 2009 Jon Ciesla <limb@jcomserv.net> - 1.0.3-5
- Actually *apply* previous patch.
- Autotools patch from debian to allow for make check.

* Wed Apr 08 2009 Jon Ciesla <limb@jcomserv.net> - 1.0.3-4
- Patch for ICC library CVE-2009-0792.

* Mon Mar 23 2009 Jon Ciesla <limb@jcomserv.net> - 1.0.3-3
- Patch for ICC library CVE-2009-{0583, 0584} by Tim Waugh.

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 3 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.0.3-1
- Bugfix release

* Mon Sep 1 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.0.2-1
- Bugfix release

* Sun Jul 27 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 1.0.1-1
- Lots of workarounds dropped — Argyll continues progressing towards “normal
  package” state
- No more jam hell, autotooling patch by Alastair M. Robinson
- New workaround added for private libusb check ⚔ We build againt system
  libusb, and will fix any problem people care to report
- Re-applied some patches still not merged upstream, including the legal - one
- It builds, what can go wrong
- Changed Huey policy file. Huey users, please test

* Wed Mar 26 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- patch applied for legal reasons

* Thu Feb 8 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.70-0.8.Beta9
- Another code fix (Stefan Brüns)
- 0.70-0.8.Beta8
- update to Stefan Brüns' latest safe-printf patch (bz421921#c18)

* Thu Feb 7 2008 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.70-0.7.Beta8
  Finally got around packaging beta8, I suck
- Fedora patches merged upstream, dropped from rpm
- Huey handling seems sanitized (needs testing by Huey users)
- Upstream relicensed icc and cgats library to plain MIT license (Thanks!)

* Thu Dec 14 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.70-0.6.Beta7
- fix udev typo
- 0.70-0.5.Beta7
- Remove files that may be GPLv2-only according to upstream

* Thu Dec 13 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.70-0.4.Beta7
- move to modern PolicyKit world (David Zeuthen, Frédéric Crozat, me)

* Wed Dec 12 2007 Nicolas Mailhot <nicolas.mailhot at laposte.net>
- 0.70-0.3.Beta7
- integrate review feedback
- 0.70-0.2.Beta7
- fix buffer overflows in dispread and iccdump (credits Daniel Berrangé)
- 0.70-0.1.Beta7
- 0.70 beta7
- initial laborious packaging
- Build system from hell untangling by Frédéric Crozat (Mandriva), and me
- device permission magic by me
- Massively under-tested package, please report problems

