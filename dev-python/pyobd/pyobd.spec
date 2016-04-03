%global ver_major 0
%global ver_minor 9
%global ver_patch 2
%global ver_rel 2
%global ver %{ver_major}.%{ver_minor}.%{ver_patch}.%{ver_rel}

Name:           pyobd
Version:        %{ver}
Release:        4%{?dist}
Summary:        OBD-II (SAE-J1979) compliant scantool software
Group:          Applications/Engineering
License:        GPLv2+
URL:            http://www.obdtester.com/
Source0:        http://www.obdtester.com/download/%{name}_%{ver_major}.%{ver_minor}.%{ver_patch}-%{ver_rel}.tar.gz
BuildArch:      noarch
# import from pyobd module
Patch0:         pyobd-0.9.2-pyobd-module.patch
Requires:       pyserial, wxPython
BuildRequires:  python2-devel, pyserial, wxPython, desktop-file-utils
BuildRequires:  dos2unix, ImageMagick

%description
pyOBD is an OBD-II (SAE-J1979) compliant scantool software written
entirely in Python. It is meant to interface with the low cost ELM 32x
devices such as ELM-USB.

%prep
%setup -q -n %{name}-%{ver_major}.%{ver_minor}.%{ver_patch}

# convert CR/LF to LF
dos2unix pyobd.desktop
# fix encoding settings
sed -i '/Encoding=/ s|UTF8|UTF-8|' pyobd.desktop
# convert GIF icon to PNG
convert pyobd.gif pyobd.png
# change icon in pyobd.desktop
sed -i 's|/usr/share/pyobd/pyobd.gif|pyobd|' pyobd.desktop
# create dummy module init
[ -f __init__.py ] || echo '# module init' > __init__.py

# remove hashbangs
for f in *.py
do
  sed -i '/^[ \t]*#!\/usr\/bin\/env/ d' $f
done

%patch0 -p1 -b .pyobd-module

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 pyobd %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{python_sitelib}/%{name}
install -m 0644 -t %{buildroot}%{python_sitelib}/%{name} *.py

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -m 0644 pyobd.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps

mkdir -p  %{buildroot}%{_datadir}/applications
desktop-file-install --add-category="Utility" \
  --dir=%{buildroot}%{_datadir}/applications \
  pyobd.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc COPYING
%{_datadir}/icons/*
%{_datadir}/applications/pyobd.desktop
%{python_sitelib}/pyobd/
%{_bindir}/pyobd

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 0.9.2.2-1
- Initial release
