%global gitdate 20160110
%global gitcommit b38ab1117e5daab79d3642b2cc85f8a5d48c89f4
%global gitshort %(c=%{gitcommit}; echo ${c:0:6})

%bcond_with audacious
%bcond_without curl
%bcond_without ibm
%bcond_without imlib
%bcond_without lua_cairo
%bcond_without lua_imlib
%bcond_with moc
%bcond_without mpd
%bcond_with ncurses
%bcond_with nvidia
%bcond_without rss
%bcond_without weather
%bcond_without weather_xoap
%bcond_without wlan
%bcond_without xdbe
%bcond_without xinerama

Name:           conky 
Version:        1.10.1
Release:        4.%{gitdate}git%{gitshort}%{?dist}
Summary:        A system monitor for X 

Group:          User Interface/X
License:        GPLv3+
URL:            https://github.com/brndnmtthws/conky
Source0:        https://github.com/brndnmtthws/%{name}/archive/%{gitshort}/%{name}-%{gitshort}.tar.gz

BuildRequires:  libXft-devel
BuildRequires:  libXt-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXext-devel
BuildRequires:  lua-devel
%{?with_audacious:BuildRequires: audacious-devel < 3.5 dbus-glib-devel}
%{?with_curl:BuildRequires: curl-devel}
%{?with_imlib:BuildRequires: imlib2-devel}
%{?with_lua_cairo:BuildRequires: cairo-devel tolua++-devel}
%{?with_lua_imlib:BuildRequires: imlib2-devel tolua++-devel}
%{?with_ncurses:BuildRequires: ncurses-devel}
%{?with_nvidia:BuildRequires: libXNVCtrl-devel}
%{?with_rss:BuildRequires: curl-devel libxml2-devel}
%{?with_weather:BuildRequires: curl-devel}
%{?with_weather_xoap:BuildRequires: libxml2-devel}
%{?with_wlan:BuildRequires: wireless-tools-devel}
%{?with_xinerama:BuildRequires: libXinerama-devel}
# needed to generate documentation in the git snapshot
BuildRequires:  docbook2X docbook-style-xsl man
BuildRequires:  cmake git

%description
A system monitor for X originally based on the torsmo code. but more kickass. 
It just keeps on given'er. Yeah.

%prep
%setup -q -n %{name}-%{gitcommit}

# remove -Werror from CFLAGS
sed -i 's|-Werror||' cmake/ConkyBuildOptions.cmake

# remove executable bits from files included in %{_docdir}
chmod a-x extras/convert.lua

for i in AUTHORS; do
    iconv -f iso8859-1 -t utf8 -o ${i}{_,} && touch -r ${i}{,_} && mv -f ${i}{_,}
done

%build
%cmake \
                            -DMAINTAINER_MODE=ON \
                            -DBUILD_BUILTIN_CONFIG=OFF \
                            -DBUILD_PORT_MONITORS=OFF \
    %{?with_audacious:      -DBUILD_AUDACIOUS=ON} \
    %{?with_curl:           -DBUILD_CURL=ON} \
    %{!?with_ibm:           -DBUILD_IBM=OFF} \
    %{?with_imlib:          -DBUILD_IMLIB2=ON} \
    %{?with_lua_cairo:      -DBUILD_LUA_CAIRO=ON} \
    %{?with_lua_imlib:      -DBUILD_LUA_IMLIB2=ON} \
    %{!?with_moc:           -DBUILD_MOC=OFF} \
    %{!?with_mpd:           -DBUILD_MPD=OFF} \
    %{!?with_ncurses:       -DBUILD_NCURSES=OFF} \
    %{?with_nvidia:         -DBUILD_NVIDIA=ON} \
    %{?with_rss:            -DBUILD_RSS=ON} \
    %{?with_weather:        -DBUILD_WEATHER_METAR=ON} \
    %{?with_weather_xoap:   -DBUILD_WEATHER_XOAP=ON} \
    %{?with_wlan:           -DBUILD_WLAN=ON} \
    %{?with_xdbe:           -DBUILD_XDBE=ON} \
    %{?!with_xinerama:      -DBUILD_XINERAMA=OFF} \
    .

make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/conky
install -m644 -p data/conky.conf $RPM_BUILD_ROOT%{_sysconfdir}/conky
rm -rf $RPM_BUILD_ROOT%{_docdir}/conky-*


