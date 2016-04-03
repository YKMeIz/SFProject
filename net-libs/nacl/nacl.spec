Name:           nacl
# http://nacl.cr.yp.to/
URL:            http://nacl.cace-project.eu/
Version:        20110221
Release:        8%{?dist}
License:        Public Domain
Group:          Development/Libraries
Summary:        Networking and Cryptography library
BuildRequires:  e2fsprogs
Source0:        http://hyperelliptic.org/nacl/nacl-%{version}.tar.bz2
Source1:        curvecpclient.1
Source2:        curvecpserver.1
Source3:        curvecpmakekey.1
Source4:        curvecpmessage.1
Source5:        curvecpprintkey.1
Source6:        nacl-sha256.1
Source7:        nacl-sha512.1
Patch0:         nacl-20110221-dist-flags.patch
Patch1:         nacl-20110221-build-dir.patch
Patch2:         nacl-20110221-noexec-stack.patch
# Fix for secondary arches
Patch3:         nacl-20110221-cpufreq-fallback.patch

%package devel
Summary:        Development files
Group:          Development/Libraries
Provides:       nacl-static = %{version}-%{release}
Requires:       %{name} = %{version}-%{release}

%description
NaCl (pronounced "salt") is a new easy-to-use high-speed software library for
network communication, encryption, decryption, signatures, etc. NaCl's goal
is to provide all of the core operations needed to build higher-level
cryptographic tools.

%description devel
Include files and devel library.

%prep
%setup -q
%patch0 -p1 -b .dist-flags
%patch1 -p1 -b .build-dir
%patch2 -p1 -b .noexec-stack
%patch3 -p1 -b .cpufreq-fallback

sed -i 's/\${CFLAGS}/%{optflags}/g' okcompilers/c okcompilers/cpp

%build
./do

%install
mkdir -p %{buildroot}%{_includedir}/%{name}
install -m 0644 -t %{buildroot}%{_includedir}/%{name} build/fedora/include/*/*.h
mkdir -p %{buildroot}%{_libdir}/
install -m 0644 -t %{buildroot}%{_libdir} build/fedora/lib/*/*.a

# install cpucycles.o and randombytes.o
install -m 0644 -t %{buildroot}%{_libdir} build/fedora/lib/*/cpucycles.o build/fedora/lib/*/randombytes.o

mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 -t %{buildroot}%{_mandir}/man1 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7}
mkdir -p %{buildroot}%{_bindir}
rm -f build/fedora/bin/ok*
install -m 0755 -t %{buildroot}%{_bindir} build/fedora/bin/*

%files
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%{_libdir}/libnacl.a
%{_libdir}/cpucycles.o
%{_libdir}/randombytes.o
%dir %{_includedir}/nacl
%{_includedir}/nacl/*

%changelog
* Mon Aug 19 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 20110221-8
- The cpucycles.o and randombytes.o moved outside the archive

* Thu Aug  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 20110221-7
- Added cpucycles.o and randombytes.o to libnacl.a archive
  Resolves: rhbz#994236

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110221-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 20110221-5
- Fixed packaging of devel subpackage not to own debuginfo files
  Resolves: rhbz#911405

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110221-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep  6 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 20110221-3
- Fixed build on secondary arches (cpufreq-fallback patch)

* Tue Sep  4 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 20110221-2
- Updated URL

* Mon Jul 02 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 20110221-1
- Initial release
