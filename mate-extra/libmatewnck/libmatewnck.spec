Name:           libmatewnck
Version:        1.6.1
Release:        1%{?dist}
Summary:        MATE Desktop Window Navigator Construction Kit libraries

Group:          System Environment/Libraries
License:        LGPLv2+ and GPLv2+
URL:            http://www.mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz

BuildRequires:  cairo-gobject-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk2-devel
BuildRequires:  gtk-doc
BuildRequires:  libX11-devel
BuildRequires:  libXres-devel
BuildRequires:  mate-common
BuildRequires:  mate-doc-utils
BuildRequires:  startup-notification-devel

%description
Window navigator construction Kit for MATE Desktop

%package devel
Summary:  Development libraries and headers for libmatewnck
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for libmatewnck

%prep
%setup -q

%build
%configure                       \
   --disable-static              \
   --enable-gtk-doc-html         \
   --enable-startup-notification \
   --with-x                      

make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install

find %{buildroot} -name '*.la' -exec rm -rf {} ';'
find %{buildroot} -name '*.a' -exec rm -rf {} ';'

%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc AUTHORS COPYING README
%{_libdir}/girepository-1.0/Matewnck-1.0.typelib
%{_libdir}/libmatewnck.so.*
%{_datadir}/gtk-doc/html/libmatewnck
%{_bindir}/matewnck-urgency-monitor
%{_bindir}/matewnckprop

%files devel
%{_libdir}/libmatewnck.so
%{_libdir}/pkgconfig/libmatewnck.pc
%{_includedir}/libmatewnck/
%{_datadir}/gir-1.0/Matewnck-1.0.gir

%changelog
* Wed Jul 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Fri Feb 08 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.1-1
- Update to latest upstream release
- Update configure flags
- Redo BRs to old style
- Add V=1 to make flags

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- remove duplicate .so from files
- change build requires style
- move .gir to devel package

* Sun Aug 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Remove build-requires field from devel package, remove static libs, bump release number.

* Mon Jul 30 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-2
- Remove unnecessary packages from build-requires field.

* Tue Jul 17 2012 Dan Mashal <dan.mashal@gmail.com> 1.4.0-1
- Initial build