%files
%doc AUTHORS COPYING README.md extras/*
%dir %{_sysconfdir}/conky
%config %{_sysconfdir}/conky/conky.conf
%{_bindir}/conky
%if %{with lua_cairo} || %{with lua_imlib}
%{_libdir}/conky
%endif
%{_mandir}/man1/conky.1*


%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-4.20160110gitb38ab1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Tim Niemueller <tim@niemueller.de> - 1.10.1-3.20160110gitb38ab1-3
- rebuild for updated tolua++

* Mon Jan 11 2016 Miroslav Lichvar <mlichvar@redhat.com> - 1.10.1-2.20160110gitb38ab1
- update to 1.10.1-20160110gitb38ab1

* Fri Dec 04 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.10.1-1.20151201git1abd25
- update to 1.10.1-20151201git1abd25
- enable double-buffering support (#1284232)

* Tue Nov 03 2015 Miroslav Lichvar <mlichvar@redhat.com> - 1.10.0-1.20150824git341495
- update to 1.10.0-20150824git341495
- don't package manual in html

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-14.20141003git30d09e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 16 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.9.0-13.20141003git30d09e
- update to 20141003git30d09e
- build with lua-5.2 for new tolua++

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-12.20140617gitab826d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 09 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.9.0-11.20140617gitab826d
- build with lua-5.1 (#1117120)

* Mon Jun 23 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.9.0-10.20140617gitab826d
- update to 20140617gitab826d

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-9.20131027git11a13d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Miroslav Lichvar <mlichvar@redhat.com> - 1.9.0-8.20131027git11a13d
- disable audacious support (#1090655)

* Tue Oct 29 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.9.0-7.20131027git11a13d
- update to 20131027git11a13d
- enable weather support (#1024089)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-6.20121101gitbfaa84
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Tom Callaway <spot@fedoraproject.org> - 1.9.0-5.20121101gitbfaa84
- rebuild for lua 5.2

* Tue Apr 09 2013 Miroslav Lichvar <mlichvar@redhat.com> - 1.9.0-4.20121101gitbfaa84
- update to 20121101gitbfaa84
- remove obsolete macros

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Miroslav Lichvar <mlichvar@redhat.com> - 1.9.0-1
- update to 1.9.0

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 24 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.8.1-4
- Rebuild as needed for 1.8.1-3 and latest Audacious library deps.
- Fix rebuild failure on Rawhide (no <curl/types.h>).

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.8.1-3
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.1-1
- update to 1.8.1

* Wed Apr 21 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.0-4
- remove rpath

* Wed Apr 14 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.0-3
- enable imlib support (#581986)

* Thu Apr 01 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.8.0-2
- update to 1.8.0

* Mon Feb 15 2010 Miroslav Lichvar <mlichvar@redhat.com> - 1.7.2-2
- fix building with new audacious (#556317)

* Tue Aug 25 2009 Miroslav Lichvar <mlichvar@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Miroslav Lichvar <mlichvar@redhat.com> - 1.7.1.1-2
- Rebuild for new audacious
- Buildrequire libxml2-devel

* Wed Jun 17 2009 Miroslav Lichvar <mlichvar@redhat.com> - 1.7.1.1-1
- Update to 1.7.1.1

* Mon May 11 2009 Miroslav Lichvar <mlichvar@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.6.1-1
- Update to 1.6.1
- Fix buffer overflow when reading interface addresses

* Tue Jul 22 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.6.0-1
- Update to 1.6.0
- Fix freq_dyn on x86_64

* Tue Apr 01 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Sun Mar 23 2008 Miroslav Lichvar <mlichvar@redhat.com> - 1.5.0-1
- Update to 1.5.0
- Convert doc files to UTF-8

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.9-2
- Autorebuild for GCC 4.3

* Tue Nov 27 2007 Miroslav Lichvar <mlichvar@redhat.com> - 1.4.9-1
- Update to 1.4.9
- Enable support for Audacious 1.4.0

* Sun Oct 21 2007 Miroslav Lichvar <mlichvar@redhat.com> - 1.4.8-1
- Update to 1.4.8
- Enable mpd, rss and wireless support
- Update license tag

* Wed Apr 18 2007 Michael Rice <errr[AT]errr-online.com> - 1.4.5-4
- Rebuild to match audacious lib in fc6 bug: 236989

* Mon Apr 09 2007 Michael Rice <errr[AT]errr-online.com> - 1.4.5-3
- Rebuild for devel

* Thu Dec 14 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.5-2
- Ship NEWS
- Add patch for license of timed_thread and NEWS

* Tue Dec 12 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.5-1
- version bump
- change group
 
* Wed Dec 06 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.4-3
- rebuild for new audacious lib version

* Thu Nov 30 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.4-2
- Move nano and vim files into docs
- remove unneeded BR's

* Tue Nov 21 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.4-1
- Version bump
- Add vim and nano syntax files to package

* Thu Oct 05 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.3-1
- Version bump
- Remove Install file from docs

* Mon Oct 02 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.2-4
- moved to configure macro from ./configure
- clean up changelog and make more informative entrys
- Fixed sumary in spec file
- remove NEWS file since it was empty
- remove xmms support due to possible security issue
- remove bmp support due to possible security issue
- add missing BR for libXext-devel and remove unneeded libX11-devel  

* Thu Sep 28 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.2-3
- use the GPL as licence since the whole package is GPL

* Thu Sep 28 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.2-2
- remove unneeded deps

* Tue Sep 26 2006 Michael Rice <errr[AT]errr-online.com> - 1.4.2-1
- Initial RPM release
