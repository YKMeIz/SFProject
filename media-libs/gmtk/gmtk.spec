Name:           gmtk
Version:        1.0.9
Release:        1%{?dist}
Summary:        Library of common functions and widgets for gnome-mplayer and gecko-mediaplayer 

License:        GPLv2+
URL:            http://code.google.com/p/%{name}/ 
Source0:        http://%{name}.googlecode.com/files/%{name}-%{version}.tar.gz

BuildRequires:  alsa-lib-devel
BuildRequires:  gettext
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  pulseaudio-libs-devel
Requires:       mplayer

%description
Library of common functions and widgets for gnome-mplayer and gecko-mediaplayer

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
#remove intrusive docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}
%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc ChangeLog COPYING INSTALL
%{_libdir}/*.so.*

%files devel
%doc
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Thu Apr 24 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.9-1
- Updated to 1.0.9

* Mon May 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.8-2
- Rebuilt for x264/FFmpeg

* Sun Mar 03 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.8-1
- Updated to 1.0.8

* Sat Jan 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.7-2
- Avoid an %%{_isa} dependency on mplayer

* Tue Oct 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.7-1
- Updated to 1.0.7

* Fri Apr 06 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.6-1
- Updated to 1.0.6

* Thu Dec 29 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.5.0-1
- Updated to 1.0.5 (as 1.0.5.0 to be newer than 1.0.5b2)

* Tue Nov 15 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.5b1-3
- Removed GConf logic since F-14 is going EOL soon
- Added %%{?_isa} to explicit Requires

* Sun Oct 09 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.5b1-2
- Updated to upstream 1.0.5b1 sources
- Fixed the source URL

* Wed Sep 28 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.0.5b1-1
- Initial RPM release
