%global _hardened_build 1

Name:          speech-dispatcher
Version:       0.8.3
Release:       4%{?dist}
Summary:       To provide a high-level device independent layer for speech synthesis
Group:         System Environment/Libraries

# Almost all files are under GPLv2+, however 
# src/c/clients/spdsend/spdsend.h is licensed under GPLv2,
# which makes %%_bindir/spdsend GPLv2.
License:       GPLv2+ and GPLv2
URL:           http://devel.freebsoft.org/speechd
Source0:       http://www.freebsoft.org/pub/projects/speechd/%{name}-%{version}.tar.gz
Source1:       http://www.freebsoft.org/pub/projects/sound-icons/sound-icons-0.1.tar.gz
Source2:       speech-dispatcherd.service

BuildRequires: alsa-lib-devel
BuildRequires: desktop-file-utils
BuildRequires: dotconf-devel
BuildRequires: espeak-devel
BuildRequires: flite-devel
Buildrequires: glib2-devel
Buildrequires: intltool
Buildrequires: libao-devel
Buildrequires: libtool-ltdl-devel
Buildrequires: libsndfile-devel
Buildrequires: pulseaudio-libs-devel
BuildRequires: python34-devel
BuildRequires: python34-setuptools
BuildRequires: texinfo
BuildRequires: systemd

%ifnarch s390 s390x
BuildRequires: libraw1394
%endif

Requires: speech-dispatcher-espeak
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
* Common interface to different TTS engines
* Handling concurrent synthesis requests – requests may come
  asynchronously from multiple sources within an application
  and/or from more different applications.
* Subsequent serialization, resolution of conflicts and
  priorities of incoming requests
* Context switching – state is maintained for each client
  connection independently, event for connections from
  within one application.
* High-level client interfaces for popular programming languages
* Common sound output handling – audio playback is handled by
  Speech Dispatcher rather than the TTS engine, since most engines
  have limited sound output capabilities.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{_isa} = %{version}-%{release}
License:        GPLv2+

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:        Documentation for speech-dispatcher
License:        GPLv2+
Group:          Documentation
Requires:       %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun):/sbin/install-info
BuildArch: noarch

%description doc
speechd documentation

%package utils
Summary:        Documentation for speech-dispatcher
License:        GPLv2+
Group:          Applications/System
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       python3-speechd = %{version}-%{release}

%description utils
Various utilities for speechd

%package espeak
Summary:        Speech Dispatcher espeak module
Requires:       %{name}%{_isa} = %{version}-%{release}
Obsoletes:      speech-dispatcher < 0.8.1-2

%description espeak
This package contains the espeak output module for Speech Dispatcher.

%package festival
Summary:        Speech Dispatcher festival module
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       festival-freebsoft-utils
Obsoletes:      speech-dispatcher < 0.8.1-2

%description festival
This package contains the festival output module for Speech Dispatcher.

%package flite
Summary:        Speech Dispatcher flite module
Requires:       %{name}%{_isa} = %{version}-%{release}
Obsoletes:      speech-dispatcher < 0.8.1-2

%description flite
This package contains the flite output module for Speech Dispatcher.

%package -n python3-speechd
Summary:        Python 3 Client API for speech-dispatcher
License:        GPLv2+
Group:          Development/Libraries
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       python3-pyxdg

%description -n python3-speechd
Python 3 module for speech-dispatcher

%prep
%setup -q

tar xf %{SOURCE1}

%build
%configure --disable-static \
	--with-alsa --with-pulse --with-libao \
	--without-oss --without-nas \
	--with-flite \
	--sysconfdir=%{_sysconfdir} --with-default-audio-method=pulse

make %{?_smp_mflags} V=1

%install
for dir in \
 config/ doc/ include/ src/audio/ src/api/ src/modules/ src/tests/ src/server/ src/clients/
 do
  pushd $dir
  make install DESTDIR=%{buildroot} INSTALL="install -p"
 popd
done

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %SOURCE2 %{buildroot}%{_unitdir}/

