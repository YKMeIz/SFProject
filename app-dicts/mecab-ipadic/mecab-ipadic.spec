# This spec file is very similar with mecab-jumandic

%define		majorver	2.7.0
%define		date		20070801

%define		mecabver	0.96

# The data in MeCab dic are compiled by arch-dependent binaries
# and the created data are arch-dependent.
# However, this package does not contain any executable binaries
# so debuginfo rpm is not created.
%define		debug_package	%{nil}

Name:		mecab-ipadic
Version:	%{majorver}.%{date}
Release:	10%{?dist}.1
Summary:	IPA dictionary for MeCab

Group:		Applications/Text
License:	mecab-ipadic
URL:		http://mecab.sourceforge.net/
Source0:	http://downloads.sourceforge.net/mecab/%{name}-%{majorver}-%{date}.tar.gz
#Source2:	http://www.icot.or.jp/ARCHIVE/terms-and-conditions-for-IFS-J.html
Source2:	http://www.jipdec.or.jp/icot/ARCHIVE/terms-and-conditions-for-IFS-J.html
Source3:	LICENSE.Fedora
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	mecab-devel >= %{mecabver}
Requires:	mecab >= %{mecabver}

%description
MeCab IPA is a dictionary for MeCab using CRF estimation
based on IPA corpus.
This dictionary is for UTF-8 use.

%package 	EUCJP
Summary:	IPA dictionary for Mecab with encoded by EUC-JP
Group:		Applications/Text
Requires:	mecab >= %{mecabver}

%description EUCJP

MeCab IPA is a dictionary for MeCab using CRF estimation
based on IPA corpus.
This dictionary is for EUC-JP use.

%prep
%setup -q -n %{name}-%{majorver}-%{date}

%build
# First build on UTF-8
%configure \
	--with-mecab-config=%{_bindir}/mecab-config \
	--with-charset=utf8
%{__make} %{?_smp_mflags}
# Preserve them
%{__mkdir} UTF-8
%{__cp} -p \
	*.bin *.dic *.def dicrc \
	UTF-8/

# Next build on EUC-JP
# This is the default, however Fedora uses UTF-8 so
# for Fedora this must be the option.
%{__make} clean
%configure \
	--with-mecab-config=%{_bindir}/mecab-config
%{__make} %{?_smp_mflags}


%install
# First install EUC-JP
%{__rm} -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
%{__mv} $RPM_BUILD_ROOT%{_libdir}/mecab/dic/ipadic \
	$RPM_BUILD_ROOT%{_libdir}/mecab/dic/ipadic-EUCJP

# Next install UTF-8
%{__mv} -f UTF-8/* .
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%{__cp} -p %{SOURCE2} LICENSE.jp.html
%{__cp} -p %{SOURCE3} .

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
# Note: post should be okay. mecab-dic expects that
# mecab is installed in advance.
if test -f %{_sysconfdir}/mecabrc ; then
	%{__sed} -i -e 's|^dicdir.*|dicdir = %{_libdir}/mecab/dic/ipadic|' \
		%{_sysconfdir}/mecabrc || :
fi

%post EUCJP
# Note: post should be okay. mecab-dic expects that
# mecab is installed in advance.
if test -f %{_sysconfdir}/mecabrc ; then
	%{__sed} -i -e 's|^dicdir.*|dicdir = %{_libdir}/mecab/dic/ipadic-EUCJP|' \
		%{_sysconfdir}/mecabrc || :
fi

%files
%defattr(-,root,root,-)
%doc COPYING LICENSE.* README
%{_libdir}/mecab/dic/ipadic/

%files EUCJP
%defattr(-,root,root,-)
%doc COPYING LICENSE.* README
%{_libdir}/mecab/dic/ipadic-EUCJP/


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0.20070801-10.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0.20070801-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0.20070801-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0.20070801-7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0.20070801-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0.20070801-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0.20070801-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 13 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Fix URL for Source2

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0.20070801-3
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0.20070801-2
- F-11: Mass rebuild

* Fri Aug  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0.20070801.dist.1
- License update

* Wed Aug  1 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0.20070801
- New release 2.7.0-20070801

* Mon Jun 11 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0.20070610
- New release 2.7.0-20070610

* Sat Mar 24 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0.20060707-2
- Fix typo

* Thu Mar  8 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.7.0.20060707-1
- Initial packaging, based on mecab-jumandic spec file