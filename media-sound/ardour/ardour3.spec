# gcc 4.8 doesn't seem to like bluetooth headers with strict
%bcond_with strict

# the test scripts seem to be broken
%bcond_with tests

%global man_langs_encodings :UTF-8 es:UTF-8 fr:ISO-8859-1 ru:KOI8-R

# Don't generate provides for internal shared objects and plugins
%global internal_libs_re (ardour.*|audiographer|evoral|gtkmm2ext|jack_audiobackend|midipp|pan[12]in2out|panvbap|panbalance|pbd|qmdsp|smf|timecode)
%global __provides_exclude_from ^%{_libdir}/(ardour3|lv2)/.*$
%global __requires_exclude ^lib%{internal_libs_re}\.so.*$

# This package is named ardour3 to allow parallel installation with ardour
# (version 2) for sessions created with ardour-2.x.
Name:       ardour3
Version:    3.5.403

Release:    1%{?dist}
Summary:    Digital Audio Workstation

Group:      Applications/Multimedia
License:    GPLv2+
URL:        http://ardour.org
# Not available via direct download. Download via
# http://ardour.org/download.html
Source0:    Ardour3-%{version}.tar.bz2
# BSD 2/3-clause licenses used in some code files
Source1:    LICENSING

BuildRequires:  alsa-lib-devel
BuildRequires:  aubio-devel >= 0.3.2
BuildRequires:  bluez-libs-devel
BuildRequires:  boost-devel >= 1.39
BuildRequires:  cppunit-devel >= 1.12.0
BuildRequires:  cwiid-devel >= 0.6.00
BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  fftw-devel
BuildRequires:  flac-devel >= 1.2.1
BuildRequires:  fontconfig
BuildRequires:  gettext
BuildRequires:  glib2-devel >= 2.14.0
BuildRequires:  glibmm24-devel >= 2.32.0
BuildRequires:  graphviz
BuildRequires:  gtk2-devel >= 2.18
BuildRequires:  gtkmm24-devel >= 2.18
BuildRequires:  jack-audio-connection-kit-devel >= 0.118.2
BuildRequires:  kernel-headers
BuildRequires:  libcurl-devel >= 7.0.0
BuildRequires:  libgnomecanvas-devel >= 2.30
BuildRequires:  libgnomecanvasmm26-devel >= 2.16
BuildRequires:  liblo-devel >= 0.24
BuildRequires:  liblrdf-devel >= 0.4.0
BuildRequires:  libltc-devel >= 1.1.1
BuildRequires:  libogg-devel >= 1.1.2
BuildRequires:  libsamplerate-devel >= 0.1.7
BuildRequires:  libsigc++20-devel >= 2.0
BuildRequires:  libsndfile-devel >= 1.0.18
BuildRequires:  libuuid-devel
BuildRequires:  libX11-devel >= 1.1
BuildRequires:  libxml2-devel
BuildRequires:  lilv-devel >= 0.14.0
BuildRequires:  lv2-devel >= 1.0.0
BuildRequires:  python
BuildRequires:  rubberband-devel >= 1.0
BuildRequires:  serd-devel >= 0.14.0
BuildRequires:  sord-devel >= 0.8.0
BuildRequires:  sratom-devel >= 0.2.0
BuildRequires:  suil-devel >= 0.6.0
BuildRequires:  taglib-devel >= 1.4
BuildRequires:  vamp-plugin-sdk-devel

Requires:       google-droid-sans-mono-fonts

%description
Ardour is a multi-channel digital audio workstation, allowing users to record,
edit, mix and master audio and MIDI projects. It is targeted at audio
engineers, musicians, soundtrack editors and composers.

%prep
%setup -q -n Ardour3-%{version}

