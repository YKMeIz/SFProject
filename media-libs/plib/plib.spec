Name:           plib
Version:        1.8.5
Release:        6%{?dist}
Summary:        Set of portable libraries especially useful for games
Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://plib.sourceforge.net/
Source:         http://plib.sourceforge.net/dist/plib-%{version}.tar.gz
Patch1:         plib-1.8.4-fullscreen.patch
Patch3:         plib-1.8.4-autorepeat.patch
Patch4:         plib-1.8.5-CVE-2011-4620.patch
BuildRequires:  freeglut-devel libpng-devel libXext-devel libXi-devel
Buildrequires:  libXmu-devel libSM-devel libXxf86vm-devel

%description
This is a set of OpenSource (LGPL) libraries that will permit programmers
to write games and other realtime interactive applications that are 100%
portable across a wide range of hardware and operating systems. Here is
what you need - it's all free and available with LGPL'ed source code on
the web. All of it works well together.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       libGL-devel

%description devel
This package contains the header files and libraries needed to write
or compile programs that use plib.


%prep
%setup -q
%patch1 -p1 -b .fs
%patch3 -p1 -b .autorepeat
%patch4 -p1
# for some reason this file has its x permission sets, which makes rpmlint cry
chmod -x src/sg/sgdIsect.cxx


%build
%configure CXXFLAGS="$RPM_OPT_FLAGS -fPIC -DXF86VIDMODE"
make %{?_smp_mflags} 
# and below is a somewhat dirty hack inspired by debian to build shared libs
# instead of static. Notice that the adding of -fPIC to CXXFLAGS above is part
# of the hack.
dirnames=(util sg ssg fnt js net psl pui puAux pw sl sl ssgAux)
libnames=(ul sg ssg fnt js net psl pu puaux pw sl sm ssgaux)
libdeps=("" \
  "-L../util -lplibul" \
  "-L../util -lplibul -L../sg -lplibsg -lGL" \
  "-L../util -lplibul -L../sg -lplibsg -lGL" \
  "-L../util -lplibul" \
  "-L../util -lplibul" \
  "-L../util -lplibul" \
  "-L../util -lplibul -L../sg -lplibsg -L../fnt -lplibfnt -lGL" \
  "-L../util -lplibul -L../sg -lplibsg -L../fnt -lplibfnt -L../pui -lplibpu -lGL" \
  "-L../util -lplibul -lX11 -lGL -lXxf86vm" \
  "-L../util -lplibul" \
  "-L../util -lplibul" \
  "-L../util -lplibul -L../sg -lplibsg -L../ssg -lplibssg -lGL")

for (( i = 0; i < 13; i++ )) ; do
  pushd src/${dirnames[$i]}
  gcc -shared -Wl,-soname,libplib${libnames[$i]}.so.%{version} \
    -o libplib${libnames[$i]}.so.%{version} `ar t libplib${libnames[$i]}.a` \
    ${libdeps[$i]}
  ln -s libplib${libnames[$i]}.so.%{version} libplib${libnames[$i]}.so
  popd
done


%install
make install DESTDIR=$RPM_BUILD_ROOT
# we don't want the static libs
rm $RPM_BUILD_ROOT%{_libdir}/*.a
# instead do a DIY install of the shared libs we created
cp -a `find . -name "libplib*.so*"` $RPM_BUILD_ROOT%{_libdir}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING ChangeLog NOTICE README
%{_libdir}/libplib*.so.%{version}

%files devel
%{_includedir}/*
%{_libdir}/libplib*.so


%changelog
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Hans de Goede <hdegoede@redhat.com> - 1.8.5-5
- Fix a bufferoverflow in ulSetError() (CVE-2011-4620)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Apr 13 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1.8.5-1
- New upstream release 1.8.5

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.8.4-10
- Autorebuild for GCC 4.3

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1.8.4-9
- Update License tag for new Licensing Guidelines compliance

* Fri Oct  6 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.8.4-8
- Fix keypresses sometimes getting lost by alternative (better) keyboard
  autorepeat support
- Cleanup specfile

* Tue Aug 29 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.8.4-7
- FE6 Rebuild

* Sat Jun 10 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.8.4-6
- Remove use of conditional BuildReqs dependent on %%fedora, this breaks
  when people try to rebuild the SRPM and don't have %%fedora defined.
  (Instead hardcode the correct BR's per Fedora Release).

* Mon Jun  5 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.8.4-5
- Add a missing Requires: libGL-devel to plib-devel subpackage.

* Sat Jun  3 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1.8.4-4
- Taking over as plib maintainer (discussed in bz 192086).
- Add a patch for better fullscreen support (bz 192086).
- Build shared libs instead of static ones. Note: this makes the base
  package a real package instead of only having a -devel package.

* Mon Mar  6 2006 Matthias Saou <http://freshrpms.net/> 1.8.4-3
- FC5 rebuild.

* Thu Feb  9 2006 Matthias Saou <http://freshrpms.net/> 1.8.4-2
- Rebuild for new gcc/glibc and modular X.
- Include gcc 4.1 patch to fix extra qualification errors.

* Mon Jun 27 2005 Matthias Saou <http://freshrpms.net/> 1.8.4-1
- Update to 1.8.4.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.8.3-7
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.8.3-6
- rebuilt

* Wed Feb  9 2005 Matthias Saou <http://freshrpms.net/> 1.8.3-5
- Force -fPIC to be added to CXXFLAGS to fix linking against the lib on x86_64.

* Wed Nov 24 2004 Matthias Saou <http://freshrpms.net/> 1.8.3-4
- Bump release to provide Extras upgrade path.

* Thu Jul 15 2004 Matthias Saou <http://freshrpms.net/> 1.8.3-3
- Only build a devel package now as all files are headers and static libs.

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 1.8.3-2
- Rebuild for Fedora Core 2.

* Thu Apr 15 2004 Matthias Saou <http://freshrpms.net/> 1.8.3-1
- Update to 1.8.3.

* Tue Nov 11 2003 Matthias Saou <http://freshrpms.net/> 1.6.0-3
- Rebuild for Fedora Core 1.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Wed Dec  4 2002 Matthias Saou <http://freshrpms.net/>
- Update to 1.6.0.

* Wed Jun 20 2001 Matthias Saou <http://freshrpms.net/>
- Initial RPM release.

