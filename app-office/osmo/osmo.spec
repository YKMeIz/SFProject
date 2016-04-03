

# 'rel' is always the release number.
# If you're building from SVN, set 'svn' to the SVN revision. If not, set it to 0.
%global rel 3
%global svn 0
%if %{svn}
# svn co https://osmo-pim.svn.sourceforge.net/svnroot/osmo-pim/trunk osmo-pim
# tar cvJf osmo-%{svn}.tar.xz osmo-pim/ --exclude=".svn*"
%global release 0.%{rel}.svn%{svn}%{?dist}.1
%global tarname %{name}-%{svn}.tar.xz
%global dirname osmo-pim
%else
%global release %{rel}%{?dist}
%global tarname %{name}-%{version}.tar.gz
%global dirname %{name}-%{version}
%endif

Summary:        Personal organizer
Summary(pl):    Osobisty organizer
Summary(de):    Persönlicher Organizer
Name:           osmo
Version:        0.2.14
Release:        %{release}
License:        GPLv2+
Group:          Applications/Productivity
URL:            http://clayo.org/osmo/
Source0:        http://downloads.sourceforge.net/%{name}-pim/%{tarname}

Patch0:         %{name}-0.2.10-configure.patch
# Distro specific patches
Patch10:        %{name}-0.2.10-aplay.patch

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gtk2-devel
BuildRequires:  gtkspell-devel
BuildRequires:  libical-devel
BuildRequires:  libnotify-devel
BuildRequires:  libxml2-devel
BuildRequires:	libical-devel
# for contacts
BuildRequires:  webkitgtk-devel
# for backup
BuildRequires:  libgringotts-devel
BuildRequires:  libtar-devel
# for the SyncML plugin - disabled due to broken libsyncml (adamw 2012/09)
# BuildRequires:  libsyncml-devel
# for Patch0
BuildRequires:  autoconf
BuildRequires:  automake

Requires:       hicolor-icon-theme
Requires:       tzdata
Requires:       xdg-utils
Requires:       alsa-utils
Requires:	libical

%description
Osmo is a handy personal organizer which includes calendar, tasks manager and
address book modules. It was designed to be a small, easy to use and good
looking PIM tool to help to manage personal information. In current state the
organizer is quite convenient in use - for example, user can perform nearly
all operations using keyboard. Also, a lot of parameters are configurable to
meet user preferences.

%description -l pl
Osmo to podręczny organizer, zawierający kalendarz, menedżer zadań i książkę
adresową. W zamierzeniu był małym, prostym w obsłudze i dobrze wyglądającym 
menedżerem informacji osobistych. Osmo jest bardzo wygodny - niemal wszystkie
operacje można wykonać za pomocą klawiatury. Program udostępnia wiele opcji,
które użytkownik może zmienić, by program bardziej mu odpowiadał.

%description -l de
Osmo ist ein handlicher persönlicher Organzier mit Kalender, Aufgabenliste und
Adressbuch. Er wurde als kleines, einfach zu benutzendes und gut aussehendes 
PIM-Werkzeug zur Verwaltung persönlicher Informationen entworfen. Im 
gegenwärtigen Zustand ist er sehr angenehm zu benutzen, so kann der Nutzer zum 
Beispiel fast alle Aktionen mit der Tastatur ausführen. Außerdem lassen sich 
viele Parameter einstellen, um die Vorlieben des Benutzers zu treffen.


%prep
%setup -q
#%patch0 -p1 -b .configure
#%patch10 -p1 -b .aplay
autoreconf -i


%build
%configure --enable-backup=yes --enable-printing=yes \
  --with-contacts --with-tasks --with-notes
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps

make install DESTDIR=%{buildroot} INSTALL="install -p"

