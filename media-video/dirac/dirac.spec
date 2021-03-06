Name:           dirac
Version:        1.0.2
Release:        19%{?dist}
Summary:        Dirac is an open source video codec 

Group:          System Environment/Libraries
License:        MPLv1.1
URL:            http://diracvideo.org
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         dirac-1.0.2-backports.patch
Patch1:         0001-Fix-uninitialised-memory-read-that-causes-the-encode.patch

BuildRequires:  cppunit-devel
BuildRequires:  doxygen
BuildRequires:  graphviz-devel
BuildRequires:  tex-latex-bin
BuildRequires:  dvipdfm

%description
Dirac is an open source video codec. It uses a traditional hybrid video codec
architecture, but with the wavelet transform instead of the usual block 
transforms.  Motion compensation uses overlapped blocks to reduce block 
artefacts that would upset the transform coding stage.

%package libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description libs
This package contains libraries for %{name}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release} 
Requires:       pkgconfig

%description devel
This package contains development files for %{name}.

%package docs
Summary:        Documentation for %{name}
Group:          Documentation

%description docs
This package contains documentation files for %{name}.


%prep
%setup -q
%patch0 -p0
%patch1 -p1
install -pm 644 README README.Dirac
install -pm 644 util/instrumentation/README README.instrumentation
# fix permission mode for sources.
find doc unit_tests util libdirac_encoder libdirac_byteio -type f -name \* -exec chmod 644 {} \;

#Remove -Werror
sed -i 's/-Werror//g' configure.ac configure


%build
%configure \
  --program-prefix=dirac_ \
  --program-transform-name=s,dirac_dirac_,dirac_, \
  --enable-overlay \
  --disable-static \
%ifarch x86_64 \
  --enable-mmx=yes \
%else \
  --enable-mmx=no \
%endif

# remove rpath from libtool (may be unneeded)
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} 


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Move doc in docdir macro
mv $RPM_BUILD_ROOT%{_datadir}/doc/dirac __doc

# Transform-name fix
mv $RPM_BUILD_ROOT%{_bindir}/dirac_create_dirac_testfile.pl \
	$RPM_BUILD_ROOT%{_bindir}/create_dirac_testfile.pl
sed -i -e 's|"RGBtoYUV"|"dirac_RGBtoYUV"|g' $RPM_BUILD_ROOT%{_bindir}/create_dirac_testfile.pl
sed -i -e 's|/home/guest/dirac-0.5.0/util/conversion|%{_bindir}|' $RPM_BUILD_ROOT%{_bindir}/create_dirac_testfile.pl


%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%doc AUTHORS ChangeLog COPYING NEWS README.Dirac TODO
%doc README.instrumentation
%{_bindir}/create_dirac_testfile.pl                   
%{_bindir}/dirac_*                             

%files devel
%{_includedir}/dirac/
%{_libdir}/pkgconfig/dirac.pc
%{_libdir}/libdirac_*.so

%files docs
%doc __doc/*

%files libs
%{_libdir}/libdirac_decoder.so.*
%{_libdir}/libdirac_encoder.so.*


%changelog
* Sun Feb 14 2016 David Tardon <dtardon@redhat.com> - 1.0.2-19
- rebuild for cppunit 1.13.2

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.2-16
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-14
- Clear spec file - Fix texlive rhbz#1121434

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.0.2-11
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-8
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Feb 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-6
- Backport Fix-uninitialised-memory-read
- Disable -Werror - solve FTBFS with gcc46

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-4
- Backport fix for gcc 4.5.0 - rhbz#660822

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 kwizart < kwizart at gmail.com > - 1.0.2-1
- Update to 1.0.2

* Sun Sep 28 2008 kwizart < kwizart at gmail.com > - 1.0.0-1
- Update to 1.0.0

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.10.0-2
- fix conditional comparison

* Sat Jun 21 2008 kwizart < kwizart at gmail.com > - 0.10.0-1
- Update to 0.10.0

* Sat Feb  9 2008 kwizart < kwizart at gmail.com > - 0.9.1-2
- Rebuild for gcc43

* Mon Jan 28 2008 kwizart < kwizart at gmail.com > - 0.9.1-1
- Update to 0.9.1

* Fri Jan  4 2008 kwizart < kwizart at gmail.com > - 0.8.0-3
- Fix gcc43

* Wed Oct 10 2007 kwizart < kwizart at gmail.com > - 0.8.0-2
- Fix perms

* Wed Oct 10 2007 kwizart < kwizart at gmail.com > - 0.8.0-1
- Update to 0.8.0

* Sun Aug 26 2007 kwizart < kwizart at gmail.com > - 0.7.0-2
- Rebuild for BuildID

* Fri Jun 15 2007 kwizart < kwizart at gmail.com > - 0.7.0-1
- Update to 0.7.0

* Sun Mar 25 2007 kwizart < kwizart at gmail.com > - 0.6.0-9.20070325cvs
- Update to cvs 20070325
- Remove -Werror for CXXFLAGS and decoder
- Fix perms and wrongs end of line encoding

* Sun Mar 25 2007 kwizart < kwizart at gmail.com > - 0.6.0-8.20070108cvs
- Fix mmx only for x86_64
- Fix ldconfig libs

* Sat Mar 24 2007 kwizart < kwizart at gmail.com > - 0.6.0-7.20070108cvs
- Cleaned comment
- Enabled dirac-libs for multi-libs
- Enabled mmx on 64 bit
- Fix Perl script create_dirac_testfile.pl

* Sat Jan 20 2007 kwizart < kwizart at gmail.com > - 0.6.0-6.20070108cvs
- Change cvs order in release
- Change package name libdirac -> dirac
- Drop redundant BR
- Move doc in docdir

* Mon Jan  8 2007 kwizart < kwizart at gmail.com > - 0.6.0-5.cvs20070108
- Update to cvs 20070108 because of a dirac-snapshot corrections.
- Disabled encoder qt4-gui 
(no more provided in the rebuilded package - will reenable later if needed!)

* Fri Jan  5 2007 kwizart < kwizart at gmail.com > - 0.6.0-4.cvs20070105
- Update diract-snapshoot.sh
- Update to cvs 20070105
- Remove BR valgrind (is only requires for test-suite)
- Try to Fix compile Flags
- Exclude static seems better
- Tweak the right FLAGs (drop debug and mmx)

* Thu Jan  4 2007 kwizart < kwizart at gmail.com > - 0.6.0-3.cvs20070104
- Fix BR required and found by mock
- Disable static
- Update doxygen -u before generate doc.
- Bootstrap during snapshot

* Thu Jan  4 2007 kwizart < kwizart at gmail.com > - 0.6.0-2.cvs20070104
- Update to Release 0.6.0 with cvs 20070104
- Enable dirac-qt4 gui

* Tue Dec 12 2006 kwizart < kwizart at gmail.com > - 0.6.0-1
- Intitial release.
