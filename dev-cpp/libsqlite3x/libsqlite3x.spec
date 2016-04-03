%global veryear 2007
%global vermon  10
%global verday  18
%global namesq3 libsq3
Name:           libsqlite3x
Version:        %{veryear}%{vermon}%{verday}
Release:        14%{?dist}
Summary:        A C++ Wrapper for the SQLite3 embeddable SQL database engine

Group:          System Environment/Libraries
# fix license tag: https://bugzilla.redhat.com/show_bug.cgi?id=491618
License:        zlib
URL:            http://www.wanderinghorse.net/computing/sqlite/
Source0:        http://www.wanderinghorse.net/computing/sqlite/%{name}-%{veryear}.%{vermon}.%{verday}.tar.gz
Source1:        libsqlite3x-autotools.tar.gz
Patch1:         libsqlite3x-prep.patch
Patch2:         libsqlite3x-includes.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  sqlite-devel dos2unix automake libtool doxygen

%description
sqlite3 is a slick embedded SQL server written in C. It's easy to use,
powerful, and quite fast. sqlite3x is a C++ wrapper API for working
with sqlite3 databases that uses exceptions.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       sqlite-devel pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n     %{namesq3}
Summary:        A C++ Wrapper for the SQLite3 embeddable SQL database engine
Group:          Development/Libraries
Requires:       %{namesq3} = %{version}-%{release}

%description -n %{namesq3}
sqlite3 is a slick embedded SQL server written in C. It's easy to use,
powerful, and quite fast. sq3 is a C++ wrapper API for working
with sqlite3 databases that does not use exceptions.

%package -n     %{namesq3}-devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{namesq3} = %{version}-%{release}
Requires:       sqlite-devel pkgconfig

%description -n %{namesq3}-devel
The %{namesq3}-devel package contains libraries and header files for
developing applications that use %{namesq3}.

%prep
%setup -q -n %{name}-%{veryear}.%{vermon}.%{verday} -a 1
dos2unix *.hpp *.cpp
%patch1 -p0 -b .prep
%patch2 -p0 -b .incl
aclocal
libtoolize -f
autoheader
autoconf
automake -a -c
%configure --disable-static
iconv -f iso8859-1 -t utf-8  < README > R
mv R README
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%build
make
make doc
make doc-sq3

%install
%{__rm} -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n %{namesq3} -p /sbin/ldconfig

%postun -n %{namesq3} -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS Doxygen-index.txt
%{_libdir}/libsqlite3x.so.*

%files devel
%defattr(-,root,root,-)
%doc README doc/html
%{_includedir}/sqlite3x
%{_libdir}/libsqlite3x.so
%{_libdir}/pkgconfig/libsqlite3x.pc

%files -n %{namesq3}
%defattr(-,root,root,-)
%doc AUTHORS Doxygen-index.txt
%{_libdir}/libsq3.so.*

%files -n %{namesq3}-devel
%defattr(-,root,root,-)
%doc README doc-sq3/html
%{_includedir}/sq3
%{_libdir}/libsq3.so
%{_libdir}/pkgconfig/libsq3.pc

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071018-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071018-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071018-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071018-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071018-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul  8 2010 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20071018-9
- conform to licensing guide update

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071018-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 29 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20071018-7
- fix license tag

* Thu Apr 16 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20071018-6
- replace %%define with %%global

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20071018-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  4 2008 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20071018-4
- separate sq3 and sqlite3x into separate binary packages
- add unused-direct-shlib-dependency build quirk
- add missing dependency

* Fri May 16 2008 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20071018-3
- add cstring includes for strlen prototypes

* Sat Mar 22 2008 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20071018-2
- add autotools based build system

* Sat Mar 22 2008 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20071018-1
- update

* Thu Aug  2 2007 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20070214-1
- update

* Thu Jan  4 2007 Thomas Sailer <t.sailer@alumni.ethz.ch> - 20060929-1
- Initial build
