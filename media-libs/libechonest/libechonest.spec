Name:		libechonest
Version: 	2.1.0
Release:	1%{?dist}
Summary:	C++ wrapper for the Echo Nest API

License:	GPLv2+
URL:		https://projects.kde.org/projects/playground/libs/libechonest
Source0:	http://files.lfranchi.com/libechonest-%{version}.tar.bz2

BuildRequires:	cmake
BuildRequires:	pkgconfig(QJson)
BuildRequires:	pkgconfig(QtNetwork)


%description
libechonest is a collection of C++/Qt classes designed to make a developer's
life easy when trying to use the APIs provided by The Echo Nest.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion libechonest)" = "%{version}"
# The tests need active internet connection, which is not available in koji builds
# besides, there's several known-failures yet anyway -- rex
#make test -C %%{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README TODO
%{_libdir}/libechonest.so.2.1*

%files devel
%{_includedir}/echonest/
%{_libdir}/libechonest.so
%{_libdir}/pkgconfig/libechonest.pc


%changelog
* Wed May 22 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.0-1
- 2.1.0

* Sun Mar 24 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.3-1
- 2.0.3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-1
- 2.0.2

* Tue Nov 27 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-3
- rebuild (qjson)

* Fri Nov 23 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-2
- rebuild (qjson)

* Thu Jul 26 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.1-1
- Update to 2.0.1

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Rex Dieter <rdieter@fedoraproject.org> 1.2.1-1
- Update to 1.2.1
- BR: pkgconfig(QtNetwork)

* Sat Oct 08 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.2.0-1
- Update to 1.2.0

* Fri Aug 19 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.9-1
- Update to 1.1.9

* Wed Jun 01 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.8-1
- 1.1.8
- track soname
- %%check: verify pkgconfig sanity

* Tue May 10 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.5-1
- Update to 1.1.5

* Sun Mar 27 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.4-1
- Update to 1.1.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 30 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.1-1
- Update to 1.1.1

* Mon Dec 20 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.1.0-1
- Initial Fedora package
