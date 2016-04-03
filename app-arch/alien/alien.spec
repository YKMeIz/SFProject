Summary:        Converter between the rpm, dpkg, stampede slp, and Slackware tgz file formats
Name:           alien
Version:        8.90
Release:        3%{?dist}

Group:          Applications/System
License:        GPLv2+
URL:            http://kitenet.net/~joey/code/alien/
Source:         http://ftp.debian.org/debian/pool/main/a/alien/alien_%version.tar.gz

Requires:       dpkg, debhelper, rpm-build
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  perl(ExtUtils::MakeMaker)

BuildArch:      noarch



%description
Alien is a program that converts between the rpm, dpkg, stampede 
slp, and Slackware tgz file formats. If you want to use a package 
from another distribution than the one you have installed on your 
system, you can use alien to convert it to your preferred package 
format and install it.

%prep
%setup -qn %{name}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor VARPREFIX=%{buildroot}

make

%install
make pure_install DESTDIR=%{buildroot} \
        VARPREFIX=%{buildroot} \
        PREFIX=%{buildroot}%{_prefix}

rm -rf %{buildroot}%{perl_vendorarch}/auto/Alien

chmod 755 %{buildroot}%{_bindir}/alien

%files
%doc GPL README debian/changelog
%{_bindir}/*
%{_datadir}/%{name}
%{perl_vendorlib}/*
%{_mandir}/man?/*
%{_localstatedir}/lib/alien

%changelog
* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 8.90-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Dmitrij S. Kryzhevich <krege@land.ru> - 8.90-1
- Update 8.90.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.88-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 8.88-3
- Perl 5.18 rebuild

* Wed May 22 2013 Dmitrij S. Kryzhevich <krege@land.ru> - 8.88-2
- No need for "defattr" in files section.

* Tue May 21 2013 Dmitrij S. Kryzhevich <krege@land.ru> - 8.88-1
- Update to 8.88.

* Tue Nov 23 2010 Dmitrij S. Kryzhevich <krege@land.ru> - 8.83-1
- First try.
