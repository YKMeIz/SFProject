Name:           GREYCstoration
Version:        2.8
Release:        18%{?dist}
Summary:        An image denoising and interpolation tool
Group:          Applications/Multimedia
License:        CeCILL
URL:            http://www.greyc.ensicaen.fr/~dtschump/greycstoration/index.html
Source0:        http://downloads.sourceforge.net/cimg/%{name}-%{version}.zip
Source1:        %{name}.png
Patch0:         GREYCstoration-2.8-fixmakefile.patch
Patch1:         GREYCstoration-2.8-libpng15.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gimp-devel gimp
BuildRequires:  desktop-file-utils
BuildRequires:  libpng-devel libjpeg-devel libtiff-devel fftw-devel

%description
GREYCstoration is an image regularization algorithm which is able to process
a color image by locally removing small variations of pixel intensities while
preserving significant global image features, such as edges and corners. The
most direct application of image regularization is image denoising. By
extension, it can also be used to inpaint or resize images.


%package gimp
Summary:        GREYCstoration image denoising and interpolation plugin for gimp
Group:          Applications/Multimedia
Requires:       gimp %{name}


%description gimp
GREYCstoration is an image regularization algorithm which is able to process
a color image by locally removing small variations of pixel intensities while
preserving significant global image features, such as edges and corners. The
most direct application of image regularization is image denoising. By
extension, it can also be used to inpaint or resize images.

This package contains the GREYCstoration plugin for gimp.


%package gui
Summary:        GREYCstoration image denoising and interpolation tool
Group:          Applications/Multimedia
Requires:       %{name} hicolor-icon-theme tcl tk


%description gui
GREYCstoration is an image regularization algorithm which is able to process
a color image by locally removing small variations of pixel intensities while
preserving significant global image features, such as edges and corners. The
most direct application of image regularization is image denoising. By
extension, it can also be used to inpaint or resize images.

This package contains the GREYCstoration GUI.


%prep
%setup -q
%patch0 -p1 -b .fixmakefile
%patch1 -p1 -b .libpng15
# Include path for CImg.h is wrong, fix it.
sed -i -r "s|#include \"../CImg.h\"|#include \"CImg.h\"|" src/greycstoration*.cpp
iconv -f iso-8859-1 -t utf-8 Licence_CeCILL_V2-en.txt > Licence_CeCILL_V2-en.txt.conv
mv Licence_CeCILL_V2-en.txt.conv Licence_CeCILL_V2-en.txt
# Fix lib path on lib64 systems
%ifarch ppc64 x86_64
  sed -ir "s|/lib|/lib64|" src/Makefile
%endif


%build
make -C src %{?_smp_mflags} CFLAGS="%{optflags} -fno-tree-pre" all

# Build desktop icon
cat >%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=GREYCstoration
GenericName=(Image noise tool)
Comment=%{summary}
Exec=%{_bindir}/%{name}_gui.tcl
Icon=%{name}.png
Terminal=false
Type=Application
StartupNotify=false
Categories=Graphics;2DGraphics;RasterGraphics;
EOF


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/gimp/2.0/plug-ins/
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/96x96/apps
install -m0755 src/greycstoration %{buildroot}%{_bindir}/
install -m0755 src/greycstoration4integration %{buildroot}%{_bindir}/
install -m0755 src/greycstoration4gimp %{buildroot}%{_libdir}/gimp/2.0/plug-ins/
install -m0755 GREYCstoration_gui.tcl %{buildroot}%{_bindir}
install -m0644 %{SOURCE1} %{buildroot}%{_datadir}/icons/hicolor/96x96/apps
desktop-file-install \
        --dir %{buildroot}%{_datadir}/applications \
        %{name}.desktop

%clean
rm -rf %{buildroot}


%post gui
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun gui
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root)
%doc README.txt
%doc Licence_CeCILL_V2-en.txt
%{_bindir}/greycstoration
%{_bindir}/greycstoration4integration

%files gimp
%{_libdir}/gimp/2.0/plug-ins/greycstoration4gimp

%files gui
%{_datadir}/icons/hicolor/96x96/apps/%{name}.png
%{_datadir}/applications/*%{name}.desktop
%{_bindir}/%{name}_gui.tcl

%changelog
* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 12 2013 Jon Ciesla <limburgher@gmail.com> - 2.8-15
- Drop desktop vendor tag.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.8-13
- rebuild due to "jpeg8-ABI" feature drop

* Mon Nov 19 2012 Nils Philippsen <nils@redhat.com> - 2.8-12
- update sourceforge download URL

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 03 2012 Nils Philippsen <nils@redhat.com> - 2.8-10
- rebuild against gimp 2.8.0 release candidate

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Nils Philippsen <nils@redhat.com> - 2.8-8
- rebuild for GIMP 2.7
- fix building with libpng-1.5

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.8-7
- Rebuild for new libpng

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.8-4
- Fixed broken revision 3

* Tue Feb 24 2009 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.8-3
- Fixed dependancy ref BZ#479993

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 08 2008 Nils Philippsen <nils@redhat.com>
- use "-fno-tree-pre" option to avoid ages long compilation with gcc-4.3

* Thu Mar 13 2008 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.8-1
- New upstream version

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.6-3
- Autorebuild for GCC 4.3

* Tue Jan 15 2008 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.6-2
- New upstream version, testing 64 bit build issues

* Wed Jan 09 2008 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.6-1
- New upstream version
-  This release deals with RGB/YCbCr color bases, and processes only particular
-  channels of a hyperspectral image. Only the command line version has been updated.

* Tue Oct 11 2007 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.5.2-6
- Source URL Change

* Mon Oct 10 2007 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.5.2-5
- Specfile fixes

* Thu Oct 04 2007 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.5.2-4
- Fixed Buildroot, Patch, Build and Setup
- Added GUI
- Added support for more image formats in Makefile
- Fixed build on systems with lib64

* Sun Sep 30 2007 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.5.2-3
- Patch makefile regarding stripped binaries

* Fri Sep 28 2007 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.5.2-2
- Missing build require added for gimp

* Fri Sep 28 2007 Marc Bradshaw <packages@marcbradshaw.co.uk> 2.5.2-1
- Initial release
