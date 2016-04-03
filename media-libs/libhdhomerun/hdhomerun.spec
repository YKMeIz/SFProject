%global         releasedate 20130328
Name:           hdhomerun
Version:        0.0
Release:        0.21.%{releasedate}%{?dist}
Summary:        Silicon Dust HDHomeRun configuration utility

Group:          Applications/System
License:        LGPLv3 and GPLv3
URL:            http://www.silicondust.com/
Source0:        http://download.silicondust.com/hdhomerun/libhdhomerun_%{releasedate}.tgz
Source1:        http://download.silicondust.com/hdhomerun/hdhomerun_config_gui_%{releasedate}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gtk2-devel
Requires:       gtk2

%description
The configuration and firmware upgrade utility for Silicon Dust's
networked HDTV dual-tuner HDHomeRun device.

%description
The configuration and firmware upgrade utility for Silicon Dust's
networked HDTV dual-tuner HDHomeRun device.

%package devel
Summary: Developer tools for the hdhomerun library
Group: Development
Requires: hdhomerun = %{version}-%{release}

%description devel
The hdhumerun-devel package provides developer tools for the hdhomerun library.

%prep
%setup -q -c -a 1
# Fix up linefeeds, drop execute bit and don't strip binaries
%{__sed} -i 's/\r//' libhdhomerun/*
%{__chmod} -x libhdhomerun/*
%{__sed} -i -e '/$(STRIP).*/d' -e 's/C\(PP\)\?FLAGS .=/C\1FLAGS ?=/' libhdhomerun/Makefile

# Convert files to utf8
for f in libhdhomerun/*; do
  /usr/bin/iconv -f iso-8859-1 -t utf-8 --output $f.new $f && mv $f.new $f
done

%build
cd hdhomerun_config_gui
%configure
make 
cd ..
cat << __EOF__ > README.firmware
The HDHomeRun Firmwares are not redistributable, but the latest versions of
both the US ATSC and European DVB-T firmwares can always be obtained from
the Silicon Dust web site:

http://www.silicondust.com/downloads/linux

__EOF__

%install
rm -rf $RPM_BUILD_ROOT
make -C hdhomerun_config_gui install DESTDIR=$RPM_BUILD_ROOT
install -m0755 libhdhomerun/hdhomerun_config $RPM_BUILD_ROOT%{_bindir}/
mkdir include
cp -a libhdhomerun/*.h include
sed -r 's|(^#include +["])(.*)(["] *$)|#include <hdhomerun/\2>|' \
    libhdhomerun/hdhomerun.h > include/hdhomerun.h
mkdir -p $RPM_BUILD_ROOT%{_includedir}/hdhomerun
install -m0755 include/*.h $RPM_BUILD_ROOT%{_includedir}/hdhomerun/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc libhdhomerun/lgpl.txt libhdhomerun/README hdhomerun_config_gui/COPYING README.firmware
# lib and cli are LGPLv3
%{_libdir}/libhdhomerun.so
%{_bindir}/hdhomerun_config
# gui is GPLv3
%{_bindir}/hdhomerun_config_gui

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/hdhomerun
%{_includedir}/hdhomerun/*.h

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.21.20130328
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 07 2013 Paul Wouters <pwouters@redhat.com> - 0.0-0.20.20130328
- Update to 20130328 (rhbz#964210)
- Removed DESTDIR patch, got merged in at upstream

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.19.20120405
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Sep 27 2012 Jeffrey Ollie <jeff@ocjtech.us> - 0.0-0.18.20120405
- Update to 20120405

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.17.20100213
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.16.20100213
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.0-0.15.20100213
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.14.20100213
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Mar 09 2010 Jarod Wilson <jarod@redhat.com> - 0.0-0.13.20100213
- Update to 20100213 release
- Add a devel sub-package so other software can be built against
  the system libhdhomerun (Rolf Fokkens, fixes rhbz#571139)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.12.20090415
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Jarod Wilson <jarod@redhat.com> 0.0-0.11.20090415
- Add README.firmware, pointing folks to firmware downloads

* Tue Jun 23 2009 Jarod Wilson <jarod@redhat.com> 0.0-0.10.20090415
- Update to 20090415 release
- Add new GTK2 config GUI

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0-0.9.20081002
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 20 2008 Jarod Wilson <jarod@redhat.com> 0.0-0.8.20081002
- Update to 20081002 release

* Tue Aug 19 2008 Jarod Wilson <jarod@redhat.com> 0.0-0.7.20080727
- Update to 20080727 release

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> 0.0-0.6.20080212
- Update to 20080212 release

* Fri Oct 19 2007 Jarod Wilson <jwilson@redhat.com> - 0.0-0.5.20071015
- Update to 20071015 release
- Update license field

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.0-0.4.20070716
- Rebuild for selinux ppc32 issue.

* Tue Jul 17 2007 Jarod Wilson <jwilson@redhat.com> 0.0-0.3.20070716
- Update to 20070716 release

* Thu Jul 12 2007 Jarod Wilson <jwilson@redhat.com> 0.0-0.2.20070616
- Use sed instead of perl, drop perl BR: (jeff@ocjtech.us)
- Convert source files to utf8 (jeff@ocjtech.us)

* Mon Jun 18 2007 Jarod Wilson <jwilson@redhat.com> 0.0-0.1.20070616
- Update to 20070616 release
- Don't install any of the header files and drop lib from the package
  name, since this really isn't a library

* Fri May 18 2007 Jarod Wilson <jwilson@redhat.com> 0.0-0.1.20070512
- Initial packaging for Fedora
