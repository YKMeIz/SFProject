%define _desktopdir %{_datadir}/applications
%define _iconsdir %{_datadir}/icons

Name:           centerim5
Version:        5.0.0beta2
Release:        3%{?dist}

Summary:        Text mode menu- and window-driven IM

Group:          Applications/Internet
License:        GPLv2+
URL:            http://www.centerim.org/
Source0:        http://www.centerim.org/download/cim5/%{name}-%{version}.tar.gz
Source1:        centerim5.svg
Source2:        centerim5.desktop

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  curl-devel
BuildRequires:  ncurses-devel >= 4.2
BuildRequires:  gettext-devel
BuildRequires:  gpgme-devel
BuildRequires:  openssl-devel
BuildRequires:  libjpeg-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libpurple-devel
BuildRequires:  libsigc++20-devel

Requires:       libpurple
Requires:       xdg-utils


# let's not obsolete anything yet, version 4 still works
#Provides:       centericq = %{version}
#Obsoletes:      centericq <= 4
#Provides:	centerim
#Obsoletes:	centerim

%description
CenterIM5 is a text mode menu and window-driven IM interface that supports
the ICQ2000, Yahoo!, MSN, AIM TOC, IRC, Gadu-Gadu and Jabber protocols.
Internal RSS reader and a client for LiveJournal are provided.


%prep
%setup -q


%build
%configure
# centerim5 bug: pgklibdir isn't getting set properly from autotools.  Set manually.
# This is so centerim5 plugins can be found.
# TODO: build using cmake instead?
sed -i 's:#define PKGLIBDIR "":#define PKGLIBDIR "%{_libdir}/%{name}":' config.h
make %{?_smp_flags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# remove unnecessary stuff
rm -f %{buildroot}%{_libdir}/%{name}/*a

install -d %{buildroot}%{_datadir}/icons
install -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icons
desktop-file-install --vendor=fedora                    \
        --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
                %{SOURCE2}

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
update-desktop-database &> /dev/null || :
/sbin/ldconfig

%postun
update-desktop-database &> /dev/null || :
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc ABOUT-NLS AUTHORS COPYING ChangeLog HACKING NEWS README TODO contrib/extnotify.py
/%{_bindir}/%{name}
/%{_libdir}/*
/%{_desktopdir}/*
/%{_iconsdir}/*
/%{_mandir}/man1/%{name}.1.gz

%changelog
* Tue Mar 03 2015 Wade Berrier <wberrier@gmail.com> - 5.0.0beta2-3
- fix finding of centerim5 plugins

* Mon May 05 2014 Nux <rpm@li.nux.ro> - 5.0.0beta2-2
- upgrade to beta2

* Mon Oct 08 2012 Nux <rpm@li.nux.ro> - 5.0.0beta1-1
- initial rpm package for centerim5
