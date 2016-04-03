%global svndate 20120803
%global svnver 9601

Name:		halibut
Summary:	TeX-like software manual tool
Version:	1.0
Release:	10.%{svndate}svn%{svnver}%{?dist}
License:	MIT and APAFML
Group:		Applications/Text
URL:		http://www.chiark.greenend.org.uk/~sgtatham/halibut.html
#Source0:	http://www.chiark.greenend.org.uk/~sgtatham/halibut/%{name}-%{version}.tar.gz
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export -r %%{svnver} svn://svn.tartarus.org/sgt/halibut halibut-%%{svndate}
#  pushd halibut-%%{svndate}
#  svn export -r %%{svnver} svn://svn.tartarus.org/sgt/charset
#  popd
#  tar -cjvf halibut-%%{svndate}.tar.bz2 halibut-%%{svndate}
Source0:	%{name}-%{svndate}.tar.bz2

%description
Halibut is yet another text formatting system, intended primarily for
writing software documentation. It accepts a single source format and
outputs a variety of formats, planned to include text, HTML, Texinfo,
Windows Help, Windows HTMLHelp, PostScript and PDF. It has comprehensive
indexing and cross-referencing support, and generates hyperlinks within
output documents wherever possible.

%package -n vim-halibut
Summary:	Syntax file for the halibut manual tool
Group:		Applications/Editors
Requires:	vim-filesystem
BuildArch:	noarch

%description -n vim-halibut
This package provides vim syntax support for Halibut input files (*.but).

%prep
%setup -q -n %{name}-%{svndate}

%build
sed -i 's/CFLAGS += -g/CFLAGS += /g' Makefile
export CFLAGS="%{optflags}"
make %{?_smp_mflags} VERSION="%{version}"
make -C doc

%install
rm -rf %{buildroot}
make install prefix="%{buildroot}%{_prefix}" mandir="%{buildroot}%{_mandir}" INSTALL="install -Dp"
install -d  html
install -pm 0644 doc/*.html html
install -d %{buildroot}%{_datadir}/vim/vimfiles/syntax
install -pm 0644 misc/halibut.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENCE html
%{_bindir}/halibut
%{_mandir}/man1/*.1*

%files -n vim-halibut
%defattr(-,root,root,-)
%doc LICENCE
%{_datadir}/vim/vimfiles/syntax/*.vim

%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10.20120803svn9601
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9.20120803svn9601
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8.20120803svn9601
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7.20120803svn9601
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 24 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0-6.20120803svn9601
- Fixed licensing (added APAFML) according to fedora-legal

* Wed Sep 19 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0-5.20120803svn9601
- Used global instead of define
- Added license file to vim-halibut subpackage
- Changed vim-halibut dependency, it depends on vim-filesystem not vim-common

* Tue Aug  7 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0-4.20120803svn9601
- New svn checkout

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-3.20100504svn8934
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 10 2010 Chen Lei <supercyper@163.com> - 1.0-2.20100504svn8934
- merge -doc subpackage to the main package

* Tue May 04 2010 Chen Lei <supercyper@163.com> - 1.0-1.20100504svn8934
- initial rpm build