# icon
mv %{buildroot}%{_datadir}/pixmaps/%{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/48x48/apps

# Remove empty directory.
rm -rf %{buildroot}%{_datadir}/pixmaps/

%find_lang %{name}

desktop-file-install \
    %if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
    --vendor fedora \
    %endif
    --delete-original \
    --dir %{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/%{name}.desktop


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TRANSLATORS
%{_bindir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_mandir}/man1/%{name}.1*
%dir %{_datadir}/sounds/osmo
%{_datadir}/sounds/osmo/alarm.wav

%changelog
* Wed Dec 02 2015 Nux <rpm@li.nux.ro>  -0.2.14-3
- rebuild with newer libical from CentOS 7.2

* Sun Oct 04 2015 Nux <rpm@li.nux.ro> - 0.2.14-2
- add libical support/deps

* Mon Aug 10 2015 Nux <rpm@li.nux.ro> - 0.2.14-1
- update to 0.2.14

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-0.6.svn924.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Rex Dieter <rdieter@fedoraproject.org> 0.2.12-0.6.svn924
- rebuild (libical)

* Tue May 14 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.12-0.5.svn924
- BuildRequire autoconf and automake (for Patch0)

* Tue May 14 2013 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.12-0.4.svn924
- Fix desktop vendor conditionals
- Spec file clean-up

* Tue Apr 30 2013 Jon Ciesla <limburgher@gmail.com> - 0.2.12-0.3.svn924.1
- Drop desktop vendor tag.
- De-macro'd setup to paper-over FTBFS.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-0.2.svn924.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 07 2012 Adam Williamson <awilliam@redhat.com> - 0.2.12-0.2.svn924
- rescue the NEVR from people using scripts
- drop syncml plugin - libsyncml has been dead for two years and is
  currently not installable
- configure.patch: don't pass -Wall to automake, as there are warnings
  from src/Makefile.am and po/Makefile.am with current autotools

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-0.1.svn924.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-0.1.svn924.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.2.12-0.1.svn924.1
- Rebuild for new libpng

* Mon Aug 15 2011 Adam Williamson <awilliam@redhat.com> - 0.2.12-0.1.svn924
- bump to current svn to get webkit support plus many other fixes
- build against webkit instead of gtkhtml2, which doesn't exist any more
- fix BR: libtar-devel, not libtar
- drop libnotify-0.7.0.patch (upstream is now version-agnostic)
- rediff configure.patch to apply to configure.ac so it works with
  snapshots

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 06 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.10-3
- Fix for libnotify 0.7.0
- Fix version string in window title
- Update icon-cache scriptlets

* Wed Oct 27 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.10-2
- BR gtkhtml2-devel for contacts (#644169)
- BR libtar for backup feature
- Add patch for aplay and require alsa-utils

* Sun Apr 04 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.2.10-1
- Update to 0.2.10.

* Tue Nov 03 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.2.8-1
- Version bump to 0.2.8. (Red Hat Bugzilla #512626)
  * Encrypted data backup.
  * Exporting tasks to iCal file.
  * Text attributes are handled now in day notes editor.
  * Default alarm sound for task reminder.
  * Option to ignore weekend days in date calculator.
  * Added new calendar marker for birthdays.
  * Locale settings are used by default.
  * Slightly improved iCal support.
  * Unencrypted notes implemented.
  * Calendar printing improvements.
  * Spell checker support.
  * Showing map location of selected contact using Google Maps.
  * The order and width of columns is configurable.
  * System tray support improvements.
  * Many small improvements and fixes.
  * Translation updates: ca, cs, de, el, es, fi, fr, it, jp, nl, pl, ru, sv,
    tr and uk.
  * http://clayo.org/osmo/ChangeLog
- Fix for crash due to SIGABRT merged upstream.
- Updated the Source0 URL.
- Added 'Requires: xdg-utils' and 'BuildRequires: gtkspell-devel'.

* Sat Jul 25 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.2.4-7
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 19 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.2.4-6
- Fixed configure to ensure correct usage of CFLAGS and CPPFLAGS, and respect
  the environment's settings.

* Thu Apr 02 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.2.4-5
- Reenabled syncml support because libsyncml has been reverted. (Red Hat
  Bugzilla #479954)

* Thu Feb 26 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.2.4-4
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.2.4-3
- Temporarily disabled syncml support until Osmo works with libsyncml-0.5.0.
  (Red Hat Bugzilla #479954)

* Sun Dec 14 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.2.4-2
- Fixed crash due to SIGABRT using patch written by Tomasz Maka.

* Mon Nov 24 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.2.4-1
- Version bump to 0.2.4. (Red Hat Bugzilla #464484)
  * Exporting calendar events to iCal file.
  * Preliminary calendar and tasks list printing.
  * Improved birthdays browser.
  * Option to save data after every modification.
  * Global notification command for tasks.
  * Added --tinygui commandline option.
  * Many bug fixes and enhancements.
  * A temporary birthday logo.
  * Translation updates: cs, de, es, fr, ja, nl, pl and tr.
  * http://clayo.org/osmo/ChangeLog
- Timezone information fix accepted by upstream.

* Sun Jul 27 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.2.2-2
- Added post and postun scriptlets to update Gtk icon cache.

* Sun Jul 27 2008 Debarshi Ray <rishi@fedoraproject.org> - 0.2.2-1
- Version bump to 0.2.2.
- Added 'Requires: tzdata' and fixed the sources since libical does not provide
  timezone information anymore.
- Added 'BuildRequires: hicolor-icon-theme' and moved icons to
  /usr/share/icons/hicolor from /usr/share/pixmaps.

* Sun Feb 24 2008 David Nielsen <gnomeuser@gmail.com> - 0.2.0-2
- Rebuild for new libical.

* Sat Feb 09 2008 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.2.0-1
- Mass rebuild for new GCC... Done
- Version jump... Updated

* Mon Dec 24 2007 Jakub 'Livio' Rusinek <jakub.rusinek@gmail.com> - 0.1.6-1
- Christmas gift: new version... Updated
- Some indents to make more readable... Added

* Tue Dec 04 2007 Jakub 'Livio' Rusinek <liviopl.pl@gmail.com> - 0.1.4-1
- Version jump

* Fri Nov 23 2007 Jakub 'Livio' Rusinek <liviopl.pl@gmail.com> - 0.1.2-7
- Make flags... Fixed

* Wed Nov 21 2007 Jakub 'Livio' Rusinek <liviopl.pl@gmail.com> - 0.1.2-6
- Desktop file name... Fixed
- RPM_OPT_FLAGS... Fixed [without bumping new release]

* Wed Nov 21 2007 Jakub 'Livio' Rusinek <liviopl.pl@gmail.com> - 0.1.2-5
- Make flags... Fixed

* Wed Nov 21 2007 Jakub 'Livio' Rusinek <liviopl.pl@gmail.com> - 0.1.2-4
- Make flags... Fixed
- Desktop file installation... Fixed
- Pixmaps directory owning... Fixed

* Tue Nov 20 2007 Jakub 'Livio' Rusinek <liviopl.pl@gmail.com> - 0.1.2-3
- Doubled translations... Fixed
- Timestamps... Fixed

* Sun Nov 18 2007 Jakub 'Livio' Rusinek <liviopl.pl@gmail.com> - 0.1.2-2
- Forgot about translations... Fixed
- Wrong icon path in osmo.desktop... Fixed

* Sun Nov 18 2007 Jakub 'Livio' Rusinek <liviopl.pl@gmail.com> - 0.1.2-1
- Initial release
