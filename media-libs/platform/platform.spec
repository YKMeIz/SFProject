Name:           platform
Version:        1.0.10
Release:        4%{?dist}
Summary:        Platform support library used by libCEC and binary add-ons for Kodi

Group:          System Environment/Libraries
License:        GPLv2+
URL:            https://github.com/Pulse-Eight/platform/
Source0:        https://github.com/Pulse-Eight/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
# GPLv2 license file
Source1:        http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
# Fix .cmake files installation path
Patch0:         %{name}-1.0.10-install.patch
# Use system fstrcmp library
Patch1:         %{name}-1.0.10-use_system_fstrcmp.patch

BuildRequires:  cmake
BuildRequires:  pkgconfig(fstrcmp)

%description
%{summary}.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.


%prep
%setup -q
%patch0 -p0 -b .install
%patch1 -p0 -b .use_system_fstrcmp

# Drop bundled fstrcmp library
rm src/util/fstrcmp.*

cp -p %{SOURCE1} .


%build
%cmake .
make %{?_smp_mflags}


%install
%make_install


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc README.md
%license gpl-2.0.txt
%{_libdir}/*.so.*


%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/*.pc


%changelog
* Fri Aug 21 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.10-4
- Add Requires on cmake for devel subpackage

* Sun Aug 16 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.10-3
- Add license text file

* Tue Jul 28 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.10-2
- Unbundle fstrcmp library

* Sun Jul 19 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.0.10-1
- Initiam RPM release
