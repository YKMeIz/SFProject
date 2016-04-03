Name:           vorbisgain
Version:        0.36
Release:        10%{?dist}
Summary:        Adds tags to Ogg Vorbis files to adjust the volume

Group:          Applications/Multimedia
License:        LGPLv2
URL:            http://sjeng.org/vorbisgain.html
Source0:	http://sjeng.org/ftp/vorbis/%{name}-%{version}.zip
Patch0:		%{name}-spelling.patch

BuildRequires:	libvorbis-devel
BuildRequires:	libogg-devel


%description
VorbisGain is a utility that uses a psychoacoustic method to correct the
volume of an Ogg Vorbis file to a predefined standardized loudness.

It needs player support to work. Non-supporting players will play back
the files without problems, but you'll miss out on the benefits.
Nowadays most good players such as ogg123, xmms and mplayer are already
compatible. 


%prep
%setup -q
%patch0 -p1 -b .spelling


%build
chmod 755 configure
%configure --enable-recursive
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc NEWS README
%{_bindir}/%{name}
%{_mandir}/man1/*


%changelog
* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 09 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.36-8
- Rebuild for new gcc.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Brian Pepple <bpepple@fedoraproject.org> - 0.36-6
- Drop buildroot & clean section since they are no longer necessary.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.36-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  8 2008 Brian Pepple <bpepple@fedoraproject.org> - 0.36-3
- Rebuild for gcc-4.3.

* Tue Aug 21 2007 Brian Pepple <bpepple@fedoraproject.org> - 0.36-2
- Rebuild.
- Update license tag.

* Fri Oct 13 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.36-1
- Update to 0.36.
- Add patch to fix spelling errors in manpage.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.34-3
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Brian Pepple <bpepple@fedoraproject.org> - 0.34-2
- Rebuild for FC6.
- Minor formatting changes.

* Sat May 13 2006 Noa Resare <noa@resare.com> 0.34-1
- Initial spec
