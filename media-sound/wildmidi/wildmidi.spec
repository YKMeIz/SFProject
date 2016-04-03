Name:           wildmidi
Version:        0.3.7
Release:        2%{?dist}
Summary:        Softsynth midi player
Group:          Applications/Multimedia
License:        GPLv3+
URL:            http://www.mindwerks.net/projects/wildmidi
Source0:        https://github.com/Mindwerks/%{name}/archive/%{name}-%{version}.tar.gz
BuildRequires:  alsa-lib-devel cmake
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
WildMidi is a software midi player which has a core softsynth library that can
be used with other applications.


%package libs
Summary:        WildMidi Midi Wavetable Synth Lib
Group:          System Environment/Libraries
License:        LGPLv3+
Requires:       timidity++-patches

%description libs
This package contains the WildMidi core softsynth library. The library is
designed to process a midi file and stream out the stereo audio data
through a buffer which an external program can then process further.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
License:        LGPLv3+
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{name}-%{version}


%build
%cmake
make %{?_smp_mflags}


%install
%make_install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -s ../timidity.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.cfg


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%doc docs/license/GPLv3.txt
%{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/*

%files libs
%doc docs/license/LGPLv3.txt
%{_libdir}/libWildMidi.so.1*
%{_mandir}/man5/*

%files devel
%{_includedir}/*
%{_libdir}/libWildMidi.so
%{_mandir}/man3/*


%changelog
* Fri Jun  6 2014 Hans de Goede <hdegoede@redhat.com> - 0.3.7-2
- Upstream has respun the tarbal, update to the new tarbal

* Fri May 30 2014 Hans de Goede <hdegoede@redhat.com> - 0.3.7-1
- New upstream release 0.3.7 (rhbz#1078135)

* Sun Apr  6 2014 Hans de Goede <hdegoede@redhat.com> 0.3.6-1
- New upstream release 0.3.6 (rhbz#1078135)

* Thu Mar 20 2014 Hans de Goede <hdegoede@redhat.com> 0.3.5-1
- New upstream release 0.3.5 (rhbz#1078135)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.2.3.4-2
- Rebuilt for gcc bug 634757

* Sun Sep 12 2010 Hans de Goede <hdegoede@redhat.com> 0.2.3.4-1
- New upstream release 0.2.3.4-1

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-6
- Fixup Summary

* Mon Jul  7 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-5
- Fix wildmidi cmdline player sound output on bigendian archs (bz 454198),
  patch by Ian Chapman

* Sat Feb  9 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-4
- Change alsa output code to use regular write mode instead of mmap to make
  it work with pulseaudio (bz 431846)

* Sun Oct 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-3
- Require timidity++-patches instead of timidity++ itself so that we don't
  drag in arts and through arts, qt and boost.

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-2
- Put the lib in a seperate -libs subpackage
- Update License tags for new Licensing Guidelines compliance

* Sat Jul 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-1
- Initial Fedora Extras version
