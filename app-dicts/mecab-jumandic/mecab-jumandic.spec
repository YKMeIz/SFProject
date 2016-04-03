%define		majorver	5.1
%define		date		20070304

# The data in MeCab dic are compiled by arch-dependent binaries
# and the created data are arch-dependent.
# However, this package does not contain any executable binaries
# so debuginfo rpm is not created.
%define		debug_package	%{nil}

Name:		mecab-jumandic
Version:	%{majorver}.%{date}
Release:	11%{?dist}
Summary:	JUMAN dictorionary for MeCab

Group:		Applications/Text
License:	BSD
URL:		http://mecab.sourceforge.net/
Source0:	http://downloads.sourceforge.net/mecab/%{name}-%{majorver}-%{date}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	mecab-devel
Requires:	mecab

%description
MeCab JUMAN is a dictionary for MeCab using CRF estimation
based on Kyoto corpus.
This dictionary is for UTF-8 use.

%package 	EUCJP
Summary:	JUMAN dictionary for Mecab with encoded by EUC-JP
Group:		Applications/Text
Requires:	mecab

%description EUCJP

MeCab JUMAN is a dictionary for MeCab using CRF estimation
based on Kyoto corpus.
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
%{__mv} $RPM_BUILD_ROOT%{_libdir}/mecab/dic/jumandic \
	$RPM_BUILD_ROOT%{_libdir}/mecab/dic/jumandic-EUCJP

# Next install UTF-8
%{__mv} -f UTF-8/* .
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
# Note: post should be okay. mecab-dic expects that
# mecab is installed in advance.
if test -f %{_sysconfdir}/mecabrc ; then
	%{__sed} -i -e 's|^dicdir.*|dicdir = %{_libdir}/mecab/dic/jumandic|' \
		%{_sysconfdir}/mecabrc || :
fi

%post EUCJP
# Note: post should be okay. mecab-dic expects that
# mecab is installed in advance.
if test -f %{_sysconfdir}/mecabrc ; then
	%{__sed} -i -e 's|^dicdir.*|dicdir = %{_libdir}/mecab/dic/jumandic-EUCJP|' \
		%{_sysconfdir}/mecabrc || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/mecab/dic/jumandic/

%files EUCJP
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_libdir}/mecab/dic/jumandic-EUCJP/


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.20070304-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.20070304-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.20070304-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.20070304-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.20070304-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.20070304-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.20070304-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.1.20070304-4
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.1.20070304-3
- F-11: Mass rebuild

* Fri Jun 13 2008 Jon Stanley <jonstanley@gmail.com> - 5.1-20070304-2
- Rebuild

* Thu Mar  8 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.1.20070304-1
- 5.1 date 20070304

* Sun Mar  4 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.1.20051121-4
- Add missing defattr and make sed script safer.

* Sat Mar  3 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.1.20051121-3
- Change default to UTF-8 and make EUC-JP charset package.

* Tue Feb 27 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.1.20051121-2
- Package requirement deps reconstruct

* Fri Feb 23 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.1.20051121-1
- Initial packaging for Fedora.
