# To use git, follow:
#
# git clone git://git.gnome.org/gnome-commander
# cd gnome-commander/
# git checkout -b gcmd-1-3 origin/gcmd-1-3
# git pull
# ...
# cd ..
# ln -sf gcmd-commander gnome-commander-%%{version}-git_%%{git_pull_JST}
# tar cjf gnome-commander-%%{version}-git_%%{git_pull_JST}.tar.xz \
#    gnome-commander-%%{version}-git_%%{git_pull_JST}/./

# Source10 is created by:
# svn co http://svn.gnome.org/svn/gnome-commander/branches/gcmd-1-3/tools/mimeedit/
# cp -p mimeedit/mimeedit.sh mimeedit-rev%%{mimeedit_rev}.sh
#
# ref: http://lists.gnu.org/archive/html/gcmd-devel/2007-11/msg00076.html

%global        EXIV2_REQ             0.14
%global        TAGLIB_REQ            1.4
%global        LIBGSF_REQ            1.12.0
%global        POPPLER_REQ           0.8

%global        git_pull_JST          D20090629T1400

%global        use_autotool          0
%global        update_po             0
%global        if_pre                0
%global        main_release          1
%global        extratag              git_%{git_pull_JST}
%undefine      extratag
%global        mimeedit_rev          1958

%if 0%{?if_pre} > 0
%global        use_autotool          1
%endif
%if 0%{?use_autotool} < 1
%global        update_po             0
%endif

# Patch1 updates configure.in
%global        use_autotool          1

# Autotool seems still needed to avoid build failure
# under doc/ diretory, need investigating
%global        use_autotool          1

%global        fedora_rel            %( [ 0%{?if_pre} -gt 0 ] && echo 0. )%{main_release}%{?extratag:.%extratag}

Name:          gnome-commander
Version:       1.4.4
# Downgrade 3 times, sorry...
Epoch:         4
Release:       %{fedora_rel}%{?dist}
Summary:       A nice and fast file manager for the GNOME desktop
Summary(pl):   Menadżer plików dla GNOME oparty o Norton Commander'a (TM)
Summary(sv):   GNOME Commander är en snabb och smidig filhanderare för GNOME

Group:         Applications/File
License:       GPLv2+
URL:           http://gcmd.github.io/
Source0:       ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/1.4/%{name}-%{version}%{?extratag:-%extratag}.tar.xz
Source1:       gnome-commander.sh
Source10:      mimeedit-svn%{mimeedit_rev}.sh
Patch10:       mimeedit-svn1958.diff
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: scrollkeeper

BuildRequires: chmlib-devel
BuildRequires: pkgconfig(exiv2)         >= %{EXIV2_REQ}
BuildRequires: pkgconfig(gnome-keyring-1)
BuildRequires: pkgconfig(gnome-vfs-2.0)
BuildRequires: pkgconfig(libgsf-1)        >= %{LIBGSF_REQ}
BuildRequires: pkgconfig(libgnome-2.0)
BuildRequires: pkgconfig(libgnomeui-2.0)
BuildRequires: pkgconfig(poppler-glib)       >= %{POPPLER_REQ}
BuildRequires: pkgconfig(taglib)        >= %{TAGLIB_REQ}
BuildRequires: pkgconfig(unique-1.0)

BuildRequires: libICE-devel
BuildRequires: libSM-devel

BuildRequires: gnome-doc-utils
BuildRequires: perl(XML::Parser)
BuildRequires: python-devel

%if %{use_autotool}
BuildRequires: automake
BuildRequires: flex
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: gnome-common
%endif

Requires:         gnome-python2-gnomevfs
Requires:         gnome-vfs2-smb
Requires:         meld

%description
GNOME Commander is a nice and fast file manager for the GNOME desktop. 
In addition to performing the basic filemanager functions the program is 
also an FTP-client and it can browse SMB-networks.

%description -l cs
GNOME Commander je pěkný a rychlý správce souborů pro GNOME desktop.
Kromě základních funkcí správy souborů je program také
FTP klient a umí procházet SMB sítěmi.

%description -l pl
GNOME Commander to niewielki i wydajny menadżer plików umożliwiający
wykonywanie za pomocą klawiatury wszystkich standardowych operacji na plikach.
Dostępne są również dodatkowe funkcje jak np. obsługa FTP, czy też obsługa
sieci SMB.

%description -l ru
Быстро работающий файловый менеджер для GNOME. Может выполнять большинство
типовых операций с файлами, умеет обнаруживать изменения, внесенные в файлы
другими программами, и автоматически обновлять отображаемый список файлов.
Поддерживает описания файловых структур в формате DND и кодировки MIME.
Реализует на базовом уровне поддержку FTP через GnomeVFS.

