Summary:   Open source remote desktop protocol (RDP) server
Name:      xrdp
Version:   0.6.1
Release:   3%{?dist}
License:   GPLv2+ with exceptions
Group:     Applications/Internet
URL:       http://xrdp.sourceforge.net/
Source0:   http://sourceforge.net/projects/xrdp/files/xrdp/%{version}/xrdp-v%{version}.tar.gz

Patch0: xrdp-pam-auth.patch
Patch1: xrdp-use-xinitrc-in-startwm-sh.patch
Patch2: xrdp-pam_session.patch
# https://sourceforge.net/tracker/?group_id=112022&atid=665248
# https://bugzilla.redhat.com/show_bug.cgi?id=905411
Patch3: xrdp-endian.patch
Patch4: xrdp-0.6.1-syslog-format.patch
Patch5: xrdp-0.6.1-memset.patch
Patch6: xrdp-0.6.1-implicit-decl.patch

Source1: xrdp.service
Source2: xrdp-sesman.service
Source3: xrdp.sysconfig
Source4: xrdp.logrotate

BuildRequires: pam-devel
BuildRequires: openssl-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
Buildrequires: libX11-devel
BuildRequires: libXfixes-devel
BuildRequires: systemd-units

#vnc-server provides Xvnc (tigervnc-server in fedora)
Requires: tigervnc-server-minimal

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-sysv

%description
The goal of this project is to provide a fully functional Linux terminal
server, capable of accepting connections from rdesktop and Microsoft's own
terminal server / remote desktop clients.

%prep
#%setup -q -n %{name}-%{version}
%setup -q -n %{name}-v%{version}
%patch0 -p2
%patch1 -p2
%patch2 -p1
%patch3 -p1 -b .endian
%patch4 -p1 -b .syslog-format
%patch5 -p1 -b .memset
%patch6 -p1 -b .implicit-decl

# remove unused modules from xrdp login combobox
%{__sed} -i -e '/\[xrdp2\]/,$d' xrdp/xrdp.ini

#Low is 40 bit key and everything from client to server is encrypted.
#Medium is 40 bit key, everything both ways is encrypted.
#High is 128 bit key everything both ways is encrypted.

# increase encryption to 128 bit's
%{__sed} -i 's/crypt_level=low/crypt_level=high/g' xrdp/xrdp.ini

# create 'bash -l' based startwm, to pick up PATH etc.
echo '#!/bin/bash -l
. %{_sysconfdir}/xrdp/startwm.sh' > sesman/startwm-bash.sh

# set 'bash -l' based startwm script as default
%{__sed} -i -e 's/DefaultWindowManager=startwm.sh/DefaultWindowManager=startwm-bash.sh/' sesman/sesman.ini

%build
./bootstrap

%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}

#remove .la and .a files
find %{buildroot} -name '*.a' -exec rm {} \;
find %{buildroot} -name '*.la' -exec rm {} \;

#install sesman pam config /etc/pam.d/xrdp-sesman
%{__install} -Dp -m 644 instfiles/pam.d/xrdp-sesman %{buildroot}%{_sysconfdir}/pam.d/xrdp-sesman

#installx xrdp systemd units
%{__install} -Dp -m 644 %{SOURCE1} %{buildroot}/lib/systemd/system/xrdp.service
%{__install} -Dp -m 644 %{SOURCE2} %{buildroot}/lib/systemd/system/xrdp-sesman.service

#install xrdp sysconfig /etc/sysconfig/xrdp
%{__install} -Dp -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/xrdp

#install logrotate /etc/logrotate.d/xrdp
%{__install} -Dp -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/xrdp

#install log file /var/log/xrdp-sesman.log
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/
touch %{buildroot}%{_localstatedir}/log/xrdp-sesman.log

# rsakeys.ini
touch %{buildroot}%{_sysconfdir}/xrdp/rsakeys.ini
%{__chmod} 0600 %{buildroot}%{_sysconfdir}/xrdp/rsakeys.ini

#install 'bash -l' startwm script
%{__install} -Dp -m 755 sesman/startwm-bash.sh %{buildroot}%{_sysconfdir}/xrdp/startwm-bash.sh


%post
if [ $1 -eq 1 ] ; then 
# Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

chcon --type=bin_t /usr/sbin/xrdp
chcon --type=bin_t /usr/sbin/xrdp-sesman

%preun
if [ $1 -eq 0 ] ; then
# Package removal, not upgrade
    /bin/systemctl --no-reload disable xrdp.service > /dev/null 2>&1 || :
    /bin/systemctl stop xrdp.service > /dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
# Package upgrade, not uninstall
    if [ "`/bin/systemctl is-active xrdp.service`" = 'active' ]; then
        /bin/systemctl stop xrdp.service >/dev/null 2>&1 || :
        /bin/systemctl start xrdp.service >/dev/null 2>&1 || :
    fi
fi

%triggerun -- xrdp < 0.6.0-1
/usr/bin/systemd-sysv-convert --save xrdp >/dev/null 2>&1 ||:

# If the package is allowed to autostart:
/bin/systemctl --no-reload enable xrdp.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del xrdp >/dev/null 2>&1 || :
if [ "`/bin/systemctl is-active xrdp.service`" = 'active' ]; then
    /bin/systemctl stop xrdp.service >/dev/null 2>&1 || :
    /bin/systemctl start xrdp.service >/dev/null 2>&1 || :
