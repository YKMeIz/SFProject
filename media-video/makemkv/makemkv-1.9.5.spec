# These files are binaries without symbols:
#
# makemkv-bin-%{version}/bin/amd64/makemkvcon
# makemkv-bin-%{version}/bin/i386/makemkvcon
# makemkv-bin-%{version}/bin/i386/mmdtsdec

# This is a binary image inserted in the compiled GUI binary:
# makemkv-oss-%{version}/makemkvgui/bin/image_data.bin

Summary:        DVD and Blu-ray to MKV converter and network streamer
Name:           makemkv
Version:        1.9.5
Release:        1%{?dist}
License:        GuinpinSoft inc and Mozilla Public License Version 1.1 and LGPLv2.1+
URL:            http://www.%{name}.com/
Packager:	Andrew Schott <andrew@schotty.com>
ExclusiveArch:  %{ix86} x86_64

Source0:        http://www.%{name}.com/download/%{name}-oss-%{version}.tar.gz
Source1:        http://www.%{name}.com/download/%{name}-bin-%{version}.tar.gz
Source2:        %{name}-changelog.txt
#Patch0:         %{name}-oss-%{version}-no-strip.patch

BuildRequires:  desktop-file-utils
BuildRequires:  expat-devel
BuildRequires:	openssl-devel
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:	qt4-devel

Requires:       hicolor-icon-theme

%description
MakeMKV is your one-click solution to convert video that you own into free and
patents-unencumbered format that can be played everywhere. MakeMKV is a format
converter, otherwise called "transcoder".It converts the video clips from
proprietary (and usually encrypted) disc into a set of MKV files, preserving
most information but not changing it in any way. The MKV format can store
multiple video/audio tracks with all meta-information and preserve chapters.

Additionally MakeMKV can instantly stream decrypted video without intermediate
conversion to wide range of players, so you may watch Blu-ray and DVD discs with
your favorite player on your favorite OS or on your favorite device.

%prep
%setup -q -T -c -n %{name}-%{version} -b 0 -b 1
#%patch0
cp %{SOURCE2} .

%build
# Accept eula  
mkdir -p %{name}-bin-%{version}/tmp
echo "accepted" > %{name}-bin-%{version}/tmp/eula_accepted
cd %{name}-oss-%{version}
%configure
make %{?_smp_mflags}

%install
make -C %{name}-oss-%{version} install DESTDIR=%{buildroot} LIBDIR=%{_libdir}
make -C %{name}-bin-%{version} install DESTDIR=%{buildroot} LIBDIR=%{_libdir}
chmod 755 %{buildroot}%{_libdir}/lib*.so*
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# Starting with version 1.8.5, MakeMKV comes with libmmbd library.
# This library also emulates libaacs/libbdplus libraries
# below are instructions how to setup libmmbd for libaacs/libbdplus emulation.
# Once done, any libbluray-based application, including VLC player, will be able to open protected blu-ray discs.

ln -s %{_libdir}/libmmbd.so.0  $RPM_BUILD_ROOT%{_libdir}/libaacs.so.0
ln -s %{_libdir}/libmmbd.so.0  $RPM_BUILD_ROOT%{_libdir}/libbdplus.so.0

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/sbin/ldconfig

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/sbin/ldconfig

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc %{name}-bin-%{version}/src/eula_en_linux.txt
%doc %{name}-oss-%{version}/License.txt
%doc %{name}-changelog.txt
%{_bindir}/makemkv
%{_bindir}/makemkvcon
# mmdtsdec should be splitted in its own ix86 subpackage:
%{_bindir}/mmdtsdec
%{_datadir}/MakeMKV
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_libdir}/libdriveio.so.0
%{_libdir}/libmakemkv.so.1
%{_libdir}/libmmbd.so.0
%{_libdir}/libaacs.so.0
%{_libdir}/libbdplus.so.0

%changelog
* Sat Aug 22 2015 Andrew Schott <andrew@schotty.com> 1.9.5-1
- Updated to 1.9.5

* Fri Sep 26 2014 Andrew Schott <andrew@schotty.com> 1.8.13-1
- Updated to 1.8.13
- Commented out patch lines

* Fri Feb 28 2014 Simone Caronni <negativo17@gmail.com> - 1.8.10-1
- Updated to 1.8.10.

* Fri Feb 28 2014 Simone Caronni <negativo17@gmail.com> - 1.8.9-1
- Updated to 1.8.9.
- Simplify configure line (now uses pkg-config).

* Thu Feb 06 2014 Simone Caronni <negativo17@gmail.com> - 1.8.8-2
- Actually package changelog.

* Wed Feb 05 2014 Simone Caronni <negativo17@gmail.com> - 1.8.8-1
- Update to 1.8.8.
- Added changelog.

* Mon Dec 30 2013 Simone Caronni <negativo17@gmail.com> - 1.8.7-2
- Add workaround for OpenSSL package not supplying required EC curves:
  https://bugzilla.redhat.com/show_bug.cgi?id=1042715#c7
  http://www.makemkv.com/forum2/viewtopic.php?f=3&t=7370&start=15#p31142

* Fri Dec 13 2013 Simone Caronni <negativo17@gmail.com> - 1.8.7-1
- Update to 1.8.7.
- Add debug package and compiler options.

* Thu Sep 19 2013 Simone Caronni <negativo17@gmail.com> - 1.8.5-1
- Update to 1.8.5.

* Mon Jul 22 2013 Simone Caronni <negativo17@gmail.com> - 1.8.4-2
- Update to 1.8.4.
- Removed EPEL 5 support, QT too old.

* Thu May 30 2013 Simone Caronni <negativo17@gmail.com> - 1.8.3-1
- Updated to 1.8.3.

* Tue May 21 2013 Simone Caronni <negativo17@gmail.com> - 1.8.2-1
- Update to 1.8.2.

* Wed May 01 2013 Simone Caronni <negativo17@gmail.com> - 1.8.2-2
- Check desktop file during %%install.

* Wed May 01 2013 Simone Caronni <negativo17@gmail.com> - 1.8.2-1
- First build.
