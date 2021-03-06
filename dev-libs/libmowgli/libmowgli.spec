%define examplesdir __tmp_examples

Name: libmowgli
Version: 1.0.0
Release: 6%{?dist}

Summary: Library of many utility functions and classes
Group: System Environment/Libraries
# https://fedoraproject.org/wiki/Licensing/MIT
License: MIT
URL: http://www.atheme.org/project/mowgli
Source0: http://distfiles.atheme.org/libmowgli-%{version}.tar.bz2

BuildRequires: autoconf libtool

%description
libmowgli is a development framework for C (like GLib), which provides high
performance and highly flexible algorithms. It can be used as a suppliment to
GLib (to add additional functions (dictionaries, hashes), or replace some of
the slow GLib list manipulation functions), or stand alone. It also provides a
powerful hook system and convenient logging for your code, as well as a high
performance block allocator.

%package devel
Summary: Files needed for developing with libmowgli
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the files that are needed when building
software that uses libmowgli.


%prep
%setup -q
# for aarch64 support - https://bugzilla.redhat.com/925798
autoreconf -f

# Make the build system more verbose
sed -i '\,^.SILENT:,d' buildsys.mk.in

# Prepare the examples for %%doc inclusion.
rm -rf %{examplesdir} ; mkdir %{examplesdir}
cp -a src/examples %{examplesdir}
find %{examplesdir} -name Makefile | xargs rm -f


%build
%configure \
    --enable-examples \
    --disable-dependency-tracking

make %{?_smp_mflags}


%install
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"


%check
# Execute examples for some testing. Not really a test-suite.
for f in $(find src/examples -type f -executable) ; do
    LD_LIBRARY_PATH=${RPM_BUILD_ROOT}%{_libdir}  $f || true
done
exit 0


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING README
%{_libdir}/*.so.*

%files devel
%doc %{examplesdir}/*
%{_libdir}/*.so
%{_includedir}/libmowgli/
%{_libdir}/pkgconfig/libmowgli.pc


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 21 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0.0-5
- BR autoconf libtool and run autoreconf -f for aarch64 updates (#925798)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0.0-2
- rebuild for GCC 4.7 as requested

* Sat Dec  3 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0.0-1
- Insert official tarball (empty diff).

* Tue Nov 22 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.0.0-0.1.20111122git
- Update to 1.0.0 git checkout (6k diff)
  also to not flag mowgli_spinlock as deprecated.

* Tue Sep 27 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 0.9.95-1
- Update to 0.9.95 (32k diff, API additions and a few internal changes).

* Fri Sep 16 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 0.9.50-2
- Use %%_isa in -devel package dependency.
- Drop unneeded BuildRoot stuff.
- Drop %%defattr lines.

* Mon Jan 31 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 0.9.50-1
- Upgrade to 0.9.50.
- mowgli_dictionary is deprecated and pending removal in Mowgli 1.0 series.
  Please use mowgli_patricia instead.

* Wed Jan  5 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.1-2
- Apply mowgli_list off-by-one patch for mowgli_node_nth.

* Fri Aug 13 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1.

* Wed Jun  9 2010 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.0-4
- Add mowgli_patricia corruption fix for keys starting with \1
  plus a few minor changes up to 2010-06-04. Special-case '\1' not
  handled yet.

* Wed Nov 18 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.0-3
- Compile examples and execute them for some testing.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun  4 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.7.0-1
- Upgrade to 0.7.0 (SONAME version change).
- License is unchanged, but more similar to MIT than ISC.
- Minor .spec updates.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5.0-2
- Autorebuild for GCC 4.3

* Sat Nov 10 2007 Ralf Ertzinger <ralf@skytale.net> 0.5.0-1
- Initial build for FE
