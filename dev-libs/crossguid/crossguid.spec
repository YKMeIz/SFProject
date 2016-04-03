%global commit 8f399e8bd4252be9952f3dfa8199924cc8487ca4
%global short_commit %(c=%{commit}; echo ${c:0:7})
%global commit_date 20150803

Name:           crossguid
Version:        0
Release:        0.2.%{commit_date}git%{short_commit}%{?dist}
Summary:        Lightweight cross platform C++ GUID/UUID library

Group:          System Environment/Libraries
License:        MIT
URL:            https://github.com/graeme-hill/crossguid/
Source0:        https://github.com/graeme-hill/%{name}/archive/%{short_commit}/%{name}-%{short_commit}.tar.gz
# Custom Makefile to properly handle build and installation
Source1:        Makefile.%{name}

BuildRequires:  gcc-c++
BuildRequires:  libuuid-devel

%description
CrossGuid is a minimal, cross platform, C++ GUID library. It uses the best
native GUID/UUID generator on the given platform and has a generic class for
parsing, stringifying, and comparing IDs.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.


%prep
%setup -q -n %{name}-%{commit}

cp -p %{SOURCE1} Makefile


%build
make %{?_smp_mflags} CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"


%install
%make_install LIBDIR=%{_libdir} INCLUDEDIR=%{_includedir}


%check
make test CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"
./test


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc README.md
%license LICENSE
%{_libdir}/*.so.*


%files devel
%{_includedir}/*
%{_libdir}/*.so


%changelog
* Tue Nov 10 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0-0.2.20150803git8f399e8
- Fix typo in description

* Thu Sep 24 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0-0.1.20150803git8f399e8
- Initial RPM release
