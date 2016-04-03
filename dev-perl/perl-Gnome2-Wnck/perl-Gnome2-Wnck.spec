Name:           perl-Gnome2-Wnck
Version:        0.16
Release:        20%{?dist}
Summary:        Perl interface to the Window Navigator Construction Kit
License:        LGPLv2+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Gnome2-Wnck/
Source0:        http://www.cpan.org/authors/id/T/TS/TSCH/Gnome2-Wnck-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  	perl(ExtUtils::Depends) >= 0.20
BuildRequires:  	perl(ExtUtils::MakeMaker)
BuildRequires:  	perl(ExtUtils::PkgConfig) >= 1.03
BuildRequires:  	perl(Glib) >= 1.180
BuildRequires:	perl(Glib::MakeHelper)
BuildRequires:  	perl(Gtk2) >= 1.00
BuildRequires:  	perl(Test::More)
BuildRequires:  	libXres-devel
BuildRequires:  	libwnck-devel
Requires:       	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
This module allows a Perl developer to 
use the Window Navigator Construction 
Kit library (libwnck for short) to write
 tasklists and pagers.

%prep
%setup -q -n Gnome2-Wnck-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags} NOECHO=

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc ChangeLog LICENSE maps NEWS README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Gnome2*
%{_mandir}/man3/*.3*

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.16-19
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 0.16-16
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Iain Arnell <iarnell@gmail.com> 0.16-14
- Rebuild for libpng 1.5
- BuildRequires perl(Test::More)

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.16-13
- Perl mass rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-11
- 661697 rebuild for fixing problems with vendorach/lib

* Sun May 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.16-10
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.16-9
- rebuild against perl 5.10.1

* Sun Jul 28 2009 Liang Suilong <liangsuilong@gmail.com> 0.16-8
- Add BR: perl(Glib::MakeHelper)
- Remove BR: perl-Glib-devel

* Sun Jul 28 2009 Liang Suilong <liangsuilong@gmail.com> 0.16-7
- Change BuildRequires from perl(Glib::MakeHelper) to perl(Glib)
- Add BR: perl-Glib-devel

* Sun Jul 27 2009 Liang Suilong <liangsuilong@gmail.com> 0.16-6
- Change BuildRequires from perl(Glib) to perl(Glib::MakeHelper)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 10 2009 Liang Suilong <liangsuilong@gmail.com> 0.16-4
- Modify BuildRequires and correct the %%files.

* Sun Apr 21 2009 Liang Suilong <liangsuilong@gmail.com> 0.16-3
- Modify BuildRequires and correct the %%files.

* Fri Mar 13 2009 Suilong Liang <liangsuilong@gmail.com> -0.16-1
-  Fix the bug that the package could not be built on x86_64

* Sat Jan 17 2009 Suilong Liang <liangsuilong@gmail.com> -svn20090118-1
- Initial Package for Fedora 10.
