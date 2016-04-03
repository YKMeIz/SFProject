Summary:	Tool to check and undelete partition, PhotoRec recovers lost files
Summary(pl.UTF8):	Narzędzie sprawdzające i odzyskujące partycje
Summary(fr.UTF8):	Outil pour vérifier et restaurer des partitions
Summary(ru_RU.UTF8): Программа для проверки и восстановления разделов диска
Name:		testdisk
Version:	6.14
Release:	4%{?dist}
License:	GPLv2+
Group:		Applications/System
Source0:	http://www.cgsecurity.org/testdisk-%{version}.tar.bz2
Patch0:		http://www.cgsecurity.org/testdisk_614_docdir.patch
Patch1:		http://www.cgsecurity.org/testdisk_614_fix_ext2_check.patch
URL:		http://www.cgsecurity.org/wiki/TestDisk
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	e2fsprogs-devel
BuildRequires:	libjpeg-devel
BuildRequires:	ntfs-3g-devel
BuildRequires:	libewf-devel
BuildRequires:	zlib-devel
BuildRequires:	libuuid-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Obsoletes:	testdisk-doc < 6.12

%description
Tool to check and undelete partition. Works with FAT12, FAT16, FAT32,
NTFS, ext2, ext3, ext4, btrfs, BeFS, CramFS, HFS, JFS, Linux Raid, Linux
Swap, LVM, LVM2, NSS, ReiserFS, UFS, XFS.
PhotoRec is a signature based file recovery utility. It handles more than
440 file formats including JPG, MSOffice, OpenOffice documents.

%description -l pl.UTF8
Narzędzie sprawdzające i odzyskujące partycje. Pracuje z partycjami:
FAT12, FAT16, FAT32, NTFS, ext2, ext3, ext4, btrfs, BeFS, CramFS, HFS, JFS,
Linux Raid, Linux Swap, LVM, LVM2, NSS, ReiserFS, UFS, XFS.
PhotoRec is a signature based file recovery utility. It handles more than
440 file formats including JPG, MSOffice, OpenOffice documents.

%description -l fr.UTF8
TestDisk vérifie et récupère les partitions. Fonctionne avec
FAT12, FAT16, FAT32, NTFS, ext2, ext3, ext4, btrfs, BeFS, CramFS, HFS, JFS,
Linux Raid, Linux Swap, LVM, LVM2, NSS, ReiserFS, UFS, XFS.
PhotoRec utilise un mécanisme de signature pour récupérer des fichiers
perdus. Il reconnait plus de 440 formats de fichiers dont les JPEG, les
documents MSOffice ou OpenOffice.

%description -l ru_RU.UTF8
Программа для проверки и восстановления разделов диска.
Поддерживает следующие типы разделов:
FAT12, FAT16, FAT32, NTFS, ext2, ext3, ext4, btrfs, BeFS, CramFS, HFS, JFS,
Linux Raid, Linux Swap, LVM, LVM2, NSS, ReiserFS, UFS, XFS.
PhotoRec is a signature based file recovery utility. It handles more than
440 file formats including JPG, MSOffice, OpenOffice documents.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure
make %{?_smp_mflags}
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR="$RPM_BUILD_ROOT" install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS documentation.html
%attr(755,root,root) %{_bindir}/fidentify
%attr(755,root,root) %{_bindir}/photorec
%attr(755,root,root) %{_bindir}/testdisk
%{_mandir}/man8/fidentify.8*
%{_mandir}/man8/photorec.8*
%{_mandir}/man8/testdisk.8*
/usr/share/doc/testdisk/AUTHORS
/usr/share/doc/testdisk/ChangeLog
/usr/share/doc/testdisk/NEWS
/usr/share/doc/testdisk/README
/usr/share/doc/testdisk/THANKS
/usr/share/doc/testdisk/documentation.html


%changelog
* Thu Feb 27 2014 Kalev Lember <kalevlember@gmail.com> - 6.14-3
- Rebuilt for ntfs-3g soname bump

