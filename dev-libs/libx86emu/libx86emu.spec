Name:          libx86emu
Version:       1.1
Release:       2.1
Summary:       A small x86 emulation library
Group:         System/Libraries
URL:           http://download.opensuse.org/source/distribution/11.2/repo/oss/suse/src/
# autospec -x libx86emu-%{version}-%{oss_release}.src.rpm -F libx86emu-%{version}.tar.bz2
Source:        libx86emu-%{version}.tar.bz2
License:       BSD
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
Small x86 emulation library with focus of easy usage and extended execution
logging functions.

%package devel
Group:         Development/Libraries
Summary:       Static libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
Small x86 emulation library with focus of easy usage and extended execution
logging functions.

This package contains static libraries and header files need for development.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%doc LICENSE README

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so

%changelog
* Wed Jun 29 2011 Huaren Zhong <huaren.zhong@gmail.com> - 1.1
- Rebuild for Fedora

* Wed Feb 17 2010 Stefano Cotta Ramusino <stefano.cotta@openmamba.org> 1.1-1mamba
- package created by autospec
