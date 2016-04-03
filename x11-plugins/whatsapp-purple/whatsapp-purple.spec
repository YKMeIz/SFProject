Summary:            WhatsApp plugin for libpurple messengers (such as Pidgin)
Name:               whatsapp-purple
Version:            0.8.2
Release:            1%{?dist}
License:            GPLv2+
Group:              System Environment/Base
Source:             %{name}-%{version}.tar.gz
URL:                https://github.com/davidgfnet/whatsapp-purple/
BuildRequires:      libpurple-devel
BuildRequires:      freeimage-devel
BuildRequires:      glib2-devel

%description
This is a WhatsApp plugin for Pidgin and libpurple messengers. It connects
to the WhatsApp servers using the password (which needs to be retrieved
separately). Only one client can connect at a time (including your phone).

%prep
echo "Preparing sources"
(cd %_builddir; tar -xf %_sourcedir/%{name}-%{version}.tar.gz)

%build
(cd %_builddir/%{name}-%{version}; make %{?_smp_mflags})

%install
(cd %_builddir/%{name}-%{version}; %make_install)

%files
%_libdir/purple-2/libwhatsapp.so
/usr/share/pixmaps/pidgin/protocols/16/whatsapp.png
/usr/share/pixmaps/pidgin/protocols/22/whatsapp.png
/usr/share/pixmaps/pidgin/protocols/48/whatsapp.png

%changelog
* Wed May 6 2015 David Guillen Fandos <david@davidgf.net> - 0.8.2
- Fixed critical functional bug