install -p -m 0644 sound-icons-0.1/* %{buildroot}%{_datadir}/sounds/%{name}/

#Remove %{_infodir}/dir file
rm -f %{buildroot}%{_infodir}/dir

find %{buildroot} -name '*.la' -delete

# Move the config files from /usr/share to /etc
mkdir -p %{buildroot}%{_sysconfdir}/speech-dispatcher/clients
mkdir -p %{buildroot}%{_sysconfdir}/speech-dispatcher/modules
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/speechd.conf %{buildroot}%{_sysconfdir}/speech-dispatcher/
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/clients/* %{buildroot}%{_sysconfdir}/speech-dispatcher/clients
mv %{buildroot}%{_datadir}/speech-dispatcher/conf/modules/* %{buildroot}%{_sysconfdir}/speech-dispatcher/modules

# Create log dir
mkdir -p -m 0700 %{buildroot}%{_localstatedir}/log/speech-dispatcher/

# Verify the desktop files
desktop-file-validate %{buildroot}/%{_datadir}/speech-dispatcher/conf/desktop/speechd.desktop

# enable pulseaudio as default with a fallback to alsa
sed 's/# AudioOutputMethod "pulse,alsa"/AudioOutputMethod "pulse,alsa"/' %{buildroot}%{_sysconfdir}/speech-dispatcher/speechd.conf

%post 
/sbin/ldconfig
%systemd_post speech-dispatcherd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart speech-dispatcherd.service

%preun
%systemd_preun speech-dispatcherd.service

%post doc
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/spd-say.info %{_infodir}/dir || :
/sbin/install-info %{_infodir}/ssip.info %{_infodir}/dir || :

%preun doc
if [ $1 = 0 ]; then
 /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
 /sbin/install-info --delete %{_infodir}/spd-say.info %{_infodir}/dir || :
 /sbin/install-info --delete %{_infodir}/ssip.info %{_infodir}/dir || :
fi

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README
%dir %{_sysconfdir}/speech-dispatcher/
%dir %{_sysconfdir}/speech-dispatcher/clients
%dir %{_sysconfdir}/speech-dispatcher/modules
%config(noreplace) %{_sysconfdir}/speech-dispatcher/speechd.conf
%config(noreplace) %{_sysconfdir}/speech-dispatcher/clients/*.conf
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/*.conf
%exclude %{_sysconfdir}/speech-dispatcher/modules/espeak*.conf
%exclude %{_sysconfdir}/speech-dispatcher/modules/festival.conf
%exclude %{_sysconfdir}/speech-dispatcher/modules/flite.conf
%{_bindir}/speech-dispatcher
%{_datadir}/speech-dispatcher/conf/desktop/speechd.desktop
%{_libdir}/libspeechd.so.2
%{_libdir}/libspeechd.so.2.6.0
%dir %{_libdir}/speech-dispatcher-modules/
%{_libdir}/speech-dispatcher-modules/sd_cicero
%{_libdir}/speech-dispatcher-modules/sd_dummy
%{_libdir}/speech-dispatcher-modules/sd_generic
%dir %{_libdir}/speech-dispatcher
%{_libdir}/speech-dispatcher/spd*.so
%{_datadir}/sounds/speech-dispatcher
%dir %attr(0700, root, root) %{_localstatedir}/log/speech-dispatcher/
%{_unitdir}/speech-dispatcherd.service

%files devel
%{_includedir}/*
%{_libdir}/lib*.so

%files doc
%{_infodir}/*

%files utils
%{_bindir}/spd-conf
%{_bindir}/spd-say
%{_bindir}/spdsend

%files espeak
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/espeak.conf
%{_libdir}/speech-dispatcher-modules/sd_espeak

%files festival
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/festival.conf
%{_libdir}/speech-dispatcher-modules/sd_festival

%files flite
%config(noreplace) %{_sysconfdir}/speech-dispatcher/modules/flite.conf
%{_libdir}/speech-dispatcher-modules/sd_flite

%files -n python3-speechd
%{python3_sitearch}/speechd*

%changelog
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.3-1
- 0.8.3

* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-5
- Add missing libsndfile dependency to fix sound icon support

* Tue Apr 14 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-4
- Always install the espeak plugin

* Fri Mar 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-3
- Fix noarch docs Requires

* Fri Mar 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-2
- Use %%license
- Make packaging more modular (rhbz #799140)

* Fri Mar 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.2-1
- 0.8.2

* Mon Sep 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.1-1
- 0.8.1
- Split utils into sub package

* Fri Aug 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.1-0.1rc1
- 0.8.1 rc1
- Enable hardened build

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 0.8-11
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Mar 27 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-7
- Rebuild

* Fri Nov  1 2013 Matthias Clasen <mclasen@redhat.com> 0.8-6
- Avoid a crash in the festival module (#995639)

* Tue Aug 13 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-5
- Install clients as not longer installed by default (fixes RHBZ 996337)

* Sat Aug 10 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8-4
- include/install missing headers

* Wed Aug  7 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-3
- Drop libao and python2 bindings

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.8-1
- Update to 0.8 stable release
- Rename python package for consistency
- Add python3 bindings - fixes RHBZ 867958
- Update the systemd scriptlets to the macroized versions

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 29 2012 Bastien Nocera <bnocera@redhat.com> 0.7.1-9
- Move RPM hacks to source patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