%description -l sv
GNOME Commander är en snabb och smidig filhanderare för GNOME.
Utöver att kunna hantera filer på din egen dator så kan programmet även
ansluta till FTP-servrar och SMB-nätverk.

%prep
%setup -q -n %{name}-%{version}%{?extratag:-%extratag}

%if 0%{use_autotool} > 0
( export NOCONFIGURE=1 ; sh autogen.sh )
%endif

#%{__cp} -p %SOURCE10 mimeedit.sh
#%%patch10 -p0

%{__sed} -i.pylib \
   -e 's|\$PY_EXEC_PREFIX/lib|%{_libdir}|' \
   configure

# gzip
gzip -9 ChangeLog-*

%build
# Install wrapper script, and move binaries to
# %%{_libexecdir}/%%{name}
mkdir _builddir || :

# For debuginfo issue
find . -name \*.cc | while read f
do
   dirn=$(dirname $f)
   %{__cat} $f | %{__sed} -n -e 's|^#line.*[ \t][ \t]*\"\(.*\)"$|\1|p' | \
      sort | uniq | while read g
   do
      %{__mkdir_p} _builddir/$dirn
      %{__cp} -p $dirn/$g _builddir/$dirn
  done
done

pushd _builddir

ln -sf ../configure
%configure \
   --srcdir=$(pwd)/.. \
   --bindir=%{_libexecdir}/%{name} \
   --disable-scrollkeeper \
   --enable-python

%{__cp} -p README ..

%if %{update_po}
%{__make} -C po gnome-commander.pot update-po
%endif

# First make po without _smp_mflags, so that messages
# won't be mixed up
# Second doc/, parallel make seems to fail
%{__make} -C po GMSGFMT="msgfmt --statistics"
%{__make} -C doc
%{__make} %{?_smp_mflags} -k

popd # from _builddir

%install
%{__rm} -rf %{buildroot}

pushd _builddir
%{__make} \
   INSTALL="%{__install} -c -p" \
   DESTDIR=%{buildroot} \
   install
popd # from _builddir

# Desktop file
desktop-file-install \
   --delete-original \
   --vendor '' \
   --remove-category Application \
   --dir %{buildroot}%{_datadir}/applications \
   %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install wrapper
%{__mkdir_p} %{buildroot}%{_bindir}
%{__install} -cpm 0755 %SOURCE1 %{buildroot}%{_bindir}/%{name}

# install gnome-file-types-properties (bug 458667)
%if 0
%{__install} -cpm 0755 mimeedit.sh \
	%{buildroot}%{_libexecdir}/%{name}/gnome-file-types-properties
%endif

%{__rm} -f %{buildroot}%{_libdir}/%{name}/*.{a,la}
%{__rm} -f %{buildroot}%{_libdir}/%{name}/*/*.{a,la}

