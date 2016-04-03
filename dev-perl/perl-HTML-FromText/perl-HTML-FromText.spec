Name:           perl-HTML-FromText
Version:        2.07
Release:        2%{?dist}
Summary:        Convert plain text to HTML
License:        GPL+ or Artistic

URL:            http://search.cpan.org/dist/HTML-FromText/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/HTML-FromText-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Email::Find::addrspec) >= 0.09
BuildRequires:  perl(Exporter::Lite) >= 0.01
BuildRequires:  perl(Scalar::Util) >= 1.12
BuildRequires:  perl(HTML::Entities) >= 1.26
BuildRequires:  perl(Text::Tabs) >= 98.1128
BuildRequires:  perl(Test::More) >= 0.47

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
"HTML::FromText" converts plain text to HTML. There are a handful of
options that shape the conversion. There is a utility function,
"text2html", that's exported by default. This function is simply a
short- cut to the Object Oriented interface described in detail below.


%prep
%setup -q -n HTML-FromText-%{version}


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test


%files
%doc Changes README
%{_bindir}/text2html
%{perl_vendorlib}/HTML/
%{_mandir}/man3/*.3*
%{_mandir}/man1/text2html.1.gz


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.07-1
- Update to 2.07

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 2.06-2
- Perl 5.18 rebuild

* Sun Jul 07 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 2.06-1
- Update to 2.06
- Drop no-longer-used macros
- Add perl default filter
- Re-enable all tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 2.05-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.05-10
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.05-7
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 2.05-6
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  2 2008 kwizart < kwizart at gmail.com > - 2.05-2
- Add fixperms

* Thu Jul 31 2008 kwizart < kwizart at gmail.com > - 2.05-1
- Initial package for Fedora

