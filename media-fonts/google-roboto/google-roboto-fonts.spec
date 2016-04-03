%global pkgname roboto
%global fontname google-roboto

Name: google-roboto-fonts
Version: 1.2
Release: 2%{?dist}
Summary: Google Roboto fonts

License: ASL 2.0
URL: https://www.google.com/fonts/specimen/Roboto
Source0: http://developer.android.com/downloads/design/%{pkgname}-%{version}.zip
Source1: 64-%{fontname}-condensed-fontconfig.conf
Source2: 64-%{fontname}-fontconfig.conf
BuildArch: noarch

BuildRequires: dos2unix
BuildRequires: fontpackages-devel

Requires: %{fontname}-common = %{version}-%{release}

%global archivename %{pkgname}-%{version}
%global fontsrcdir Roboto_v%{version}
%global fontconf 64-%{fontname}

%description
Roboto is a sans-serif typeface family introduced with Android Ice Cream
Sandwich operating system. Google describes the font as "modern, yet
approachable" and "emotional".

%package -n %{fontname}-condensed-fonts
Summary: Google Roboto condensed fonts
Requires: %{fontname}-common = %{version}-%{release}

%description -n %{fontname}-condensed-fonts
Google Roboto condensed fonts.

%package -n %{fontname}-common
Summary: Common files for Google Roboto fonts
Requires: fontpackages-filesystem

%description -n %{fontname}-common
Common files for Google Roboto fonts.

%prep
%autosetup -c -n %{name}-%{version}
dos2unix %{fontsrcdir}/*/LICENSE.txt

%build

%install
# install fonts
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p %{fontsrcdir}/Roboto/*.ttf %{buildroot}%{_fontdir}
install -m 0644 -p %{fontsrcdir}/RobotoCondensed/*.ttf %{buildroot}%{_fontdir}

# install fontconfig files
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -m 0644 -p %{SOURCE1} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}.conf
install -m 0644 -p %{SOURCE2} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-condensed.conf
for fconf in %{fontconf}.conf %{fontconf}-condensed.conf; do
  ln -s %{_fontconfig_templatedir}/$fconf %{buildroot}%{_fontconfig_confdir}/$fconf
done

%_font_pkg -f %{fontconf}.conf Roboto-*.ttf

%_font_pkg -n condensed -f %{fontconf}-condensed.conf RobotoCondensed-*.ttf

%files -n %{fontname}-common
%doc %{fontsrcdir}/Roboto/LICENSE.txt
%doc %{fontsrcdir}/RobotoSpecimenBook.pdf

%changelog
* Mon Apr 07 2014 David Tardon <dtardon@redhat.com> - 1.2-2
- integrate package review suggestions

* Thu Apr 03 2014 David Tardon <dtardon@redhat.com> - 1.2-1
- initial import
