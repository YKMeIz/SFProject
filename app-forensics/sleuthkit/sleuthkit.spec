# Could be part of http://fedoraproject.org/wiki/LukeMacken/SecurityLiveCD

Name:           sleuthkit
Version:        4.1.3
Release:        4%{?dist}
Summary:        The Sleuth Kit (TSK)

Group:          Applications/System
License:        CPL and IBM and GPLv2+
URL:            http://www.sleuthkit.org
Source0:        http://downloads.sourceforge.net/sleuthkit/sleuthkit-%{version}.tar.gz
Patch0:         %{name}-4.1.3-system-sqlite.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  libtool

# afflib - BSD with advertising, GPL incompatible
BuildRequires:  afflib-devel >= 3.3.4
# libewf - Newer versions are plain BSD (older are BSD with advertising)
BuildRequires:  libewf-devel
BuildRequires:  sqlite-devel

%{?_with_java:
BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils

Requires:       java >= 1:1.6.0
Requires:       jpackage-utils
}

Requires: %{name}-libs = %{version}-%{release}
Requires: file
Requires: mac-robber

%description
The Sleuth Kit (TSK) is a collection of UNIX-based command line tools that
allow you to investigate a computer. The current focus of the tools is the
file and volume systems and TSK supports FAT, Ext2/3, NTFS, UFS,
and ISO 9660 file systems


%package        libs
Summary:        Library for %{name}
Group:          System Environment/Libraries

%description    libs
The %{name}-libs package contains library for %{name}.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.



%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .system-sqlite
for file in $(find . -name "*.system-sqlite"); do
    touch -r $file ${file%.system-sqlite}
done
rm tsk/auto/sqlite3.[hc]


# re-run autotools
%if 0
libtoolize  --force
aclocal
autoheader
autoconf
automake
%endif


%build
export LIBS='-lpthread -ldl'
%configure --disable-static

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# clean unused-direct-shlib-dependencies
#sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'



%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig



%files
%defattr(-,root,root,-)
%doc ChangeLog.txt NEWS.txt README.txt licenses/*
# License is CPL 1.0 exept for some files.
%{_bindir}/blkcalc
%{_bindir}/blkcat
%{_bindir}/blkls
%{_bindir}/blkstat
#{_bindir}/disk_sreset
#{_bindir}/disk_stat
#fcat conflicts with freeze fcat
%exclude %{_bindir}/fcat
%{_bindir}/ffind
%{_bindir}/fiwalk
%{_bindir}/fls
%{_bindir}/fsstat
%{_bindir}/hfind
%{_bindir}/icat
%{_bindir}/ifind
%{_bindir}/ils
%{_bindir}/img_cat
%{_bindir}/img_stat
%{_bindir}/istat
%{_bindir}/jcat
%{_bindir}/jpeg_extract
%{_bindir}/jls
# This file is described as GPL in the doc
# But the license remains CPL in the source.
%{_bindir}/mactime
##
%{_bindir}/mmcat
%{_bindir}/mmls
%{_bindir}/mmstat
%{_bindir}/sigfind
%{_bindir}/sorter
## This file is GPLv2+
%{_bindir}/srch_strings
%{_bindir}/tsk_comparedir
%{_bindir}/tsk_gettimes
%{_bindir}/tsk_loaddb
%{_bindir}/tsk_recover
#
%{_mandir}/man1/blkcalc.1*
%{_mandir}/man1/blkcat.1*
%{_mandir}/man1/blkls.1*
%{_mandir}/man1/blkstat.1*
#{_mandir}/man1/disk_sreset.1*
#{_mandir}/man1/disk_stat.1*
%{_mandir}/man1/ffind.1*
%{_mandir}/man1/fls.1*
%{_mandir}/man1/fsstat.1*
%{_mandir}/man1/hfind.1*
%{_mandir}/man1/icat.1*
%{_mandir}/man1/ifind.1*
%{_mandir}/man1/ils.1*
%{_mandir}/man1/img_cat.1*
%{_mandir}/man1/img_stat.1*
%{_mandir}/man1/istat.1*
%{_mandir}/man1/jcat.1*
%{_mandir}/man1/jls.1*
%{_mandir}/man1/mactime.1*
%{_mandir}/man1/mmcat.1*
%{_mandir}/man1/mmls.1*
%{_mandir}/man1/mmstat.1*
%{_mandir}/man1/sigfind.1*
%{_mandir}/man1/sorter.1*
%{_mandir}/man1/tsk_comparedir.1*
%{_mandir}/man1/tsk_gettimes.1*
%{_mandir}/man1/tsk_loaddb.1*
%{_mandir}/man1/tsk_recover.1*
%dir %{_datadir}/tsk
%{_datadir}/tsk/sorter/

%files libs
%defattr(-,root,root,-)
# CPL and IBM
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
# CPL and IBM
%{_includedir}/tsk/
%{_libdir}/*.so

%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 18 2014 Ville Skyttä <ville.skytta@iki.fi> - 4.1.3-2
- Use system sqlite instead of bundled one

* Wed Feb 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 4.1.3-1
- Update to 4.1.3

* Thu Oct 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1
- Update to 4.1.2

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 4.1.0-2
- Perl 5.18 rebuild

* Wed Jul 24 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.1.0-1
- Update to 4.1.0

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.0.2-3
- Perl 5.18 rebuild

* Fri Mar 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.0.2-2
- Rebuilt for libewf

* Thu Feb 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.0.2-1
- Update to 4.0.2

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.0.1-1
- Update to 4.0.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.2.3-1
- Update to 3.2.3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.2.2-1
- Update to 3.2.2

* Sun Mar 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.2.1-1
- Update to 3.2.1

* Sun Feb 13 2011 Nicolas Chauvet <kwizart@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 29 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 kwizart < kwizart at gmail.com > - 3.0.1-1
- Update to 3.0.1 (final)

* Tue Oct 28 2008 kwizart < kwizart at gmail.com > - 3.0.0-1
- Update to 3.0.0 (final)

* Fri Oct  3 2008 kwizart < kwizart at gmail.com > - 3.0.0-0.1.b4
- Update to 3.0.0b4

* Tue Jun 17 2008 kwizart < kwizart at gmail.com > - 2.52-1
- Update to 2.52
- Remove merged patches
- Remove clean unused-direct-shlib-dependencies 
- Fix rpath at source.
- Sort license within the spec
- Move configure.ac to pkg-config detection
- Remove Perl-Date-Manip installation

* Tue Mar 18 2008 kwizart < kwizart at gmail.com > - 2.51-1
- Update to 2.51
- Add libewf/afflib BR
- Requires mac-robber external package.
- Remove internal perl-Date-Manip.

* Fri Dec 28 2007 kwizart < kwizart at gmail.com > - 2.10-1
- Update to 2.10

* Mon Oct 29 2007 kwizart < kwizart at gmail.com > - 2.09-1
- Initial package for Fedora 
  (inspired from Oden Eriksson mdk spec).


