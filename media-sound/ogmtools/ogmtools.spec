Name:           ogmtools
Version:        1.5
Release:        14%{?dist}
Summary:        Tools for Ogg media streams

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://www.bunkus.org/videotools/ogmtools/
Source0:        http://www.bunkus.org/videotools/ogmtools/ogmtools-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libdvdread-devel

Patch0:         ogmtools-1.5-optflags.patch

%description
These tools allow information about (ogminfo) or extraction from (ogmdemux) or
creation of (ogmmerge) OGG media streams. Note that OGM is used for "OGG media
streams".


%prep
%setup -q
%patch0 -p1
# Convert Changelog to UTF8
iconv -f iso8859-1 -t utf8 ChangeLog -o ChangeLog.txt
touch -r ChangeLog ChangeLog.txt
mv ChangeLog.txt ChangeLog


%build
%configure --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc ChangeLog COPYING README TODO
%{_bindir}/*
%{_mandir}/man1/*


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 20 2009 Gianluca Sforna <giallu gmail com> - 1.5-6
- honour RPM_OPT_FLAGS
- use --disable-dependency-tracking

* Thu Apr  9 2009 Gianluca Sforna <giallu gmail com> - 1.5-5
- Fix rpmlint issues
- Fix license tag

* Thu Dec 16 2008 Gianluca Sforna <giallu gmail com> - 1.5-4
- New spec based off freshrpms for Fedora submission
