# Only a static library is provided, so no debug information can be extracted.
%global debug_package %{nil}

# This package uses assembly to do its work.  This is the entire list of
# supported architectures understood by RPM, even those not currently supported
# by Fedora.  RPM hasn't heard about line continuations, hence the mess.
%global ffcall_arches %{ix86} x86_64 amd64 %{alpha} armv3l armv4b armv4l armv4tl armv5tel armv5tejl armv6l armv7l armv7hl armv7hnl parisc hppa1.0 hppa1.1 hppa1.2 hppa2.0 ia64 m68k mips mipsel ppc ppc8260 ppc8560 ppc32dy4 ppciseries ppcpseries %{power64} s390 s390x %{sparc}

Name:           ffcall
Version:        1.10
Release:        16.20120424cvs%{?dist}
Summary:        Libraries for foreign function call interfaces

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://www.gnu.org/software/libffcall/
# There has been no official release for several years, and the project web
# site encourages use of a CVS snapshot.  Make the tarball as follows:
#   cvs -z3 -d:pserver:anonymous@cvs.savannah.gnu.org:/sources/libffcall 
#       export -D 2012-04-24 ffcall
#   tar cJf ffcall-20120424cvs.tar.xz ffcall
Source0:        %{name}-20120424cvs.tar.xz
# This patch will not be sent upstream.  It removes the possibility of using
# mprotect() to make memory executable, as that runs afoul of SELinux.
Patch0:         %{name}-trampoline.patch
# Upstream is dead, so this patch will not be sent.  Update some uses of OABI
# on ARM to their EABI equivalents.
Patch1:         %{name}-arm.patch

Provides:       %{name}-static = %{version}-%{release}

ExclusiveArch:  %{ffcall_arches}

%description
This is a collection of four libraries which can be used to build
foreign function call interfaces in embedded interpreters.  The four
packages are:
 - avcall: calling C functions with variable arguments
 - vacall: C functions accepting variable argument prototypes
 - trampoline: closures as first-class C functions
 - callback: closures with variable arguments as first-class C functions
   (a reentrant combination of vacall and trampoline)


%prep
%setup -q -n ffcall
%patch0
%patch1

# Remove prebuilt object files
find . -name \*.o | xargs rm -f

%build
export CFLAGS="$RPM_OPT_FLAGS -fPIC -DMAP_VARIABLE=2"
%configure
make # %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}
make install DESTDIR=$RPM_BUILD_ROOT
rm -fr $RPM_BUILD_ROOT%{_datadir}/html
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
cd $RPM_BUILD_ROOT%{_mandir}/man3

# Advertise supported architectures
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat > $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.%{name} << EOF
# arches that ffcall supports
%%ffcall_arches %{ffcall_arches}
EOF

# Fix man pages with overly generic names (bz 800360)
for page in *; do
  mv $page %{name}-$page
done

%files
%doc README NEWS COPYING
%doc avcall/avcall.html
%doc callback/callback.html
%doc callback/trampoline_r/trampoline_r.html
%doc trampoline/trampoline.html
%doc vacall/vacall.html
%{_libdir}/*.a
%{_includedir}/*
%{_mandir}/man*/*
%{_rpmconfigdir}/macros.d/macros.%{name}


%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-16.20120424cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-15.20120424cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb  3 2014 Jerry James <loganjerry@gmail.com> - 1.10-14.20120424cvs
- Update location of rpm macro file for rpm >= 4.11

* Fri Sep  6 2013 Jerry James <loganjerry@gmail.com> - 1.10-13.20120424cvs
- Update -arm patch to really use the EABI and hopefully fix clisp

* Wed Sep  4 2013 Jerry James <loganjerry@gmail.com> - 1.10-12.20120424cvs
- Add -arm patch to fix clisp build failure

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-11.20120424cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 27 2013 Jerry James <loganjerry@gmail.com> - 1.10-10.20120424cvs
- Update to CVS 20120424
- List all architectures supported by this package (bz 925335)
- Rename man pages to avoid conflicts (bz 800360)
- Add Provides: ffcall-static

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-9.20100903cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-8.20100903cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Jerry James <loganjerry@gmail.com> - 1.10-7.20100903cvs
- Clean out prebuilt object files
- Add trampoline patch to force use of mmap() to get executable memory

* Mon Jan  9 2012 Jerry James <loganjerry@gmail.com> - 1.10-6.20100903cvs
- Update to CVS 20100903
- Minor spec file cleanups

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5.20080704cvs.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4.20080704cvs.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3.20080704cvs.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Jochen Schmitt <Jochen herr-schmitt de> - 1.10-2.20080704cvs.1
- Fix -FPIC issue (BZ #475112)

* Fri Jul  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 1.10-2.20080704cvs
- update to cvs 20080704
- support for ppc64

* Mon Feb 25 2008 Gerard Milmeister <gemi@bluewin.ch> - 1.10-1
- first Fedora release
