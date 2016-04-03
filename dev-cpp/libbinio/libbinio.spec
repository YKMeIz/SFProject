# SPEC file for libbinio, primary target is the Fedora Extras
# RPM repository.

Name:		libbinio
Version:	1.4
Release:	17%{?dist}
Summary:	A software library for binary I/O classes in C++
URL:		http://libbinio.sourceforge.net/
Group:		System Environment/Libraries
Source:		http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:		libbinio-1.4-texinfo.patch
Patch1:		libbinio-1.4-pkgconfigurl.patch
Patch2:		libbinio-1.4-includes.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:	LGPLv2+
BuildRequires:	/sbin/install-info

%description
This binary I/O stream class library presents a platform-independent
way to access binary data streams in C++. The library is hardware 
independent in the form that it transparently converts between the 
different forms of machine-internal binary data representation.
It further employs no special I/O protocol and can be used on
arbitrary binary data sources.

%package devel
Summary:        Development files for libbinio
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires:	texinfo
Requires(post):	/sbin/install-info
Requires(preun): /sbin/install-info

%description devel
This package contains development files for the libbinio binary
data stream class for C++.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall
# Remove libtool archive remnants
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Remove doc "dir"
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/libbinio.info.gz %{_infodir}/dir || :

%preun devel
if [ $1 = 0 ]; then
# uninstall the info reference in the dir file
/sbin/install-info --delete %{_infodir}/libbinio.info.gz %{_infodir}/dir || :
fi

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%doc AUTHORS README COPYING INSTALL INSTALL.unix NEWS TODO

%files devel
%defattr(-, root, root)
%dir %{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}/*.h
%{_infodir}/*.gz

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 02 2009 Caolán McNamara <caolanm@redhat.com> - 1.4-11
- include stdio.h for EOF

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 9 2008 Linus Walleij <triad@df.lth.se> 1.4-9
- Rebuild for GCC 4.3.

* Fri Jan 18 2008 Linus Walleij <triad@df.lth.se> 1.4-8
- New glibc ABI wants a rebuild.

* Fri Aug 17 2007 Linus Walleij <triad@df.lth.se> 1.4-7
- License field update from LGPL to LGPLv2+

* Mon Aug 28 2006 Linus Walleij <triad@df.lth.se> 1.4-6
- Rebuild for Fedora Extras 6.

* Tue Feb 14 2006 Linus Walleij <triad@df.lth.se> 1.4-5
- Rebuild for Fedora Extras 5.

* Thu Oct 6 2005 Linus Walleij <triad@df.lth.se> 1.4-4
- BuildRequire texinfo to get makeinfo.

* Sat Oct 1 2005 Linus Walleij <triad@df.lth.se> 1.4-3
- Conforming pkg-config for FC4 and texinfo bug patch.

* Sun Sep 18 2005 Linus Walleij <triad@df.lth.se> 1.4-2
- More minor corrections.

* Sun Sep 18 2005 Linus Walleij <triad@df.lth.se> 1.4-1
- Upstream fixed header problem.

* Fri Sep 16 2005 Linus Walleij <triad@df.lth.se> 1.3-4
- Trying to resolve dispute about header subdirs.

* Thu Sep 15 2005 Linus Walleij <triad@df.lth.se> 1.3-3
- Reverted some and added some after comments from Ville Skyttä.

* Thu Sep 15 2005 Linus Walleij <triad@df.lth.se> 1.3-2
- Fixed some points raised by Ralf Corsepius.

* Wed Sep 14 2005 Linus Walleij <triad@df.lth.se> 1.3-1
- First try at a libbinio RPM.
