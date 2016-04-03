Name:           perl-Gtk2-Ex-PodViewer
Version:        0.18
Release:        16%{?dist}
Summary:        A Gtk2 widget for displaying Plain old Documentation (POD)

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Gtk2-Ex-PodViewer/
Source0:        http://search.cpan.org/CPAN/authors/id/G/GB/GBROWN/Gtk2-Ex-PodViewer-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(Gtk2)
BuildRequires:  perl(Gtk2::Ex::Simple::List)
BuildRequires:  perl(Gtk2::Gdk::Keysyms)
BuildRequires:  perl(Gtk2::Pango)
BuildRequires:  perl(IO::Scalar)
BuildRequires:  perl(lib)
BuildRequires:  perl(Locale::gettext)
BuildRequires:  perl(Pod::Parser)
BuildRequires:  perl(Pod::Simple::Search)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
A Gtk2 widget for displaying Plain old Documentation (POD) files.


%prep
%setup -q -n Gtk2-Ex-PodViewer-%{version}

# remove -x bits from files that don't need them
find . -type f -print | xargs chmod a-x

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%files
%doc README
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
* Mon Jun 09 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.18-16
- Add missing BR:s (Address FTBFS, RHBZ #1106052).
- Modernize spec.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.18-13
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.18-10
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.18-8
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-6
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.18-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.18-4
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 06 2008 Bernard Johnson <bjohnson@symetrix.com> - 0.18-1
- v 0.18

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17-4
Rebuild for new perl

* Thu May 03 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.17-3
- BR on perl(ExtUtils::MakeMaker) rather than perl

* Sun Mar 25 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.17-2
- use perl(...) style requires (bz #233767)

* Mon Mar 19 2007 Bernard Johnson <bjohnson@symetrix.com> - 0.17-1
- initial release
