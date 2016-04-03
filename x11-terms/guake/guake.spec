Name:           guake
Version:        0.4.4
Release:        11%{?dist}
Summary:        Drop-down terminal for GNOME

Group:          Applications/System
License:        GPLv2+
URL:            http://www.guake.org/
Source0:        http://guake.org/files/%{name}-%{version}.tar.gz
Patch1:         0001-Fix-notification.patch
Patch2:         0001-Let-allow-the-signal.SIGTERM-to-fail.patch
Patch3:         0001-Fix-regex-to-include-the-port-number-when-there-is-o.patch
# Upstream patch at https://github.com/Guake/guake/pull/75
Patch4:         0001-Include-bpython-and-ipython-as-interpreters.patch

# Not used here -- official release --
#Source0:        %{name}-%{version}.20090321git.tar.gz
# Source generated from
# git clone git://repos.guake-terminal.org/guake
# cd guake
# ./autogen.sh
# cd ../
# tar zcvf guake-0.3.1.20090321git.tar.gz guake/
# ---------------------------------------------

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel gtk2-devel gettext desktop-file-utils perl(XML::Parser) GConf2-devel
BuildRequires:  pygtk2-devel >= 2.10 intltool vte
Requires:       pygtk2 >= 2.10 vte notify-python pygtk2-libglade gnome-python2-gconf dbus-python
Requires:       desktop-notification-daemon pyxdg

Requires(pre):   GConf2
Requires(post):  GConf2
Requires(preun): GConf2

%description
Guake is a drop-down terminal for Gnome Desktop Environment,
so you just need to press a key to invoke him,
and press again to hide.

%prep
%setup -q 

# Enables to pass the configure without problem concerning python vte library
sed -i -e 's|if test -z "$ac_pvte_result"; then|if test -z "" ; then|g' configure
sed -i -e "s|include <glib/gtypes.h>|include <glib.h>|" src/globalhotkeys/keybinder.h

%patch1 -p1 -b .
%patch2 -p1 -b .
%patch3 -p1 -b .
%patch4 -p1 -b .

%build
%configure --disable-schemas-install --disable-static
make %{?_smp_mflags}


%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

desktop-file-install --vendor=""                           \
  --delete-original                                        \
  --dir=%{buildroot}%{_datadir}/applications               \
  %{buildroot}%{_datadir}/applications/%{name}.desktop


desktop-file-install --vendor=""                           \
  --delete-original                                        \
  --dir=%{buildroot}%{_datadir}/applications               \
  %{buildroot}%{_datadir}/applications/%{name}-prefs.desktop


%find_lang %{name}
rm -f %{buildroot}%{python_sitearch}/%{name}/globalhotkeys.la


if [ "%{python_sitearch}" != "%{python_sitelib}" ]; then
  mv %{buildroot}%{python_sitelib}/%{name}/* %{buildroot}%{python_sitearch}/%{name}/
fi

%pre
%gconf_schema_prepare %{name}

%post
%gconf_schema_upgrade %{name}

%preun
%gconf_schema_remove %{name}

%posttrans
killall gconfd-2 > /dev/null || :

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING README TODO
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/%{name}
%{_bindir}/%{name}-prefs
%{python_sitearch}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-prefs.desktop
%{_datadir}/dbus-1/services/org.guake.Guake.service
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}
%{_mandir}/man1/guake.1.gz
%{_datadir}/icons/hicolor/*/apps/%{name}*.png

%changelog
* Mon Sep 30 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.4-11
- Remove the Fix-focus-issue-on-gnome-shell patch which seems no longer needed

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 21 2013 Ralph Bean <rbean@redhat.com> - 0.4.4-9
- Patch to include bpython and ipython as interpreters.

* Mon Feb 25 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.4-8
- Replace the Requires on notification-daemon by a Requires on desktop-notification-daemon

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.4-6
- Let's be a little more brutal in our killall since we know the guilty guy

* Fri Nov 02 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.4-5
- Add patch to handle the selection of url/link correctly

