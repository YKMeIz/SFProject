Name:		calf
Version:	0.0.19
Release:	6%{?dist}
Summary:	Audio plugins pack
Group:		Applications/Multimedia
# The jackhost code is GPLv2+ 
# The GUI code is LGPLv2+
# ladspa plugin is LGPLv2+
# lv2 plugin is GPLv2+ and LGPLv2+ and Public Domain
# dssi plugin is LGPLv2+
License:	GPLv2+ and LGPLv2+
URL:		http://calf.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}-dssi.desktop
# Add LADSPA / DSSI as dropped by upstream
# https://github.com/falkTX/calf.git calf-falktx
Patch0:		calf-falktx-96c9e772-add-LADSPA-DSSI.patch

BuildRequires:	desktop-file-utils
BuildRequires:	dssi-devel
BuildRequires:	expat-devel
BuildRequires:	glib2-devel
BuildRequires:	gtk2-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	ladspa-devel
BuildRequires:	lash-devel
BuildRequires:	libglade2-devel
BuildRequires:	lv2-devel
BuildRequires:  fluidsynth-devel
BuildRequires:  cairo-devel
BuildRequires:  libtool
BuildRequires:  fftw3-devel

%global common_desc \
The Calf project aims at providing a set of high quality open source audio\
plugins for musicians. All the included plugins are designed to be used with\
multitrack software, as software replacement for instruments and guitar stomp\
boxes.

%description
%common_desc

The plugins are available in LV2, DSSI, Standalone JACK and LADSPA formats.
This package contains the common files and the Standalone JACK plugin.

%package -n ladspa-%{name}-plugins
Summary:	Calf plugins in LADSPA format
Group:		Applications/Multimedia
License:	LGPLv2+
Requires:	%{name} = %{version}-%{release}
Requires:	ladspa

%description -n ladspa-%{name}-plugins
%common_desc

This package contains only LADSPA effect plugins (no GUI), with LRDF.

%package -n lv2-%{name}-plugins
Summary:	Calf plugins in LV2 format
Group:		Applications/Multimedia
License:	GPLv2+ and LGPLv2+ and Public Domain
Requires:	%{name} = %{version}-%{release}
Requires:	lv2core

%description -n lv2-%{name}-plugins
%common_desc

This package contains LV2 synthesizers and effects, MIDI I/O and GUI
extensions.

%package -n dssi-%{name}-plugins
Summary:	Calf plugins in DSSI format
Group:		Applications/Multimedia
License:	LGPLv2+
Requires:	%{name} = %{version}-%{release}
Requires:	dssi

%description -n dssi-%{name}-plugins
%common_desc

This package contains DSSI synthesizers and effects, also GUI extensions.

%prep
%setup -q
%patch0 -p1

%build
# Add GenericName to the .desktop file
echo "GenericName= Audio Effects" >> %{name}.desktop.in
./autogen.sh
# Make sure that optflags are not overriden.
sed -i 's|-O3||' configure

%configure \
	--with-ladspa-dir=%{_libdir}/ladspa/ \
	--with-dssi-dir=%{_libdir}/dssi/ \
	--with-lv2-dir=%{_libdir}/lv2 \
    --enable-ladspa 
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# The Jack host
desktop-file-install \
	--remove-category="Application" \
	--remove-key="Version" \
	--add-category="X-Synthesis" \
	--dir=$RPM_BUILD_ROOT%{_datadir}/applications \
	$RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop

# The DSSI host
ln -s jack-dssi-host $RPM_BUILD_ROOT%{_bindir}/%{name}
desktop-file-install \
	--dir=$RPM_BUILD_ROOT%{_datadir}/applications \
	%{SOURCE1}

# We don't need this file:
rm -f $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/icon-theme.cache

rm $RPM_BUILD_ROOT/%{_libdir}/%{name}/*.a*

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null
update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null
fi
update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc AUTHORS ChangeLog COPYING* README TODO
%{_bindir}/%{name}*
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}*
%{_mandir}/man7/%{name}*
%{_docdir}/%{name}

%files -n ladspa-%{name}-plugins
%{_libdir}/ladspa/%{name}.so
%{_datadir}/ladspa/rdf/%{name}.rdf

%files -n lv2-%{name}-plugins
%{_libdir}/lv2/%{name}.lv2/

%files -n dssi-%{name}-plugins
%{_bindir}/%{name}
%{_datadir}/applications/%{name}-dssi.desktop
%{_libdir}/dssi/%{name}/
%{_libdir}/dssi/%{name}.so

%changelog
* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat May 04 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.0.19-3
- Another missing BR fftw3-devel

* Fri May 03 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.0.19-2
- Add libtool

* Fri Dec 14 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.0.19.0-1
- New upstream release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.18.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.18.6-6
- Rebuilt for c++ ABI breakage

* Mon Jan 09 2012 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.0.18.6-5
- gcc-4.7 compile fix
- remove parts of the spec file that are no longer required by the guidelines

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.0.18.6-4
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.18.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.0.18.6-2
- Rebuilt for gcc bug 634757

* Sat Sep 11 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.0.18.6-1
- Update to 0.0.18.6
- Drop upstreamed patch

* Wed Jul 14 2010 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.0.18.5-4
- Fix ladspa_wrapper crash RHBZ#600713

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.18.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.0.18.5-2
- Add a .desktop file for the DSSI plugin
- Add X-Synthesis category to the existing .desktop file of the JACK plugin
- Backport the LADSPA URI fix from trunk

* Thu Jun 11 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.0.18.5-1
- Update to 0.0.18.5
- Drop upstreamed gcc44 patch

* Mon Mar 30 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 0.0.18.3-1
- Initial build
