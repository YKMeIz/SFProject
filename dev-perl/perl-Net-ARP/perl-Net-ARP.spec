%define real_name Net-ARP

Name:       perl-Net-ARP
Version:    1.0.9
Release:    1%{?dist}
Summary:    Create and Send ARP Packets 
Group:      Development/Libraries
License:    GPLv2
URL:        http://search.cpan.org/dist/%{real_name}
Source0:    http://search.cpan.org/CPAN/authors/id/C/CR/CRAZYDJ/%{real_name}-%{version}.tgz
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires: perl(ExtUtils::MakeMaker)

Patch0:     Net-Arp-1.0.6-tests.patch

%{?perl_default_filter}

%description
This module is a Perl extension to create and send ARP packets and lookup
local or remote mac addresses. You do not need to install any additional 
libraries like Libnet to compile this extension. It uses kernel header files 
to create the packets.

%prep
%setup -q -n %{real_name}
chmod -x README *.pm *.c *.h
%patch0 -p1 -b .tests

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
find %{buildroot} -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
# The tests for this package require root privileges and network access,
# therefore for automated building we need to leave it out.
#
#make test
#

%files
%doc Changes README
%{perl_vendorarch}/Net/
%{_mandir}/man3/Net::ARP.3pm*
%{perl_vendorarch}/auto/Net/

%changelog
* Sun Oct 26 2014 Robin Lee <cheeselee@fedoraproject.org> - 1.0.9-1
- Update to 1.0.9

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.0.8-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug  3 2013 Robin Lee <cheeselee@fedoraproject.org> - 1.0.8-1
- Update to 1.0.8
- License changed from 'GPL+ or Artistic' to 'GPLv2'
- Co-own directories following convention in Perl packages
- Other cleanups

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.0.6-11.1
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-10.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1.0.6-8.1
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.6-6.1
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.0.6-4.1
- 661697 rebuild for fixing problems with vendorach/lib

* Tue May 04 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.0.6-3.1
- Mass rebuild with perl-5.12.0

* Fri Nov 06 2009 BJ Dierkes <wdierkes@rackspace.com> - 1.0.6-2.1
- BuildRequires: perl(ExtUtils::MakeMaker)

* Tue Nov 03 2009 BJ Dierkes <wdierkes@rackspace.com> - 1.0.6-2
- Set _use_internal_dependency_generator to 0 as well as override
  __find_provides in prep to remove unwanted provides.
- Use make pure_install
- Rename spec to match package name

* Thu Oct 29 2009 BJ Dierkes <wdierkes@rackspace.com> - 1.0.6-1
- Initial spec build (modified from perl-Net-SNMP) 
- Added Patch0: Net-Arp-1.0.6-tests.patch

