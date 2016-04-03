Name:       wmfrog
Version:    0.3.1
Release:    12%{?dist}
Summary:    A weather application, it shows the weather in a graphical way
Group:      Amusements/Graphics
License:    GPLv2+
URL:        http://wiki.colar.net/wmfrog_dockapp
Source0:    http://bitbucket.org/tcolar/%{name}/downloads/%{name}-%{version}.tgz
# Bug 822219, submitted to upstream.
Patch0:     %{name}-0.3.1-Skip-warning.patch
BuildRequires:  libX11-devel, libXext-devel, libXpm-devel 
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:   wget

%description
This is a weather application, it shows the weather in a graphical way. The
artwork looks like a kiddo did it, but that's part of the charm… Ok, I did it
when I was 25, I'm a programmer not a designer :)

%prep
%setup -q -c
%patch0 -p1 -b .warning
sed -i -e 's|/lib/wmfrog|/libexec/wmfrog|' Src/Makefile
sed -i -e 's|/usr/lib/|%{_libexecdir}/|' Src/wmFrog.c
# Remove prebuilt binaries
make -C Src clean

%build
cd Src
make CFLAGS="${RPM_OPT_FLAGS}" %{?_smp_mflags}

%install
cd Src
make install DESTDIR=$RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_libexecdir}/%{name}
%doc CHANGES COPYING HINTS 

%changelog
* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.3.1-12
- Perl 5.20 rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.3.1-8
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.3.1-5
- Perl 5.16 rebuild

* Thu May 17 2012 Petr Pisar <ppisar@redhat.com> - 0.3.1-4
- Adjust to NOAA web page change (bug #822219)
- Depend on perl ABI
- Clean spec file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 02 2010 Petr Pisar <ppisar@redhat.com> - 0.3.1-1
- 0.3.1 bump
- Fixed clouds/wind parsing issues

* Wed Sep 01 2010 Petr Pisar <ppisar@redhat.com> - 0.2.2-1
- 0.2.2 bump

* Mon Aug 09 2010 Petr Pisar <ppisar@redhat.com> - 0.2.1-2
- Change RPM group to Amusements/Graphics

* Thu Aug 05 2010 Petr Pisar <ppisar@redhat.com> - 0.2.1-1
- 0.2.1 bump
- Fix METAR parser

* Tue Aug 03 2010 Petr Pisar <ppisar@redhat.com> - 0.2.0-1
- 0.2.0 import