%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS
%doc BUGS
%doc ChangeLog*
%doc COPYING
%doc NEWS
%doc README
%doc README.commits
%doc TODO
%doc doc/*.txt

%{_bindir}/*
%{_libexecdir}/%{name}/
%{_libdir}/%{name}/
%{_mandir}/man1/%{name}.1*

%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml

%{_datadir}/gnome/help/%{name}/
%{_datadir}/omf/%{name}/

%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}/

%changelog
* Thu Nov 13 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.4-1
- Update to 1.4.4

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4:1.4.3-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 25 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.3-1
- Update to 1.4.3

* Thu Jun 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.2-2
- F-21: mass rebuild

* Mon May 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.2-1
- Update to 1.4.2

* Mon May 26 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.1-3
- Remove no longer supported mimetype configuration

* Fri Apr 11 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.1-2
- F21 gcc49 rebuild

* Mon Apr 07 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.1-1
- Update to  1.4.1

* Wed Mar 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.0-2
- Fix build error on armv7fl about missing vtable

* Tue Mar 18 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.4.0-1
- Update to 1.4.0

* Tue Jan 14 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.2.8.17-1
- Update to 1.2.8.17

* Thu Dec 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.2.8.16-1
- Update to 1.2.8.16

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 4:1.2.8.15-12.1
- rebuild (exiv2)

* Tue Dec  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.2.8.15-12
- Support -Werror=format-security

* Sat Aug 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.2.8.15-11
- Patch to compile with poppler 0.24.0

* Mon Aug 19 2013 Marek Kasik <mkasik@redhat.com> - 4:1.2.18.15-10
- Rebuild (poppler-0.24.0)

* Wed Aug  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.2.18.15-9
- F-20: mass rebuild

* Mon Jul  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4:1.2.18.15-8
- F-20: rebuild (poppler)
- Patch to build against libgsf 1.14.26

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.2.8.15-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jan 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3:1.2.8.15-8
- Fix additional build error with gcc47

* Fri Jan 18 2013 Marek Kasik <mkasik@redhat.com> - 3:1.2.8.15-7
- Rebuild (poppler-0.22.0)

* Mon Aug  6 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3:1.2.8.15-6
- F-18: Mass rebuild

* Mon Jul  2 2012 Marek Kasik <mkasik@redhat.com> - 3:1.2.8.15-5
- Rebuild (poppler-0.20.1)

* Fri May 18 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3:1.2.8.15-4
- Patch to compile with poppler 0.20.0
  (bug 822405: patch by Marek Kašík [mkasik@redhat.com])

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 3:1.2.8.15-3
- rebuild (exiv2)

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3:1.2.8.15-2
- F-17: rebuild against gcc47

* Wed Dec  7 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3:1.2.8.15-1
- Update to 1.2.8.15

* Fri Oct 28 2011 Rex Dieter <rdieter@fedoraproject.org> - 3:1.2.8.14-1.2
- rebuild(poppler)

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 3:1.2.8.14-1.1
- rebuild (exiv2)

* Sun Oct  9 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3:1.2.8.14-1
- Update to 1.2.8.14

* Fri Sep 30 2011 Marek Kasik <mkasik@redhat.com> - 3:1.2.8.13-3
- Rebuild (poppler-0.18.0)

* Mon Sep 19 2011 Marek Kasik <mkasik@redhat.com> - 3:1.2.8.13-2
- Rebuild (poppler-0.17.3)

* Sun Aug  7 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3:1.2.8.13-1
- Update to 1.2.8.13

* Fri Jul 15 2011 Marek Kasik <mkasik@redhat.com> - 3:1.2.8.12-2
- Rebuild (poppler-0.17.0)

* Sat Jun 18 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3:1.2.8.12-1
- Update to 1.2.8.12

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 3:1.2.8.11-1
- Update to 1.2.8.11

* Sun Mar 13 2011 Marek Kasik <mkasik@redhat.com> - 3:1.2.8.10-3
- Rebuild (poppler-0.16.3)

* Mon Feb 14 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3:1.2.8.10-2
- F-15 mass rebuild

* Thu Jan 20 2011 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3:1.2.8.10-1
- Update to 1.2.8.10

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 3:1.2.8.9-1.2
- rebuild (exiv2,poppler)

* Wed Dec 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 3:1.2.8.9-1.1
- rebuild (poppler)

* Sat Dec  4 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3:1.2.8.9-1
- Update to 1.2.8.9

* Sun Nov 7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-15: rebuild against new poppler

* Sat Oct  2 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3:1.2.8.8-3
- Add more explicit BRs
- F-15: rebuild against newer poppler

* Fri Sep 10 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3:1.2.8.8-1
- Update to 1.2.8.8
- Fix parallel make issue

* Thu Aug 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 3:1.2.8.7-1.1
- rebuild (poppler)

* Fri Jul 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3:1.2.8.7-1
- Update to 1.2.8.7

* Fri Jul 23 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-14: rebuild against python 2.7

* Sat Jun 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 3:1.2.8.6-1
- Finally downgrade to 1.2.8.6 even on rawhide as the upsteam changed release plan

* Mon May 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 2:1.2.9-0.6.git_D20100215T0000
- rebuild (exiv2)

* Wed May 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Bump Epoch again to keep upgrade path from F-13

* Wed May  5 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.9-0.4.git_D20100215T0000
- Rebuild against new poppler

* Mon Feb 15 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Again try latest git

* Thu Jan 14 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.9-0.3.git_D20100114T1630
- Update to the latest git
- Add Requires: gnome-vfs2-smb (from a request from the upstream)

* Mon Jan  4 2010 Rex Dieter <rdieter@fedoraproject.org> 1:1.2.9-0.2
- rebuild (exiv2)

* Fri Jan  1 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- A Happy New Year

* Thu Dec  3 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Update to the latest git
  (to fix crash when cancelling symlink creation with ESC
   bug 542366, GNOME bug 603301)

* Thu Nov 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.2.9-0.1.git_D20091126T1510
- Chase master git branch for F-13 after discussion with the upstream
  developer

* Thu Nov 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.2.8.3-1
- Use stable 1.2.8.x branch for F-12 after discussion with
  the upstream developer

* Mon Sep 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Try latest git

* Sat Sep 26 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3-0.3.git_D20090924T0215_13dev
- Update Russian translation (from mailing list)

* Thu Sep 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Try latest git

* Tue Jul 28 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-12: Mass rebuild

* Tue Jun 23 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Try latest git

* Mon May 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3-0.2.git_D20090524T2355_13dev
- Upstream moved to git

* Sat Apr 11 2009 Mamour Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3-0.1.svn2532_13dev
- rev 2532

* Thu Apr  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.3-0.1.svn2502_13dev
- F-12: switch to 1.3 development branch

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-11: Mass rebuild

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org>
- respin (exiv2)

* Thu Dec 18 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 2361

* Sat Dec  6 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 2332
- libtool 2.2 patch went upstream
- "replace_icon" hack seems no longer needed

* Thu Dec  4 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 2330
- Add patch to compile with libtool 2.2
- And also compile with python 2.6

* Mon Oct 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- 1.2.8 branch
- rev 2221

* Wed Aug 13 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.7-4
- More fix for mimeedit.sh to remove potentially unsafe tmpfile
  creation

* Tue Aug 12 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.7-3
- Install mimeedit script pulled from svn to support mime edit
  menu (bug 458667)

* Wed Jul 30 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.7-2
- F-10+: Fix icon name due to gnome-icon-theme 2.23.x change

* Wed Jul 30 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.7-1
- 1.2.7

* Wed Jul 23 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1901
- Previous workaround removed

* Mon Jul 14 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1874
- Workaround for Decimal offset mode in Hexdump display mode

* Fri Jul 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- try rev 1870
- ja.po is merged upstream

* Wed Jun 25 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.2.6-3 
- respin for exiv2

* Mon Jun  2 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.6-2
- 1.2.6
- Add patch to compile with GTK 2.13.X

* Sat Mar  1 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.5-1
- 1.2.5

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43

* Fri Oct  5 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-4
- Drop yelp dependency

* Wed Aug 22 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-3.dist.2
- Mass rebuild (buildID or binutils issue)

* Fri Aug  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-3.dist.1
- License update

* Mon Jun 11 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-3
- Drop dependency for yelp

* Sat Jun  9 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-2
- Add missing BR libgsf-devel

* Sat Jun  9 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.4-1
- Update to 1.2.4
- Support python chmlib libiptcdata

* Sat Jun  9 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-7
- Require yelp (#243392)

* Tue Apr 17 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-6
- Add maintainer, description elements to gnome-commander.xml for
  newer libxslt

* Tue Jan 20 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-5
- Require meld (#225324)

* Thu Jan 11 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-4
- Don't remove plugins (#222203)

* Thu Jan  4 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-3
- Explicitly require version-dependent libraries accroding to
  the request from upstream.

* Thu Dec 21 2006 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.3-2
- Clean up.

* Tue Nov 14 2006 Piotr Eljasiak <epiotr@use.pl>
- fixed Source0 address

* Mon Jul 17 2006 Piotr Eljasiak <epiotr@use.pl>
- added glib dependencies

* Sun May 14 2006 Stephanos Manos <stefmanos@gmail.com>
- Fixed Scrollkeeper database update
        -disabled scrollkeeper update from make
        -added scrollkeeper-database-update in the %%post & %%postun section
- Added %%post & %%postun entries for the desktop file
- Added %%post & %%postun entries for the gtk+ icon cache file

* Sun Apr 9 2006 Piotr Eljasiak <epiotr@use.pl>
- minor cleanups

* Thu Mar 5 2006 Piotr Eljasiak <epiotr@use.pl>
- added OMF files

* Mon Feb 13 2006 Piotr Eljasiak <epiotr@use.pl>
- install gnome-commander icon to %%{_datadir}/pixmaps/
- install gnome-commander.1* to %%{_mandir}/man1/

* Sat Feb 11 2006 Piotr Eljasiak <epiotr@use.pl>
- set default srcext to .bz2

* Fri Jan 28 2005 Piotr Eljasiak <epiotr@use.pl>
- fixed typo: rpm --> rpmbuild

* Mon May 03 2004 Piotr Eljasiak <epiotr@use.pl>
- converted spec file to utf-8
- used RPM macros a bit more

* Thu Jun 19 2003 Piotr Eljasiak <epiotr@use.pl>
- added libraries

* Tue Mar 25 2003 Piotr Eljasiak <epiotr@use.pl>
- updated Sources

* Mon Jan 20 2003 Piotr Eljasiak <epiotr@use.pl>
- added build dependencies

* Fri Jan 10 2003 Piotr Eljasiak <epiotr@use.pl>
- added localization

* Thu Jan 09 2003 Piotr Eljasiak <epiotr@use.pl>
- added dependencies

* Mon Jun 24 2002 Piotr Eljasiak <epiotr@use.pl>
- more cleanup in install section

* Sat Jun 15 2002 Piotr Eljasiak <epiotr@use.pl>
- simplified install and files sections

* Mon Jun 10 2002 Piotr Eljasiak <epiotr@use.pl>
- .spec file is now generated from .spec.in

* Mon Jun 10 2002 Marcus Bjurman <marbj499@student.liu.se>
- The default icon for this project is now called gnome-commander.png
  The xpm variant of the same icon is now also renamed in the same manner.

* Sat Mar  9 2002 Marcus Bjurman <marbj499@student.liu.se>
- Pumped up the version nr

* Sun Nov  4 2001 Marcus Bjurman <marbj499@student.liu.se>
- Initial build.
