Name: 		perl-Locale-Maketext-Lexicon
Version: 	1.00
Release: 	3%{?dist}
Summary: 	Extract translatable strings from source
License:	MIT
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/Locale-Maketext-Lexicon/

Source0:        http://search.cpan.org/CPAN/authors/id/D/DR/DRTECH/Locale-Maketext-Lexicon-%{version}.tar.gz

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:	perl(ExtUtils::MakeMaker) > 6.30
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(HTML::Parser) >= 3.56
BuildRequires:  perl(Lingua::EN::Sentence) >= 0.25
BuildRequires:  perl(Locale::Maketext) >= 1.17
BuildRequires:  perl(PPI) >= 1.203
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Template) >= 2.20
BuildRequires:  perl(Template::Constants) >= 2.75
BuildRequires:  perl(Template::Directive)
BuildRequires:  perl(Template::Parser)
BuildRequires:  perl(Text::Haml)
BuildRequires:  perl(YAML) >= 0.66
BuildRequires:  perl(YAML::Loader) >= 0.66
BuildRequires:  perl(base)
BuildRequires:  perl(constant)
BuildRequires:  perl(strict)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)

# Required by the tests
BuildRequires:  /usr/bin/msgunfmt
BuildRequires:  perl(Test::Pod) >= 1.00

BuildArch: noarch

%{?perl_default_filter}

%description
Locale::Maketext::Lexicon provides lexicon-handling backends for
Locale::Maketext to read from other localization formats, such as PO files,
MO files, or from databases via the "Tie" interface.

%prep
%setup -q -n Locale-Maketext-Lexicon-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=${RPM_BUILD_ROOT}
find ${RPM_BUILD_ROOT} -type f -name .packlist -exec rm -f {} ';'
find ${RPM_BUILD_ROOT} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w ${RPM_BUILD_ROOT}/*

%check
make test

%files
%doc AUTHORS Changes README
%doc docs
%{_bindir}/*
%{_mandir}/man1/*
%{perl_vendorlib}/Locale
%{_mandir}/man3/*

%changelog
* Fri Aug 29 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.00-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 07 2014 Ralf Cors??pius <corsepiu@fedoraproject.org> - 1.00-1
- Upstream update.

* Tue Feb 04 2014 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.99-1
- Upstream update.
- Remove redundant explicit R: perl(YAML::Loader).
- Extend BR:'s.

* Mon Jan 27 2014 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.98-2
- Reflect Text::Haml having made it into Fedora.

* Sun Jan 26 2014 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.98-1
- Upstream update.

* Wed Jan 22 2014 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.97-2
- Reflect Lingua::EN::Sentence having made it into Fedora.

* Fri Jan 17 2014 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.97-1
- Upstream update.
- Modernize spec-file.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 Petr Pisar <ppisar@redhat.com> - 0.96-2
- Perl 5.18 rebuild

* Fri Jul 12 2013 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.96-1
- Upstream update.

* Tue May 07 2013 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.94-1
- Upstream update.
- Modernize spec.
- Filter perl(Text::Haml).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Pisar <ppisar@redhat.com> - 0.91-3
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 06 2011 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.91-1
- Upstream update.

* Fri Aug 19 2011 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.86-1
- Upstream update.

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.84-3
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.84-1
- Upstream update.
- Replace custom filters with perl_default_filter.

* Mon Dec 20 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.82-3
- 661697 rebuild for fixing problems with vendorach/lib

* Wed Jun 23 2010 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.82-2
- Rebuild for perl-5.12.1.

* Thu May 06 2010 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.82-1
- Upstream update.

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.79-2
- Mass rebuild with perl-5.12.0

* Wed Mar 03 2010 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.79-1
- Upstream update.

* Tue Mar 02 2010 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.78-1
- Upstream update.

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.77-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 02 2009 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.77-1
- Upstream update.

* Sat Dec 20 2008 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.76-1
- Upstream update.

* Sat Nov 29 2008 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.75-1
- Upstream update.
- Reflect upstream maintainer having changed.
- BR: perl(Template), BR: perl(Test::Pod).

* Fri Oct 10 2008 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.71-1
- Upstream update.
- Spec cleanup.
- Add spec hacks to work around rpm bugs.

* Thu Aug 28 2008 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.68-2
- Filter out bogus requires.

* Tue Aug 26 2008 Ralf Cors??pius <corsepiu@fedoraproject.org> - 0.68-1
- Upstream update.
- Reflect new Source0-URL.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.66-2
- Rebuild for perl 5.10 (again)

* Thu Feb 14 2008 Ralf Cors??pius <rc040203@freenet.de> - 0.66-1
- Upstream update.

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.65-2
- rebuild for new perl

* Fri Dec 28 2007 Ralf Cors??pius <rc040203@freenet.de> - 0.65-1
- Upstream update.

* Tue Sep 04 2007 Ralf Cors??pius <rc040203@freenet.de> - 0.64-2
- Update license tag.
- BR: perl(ExtUtils::MakeMaker).

* Mon Jun 11 2007 Ralf Cors??pius <rc040203@freenet.de> - 0.64-1
- Upgrade to 0.64.
- Reflect source-url having changed.

* Fri Feb 16 2007 Ralf Cors??pius <rc040203@freenet.de> - 0.62-1
- Upgrade to 0.62.
- Reflect licence change from Artistic/GPL to MIT.
- BR: /usr/bin/msgunfmt.

* Tue Sep 05 2006 Ralf Cors??pius <rc040203@freenet.de> - 0.60-2
- Mass rebuild.

* Sat Apr 22 2006 Ralf Cors??pius <rc040203@freenet.de> - 0.60-1
- Upstream update.

* Sun Mar 19 2006 Ralf Cors??pius <rc040203@freenet.de> - 0.54-1
- Upstream update.

* Wed Mar 01 2006 Ralf Cors??pius <rc040203@freenet.de> - 0.53-2
- Rebuild for perl-5.8.8.

* Mon Dec 05 2005 Ralf Corsepius <rc040203@freenet.de> - 0.53-1
- Upstream update.
