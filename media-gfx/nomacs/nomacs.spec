Name:		nomacs
Version:	1.6.4
Release:	2%{?dist}
License:	GPLv3+
Url:		http://nomacs.org
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-source.tar.bz2
Summary:	Lightweight image viewer
BuildRequires:	cmake, dos2unix, desktop-file-utils
# exiv2-devel opencv-devel LibRaw-devel libtiff-devel
BuildRequires:	pkgconfig(QtGui) >= 4.7, pkgconfig(exiv2) >= 0.20, pkgconfig(opencv) >= 2.1.0, pkgconfig(libraw) >= 0.12.0, pkgconfig(libtiff-4)

%description
nomacs is image viewer based on Qt4 library.
nomacs is small, fast and able to handle the most common image formats.
Additionally it is possible to synchronize multiple viewers
running on the same computer or via LAN is possible.
It allows to compare images and spot the differences
e.g. schemes of architects to show the progress).

%prep
%setup -q
dos2unix Readme/*

%build
mkdir build
pushd build
%cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE:STRING="-O2" -DENABLE_RAW=1 ..
make %{?_smp_mflags}
popd

%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :

%install
pushd build
make DESTDIR=%{buildroot} install
popd
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
# hack - wrong lang code "als" (http://www.nomacs.org/redmine/issues/228)
rm -f translations/nomacs_als.ts
rm -f %{buildroot}/%{_datadir}/%{name}/translations/nomacs_als.qm
%find_lang %{name} --with-qt --without-mo

%files -f %{name}.lang
%doc Readme/[CLR]*
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/translations/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/man1/%{name}.*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 TI_Eugene <ti.eugene@gmail.com> 1.6.4-1
- Version bump.

* Wed Jan 22 2014 Jon Ciesla <limburgher@gmail.com> 1.6.2-2
- Rebuild for new LibRaw.

* Fri Dec 20 2013 TI_Eugene <ti.eugene@gmail.com> 1.6.2-1
- Version bump.

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.6.0.2-2
- rebuild (exiv2)

* Wed Oct 23 2013 TI_Eugene <ti.eugene@gmail.com> 1.6.0.2-1
- Version bump (hotfix).

* Wed Oct 16 2013 TI_Eugene <ti.eugene@gmail.com> 1.6.0-1
- Version bump.

* Mon Jul 15 2013 TI_Eugene <ti.eugene@gmail.com> 1.4.0-1
- Version bump.
- BR libtiff-devel added

* Sat Jun 15 2013 TI_Eugene <ti.eugene@gmail.com> 1.2.0-1
- Version bump.
- %%find_lang macro added
- _als translation removed

* Fri May 31 2013 Jon Ciesla <limburgher@gmail.com> 1.0.2-4
- Rebuild for new LibRaw.

* Tue Apr 09 2013 TI_Eugene <ti.eugene@gmail.com> 1.0.2-3
- CXX flags - -O3 only

* Tue Apr 09 2013 TI_Eugene <ti.eugene@gmail.com> 1.0.2-2
- CXX flags added to %%cmake macro

* Sun Apr 07 2013 TI_Eugene <ti.eugene@gmail.com> 1.0.2-1
- next version
- source url fixed
- description update (removed "free", "windows", licensing)
- update-desktop-database added

* Fri Mar 29 2013 TI_Eugene <ti.eugene@gmail.com> 1.0.0-3
- BuildRequires libraries versions defined

* Fri Mar 29 2013 TI_Eugene <ti.eugene@gmail.com> 1.0.0-2
- disabled EL6/CentOS6 build (due qt < 4.7)

* Fri Mar 29 2013 TI_Eugene <ti.eugene@gmail.com> 1.0.0-1
- initial packaging for Fedora
