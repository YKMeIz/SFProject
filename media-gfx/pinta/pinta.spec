%global debug_package %{nil}

Name:	    pinta
Version:	1.4
Release:	2%{?dist}
Summary:	An easy to use drawing and image editing program

Group:		Applications/Multimedia

# the code is licensed under the MIT license while the icons are licensed as CC-BY
License:	MIT and CC-BY
URL:		http://pinta-project.com/

Source0:	http://github.com/downloads/PintaProject/Pinta/%{name}-%{version}.tar.gz

# Mono only available on these:
ExclusiveArch: %ix86 x86_64 ppc ppc64 ia64 %{arm} sparcv9 alpha s390x

Requires:	hicolor-icon-theme, mono-addins
BuildRequires:	mono-devel, gtk-sharp2-devel, gettext, desktop-file-utils
BuildRequires:	intltool, mono-addins-devel

%description
Pinta is an image drawing/editing program.
It's goal is to provide a simplified alternative to GIMP for casual users.

%prep
%setup -q

chmod -x readme.md
chmod -x license-mit.txt
chmod -x license-pdn.txt
chmod -x xdg/pinta.1
chmod -x xdg/pinta.xpm
chmod -x xdg/scalable/pinta.svg

sed -i 's/\r//' readme.md
sed -i 's/\r//' license-mit.txt
sed -i 's/\r//' license-pdn.txt
sed -i 's/\r//' pinta.in
sed -i 's/\r//' xdg/pinta.xpm
sed -i 's/\r//' xdg/pinta.1
sed -i 's/\r//' xdg/scalable/pinta.svg

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%find_lang %name
  
%post
update-desktop-database &> /dev/null ||:

touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :

if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc readme.md license-mit.txt license-pdn.txt
%{_libdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}.*
%{_datadir}/man/man1/%{name}*
%{_datadir}/pixmaps/%{name}*

%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 07 2012 Paul Lange <palango@gmx.de> - 1.4-1
- Update to 1.4

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 30 2012 Paul Lange <palango@gmx.de> - 1.3-1
- update to 1.3

* Wed Apr 18 2012 Paul Lange <palango@gmx.de> - 1.2-1
- update to 1.2

* Sat Feb 18 2012 Paul Lange <palango@gmx.de> - 1.1-4
- correct path in bin/pinta

* Sat Feb 11 2012 Paul Lange <palango@gmx.de> - 1.1-3
- Update libdir

* Fri Feb 10 2012 Paul Lange <palango@gmx.de> - 1.1-2
- Add intltool to BuildRequires

* Fri Feb 10 2012 Paul Lange <palango@gmx.de> - 1.1-1
- Update to 1.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Apr 28 2011 Paul Lange <palango@gmx.de> - 1.0-1
- Upload right sources

* Tue Apr 19 2011 Dan Horák <dan[at]danny.cz> - 0.8-2
- updated the supported arch list

* Wed Apr 06 2011 Paul Lange <palango@gmx.de> - 0.8-1
- Update to version 0.8

* Thu Mar 03 2011 Paul Lange <palango@gmx.de> - 0.7-1
- Update to version 0.7

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Paul Lange <palango@gmx.de> - 0.6-1
- Update to version 0.6

* Thu Dec 09 2010 Paul Lange <palango@gmx.de> - 0.5-6
- Upload right sources

* Thu Dec 09 2010 Paul Lange <palango@gmx.de> - 0.5-5
- Fix build for x86_64

* Wed Dec 08 2010 Paul Lange <palango@gmx.de> - 0.5-4
- Fix issues from review

* Sun Dec 05 2010 Paul Lange <palango@gmx.de> - 0.5-3
- Fix build for x86_64

* Wed Dec 01 2010 Paul Lange <palango@gmx.de> - 0.5-2
- Fix rpmlint warnings

* Sat Nov 20 2010 Paul Lange <palango@gmx.de> - 0.5-1
- update to version 0.5

* Sun Aug 01 2010 Paul Lange <palango@gmx.de> - 0.4-3
- Fix links in /bin
- Improve patch naming and add upstream links
- Fix mimetype patch

* Thu Jul 29 2010 Paul Lange <palango@gmx.de> - 0.4-2
- Fix icon cache handling
- Add some Requires and BuildRequires
- Add docs
- Add patches from debian

* Sat May 08 2010 Paul Lange <palango@gmx.de> - 0.4-1
- Initial packaging
