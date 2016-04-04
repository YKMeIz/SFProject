Summary: Utilities for configuring most popular joysticks.
Name: joystick
Version: 1.2.15
Release: 30%{?dist}
License: GPLv2+
Group: System Environment/Base
ExcludeArch: s390 s390x
Source: ftp://atrey.karlin.mff.cuni.cz/pub/linux/joystick/%{name}-%{version}.tar.gz
Patch0: joystick-1.2.15-redhat.patch
Patch1: joystick-1.2.15-newkernel.patch
URL: http://atrey.karlin.mff.cuni.cz/~vojtech/joystick/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description 
The Linux Joystick Driver provides support for a variety of joysticks
and similar devices. This package includes several utilities for
setting up, calibrating, and testing your joystick.

%prep
%setup -q
%patch0 -p1 -b .redhat
%patch1 -p1 -b .24kernel

%build
rm -f joystick.h

make compile-programs

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}
make BINDIR=%{_bindir} MANDIR=%{_mandir} install-programs

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING ChangeLog TODO joystick.txt
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.2.15-25
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.15-22
- fix license tag

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 1.2.15-21
- rebuilt against gcc 4.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.15-20.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.15-20.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.15-20.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 1.2.15-20
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 1.2.15-19
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.2.15-14
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 1.2.15-11
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Aug 24 2001 Preston Brown <pbrown@redhat.com>
- rebuild because version of joystick driver in the kernel is newer

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add ExcludeArch: s390 s390x

* Fri Mar  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- New URL and location
- fix docs
- Patch it to use the 2.4 input headers, so it works again

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- add %%defattr

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Thu Jan 13 2000 Preston Brown <pbrown@redhat.com>
- initial RPM.
