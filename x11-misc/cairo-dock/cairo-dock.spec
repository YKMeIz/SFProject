%global	urlver		3.4
%global	mainver	3.4.1

%global	plugin_least_ver	3.4.1

Name:			cairo-dock
Version:		3.4.1
Release:		3%{?dist}
Summary:		Light eye-candy fully themable animated dock

License:		GPLv3+
URL:			http://glx-dock.org/
# Source0:		http://launchpad.net/cairo-dock-core/%%{urlver}/%%{mainver}/+download/cairo-dock-%%{mainver}.tar.gz
# Modified due to some may-be-patent-infringement issue
Source0:		cairo-dock-fedora-%{version}.tar.gz
# Source0 is created by Source1
Source1:		cairo-dock-create-fedora-tarball.sh
# And some legal explanation
Source2:		LEGAL.fedora.cairo-dock

BuildRequires:	cmake

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gthread-2.0)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xrender)
BuildRequires:	pkgconfig(xtst)

Requires:	%{name}-core%{?isa} = %{version}-%{release}
Requires:	%{name}-plug-ins%{?isa} >= %{plugin_least_ver}
# Per upstream's request, install the below by default
Requires:	%{name}-plug-ins-xfce%{?isa} >= %{plugin_least_ver}
Requires:	%{name}-plug-ins-kde%{?isa} >= %{plugin_least_ver}

%description
This is a metapackage for installing all default packages
related to cairo-dock.

%package	libs
Summary:	Library files for %{name}

%description	libs
This package contains library files for %{name}.

%package	core
Summary:	Core files for %{name}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
# Requires related to commands used internally
# in cairo-dock
Requires:	findutils
Requires:	curl
Requires:	xterm
# Ancient Obsoletes (and no provides)
Obsoletes:	%{name}-plug-ins-gecko < %{version}-%{release}
Obsoletes:	%{name}-themes < %{version}-%{release}

%description	core
An light eye-candy fully themable animated dock for any 
Linux desktop. It has a family-likeness with OSX dock,
but with more options.

This is the core package of cairo-dock.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%prep
%setup -q

## permission
# %%_fixperms cannot fix permissions completely here
for dir in */
do
	find $dir -type f | xargs chmod 0644
done
chmod 0644 [A-Z]*
chmod 0755 */

# cmake issue
sed -i.debuglevel \
	-e '\@add_definitions@s|-O3|-O2|' \
	CMakeLists.txt
sed -i.stat \
	-e 's|\${MSGFMT_EXECUTABLE}|\${MSGFMT_EXECUTABLE} --statistics|' \
	po/CMakeLists.txt

%build
rm -f CMakeCache.txt
%cmake -DCMAKE_SKIP_RPATH:BOOL=ON .
make %{?_smp_mflags}

%install
%make_install \
	INSTALL="install -c -p"
chmod 0755 ${RPM_BUILD_ROOT}%{_libdir}/lib*.so.*

