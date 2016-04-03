# Review: https://bugzilla.redhat.com/show_bug.cgi?id=442473

Name:           parcellite
Version:        1.1.7
Release:        3%{?prerelease:.%{?prerelease}}%{?dist}
Summary:        A lightweight GTK+ clipboard manager

Group:          User Interface/Desktops
License:        GPLv3+
URL:            http://parcellite.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

# Fedora bug:   https://bugzilla.redhat.com/show_bug.cgi?id=1038899
# upstream bug: http://sourceforge.net/p/parcellite/bugs/101/
# upstream fix: http://sourceforge.net/p/parcellite/code/491/
Patch0:         parcellite-1.1.7-issue-107.patch

# upstream bug: http://sourceforge.net/p/parcellite/bugs/109/
# upstream fix: http://sourceforge.net/p/parcellite/code/492/
Patch1:         parcellite-1.1.7-issue-109.patch

# upstream bug: http://sourceforge.net/p/parcellite/bugs/108/
# upstream fix: http://sourceforge.net/p/parcellite/code/493/
Patch2:         parcellite-1.1.7-issue-108.patch

# upstream bug: http://sourceforge.net/p/parcellite/code/496/
# upstream fix: http://sourceforge.net/p/parcellite/code/495/ and
Patch3:         parcellite-1.1.7-update-russian-translation.patch

# upstream fix: http://sourceforge.net/p/parcellite/code/497/
Patch4:         parcellite-1.1.7-fix-case-sensitive-search.patch

# upstream bug: http://sourceforge.net/p/parcellite/bugs/111/
# upstream fix: http://sourceforge.net/p/parcellite/code/498/
Patch5:         parcellite-1.1.7-issue-111.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk2-devel >= 2.10.0 
BuildRequires:  desktop-file-utils, intltool >= 0.23

%description
Parcellite is a stripped down, basic-features-only clipboard manager with a 
small memory footprint for those who like simplicity.

In GNOME and Xfce the clipboard manager will be started automatically. For 
other desktops or window managers you should also install a panel with a 
system tray or notification area if you want to use this package.


%prep
%setup -q
# remove useless files
rm -rf autom4te.cache */*~ || :
%patch0 -p0 -b .issue107
%patch1 -p0 -b .issue109
%patch2 -p0 -b .issue108
%patch3 -p0 -b .update-russian-translation
%patch4 -p0 -b .fix-case-sensitive-search
%patch5 -p0 -b .issue111

%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p'
%find_lang %{name}

desktop-file-install \
    %if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
        --vendor fedora \
    %endif
    --delete-original \
    --remove-category=Application \
    --remove-only-show-in=Old \
    --dir=%{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install \
    --delete-original \
    --add-category=TrayIcon \
    --add-only-show-in="GNOME;KDE;LXDE;MATE;Razor;ROX;TDE;Unity;XFCE;" \
    --dir=%{buildroot}%{_sysconfdir}/xdg/autostart \
    %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-startup.desktop


%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README NEWS
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{name}-startup.desktop
%{_bindir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_mandir}/man1/%{name}.1.*


%changelog
* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 03 2014 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.7-2
- Add 6 upstream patches to fix three segfaults (#1038899 is one of them),
  case-sensitive search, search-as-you-type and updates Russian translations

* Wed Oct 16 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.7-1
- Update to 1.1.7 (#1019649)

* Sun Aug 04 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.6-1
- Update to 1.1.6 (#991766, fixes and #989098)
- Remove upstreamed patch for German translation

* Thu Jul 25 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.5-2
- Fix typo in German translation

* Wed Jul 24 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5 (#987384, fixes #919693 and #919696)
- Remove upstreamed or unnecessary patches

* Tue May 14 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.4-3
- Fix desktop vendor conditionals
- Add aarch64 support (#926310)

* Wed May 01 2013 Jon Ciesla <limburgher@gmail.com> - 1.1.4-2
- Drop desktop vendor tag.

* Sun Jan 27 2013 Christoph Wickert <cwickert@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4
- Update de-po.patch

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-0.3.rc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.2-0.2.rc5
- Don't ship prebuilt binaries (#800644)
- Fix build error with glib2 >= 2.30

* Sat Mar 03 2012 Christoph Wickert <cwickert@fedoraproject.org> - 1.0.2-0.1.rc5
- Update to 1.0.2 RC5 (#730240)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 17 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.2-2
- Add patch to fix DSO linking (#565054)

* Fri Jan 01 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 18 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1
- Remove both patches as all fixes got upstreamed

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.9-1
- Update to 0.9
- Fix Control+Click behaviour
- Small corrections to German translation

* Sat Apr 19 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.8-1
- Update to 0.8

* Sat Apr 19 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.7-2
- No longer require lxpanel
- Preserve timestamps during install
- Include NEWS in doc

* Sat Apr 12 2008 Christoph Wickert <cwickert@fedoraproject.org> - 0.7-1
- Initial Fedora RPM
