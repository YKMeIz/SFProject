Name:			perl-Gtk2-Unique
Version:		0.05
Release:		10%{?dist}
Summary:		Perl bindings for the C library "libunique"
License:		GPL+ or Artistic
Group:			Development/Libraries
URL:			http://search.cpan.org/dist/Gtk2-Unique/
Source0:		http://mirrors.163.com/cpan/authors/id/P/PO/POTYL/Gtk2-Unique-%{version}.tar.gz
BuildRequires:		perl(ExtUtils::Depends) >= 0.20
BuildRequires:		perl(ExtUtils::MakeMaker)
BuildRequires:		perl(ExtUtils::PkgConfig) >= 1.03
BuildRequires:		perl(Glib) >= 1.180
BuildRequires:		perl(Glib::MakeHelper)
BuildRequires:		perl(Gtk2) >= 1.00
BuildRequires:		perl(Test::More)
BuildRequires:		unique-devel
Requires:		perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%{?perl_default_filter}

%description
Gtk2::Unique is a Perl binding for the C library libunique 
which provides a way for writing single instance application. 
If you launch a single instance application twice, the second 
instance will either just quit or will send a message to 
the running instance.

For more information about libunique see: 
http://live.gnome.org/LibUnique.

%package devel
Summary:		Development headers for %{name}
Group:			Development/Libraries
Requires:		%{name} = %{version}-%{release}

%{?perl_default_filter}

%description devel
Development headers for %{name}

%prep
%setup -q -n Gtk2-Unique-%{version}

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
%doc Changes README
%{perl_vendorarch}/auto/Gtk2/Unique/
%{perl_vendorarch}/Gtk2*
%exclude %{perl_vendorarch}/Gtk2/Unique/Install/*.h
%{_mandir}/man3/*.3pm*

%files devel
%{perl_vendorarch}/Gtk2/Unique/Install/*.h

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 0.05-9
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Petr Pisar <ppisar@redhat.com> - 0.05-6
- Perl 5.16 rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.05-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Iain Arnell <iarnell@gmail.com> 0.05-4
- Rebuild for libpng 1.5
- BuildRequires perl(Test::More)

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 0.05-3
- Perl mass rebuild

* Sun Jun 19 2011 Liang Suilong <liangsuilong@gmail.com> 0.05-2
- Add a devel subpackage
- Fix spec file errors 

* Sat Jun 04 2011 Liang Suilong <liangsuilong@gmail.com> 0.05-1
- Intial Package for Fedora 15

