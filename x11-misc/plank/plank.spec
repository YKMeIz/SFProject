Name:           plank
Version:        0.6.0
Release:        3%{?dist}
Summary:        A port of docky to Vala

License:        GPLv3+
URL:            http://wiki.go-docky.com/index.php?title=Plank:Introduction
Source0:        https://launchpad.net/%{name}/1.0/%{version}/+download/%{name}-%{version}.tar.xz

BuildRequires:  gnome-common
BuildRequires:  libgee-devel
BuildRequires:  vala
BuildRequires:  gobject-introspection-devel
BuildRequires:  vala-tools
BuildRequires:  glib2-devel
BuildRequires:  libwnck3-devel
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  libdbusmenu-gtk3-devel
BuildRequires:  libdbusmenu-devel

%if 0%{?fedora} >= 21
BuildRequires:  bamf-devel
%else
BuildRequires:  bamf3-devel
%endif

Requires:       bamf-daemon

%description
A very simple dock written in Vala.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       vala-tools

%description devel
Development files for %{name}

%prep
%setup -q

%build
%configure
# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Fix unused-direct-shlib-dependency from rpmlint
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags} V=1

%install
make install DESTDIR=%{buildroot}
# Fedora does not use apport
rm -f %{buildroot}%{_sysconfdir}/apport/crashdb.conf.d/%{name}-crashdb.conf
rm -f %{buildroot}%{_datadir}/apport/package-hooks/source_%{name}.py
# Remove built .la file
rm -f %{buildroot}%{_libdir}/lib%{name}.la
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.0
%{_libdir}/lib%{name}.so.0.0.0
%{_mandir}/man1/%{name}.1*
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.svg

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}
%{_datadir}/vala/vapi/%{name}.vapi
%{_datadir}/vala/vapi/%{name}.deps

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Wesley Hearn <whearn@redhat.com> - 0.6.0-1
- New upstream version

* Mon Feb 17 2014 Wesley Hearn <whearn@redhat.com> - 0.5.0-4
- Build against bamf-devel and not bamf4-devel in Fedora 21+

* Mon Feb 17 2014 Wesley Hearn <whearn@redhat.com> - 0.5.0-3
- Removed Group from devel package

* Fri Feb 14 2014 Wesley Hearn <whearn@redhat.com> - 0.5.0-2
- Cleaned up SPEC file

* Tue Jan 14 2014 Wesley Hearn <whearn@redhat.com> - 0.5.0-1
- Updating to new upstream release

* Thu Aug 08 2013 Wesley Hearn <whearn@redhat.com> - 0.3.0-1
- Updating to new upstream release

* Thu Jan 24 2013 Wesley Hearn <whearn@redhat.com> - 0.2.0.734-0.1.20130124bzr
- Updated to 734

* Mon Jan 21 2013 Wesley Hearn <whearn@redhat.com> - 0.2.0.731-1.20130121
- Updates to revision 731
- Fixed version numbers and how I generate the source ball
- Cleaned up spec file some more

* Thu Jan 17 2013 Wesley Hearn <whearn@redhat.com> - 0.0-1.20130117bzr723
- Updated to revision 723
- Cleaned up the spec file some

* Wed Jan 16 2013 Wesley Hearn <whearn@redhat.com> - 0.0-1.20130116bzr722
- Initial package

