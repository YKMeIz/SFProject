# currently just a meta-package (since 3.9.1 plugins movement)

%global pluginapi 3.11.1.0

Name:           claws-mail-plugins
Version:        3.11.1
Release:        3%{?dist}
Summary:        Additional plugins for Claws Mail

Group:          Applications/Internet
License:        GPLv2 and GPLv3+ and MIT
URL:            http://claws-mail.org

Source0:        README.Fedora
#Source0:        http://downloads.sourceforge.net/sylpheed-claws/claws-mail-extra-plugins-%{version}.tar.bz2

#BuildRequires:  claws-mail-devel >= %{version}

Obsoletes:      %{name}-devel <= 3.9.0
Provides:       %{name}-devel = %{version}-%{release}

# the ones from main claws-mail package...
Requires:       %{name}-acpi-notifier
Requires:       %{name}-address-keeper
Requires:       %{name}-archive
Requires:       %{name}-att-remover
Requires:       %{name}-attachwarner
Requires:       %{name}-bogofilter
%if !0%{?rhel}
Requires:       %{name}-bsfilter
%endif
Requires:       %{name}-clamd
Requires:       %{name}-fancy
Requires:       %{name}-fetchinfo
Requires:       %{name}-gdata
%if !0%{?rhel}
Requires:       %{name}-geolocation
%endif
Requires:       %{name}-libravatar
Requires:       %{name}-mailmbox
Requires:       %{name}-newmail
Requires:       %{name}-notification
Requires:       %{name}-pdf-viewer
Requires:       %{name}-perl
Requires:       %{name}-pgp
Requires:       %{name}-python
Requires:       %{name}-rssyl
Requires:       %{name}-smime
Requires:       %{name}-spamassassin
Requires:       %{name}-spam-report
Requires:       %{name}-tnef
Requires:       %{name}-vcalendar


%description
Additional plugins for Claws Mail.


%prep
#setup -q -n claws-mail-extra-plugins-%{version}

# guard for pluginapi
# disable guard
SOURCEAPI=$(grep -A 1 VERSION_NUMERIC %{_includedir}/claws-mail/common/version.h | tr -d '\n' | perl -ne 's/[\\\s]//g; m/(\d+),(\d+),(\d+),(\d+)/; print("$1.$2.$3.$4");')
#[ "%pluginapi" == "$SOURCEAPI" ] || exit -1

%build


%install
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type f -name "*.a" -exec rm -f {} ';'


%files
#%doc RELEASE_NOTES


%changelog
* Wed Feb 04 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.11.1-3
- remove geolocation on epel

* Tue Feb 03 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 3.11.1-2
- add tnef and gdata plugin on epel
- remove bsfilter plugin on epel

* Fri Oct 31 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.11.1-1
- bump for 3.11.1 release

* Sat Oct 25 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.11.0-1
- bump for 3.11.0 release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.10.1-1
- bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.10.0-1
- bump
- add libravatar plugin

* Sun Dec 15 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.3-1
- bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.2-1
- rebuild for 3.9.2

* Wed May 22 2013 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.9.1-1
- build just the claws-mail-plugins meta-package
- disable BuildRequires claws-mail-devel
- disable %%setup, because it's not needed currently
- redirect Source0 tag to a readme file, since no tarball is used currently
- also drop moved geolocation plugin stuff and dead gtkhtml2

* Wed Mar 13 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.0-7
- bump api to 122

* Wed Mar 06 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.0-6
- move plugins to main package
- obsolete devel
- build as empty package to clear up rawhide deps

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 20 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.9.0-4
- Fix rebuild for F19 development: no longer autoreconf gdata and fancy
  plug-ins, because that would require fixing the configure.ac beyond
  replacing AM_PROG_CC_STDC with AC_PROG_CC.

* Thu Jan 17 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.9.0-3
- Rebuilt for new libarchive

* Tue Nov 20 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.0-2
- fix vCalendar user credential disclosure rhbz: 877372 877375 877376

* Mon Nov 19 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.9.0-1
- version upgrade

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Petr Pisar <ppisar@redhat.com> - 3.8.1-2
- Perl 5.16 rebuild

