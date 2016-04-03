%define shortname ssr
Name:           simplescreenrecorder
Version:        0.3.3
Release:        1%{?dist}
Summary:        SimpleScreenRecorder is a screen recorder for Linux

License:        GPLv3
URL:            http://www.maartenbaert.be/simplescreenrecorder/
Source0:        https://github.com/MaartenBaert/ssr/archive/%{version}.tar.gz
Patch0:         fix_ldpath.patch

BuildRequires:  desktop-file-utils
BuildRequires:  ffmpeg-devel
BuildRequires:  qt4-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libX11-devel
BuildRequires:  libXfixes-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
SimpleScreenRecorder is a screen recorder for Linux.
Despite the name, this program is actually quite complex.
It's 'simple' in the sense that it's easier to use than ffmpeg/avconv or VLC

%package libs
Summary: SimpleScreenRecorder opengl injection library

%description libs
SimpleScreenRecorder is a screen recorder for Linux.
Despite the name, this program is actually quite complex.
It's 'simple' in the sense that it's easier to use than ffmpeg/avconv or VLC
This is a package for opengl capture

%prep
%setup -q -n %{shortname}-%{version}
%patch0 -p1 -b .ldpath


%build
export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L libavformat libavcodec libavutil libswscale`"
export CPPFLAGS="$CPPFLAGS `pkg-config --cflags-only-I libavformat libavcodec libavutil libswscale`"
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
%make_install
rm -f %{buildroot}%{_libdir}/*.la
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
mkdir -p %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/lib%{shortname}-glinject.so %{buildroot}%{_libdir}/%{name}/lib%{shortname}-glinject.so

%files
%doc COPYING README.md AUTHORS.md CHANGELOG.md notes.txt todo.txt
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_bindir}/%{shortname}-glinject

%files libs
%doc COPYING README.md AUTHORS.md CHANGELOG.md notes.txt todo.txt
%{_libdir}/%{name}/lib%{shortname}-glinject.so

%changelog
* Mon Mar 23 2015 Ivan Epifanov <isage.dna@gmail.com> - 0.3.3-1.R
- Update to 0.3.3

* Tue Dec 16 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.1-1.R
- Update to 0.3.1

* Thu Jul  3 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.0-2.R
- Move gl-inject library to subdir

* Thu Jul  3 2014 Ivan Epifanov <isage.dna@gmail.com> - 0.3.0-1.R
- Initial spec for fedora