* Wed Nov 06 2013 Christophe Grenier <grenier@cgsecurity.org> - 6.14-2
- Patch for additional ext2 check (Bug #1027026)

* Mon Sep 09 2013 Christophe Grenier <grenier@cgsecurity.org> - 6.14-1
- Update to latest version http://www.cgsecurity.org/wiki/TestDisk_6.14_Release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 6.13-6
- Rebuilt for libewf

* Sun Jan 27 2013 Christophe Grenier <grenier@cgsecurity.org> - 6.13-5
- rebuild for new ntfs-3g

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 6.13-4
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 6.13-3
- rebuild against new libjpeg

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 12 2012 Christophe Grenier <grenier@cgsecurity.org> - 6.13-1
- Update to latest version

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Christophe Grenier <grenier@cgsecurity.org> - 6.12.2
- Rebuild for ntfs-3g

* Thu May 12 2011 Christophe Grenier <grenier@cgsecurity.org> - 6.12.1
- Update to latest version

* Sat Apr 16 2011 Christophe Grenier <grenier@cgsecurity.org> - 6.11-9
- Rebuild for ntfs-3g

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 27 2010 Christophe Grenier <grenier@cgsecurity.org> 6.11-7
- Move binaries to /usr/bin (#628050)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 6.11-6
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Christophe Grenier <grenier@cgsecurity.org> 6.11-4
- Add "BuildRequires:  libuuid-devel"

* Wed May  6 2009 Christophe Grenier <grenier@cgsecurity.org> 6.11-3
- Use upstream patch v2

* Fri Apr 24 2009 Christophe Grenier <grenier@cgsecurity.org> 6.11-2
- Add upstream patch that add missing bound checks when parsing EXIF information

* Sun Apr 19 2009 Christophe Grenier <grenier@cgsecurity.org> 6.11-1
- Update to latest version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 31 2008 Christophe Grenier <grenier@cgsecurity.org> 6.10-1
- Update to latest version

* Wed Mar 19 2008 Christophe Grenier <grenier@cgsecurity.org> 6.9-2
- Fix for new API in libewf > 20070512

* Wed Feb 13 2008 Christophe Grenier <grenier@cgsecurity.org> 6.9-1
- Update to latest version

* Mon Dec 10 2007 Christophe Grenier <grenier@cgsecurity.org> 6.8-6
- Don't disable libewf during compilation

* Mon Dec  3 2007 Christophe Grenier <grenier@cgsecurity.org> 6.8-5
- Don't require ntfsprogs-devel on ppc and ppc64

* Mon Dec  3 2007 Christophe Grenier <grenier@cgsecurity.org> 6.8-4
- Rename TestDisk list functions to avoid conflict with latest ntfsprogs-devel 2.0.0

* Sun Dec  2 2007 Christophe Grenier <grenier@cgsecurity.org> 6.8-3
- Use libewf for support of the Expert Witness Compression Format (EWF)

* Thu Aug 16 2007 Christophe Grenier <grenier@cgsecurity.org> 6.8-2
- Fix the license in the spec file

* Tue Aug 14 2007 Christophe Grenier <grenier@cgsecurity.org> 6.8-1
- Update to latest version

* Fri Jun 29 2007 Christophe Grenier <grenier@cgsecurity.org> 6.7-1
- Update to latest version

* Sun Feb 18 2007 Christophe Grenier <grenier@cgsecurity.org> 6.6-1
- Update to latest version

* Mon Feb 5 2007 Christophe Grenier <grenier@cgsecurity.org> 6.5-3
- Fix russian description in spec file

* Sun Nov 26 2006 Christophe Grenier <grenier@cgsecurity.org> 6.5-2
- Use ntfsprogs to provide NTFS listing capabilities to TestDisk

* Tue Oct 24 2006 Christophe Grenier <grenier@cgsecurity.org> 6.5-1
- Update to latest version

* Mon Aug 28 2006 Christophe Grenier <grenier@cgsecurity.org> 6.4-3
- Rebuild for Fedora Extras 6

* Wed Jun 21 2006 Christophe Grenier <grenier@cgsecurity.org> 6.4-2
- FC3 and FC4 has a release of 2, need to align

* Wed Jun 21 2006 Christophe Grenier <grenier@cgsecurity.org> 6.4-1
- Update to latest version

* Mon Mar  6 2006 Christophe Grenier <grenier@cgsecurity.org> 6.3-1
- Update to latest version

* Tue Feb 28 2006 ChangeLog Grenier <grenier@cgsecurity.org> 6.2-4
- Rebuild for Fedora Extras 5

* Mon Jan 23 2006 Christophe Grenier <grenier@cgsecurity.org> 6.2-3
- same spec for all arches hence add dist

* Sun Jan 4 2004 Christophe Grenier <grenier@cgsecurity.org> 5.0
- 5.0

* Wed Oct 1 2003 Christophe Grenier <grenier@cgsecurity.org> 4.5
- 4.5

* Wed Apr 23 2003 Christophe Grenier <grenier@cgsecurity.org> 4.4-2

* Sat Mar 29 2003 Pascal Terjan <CMoi@tuxfamily.org> 4.4-1mdk
- 4.4

* Fri Dec 27 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.2-2mdk
- rebuild for rpm and glibc

* Sun Oct 06 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.2-1mdk
- 4.2

* Mon Sep 02 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 4.1-1mdk 
- By Pascal Terjan <pascal.terjan@free.fr>
	- first mdk release, adapted from PLD.
	- gz to bz2 compression.
- fix %%tmppath
- %%make instead %%{__make}