* Thu Jul 05 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.8.1-1
- version upgrade
- add subpackage for -pdf-viewer plugin

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 3.8.0-5
- Perl 5.16 rebuild

* Thu Jan 26 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.8.0-4
- Rebuilt for new libarchive

* Sun Jan 22 2012 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.8.0-3
- adjust claws-mail-devel Requires to '>= %%version' and be arch-specific
  (so claws-mail %%release can differ from claws-mail-plugins %%release)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 29 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.8.0-1
- version upgrade
- cleanup patches
- add -devel subpackage with include files

* Thu Dec 15 2011 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.10-12
- fix undefined symbol in vcalendar plugin snapshot (#768077)

* Mon Dec 12 2011 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.10-11
- fix Fedora 15 specific typo in spec file, which made koji build stop early

* Wed Nov 30 2011 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.10-10
- don't build geolocation plugin since we can't mix gtk2 and gtk3
  (#758173, #662800)
- remove libchamplain* pkg-config hacks for geolocation plugin
  (it supports 0.4 to 0.8 only)
- merge newer vcalendar plugin to fix a crash (#742249)
- drop ancient Obsoletes/Provides
- drop old spec sections not needed anymore

* Fri Nov 25 2011 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.10-9
- fix missing %%doc files in -perl subpackage (#707662)
- fix for new glib2 where only glib.h must be included

* Thu Nov 24 2011 Tomas Bzatek <tbzatek@redhat.com>
- 3.7.10-8
- Rebuilt for new libarchive and clutter

* Thu Oct 06 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-7
- pull cvs version of fancy for newer webkit support (rhbz#743834)
- fix debuginfo (rhbz#742249)

* Wed Sep 28 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-6
- drop unneeded plugin requires

* Tue Sep 27 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-5
- fix requires for mock

* Mon Sep 26 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-4
- make plugin api isa dependent

* Sun Sep 25 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-3
- change plugin dependencies to depend on plugin api version
  (rhbz#740662)

* Thu Sep 22 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-2
- pull gdata cvs version with upstreamed patch for authorizers in
  libgdata >= 0.9.x

* Tue Aug 30 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.10-1
- version upgrade
- add gdata plugin
- remove upstreamed patches

* Thu Aug 04 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-9
- deprecate gtkhtml2 on f16 upwards

* Wed Aug 03 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-8
- rebuild (cogl)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 3.7.9-7
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 3.7.9-6
- Perl mass rebuild

* Tue Jul 05 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-5
- fix libnotify support (rhbz#718828)

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 3.7.9-4
- Perl mass rebuild

* Fri May 20 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-3
- fix clam plugin crash (#706322)

* Mon Apr 11 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-2
- move some obsoletes to claws-mail package

* Sun Apr 10 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.9-1
- version upgrade
- spec cleanups

* Sat Apr 09 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-11
- add build fix for libchamplain 0.9

* Wed Apr 06 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-10
- rebuild for libchamplain

* Sun Feb 13 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-9
- fix crash in spam plugin (#676352)

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com>
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com>
- Rebuild against newer gtk

* Mon Jan 24 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-5
- disable tnef on rhel

* Sun Jan 23 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-4
- disable dillo on rhel
- make python plugin dlopen right python so (#666335)
- include python plugin examples (#664265)

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com>
- Rebuild against newer gtk

* Wed Dec 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-2
- fixup clutter-gtk-devel dep

* Wed Dec 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.8-1
- version upgrade
- retire cachesaver, synce

* Fri Nov 12 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7.6-9
- patch notification plugin and rebuild for new libnotify 0.7.0

* Mon Nov 08 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.6-8
- rebuild against new libnotify

* Wed Sep 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.7.6-7
- rebuild against champlain 0.8

* Sat Sep 04 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.6-6
- bump

* Sat Jul 31 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 3.7.6-5
- patch geolocation plugin temporarily to look for champlain-gtk-0.6.pc
  (Fedora 14) so the entire package can be rebuilt for Python 2.7

* Sun Jul 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.6-4
- rebuild libchamplain

* Fri Jul 02 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.6-3
- rebuild for webkitgtk

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.7.6-2
- Mass rebuild with perl-5.12.0

* Tue May 11 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.6-1
- version upgrade

* Tue Feb 09 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.5-1
- version upgrade
- unify specs

* Tue Jan 12 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.4-2
- change Provides/Obsoletes of the geolocation plugin

* Fri Jan 08 2010 Kevin Fenzi <kevin@tummy.com> 
- 3.7.4-1

* Mon Oct 12 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.3-1
- version upgrade
- new plugins bsfilter, python

* Fri Aug 07 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.2-3
- fix crash in fancy plugin (#515373)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.2-1
- version upgrade
- new plugin: fancy
- fix notification plugin to work with libnotify (#496149)

* Mon Mar 30 2009 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.1-2
- use %%find_lang macro

* Sat Mar 28 2009 Kevin Fenzi <kevin@tummy.com> - 3.7.1-1
- Update to 3.7.1

* Thu Mar 19 2009 Michael Schwendt <mschwendt@fedoraproject.org>
- 3.7.0-3
- include directories /usr/include/claws-mail{,/plugins} in
  "archive" and "vcalendar" sub-packages (#473638)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.7.0-1
- version upgrade

* Fri Nov 21 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.6.1-1
- version upgrade

* Sat Oct 04 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.6.0-1
- version upgrade
- transition smime from plugins to main package

* Mon Sep 08 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.5.0-2
- rebuild

* Mon Jun 30 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.5.0-1
- version upgrade
- upstream dropped pdf plugin
- new archive plugin

* Wed Apr 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.4.0-1
- version upgrade

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 3.3.1-4
- add missing BR: ExtUtils::Embed

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 
- 3.3.1-3
- add Requires for versioned perl (libperl.so)

* Tue Mar 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.3.1-2
- correct BR

* Sat Feb 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.3.1-1
- version upgrade
- clamav plugin has been dropped upstream
- improve descriptions

* Fri Feb 08 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.3.0-1
- version upgrade
- clamav

* Mon Dec 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.2.0-1
- version upgrade
- added tnef plugin

* Wed Nov 21 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.1.0-1
- version upgrade

* Mon Oct 08 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.0.1-1
- version upgrade

* Mon Sep 10 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.0.0-2
- fix typo

* Wed Sep 05 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 3.0.0-1
- version upgrade

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.10.0-2
- new license tag

* Tue Jul 03 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.10.0-1
- version upgrade

* Sat Jun 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9.2-2
- bump

* Tue May 15 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9.2-1
- version upgrade

* Sat Apr 21 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9.1-1
- version upgrade which fixes pdfviewer bug

* Mon Apr 16 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.9.0-1
- version upgrade

* Tue Mar 06 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.8.0-2
- bump

* Wed Feb 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.8.0-1
- version upgrade
- fix rpath

* Wed Feb 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.7.1-2
- bump

* Thu Jan 18 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.7.1-1
- version upgrade

* Fri Dec 22 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.6.1-2
- some more fixes

* Mon Dec 11 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.6.1-1
- version upgrade
- rename to claws-mail-plugins

* Thu Nov 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.6.0-1
- version upgrade

* Tue Nov 07 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.2-5
- rebuild

* Fri Oct 20 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.2-4
- rebuild

* Thu Oct 12 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.2-3
- rebuild

* Sun Oct 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.2-2
- rebuild

* Sat Sep 30 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.2-1
- version upgrade

* Tue Sep 26 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.5.0-1
- version upgrade

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.4.0-2
- FE6 rebuild

* Wed Aug 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.4.0-1
- version upgrade

* Wed Jul 05 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.3.0-2
- bump

* Tue Jun 13 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.3.0-1
- version upgrade

* Tue May 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.2.0-1
- version upgrade

* Sat Apr 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.1.0-1
- version upgrade

* Fri Feb 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-2
- Rebuild for Fedora Extras 5

* Fri Feb 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
2.0.0-1
- version upgrade

* Sun Dec 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.100-2
- rebuild

* Thu Nov 17 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.100-1
- version upgrade

* Sun Aug 21 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-5
- enable x86_64 synce plugin

* Sat Aug 20 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-4
- add dist tag

* Sat Aug 20 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-3
- exlude ical.h

* Thu Aug 18 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-2
- use setup macro (-c)
- disable synce build on x86_64 for now (#148003)

* Sun Jul 31 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.9.13-1
- Initial Release
