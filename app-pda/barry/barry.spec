Name:           barry
Version:        0.18.4
Release:        14%{?dist}
Summary:        BlackBerry Desktop for Linux
License:        GPLv2+
URL:            http://www.netdirect.ca/software/packages/barry
# The source for this package is often pulled from upstream's git.  Use the following
# commands to generate the tarball:
# git clone git://repo.or.cz/barry.git OR git pull barry
# cd barry/maintainer
# ./git-extract.sh 0 15 master
# (cd build/barry* && ../../tar-prepare.sh)
# (cd build && ../tar-create.sh 0 15)
Source0:        http://downloads.sourceforge.net/projects/%{name}/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2
Patch1:         barry-0.18-cxx11.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  fuse-devel
BuildRequires:  gettext-devel
BuildRequires:  gtkmm24-devel
BuildRequires:  libglade2-devel
BuildRequires:  libglademm24-devel
BuildRequires:  libtar-devel
BuildRequires:  libtool
BuildRequires:  libusb-devel
BuildRequires:  libxml++-devel
BuildRequires:  zlib-devel
Requires:       hicolor-icon-theme
Requires:       initscripts

%description
Barry is a desktop tool set for managing your BlackBerry device.

This package contains command line tools which will enable you to charge your
device with a proper 500mA and be able to access data on the device. It also
includes a GUI application to backup your BlackBerry.

%package        libs
Summary:        Library files for %{name}
Requires:       kmod
Requires:       pam

%description    libs
This package contains the library files used by BlackBerry Desktop for Linux.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       boost-devel%{?_isa}
Requires:       libusb-devel%{?_isa}

%description    devel
This package contains the development library files for Barry, barry-libs.

%package        devel-docs
Summary:        Development libraries documentation of %{name}
BuildArch:      noarch

%description    devel-docs
This package contains the documentation for the development library files for
Barry.

%package        opensync
Summary:        Opensync plugin of BlackBerry Desktop for Linux
BuildRequires:  libopensync-devel
Requires:       libopensync = 1:0.22

%description    opensync
This package contains the opensync plugin to synchronize your BlackBerry.

