%global theme_name Clearlooks-Phenix

Name: clearlooks-phenix
Version: 4
Release: 1%{?dist}
Summary: %{theme_name} theme
BuildArch: noarch

Group: User Interface/Desktops
License: GPLv3+
URL: http://www.jpfleury.net/en/software/clearlooks-phenix.php
# git clone git://jpfleury.indefero.net/jpfleury/clearlooks-phenix.git
# git checkout 3.0.15
# git archive --prefix=clearlooks-phenix-theme-3.0.15/ 3.0.15 | xz > clearlooks-phenix-theme-3.0.15.tar.xz
Source0: https://github.com/jpfleury/clearlooks-phenix/archive/v4.zip
#Source0: http://jpfleury.indefero.net/p/clearlooks-phenix/source/download/%{version}/

%description
%{theme_name} is a GTK+ 3 port of Clearlooks, the default theme
for GNOME 2. Style is also included for GTK2, Unity and for Metacity,
Openbox and Xfwm4 window managers.

%package common
Summary: Files common to %{theme_name} themes
Group: User Interface/Desktops

%description common
Files which are common to all %{theme_name} themes.


%package gtk2-theme
Summary: %{theme_name} GTK+2 themes
Group: User Interface/Desktops
Requires: %{name}-common = %{version}-%{release}, gtk2-engines

%description gtk2-theme
Themes for GTK+2 as part of the %{theme_name} theme.


%package gtk3-theme
Summary: %{theme_name} GTK+3 themes
Group: User Interface/Desktops
Requires: %{name}-common = %{version}-%{release}, gtk3

%description gtk3-theme
Themes for GTK+3 as part of the %{theme_name} theme.


%package xfwm4-theme
Summary: %{theme_name} Xfwm4 themes
Group: User Interface/Desktops
Requires: %{name}-common = %{version}-%{release}, xfwm4

%description xfwm4-theme
Themes for Xfwm4 as part of the %{theme_name} theme.


%package metacity-theme
Summary: %{theme_name} Metacity themes
Group: User Interface/Desktops
Requires: %{name}-common = %{version}-%{release}, metacity

%description metacity-theme
Themes for Metacity as part of the %{theme_name} theme.


%package openbox-theme
Summary: %{theme_name} Openbox themes
Group: User Interface/Desktops
Requires: %{name}-common = %{version}-%{release}, openbox

%description openbox-theme
Themes for Openbox as part of the %{theme_name} theme.


%prep
%setup -q -n %{name}-%{version}

%build

%install
mkdir -p %{buildroot}%{_datadir}/themes/%{theme_name}/
for dir in gtk-2.0 gtk-3.0 metacity-1 openbox-3 wallpapers xfwm4; do
  cp -R $dir %{buildroot}%{_datadir}/themes/%{theme_name}/
done
install -Dpm 0644 index.theme %{buildroot}%{_datadir}/themes/%{theme_name}/

rm doc/images.sh.txt

%files common
%doc doc/*.txt
%doc doc/*.mkd
%{_datadir}/themes/%{theme_name}

%files gtk2-theme
%{_datadir}/themes/%{theme_name}/gtk-2.0/

%files gtk3-theme
%{_datadir}/themes/%{theme_name}/gtk-3.0/

%files xfwm4-theme
%{_datadir}/themes/%{theme_name}/xfwm4/

%files metacity-theme
%{_datadir}/themes/%{theme_name}/metacity-1/

%files openbox-theme
%{_datadir}/themes/%{theme_name}/openbox-3/


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jan 26 2013 Richard Marko <rmarko@fedoraproject.org> - 3.0.15-1
- Version bump
- Splitting to multiple subpackages

* Sat Jan 26 2013 Richard Marko <rmarko@fedoraproject.org> - 3.0.14-1
- Initial packaging
