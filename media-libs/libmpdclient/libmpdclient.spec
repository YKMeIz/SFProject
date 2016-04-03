Summary: Library for interfacing Music Player Daemon
Name: libmpdclient
Version: 2.7
Release: 4%{?dist}
License: BSD
Url: http://mpd.wikia.com/wiki/ClientLib:libmpdclient
Group: System Environment/Libraries
Source: http://downloads.sourceforge.net/musicpd/%{name}-%{version}.tar.bz2
BuildRequires: doxygen

%package devel
Summary: Header files for developing programs with %{name}
Requires: %{name} = %{version}-%{release}
Group: Development/Libraries

%description
A stable, documented, asynchronous API library for interfacing MPD
in the C, C++ & Objective C languages. 

%description devel
%{name}-devel is a sub-package which contains header files and
libraries for developing programs with %{name}.

%prep
%setup -q

%build
%configure --disable-static
%{__make} %{?_smp_mflags}

%install
%{__sed} -i -e "s,doc/api/html/\*.gif,,g" Makefile
%{__make} DESTDIR="$RPM_BUILD_ROOT" install
%{__rm} -f $RPM_BUILD_ROOT%{_libdir}/%{name}.la
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name} _doc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/libmpdclient.so.2*

%files devel
%doc _doc/html
%{_libdir}/libmpdclient.so
%{_libdir}/pkgconfig/libmpdclient.pc
%{_includedir}/mpd/

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Jamie Nguyen <jamie@tomoyolinux.co.uk> - 2.7-1
- update to upstream version 2.7
- remove obsolete BuildRoot tag, %%clean section and %%defattr

* Wed Mar 02 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 2.4-1
- version upgrade

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Adrian Reber <adrian@lisas.de> - 2.2-1
- fixes "FTBFS libmpdclient-2.1-3.fc13" (#631331)
- updated to 2.2

* Wed Jan 27 2010 Adrian Reber <adrian@lisas.de> - 2.1-3
- make devel subpackage require %%{name} = %%{version}-%%{release}

* Fri Jan 08 2010 Michal Nowak <mnowak@redhat.com> - 2.1-2
- spec file fixes

* Thu Jan 07 2010 Adrian Reber <adrian@lisas.de> - 2.1-1
- updated to 2.1

* Thu Dec 03 2009 Adrian Reber <adrian@lisas.de> - 2.0-1
- initial spec file (based on libmpd)