# use ardour3 name for all and reencode some man pages
for lang_enc in %{man_langs_encodings}; do
    lang="${lang_enc%%:*}"
    enc="${lang_enc#*:}"
    if [ -n "$lang" ]; then
        lang=".${lang}"
    fi
    fromfile="ardour.1${lang}"
    tofile="ardour3.1${lang}"
    iconv -f "$enc" -t UTF-8 "$fromfile" > "$tofile"
    touch -r "$fromfile" "$tofile"
done

cp %{SOURCE1} .

%build
export LC_ALL=en_US.UTF-8
./waf configure \
%if %{with strict}
    --strict \
%endif
%if %{with tests}
    --test \
%endif
    --prefix="%_prefix" \
    --bindir="%_bindir" \
    --configdir="%_sysconfdir" \
    --datadir="%_datadir" \
    --includedir="%_includedir" \
    --libdir="%_libdir" \
    --mandir="%_mandir" \
    --docdir="%_docdir" \
    --docs \
    --freedesktop \
    --lv2 \
    --lv2-system \
    --lxvst \
    --nls \
    --noconfirm \
    --no-phone-home \
    --optimize \
%ifarch %ix86 x86_64
    --arch="%optflags -msse -mfpmath=sse -DUSE_XMMINTRIN" \
%else
    --arch="%optflags" \
%endif
    --use-external-libs

./waf build -v %{?_smp_mflags}
./waf i18n -v %{?_smp_mflags}

cp gtk2_ardour/ardour3.desktop{.in,}

%install
./waf --destdir=%{buildroot} install -v

# ArdourMono.ttf is really Droid Sans Mono
ln -snf ../fonts/google-droid/DroidSansMono.ttf %{buildroot}%{_datadir}/ardour3/ArdourMono.ttf

# install man pages
install -d -m755 %{buildroot}%{_mandir}/man1
for lang_enc in %man_langs_encodings; do
    lang="${lang_enc%%:*}"
    if [ -n "$lang" ]; then 
        _lang=".${lang}"
    else
        _lang=""
    fi
    fromfile="ardour3.1${_lang}"
    todir="%{buildroot}%{_mandir}/${lang}/man1"
    tofile="${todir}/ardour3.1"
    install -d -m755 "$todir"
    install -p -m644 "$fromfile" "$tofile"
done

# install icons to freedesktop locations
for s in 16 22 32 48 ; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
    cp -p %{buildroot}%{_datadir}/ardour3/icons/ardour_icon_${s}px.png \
       %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/ardour3.png
done

# tweak and install desktop file
mkdir -p %{buildroot}%{_datadir}/applications/
desktop-file-install --dir %{buildroot}%{_datadir}/applications \
    --set-key=Name --set-value="Ardour %{version}" \
    --set-generic-name="Digital Audio Workstation" \
    --set-key=X-GNOME-FullName \
    --set-value="Ardour v%{version} (Digital Audio Workstation)" \
    --set-comment="Record, mix and master audio" \
    --remove-category=AudioEditing \
    --add-category=X-AudioEditing \
    gtk2_ardour/ardour3.desktop

# install mime entry
mkdir -p %{buildroot}%{_datadir}/mime/packages/
install -p -m 0644 gtk2_ardour/ardour3.xml %{buildroot}%{_datadir}/mime/packages/

%find_lang ardour3
%find_lang gtk2_ardour3
%find_lang gtkmm2ext3

%if %{with tests}
%check
WAFTPATH="$PWD/doc/waft"
pushd libs/ardour
sh "$WAFTPATH" --targets=libardour-tests && ./run-tests.sh
popd
%endif

rm -f %{buildroot}%{_bindir}/run-tests

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
/bin/touch --no-create %{_datadir}/mime/packages &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /bin/touch --no-create %{_datadir}/mime/packages &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files -f ardour3.lang -f gtk2_ardour3.lang -f gtkmm2ext3.lang
%doc COPYING LICENSING
%{_bindir}/ardour3
%config(noreplace) %{_sysconfdir}/ardour3
%{_libdir}/ardour3
%{_datadir}/ardour3
%{_datadir}/icons/hicolor/*/apps/ardour3.png
%{_datadir}/applications/ardour3.desktop
%{_datadir}/mime/packages/ardour3.xml
%{_mandir}/man1/ardour3.1*
%{_mandir}/*/man1/ardour3.1*
# The lv2 package isn't needed for ardour to function, just the directory and
# the shipped plugin
%{_libdir}/lv2

