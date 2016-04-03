Summary:        FrameBuffer Imageviewer
Name:           fbida
Version:        2.09
Release:        7%{?dist}
License:        GPLv2+
Group:          Applications/Multimedia
URL:            http://linux.bytesex.org/fbida/
Source:         http://dl.bytesex.org/releases/fbida/fbida-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  libexif-devel fontconfig-devel libjpeg-devel
BuildRequires:  libpng-devel libtiff-devel pkgconfig
BuildRequires:  giflib-devel curl-devel
BuildRequires:  libXpm-devel
Requires:       ImageMagick dejavu-sans-mono-fonts
Obsoletes:      fbida-ida < 2.06-1

%description
fbi displays the specified file(s) on the linux console using the
framebuffer device. PhotoCD, jpeg, ppm, gif, tiff, xwd, bmp and png
are supported directly. For other formats fbi tries to use
ImageMagick's convert.

%package fbgs
Group: Applications/Multimedia
Summary: Framebuffer Postscript Viewer
Requires: ghostscript fbida

%description fbgs
A wrapper script for viewing ps/pdf files on the framebuffer console using fbi

%prep
%setup -q
%{__sed} -i -e "s,/X11R6,,g" GNUmakefile
%{__sed} -i -e "s,/usr/X11R6/lib/X11,%{_datadir}/X11,g" mk/Autoconf.mk

%build
LIB=%{_lib} prefix=%{_prefix} CFLAGS=$RPM_OPT_FLAGS %{__make} %{?_smp_mflags} HAVE_MOTIF=no exiftran thumbnail.cgi fbi

%install
%{__rm} -rf %{buildroot}
iconv -t UTF-8 -f ISO-8859-1 fbi.man > fbi.man.new
iconv -t UTF-8 -f ISO-8859-1 exiftran.man > exiftran.man.new
iconv -t UTF-8 -f ISO-8859-1 fbgs.man > fbgs.man.new
%{__mv} fbi.man.new fbi.man
%{__mv} exiftran.man.new exiftran.man
%{__mv} fbgs.man.new fbgs.man
lib=%{_lib} prefix=%{_prefix} %{__make} DESTDIR=%{buildroot} STRIP= install

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes COPYING README TODO
%doc %{_mandir}/man1/fbi*
%doc %{_mandir}/man1/exiftran*
%{_bindir}/fbi
%{_bindir}/exiftran

%files fbgs
%defattr(-, root, root, -)
%doc %{_mandir}/man1/fbgs*
%{_bindir}/fbgs

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.09-4
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.09-3
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 07 2012 Adrian Reber <adrian@lisas.de> - 2.09-1
- updated to 2.09

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.07-9
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Matěj Cepl <mcepl@redhat.com> - 2.07-6
- actually ida* stuff doesn't get build without Motif

* Thu Feb 26 2009 Matěj Cepl <mcepl@redhat.com> - 2.07-5
- Fix dependencies on fonts (bug# 480450) -- I made a typo in
  BuildRequires.
- Fix %%files (missing *ida* stuff).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Adrian Reber <adrian@lisas.de> - 2.07-3
- removed bitstream-vera dependency to fix (#473559)
  "Replace bitstream-vera dependencies with dejavu dependencies"
- changed BR libungif-devel to giflib-devel

* Fri Jul 04 2008 Adrian Reber <adrian@lisas.de> - 2.07-2
- applied patch from Ville Skyttä to fix
  "fbida: empty debuginfo package" (#453998)

* Mon Jun 09 2008 Adrian Reber <adrian@lisas.de> - 2.07-1
- updated to 2.07
- fixes "The fbi command aborts with a stack trace" (#448126)

* Fri Feb 15 2008 Adrian Reber <adrian@lisas.de> - 2.06-5
- rebuilt
- added patch to fix build failure on ppc/ppc64

* Sat Aug 25 2007 Adrian Reber <adrian@lisas.de> - 2.06-4
- rebuilt

* Tue Oct 31 2006 Adrian Reber <adrian@lisas.de> - 2.06-3
- rebuilt for new curl

* Fri Sep 29 2006 Adrian Reber <adrian@lisas.de> - 2.06-2
- obsoleted fbida-ida subpackage (#208457)

* Wed Aug 30 2006 Tom "spot" Callaway <tcallawa@redhat.com> - 2.06-1
- get rid of ida, we can't build a working version without openmotif

* Fri Jul 28 2006 Adrian Reber <adrian@lisas.de> - 2.05-1
- updated to 2.05
- dropped fbida.CVE-2006-1695.patch (now included)
- dropped fix for #200321 (included in new release)
- added two patches from debian to fix typos in manpages

* Thu Jul 27 2006 Adrian Reber <adrian@lisas.de> - 2.03-12
- security fix for #200321

* Mon Apr 24 2006 Adrian Reber <adrian@lisas.de> - 2.03-11
- security fix for #189721

* Mon Feb 13 2006 Adrian Reber <adrian@lisas.de> - 2.03-10
- rebuilt

* Wed Jan 18 2006 Adrian Reber <adrian@lisas.de> - 2.03-9
- this should finally work; also on x86_64

* Wed Jan 18 2006 Adrian Reber <adrian@lisas.de> - 2.03-8
- rebuilt

* Wed Jan 18 2006 Adrian Reber <adrian@lisas.de> - 2.03-7
- moved file Ida to %%{_datadir}/X11/app-defaults

* Thu Nov 24 2005 Adrian Reber <adrian@lisas.de> - 2.03-6
- updated for modular xorg-x11

* Tue May 10 2005 Adrian Reber <adrian@lisas.de> - 2.03-5
- fix debuginfo subpackage creation

* Mon Apr 04 2005 Adrian Reber <adrian@lisas.de> - 2.03-4
- rebuild for new libexif

* Mon Feb 21 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 2.03-3
- Fix typo; must be LIB=%%{_lib}; really fixes x86_64

* Sat Feb 12 2005 Thorsten Leemhuis <fedora at leemhuis dot info> - 2.03-2
- lib=%%{_lib} in make call; fixes x86_64

* Fri Feb 11 2005 Adrian Reber <adrian@lisas.de> - 2.03-1
- updated to 2.03
- created subpackages for ida and fbgs

* Sun Nov 28 2004 Adrian Reber <adrian@lisas.de> - 2.02-1
- updated to 2.02
- converted manpages to UTF-8

* Sun Nov 28 2004 Adrian Reber <adrian@lisas.de> - 2.01-1
- initial package
