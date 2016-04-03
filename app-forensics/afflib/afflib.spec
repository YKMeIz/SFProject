%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           afflib
Version:        3.7.3
Release:        3%{?dist}
Summary:        Library to support the Advanced Forensic Format

Group:          System Environment/Libraries
License:        BSD with advertising
URL:            http://www.afflib.org
Source0:        https://github.com/simsong/AFFLIBv3/archive/v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libtool

BuildRequires:  curl-devel
BuildRequires:  expat-devel
# GPLv2 FOSS incompatible with BSD with advertising
##BuildRequires:  fuse-devel
# Afflib uses lzma-SDK 443
BuildRequires:  lzma-devel
BuildRequires:  ncurses-devel
BuildRequires:  libtermcap-devel
BuildRequires:  openssl-devel
BuildRequires:  python-devel
# GPLv2 FOSS incompatible with BSD with advertising
##BuildRequires:  readline-devel
#BuildRequires:  libedit-devel - good replacement for readline - not supported for now
BuildRequires:  zlib-devel


%description
AFF® is an open and extensible file format designed to store disk images and
associated metadata.
afflib is library for support of the Advanced Forensic Format (AFF).


%package -n     afftools
Summary:        Utilities for %{name}
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description -n afftools
The %{name}-utils package contains utilities for using %{name}.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n AFFLIBv3-%{version}
# prevent internal lzma to be built - testing
#rm -rf lzma443

#fix spurious permissions with lzma443
find lzma443 -type f -exec chmod 0644 {} ';'
chmod 0644 lib/base64.{h,cpp}

./bootstrap.sh

%build
%configure --enable-shared \
  --disable-static \
  --enable-python=yes \
  --enable-s3=yes

# Remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# clean unused-direct-shlib-dependencies
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'



%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGLIST.txt ChangeLog COPYING NEWS README
%doc doc/announce_2.2.txt 
%{_libdir}/*.so.*

%files -n afftools
%defattr(-,root,root,-)
%{_bindir}/aff*
%{python_sitearch}/pyaff.so
%{_mandir}/man1/affcat.1.*

%files devel
%defattr(-,root,root,-)
%doc doc/crypto_design.txt doc/crypto_doc.txt
%{_includedir}/afflib/
%{_libdir}/*.so
%{_libdir}/pkgconfig/afflib.pc


%changelog
* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jan 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.6.15-1
- Update to 3.6.15

* Thu Sep 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.6.12-2
- Enable S3

* Fri May 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.6.12-1
- Update to 3.6.12

* Sat Mar 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.6.8-1
- Update to 3.6.8

* Sun Feb 13 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.6.6-1
- Update to 3.6.6

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Nicolas Chauvet <kwizart@gmail.com> - 3.6.4-1
- Update to 3.6.4
- Disable libewf support - http://afflib.org/archives/75

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.5.12-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 3.5.12-1
- Update to 3.4.12

* Sun Apr 18 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 3.5.10-1
- Update to 3.5.10
- Remove upstreamed patch

* Tue Jan 19 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 3.5.7-1
- Update to 3.5.7

* Fri Nov 27 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 3.5.3-1
- Update to 3.5.3

* Tue Oct 27 2009 kwizart < kwizart at gmail.com > - 3.5.2-1
- Update to 3.5.2
- Remove upstreamed patch

* Thu Sep 24 2009 kwizart < kwizart at gmail.com > - 3.4.1-1
- Update to 3.4.1
- Update gcc43 (new case)
- Enable python binding.
- Avoid version-info on the python module.

* Wed Sep  2 2009 kwizart < kwizart at gmail.com > - 3.3.7-2
- Update to 3.3.7
- Update gcc44 patch

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.3.6-4
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 21 2009 kwizart < kwizart at gmail.com > - 3.3.6-2
- Update to 3.3.6
- Add BR python-devel
- Re-introduce gcc44 patch

* Tue May 12 2009 kwizart < kwizart at gmail.com > - 3.3.5-1
- Update to 3.3.5
- Remove afflib-3.3.4-WCtype.patch

* Mon Mar  2 2009 kwizart < kwizart at gmail.com > - 3.3.4-7
- Fix for gcc44

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 3.3.4-5
- rebuild with new openssl
- call libtoolize to refresh libtool

* Fri Oct  3 2008 kwizart < kwizart at gmail.com > - 3.3.4-4
- Fix release mismatch

* Fri Oct  3 2008 kwizart < kwizart at gmail.com > - 3.3.4-3
- Update to 3.3.4

* Mon Sep 15 2008 kwizart < kwizart at gmail.com > - 3.3.3-3
- Update to 3.3.3

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 3.3.2-2
- Update gcc43 patch

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 3.3.2-1
- Update to 3.3.2
- Remove Requires for ewftools from afftools
- Qemu image support is disabled

* Mon Sep  1 2008 kwizart < kwizart at gmail.com > - 3.3.1-1
- Update to 3.3.1

* Tue Jul 29 2008 kwizart < kwizart at gmail.com > - 3.2.5-3
- Patch with fuzz 2

* Thu Jul 24 2008 kwizart < kwizart at gmail.com > - 3.2.5-2
- Remove nos3 patch

* Thu Jul 24 2008 kwizart < kwizart at gmail.com > - 3.2.5-1
- Update to 3.2.5

* Fri Jul  4 2008 kwizart < kwizart at gmail.com > - 3.2.3-1
- Update to 3.2.3

* Thu Jun 26 2008 kwizart < kwizart at gmail.com > - 3.2.1-4
- Explicitely disable s3

* Thu Jun 26 2008 kwizart < kwizart at gmail.com > - 3.2.1-3
- Disable s3

* Wed Jun 25 2008 kwizart < kwizart at gmail.com > - 3.2.1-2
- Fix redefinition of typedef AFFILE

* Sat Jun  7 2008 kwizart < kwizart at gmail.com > - 3.2.1-1
- Update to 3.2.1

* Wed May 21 2008 kwizart < kwizart at gmail.com > - 3.2.0-1
- Update to 3.2.0

* Tue Apr 15 2008 kwizart < kwizart at gmail.com > - 3.1.6-1
- Update to 3.1.6

* Fri Mar 21 2008 kwizart < kwizart at gmail.com > - 3.1.3-4
- Fix typo

* Wed Mar 19 2008 kwizart < kwizart at gmail.com > - 3.1.3-3
- Add missing requires with pkgconfig

* Mon Mar 17 2008 kwizart < kwizart at gmail.com > - 3.1.3-2
- Rebuild with newer libewf and enable-libewf=yes
- Add pkg-config support in afflib-devel.
- Add a patch to remove ldconfig call when building the package.
- Add libtermcap-devel

* Wed Mar 12 2008 kwizart < kwizart at gmail.com > - 3.1.3-1
- Update to 3.1.3
- Disable libewf support in afflib for now.
- Disable rpath
- Fix for gcc43 and s3

* Fri Nov 30 2007 kwizart < kwizart at gmail.com > - 3.0.4-1
- Update to 3.0.4

* Sun Nov 18 2007 kwizart < kwizart at gmail.com > - 3.0.1-1
- Update to 3.0.1

* Fri Nov  2 2007 kwizart < kwizart at gmail.com > - 2.4.0-1
- Initial package for Fedora

