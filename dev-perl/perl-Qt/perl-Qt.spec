Name:           perl-Qt
Version:        0.96.0
Release:        11%{?dist}
Summary:        Perl bindings for Qt
# Files under qtcore/tools/ and qtdbus/tools/ are LGPLv2.1+ with Nokia
# exceptions or GPLv3+. The Nokia files only appear in -devel subpackage.
# QtCore4.pm is 'same terms as Perl itself'. The rest is GPLv2+.
License:        GPLv2+ and (GPL+ or Artistic)
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Qt/
Source0:        http://www.cpan.org/modules/by-module/Qt/Qt-%{version}.tar.gz
Patch1:         0001-Changes-to-support-perl-5.18.0.patch
Patch2:         0002-Fixes-for-perl-5.18.patch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

BuildRequires:  cmake
BuildRequires:  libdb-devel
BuildRequires:  gdbm-devel
BuildRequires:  phonon-devel
BuildRequires:  qimageblitz-devel
BuildRequires:  qscintilla-devel
BuildRequires:  qt-devel
BuildRequires:  qwt-devel
BuildRequires:  smokeqt-devel

BuildRequires:  perl(Carp)  
BuildRequires:  perl(Devel::Peek)  
BuildRequires:  perl(Exporter)  
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(List::MoreUtils)  
BuildRequires:  perl(Scalar::Util)  
BuildRequires:  perl(Test::More)
BuildRequires:  perl(XSLoader)  
BuildRequires:  perl(base)  
BuildRequires:  perl(strict)  
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)  

%?perl_default_filter
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}::_(internal|overload)\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}::_(internal|overload)\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^QtCore4\\.so

%description
This module provides Perl bindings for the Qt 4 libraries.

%package devel
Summary:        Development files for perl-Qt
License:        GPLv2+ and (GPL+ or Artistic) and (LGPLv2+ with exceptions or GPLv3+)
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for perl-Qt.

%prep
%setup -q -n Qt-%{version}

# Fixes from upstream for Perl 5.18
%patch1 -p1
%patch2 -p1

mkdir build

# fix smoke qwt detection
sed -i -e 's/SMOKE_Qwt5_Qt4_FOUND/SMOKE_QWT_FOUND/' CMakeLists.txt

# these tests require running X server
sed -i -e '/perlqt_qtcore4_qapp/d' \
       -e '/perlqt_qtcore4_sigslot/d' \
       -e '/perlqt_qtcore4_sigslot_inherit/d' \
       -e '/perlqt_qtcore4_handlers/d' qtcore/t/CMakeLists.txt
sed -i -e '/perlqt_qsignalspy/d' qttest/t/CMakeLists.txt
sed -i -e '/perlqt_itemviewspixelator/d' \
       -e '/perlqt_itemviewspuzzle/d' \
       -e '/perlqt_helpcontextsensitivehelp/d' \
       -e '/perlqt_mainwindowsmdi/d' \
       -e '/perlqt_networkbroadcast/d' \
       -e '/perlqt_networkfortune/d' \
       -e '/perlqt_networkgooglesuggest/d' \
       -e '/perlqt_paintingfontsampler/d' \
       -e '/perlqt_richtextcalendar/d' \
       -e '/perlqt_sqlquerymodel/d' \
       -e '/perlqt_widgetscalculator/d' \
       -e '/perlqt_xmlstreambookmarks/d' qtgui/t/CMakeLists.txt

%build
cd build
%{cmake_kde4} \
    -DCUSTOM_PERL_SITE_ARCH_DIR=%{perl_vendorarch} \
    -DCMAKE_SKIP_RPATH=YES \
    -DENABLE_GUI_TESTS=YES \
    ..
make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

%{_fixperms} %{buildroot}/*

%check
cd build
export PERL5LIB="$PWD/blib/lib:$PWD/blib/arch"
make test

%files
%doc LICENSE README
%{perl_vendorarch}/*
%exclude %dir %{perl_vendorarch}/auto/

%files devel
%doc qtgui/examples
%{_bindir}/*
%{_includedir}/perlqt
%{_datadir}/perlqt

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 30 2013 Paul Howarth <paul@city-fan.org> - 0.96.0-9
- Add some fixes from upstream git for Perl 5.18 compatibility

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 0.96.0-7
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Petr Pisar <ppisar@redhat.com> - 0.96.0-4
- Perl 5.16 rebuild

* Thu Apr 19 2012 Iain Arnell <iarnell@gmail.com> 0.96.0-3
- build against db5 (rhbz#814083)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.96.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Iain Arnell <iarnell@gmail.com> 0.96.0-1
- initial packaging attempt
