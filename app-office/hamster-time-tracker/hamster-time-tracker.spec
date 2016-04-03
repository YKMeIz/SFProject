Name:       hamster-time-tracker
Version:    1.04
Release:    3%{?dist}
Summary:    The Linux time tracker

License:    GPLv3+
URL:        http://projecthamster.wordpress.com/
# wget --content-disposition https://github.com/projecthamster/hamster/archive/%{name}-%{version}.tar.gz
Source0:    hamster-%{name}-%{version}.tar.gz
Source1:    %{name}.appdata.xml

# Move service files to bindir rather than libdir
# Stop gschema installation etc.
# http://fedoraproject.org/wiki/Packaging:ScriptletSnippets#GConf
Patch0:     %{name}-1.03.3-file-locations.patch

# Correct service files to point to BINDIR rather than LIBDIR
Patch1:     %{name}-1.03.3-service-dbus1.patch
Patch2:     %{name}-1.03.3-service-dbus2.patch

# Notification fixes. See URLs in changelog for details
# Patch3:     %{name}-1.03.3-notification-fix.patch

BuildArch:  noarch
BuildRequires:    desktop-file-utils
BuildRequires:    gettext intltool
BuildRequires:    glib2-devel dbus-glib
BuildRequires:    docbook-utils gnome-doc-utils libxslt
Requires:         dbus
Requires:         hicolor-icon-theme
Requires:         bash-completion
Requires:         gnome-python2-gconf
Requires:         gnome-python2-libwnck
Requires:         pyxdg

BuildRequires: GConf2
Requires(pre): GConf2
Requires(post): GConf2
Requires(preun): GConf2


%description
Project Hamster is time tracking for individuals. It helps you to keep track on
how much time you have spent during the day on activities you choose to track. 

Whenever you change from doing one task to other, you change your current
activity in Hamster. After a while you can see how many hours you have spent on
what. Maybe print it out, or export to some suitable format, if time reporting
is a request of your employee. 

%prep
%setup -q -n hamster-%{name}-%{version}
%patch0
%patch1
%patch2
#%patch3

# remove shebang
sed -ibackup '1d' src/hamster/today.py

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
export LINKFLAGS="-Wl,-z,relro"

./waf configure -vv --prefix=%{_prefix} --datadir=%{_datadir} 
./waf build -vv %{?_smp_mflags}


%install
./waf install --destdir=%{buildroot}

mkdir -p %{buildroot}/%{_datadir}/appdata/
cp %{SOURCE1} %{buildroot}/%{_datadir}/appdata/  -v

%find_lang %{name} --with-gnome

# Fedora 19's build barfs if I mention them all together using a wildcard.
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-overview.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/hamster-windows-service.desktop

%pre
%gconf_schema_prepare %{name}
%gconf_schema_obsolete %{name}

%post
%gconf_schema_upgrade %{name}
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%preun
%gconf_schema_remove %{name}

%files -f %{name}.lang
%doc AUTHORS COPYING MAINTAINERS NEWS 
%{_bindir}/hamster*
%{python_sitelib}/hamster
%{_datadir}/%{name}/
%{_datadir}/dbus-1/services/*hamster*.service

%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/hamster.bash

%{_sysconfdir}/gconf/schemas/hamster-time-tracker.schemas

%{_datadir}/applications/hamster*desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%dir %{_datadir}/gnome/help

%{_datadir}/appdata/
%{_datadir}/appdata/%{name}.appdata.xml


%changelog
* Tue Jul 15 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.04-3
- Add requires on pyxdg

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.04-1
- Update to latest upstream release. 

* Mon Dec 30 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-6
- Update desktop-file-validate command for F19

* Sat Dec 28 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-5
- Add patch for notification fix
- https://bugzilla.redhat.com/show_bug.cgi?id=1046991
- https://github.com/projecthamster/hamster/pull/127
- https://github.com/projecthamster/hamster/pull/117

* Tue Dec 24 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-4
- Add wnck dependency so users can use workspaces out of the box
- https://bugzilla.redhat.com/show_bug.cgi?id=1046077

* Tue Dec 17 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-3
- Add missing gnome-python2-gconf requirement
- https://bugzilla.redhat.com/show_bug.cgi?id=1043564

* Mon Dec 02 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-2
- Fixes as per https://bugzilla.redhat.com/show_bug.cgi?id=1036254
- Correct schame functions
- Own gnome help dir
- Own bash completion dir
- schema and bash completion files do not need to be %config
- https://lists.fedoraproject.org/pipermail/packaging/2013-December/009834.html

* Sat Nov 30 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 1.03.3-1
- Initial rpm build

