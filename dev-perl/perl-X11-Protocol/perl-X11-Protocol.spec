Name:           perl-X11-Protocol
Version:        0.56
Release:        16%{?dist}
Summary:        X11-Protocol - Raw interface to X Window System servers

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/X11-Protocol/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SM/SMCCAM/X11-Protocol-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  /usr/bin/perldoc
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
X11::Protocol is a client-side interface to the X11 Protocol (see X(1) for
information about X11), allowing perl programs to display windows and
graphics on X11 servers.

A full description of the protocol is beyond the scope of this documentation;
for complete information, see the I<X Window System Protocol, X Version 11>,
available as Postscript or *roff source from C<ftp://ftp.x.org>, or
I<Volume 0: X Protocol Reference Manual> of O'Reilly & Associates's series of
books about X (ISBN 1-56592-083-X, C<http://www.oreilly.com>), which contains
most of the same information.

%prep
%setup -q -n X11-Protocol-%{version}

# Testing requires X - use "rpmbuild --with X"
%if 0%{!?_with_X:1}
%{__perl} -pi -e 'print "print \"Remaining tests require X\n\"; exit 0;" 
    if /Insert your test code below/;' test.pl 
%endif

/usr/bin/perldoc -t perlartistic > Artistic
/usr/bin/perldoc -t perlgpl > COPYING

# Remove shebangs from module code
find . -name '*.pm' -exec sed -i -e '/^#!\/usr\/bin\/perl$/d' {} ';'


%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README Changes Todo eg COPYING Artistic
%{perl_vendorlib}/X11/
%{_mandir}/man3/*.3*


%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 0.56-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 0.56-12
- Perl 5.16 rebuild

* Tue Jan 17 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 0.56-11
- BR: and use /usr/bin/perldoc (Fix mass rebuild FTBFS).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.56-9
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.56-7
- 661697 rebuild for fixing problems with vendorach/lib

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.56-6
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.56-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.56-2
Rebuild for new perl

* Tue Sep 18 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 0.56-1
- New upstream release (bugfix)
- Added BR for perl(ExtUtils::MakeMaker)
- License clarification
- Minor spec cleanup, mainly to suppress rpmlint warnings

* Fri Sep 15 2006 Duncan Ferguson <duncan_j_ferguson@yahoo.co.uk> 0.55-5
- FC-6 rebuild requests

* Tue Jun 20 2006 Duncan Ferguson <duncan_j_ferguson@yahoo.co.uk> 0.55-4
- Update due to bug 195879

* Sun Apr 02 2006 Duncan Ferguson <duncan_j_ferguson@yahoo.co.uk> 0.55-3
- Change tests for X environment

* Sat Apr 01 2006 Duncan Ferguson <duncan_j_ferguson@yahoo.co.uk> 0.55-2
- Specfile bugfile

* Fri Mar 31 2006 Duncan Ferguson <duncan_j_ferguson@yahoo.co.uk> 0.55-1
- Update to new version of X11::Protocol

* Fri Aug 26 2005 Paul Howarth <paul@city-fan.org> 0.54-2
- remove redundant BR: perl
- remove compiler optimization flags, redundant for noarch package
- require "rpmbuild --with X" to run tests requiring X
- include examples as %%doc
- include license text

* Thu Aug 18 2005 Duncan Ferguson <duncan_j_ferguson@yahoo.co.uk> 0.54-1
- Initial build
