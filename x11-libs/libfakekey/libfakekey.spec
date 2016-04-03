Name:           libfakekey
Version:        0.1
Release:        10%{?dist}
Summary:        Library for converting characters to X key-presses

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://projects.o-hand.com/matchbox/
Source0:        http://matchbox-project.org/sources/libfakekey/0.1/%{name}-%{version}.tar.bz2
BuildRequires:  libXtst-devel
BuildRequires:  libXi-devel

%description
libfakekey is a simple library for converting UTF-8 characters into
'fake' X key-presses.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       libXtst-devel
Requires:       libXi-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags} AM_LDFLAGS=-lX11


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libfakekey.la


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libfakekey.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/fakekey/
%{_libdir}/libfakekey.so
%{_libdir}/pkgconfig/libfakekey.pc

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.1-9
- Add libXi to fix FTBFS

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 14 2011 Peter Robinson <pbrobinson@gmail.com> - 0.1-6
- Add devel dep on libXtst-devel - BZ 680878

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Sep  2 2010 Dan Horák <dan[at]danny.cz> - 0.1-4
- fix linking with --no-add-needed (#564882)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon May 19 2008 Jon McCann <jmccann@redhat.com> 0.1-1
- Initial package
