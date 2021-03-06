Summary: Library for reading RAW files obtained from digital photo cameras
Name: LibRaw
Version: 0.17.1
Release: 3%{?dist}
License: GPLv3+
Group: Development/Libraries
URL: http://www.libraw.org

BuildRequires: lcms2-devel
BuildRequires: jasper-devel

Source0: http://www.libraw.org/data/%{name}-%{version}.tar.gz
Source1: http://www.libraw.org/data/%{name}-demosaic-pack-GPL2-%{version}.tar.gz
Source2: http://www.libraw.org/data/%{name}-demosaic-pack-GPL3-%{version}.tar.gz
Patch0:  LibRaw-0.6.0-pkgconfig.patch
Patch1:  LibRaw-0.17.1-CVE-2015-8366-8367.patch

Provides: bundled(dcraw) = 9.25

%description
LibRaw is a library for reading RAW files obtained from digital photo
cameras (CRW/CR2, NEF, RAF, DNG, and others).

LibRaw is based on the source codes of the dcraw utility, where part of
drawbacks have already been eliminated and part will be fixed in future.

%package devel
Summary: LibRaw development libraries
Group: Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
LibRaw development libraries.

This package contains libraries that applications can use to build
against LibRaw.

%package static
Summary: LibRaw static development libraries
Group: Development/Libraries

%description static
LibRaw static development libraries.

%package samples
Summary: LibRaw sample programs
Group: Development/Libraries

%description samples
LibRaw sample programs

%prep
%setup -q -a1 -a2

%patch0 -p0 -b .pkgconfig
%patch1 -p1 -b .CVE-2015-8366

%build
%configure --enable-examples=yes --enable-jasper --enable-lcms \
	--enable-demosaic-pack-gpl2 --enable-demosaic-pack-gpl3
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
cp -pr doc manual
chmod 644 LICENSE.CDDL LICENSE.LGPL COPYRIGHT Changelog.txt
chmod 644 manual/*.html

# The Libraries
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.CDDL LICENSE.LGPL COPYRIGHT Changelog.txt
%{_libdir}/*.so.*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%files devel
%defattr(-,root,root,-)
%doc manual
%doc samples
%dir %{_includedir}/libraw
%{_includedir}/libraw/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/*.la
%exclude %{_docdir}/libraw/*

%files samples
%defattr(-,root,root,-)
%{_bindir}/*

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Mon Jan 11 2016 Ding-Yi Chen <dchen@redhat.com> - 0.17.1-3
- Remvoe rpath.

* Tue Dec 01 2015 Jon Ciesla <limburgher@gmail.com> - 0.17.1-2
- Patch for CVE-2015-8366 and CVE-2015-8367, BZ 1287057.

* Sun Nov 29 2015 Jon Ciesla <limburgher@gmail.com> - 0.17.1-1
- 0.17.1.

* Mon Aug 17 2015 Jon Ciesla <limburgher@gmail.com> - 0.17.0-1
- 0.17.0.

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 16 2015 Jon Ciesla <limburgher@gmail.com> - 0.16.2-1
- 0.16.2, BZ 1222258.

* Thu May 14 2015 Jon Ciesla <limburgher@gmail.com> - 0.16.1-7
- Add provides for bundled dcraw, https://fedorahosted.org/fpc/ticket/530
- Fix EVR in changelog.

* Mon May 11 2015 Jon Ciesla <limburgher@gmail.com> - 0.16.1-6
- 0.16.1, BZ 1220382.

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.16.0-5
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Jon Ciesla <limburgher@gmail.com> - 0.16.0-2
- Fix pkg-config flags, BZ 837248.

* Tue Jan 21 2014 Jon Ciesla <limburgher@gmail.com> - 0.16.0-1
- 0.16.0, BZ 1055281.

* Fri Aug 30 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.4-1
- 0.15.4, CVE-2013-1439, BZ 1002717.

* Wed Aug 07 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.3-3
- Enable samples, BZ 991514,

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.3-1
- 0.15.3.

* Wed May 29 2013 Jon Ciesla <limburgher@gmail.com> - 0.15.2-1
- Latest upstream, two security fixes.

* Wed May 29 2013 Jon Ciesla <limburgher@gmail.com> - 0.14.8-2
- Patch for double free, CVE-2013-2126, BZ 968387.

* Wed May 29 2013 Jon Ciesla <limburgher@gmail.com> - 0.14.8-1
- Latest upstream, fixes gcc 4.8 issues.

* Thu Apr 11 2013 Jon Ciesla <limburgher@gmail.com> - 0.14.7-4
- Revert prior patch.

* Thu Apr 11 2013 Jon Ciesla <limburgher@gmail.com> - 0.14.7-3
- Patch for segfault, BZ 948628.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Jon Ciesla <limburgher@gmail.com> - 0.14.7-1
- New upstream 0.14.7

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun  2 2012 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 0.14.6-2
- Use lcms2.

* Sat Jun  2 2012 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 0.14.6-1
- New upstream 0.14.6

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.3-4
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec  9 2011 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 0.14.3-2
- Add demosaic packs (bz #760638)
- Change license to GPLv3+ due to above change

* Wed Nov 16 2011 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> - 0.14.3-1
- Rebase to upstream 0.14.3

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.11.3-2
- Of course, you need to upload the new sources.

* Sun Dec 12 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.11.3-1
- upstream 0.11.3

* Sat Nov 13 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-9
- Build position independent object code

* Thu Jul 08 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-8
- Remove LibRaw license since we're not distributing LibRaw under its terms

* Wed Jul 07 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-7
- Buildroot is unnecessary
- Corrected license to LGPLv2 or CDDL

* Sun Jul 04 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-6
- Do not impose -O4 and -w in build options
- Change package group to Development/Libraries
- Corrected license to LGPLv2
- setup macro no longer needs the name and version arguments
- Rename patches to include name and version

* Wed Jun 30 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-5
- Use optflags for build
- Install the documentation in a cleaner way

* Tue Jun 29 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-4
- Use upstream package name (libRaw) instead of libraw

* Tue Jun 29 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-3
- Remove the clean section since it is not needed in F-13 and later
- Correct installation of docs into defaultdocdir instead of docdir

* Thu Jun 10 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-2
- Disable lcms and openmp support by default so that we're in line with
  upstream default

* Fri Jun 04 2010 Siddhesh Poyarekar <siddhesh.poyarekar@gmail.com> 0.9.1-1
- New package