* Thu Aug 02 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.4-4
- Fix indentation in the patch 3

* Wed Aug 01 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.4-3
- Add patch to allow os.kill(pid, signal.SIGTERM) to fails

* Fri Jul 27 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.4-2
- Re-add the fix notification patch

* Fri Jul 27 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.4-1
- Update to 0.4.4
- Clean a little bit the spec according to new guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.3-3
- Add patch to fix the focus issue: RHBZ#828243 - Guake Trac #436

* Tue Jun 12 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.3-2
- Temporary fix for the globalhotkeys

* Fri Jun 08 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.3-1
- Update to 0.4.3
- Add Requires: notification-daemon
- Drops patches

* Mon Feb 27 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.2-7
- Fix notifications for non-GNOME DE not having the right library RHBZ#710586

* Sat Jan 14 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4.2-6
- Fix FTBFS by remove some includes in the file keybinder.c

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.4.2-4
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 24 2010 pingou <pingou@pingoured.fr> - 0.4.2-2
- Fix 626303 (import of port from proxy as int and not as string)

* Tue Aug 03 2010 pingou <pingou@pingoured.fr> - 0.4.2-1
- Update to 0.4.2

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat May 08 2010 pingou <pingou@pingoured.fr> - 0.4.1-4
- Change the name.schema to name for the gconf macro

* Sat May 08 2010 pingou <pingou@pingoured.fr> - 0.4.1-3
- Use the gconf_schema macro instead of the former code
- Add the posttrans part

* Thu Feb 04 2010 pingou <pingou@pingoured.fr> - 0.4.1-2
- Rebuild to include French translations

* Tue Feb 02 2010 pingou <pingou@pingoured.fr> - 0.4.1-1
- Update to 0.4.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 07 2009 pingou <pingou@pingoured.fr> - 0.4.0-1
- Update to version 0.4.0

* Sat Mar 21 2009 pingou <pingou@pingoured.fr> - 0.3.1-10.20090321git
- New version from git

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-9.20090210git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 pingou <pingou@pingoured.fr> - 0.3.1-8.20090210git
- Correct setup -n

* Tue Feb 10 2009 pingou <pingou@pingoured.fr> - 0.3.1-7.20090210git
- Correct typo in the release number

* Tue Feb 10 2009 pingou <pingou@pingoured.fr> - 0.3.1-6.20090210git
- Add a .desktop file for the preferences (see: http://trac.guake-terminal.org/ticket/86 )
- New version from git
- Correct the tab

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.1-5
- Rebuild for Python 2.6

* Wed Nov 26 2008 pingou <pingou@pingoured.fr> - 0.3.1-4
- Quick and dirty trick before upstream patch

* Thu Nov 20 2008 pingou <pingou@pingoured.fr> - 0.3.1-3
- Correct the Source0

* Mon Aug 25 2008 pingou <pingou@pingoured.fr> - 0.3.1-2
- Add pygtk2 >= 2.10 in the BR

* Mon Aug 25 2008 pingou <pingou@pingoured.fr> - 0.3.1-1
- New owner
- New upstream release 0.3.1

* Thu Jul 10 2008  <lokthare@gmail.com> - 0.2.2-5
- Remove NEWS from the doc
- Add dbus-python in Requires 

* Tue Jul  1 2008  <lokthare@gmail.com> - 0.2.2-4
- Add BR for GConf
- Fix schemas file

* Sun Jun  8 2008 Jean-François Martin <lokthare@gmail.com> 0.2.2-3
- Don't own /etc/gconf/schemas/
- Don't replace /etc/gconf/schemas/guake.schemas config file
- Remove globalhotkeys.la

* Fri Jun  6 2008 Jean-François Martin <lokthare@gmail.com> 0.2.2-2
- Fix gconf schema install
- Disable static library

* Wed Jun  4 2008 Jean-François Martin <lokthare@gmail.com> 0.2.2-1
- Initial release
