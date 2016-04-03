%global commit 55efd0f6acba29e8f8ef9191f98fce80ac627bc6
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:        Tvheadend - a TV streaming server and DVR
Name:           tvheadend
Version:        4.1.322
Release:        git.%{shortcommit}.1%{?dist}

License:        GPLv3
Group:          Applications/Multimedia
URL:            https://tvheadend.org/projects/tvheadend

# The source was pulled from upstreams git scm. Use the following
# commands to generate the tarball
# git clone https://github.com/tvheadend/tvheadend.git 
# cd tvheadend/
# git archive 55efd0f6acba29e8f8ef9191f98fce80ac627bc6 --format=tar --prefix=tvheadend/ | gzip > ~/tvheadend/tvheadend-4.1.322-git.55efd0f.tar.gz

Source0:	tvheadend-4.1.322-git.55efd0f.tar.gz
#Patch999:      test.patch

BuildRequires:  systemd-units >= 1
BuildRequires:  dbus-devel
BuildRequires:  avahi-libs
BuildRequires:  openssl-devel
BuildRequires:  git 
BuildRequires:  wget
BuildRequires:  ffmpeg-devel
BuildRequires:  libvpx-devel
BuildRequires:  python
BuildRequires:  gettext-devel

Requires:       systemd-units >= 1

%description
Tvheadend is a TV streaming server with DVR for Linux supporting
DVB, ATSC, IPTV, SAT>IP as input sources. Can be used as a backend
to Showtime, XBMC and various other clients.

%prep
%setup -q -n %{name}
#%patch999 -p1 -b .test

%build
echo %{version}-%{release} > %{_builddir}/%{name}/rpm/version

%ifarch %arm
      %configure --disable-lockowner --enable-bundle --disable-libffmpeg_static
%else
      %configure --disable-lockowner --enable-bundle --enable-libffmpeg_static
%endif

%{__make}

%install
# binary
make install DESTDIR=%{buildroot}

# systemd stuff
mkdir -p -m755 %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 644 rpm/tvheadend.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/tvheadend
mkdir -p -m755 %{buildroot}%{_unitdir}
install -p -m 644 rpm/tvheadend.service %{buildroot}%{_unitdir}

%pre
getent group tvheadend >/dev/null || groupadd -f -g 283 -r tvheadend
if ! getent passwd tvheadend > /dev/null ; then
  if ! getent passwd 283 > /dev/null ; then
    useradd -r -l -u 283 -g tvheadend -d /home/tvheadend -s /sbin/nologin -c "Tvheadend TV server" tvheadend
  else
    useradd -r -l -g tvheadend -d /home/tvheadend -s /sbin/nologin -c "Tvheadend TV server" tvheadend
  fi
  usermod -a -G wheel tvheadend
  usermod -a -G video tvheadend
  usermod -a -G audio tvheadend
fi
if ! test -d /home/tvheadend ; then
  mkdir -m 0755 /home/tvheadend || exit 1
  chown tvheadend.tvheadend /home/tvheadend || exit 1
fi
exit 0

%post
%systemd_post tvheadend.service

%postun
%systemd_postun_with_restart tvheadend.service

%files
%{_bindir}/*
%{_mandir}/*
%{_datadir}/%{name}/*
%{_sysconfdir}/sysconfig/*
%{_unitdir}/*

%changelog
* Sun Jun 28 2015 Bob Lightfoot <boblfoot@gmail.com> - 4.1.322-git.55efd0f.1
- Packaging for updated version 4.1
* Sun May 24 2015 Bob Lightfoot <boblfoot@gmail.com> - 4.1.52-git.abf044d.1
- Packaging of version 4.1 for first time
* Sun Apr 19 2015 Bob Lightfoot <boblfoot@gmail.com> - 3.9.2709-git.6b472cd.1
- Packaging of latest updates
* Fri Mar 27 2015 Bob Lightfoot <boblfoot@gmail.com> - 3.9.2662-git.e4cdd3c.1
- initial packaaging with proper versioning 
* Mon Oct 13 2014 Jaroslav Kysela <perex@perex.cz> 
- Original RPM Build Spec File non-Distro Specific
