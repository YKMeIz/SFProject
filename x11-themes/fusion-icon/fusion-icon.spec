Name:           fusion-icon
Version:        0.1
Release:        8%{?dist}
Epoch:          1
Summary:        Compiz Fusion panel applet
Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.compiz.org/
Source0:        http://cgit.compiz.org/~crdlb/fusion-icon/snapshot/%{name}-%{version}.tar.bz2
BuildArch:      noarch
ExcludeArch:    ppc64

BuildRequires:  python2-devel
BuildRequires:  desktop-file-utils

Requires:       ccsm
Requires:       %{name}-gtk = %{epoch}:%{version}-%{release}

Patch0:         fusion-icon-runpatch.patch
Patch3:         fusion-icon_add_marco.patch
Patch4:         fusion-icon_mate.patch
Patch5:         fusion-icon_mate-gnome.patch

%description
The Compiz Fusion Icon is a simple panel applet for starting and controlling
Compiz Fusion. Upon launch, it will attempt to start Compiz Fusion
automatically. You may need to select a window decorator, if one does not
appear.

%package gtk
Requires:  pygtk2
Requires:  %{name} = %{epoch}:%{version}-%{release}
Group:     User Interface/Desktops
Summary:   GTK UI for fusion-icon

%description gtk
This package provides the gtk UI for fusion-icon


%prep
%setup -q
sed -i -e 's,Encoding=UTF-8,,g' fusion-icon.desktop fusion-icon.desktop
%patch0
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{python_sitelib}/FusionIcon/interface_qt4/__init__.py
rm -f $RPM_BUILD_ROOT%{python_sitelib}/FusionIcon/interface_qt4/__init__.pyc
rm -f $RPM_BUILD_ROOT%{python_sitelib}/FusionIcon/interface_qt4/__init__.pyo
rm -f $RPM_BUILD_ROOT%{python_sitelib}/FusionIcon/interface_qt4/main.py
rm -f $RPM_BUILD_ROOT%{python_sitelib}/FusionIcon/interface_qt4/main.pyc
rm -f $RPM_BUILD_ROOT%{python_sitelib}/FusionIcon/interface_qt4/main.pyo

for file in $RPM_BUILD_ROOT%{python_sitelib}/FusionIcon/{environment,parser,interface,util,start,execute,__init__,data}.py; do
   chmod a+x $file
done
for file in $RPM_BUILD_ROOT%{python_sitelib}/FusionIcon/interface_gtk/{main,__init__}.py; do
   chmod a+x $file
done


%check
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/fusion-icon.desktop


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc COPYING
%{_bindir}/fusion-icon
%{_datadir}/applications/fusion-icon.desktop
%dir %{python_sitelib}/FusionIcon/
%{python_sitelib}/FusionIcon/*py*
%{_datadir}/icons/hicolor/*/apps/fusion-icon.png
%{_datadir}/icons/hicolor/scalable/apps/fusion-icon.svg
/usr/lib/python2.7/site-packages/fusion_icon-0.1.0-py2.7.egg-info

%files gtk
%{python_sitelib}/FusionIcon/interface_gtk/


%changelog
* Wed Mar 18 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:0.1-8
- rebuild for f22

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> -  1:0.1-4
- bump version

* Mon Oct 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> -  1:0.1-3
- build for fedora
- review package
- remove python_sitelib stuff
- fix icon cache scriptlets
- fix python2-devel BR
- fix non-executable-script

* Sat Sep 29 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.1-2
- add %%{?dist} tag again

* Sat Sep 29 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.1-1
- add Epoch tag
- improve spec file

* Wed Sep 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.1.0-0.9.5e2dc9git
- improve spec file
- remove qt subpackage

* Tue May 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 0.1.0-0.8.5e2dc9git
- build for mate

