Name:           sdcc
Version:        3.5.0
Release:        6%{?dist}
Summary:        Small Device C Compiler
Group:          Applications/Engineering
License:        GPLv2+
URL:            http://sdcc.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sdcc/sdcc-src-%{version}.tar.bz2
Source1:        README.fedora
Patch0:         binutils-2.25-bfd.patch
Patch1:         sdcc-%{version}-libiberty.patch
Patch2:		libboost1.60.patch

BuildRequires:  bison
BuildRequires:  boost-devel
BuildRequires:  flex
Buildrequires:  gputils
BuildRequires:  lyx
BuildRequires:  latex2html
BuildRequires:  tex(ulem.sty)
# Work around to lyx-common missing R: /usr/bin/python
BuildRequires:  /usr/bin/python
Provides: bundled(libiberty)


%description
SDCC is a C compiler for 8051 class and similar microcontrollers.
The package includes the compiler, assemblers and linkers, a device
simulator and a core library. The processors supported (to a varying
degree) include the 8051, ds390, z80, hc08, and PIC.


%package libc-sources
Summary:        Small Device C Compiler
Group:          Applications/Engineering
License:        GPLv2+
Requires:       sdcc = %{version}-%{release}

%description libc-sources
SDCC is a C compiler for 8051 class and similar microcontrollers.
This package includes the sources for the C library, and is only necessary
if you want to modify the C library or as reference of how it works.


%package -n emacs-sdcc
Summary:        Emacs extensions for SDCC
Group:          Applications/Editors
License:        GPLv2+
Requires:       sdcc = %{version}-%{release}
Requires:       emacs(bin)

%description -n emacs-sdcc
Emacs extensions for SDCC.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
find -name '*.{c,h,cc}' -exec chmod -x '{}' \;

# Disable brp-strip-static-archive for now because it errors trying to
# strip foreign binaries.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's#/usr/lib/rpm.*/brp-strip-static-archive .*##g')


%build
# Preset PDFOPT to /bin/cp
OPTS='PDFOPT="/bin/cp"'

%configure --enable-doc --disable-non-free STRIP=: ${OPTS}
%{__make} Q= QUIET=


