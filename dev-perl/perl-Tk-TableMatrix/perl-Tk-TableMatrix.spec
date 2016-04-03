Name:           perl-Tk-TableMatrix
Version:        1.23
Release:        20%{?dist}
Summary:        Perl module for creating and manipulating tables

License:        (GPL+ or Artistic) and BSD
URL:            http://search.cpan.org/dist/Tk-TableMatrix/
Source0:        http://search.cpan.org/CPAN/authors/id/C/CE/CERNEY/Tk-TableMatrix-%{version}.tar.gz

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  libX11-devel
# See (RHBZ#456019)
BuildRequires:  perl(Tk)
BuildRequires:  perl(Tk::MMutil)

Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
The TableMatrix command creates a 2-dimensional grid of cells. The
table can use a Tcl array variable or Tcl command for data storage and
retrieval.

%prep
%setup -q -n Tk-TableMatrix-%{version}

# fix perms
chmod 644 COPYING README TableMatrix.pm TableMatrix.xs TableMatrix/Spreadsheet.pm \
  TableMatrix/SpreadsheetHideRows.pm pTk/license.terms pTk/mTk/license.terms
# copy license
cp -p pTk/license.terms license.terms.pTk
cp -p pTk/mTk/license.terms license.terms.mTk

# Fix end-of-line-encoding
touch -r demos/edit_styles.pl demos/edit_styles.pl.timestamps
sed -i 's/\r//' demos/edit_styles.pl
touch -r demos/edit_styles.pl.timestamps demos/edit_styles.pl
rm demos/edit_styles.pl.timestamps


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%install
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

chmod -x demos/*

%check
# disabled by default because it needs an x screen
%{?_with_tests:make test}


%files
%doc ChangeLog COPYING README Changes
# See (RHBZ#456019).
%doc license.terms.pTk license.terms.mTk
%doc demos
%{perl_vendorarch}/Tk/
%{perl_vendorarch}/auto/*
%{_mandir}/man3/*.3*


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep 08 2013 Emmanuel Seyman <emmanuel@seyman.fr> - 1.23-19
- Remove no-longer-needed macros
- Add perl default filter

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.23-17
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.23-14
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 13 2011 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.23-12
- Add BR: perl(Tk::MMutil).

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.23-11
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.23-9
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.23-8
- Mass rebuild with perl-5.12.0

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1.23-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 kwizart < kwizart at gmail.com > - 1.23-4
- Fix encoding

* Sat Jul 19 2008 kwizart < kwizart at gmail.com > - 1.23-3
- Add conditional build --with tests
- Add demos directory as %%doc

* Mon May 19 2008 kwizart < kwizart at gmail.com > - 1.23-2
- Fix directory owership for perl packages.
- Add BR libX11-devel

* Wed Apr 30 2008 kwizart < kwizart at gmail.com > - 1.23-1
- Initial package for Fedora

