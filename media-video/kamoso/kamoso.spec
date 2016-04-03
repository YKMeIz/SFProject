Name:           kamoso
Version:        2.0.2
Release:        14%{?dist}
Summary:        Application for taking pictures and videos from a webcam

Group:          Applications/Multimedia
License:        GPLv2+
URL:            https://projects.kde.org/projects/extragear/multimedia/kamoso/
Source0:        http://download.kde.org/stable/kamoso/%{version}/src/%{name}-%{version}.tar.bz2

## upstream patches
Patch105: 0005-Make-the-About-dialog-work.patch
Patch121: 0021-add-include.patch
Patch131: 0031-Store-and-install-kamoso.desktop-with-755-permission.patch
Patch132: 0032-use-camera-web-icon-instead-of-webcamreceive.patch
Patch133: 0033-initial-port-to-libkipi-2.x.patch
Patch134: 0034-add-license-header.patch
Patch135: 0035-fix-build-for-libkipi-2.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  kdelibs4-devel >= 4.6.0
BuildRequires:  pkgconfig(libkipi) 
BuildRequires:  qt-gstreamer-devel

Requires: kde-runtime
%{?_kde4_version:Requires: kdelibs4%{?_isa} >= %{_kde4_version}}

%description
Kamoso is an application to take pictures and videos out of your webcam.


%prep
%setup -q

%patch105 -p1 -b .0005
%patch121 -p1 -b .0021
%patch131 -p1 -b .0031
%patch132 -p1 -b .0032
%patch133 -p1 -b .0033
%patch134 -p1 -b .0034
%patch135 -p1 -b .0035

# rename some icons that conflict with kdeplasma-addons
# upstreamed,
# http://commits.kde.org/kamoso/b8b03322d58a920deac198c2360d65deddccd610
pushd src/plugins/youtube 
sed -i.bak -e 's|^Icon=youtube|Icon=kipiplugin_youtube|' *.desktop
for icon in icons/*-action-youtube.* ; do
  new_name=$(echo ${icon} | sed -e's|-youtube|-kipiplugin_youtube|')
  mv ${icon} ${new_name}
done


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name}


%check
desktop-file-validate %{buildroot}%{_kde4_datadir}/applications/kde4/%{name}.desktop


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%clean
rm -rf %{buildroot}


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING TODO
%{_kde4_bindir}/%{name}
%{_kde4_bindir}/kamosoPluginTester
%{_kde4_libdir}/kde4/kipiplugin_youtube.so
%{_kde4_iconsdir}/hicolor/*/apps/%{name}.*
%{_kde4_iconsdir}/hicolor/*/actions/*youtube.*
%{_kde4_datadir}/applications/kde4/%{name}.desktop
%{_kde4_datadir}/kde4/services/kipiplugin_youtube.desktop
%{_kde4_datadir}/kde4/servicetypes/kamosoplugin.desktop


%changelog
* Wed Nov  6 2013 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.2-14
- Requires: kde-runtime (#986964)

* Tue Nov  5 2013 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.2-13
- Requires: oxygen-icon-theme (#986964)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-11
- rebuild (libkipi)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-9
- fix build for older libkipi

* Fri Dec 21 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-8
- Kamoso has a missing icon for the pictures button (848079)
- pull in upstream fix for broken about dialog

* Wed Nov 21 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-7
- fix build against libkipi-4.9.50+ (kde#307147)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-5
- rename icons to avoid conflict with kdeplasma-addons' krunner plugin

* Tue May 29 2012 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.2-4
- fix build against libkipi-4.8.80

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 01 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.2-2
- s/libkipi-devel/pkgconfig(libkipi)/

* Mon May 30 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0.2-1
- kamoso-2.0.2

* Sun May 29 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0-1
- kamoso-2.0-final
- License: GPLv2+

* Wed Feb 23 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0-0.4.beta1
- kamoso-2.0-beta1

* Tue Feb 22 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0-0.3.alpha2
- BR: libkipi-devel

* Fri Feb  4 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0-0.2.alpha2
- License: GPLv2+ and GPLv3+

* Thu Feb  3 2011 Alexey Kurov <nucleo@fedoraproject.org> - 2.0-0.1.alpha2
- Initial RPM release
