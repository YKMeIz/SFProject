Name:		f2fs-tools
Version:	1.4.1
Release:	2%{?dist}
Summary:	Tools for Flash-Friendly File System (F2FS)
License:	GPLv2+
URL:		http://sourceforge.net/projects/f2fs-tools/
Source0:	http://git.kernel.org/cgit/linux/kernel/git/jaegeuk/f2fs-tools.git/snapshot/%{name}-%{version}.tar.gz
Patch0:		f2fs-tools-1.4.0-bigendian.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	uuid-devel
BuildRequires:	libuuid-devel
BuildRequires:	libtool

%description
NAND flash memory-based storage devices, such as SSD, and SD cards,
have been widely being used for ranging from mobile to server systems. 
Since they are known to have different characteristics from the 
conventional rotational disks,a file system, an upper layer to 
the storage device, should adapt to the changes
from the sketch.

F2FS is a new file system carefully designed for the 
NAND flash memory-based storage devices. 
We chose a log structure file system approach,
but we tried to adapt it to the new form of storage. 
Also we remedy some known issues of the very old log
structured file system, such as snowball effect 
of wandering tree and high cleaning overhead.

Because a NAND-based storage device shows different characteristics 
according to its internal geometry or flash memory management 
scheme aka FTL, we add various parameters not only for configuring 
on-disk layout, but also for selecting allocation
and cleaning algorithms.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?isa} = %{version}-%{release}
%description devel
This package contains the libraries needed to develop applications
that use %{name}

%prep
%setup -q
%patch0 -p1 -b .bigendian
sed -i 's/AC_PROG_LIBTOOL/LT_INIT/' configure.ac

%build
autoreconf --install
%configure \
	--disable-static
make %{?_smp_mflags}


%install
make DESTDIR=%{buildroot} INSTALL="install -p" CP="cp -p" sbindir=%{_sbindir} install
mkdir -m 755 -p %{buildroot}%{_includedir}
install -m 644 include/f2fs_fs.h %{buildroot}%{_includedir}
install -m 644 mkfs/f2fs_format_utils.h %{buildroot}%{_includedir}
rm -f %{buildroot}/%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING AUTHORS ChangeLog
%{_sbindir}/mkfs.f2fs
%{_sbindir}/fibmap.f2fs
%{_sbindir}/fsck.f2fs
%{_sbindir}/dump.f2fs
%{_sbindir}/parse.f2fs
%{_sbindir}/f2fstat
%{_libdir}/*.so.*
%{_mandir}/man8/mkfs.f2fs.8*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 8  2015 Eduardo Echeverria  <echevemaster@gmail.com> - 1.4.1-1
- Updated to 1.4.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 03 2015 Dan Horák <dan[at]danny.cz> - 1.4.0-3
- fix build on big endian arches

* Fri Dec 26 2014 Jonathan Dieter <jdieter@lesbg.com> - 1.4.0-2
- Add missing header to development package

* Thu Dec 25 2014 Eduardo Echeverria  <echevemaster@gmail.com> - 1.4.0-1
- Update to the latest upstream version

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 19 2014 Eduardo Echeverria  <echevemaster@gmail.com> - 1.2.0-1
- Update to the latest upstream version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 1.1.0-2
- Minor fix in the changelogs

* Mon Mar 18 2013 Eduardo Echeverria  <echevemaster@gmail.com> - 1.1.0-1
- Updated to the new upstream release

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 22 2012 Eduardo Echeverria  <echevemaster@gmail.com> - 1.0.0-3
- Change to the correct license GPLv2+
- Remove README file to the section doc

* Mon Oct 15 2012 Eduardo Echeverria  <echevemaster@gmail.com> - 1.0.0-2
- Add Changelog AUTHORS files to section doc
- Add wilcard to the manpages section.

* Sun Oct 07 2012 Eduardo Echeverria  <echevemaster@gmail.com> - 1.0.0-1
- Initial packaging
