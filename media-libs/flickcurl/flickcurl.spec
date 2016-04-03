Name:           flickcurl
Version:        1.25
Release:        2%{?dist}
Summary:        C library for the Flickr API
License:        LGPLv2+ or GPLv2+ or ASL 2.0
URL:            http://librdf.org/flickcurl
Source0:        http://download.dajobe.org/%{name}/%{name}-%{version}.tar.gz
BuildRequires:  chrpath
BuildRequires:  libcurl-devel
BuildRequires:  libxml2-devel
BuildRequires:  raptor2-devel
BuildRequires:  pkgconfig

%description
Flickcurl is a C library for the Flickr API, handling creating the requests, 
signing, token management, calling the API, marshalling request parameters 
and decoding responses. It uses libcurl to call the REST web service and 
libxml2 to manipulate the XML responses. Flickcurl supports all of the API 
including the functions for photo/video uploading, browsing, searching, 
adding and editing comments, groups, notes, photosets, categories, activity, 
blogs, favorites, places, tags, machine tags, institutions, pandas and 
photo/video metadata. It also includes a program flickrdf to turn photo 
metadata, tags, machine tags and places into an RDF triples description.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libcurl-devel
Requires:       libxml2-devel
Requires:       raptor2-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

#removing rpaths with chrpath
chrpath --delete %{buildroot}%{_bindir}/flickcurl
chrpath --delete %{buildroot}%{_bindir}/flickrdf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING README NOTICE
%doc LICENSE-2.0.txt LICENSE.html COPYING.LIB
%doc coverage.html ChangeLog README.html NEWS.html
%{_bindir}/flickcurl
%{_bindir}/flickrdf
%{_libdir}/*.so.*
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/flickrdf.1*

%files devel
%doc COPYING COPYING.LIB
%{_bindir}/flickcurl-config
%{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man1/%{name}-config.1*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 30 2013 Christopher Meng <rpm@cicku.me> - 1.25-1
- Update to 1.25

* Sun Aug 25 2013 Christopher Meng <rpm@cicku.me> - 1.24-1
- Update to new version.
- SPEC cleanup and update the description.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.22-1
- Update to 1.22, build against raptor2 (bz#838709).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 05 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 1.18-1
- Updated to 1.18

* Sat Jan 30 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 1.16-1
- Updated to 1.16

* Thu Dec 03 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1.14-1
- Updated to 1.14

* Thu Aug 06 2009 Rakesh Pandit <rakesh@fedoraproject.org> - 1.13-1
- Updated to 1.13

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 24 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.10-3
- Added pkgconfig as devel sub package BR
- Fixed %%files folder *gtk-doc/html ownership

* Wed May 06 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.10-2
- Added raptor-devel require.

* Wed May 06 2009 Rakesh Pandit <rakesh@fedoraproject.org> 1.10-1
- Initial package
