Name:           perl-Gtk2-GladeXML
Version:        1.007
Release:        19%{?dist}
Summary:        Create user interfaces directly from Glade XML files

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://search.cpan.org/dist/Gtk2-GladeXML/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TS/TSCH/Gtk2-GladeXML-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# non-perl
BuildRequires:  libglade2-devel >= 2.0.0

BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(ExtUtils::Depends) >= 0.300
BuildRequires:  perl(ExtUtils::PkgConfig)
BuildRequires:  perl(Glib)
BuildRequires:  perl(Glib::MakeHelper)
BuildRequires:  perl(Gtk2)
BuildRequires:  perl(Test::More)

%{?perl_default_filter}

%description
Glade is a free user interface builder for GTK+ and GNOME. 
After designing a user interface with glade-2 the layout 
and configuration are saved in an XML file. libglade is a 
library which knows how to build and hook up the user interface 
described in the Glade XML file at application run time.

This extension module binds libglade to Perl so you can 
create and manipulate user interfaces in Perl code in 
conjunction with Gtk2 and even Gnome2. Better yet you can 
load a file's contents into a PERL scalar do a few magical 
regular expressions to customize things and the load up the app. 
It doesn't get any easier.


%prep
%setup -q -n Gtk2-GladeXML-%{version}

chmod -c -x examples/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'

%{_fixperms} %{buildroot}/*


%check
make test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog LICENSE NEWS README
%doc examples/
%{perl_vendorarch}/auto/Gtk2/
%{perl_vendorarch}/Gtk2*
%{_mandir}/man3/*.3*


%changelog
* Mon Sep 01 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.007-19
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 1.007-15
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 1.007-12
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Iain Arnell <iarnell@gmail.com> 1.007-10
- Rebuild for libpng 1.5
- BuildRequires perl(Test::More)

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.007-9
- Perl mass rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.007-8
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.007-7
- Mass rebuild with perl-5.12.0

* Sun Mar 14 2010 Chris Weyl <cweyl@alumni.drew.edu> 1.007-6
- add perl_default_filter

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.007-5
- rebuild against perl 5.10.1

* Wed Aug 05 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.007-4
- Fix mass rebuild breakdown: Add BR: perl(Glib::MakeHelper).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Chris Weyl <cweyl@alumni.drew.edu> 1.007-1
- update to 1.007
- correct license tag (LGPLv2+, _not_ GPLv2+)
- minor spec tweaks, mostly cosmetic

* Thu Mar  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.006-4
- rebuild for new perl

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.006-3
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.006-2
- bump

* Wed Sep 20 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.006-1
- update to 1.006

* Tue Sep 19 2006 Chris Weyl <cweyl@alumni.drew.edu> 1.005-5
- taking co-maintainership post-mass rebuild
- fix certain rpmlint warnings

* Wed Sep 14 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 1.005-4
- Added OPTIMIZE="$RPM_OPT_FLAGS" and 
  removed "find examples -type f -exec chmod -x {} ';'"

* Thu Aug 18 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 1.005-3
- Third build.

* Thu Aug 18 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 1.005-2
- Second build.

* Sun Jul 3 2005 Gavin Henry <ghenry[AT]suretecsystems.com> - 1.002-1
- First build.