%prep
%setup -q
%patch1 -p1
rm -frv ./doc/www/*.php
rm -frv ./doc/www/*.sh
#find ./doc/www/doxygen/html -type f -size 0 -name \*.map -exec rm '{}' \;

%build
# main tree
%configure --enable-boost --with-zlib --disable-rpath
#--disable-rpath doesn't seem effective
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

# gui tree
pushd gui/
%configure --disable-rpath PKG_CONFIG_PATH="..:$PKG_CONFIG_PATH" CXXFLAGS="-I../.." LDFLAGS="-L../../src"
#--disable-rpath doesn't seem effective
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build
popd

# opensync tree
pushd opensync-plugin/
%configure --disable-rpath PKG_CONFIG_PATH="..:$PKG_CONFIG_PATH" CXXFLAGS="-I../.." LDFLAGS="-L../../src"
#--disable-rpath doesn't seem effective
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build
popd

%install
# main tree
%make_install

mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
cp udev/*.rules %{buildroot}%{_prefix}/lib/udev/rules.d/

#mkdir -p %{buildroot}%{_sysconfdir}/security/console.perms.d

mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d
cp modprobe/blacklist-berry_charge.conf %{buildroot}%{_sysconfdir}/modprobe.d/

mkdir -p %{buildroot}%{_sysconfdir}/ppp/peers
cp ppp/barry-* %{buildroot}%{_sysconfdir}/ppp/peers/

mkdir -p %{buildroot}%{_sysconfdir}/chatscripts
cp ppp/barry-*.chat %{buildroot}%{_sysconfdir}/chatscripts/

# Install hal fdi config
mkdir -p %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop
mkdir -p %{buildroot}%{_datadir}/hal/fdi/policy/10osvendor
cp hal/fdi/information/10freedesktop/10-blackberry.fdi %{buildroot}%{_datadir}/hal/fdi/information/10freedesktop
#cp hal/fdi/policy/10osvendor/19-blackberry-acl.fdi %{buildroot}%{_datadir}/hal/fdi/policy/10osvendor

# Install hal support script
mkdir -p %{buildroot}%{_bindir}
cp hal/hal-blackberry %{buildroot}%{_bindir}

%find_lang %{name}

# gui tree
pushd gui/
%make_install
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ ../menu/barrybackup.desktop
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
install -pm0644 ../logo/barry_logo_icon.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
popd

# opensync tree
pushd opensync-plugin/
%make_install
popd

find %{buildroot} -name '*.la' -delete -print
find %{buildroot} -name '*.a' -delete -print

%files -f %{name}.lang
%license COPYING
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/hal/fdi/information/10freedesktop/10-blackberry.fdi
#%{_datadir}/hal/fdi/policy/10osvendor/19-blackberry-acl.fdi
%{_datadir}/barry/glade/*.glade
%{_datadir}/applications/barrybackup.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/locale/fr/LC_MESSAGES/barry-backup.mo
%{_datadir}/locale/fr/LC_MESSAGES/barry-opensync-plugin.mo
%{_datadir}/locale/es/LC_MESSAGES/barry-backup.mo
%{_datadir}/locale/es/LC_MESSAGES/barry-opensync-plugin.mo
%config(noreplace) %{_sysconfdir}/ppp/peers/*
%config(noreplace) %{_sysconfdir}/chatscripts/*.chat

%files libs
%{_libdir}/*.so.*
%{_prefix}/lib/udev/rules.d/*
#%config(noreplace) %{_sysconfdir}/security/console.perms.d/*
%config(noreplace) %{_sysconfdir}/modprobe.d/blacklist-berry_charge.conf
%doc AUTHORS ChangeLog NEWS README
%license COPYING

%files devel
%{_includedir}/barry18/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%doc TODO examples/*.cc examples/*.am
%license COPYING

%files devel-docs
%doc doc/*

%files opensync
%{_libdir}/opensync/plugins/*
%{_datadir}/opensync/defaults/*
%license COPYING

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Jonathan Wakely <jwakely@redhat.com> 0.18.4-13
- Patched for C++14 and rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.18.4-12
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.4-11
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.18.4-10
- rebuild for Boost 1.58

* Tue Jul 14 2015 Mosaab Alzoubi <moceap@hotmail.com> - 0.18.4-9
- Fix #1239384
- Fix some days in %%changelog

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.18.4-7
- Rebuild for boost 1.57.0

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.18.4-4
- Rebuild for boost 1.55.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.18.4-2
- Rebuild for boost 1.54.0

* Fri Apr 19 2013 Nathanael Noblet <nathanael@gnat.ca> - 0.18.4-1
- New upstream release

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.18.3-5
- Rebuild for Boost-1.53.0

* Sat Feb 09 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 0.18.3-4
- Rebuild for Boost-1.53.0

* Mon Jul 30 2012 Nathanael Noblet <nathanael@gnat.ca> - 0.18.3-3
- Rebuilt for new boost 1.50 release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 6 2012 Nathanael Noblet <nathanael@gnat.ca> - 0.18.3-1
- remove udev requires
- moved udev rules to system directory
- removed un-needed security directory
- New upstream release

* Wed May 2 2012 Nathanael Noblet <nathanael@gnat.ca> - 0.18.0-1
- New upstream release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.1-7
- Rebuilt for c++ ABI breakage

* Thu Jan 5 2012 Nathanael Noblet <nathanael@gnat.ca> - 0.17.1-6
- Fixes for gcc 4.7

* Sun Nov 20 2011 Nathanael Noblet <nathanael@gnat.ca> - 0.17.1-5
- Release bump for F16 boost soname change

* Wed Nov 9 2011  Nathanael Noblet <nathanael@gnat.ca> - 0.17.1-4
- patch for bug #752000

* Fri Jul 22 2011 Nathanael Noblet <nathanael@gnat.ca> - 0.17.1-3
- boost requirements

* Wed Apr 6 2011 Nathanael Noblet <nathanael@gnat.ca> - 0.17.1-2
- Release bump for F16 boost soname change

* Fri Mar 4 2011 Nathanael Noblet <nathanael@gnat.ca> - 0.17.1-1
- Version bump - fixes build issues + some other minor software bugs

* Wed Feb 16 2011 Nathanael Noblet <nathanael@gnat.ca> - 0.17.0-2
- Readded smp_mflags as they aren't the build issue
- added disable-rpath which fixes the build issue and saves us rpath sed commands

* Mon Feb 14 2011 Nathanael Noblet <nathanael@gnat.ca> - 0.17.0-1
- Latest release
- Updates Source0 and URL tags accordingly
- Add libxml++ dependency
- Removed smp_mflags as we're experiencing build failures - prompted upstream to fix recursive makefiles

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-0.7.20110126git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Nathanael Noblet <nathanael@gnat.ca> - 0.6.20110126git
- fix for bz#665648

* Tue Jan 18 2011 Nathanael Noblet <nathanael@gnat.ca> - 0.6.20110118git
- New git snapshot to fix udev acl permissions

* Fri Dec 31 2010 Nathanael Noblet <nathanael@gnat.ca> - 0.6.20101231git
- New git snapshot - essentially RC1

* Fri Nov 26 2010 Nathanael Noblet <nathanael@gnat.ca> - 0.6.20101126git
- New git snapshot

* Thu Aug 05 2010 Nathanael Noblet <nathanael@gnat.ca> - 0.4.20100730git
- Removed un-needed specfile conditionals
- Version bump

* Wed Aug 04 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.20100329git
- Rebuild for Boost soname bump
- Update spec for guidelines and drop obsolete ifdefs

* Thu Jul 29 2010 Nathanael Noblet <nathanael@gnat.ca> - 0.3.20100730git
- Rebuilt against new boost
- Release version bump to keep upgrade path proper

* Mon Mar 29 2010 Nathanael Noblet <nathanael@gnat.ca> - 0.1.20100329git
- Update version to include new udev rules fixing permission issue on f12
- Fix icon and .desktop file installation
- rpmlint spelling errors fixed

* Fri Jan 22 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.5-0.10.200963git
- Rebuild for Boost soname bump

* Thu Sep 17 2009 Peter Lemenkov <lemenkov@gmail.com> - 0.15-0.9.20090630git
- Rebuilt with new fuse

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-0.8.20090630git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Christopher D. Stover <quantumburnz@hotmail.com> 0.15-0.7.20090630git
- version/git bump
- create separate doc package; BZ#508462
- fixed opensync build issue; BZ#506609
- incorporated hal changes to fix permission issues; BZ#478851
- add icon for BarryBackup; BZ#483151

* Tue Jun 23 2009 Christopher D. Stover <quantumburnz@hotmail.com> 0.15-0.6.20090623git
- version/git bump
- added configure --with-zlib

* Tue Mar 03 2009 Caolán McNamara <caolanm@redhat.com> - 0.15-0.5.20090109git
- include stdio.h for EOF

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-0.4.20090109git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Christopher D. Stover <quantumburnz@hotmail.com> 0.15-0.3.20090109git
- version bump for proper patch name

* Mon Jan 12 2009 Christopher D. Stover <quantumburnz@hotmail.com> 0.15-0.2.20090109git
- enable fuse module during build
- include ip_modem password patch for the Blackberry Bold 9000

* Mon Jan 12 2009 Christopher D. Stover <quantumburnz@hotmail.com> 0.15-0.1.20090109git
- version/git bump

* Thu Dec 18 2008 Petr Machata <pmachata@redhat.com> - 0.14-6
- rebuild for new boost

* Wed Nov 12 2008 Christopher D. Stover <quantumburnz@hotmail.com> 0.14-5
- removed opensync support for F11

* Mon Nov 10 2008 Christopher D. Stover <quantumburnz@hotmail.com> 0.14-4
- merged gui with the main package

* Mon Nov 10 2008 Christopher D. Stover <quantumburnz@hotmail.com> 0.14-3
- fixed Requires and BuildRequires
- modified gui package summary
- moved some config files to the libs package
- removed static libraries

* Sun Nov 09 2008 Christopher D. Stover <quantumburnz@hotmail.com> 0.14-2
- updated license to GPLv2+
- fixed directory ownership issues
- created separate libs package and moved *.so to devel package
- cleaned up /doc/www
- removed Rpaths

* Tue Oct 28 2008 Christopher D. Stover <quantumburnz@hotmail.com> 0.14-1
- initial package for fedora

* Wed Sep 24 2008 Chris Frey <cdfrey@foursquare.net> 0.14-0
- version bump
- added new ppp chat script for T-Mobile US
- renamed libbarry to libbarry0

* Thu May 29 2008 Chris Frey <cdfrey@foursquare.net> 0.13-1
- version bump
- added brecsum
- added ppp options and chat scripts
- added manpages for pppob, brecsum, breset, upldif, barrybackup
- spec file now assumes gui and opensync, with conditional checks depending on host

* Fri Dec 07 2007 Chris Frey <cdfrey@foursquare.net> 0.12-1
- version bump

* Fri Nov 30 2007 Chris Frey <cdfrey@foursquare.net> 0.11-1
- version bump

* Fri Nov 30 2007 Chris Frey <cdfrey@foursquare.net> 0.10-1
- version bump
- removed ktrans and translate from rpm package
- added bidentify

* Thu Aug 09 2007 Chris Frey <cdfrey@foursquare.net> 0.9-1
- version bump

* Fri Aug 03 2007 Chris Frey <cdfrey@foursquare.net> 0.8-1
- version bump
- changed tarball to bz2

* Tue May 01 2007 Chris Frey <cdfrey@foursquare.net> 0.7-2
- added pppob to utils

* Thu Mar 08 2007 Chris Frey <cdfrey@foursquare.net> 0.7-1
- removed barry base package that only contained docs, and put docs in libbarry*
- changed barrybackup reference to barry-gui
- removed the patch step, as version 0.7 shouldn't need it
- added license file to each package

* Sun Mar 04 2007 Troy Engel <tengel@users.sourceforge.net> 0.6-1
- initial build
- adding udev and console perms patch for raw 0.6
