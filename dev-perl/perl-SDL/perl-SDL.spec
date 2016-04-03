Name:           perl-SDL
Version:        2.544
Release:        5%{?dist}
Summary:        Simple DirectMedia Layer for Perl
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://sdl.perl.org/
Source0:        http://www.cpan.org/authors/id/F/FR/FROGGS/SDL-%{version}.tar.gz
BuildRequires:  libGLU-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  SDL_gfx-devel
BuildRequires:  SDL_image-devel
BuildRequires:  SDL_mixer-devel
BuildRequires:  SDL_net-devel
BuildRequires:  SDL_Pango-devel
BuildRequires:  SDL_ttf-devel
BuildRequires:  perl(Alien::SDL) >= 1.444
BuildRequires:  perl(Archive::Zip)
BuildRequires:  perl(base)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(CPAN) >= 1.92
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::CBuilder)
BuildRequires:  perl(File::ShareDir) >= 1.0
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(lib)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Most) >= 0.21
BuildRequires:  perl(Test::Simple) >= 0.88
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(Tie::Simple)
BuildRequires:  perl(Time::HiRes)
Requires:       perl(CPAN) >= 1.92
Requires:       perl(File::ShareDir) >= 1.0
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%define _use_internal_dependency_generator 0
%{?perl_default_filter}

%description
SDL_perl is a package of Perl modules that provide both functional and
object oriented interfaces to the Simple DirectMedia Layer for Perl 5. This
package takes some liberties with the SDL API, and attempts to adhere to
the spirit of both the SDL and Perl.

%prep
%setup -q -n SDL-%{version}
# Move the pod files directly to directory lib to have correctly generated
# man pages without prefix pods::
cd lib/pods
find * -type d -exec mkdir -p ../{} \;
find * -type f -exec mv {} ../{} \;
cd ..
rm -r pods
cd ..
sed -i -e 's|lib/pods|lib|' MANIFEST
# Disable the sdlx_controller_interface.t test, it hangs on arm
rm t/sdlx_controller_interface.t

%build
perl Build.PL installdirs=vendor optimize="$RPM_OPT_FLAGS"
./Build

%check
./Build test

%install
./Build install destdir=$RPM_BUILD_ROOT create_packlist=0
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;
%{_fixperms} $RPM_BUILD_ROOT/*

%files
%doc CHANGELOG COPYING README TODO
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/SDL*
%{perl_vendorarch}/Module*
%{_mandir}/man3/*

%changelog
* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.544-5
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.544-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Hans de Goede <hdegoede@redhat.com> - 2.544-3
- Rebuild for new SDL_gfx (rhbz#1106197)
- Disable the sdlx_controller_interface.t test, it hangs on arm

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.544-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Pisar <ppisar@redhat.com> - 2.544-1
- 2.544 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.540-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 2.540-4
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.540-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.540-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Jitka Plesnikova <jplesnik@redhat.com> - 2.540-1
- Update to 2.540

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.2.6-7
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.2.6-5
- Rebuild for new libpng

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 2.2.6-4
- Perl mass rebuild

* Fri Jul 15 2011 Hans de Goede <hdegoede@redhat.com> - 2.2.6-3
- Rebuild for new SDL_gfx

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.2.6-2
- Perl mass rebuild

* Tue Feb 22 2011 Hans de Goede <hdegoede@redhat.com> - 2.2.6-1
- Rebase to 2.2.6 upstream release (#679313)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.1.3-14
- 661697 rebuild for fixing problems with vendorach/lib

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.1.3-13
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.1.3-12
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Mar  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.3-9
- rebuild for new perl (again)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.3-8
- Autorebuild for GCC 4.3

* Thu Feb  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.1.3-7
- rebuild for new perl

* Wed Aug 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.1.3-6
- Rebuild for buildId

* Sun Aug 12 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 2.1.3-5
- Update License tag for new Licensing Guidelines compliance
- Add BuildRequires: perl(Test::More) to fix building with the new splitup
  perl

* Tue Jun 19 2007 Matthias Saou <http://freshrpms.net/> 2.1.3-4
- Rebuild against SDL_gfx 2.0.16.

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.1.3-3
- FE6 Rebuild

* Wed Aug 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.1.3-2
- Filter wrong perl(main) and perl(Walker) out of Provides

* Tue Aug 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 2.1.3-1
- Major new upstream version 2.1.3
- Thanks to the rpmforge crew for the filter depends hack!

* Mon Aug 14 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.20.3-8
- Submit to Fedora Extras since it will build without the patented smpeg
  and none of the packages currently using perl-SDL need the smpeg part.
- Drop smpeg BR (see above).
- Cleanup BR's a bit to match FE-guidelines

* Sat Mar 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.20.3-7
- Sync with Debian's 1.20.3-4.
- Default SDL_mixer tests to off.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> 1.20.3-6
- switch to new release field
- fix BR

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Sep 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.20.3-0.lvn.5
- Clean up obsolete pre-FC3 support (SDL_gfx support is now unconditional).
- Drop zero Epochs.

* Mon Jul  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20.3-0.lvn.4
- Clean up obsolete pre-FC2 support.

* Fri Feb 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20.3-0.lvn.3
- Build with SDL_gfx support by default, add "--without gfx" build option.
- Patch to sync with SDL_gfx >= 2.0.12 API changes (bug 374).

* Sun Jul 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20.3-0.lvn.2
- Add "--without mixertest" build option for build roots without audio devices,
  and "--without tests" option to disable tests altogether, needed in FC1
  due to buggy libtiff package (bug 107).

* Sat Jul  3 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20.3-0.lvn.1
- Update to 1.20.3.
- Clean up list of searched include dirs.

* Wed Jun 30 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.20.0-0.lvn.4
- Partial specfile rewrite according to current fedora.us Perl spec template.
- Use tarball + patch from Debian.
- Borrow libGLU fix from Ian Burrell and Matthias Saou, and adjust it a bit:
  http://lists.freshrpms.net/pipermail/freshrpms-list/2003-December/006843.html
- BuildRequire SDL_ttf-devel.

* Fri Jun 27 2003 Phillip Compton <pcompton at proteinmedia dot com> 0:1.20.0-0.fdr.3
- Applied patch to spec from Ville Skyttä changeing:
- BuildRequires: smpeg-devel.
- Run make tesst during build.
- Get rid of unneeded files in installation directories.
- Make installed files writable so that non-root strip works.

* Sun Jun 22 2003 Phillip Compton <pcompton at proteinmedia dot com> 0:1.20.0-0.fdr.2
- Used cpanflute2 to redo the build and install sections.

* Tue May 27 2003 Phillip Compton <pcompton at proteinmedia dot com> 0:1.20.0-0.fdr.1
- Fedorafied

* Mon Mar 31 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Rebuilt for Red Hat Linux 9.

* Mon Feb 17 2003 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.20.0.

* Mon Oct 28 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.19.0.
- Major spec file adaptation :-/

* Fri Sep 20 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.18.7.
- Minor spec cleanups.

* Mon Apr 15 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Update to 1.16.

* Thu Feb  7 2002 Matthias Saou <matthias.saou@est.une.marmotte.net>
- Initial RPM release.