## Desktop files
for f in $RPM_BUILD_ROOT%{_datadir}/applications/*desktop
do
	desktop-file-validate $f
done

%find_lang %{name}

# Cleanups
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/ChangeLog.txt

# Collect docment files
rm -rf documents licenses
mkdir documents licenses
install -cpm 644 \
	ChangeLog \
	data/ChangeLog*.txt \
	documents/

install -cpm 644 \
	LGPL-2 \
	LICENSE \
	copyright \
	%{SOURCE2} \
	licenses/

# Just to suppress rpmlint...
pushd $RPM_BUILD_ROOT
for f in \
	`find ./%{_datadir}/%{name} -name \*.desktop` \
	`find . -name \*.conf`
	do
		sed -i -e '1i\ ' $f
	done
popd

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files

%files	libs
%license	licenses/*

%{_libdir}/libgldi.so.3*
%dir	%{_datadir}/%{name}/
%dir	%{_datadir}/%{name}/plug-ins/
%dir	%{_libdir}/%{name}/

%files	core -f %{name}.lang
%doc	documents/*

%{_bindir}/*%{name}*
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/pixmaps/%{name}.svg

%{_datadir}/%{name}/*.conf
%{_datadir}/%{name}/*.desktop
%{_datadir}/%{name}/*.svg
%{_datadir}/%{name}/images/
%{_datadir}/%{name}/*view
#%%{_datadir}/%%{name}/emblems/
%{_datadir}/%{name}/explosion/
%{_datadir}/%{name}/gauges/
%{_datadir}/%{name}/icons/
%{_datadir}/%{name}/scripts/
%dir	%{_datadir}/%{name}/themes/

%{_datadir}/%{name}/themes/Default-Panel/
%{_datadir}/%{name}/themes/Default-Single/

%{_libdir}/%{name}/libcd-Help.so
%{_datadir}/%{name}/plug-ins/Help/

%{_mandir}/man1/%{name}.1*

%files	devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/libgldi.so
%{_libdir}/pkgconfig/gldi.pc

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar  5 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.1-1
- 3.4.1

* Sat Feb 28 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-11
- Bump release

* Tue Jan 20 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-10
- Move license files to -libs
- Add an explanation text for legal issue

* Thu Jan  1 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-9
- Split out -core and -plug-ins srpm
- Remove may-be-patent-infringement part
- Create libs subpackage

* Tue Dec 30 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-8
- Make -kde, -xfce installed as default, per request from
  the upstream (no extra dependency will be added)

* Mon Dec 29 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-7
- Build unstable plug-ins (except for KDE experimental)
  (not installed by default option)

* Mon Dec 29 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-6
- Enable vala interface

* Sat Dec 20 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-5
- Make plug-ins depending on python(2), due to cairo-dock-launcher-API-daemon
  dependency (bug 3470)

* Fri Dec 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-4
- Add Dbus demos

* Fri Dec 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-3
- Build ruby

* Fri Dec 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-2
- Build Messaging-Menu, Status-Notifier

* Mon Dec  1 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-1
- 3.4.0

* Sun Aug 24 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-3
- F-21: rebuild against new upower

* Mon Jun 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-2
- Fix build with upower 0.99

* Mon Jun 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-1
- Update to 3.3.2

* Sat Apr 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 3.2.1-2.1
- Rebuilt for libgcrypt

* Mon Jul  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org>
- F-20: rebuid against new libical

* Mon Apr 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1

* Fri Apr 12 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.0.2-2.1
- Mass rebuilt for Fedora 19 Features

* Thu Dec 21 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.0.2-2
- Update plug-ins to 2.1

* Mon Dec 12 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.0.2-1
- 2.4.0-2

* Tue Nov  8 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0.3-3
- Rebuilt

* Wed Sep 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0.3-2.1
- Rebuilt for libgnome-menu

* Sun Jul 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- Rebuild against new libetpan

* Tue Jun 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0.3-1
- 2.3.0-3

* Sun Jun  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0.2.1-2
- core 2.3.0~2.1

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0.2-1
- 2.3.0~2

* Sat Mar  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0-0.2.0rc1
- Add BR: lm_sensors-devel for Sensors support

* Fri Mar  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0-0.1.0rc1
- 2.3.0 0rc1
- Dbus interface: enable python, disable python, disable vala for now

* Thu Dec  9 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.2.0.4-1
- 2.2.0-4

* Sat Jul  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against new webkitgtk

* Fri Jun 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.9-3
- Fix for "GMenu does not handle desktop file exec strings properly"
  (Lauchpad 526138, rpmfusion 1265)

* Wed May 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rebuild against new libetpan

* Thu Apr 22 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.9-1
- 2.1.3-9

* Wed Apr  7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.8-1
- 2.1.3-8

* Thu Apr  1 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.7-2
- Try to enable Network-Monitor and Scooby-do (while the codes say that
  this will be enabled from 2.1.4) (bug 578393)

* Sun Mar 14 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.7-1
- 2.1.3-7
- Some packaging changes out of requests from the upstream
  * rename %%name package to -core, make %%name be a metapkg for
    pulling -core and -plug-ins
  * split kde related files from -plug-ins
- Change R: wget -> curl

* Wed Mar  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.6-1
- 2.1.3-6

* Fri Feb 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.5-1
- 2.1.3-5

* Thu Feb 18 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.3-1
- 2.1.3-3

* Fri Feb 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.2-1
- 2.1.3-2

* Sun Jan 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-13: Rebuild for libxklavier soname bump

* Fri Dec 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.2.4-1
- 2.1.2-4

* Sat Nov  6 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.1.2-1
- 2.1.1-2

* Sat Oct 10 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.0-1
- 2.1.0

* Wed Sep 30 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.8.2-1
- 2.0.8.2

* Sun Jul 12 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.8-1
- 2.0.8

* Fri Jul  3 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.7-1
- 2.0.7

* Thu Jul  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-12: rebuild against new libxklavier

* Sat Jun 27 2009 Mamoru Tasaka <mtaaska@ioa.s.u-tokyo.ac.jp> - 2.0.6-1
- 2.0.6

* Thu Jun 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1833
- Remove workaround for bug 506656

* Thu Jun 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1825
- Remove debugedit workaround as bug 505774 is solved.
- Workaround for X11/extensions/XTest.h bug 506656

* Mon Jun 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1821
- Compile with -gdwarf-2 until bug 505774 is resolved.

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.5-1
- 2.0.5

* Tue Jun  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-1
- 2.0.4

* Mon May 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.3-2
- Workaround to avoid endless loop on po/ directory

* Sun May 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.3-1
- 2.0.3

* Tue May 19 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.2-1
- 2.0.2

* Sun May 17 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- 2.0.1

* Mon May 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-2.respin1
- Tarballs respun

* Sun May 10 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-1
- 2.0.0 release

* Wed Apr 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-0.7.rc5
- 2.0.0 rc5

* Mon Apr 27 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-0.6.svn1689_trunk
- Kill AutoProv on -themes subpackage to avoid unneeded desktop prov
- Build -themes subpackage as noarch

* Sat Apr 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-0.4.rc3
- 2.0.0 rc3
- Move to rpmfusion
- Enable mail plugin, license is now changed to GPL+
- borrow some missing files from svn trunk for rc3
- Drop "fedora-" prefix from desktop file

* Wed Feb 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1527

* Thu Jan 22 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1496
- Include Wanda directory in Cairo-Penguin plug-in again

* Thu Jan 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1484
- Trademarked icons under plug-ins/Cairo-Penguin/data/themes are
  removed.

* Thu Dec 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1451
- Remove icons maybe under non-free copyright/license from Cairo-Penguin plugin
  (need ask)

* Sat Dec 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1444
- Support xfce plugin again because dependency on hal-devel
  is resoved

* Wed Dec 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Trial fix to compile motion-blur plugin on rev 1439

* Sun Dec  7 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1429
- Try 2.0.0 development branch
- Build weblet plugin with WebKit, switching from Gecko,
  rename weblet related plugin
- Disable xfce related plugin for now until hal-devel is properly
  rebuilt

* Wed Nov 12 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3.1-1
- 1.6.3.1

* Wed Nov  5 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3-1
- 1.6.3

* Wed Oct 29 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3-0.3.rc2
- 1.6.3 rc2

* Tue Oct 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3-0.3.rc1
- 1.6.3 rc1

* Thu Oct 16 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3-0.2.svn1353_trunk
- GMenu plugin needs gnome-menus-devel

* Wed Sep 24 2008 Christopher Aillon <caillon@redhat.com> - 1.6.2.3-1.1
- Rebuild against newer gecko (F-9/8)

* Tue Sep  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2.3-1
- 1.6.2.3

* Thu Sep  4 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2.2-1
- 1.6.2.2

* Sat Aug 30 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2.1-1
- 1.6.2.1

* Thu Aug 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-1
- 1.6.2

* Tue Aug 26 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-0.6.RC4
- 1.6.2 RC4
- Temporary fix for stack/ plugin

* Sat Aug 23 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-0.3.RC2
- 1.6.2 RC2

* Sun Aug 10 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-0.2.svn1235_trunk
- Enable unstable plugins again

* Sun Aug 10 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-0.1.svn1235_trunk
- Patch to fix infinite loop of function call (this patch is needed
  for rev. 1235 and the released 1.6.1.2)
  (Fixed in svn 1241)

* Sat Aug  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Build only stable plug-ins for now

* Thu Jul 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.1.2-1
- 1.6.1.2

* Tue Jul 15 2008 Christopher Aillon <caillon@redhat.com>
- F-8: Rebuild against newer gecko

* Tue Jul 15 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.1.1-1
- 1.6.1.1

* Thu Jul  3 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-8: rebuild against new gecko

* Sat Jun 21 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0.2-1.date20080621
- 1.6.0.2

* Fri Jun 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0.1-2.date20080619
- Revert XCompositeRedirectSubwindows() part in 
  cairo-dock-X-utilities.c - fixed in rev. 1142

* Thu Jun 19 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0.1-1.date20080619
- 1.6.0.1

* Wed Jun 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0-0.2.svn1089_trunk
- Fix possibly unsafe tmpfile creation

* Thu Jun  5 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0-0.1.svn1080_trunk
- Prepare for using unified configure script on plug-ins directory
- Install desktop icon

* Wed May 27 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.6-1.date20080528
- 1.5.6

* Sat May 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-5.svn990_trunk
- Update to svn 990
- 2 issues fixed in upstream
  * plug-in directory moved to %%_libdir/%%name
  * %%name.pc fixed

* Sat May 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-4.date20080506
- F-10: don't build weblets plugin until xulrunner BR dependency is solved

* Sat May 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-3.date20080506
- Misc cleanup
- Remove template, upstream says this is not needed

* Sun May 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-2.date20080506
- Remove mail plug-in for now as there is license conflict
- Enable weblet plug-in

* Fri May  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-1.date20080506
- 1.5.5.4

* Thu May  1 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.3-1.date20080501
- Initial packaging
- remove Ubuntu related themes
- plugin dir is moved to %%_libdir/%%name/plug-in

