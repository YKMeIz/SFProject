Name:           megatools
Version:        1.9.91
Release:        2%{?dist}
Summary:        Command line client for Mega.co.nz

License:        GPLv2+
URL:            http://megatools.megous.com/
Source0:        http://megatools.megous.com/builds/%{name}-%{version}.tar.gz

BuildRequires:  fuse-devel
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  glib2-devel


%description
Megatools is a collection of programs for accessing Mega service from a command
line of your desktop or server.

Megatools allow you to copy individual files as well as entire directory trees
to and from the cloud. You can also perform streaming downloads for example to
preview videos and audio files, without needing to download the entire file.

You can register account using a 'megareg' tool, with the benefit of having
true control of your encryption keys.

Megatools are robust and optimized for fast operation - as fast as Mega servers
allow. Memory requirements and CPU utilization are kept at minimum.

%package        devel
Summary:        Include files and mandatory libraries for development megatools
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Include files and mandatory libraries for development.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
%make_install
find %{buildroot} -name "*" -exec chrpath --delete {} \; 2>/dev/null
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'
rm %{buildroot}%{_docdir}/%{name}/INSTALL

%post -n %{name} -p /sbin/ldconfig

%postun -n %{name} -p /sbin/ldconfig

%files
%doc
%{_bindir}/*
%{_libdir}/libmega.so.*
%{_docdir}/%{name}
%{_datadir}/gjs-1.0/mega.js
%{_mandir}/man1/*
%{_mandir}/man5/megarc.5.gz
%{_mandir}/man7/%{name}.7.gz

%files devel
%{_includedir}/mega
%{_libdir}/libmega.so
%{_libdir}/pkgconfig/libmega.pc


%changelog
* Mon Jul 08 2013 Vasiliy N. Glazov <vascom2@gmail.com> 1.9.91-2.R
- Remove BR gobject-introspection-devel

* Tue Jun 04 2013 Vasiliy N. Glazov <vascom2@gmail.com> 1.9.91-1.R
- Initial release