%changelog
* Sun Oct 05 2014 Nils Philippsen <nils@redhat.com> - 3.5.403-1
- version 3.5.403

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.380-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 08 2014 Rex Dieter <rdieter@fedoraproject.org> 3.5.380-3
- optimize mimeinfo scriptlet

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.380-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 3.5.380-2
- Rebuild for boost 1.55.0

* Wed May 14 2014 Nils Philippsen <nils@redhat.com> - 3.5.380-1
- version 3.5.380

* Tue Feb 25 2014 Nils Philippsen <nils@redhat.com> - 3.5.357-1
- version 3.5.357

* Sat Jan 25 2014 Nils Philippsen <nils@redhat.com> - 3.5.308-2
- filter out new dependency on internal libpanbalance

* Fri Jan 24 2014 Nils Philippsen <nils@redhat.com> - 3.5.308-1
- version 3.5.308

* Mon Dec 23 2013 Nils Philippsen <nils@redhat.com> - 3.5.143-1
- version 3.5.143

* Wed Nov 06 2013 Nils Philippsen <nils@redhat.com> - 3.5.74-2
- use recreated official tarball without binaries

* Wed Nov 06 2013 Nils Philippsen <nils@redhat.com> - 3.5.74-1
- version 3.5.74

* Mon Nov 04 2013 Nils Philippsen <nils@redhat.com> - 3.5.14-1
- rename patch files to ardour3-*.patch
- re-add SSE flags on ix86, x86_64

* Sat Nov 02 2013 Nils Philippsen <nils@redhat.com> - 3.5.14-1
- filter out requires satisfied by internal libraries

* Wed Oct 30 2013 Nils Philippsen <nils@redhat.com> - 3.5.14-1
- include BSD 2/3 clause license texts
- filter out provides of plug-ins and internal shared objects

* Mon Oct 28 2013 Nils Philippsen <nils@redhat.com> - 3.5.14-1
- version 3.5.14
- drop obsolete arm patch
- unbundle some libraries
- set optimization flags hard

* Tue Sep 24 2013 Nils Philippsen <nils@redhat.com> - 3.4-1
- use RPM %%optflags for building (Orcan Ogetbil)

* Thu Sep 12 2013 Nils Philippsen <nils@redhat.com> - 3.4-1
- add missing/correct wrong build dependencies: alsa-lib-devel, graphviz,
  libuuid-devel
- fix building on ARM

* Wed Sep 11 2013 Nils Philippsen <nils@redhat.com> - 3.4-1
- use separately packaged Droid Sans Mono font instead of ArdourMono (embedded
  copy)
- tweak and install desktop file
- copy desktop-relevant scriptlets from Fedora Wiki
- merge ardour v2 spec file:
  - install icons (Hans de Goede)
  - rename, reencode and install man pages (Hans de Goede)
  - install mime entry (Orcan Ogetbil)

* Tue Sep 10 2013 Nils Philippsen <nils@redhat.com> - 3.4-1
- version 3.4
- don't use --strict by default because (at least) gcc 4.8 doesn't like
  bluetooth headers with it
- set LC_ALL=en_US.UTF-8 to prevent "./waf configure" from tripping over
  non-ASCII characters
- don't run tests as the test scripts seem to be broken

* Mon Sep 09 2013 Nils Philippsen <nils@redhat.com> - 3.0-1
- fix %%check to work as documented

* Mon Mar 18 2013 Nils Philippsen <nils@redhat.com> - 3.0-1
- version 3.0, initial version
