Summary: Natural language translation library
Name: libtranslate
Version: 0.99
Release: 30%{?dist}
Group: System Environment/Libraries
License: BSD
URL: http://www.nongnu.org/libtranslate
%define url	http://savannah.nongnu.org/download/libtranslate
Source0: %{url}/libtranslate-%{version}.tar.gz
Source1: libtranslate-services.xml-20100303
Patch1: %{url}/libtranslate-0.99-charsetparse.diff
Patch2: %{url}/libtranslate-0.99-condfix.diff
Patch3: %{url}/libtranslate-0.99-int64.diff
Patch4: %{url}/libtranslate-0.99-postmarker.diff
Patch10: libtranslate-0.99-libsoup24.diff
Patch11: libtranslate-0.99-fix-modules.patch
Patch12: libtranslate-0.99-strip_tags.patch
Patch13: libtranslate-0.99-autoconf.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig >= 1:0.8, gettext, intltool, libtool
BuildRequires: glib2-devel, libsoup-devel >= 2.2, libxml2-devel
BuildRequires: gnutls-devel, libgcrypt-devel
#  needed for autoconf tools
BuildRequires: gtk-doc


%description 
Libtranslate is a library for translating text and web pages
between natural languages. Its modular infrastructure allows
to implement new translation services separately from the core library.

Libtranslate is shipped with a generic module supporting
web-based translation services such as Babel Fish, Google Language Tools
and SYSTRAN. Moreover, the generic module allows to add new services
simply by adding a few lines to a XML file (see libtranslate(5)).

The libtranslate distribution includes a powerful command line interface
(see translate(1)). GNOME GUI can be found as separate "gnome-translate"
package at the same web source.


%package devel
Summary: Natural language translation library, static libs and headers
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig >= 1:0.8

%description devel
The static libraries and header files for %{name} library.


%prep
%setup -q -n %{name}-%{version}
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

libtoolize --automake
intltoolize --automake --force
aclocal -I m4
autoheader
autoconf
automake --add-missing


%build
%configure --disable-static
make

pushd docs/man
iconv -f ISO8859-1 -t UTF8 <translate.1 > translate.1.new && \
					mv -f translate.1.new translate.1
popd


%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

pushd $RPM_BUILD_ROOT%{_mandir}/man5
mv -f services.xml.5 libtranslate.5
popd

rm -f $RPM_BUILD_ROOT%{_datadir}/libtranslate/services.xml
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/libtranslate/services.xml

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libtranslate/modules/*.la

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-, root, root, -)

%doc AUTHORS COPYING README
%{_libdir}/libtranslate.so.*
%{_libdir}/libtranslate/
%{_datadir}/libtranslate/
%{_bindir}/*
%{_mandir}/*/*


%files devel
%defattr(-, root, root, -)

%{_libdir}/libtranslate.so
%{_includedir}/libtranslate/
%{_datadir}/gtk-doc/html/*
%{_libdir}/pkgconfig/*


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-28
- fix build (#914152)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-24
- fix autoconf stuff for Fedora 15 (#631105)

* Wed Mar  3 2010 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-23
- handle tags inside the text properly (#541234)
- remove static library (#556076)
- update services.xml (by me and Dwayne Bailey <dwayne@translate.org.za>)

* Wed Aug 26 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-22
- add new language pairs for google service
  (#519247, by Dwayne Bailey <dwayne@translate.org.za>)
- use up-to-date services.xml.in plain file as an additional source,
  instead of a lot of patches for upstream's one

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar  3 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-20
- add more language pairs for google service
  (#487951, by Dwayne Bailey (dwayne@translate.org.za>)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-18
- update services.xml (google, babelfish, add apertium and opentrad) (#478626)
  (by Dwayne Bailey <dwayne@translate.org.za>)

* Mon Dec 22 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-17
- update fix-modules patch, more autotools to run
  (by Dwayne Bailey <dwayne@translate.org.za>)

* Fri Dec 19 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-16
- add fix-modules patch (#477077)

* Wed Jun 25 2008 Tomas Mraz <tmraz@redhat.com> - 0.99-15
- rebuild with new gnutls

* Thu Feb 14 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-14
- rebuild against libsoup-2.3.2

* Tue Jan 29 2008 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-13
- Add support for libsoup > 2.2 (Patch from Dan Winship <dwinship@redhat.com>)
- Change upstreamed patches to the correspond upstream ones.

* Mon Dec 10 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-12
- more updates for services.xml (fix 1800translate, papiamentu,
  drop tsunami and worldlingo as not useful now).

* Thu Dec  6 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-11
- add post-marker patch (#411861, from <timosha@gmail.com>)
- more updates for services.xml (#401621)

* Mon Dec  3 2007 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-10
- update services.xml to conform the current conditions.

* Fri Sep  1 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-9
- rebuild for FC6

* Mon Jul  3 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-8
- add BR: intltool

* Fri Jun 16 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-7
- rebuilt with new gnutls for FC6

* Tue Mar 21 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-6
- add upstream's patch fixing memory exhaustion on 64-bit platforms

* Wed Feb 15 2006 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-5
- rebuild for FC5

* Wed Sep  7 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-4
- even more cleanups
- Accepted for Fedora Extra
  (review by Tom "spot" Callaway <tcallawa@redhat.com>)

* Fri Aug 19 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-3
- more cleanups

* Thu Aug 18 2005 Tom "spot" Callaway <tcallawa@redhat.com> - 0.99-2
- cleanups

* Mon Aug  8 2005 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.99-1
- convert translate(1) manual to unicode (it contains non-ascii in examples)
- rename service.xml(5) manual to libtranslate(5)

* Fri Jul 29 2005 Dmitry Butskoy <Dmitry@Butskoy.name>
- Add Promt (www.online-translator.com) service.

* Fri Jul 22 2005 Dmitry Butskoy <Dmitry@Butskoy.name> 
- Initial release.
