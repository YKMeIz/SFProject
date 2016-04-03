%global debug_package %{nil}
%global __provides_exclude_from ^/opt/viber/.*$

Summary:        Free instant messages and calls
Summary(ru):    Бесплатные сообщения и звонки
Name:           viber
Version:        4.2.2.6
Release:        8%{dist}

Group:      Applications/Internet
License:    Proprietary
URL:        http://viber.com
Source0:    http://download.cdn.viber.com/cdn/desktop/Linux/%{name}.deb

BuildRequires:  desktop-file-utils
BuildRequires:  chrpath

Provides:   libicuuc.so.48()(64bit)
Provides:   libicui18n.so.48()(64bit)
Provides:   libqfacebook.so()(64bit)

ExclusiveArch:    x86_64

%description
More than 200 million Viber users text, call, and send photo and video messages
worldwide - for free.

Your phone number is your ID. Viber syncs with your mobile contact list,
automatically detecting which of your contacts have Viber.

Viber Desktop and the latest versions of the Viber mobile app were designed for
individuals using Viber on multiple devices, so you can always use the app
that's right for you, whether at home, in school, at the office, or on the go.

Viber is completely free with no advertising. We value your privacy.

Main features:
- Text with your friends, privately or in groups
- Make free calls with HD sound quality
- Seamlessly transfer calls between Viber Desktop and the Viber app with one
  click or tap
- Send stickers and emoticons
- Messages are shown on all devices

%description -l ru
Более 200 миллионов пользователей Viber бесплатно звонят, отправляют сообщения,
фото и видео по всему миру.

Номер телефона — это ваш ID. Viber синхронизируется со списком контактов вашего
мобильного телефона, автоматически определяя, какие из контактов привязаны к
Viber.

Viber Desktop и последние версии Viber Mobile были разработаны для людей,
исплользующих Viber на нескольких устройствах. Поэтому вы всегда можете
использовать приложение, где бы вы ни были: дома, в школе, офисе или в пути.

Viber полностью бесплатен и не показывает рекламу. Конфиденциальность превыше
всего.

Основные возможности:
- Общайтесь с друзьями наедине или в группах
- Совершайте звонки с высоким качеством звука
- Бесшовно перенаправляйте звонки между приложениями, запущенными на ПК и
  смартфоне, одним кликом мыши или касанием экрана
- Отправляйте стикеры и смайлы
- Сообщения показываются на всех устройствах с установленным Viber

%prep
%setup -q -c -T

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# Extract DEB packages:
pushd %{buildroot}
    ar p %{SOURCE0} data.tar.gz | gzip -d > %{name}-%{version}.x86_64.tar
    tar -xf %{name}-%{version}.x86_64.tar
popd

# Modify *.desktop file:
sed -e 's|Exec=\/opt\/viber\/Viber|Exec=%{name}|' -i %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -e 's/Path=/Path=\/opt\/viber/' -i %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install *.desktop file:
desktop-file-install --vendor rfremix \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category Network \
  --add-category X-Fedora \
  --remove-category Application \
  --remove-key Encoding \
  --set-icon viber \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
echo "StartupWMClass=ViberPC" >> %{buildroot}%{_datadir}/applications/rfremix-%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/rfremix-%{name}.desktop

# Fix executable attributes:
chmod 755 %{buildroot}/opt/%{name}/Viber

# Create run srcipt:
mkdir -p %{buildroot}%{_bindir}
echo -e '#!/bin/bash\n\nLD_LIBRARY_PATH=/opt/viber /opt/viber/Viber\n' > %{buildroot}%{_bindir}/%{name}
chmod +x %{buildroot}%{_bindir}/%{name}

# Remove unused directories and tarball:
pushd %{buildroot}
    rm %{name}-%{version}.x86_64.tar
popd

#Remove rpath
find %{buildroot} -name "*" -exec chrpath --delete {} \; 2>/dev/null

%post
update-desktop-database &> /dev/null || :
touch --no-create /usr/share/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache --quiet /usr/share/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create /usr/share/icons/hicolor &>/dev/null
    gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :

%files
/opt/viber
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*
%{_datadir}/pixmaps/*
%{_datadir}/%{name}/*

%changelog
* Sat Aug 10 2015 Vasiliy N. Glazov <vascom2@gmail.com> - 4.2.2.6-8.R
- Correct .desktop file for Gnome

* Tue Dec 23 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 4.2.2.6-7.R
- Correct .desktop file

* Fri Dec 12 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 4.2.2.6-6.R
- Provides libqfacebook

* Wed Dec 10 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 4.2.2.6-5.R
- Bump release

* Wed Dec 10 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 4.2.2.6-4.R
- Disable provides for Qt5 libs

* Wed Sep 03 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 4.2.2.6-3.R
- Correct script creating

* Wed Sep 03 2014 Vasiliy N. Glazov <vascom2@gmail.com> - 4.2.2.6-2.R
- Remove rpath
- Remake run script and modify desktop-file

* Sat Aug 30 2014 carasin berlogue <carasin DOT berlogue AT mail DOT ru> - 4.2.2.6-1
- initial build for Fedora
