%global fontname    courier-prime

Name:    %{fontname}-ib-fonts
Version: 1.203
Release: 2%{?dist}
Summary: Courier Prime fonts

Group:     User Interface/X
License:   OFL
URL:       http://quoteunquoteapps.com/courierprime/
Source0:   http://quoteunquoteapps.com/downloads/courier-prime.zip
Source1:   45-courier-prime.conf
Source2:   90-tt-courier-prime.conf

BuildArch:      noarch
BuildRequires:  fontpackages-devel
Requires:       fontpackages-filesystem

%description
Courier Prime fonts for Infinality.

%_font_pkg -f *-%{fontname}.conf *.ttf

%prep
%setup -q -n "Courier Prime"

%build

%install
rm -fr %{buildroot}

install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} %{buildroot}%{_fontconfig_templatedir}
install -m 0644 -p %{SOURCE2} %{buildroot}%{_fontconfig_templatedir}
ln -s %{_fontconfig_templatedir}/45-courier-prime.conf %{buildroot}%{_fontconfig_confdir}/45-courier-prime.conf
ln -s %{_fontconfig_templatedir}/90-tt-courier-prime.conf %{buildroot}%{_fontconfig_confdir}/90-tt-courier-prime.conf

%clean
rm -fr %{buildroot}

%changelog
* Tue Mar 29 2016 Néil Ge <neil@gyz.io> - 1.203-2
- Rebuilt for EL7.

* Tue Nov 10 2015 Daniel Renninghoff <daniel.renninghoff@gmail.com> - 1.203-1
- First version
