Name:           fftw
Version:        3.3.4
Release:        7%{?dist}
Summary:        A Fast Fourier Transform library
Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.fftw.org
Source0:        http://www.fftw.org/fftw-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gcc-gfortran

%global quad 0
# Quad precision support only available with gcc >= 4.6 (Fedora >= 15)
# and only on these arches
%ifarch %{ix86} x86_64 ia64
%global quad 1
%endif

# For check phase
BuildRequires:  time
BuildRequires:  perl

Requires(post): info 
Requires(preun): info


%description
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

%package libs
Summary:        FFTW run-time library
Group:          System Environment/Libraries
Provides:       fftw3 = %{version}-%{release}
# Libs rearranged in 3.3.1-2
Obsoletes:      fftw-libs-threads < %{version}-%{release}
Obsoletes:      fftw-libs-openmp < %{version}-%{release}

# Pull in the actual libraries
Requires:        %{name}-libs-single%{?_isa} = %{version}-%{release}
Requires:        %{name}-libs-double%{?_isa} = %{version}-%{release}
Requires:        %{name}-libs-long%{?_isa} = %{version}-%{release}
%if %{quad}
Requires:        %{name}-libs-quad%{?_isa} = %{version}-%{release}
%endif

%description libs
This is a dummy package package, pulling in the individual FFTW
run-time libraries.


%package devel
Summary:        Headers, libraries and docs for the FFTW library
Group:          Development/Libraries
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Provides:       fftw3-devel%{?_isa} = %{version}-%{release}
Provides:       fftw3-devel = %{version}-%{release}

%description devel
FFTW is a C subroutine library for computing the Discrete Fourier
Transform (DFT) in one or more dimensions, of both real and complex
data, and of arbitrary input size.

This package contains header files and development libraries needed to
develop programs using the FFTW fast Fourier transform library.

%package libs-double
Summary:        FFTW library, double precision
Group:          Development/Libraries

%description libs-double
This package contains the FFTW library compiled in double precision.

%package libs-single
Summary:        FFTW library, single precision
Group:          Development/Libraries

%description libs-single
This package contains the FFTW library compiled in single precision.

%package libs-long
Summary:        FFTW library, long double precision 
Group:          Development/Libraries

%description libs-long
This package contains the FFTW library compiled in long double
precision.

%if %{quad}
%package libs-quad
Summary:        FFTW library, quadruple
Group:          Development/Libraries

%description libs-quad
This package contains the FFTW library compiled in quadruple
precision.
%endif

%package        static
Summary:        Static versions of the FFTW libraries
Group:          Development/Libraries
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Provides:       fftw3-static%{?_isa} = %{version}-%{release}
Provides:       fftw3-static = %{version}-%{release}

%description static
The fftw-static package contains the statically linkable version of
the FFTW fast Fourier transform library.

%package doc
Summary:        FFTW library manual
Group:          Documentation
BuildArch:      noarch

%description doc
This package contains the manual for the FFTW fast Fourier transform
library.

%prep
%setup -q

%build
# Configure uses g77 by default, if present on system
export F77=gfortran

BASEFLAGS="--enable-shared --disable-dependency-tracking --enable-threads"
BASEFLAGS+=" --enable-openmp"

# Precisions to build
prec_name[0]=single
prec_name[1]=double
prec_name[2]=long
prec_name[3]=quad

# Corresponding flags
prec_flags[0]=--enable-single
prec_flags[1]=--enable-double
prec_flags[2]=--enable-long-double
prec_flags[3]=--enable-quad-precision

%ifarch x86_64
# Enable SSE2 and AVX support for x86_64
for((i=0;i<2;i++)); do
 prec_flags[i]+=" --enable-sse2 --enable-avx"
done
%endif

# No NEON run time detection, not all ARM SoCs have NEON
#%ifarch %{arm}
## Compile support for NEON instructions
#for((i=0;i<2;i++)); do
# prec_flags[i]+=" --enable-neon"
#done
#%endif

#%ifarch ppc ppc64
## Compile support for Altivec instructions
#for((i=0;i<2;i++)); do
 #prec_flags[i]+=" --enable-altivec"
#done
#%endif

# Loop over precisions
%if %{quad}
for((iprec=0;iprec<4;iprec++))
%else
for((iprec=0;iprec<3;iprec++))
%endif
do
 mkdir ${prec_name[iprec]}${ver_name[iver]}
 cd ${prec_name[iprec]}${ver_name[iver]}
 ln -s ../configure .
 %{configure} ${BASEFLAGS} ${prec_flags[iprec]}
 sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
 sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
 make %{?_smp_mflags}
 cd ..
done

%install
rm -rf %{buildroot}
%if %{quad}
for ver in single double long quad
%else
for ver in single double long
%endif
do
 make -C $ver install DESTDIR=%{buildroot}
