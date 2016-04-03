Name:           gscan2pdf
Version:        1.2.5
Release:        2%{?dist}
Summary:        GUI for producing a multipage PDF from a scan

Group:          Applications/Publishing
License:        GPLv3
URL:            http://gscan2pdf.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  perl(ExtUtils::MakeMaker), perl(Test::More)
BuildRequires:  gettext, desktop-file-utils

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       djvulibre, sane-backends >= 1.0.17, sane-frontends
Requires:       xdg-utils, unpaper, gocr, GConf2, libtiff-tools
Requires:       perl(Gtk2::Ex::PodViewer), perl(PDF::API2), perl(forks)
Requires:       perl(Set::IntSpan)

%description
A GUI to ease the process of producing a multipage PDF from a scan.


%prep
%setup -q

# substitute gconftool-2 for gconftool
sed -i 's/gconftool --get/gconftool-2 --get/' bin/gscan2pdf

# fix file that is not UTF-8
iconv --from=ISO-8859-1 --to=UTF-8 History > History.new
mv History.new History

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
rm -f $RPM_BUILD_ROOT/%{perl_archlib}/perllocal.pod
chmod -R u+w $RPM_BUILD_ROOT/*

desktop-file-install --delete-original \
  --dir=$RPM_BUILD_ROOT/%{_datadir}/applications         \
  $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%check
# disable test for now - there are a lot of dependencies that were not in
# versions prior to 1.0.0
#make test

%post
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc LICENCE History
%{_bindir}/*
%{perl_vendorlib}/*
%{_datadir}/%{name}
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/pixmaps/%{name}.svg
%{_mandir}/man1/*.1*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Richard Hughes <richard@hughsie.com> - 1.2.5-1
- v 1.2.5

* Tue Mar 11 2014 Bernard Johnson <bjohnson@symetirx.com> - 1.2.3-1
- v 1.2.3 (bz #1034069)
- substitute a sed command to change gconftool-2 change

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.1.3-3
- Perl 5.18 rebuild

* Tue Apr 23 2013 Jon Ciesla <limburgher@gmail.com>  -1.1.3-2
- Drop desktop vendor tag.

* Tue Mar 05 2013 Sven Lankes <sven@lank.es>  -1.1.3-1
- new upstream release

* Sat Feb 16 2013 Sven Lankes <sven@lank.es>  -1.1.2-1
- new upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 16 2012 Sven Lankes <sven@lank.es>  -1.1.0-1
- new upstream release

* Fri Aug 24 2012 Sven Lankse <sven@lank.es> - 1.0.6-1
- new upstream release (bz #840442)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.0.4-2
- Perl 5.16 rebuild

* Fri May 25 2012 Bernard Johnson <bjohnson@symetirx.com> - 1.0.4-1
- v 1.0.4 (bz #810826)

* Wed Mar 28 2012 Bernard Johnson <bjohnson@symetrix.com> - 1.0.2-1
- v 1.0.2 (bz #787361, bz #807604)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Bernard Johnson <bjohnson@symetrix.com> - 1.0.0-1
- v 1.0.0 (bz #740997)
- disable tests for now due to dependencies
