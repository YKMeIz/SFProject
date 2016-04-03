Name: dcmtk
Summary: Offis DICOM Toolkit (DCMTK)
Version: 3.6.0
Release: 16%{?dist}
License: BSD
Group: Development/Libraries
Source: ftp://dicom.offis.de/pub/dicom/offis/software/dcmtk/dcmtk360/dcmtk-3.6.0.tar.gz
URL: http://dicom.offis.de/dcmtk.php.en

Patch1: dcmtk-3.6.0-0001-Added-soname-information-for-all-targets.patch
Patch2: dcmtk-3.6.0-0002-Install-libs-in-the-correct-arch-dir.patch
Patch3: dcmtk-3.6.0-0003-Removed-bundled-libcharl-reference-in-dcmjpls.patch
Patch4: dcmtk-3.6.0-0004-Use-system-charls.patch
Patch5: dcmtk-3.6.0-0005-Fixed-includes-for-CharLS-1.0.patch
Patch6: dcmtk-3.6.0-0006-Added-optional-support-for-building-shared-libraries.patch
Patch7: dcmtk-3.6.0-0007-Add-soname-generation-for-modules-which-are-not-in-D.patch
Patch8: dcmtk-3.6.0-0008-Compiler-Fixes.patch

BuildRequires: cmake
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libxml2-devel
BuildRequires: openssl-devel
BuildRequires: tcp_wrappers-devel
BuildRequires: zlib-devel
BuildRequires: CharLS-devel
BuildRequires: doxygen

%description
DCMTK is a collection of libraries and applications implementing large
parts the DICOM standard. It includes software for examining,
constructing and converting DICOM image files, handling offline media,
sending and receiving images over a network connection, as well as
demonstrative image storage and worklist servers. DCMTK is is written
in a mixture of ANSI C and C++.  It comes in complete source code and
is made available as "open source" software. This package includes
multiple fixes taken from the "patched DCMTK" project.

Install DCMTK if you are working with DICOM format medical image files.

%package devel
Summary: Development Libraries and Headers for dcmtk
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: CharLS-devel%{?_isa}
Requires: libpng-devel%{?_isa}
Requires: libtiff-devel%{?_isa}

%description devel
Development Libraries and Headers for dcmtk.  You only need to install
this if you are developing programs that use the dcmtk libraries.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

#Remove bundled libraries
rm -rf dcmjpls/libcharls/

%build

%cmake -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"\
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DDCMTK_WITH_OPENSSL:BOOL=ON\
	-DDCMTK_WITH_PNG:BOOL=ON\
	-DDCMTK_WITH_PRIVATE_TAGS:BOOL=ON\
	-DDCMTK_WITH_TIFF:BOOL=ON\
	-DDCMTK_WITH_XML:BOOL=ON\
	-DDCMTK_WITH_CHARLS=ON\
	-DDCMTK_WITH_ZLIB:BOOL=ON .

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

#move libraries from lib64 to lib64/${name}
#mv $RPM_BUILD_ROOT/usr/%{_lib} $RPM_BUILD_ROOT/tmp_lib
#mkdir -p $RPM_BUILD_ROOT/usr/%{_lib}
#mv $RPM_BUILD_ROOT/tmp_lib $RPM_BUILD_ROOT/usr/%{_lib}/%{name}

#Move configuration file from /usr/etc to /etc/
mv $RPM_BUILD_ROOT/usr/etc $RPM_BUILD_ROOT

#Move doc files from /usr/share/doc to /usr/share/doc/dcmtk-name-version/
#mv $RPM_BUILD_ROOT/usr/share/doc $RPM_BUILD_ROOT/usr/share/%{name}
#mkdir $RPM_BUILD_ROOT/usr/share/doc
#mv $RPM_BUILD_ROOT/usr/share/%{name}-%{version} $RPM_BUILD_ROOT/usr/share/doc/

# Remove zero-lenght file
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/wlistdb/OFFIS/lockfile

# Install ldd config file
#mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
#echo %{_libdir}/%{name} > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

%files
%dir %{_sysconfdir}/%{name}/
#%dir %{_libdir}/%{name}/
%dir %{_datarootdir}/%{name}
%dir %{_docdir}/%{name}/
%docdir %{_docdir}/%{name}/
%{_docdir}/%{name}/*
%{_bindir}/*
%{_libdir}/*.so.*
%config(noreplace) %{_sysconfdir}/%{name}/dcmpstat.cfg
%config(noreplace) %{_sysconfdir}/%{name}/dcmqrscp.cfg
%config(noreplace) %{_sysconfdir}/%{name}/printers.cfg
%config(noreplace) %{_sysconfdir}/%{name}/storescp.cfg
%config(noreplace) %{_sysconfdir}/%{name}/storescu.cfg
%config(noreplace) %{_sysconfdir}/%{name}/filelog.cfg
%config(noreplace) %{_sysconfdir}/%{name}/logger.cfg
#In order to recognize /usr/lib64/dcmtk we need to ship a proper file for /etc/ld.so.conf.d/
#%config %{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_datadir}/%{name}/*
%{_mandir}/man1/*


%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%changelog
* Tue Aug 06 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 3.6.0-16
- General spec cleanup
- Move libs into _lib and remove ldd config file
- Fixes versioned doc dir as per BZ993719
- Bump up release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Mario Ceresa <mrceresa AT fedoraproject DOT org> - 3.6.0-14
- Added more requires to devel package as per BZ922937
- Added _isa to explicit requires

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 01 2012 Jon Ciesla <limburgher@gmail.com> - 3.6.0-12
- FTBFS, BZ 819236.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-10
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 3.6.0-8
- Rebuild for new libpng

* Thu Oct 20 2011 Dan Horák <dan[at]danny.cz> 3.6.0-7
- skip the EOL conversion step, files are correct (FTBFS due a change in dos2unix)

* Wed Oct 19 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-6
- Added explicit require for CharLS-devel as requested in #745277

* Wed Apr 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-5
- Fixed dir ownership

* Wed Apr 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-4
- Added doxygen BR

* Tue Mar 22 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-3
- Fixed soname generation for residual modules

* Mon Mar 21 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-2
- Fixed shared library generation
- Fixed patch schema numbering

* Sun Mar 20 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.0-1
- Removed bundled charls
- Rebased on public dcmtk git repository

* Thu Feb 3 2011 Mario Ceresa <mrceresa@fedoraproject.org> 3.6.1-1.20110203git
- Updated to new version
- Added patch to fix shared lib generation

* Tue Oct 19 2010 Mario Ceresa <mrceresa@fedoraproject.org> 3.5.4-4
- Adding soname's to generated lib

* Mon Mar 15 2010 Andy Loening <loening@alum dot mit dot edu> 3.5.4-3
- updates for packaging with fedora core
- multiple fixes/enhancements from pdcmtk version 48

* Sat Jan 02 2010 Andy Loening <loening@ alum dot mit dot edu> 3.5.4-2
- tlslayer.cc patch for openssl 1.0 

* Thu Feb 02 2006 Andy Loening <loening @ alum dot mit dot edu> 3.5.4-1
- initial build
