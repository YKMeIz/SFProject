Name:           perl-Gnome2-VFS
Version:        1.082
Release:        1%{?dist}
Summary:        Perl interface to the 2.x series of the GNOME VFS library
License:        LGPLv2+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Gnome2-VFS/
Source0:        http://www.cpan.org/authors/id/X/XA/XAOC/Gnome2-VFS-%{version}.tar.gz
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


BuildRequires:  perl
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::Depends) >= 0.20
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::PkgConfig) >= 1.03
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Glib) >= 1.120
BuildRequires:  perl(Glib::CodeGen)
BuildRequires:  perl(Glib::MakeHelper)
BuildRequires:  perl(strict)
# Run-time
BuildRequires:  perl(constant)
BuildRequires:  perl(DynaLoader)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(warnings)
# Tests
BuildRequires:  perl(Config)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
BuildRequires:  gnome-vfs2-devel


%description
This module allows you to interface with the GNOME Virtual File System
library. It provides the means to transparently access files on all kinds of
filesystems.


%prep
%setup -q -n Gnome2-VFS-%{version} 


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}


%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} %{buildroot}/*


%check
make test


%files
%doc doctypes LICENSE NEWS README examples/ t/
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Gnome2*
%{_mandir}/man3/*

%changelog
* Wed Oct 02 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.0182-1
- 0.0182 bump
- Update dependencies
- Modernize spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.081-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.081-14
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.081-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.081-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Petr Pisar <ppisar@redhat.com> - 1.081-11
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.081-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.081-9
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.081-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.081-7
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.081-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.081-5
- rebuild against perl 5.10.1

* Thu Jul 30 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.081-4
- Fix mass rebuild breakdown: Add BR: perl(Glib::MakeHelper).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.081-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.081-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 1.081-1
- update to 1.081

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.080-3
Rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.080-2
- Autorebuild for GCC 4.3

* Tue Oct 23 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.080-1
- update to 1.080

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.061-3
- bump

* Sat Dec 02 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.061-2
- bump

* Wed Nov 29 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.061-1
- updated to 1.061

* Sun Aug 13 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.060-1
- Specfile autogenerated by cpanspec 1.68.
- Initial spec file for F-E