done
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_libdir}/*.la

%check
bdir=`pwd`
%if %{quad}
for ver in single double long quad
%else
for ver in single double long
%endif
do 
 export LD_LIBRARY_PATH=$bdir/$ver/.libs:$bdir/$ver/threads/.libs
 make -C $ver check
done

%clean
rm -rf %{buildroot}

%post libs-single -p /sbin/ldconfig
%postun libs-single -p /sbin/ldconfig
%post libs-double -p /sbin/ldconfig
%postun libs-double -p /sbin/ldconfig
%post libs-long -p /sbin/ldconfig
%postun libs-long -p /sbin/ldconfig
%if %{quad}
%post libs-quad -p /sbin/ldconfig
%postun libs-quad -p /sbin/ldconfig
%endif

%post devel
/sbin/install-info --section="Math" %{_infodir}/%{name}.info.gz %{_infodir}/dir  2>/dev/null || :

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir 2>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc %{_mandir}/man1/fftw*.1.*
%{_bindir}/fftw*-wisdom*

%files libs
%defattr(-,root,root,-)

%files libs-single
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/libfftw3f.so.*
%{_libdir}/libfftw3f_threads.so.*
%{_libdir}/libfftw3f_omp.so.*

%files libs-double
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/libfftw3.so.*
%{_libdir}/libfftw3_threads.so.*
%{_libdir}/libfftw3_omp.so.*

%files libs-long
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/libfftw3l.so.*
%{_libdir}/libfftw3l_threads.so.*
%{_libdir}/libfftw3l_omp.so.*

%if %{quad}
%files libs-quad
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYRIGHT ChangeLog NEWS README* TODO
%{_libdir}/libfftw3q.so.*
%{_libdir}/libfftw3q_threads.so.*
%{_libdir}/libfftw3q_omp.so.*
%endif

%files devel
%defattr(-,root,root,-)
%doc doc/FAQ/fftw-faq.html/
%doc %{_infodir}/fftw3.info*
%{_includedir}/fftw3*
%{_libdir}/pkgconfig/fftw3*.pc
%{_libdir}/libfftw3*.so

%files doc
%defattr(-,root,root,-)
%doc doc/*.pdf doc/html/

%files static
%defattr(-,root,root,-)
%{_libdir}/libfftw3*.a

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.3.4-4
- Disable SSE2/AVX on x86(32) as we support Pentium Pro as base
- SSE2 only arrived with P-4
- https://fedoraproject.org/wiki/Features/F12X86Support
- Fix ARM macro
- Disable NEON on ARM (we don't enable by default, needs runtime detection)

* Thu Jul 03 2014 Conrad Meyer <cemeyer@uw.edu> - 3.3.4-3
- Build with --enable-avx (rhbz# 1114964)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.4-1
- Update to 3.3.4.

* Sat Dec 14 2013 Conrad Meyer <cemeyer@uw.edu> - 3.3.3-8
- Remove non-OpenMP / g77 build for obsolete RHEL (< 5)
- Remove ancient Obsoletes (fftw < 3.3, Fedora < 16)
- Remove ancient non-Quad build (Fedora < 15) on supported arch(s)
- Remove obsolete conditional on BuildArch: noarch (RHEL < 6, Fedora < 13)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 PPC Secondary Arch Admin <karsten@redhat.com> 3.3.3-5
- disable altivec flag again, that works with single precision only

* Mon Dec 24 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-4
- Fix typo: should be %%ix86 instead of %%x86. Now should have SSE2 support
  on x86 as well.

* Tue Dec 18 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-3
- After consultation with upstream, enable SSE2 also on x86, altivec on ppc
  and ppc64 and NEON on arm.

* Tue Dec 18 2012 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-2
- Enable SSE2 on x86_64.

* Mon Nov 26 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.3-1
- Update to 3.3.3.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Orion Poplawski <orion@cora.nwra.com> - 3.3.2-1
- Update to 3.3.2
- Drop alignment patch

* Fri Apr 27 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-3
- Fix FTBFS with gcc 4.7.

* Thu Apr 26 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-2
- Reorganized libraries (BZ #812981).

* Mon Feb 27 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Dan Horák <dan[at]danny.cz> - 3.3-4
- libquadmath exists only on x86/x86_64 and ia64

* Mon Oct 10 2011 Rex Dieter <rdieter@fedoraproject.org> 3.3-3
- -devel: Provides: fftw3-devel (#744758)
- -static: Provides: fftw3-static
- drop %%_isa from Obsoletes

* Sat Jul 30 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3-2
- Conditionalize OpenMP and quadruple precision support based on capabilities
  of system compiler.

* Thu Jul 28 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.3-1
- Update to 3.3.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-4
- Get rid of rpath.

* Sat Jan 9 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-3
- Branch out developers' manual to -doc.

* Sat Jan 2 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-2
- Add check phase.
- Cosmetic changes to spec file (unified changelog format, removed unnecessary
  space).
- Use rm instead of find -delete, as latter is not present on EPEL-4.
- Generalize obsoletes of fftw3 packages. Add Obsoletes: fftw3-static.

* Fri Jan 1 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.2.2-1
- Update to 3.2.2.
- Make file listings more explicit.
- Don't use file dependencies for info.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Conrad Meyer <konrad@tylerc.org> - 3.2.1-1
- Bump to 3.2.1.

* Thu Dec 4 2008 Conrad Meyer <konrad@tylerc.org> - 3.2-1
- Bump to 3.2.

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.1.2-7
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.1.2-6
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Quentin Spencer <qspencer@users.sf.net> 3.1.2-5
- Rebuild for F8.

* Fri Jul 27 2007 Quentin Spencer <qspencer@users.sf.net> 3.1.2-4
- Split static libs into separate package (bug 249686).

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 3.1.2-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-2
- BuildRequires: pkgconfig for -devel (bug 206444).

* Fri Sep  8 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.2-1
- New release.

* Fri Jun  2 2006 Quentin Spencer <qspencer@users.sf.net> 3.1.1-1
- New upstream release.

* Fri Feb 24 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-4
- Re-enable static libs (bug 181897).
- Build long-double version of libraries (bug 182587).

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-3
- Add Obsoletes and Provides.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-2
- Rebuild for Fedora Extras 5.
- Disable static libs.
- Remove obsolete configure options.

* Wed Feb  1 2006 Quentin Spencer <qspencer@users.sf.net> 3.1-1
- Upgrade to the 3.x branch, incorporating changes from the fftw3 spec file.
- Add dist tag.
