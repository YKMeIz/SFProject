Name:           perl-X11-Protocol-Other
Version:        28
Release:        1%{?dist}
Summary:        Miscellaneous X11::Protocol helpers
License:        GPLv3+
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/X11-Protocol-Other/
Source0:        http://www.cpan.org/modules/by-module/X11/X11-Protocol-Other-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Encode::Encoding)
BuildRequires:  perl(Encode::HanExtra)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(lib)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test)
BuildRequires:  perl(X11::Protocol)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
These are some helper functions for X11::Protocol.

%prep
%setup -q -n X11-Protocol-Other-%{version}
chmod a-x examples/*

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes COPYING examples
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Nov 13 2013 Robin Lee <cheeselee@fedoraproject.org> - 28-1
- Update to version 28

* Tue Oct  1 2013 Robin Lee <cheeselee@fedoraproject.org> - 25-1
- Update to 25

* Thu Sep 26 2013 Robin Lee <cheeselee@fedoraproject.org> - 24-1
- Update to version 24

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Petr Pisar <ppisar@redhat.com> - 23-3
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Petr ??abata <contyk@redhat.com> - 23-1
- 23 bump (testsuite update)

* Mon Nov 26 2012 Petr ??abata <contyk@redhat.com> - 22-1
- 22 bump (testsuite update)

* Mon Nov 05 2012 Petr ??abata <contyk@redhat.com> - 21-1
- 21 bump
- Fix the deps
- Modernize the spec a bit
- Package the examples

* Sat Aug 11 2012 Robin Lee <cheeselee@fedoraproject.org> 18-1
- Specfile autogenerated by cpanspec 1.78.
