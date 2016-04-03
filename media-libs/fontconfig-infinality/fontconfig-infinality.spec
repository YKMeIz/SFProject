%define	name	fontconfig-infinality
%define version	1
%define release	20120615_1

Summary: A configurable fontconfig configuration meant to be used in conjunction with Freetype patches from http://www.infinality.net.  It should drop cleanly into most existing fontconfig setups.  While this package will work without infinality patches, much of it is tailored to rendering when using those patches, and may not look correct otherwise.  This package also includes an /etc/profile.d file called infinality-settings.sh, which sets system-wide runtime variables to work in conjunction with the Infinality freetype package.  
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
#Group: System/Fonts/TTF
BuildArch: noarch
BuildRoot: %{_builddir}/%{name}-root
URL: http://www.infinality.net/
Distribution: Fedora
Vendor: Infinality
Packager: infinality@infinality.net
Provides: fontconfig-infinality
Requires: freetype-infinality 
BuildRequires: git
Requires: fontconfig
Obsoletes: fonts-config
Obsoletes: infinality-settings

%description
A configurable fontconfig configuration meant to be used in conjunction with Freetype patches from http://www.infinality.net.  It should drop cleanly into most existing fontconfig setups.  While this package will work without infinality patches, much of it is tailored to rendering when using those patches, and may not look correct otherwise.  This package also includes an /etc/profile.d file called infinality-settings.sh, which sets system-wide runtime variables to work in conjunction with the Infinality freetype package.  


%prep
exit 0

%build
exit 0

%install
mkdir -p %{buildroot}/etc/fonts/
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}

touch fontconfig-infinality
rm -rf fontconfig-infinality
git clone git://github.com/Infinality/fontconfig-infinality.git
cp -R fontconfig-infinality/* %{buildroot}/etc/fonts/
cd %{buildroot}/etc/fonts/
tar jcf %{buildroot}/usr/share/doc/%{name}-%{version}-%{release}/fontconfig-infinality-%{version}-%{release}.tar.bz2 conf.d conf.avail infinality

exit 0

%clean
exit 0

%files
%defattr(-,root,root)
%config %{_sysconfdir}/fonts/infinality
%{_sysconfdir}/fonts/conf.avail/52-infinality.conf
%{_sysconfdir}/fonts/conf.d/52-infinality.conf
/usr/share/doc/%{name}-%{version}-%{release}/fontconfig-infinality-%{version}-%{release}.tar.bz2

%changelog

* Thu Nov 20 2011 Infinality <infinality@infinality.net>
- Remove Canwell replacments from local.conf

* Thu Nov 17 2011 Infinality <infinality@infinality.net>
- New version created

