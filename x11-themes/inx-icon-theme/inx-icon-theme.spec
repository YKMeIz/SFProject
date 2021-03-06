%define theme_name iNX-GTK

Summary: %{theme_name} icon theme
Name: inx-icon-theme
Version: 0.6
Release: 2.3
License: CC BY-NC-ND 3.0
Group: User Interface/Desktops
URL: http://deviantn7k1.deviantart.com/art/iNX-Icon-set-344494902
Source: inx.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch: noarch

%description
iNX is an Icon set based on the look and feel of iOS. It's inspired by
elementary ([link]) and Matrilineare ([link]). iNX contains a beautiful
set of Icons tailored for those that want a good looking workspace.

%prep
%setup -q -c
mv %{theme_name}/COPYING %{theme_name}/CREDITS .

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons
cp -a %{theme_name} $RPM_BUILD_ROOT%{_datadir}/icons

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README-Icons COPYING CREDITS
%{_datadir}/icons/%{theme_name}

%changelog
* Sun Jun 16 2013 Huaren Zhong <huaren.zhong@gmail.com> - 0.6
- Rebuild for Fedora
