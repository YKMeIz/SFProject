Name:           w_scan
Version:        20140727
Release:        3%{?dist}
Summary:        Tool for scanning DVB transponders

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://wirbel.htpc-forum.de/w_scan/index2.html
Source0:        http://wirbel.htpc-forum.de/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The w_scan tool is similar to dvbscan from dvb-apps. However it does not 
require initial tuning data and thus is able to find more channels.


%prep
%setup -q
iconv -f iso-8859-1 -t utf-8 doc/w_scan.1 > doc/w_scan.1.utf-8
touch -r doc/w_scan.1 doc/w_scan.1.utf-8
mv doc/w_scan.1.utf-8 doc/w_scan.1

chmod 644 README

%build
%configure
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README
%doc doc/README.file_formats doc/README_VLC_DVB doc/rotor.conf
%{_bindir}/%{name}
%{_datadir}/man/man?/%{name}*


%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140727-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140727-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Aug 17 2014 Felix Kaechele <heffer@fedoraproject.org> - 20140727-1
- update to 20140727

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140118-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Felix Kaechele <heffer@fedoraproject.org> - 20140118-1
- update to 20140118

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130331-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Felix Kaechele <heffer@fedoraproject.org> - 20130331-1
- bugfixes
- support for VDR < 1.7.3 was dropped upstream

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120605-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 04 2012 Felix Kaechele <heffer@fedoraproject.org> - 20120605-1
- bugfixes
- Israel DVB-T support
- updated all sattelite info
- added support for 67 more sattelites

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120112-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 21 2012 Felix Kaechele <heffer@fedoraproject.org> - 20120112-1
- many updates and code cleanups
- preliminary DVB-T2 support

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20111011-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 23 2011 Felix Kaechele <heffer@fedoraproject.org> - 20111011-1
- various output format fixes
- various transponder updates

* Sun Jun 12 2011 Felix Kaechele <heffer@fedoraproject.org> - 20110502-1
- memory leak and various other fixes
- added ISDB-T/DVB-C support for Brazil

* Tue Feb 08 2011 Felix Kaechele <heffer@fedoraproject.org> - 20110206-1
- various bugfixes

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20101001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 04 2010 Felix Kaechele <heffer@fedoraproject.org> - 20101001-1
- additional DVB-C symbol rates 6956 and 6956.5 for New Zealand
- mplayer output format as suggested Pedro A. Aranda
- cosmetics

* Thu Jun 03 2010 Felix Kaechele <heffer@fedoraproject.org> - 20100529-1
- added several descriptor IDs
- typo in help text fixed
- updated Astra 1E/1G/3A
- updated Hispasat 1C/1D
- zero pids fix
- added Telstar 5 S97W0
- New: ATSC channel syntax for VDR-1.7.14
- New: DVB-C symbol rates 5156, 4583 

* Mon Jan 18 2010 Felix Kaechele <heffer@fedoraproject.org> - 20091230-1
- DVB-T UK: 8k tm mode
- allow any DVB 5.x API
- fixes compiler warnings
- update S28E2

* Mon Oct 12 2009 Felix Kaechele <heffer@fedoraproject.org> - 20090918-1
- new upstream release

* Sat Aug 08 2009 Felix Kaechele <heffer@fedoraproject.org> - 20090808-1
- fixes 513871

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090528-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Felix Kaechele <heffer@fedoraproject.org> - 20090528-2
- added dos2unix BuildReq

* Sat Jun 20 2009 Felix Kaechele <heffer@fedoraproject.org> - 20090528-1
- new upstream version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20081106-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Felix Kaechele <heffer@fedoraproject.org> - 20081106-1
- Initial build
