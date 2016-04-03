Name:           imagination          
Version:        3.0
Release:        10%{?dist}
Summary:        A lightweight and simple GTK based DVD slide show creator

Group:          Applications/Multimedia
License:        GPLv2
URL:            http://imagination.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/imagination/imagination/%{version}/%{name}-%{version}.tar.gz
Patch0:         imagination-3.0-plugins.patch
Patch1:         imagination-3.0-docfix.patch
# Fix icon references to not require gnome-icon-theme-legacy
Patch2:         imagination-3.0-icon_fix.patch
# Fixed in upstream trunk
# http://imagination.svn.sourceforge.net/viewvc/imagination/trunk/configure.in?view=patch&r1=599&r2=598&pathrev=599
Patch3:         imagination-3.0-configure.in.patch

BuildRequires:  gtk2-devel
BuildRequires:  sox-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  libxslt docbook-style-xsl
BuildRequires:  intltool
BuildRequires:  hicolor-icon-theme
BuildRequires:  desktop-file-utils
BuildRequires:  libtool

Requires:       ffmpeg
Requires:       hicolor-icon-theme
Requires:       gnome-icon-theme


%description
Imagination is a lightweight and simple DVD slide show maker written in C
language and built with the GTK+2 toolkit.


%prep
%setup -q
%patch0 -b .plugins
%patch1 -b .docfix
%patch2 -p1 -b .iconfix
%patch3 -p1 -b .conffix


%build
# Necessary due to patched configure.in
/bin/bash ./autogen.sh
LDFLAGS=`pkg-config --libs gmodule-2.0`; export LDFLAGS
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Move documentation so it will go in the right directory
rm -rf $(pwd)/_tmpdoc && mkdir $(pwd)/_tmpdoc
mv -f %{buildroot}%{_docdir}/%{name}/html $(pwd)/_tmpdoc/

# Remove unnecessary library files
rm %{buildroot}%{_libdir}/%{name}/*.la

%find_lang %{name}

desktop-file-validate %{buildroot}/%{_datadir}/applications/imagination.desktop

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README _tmpdoc/*
%{_bindir}/imagination
%{_datadir}/applications/*
%{_datadir}/icons/*
%{_datadir}/%{name}
%{_libdir}/%{name}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%changelog
* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.0-10
- Rebuilt for x264/FFmpeg

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 3.0-9
- Mass rebuilt for Fedora 19 Features

* Tue May 01 2012 Richard Shaw <hobbes1069@gmail.com> - 3.0-8
- Fix FTBFS.

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun May  1 2011 Richard Shaw <hobbes1069@gmail.com> - 3.0-6
- Fixed minor issues with spec file for packaging compliance.

* Sat Apr 23 2011 Richard Shaw <hobbes1069@gmail.com> - 3.0-5
- Added upstream patch to fix building for Fedora 13

* Mon Apr 18 2011 Richard Shaw <hobbes1069@gmail.com> - 3.0-4
- Patched to use new icon names instead of requiring a legacy package.

* Mon Apr 18 2011 Richard Shaw <hobbes1069@gmail.com> - 3.0-3
- Fixed missing icons thanks to https://bugzilla.rpmfusion.org/show_bug.cgi?id=1617#c3

* Sat Apr 16 2011 Richard Shaw <hobbes1069@gmail.com> - 3.0-2
- Updated spec file to correct documentation location.

* Thu Apr 14 2011 Richard Shaw <hobbes1069@gmail.com> - 3.0-1
- Build for initial release.
