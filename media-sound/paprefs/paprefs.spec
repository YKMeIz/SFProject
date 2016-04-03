Name:           paprefs
Version:        0.9.10
Release:        8%{?dist}
Summary:        Management tool for PulseAudio

License:        GPLv2+
URL:            http://freedesktop.org/software/pulseaudio/%{name}
Source0:        http://freedesktop.org/software/pulseaudio/%{name}/%{name}-%{version}.tar.xz
Patch0:         %{name}-%{version}-modules-path.patch
Patch1:         %{name}-%{version}-module-combine-sink.patch

BuildRequires:  gconfmm26-devel
BuildRequires:  libglademm24-devel 
BuildRequires:  lynx
BuildRequires:  desktop-file-utils
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  intltool
BuildRequires:  dbus-glib-devel

Requires:       pulseaudio-module-gconf
Requires:       PackageKit-session-service

%description
PulseAudio Preferences (paprefs) is a simple GTK based configuration dialog
for the PulseAudio sound server.

%prep
%setup -q
touch -r configure.ac configure.ac.stamp
%patch0 -p1 -b .modules-path
touch -r configure.ac.stamp configure.ac
%patch1 -p1 -b .module-combine-sink

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

desktop-file-install \
    --dir $RPM_BUILD_ROOT%{_datadir}/applications \
    --vendor= \
    --remove-category Application \
    $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang %{name}


%files -f %{name}.lang
%doc LICENSE doc/README
%{_bindir}/paprefs
%dir %{_datadir}/paprefs
%{_datadir}/paprefs/paprefs.glade
%{_datadir}/applications/paprefs.desktop


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Mar 01 2014 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.10-6
- Use module-combine-sink instead of module-combine

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.9.10-3
- Pulled some changes from upstream git to avoid a rebuild every PA release (RH #870899)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun  3 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.10-1
- Incorporate changes from Julian Sikorski (belegdol) (#827764):
  * update to 0.9.10
  * update URL and source fields; switch to xz tarball
  * drop obsoleted Group, Buildroot, %%clean and %%defattr
- Further spec clean-ups (buildroot-cleanup-on-install, indentation)
- Hard-coded dependency on build-time PulseAudio version dropped

* Thu May 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.9-12
- rebuild(pulseaudio)

* Sun Feb  5 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.9-11
- Make pulseaudio runtime dependency versioned

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.9-9
- Rebuild for pulseaudio 0.9.23 (F-16) / 1.1 (F-17)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 06 2011 Lubmir Rintel <lkundrak@v3.sk> 0.9.9-7
- Rebuild for pulseaudio-0.9.22

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> 0.9.9-6
- Requires: PackageKit-session-service (#561437)

* Mon Oct 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.9-5
- Rebuild to make sure we look for /usr/lib/pulse-0.9.21/modules/xxx instead of /usr/lib/pulse-0.9.19/modules/xxx
- https://bugzilla.redhat.com/show_bug.cgi?id=528557

* Wed Oct 14 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.9-4
- Fix mistag

* Wed Oct 14 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.9-3
- Rebuild to make sure we look for /usr/lib/pulse-0.9.19/modules/xxx instead of /usr/lib/pulse-0.9.16/modules/xxx

* Thu Sep 10 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.9-2
- Final 0.9.9 release

* Tue Aug 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.9-1.git20090825
- Add dbus-glib to deps

* Tue Aug 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.9-0.git20090825
- Snapshot

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Lennart Poettering <lpoetter@redhat.com> 0.9.8-1
- Update to 0.9.8

* Sun Mar 15 2009 Lubomir Rintel <lkundrak@v3.sk> - 0.9.7-5
- Try harder when looking for modules

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 9 2008 Matthias Clasen <mclasen@redhat.com> 0.9.7-3
- Handle locales properly

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.7-2
- Include intltool in deps

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9.7-1
- Update to 0.9.7

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.9.6-4
- Include unowned directory /usr/share/paprefs

* Thu Mar 27 2008 Christopher Aillon <caillon@redhat.com> - 0.9.6-3
- Add compile patch for GCC 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.6-2
- Autorebuild for GCC 4.3

* Wed Nov 28 2007 Julian Sikorski <belegdol[at]gmail[dot]com> 0.9.6-1
- Update to 0.9.6

* Thu Sep 25 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.6-0.2.svn20070925
- Update SVN snapshot

* Thu Aug 16 2007 Lennart Poettering <lpoetter@redhat.com> 0.9.6-0.1.svn20070816
- Get snapshot from SVN

* Thu Jul 2 2007 Eric Moret <eric.moret@epita.fr> 0.9.5-2
- Update license field

* Wed Jan 10 2007 Eric Moret <eric.moret@epita.fr> 0.9.5-1
- Initial package for Fedora