%install
make install DESTDIR=$RPM_BUILD_ROOT Q=
mv $RPM_BUILD_ROOT%{_datadir}/doc installed-docs
install -m 644 %SOURCE1 installed-docs
mkdir -p $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
mv $RPM_BUILD_ROOT%{_bindir}/*.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
find $RPM_BUILD_ROOT -type f -name \*.c -exec chmod a-x '{}' \;
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/sdcc
mv $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_libexecdir}/sdcc


# Create launch scripts in _bindir
pushd $RPM_BUILD_ROOT%{_bindir}
for x in ../libexec/sdcc/*; do
echo "#!/bin/sh
PATH=/usr/libexec/sdcc:\$PATH
/usr/libexec/%{name}/$(basename $x) \"\$@\"" > %{name}-$(basename $x)
chmod 755 %{name}-$(basename $x)
done
popd

pushd $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/src/pic16
find . -type f -name '*.a' -exec chmod 664 '{}' \;
popd


%files
%doc installed-docs/*
%{_bindir}/*
%{_libexecdir}/%{name}
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/lib/src
# Don't include support files as already in binutils-devel
%exclude %{_includedir}/
%exclude %{_libdir}/



%files libc-sources
%{_datadir}/%{name}/lib/src


%files -n emacs-sdcc
%{_datadir}/emacs/site-lisp/*.el


%changelog
* Sun Feb 07 2016 Roy Rankin <rrankin@ihug.com.au> - 3.5.0-6
- Patch for boost-1.60 bug

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 3.5.0-4
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 3.5.0-2
- rebuild for Boost 1.58

* Sat Jul 04 2015 Roy Rankin <rrankin@ihug.com.au> - 3.5.0-1
- Update to upstream release 3.5.0
- Use new --disable-non-free flag in configure

* Mon Jun 29 2015 Jaromir Capik <jcapik@redhat.com> - 3.4.0-7
- Adapting the brp-strip-static-archive hack to work on epel7 too

* Mon Jun 29 2015 Jaromir Capik <jcapik@redhat.com> - 3.4.0-6
- Applying the PDFOPT hack unconditionally
- Cleaning the spec

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 3.4.0-4
- Rebuild for boost 1.57.0

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 3.4.0-3
- Rebuild for boost 1.57.0

* Fri Oct 24 2014 Roy Rankin <rrankin@ihug.com.au> - 3.4.0-2
- Fix brp-strip-static-archive for path change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Roy Rankin <rrankin@ihug.com.au> - 3.4.0-0
- Security patch for libiberty
- Upstream update 3.4.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Dan Horák <dan[at]danny.cz> - 3.3.0-2
- fix FTBFS in bfd caused by GCC 4.9

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 3.3.0-1
- Rebuild for boost 1.55.0

* Mon Sep 02 2013 Roy Rankin <rrankin@ihug.com.au> - 3.3.0-0
- Remove non-free directory tree which is not GPL compatible
- Upstream update 3.3.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 3.2.0-4
- Rebuild for boost 1.54.0

* Fri May 17 2013 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.2.0-3
- Modernize spec.
- Reflect ghostscript in Fedora >= 18 having dropped pdfopt.
  Resort to PDFOPT=/bin/cp.
- Apply patches to allow building against boost > 1.50.0 (Add sdcc-3.2.0.diff).
- BR: /usr/bin/python to work around lyx packaging bug.
- Fix up broken %%changelog entries.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> - 3.2.0-1
- Provides: bundled(libiberty)

* Fri Jul 27 2012 Roy Rankin <rrankin@ihug.com.au> - 3.2.0-0
- Upstream release 3.2.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 26 2012 Conrad Meyer <konrad@tylerc.org> - 3.1.0-1
- Bump to latest upstream (#797496)
- Drop upstreamed patch (workaround for gcc 4.6 bug)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 13 2011 Roy Rankin <rrankin@ihug.com.au> - 3.0.0-1
- Patch for infinite loop in gcc during build

* Sun Mar 20 2011 Roy Rankin <rrankin@ihug.com.au> - 3.0.0-0
- Upstrem release 3.0.0, do not use gc

* Sun Dec 6 2009 Conrad Meyer <konrad@tylerc.org> - 2.9.0-7
- Only disable brp-strip-static.

* Sun Dec 6 2009 Conrad Meyer <konrad@tylerc.org> - 2.9.0-6
- Work around rpmbuild failure by disabling brp-strip.

* Fri Sep 11 2009 Conrad Meyer <konrad@tylerc.org> - 2.9.0-5
- Fix a bug with single-bit types, logical NOT, and casting to char
  (I'm fuzzy on the details) that was reported by a Fedora user with the
  r5508 patch from upstream.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Conrad Meyer <konrad@tylerc.org> - 2.9.0-3
- Fix double-free (rhbz# 509278) with patch from upstream.

* Wed Jul 1 2009 Conrad Meyer <konrad@tylerc.org> - 2.9.0-2
- Fix #454205 by BR'ing gputils and re-adding install_post hack.

* Thu Apr 30 2009 Conrad Meyer <konrad@tylerc.org> - 2.9.0-1
- Bump to 2.9.0.

* Thu Feb 26 2009 Conrad Meyer <konrad@tylerc.org> - 2.8.0-5
- Make subpackages noarch.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 13 2008 Conrad Meyer <konrad@tylerc.org> - 2.8.0-3
- Separate out emacs-sdcc subpackage.

* Thu Oct 16 2008 José Matos <jamatos@fc.up.pt> - 2.8.0-2
- use lyx to generate the pdf documentation and ignore its warnings (for now)

* Tue Sep 9 2008 Conrad Meyer <konrad@tylerc.org> - 2.8.0-1
- Bump to 2.8.0.
- Patch configure to not mess up CFLAGS.
- Patch debugger Makefile to not break canonicalized paths.

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.6.0-13
- fix license tag

* Sun Mar 2  2008 Marek Mahut <mmahut@fedoraproject.org> - 2.6.0-12
- Fixing build problems under GCC 4.3

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.6.0-11
- Autorebuild for GCC 4.3

* Sat Apr 07 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-10
- Added patch to fix a problem with sdccman.lyx that caused lyx to fail.

* Fri Mar 23 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-9
- Removed symlinks, added scripts (solves bug #233385).

* Thu Mar 01 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-8
- Added Fedora specific README file.
- Corrected permissions on files in debuginfo package.

* Wed Feb 28 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-7
- Updated requirement for libc-source to include version and release number.

* Wed Feb 28 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-6
- Renamed source code package to libc-sources.
- Change BuildRequire from byacc to bison.
- Added "Require: sdcc" to libc-sources package.
- Empty %%doc entry removed.
- Updated description of libc-sources package.

* Tue Feb 27 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-5
- Source URL updated.
- Separate src package created.
- Disabling stripping of binaries to get proper debuginfo package.

* Mon Feb 26 2007 Ralf Corsépius <rc040203@freenet.de> - 2.6.0-4
- Add sdcc-2.6.0-configure.diff.
- Pass Q= to make to make building verbose.
- Add __os_install_post post-hacks to prevent brp-strip from processing
  foreign binaries.

* Mon Feb 26 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-3
- Broken symlinks fixed.

* Mon Feb 5 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-2
- Emacs scripts moved to the correct folder.
- Moved binaries to /urs/libexec/sdcc, added symlinks with sdcc- prefix in /usr/bin.
- Various rpmlint errors fixed.

* Thu Feb 1 2007 Trond Danielsen <trond.danielsen@gmail.com> - 2.6.0-1
- Initial version.
