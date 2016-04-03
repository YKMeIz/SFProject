Name:           pavucontrol
Version:        3.0
Release:        5%{?dist}
Summary:        Volume control for PulseAudio

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://freedesktop.org/software/pulseaudio/%{name}
Source0:        http://freedesktop.org/software/pulseaudio/%{name}/%{name}-%{version}.tar.xz
# Fix icons with adwaita-icon-theme
Patch0:         0001-Use-freedesktop.org-standard-icon-name.patch

BuildRequires:  pulseaudio-libs-devel >= 3.0
BuildRequires:  gtkmm30-devel
BuildRequires:  libsigc++20-devel lynx
BuildRequires:  desktop-file-utils
BuildRequires:  libcanberra-devel
BuildRequires:  intltool

%description
PulseAudio Volume Control (pavucontrol) is a simple GTK based volume control
tool ("mixer") for the PulseAudio sound server. In contrast to classic mixer
tools this one allows you to control both the volume of hardware devices and
of each playback stream separately.

%prep
%setup -q
%patch0 -p1

%build
%configure
make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make V=1 install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/usr/share/doc/pavucontrol/README
rm $RPM_BUILD_ROOT/usr/share/doc/pavucontrol/README.html
rm $RPM_BUILD_ROOT/usr/share/doc/pavucontrol/style.css

%find_lang %{name}

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/pavucontrol.desktop

%files -f %{name}.lang
%license LICENSE
%doc doc/README
%{_bindir}/pavucontrol
%{_datadir}/pavucontrol
%{_datadir}/applications/pavucontrol.desktop

%changelog
* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 3.0-5
- Patch to work with the default icon theme (bug 1249198)

* Sat Aug 01 2015 Julian Sikorski <belegdol@fedoraproject.org> - 3.0-4
- Added gnome-icon-theme-legacy to Requires (bug 1249198)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 3.0-1
- Update to 3.0
- Use license macro for the LICENCE file
- Use desktop-file-validate instead of desktop-file-install

* Sat Feb 28 2015 Kevin Fenzi <kevin@scrye.com> 2.0-10
- Rebuild for new gcc

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.0-9
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Aug 28 2014 Hans de Goede <hdegoede@redhat.com> - 2.0-8
- Add a patch fixing various crashes due to referencing freed memory (#1133339)
- Cherry-pick some other fixes from upstream git

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 2.0-5
- Drop obsolete libglademm24-devel build dep

* Tue Nov 12 2013 Julian Sikorski <belegdol@fedoraproject.org> - 2.0-4
- Added support for AAC passthrough

* Wed Oct 23 2013 Bruno Wolff III <bruno@wolff.to> - 2.0-3
- Rebuild seems to fix segfaulting issue (bz 1021118)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 09 2013 Julian Sikorski <belegdol@fedoraproject.org> - 2.0-1
- Updated to 2.0
- Made the make calls verbose
- Dropped explicit pulsaudio-libs dependency
- Updated the version in the pulseaudio-libs-devel BR

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 03 2012 Jonathan Steffan <jsteffan@fedoraproject.org> - 1.0-2
- Merge in patch from BZ#588724

* Mon Sep 03 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-1
- Updated to 1.0
- Switched to .xz sources
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Updated Source0 and URL
- Switched to gtk3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 14 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.10-1
- New upstream 0.9.10

* Thu Sep 10 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.9-1
- Final 0.9.9

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-0.test1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.9-1
- Preview of upcoming 0.9.9

* Mon Apr 13 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.8-1
- New upstream release 0.9.8

* Fri Apr 10 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.7-6
- Third preview of upcoming 0.9.8

* Thu Mar 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.7-5
- Second preview of upcoming 0.9.8

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.7-4
- Preview of upcoming 0.9.8

* Thu Oct 9 2008 Matthias Clasen  <mclasen@redhat.com> 0.9.7-3
- Handle locales properly

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.7-2
- Add intltool to deps

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.7-1
- Update to 0.9.7

* Tue Jul 15 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.7-0.1.git20080715
- Update from GIT snapshot

* Fri Mar 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.6-1
- Update to 0.9.6

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.5-2
- Autorebuild for GCC 4.3

* Wed Nov 28 2007 Julian Sikorski <belegdol[at]gmail[dot]com> 0.9.5-1
- Update to 0.9.5

* Tue Sep 25 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.5-0.4.svn20070925
- Update from SVN

* Wed Sep 5 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.5-0.3.svn20070905
- Add versioned dependency on pulseaudio-libs

* Wed Sep 5 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.5-0.2.svn20070905
- Update from SVN snapshot

* Thu Aug 16 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.5-0.1.svn20070816
- Update from SVN snapshot

* Sat Sep  9 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.4-3
- Spec file cleanup.

* Sat Sep  9 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.4-2
- Add BuildRequires for desktop-file-utils.

* Fri Sep  8 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.4-1
- Update to 0.9.4
- Fix installation of desktop file.

* Sun Aug 20 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.3-1
- Update to 0.9.3

* Sun Jul  9 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.2-1
- Update to 0.9.2

* Thu Jun  8 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.1-1
- Update to 0.9.1

* Mon May 29 2006 Pierre Ossman <drzeus@drzeus.cx> 0.9.0-1
- Initial package for Fedora Extras