fi


%files
%doc COPYING *.txt
%dir %{_libdir}/xrdp
%dir %{_sysconfdir}/xrdp
%dir %{_datadir}/xrdp
%config(noreplace) %{_sysconfdir}/xrdp/sesman.ini
%config(noreplace) %{_sysconfdir}/xrdp/xrdp.ini
%config(noreplace) %{_sysconfdir}/pam.d/xrdp-sesman
%config(noreplace) %{_sysconfdir}/logrotate.d/xrdp
%config(noreplace) %{_sysconfdir}/sysconfig/xrdp
%{_sysconfdir}/xrdp/*.sh
%{_sysconfdir}/xrdp/km*.ini
%{_bindir}/xrdp-genkeymap
%{_bindir}/xrdp-sesadmin
%{_bindir}/xrdp-keygen
%{_bindir}/xrdp-sesrun
%{_bindir}/xrdp-sestest
%{_bindir}/xrdp-dis
%{_sbindir}/xrdp-chansrv
%{_sbindir}/xrdp
%{_sbindir}/xrdp-sesman
%{_sbindir}/xrdp-sessvc
%{_datadir}/xrdp/ad256.bmp
%{_datadir}/xrdp/cursor0.cur
%{_datadir}/xrdp/cursor1.cur
%{_datadir}/xrdp/xrdp256.bmp
%{_datadir}/xrdp/sans-10.fv1
%{_datadir}/xrdp/ad24b.bmp
%{_datadir}/xrdp/xrdp24b.bmp
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_libdir}/xrdp/lib*.so.*
%{_libdir}/xrdp/libcommon.so
%{_libdir}/xrdp/libmc.so
%{_libdir}/xrdp/librdp.so
%{_libdir}/xrdp/libscp.so
%{_libdir}/xrdp/libvnc.so
%{_libdir}/xrdp/libxrdp.so
%{_libdir}/xrdp/libxup.so
/lib/systemd/system/xrdp-sesman.service
/lib/systemd/system/xrdp.service

%ghost %{_localstatedir}/log/xrdp-sesman.log
%attr(0600,root,root) %verify(not size md5 mtime) %{_sysconfdir}/xrdp/rsakeys.ini

%changelog
* Wed Jul 15 2015 Nux <rpm@li.nx.ro> - 0.6.1-3
- add some chcon hacks in %post so Selinux will allow operation

* Tue Apr  1 2014 Bojan Smojver <bojan@rexursive.com> - 0.6.1-2
- try a bump to official 0.6.1
- provide format for syslog() call
- fix memset() call
- fix implicit declarations

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jan 29 2013 Dan Horák <dan[at]danny.cz> - 0.6.0-0.7
- fix check for big endian arches (#905411)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.5
- bind xrdp-sesman.service to xrdp.service, so that restarts work
- do not use forking style, but run services in the foreground instead
- dispense with ExecStop, systemd will do that for us

* Sat May 26 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.4
- do explicit stop/start in order to get xrdp-sesman.service up too

* Sat May 26 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.3
- also attempt to restart xrdp-sesman.service (just xrdp.service won't do it)
- stop xrdp-sesman.service when not needed by xrdp.service

* Fri May 25 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.2
- bump release for rebuild with the correct e-mail address

* Fri May 25 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.1
- more work on systemd support
- remove xrdp-dis for now, current HEAD is broken (explicit rpaths)

* Wed May 23 2012 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.6.0-0.1
- include patch's from Bojan Smojver bz#821569 , bz#611669

* Sat Feb 04 2012 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.16
- add support for systemd

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.13
- up to git tag a9cfc235211a49c69c3cce3f98ee5976ff8103a4

* Thu Nov 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.12.03172010
- fix logrotate to not restart xrdp and drop all open connections

* Mon Oct 04 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.11.03172010
- Load a default keymap when current keymap doesnt exist

* Thu Jul 08 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.10.03172010
- fix rhbz #611669 (load environment variables)

* Thu Mar 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.9.03172010
- buildrequires libXfixes-devel

* Thu Mar 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.8.03172010
- buildrequires libX11-devel

* Thu Mar 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.7.03172010
- sync with last xrdp cvs

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.0-0.6.20090811cvs
- use password-auth instead of system-auth

* Tue Sep 08 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.5.20090811cvs
- fix xrdp-sesman pam.d to uses system-auth

* Fri Sep 04 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.4.20090811cvs
- increase encryption to 128 bit's
- include system-auth into /etc/pam.d/xrdp-sesman

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.0-0.3.20090811cvs
- rebuild with new openssl

* Thu Aug 13 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.2.20090811cvs
- more changes to spec file https://bugzilla.redhat.com/show_bug.cgi?id=516364#c10

* Wed Aug 12 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.1.20090811cvs
- change versioning schema
- improve initscript
- fix some macros


* Tue Aug 11 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-2.20090811cvs
- changes from BZ#516364 comment 2 from Mamoru Tasaka
- changed license to "GPLv2+ with exceptions"
- dropped -libs subpackage
- use cvs version
- remove a patch and use sed instead
- remove attr's

* Thu Apr 02 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.5.0-1
- Initial RPM release
