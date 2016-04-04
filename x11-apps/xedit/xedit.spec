Name:		xedit
Version:	1.2.2
Release:	3%{?dist}
Summary:	Simple text editor for X
Group:		Applications/Editors
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/app/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
License:	MIT and BSD
BuildRequires:	desktop-file-utils
BuildRequires:	libXaw-devel
BuildRequires:	xorg-x11-util-macros
Requires:	xorg-x11-xbitmaps
Requires:	aspell
Requires:	aspell-en
Requires:	grep
Requires:	words
Requires:	ctags
Requires:	xorg-x11-fonts-misc
Requires:	xorg-x11-fonts-75dpi
Requires:	xorg-x11-fonts-100dpi

%description
Xedit provides a simple text editor for X.

%prep
%setup -q

%build
%configure --with-lispdir=%{_datadir}/X11/%{name}

%install
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
install -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop
desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%check
make check

%files
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/%{name}
%{_datadir}/X11/%{name}
%{_datadir}/X11/app-defaults/Xedit
%{_datadir}/X11/app-defaults/Xedit-color
%{_datadir}/applications/%{name}.desktop
%{_mandir}/man1/xedit.1*

%changelog
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.2-2
- Update to latest upstream release (#1195020).

* Wed Jul 16 2014 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.1-1
- Update to latest upstream release.
- Remove patches already in upstream.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 26 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-2
- Patch package to not have BSD 4 clause files.
- Write patch to correct 64 bit overflow tests in a compatible license.
- Update extra patches to use the ones submitted upstream.

* Mon May 21 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.2.0-1
- Add proper documentation to package.
- Update to latest upstream release.
- Remove patches already in upstream.

* Mon Apr 23 2012 pcpa <paulo.cesar.pereira.de.andrade@gmail.com> - 1.1.2-1
- Initial xedit spec.
