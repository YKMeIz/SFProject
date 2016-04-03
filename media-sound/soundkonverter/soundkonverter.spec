# lib%%{name}core.so* is a private lib with no headers, so we should
# not provide that.
%global __provides_exclude ^lib%{name}.*\\.so.*$
%global __requires_exclude ^lib%{name}.*\\.so.*$

Name:		soundkonverter
Version:	2.1.1
Release:	3%{?dist}
Summary:	Audio file converter, CD ripper and Replay Gain tool

License:	GPLv2+
URL:		http://kde-apps.org/content/show.php?content=29024
Source0:	https://github.com/HessiJames/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Upstreamed, see: https://github.com/HessiJames/soundkonverter/pull/13
Patch0:		http://besser82.fedorapeople.org/patches/soundkonverter-2.1.1_fixes.patch

BuildRequires:	cdparanoia-devel
BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	kdelibs-devel
BuildRequires:	kdemultimedia-devel
BuildRequires:	qt4-devel
BuildRequires:	taglib-devel

Requires:	cdparanoia
Requires:	flac
Requires:	fluidsynth
Requires:	opus-tools
Requires:	speex
Requires:	sox
Requires:	timidity++
Requires:	vorbisgain
Requires:	vorbis-tools
Requires:	wavpack

%description
SoundKonverter is a front-end to various audio converters.

The key features are:
  * Audio conversion
  * Replay Gain calculation
  * CD ripping


%prep
%setup -q
%patch0 -p 1


%build
mkdir -p build
pushd build
%cmake_kde4 ../src
make %{?_smp_mflags}
popd


%install
pushd build
%make_install

# Remove the unneeded unversioned-so-symlink.
rm %{buildroot}%{_libdir}/lib%{name}*.so

# Validate the installed desktop-files.
for _file in `find %{buildroot}%{_datadir} -type f -name '%{name}*.desktop'`
do
  echo ${_file} | sed -e 's!^%{buildroot}!!g' >> %{name}.desktopfiles
  [[ `echo "${_file}" | grep -ve "/actions/" -ve "/servicetypes/"` ]] && \
    desktop-file-validate ${_file}
done

%find_lang %{name}
popd


%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f build/%{name}.desktopfiles -f build/%{name}.lang
%dir %{_kde4_appsdir}/solid/
%dir %{_kde4_appsdir}/solid/actions
%doc src/CHANGELOG src/COPYING src/README
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*.png
%{_kde4_appsdir}/%{name}
%{_libdir}/lib%{name}*.so.*
%{_libdir}/kde4/%{name}_*.so


%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Björn Esser <bjoern.esser@gmail.com> - 2.1.1-2
- use %%{_kde4_appsdir}-macro as suggested by Rex Dieter (#1114547)
  see: https://bugzilla.redhat.com/show_bug.cgi?id=1114547#c7

* Sun Jun 29 2014 Björn Esser <bjoern.esser@gmail.com> - 2.1.1-1
- initial rpm release (#1114547)
