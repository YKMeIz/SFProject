%define         solib tolua++-5.1

Name:           tolua++
Version:        1.0.93
Release:        6%{?dist}
Summary:        A tool to integrate C/C++ code with Lua
Group:          Development/Tools
License:        MIT
URL:            http://www.codenix.com/~tolua/
Source0:        http://www.codenix.com/~tolua/%{name}-%{version}.tar.bz2
Patch0:         tolua++-1.0.93-lua51.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  scons
BuildRequires:  lua-devel >= 5.1
ExcludeArch:    ppc

%description
tolua++ is an extended version of tolua, a tool to integrate C/C++ code with
Lua. tolua++ includes new features oriented to C++


%package devel
Summary:        Development files for tolua++
Group:          Development/Libraries
Requires:       tolua++ = %{version}-%{release}
Requires:       lua-devel >= 5.1

%description devel
Development files for tolua++


%prep
%setup -q
%patch0 -p1 -b .lua51
sed -i 's/\r//' doc/%{name}.html


%build
scons %{?_smp_mflags} -Q CCFLAGS="%{optflags}  -I%{_includedir}" tolua_lib=%{solib} LINKFLAGS="-Wl,-soname,lib%{solib}.so" shared=1
#Recompile the exe without the soname. An ugly hack.
gcc -o bin/%{name} src/bin/tolua.o src/bin/toluabind.o -Llib -l%{solib} -llua -ldl -lm


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir %{buildroot}%{_libdir}
mkdir %{buildroot}%{_includedir}
install -m0755 bin/%{name}  %{buildroot}%{_bindir}
install -m0755 lib/lib%{solib}.so %{buildroot}%{_libdir}
install -m0644 include/%{name}.h %{buildroot}%{_includedir}
cd %{buildroot}%{_libdir}
ln -s lib%{solib}.so libtolua++.so


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_libdir}/lib%{solib}.so
%doc README doc/*


%files devel
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/libtolua++.so
%{_includedir}/%{name}.h


%changelog
* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.93-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.93-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.93-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Tim Niemueller <tim@niemueller.de> - 1.0.93-3
- Exclude ppc, there are problems according to bz #704372

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 25 2010 Tim Niemueller <tim@niemueller.de> - 1.0.93-1
- Upgrade to 1.0.93

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.92-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.92-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 13 2008 Tim Niemueller <tim@niemueller.de> - 1.0.92-7
- Added patch to make tolua++ compatible with GCC 4.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.92-6
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Ian Chapman <packages@amiga-hardware.com> 1.0.92-5
- Release bump for F8 mass rebuild
- Updated license due to new guidelines

* Mon Aug 28 2006 Ian Chapman <packages@amiga-hardware.com> 1.0.92-4
- Release bump for FC6 mass rebuild

* Sat Jun 03 2006 Ian Chapman <packages@amiga-hardware.com> 1.0.92-3
- Fixed issue with where tolua++ was tagged with an soname the same as the lib
  meaning ld would fail to locate the library.

* Fri Jun 02 2006 Ian Chapman <packages@amiga-hardware.com> 1.0.92-2
- Changed license from Freeware Style to just Freeware
- Changed => to more conventional >= for (build)requires
- Moved %%{_bindir}/tolua++ to devel package
- Now adds soname to library

* Fri Jun 02 2006 Ian Chapman <packages@amiga-hardware.com> 1.0.92-1
- Initial Release
