Name:           mate-doc-utils
Summary:        MATE Desktop doc utils
Version:        1.6.2
Release:        1%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            http://mate-desktop.org
Source0:        http://pub.mate-desktop.org/releases/1.5/%{name}-%{version}.tar.xz
BuildArch:      noarch

BuildRequires:  mate-common
BuildRequires:  pkgconfig(libxslt)
BuildRequires:  pkgconfig(rarian)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  libxml2-python

Requires:       mate-common
Requires:       gnome-doc-utils
# for /usr/share/aclocal
Requires: automake
# for the validation with xsltproc to use local dtds
Requires: docbook-dtds
# for /usr/share/pkgconfig
Requires: pkgconfig
# for /usr/share/xml
Requires: xml-common
# for /usr/share/xml/mallard
Requires: gnome-doc-utils-stylesheets

#For users upgrading from the unofficial MATE desktop Fedora repo
Obsoletes: mate-doc-utils-stylesheets < %{version}-%{release}
Provides: mate-doc-utils-stylesheets = %{version}-%{release}

%description
mate-doc-utils is a collection of documentation utilities for the Mate
project.  Notably, it contains utilities for building documentation and
all auxiliary files in your source tree, and it contains the DocBook
XSLT style sheets that were once distributed with Yelp.

%prep
%setup -q

%build
%configure --disable-scrollkeeper
make %{?_smp_mflags} V=1

%install
%{make_install}

#Remove unnecessary python sitepackages provided by gnome-doc-utils
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/*
rm -rf $RPM_BUILD_ROOT/%{python_sitelib}/xml2po/
rm -rf $RPM_BUILD_ROOT/%{_mandir}/man1/*
rm -rf $RPM_BUILD_ROOT/%{_datadir}/xml/mallard
rm -rf $RPM_BUILD_ROOT/%{_bindir}/xml2po
rm -rf $RPM_BUILD_ROOT/%{_datadir}/pkgconfig/xml2po.pc

%find_lang %{name}


%files -f %{name}.lang
%doc AUTHORS README NEWS COPYING COPYING.GPL COPYING.LGPL
%{_bindir}/mate-doc-prepare
%{_bindir}/mate-doc-tool
%{_datadir}/aclocal/mate-doc-utils.m4
%{_datadir}/mate/help/mate-doc-make
%{_datadir}/mate/help/mate-doc-xslt
%{_datadir}/omf/mate-doc-make
%{_datadir}/omf/mate-doc-xslt
%{_datadir}/mate-doc-utils
%{_datadir}/xml/mate
%{_datadir}/pkgconfig/mate-doc-utils.pc


%changelog
* Fri Oct 25 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-1
- update to 1.6.2 release
- sort spec file
- use modern 'make install' macro
- clean up BR's
- remove debian sript removal, no need anymore
- fix %%{buildroot} vs $RPM_BUILD_ROOT mismatch

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr 21 2013 Dan Mashal <dan.mashal@fedoraproject.org - 1.6.1-1
- Update to 1.6.1
- Remove autogen flags as configure script is included in tarball now

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0 stable release

* Mon Mar 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-4
- Rebuild for Fedora 20 rawhide

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-2
- Add patch to prevent mock build errors

* Tue Oct 30 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release

* Tue Jul 24 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-13
- Update spec file.

* Mon Jul 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-12
- Make changes per package review.

* Mon Jul 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-11
- Make changes per package review.

* Mon Jul 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-10
- Create devel package, fix license and requirements field per package review.

* Mon Jul 23 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-9
- Update spec file

* Sun Jul 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-8
- Fix python sitelib conflicts.

* Sun Jul 22 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-7
- Add language macros and add doc files

* Sat Jul 21 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-6
- Clean up spec file further.

* Tue Jul 17 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-5
- Update requires, licensing, remove unneeded python files

* Mon Jul 16 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-4
- Update licensing

* Sat Jul 14 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-3
- Incorporate Rex's changes, clean up spec file.

* Fri Jul 13 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-2
- omit Group: tag
- fix URL, Source0
- use %%configure macro
- BuildArch: noarch

* Thu Jul 12 2012 Dan Mashal <dan.mashal@fedoraproject.org> 1.4.0-1
- Initial build
