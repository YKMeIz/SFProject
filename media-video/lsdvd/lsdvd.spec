Summary: Small application for listing the contents of DVDs
Name: lsdvd
Version: 0.16
Release: 18%{?dist}
License: GPLv2
Group: Applications/Multimedia
URL: http://untrepid.com/lsdvd/
Source: http://downloads.sf.net/lsdvd/lsdvd-%{version}.tar.gz
Patch0: lsdvd-0.16-strip-trailing-spaces.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: autoconf, automake
BuildRequires: libdvdread-devel

%description
lsdvd is a small application which lists the contents of DVDs to your terminal.


%prep
%setup -q
%patch0 -p1 -b .strip-trailing-spaces


%build
%configure --disable-dependency-tracking
%{__make} %{?_smp_mflags} CFLAGS="%{optflags}"


%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/lsdvd
%{_mandir}/man1/lsdvd.1*


%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 28 2010 Matthias Saou <http://freshrpms.net/> 0.16-13
- Include patch to fix trailing spaces stripping (#556416).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep  2 2008 Matthias Saou <http://freshrpms.net/> 0.16-10
- Update build patch for new s/dvdread/libdvdread/ include path.
- Actually, drop patch entirely as latest libdvdread changes the path back and
  seems to include a fix for the missing <inttypes.h> include.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Mon Nov 26 2007 Matthias Saou <http://freshrpms.net/> 0.16-6
- Rebuild against new libdvdread.

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 0.16-5
- Bump release to make our package newer than all known external ones.
- Add dist tag.
- Add --disable-dependency-tracking to %%configure.
- Simplify %%description to remove useless technical details.

* Mon May  8 2006 Matthias Saou <http://freshrpms.net/> 0.16-2
- Rebuild with latest tarball from sf.net, as apparently the original 0.16
  source was replaced after 3 days by a "fixed" source with the same file name.

* Wed Apr 19 2006 Matthias Saou <http://freshrpms.net/> 0.16-1
- Update to 0.16.
- Update URL.
- Update build patch, keep fixed libdvdread include detection.
- Include newly added man page.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 0.15-2
- Release bump to drop the disttag number in FC5 build.

* Mon Jan  9 2006 Matthias Saou <http://freshrpms.net/> 0.15-1
- Initial RPM release.

