Summary:      Library for manipulating RDF files describing LADSPA plugins
Name:         liblrdf
Version:      0.5.0
Release:      8%{?dist}
License:      GPLv2+
Group:        System Environment/Libraries
URL:          https://github.com/swh/LRDF
# No direct download for the tarball. Download autogenerated
# tarball from https://github.com/swh/LRDF/tarball/0.5.0
Source0:      liblrdf-%{version}.tar.gz
Source1:      liblrdf-README.fedora
BuildRequires: pkgconfig
BuildRequires: ladspa-devel
BuildRequires: openssl-devel
BuildRequires: raptor2-devel
Requires:     ladspa

%description
liblrdf is a library to make it easy to manipulate RDF files describing
LADSPA plugins.

%package devel
Summary:      Library for manipulating RDF files describing LADSPA plugins
Group:        Development/Libraries
Requires:     liblrdf%{?_isa} = %{version}-%{release}
Requires:     raptor2-devel

%description devel
This is a library to make it easy to manipulate RDF files describing
LADSPA plugins. This package includes the development tools.

%prep
%setup -q
cp -a %{SOURCE1} README.fedora

%build
%configure --disable-static

%install
%{make_install}
rm -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING NEWS README
%{_libdir}/liblrdf.so.*
%{_datadir}/ladspa/rdf/ladspa.rdfs

%files devel
%doc ChangeLog README.fedora
%{_includedir}/*
%{_libdir}/liblrdf.so
%{_libdir}/pkgconfig/*

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.5.0-3
- devel package requires raptor2-devel instead of raptor-devel
- Some specfile cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Anthony Green <green@redhat.com> 0.5.0-1
- Upgrade.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4.0-14
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.0-13
- Autorebuild for GCC 4.3

* Tue Oct 08 2007 Anthony Green <green@redhat.com> 0.4.0-12
- Don't %%exclude %%{_datadir}/ladspa/rdf/ladspa.rdfs
- Require ladspa to get directory ownerships right.

* Fri Jul 20 2007 Callum Lerwick <seg@haxxed.com> 0.4.0-11
- Bump to build on ppc64, bug #247583.

* Thu Oct 05 2006 Anthony Green <green@redhat.com> 0.4.0-10
- Delete .la file after installing it instead of using %%exclude.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.4.0-9
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Anthony Green <green@redhat.com> 0.4.0-8
- Fix release tag.

* Mon Sep 18 2006 Anthony Green <green@redhat.com> 0.4.0-7.1
- Rebuild.

* Thu May 18 2006 Anthony Green <green@redhat.com> 0.4.0-7
- Don't install generic INSTALL documentation.

* Sat May 13 2006 Anthony Green <green@redhat.com> 0.4.0-6
- Exclude ladspa.rdfs.
- Don't use %%{__rm} or %%{__make} macros.
- Standardize on $RPM_BUILD_ROOT from %%{buildroot}.

* Mon Apr 24 2006 Anthony Green <green@redhat.com> 0.4.0-5
- Clean up BuildRequires based on raptor mods.

* Sun Apr 23 2006 Anthony Green <green@redhat.com> 0.4.0-4
- Remove examples dir.  Add README.fedora.
- Configure with --disable-static.

* Sun Apr 23 2006 Anthony Green <green@redhat.com> 0.4.0-3
- Update URLs.
- Remove gcc-c++ from BuildRequires.
 
* Tue Apr 18 2006 Anthony Green <green@redhat.com> 0.4.0-2
- Minor tweaks.  Build for Fedora Extras.
 
* Wed Dec 22 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.4.0-1
- updated to 0.4.0
* Fri Dec 16 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 
- spec file tweaks
* Thu Apr 15 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.3.7-1
- updated to 0.3.7, added proper build requirements
* Wed Feb 18 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.3.5-1
- updated to 0.3.5
* Wed Feb  4 2004 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.3.4-1
- updated to 0.3.4
* Fri Nov  7 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.3.2-1
- updated to 0.3.2
* Tue May  6 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.3.1-1
- updated to 0.3.1
* Thu Mar  6 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.4-1
- added ldconfig, pkgconfig file to devel file list
* Wed Feb 19 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.3-2
- added raptor-devel dependency to liblrdf-devel
* Fri Feb 14 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.3-1
- updated to 0.2.3
* Wed Feb 11 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.2-1
- updated to 0.2.2
* Mon Jan 13 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.2.1-1
- updated to 0.2.1
* Thu Jan  9 2003 Fernando Lopez-Lezcano <nando@ccrma.stanford.edu> 0.1.3-1
- Initial build, fix missing symbolic links to the shared library