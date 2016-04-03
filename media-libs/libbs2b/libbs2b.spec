Name:		libbs2b
Version:	3.1.0
Release:	8%{?dist}
Summary:	Bauer stereophonic-to-binaural DSP library

Group:		Applications/Multimedia
License:	Copyright only
URL:		http://bs2b.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/bs2b/bs2b/%{version}/%{name}-%{version}.tar.lzma
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	autoconf automake libtool
BuildRequires:	libsndfile-devel
# the dependency (required for bs2bconvert) gets added automatically
#Requires:	libsndfile


%package devel
Summary:	Development files for libbs2b
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description
The Bauer stereophonic-to-binaural DSP (bs2b) library and plugins is designed
to improve headphone listening of stereo audio records. Recommended for
headphone prolonged listening to disable superstereo fatigue without essential
distortions.


%description devel
This package contains the development files for the Bauer
stereophonic-to-binaural (bs2b) DSP effect library.


%prep
%setup -q
# automake 1.12 removes support for lzma, it has been replaced by xz
# it is safe to substitute xz for lzma to get rid of autoreconf errors,
# we don't build the dist archive anyways
sed -i -e 's/lzma/xz/g' configure.ac
# new libool needs new ltmain script
rm build-aux/ltmain.sh
ln -s /usr/share/libtool/config/ltmain.sh build-aux/ltmain.sh
# reconf to support aarch64 (bug #925677)
autoreconf


%build
%configure --disable-static
# disable rpath as suggested in
# https://fedoraproject.org/wiki/Packaging:Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm %{buildroot}/%{_libdir}/%{name}.la


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README
%{_bindir}/*
%{_libdir}/%{name}.so.*


%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%changelog
* Mon Aug 26 2013  Karel Volný <kvolny@redhat.com> 3.1.0-8
- run autoreconf to support aarch64 (bug #925677)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 31 2009 Karel Volný <kvolny@redhat.com> 3.1.0-2
- specfile cleanup as per review (bug #519138 comment #1)

* Tue Aug 25 2009 Karel Volný <kvolny@redhat.com> 3.1.0-1
- initial Fedora package version
