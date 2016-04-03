Summary: Screen lock and screen saver
Name: xlockmore
Version: 5.43
Release: 6%{?dist}
License: BSD
Group: Amusements/Graphics
URL: http://www.tux.org/~bagleyd/xlockmore.html
Source0: http://www.tux.org/~bagleyd/xlock/xlockmore-5.43/xlockmore-5.43.tar.bz2
Patch0: xlockmore-5.40-fix_exitcode.patch
BuildRequires: pam-devel
BuildRequires: mesa-libGL-devel mesa-libGLU-devel
BuildRequires: desktop-file-utils libXdmcp-devel
BuildRequires: lesstif-devel gtk2-devel
BuildRequires: libXau-devel
%if 0%{?rhel}
Requires: gnome-icon-theme
%else
Requires: gnome-icon-theme-legacy
%endif

%description
Locks the local X display until a password is entered.

%package motif
Group: Amusements/Graphics
Summary: Motif based frontend for xlockmore
Requires: %{name} = %{version}-%{release}

%description motif
Motif based frontend for xlockmore.

%package gtk
Group: Amusements/Graphics
Summary: GTK based frontend for xlockmore
Requires: %{name} = %{version}-%{release}

%description gtk
GTK based frontend for xlockmore.

%prep
%setup -q
%patch0

%{__sed} -i -e "s,/lib,/%{_lib},g;s,-Wno-format,,g;" configure

%build
%configure --with-crypt --enable-pam --enable-syslog --disable-setuid --disable-mb
%{__make} %{?_smp_mflags}

%install
%{__install} -D -m0755 xlock/xlock %{buildroot}%{_bindir}/xlock
%{__install} -D -m0755 xmlock/xmlock %{buildroot}%{_bindir}/xmlock
%{__install} -D -m0755 xglock/xglock %{buildroot}%{_bindir}/xglock
%{__install} -p -D -m0644 xlock/xlock.man %{buildroot}%{_mandir}/man1/xlock.1
%{__install} -p -D -m0644 xlock/XLock.ad %{buildroot}%{_libdir}/X11/app-defaults/XLock
%{__install} -p -D -m0644 xmlock/XmLock.ad %{buildroot}%{_libdir}/X11/app-defaults/XmLock
%{__chmod} 644 README
%{__chmod} 644 docs/Revisions


%{__mkdir_p} %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/xlock << EOF
#%PAM-1.0
auth       include      system-auth
account    include      system-auth
password   include      system-auth
session    include      system-auth
EOF

%{__mkdir_p} %{buildroot}%{_datadir}/applications

cat >> %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Xlock
Comment=Screen Saver
Encoding=UTF-8
Icon=gnome-lockscreen
Exec=xlock
Terminal=false
Type=Application
EOF

desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	--delete-original \
	--add-category X-Fedora \
	--add-category Application \
	--add-category Graphics \
	%{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README docs/*
%doc %{_mandir}/man1/xlock.1*
%{_bindir}/xlock
%{_libdir}/X11/app-defaults/XLock
%config(noreplace) %{_sysconfdir}/pam.d/xlock
%{_datadir}/applications/*

%files motif
%{_bindir}/xmlock
%{_libdir}/X11/app-defaults/XmLock

%files gtk
%{_bindir}/xglock

%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.43-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Dec 22 2013  Sebastien Lugan <1698DA98@dynmail.crt1.net> - 5.43-4
- Fixed locale support "xlock need to enter password twice" (#991010)

* Thu Dec 05 2013 Adrian Reber <adrian@lisas.de> - 5.43-3
- fixed "xlockmore FTBFS if "-Werror=format-security" flag is used" (#1037397)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Adrian Reber <adrian@lisas.de> - 5.43-1
- updated to 5.43
- fixed "NULL pointer dereference leads to crash and bypass of screen lock" (#985542)

* Sun Feb 10 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 5.41-2
- Remove vendor tag from desktop file as per https://fedorahosted.org/fesco/ticket/1077
- Cleanup spec as per recently changed packaging guidelines

* Tue Nov 20 2012 Adrian Reber <adrian@lisas.de> - 5.41-1
- updated to 5.41
- dropped upstreamed patch for CVE-2012-4524
- fixed "xlock exits on segfault, unlocking the screen" (#874484)

* Mon Oct 22 2012 Adrian Reber <adrian@lisas.de> - 5.40-4
- conditionalize icon BR

* Thu Oct 18 2012 Adrian Reber <adrian@lisas.de> - 5.40-3
- fixed "CVE-2012-4524 xlockmore: Screensaver crash (screen lock bypass) when 'dclock' mode used" (#867908)

* Thu Oct 18 2012 Adrian Reber <adrian@lisas.de> - 5.40-2
- removed esound-devel BR

* Sun Oct 14 2012 Adrian Reber <adrian@lisas.de> - 5.40-1
- updated to 5.40

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 25 2012 Adrian Reber <adrian@lisas.de> - 5.38-1
- updated to 5.38
- removed buildroot and clean section

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 5.34-2
- Rebuild for new libpng

* Tue Jun 07 2011 Adrian Reber <adrian@lisas.de> - 5.34-1
- updated to 5.34
- fixed "Desktop file should not include extension..." (#701699)
- fixed "...missing Requires" (#701699); added R: gnome-icon-theme-legacy

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adrian Reber <adrian@lisas.de> - 5.31-1
- updated to 5.31
- removed xlockmore-fix_petri.patch

* Sat May 08 2010 Adrian Reber <adrian@lisas.de> - 5.28-2
- fixed "FTBFS xlockmore-5.28-1.fc12: ImplicitDSOLinking" (#564929)

* Sun Aug 30 2009 Adrian Reber <adrian@lisas.de> - 5.28-1
- updated to 5.28
- applied patch to fix "xlock -mode petri segfaults with 32 bit displays" (#518379)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.26.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 09 2008 Adrian Reber <adrian@lisas.de> - 5.26.1-1
- updated to 5.26.1

* Mon Feb 18 2008 Adrian Reber <adrian@lisas.de> - 5.25-1
- updated to 5.25

* Sat Oct 13 2007 Adrian Reber <adrian@lisas.de> - 5.24-1
- updated to 5.24

* Tue Feb 06 2007 Adrian Reber <adrian@lisas.de> - 5.23-1
- updated to 5.23

* Tue Sep 12 2006 Adrian Reber <adrian@lisas.de> - 5.22-3
- rebuilt
- swtiched to lesstif

* Sun Jul 09 2006 Adrian Reber <adrian@lisas.de> - 5.22-2
- rebuild for new freetype

* Mon May 01 2006 Adrian Reber <adrian@lisas.de> - 5.22-1
- updated to 5.22
- changed pam file to use include instead of pam_stack.so

* Tue Feb 21 2006 Adrian Reber <adrian@lisas.de> - 5.21-1
- updated to 5.21

* Fri Dec 16 2005 Adrian Reber <adrian@lisas.de> - 5.20.1-1
- updated to 5.20.1
- changes for modular X
- removed "GENTOO" hack

* Sun Aug 21 2005 Adrian Reber <adrian@lisas.de> - 5.19-1
- updated to 5.19
- upstream included a fix for (BZ #161740), but "GENTOO" needs
  to be defined during compilation

* Mon Jun 27 2005 Adrian Reber <adrian@lisas.de> - 5.18-3
- included patch to make it work again with PAM (BZ #161740)

* Fri Jun 17 2005 Adrian Reber <adrian@lisas.de> - 5.18-2
- update to 5.18

* Wed Apr 13 2005 Adrian Reber <adrian@lisas.de> - 5.16-1
- update to 5.16

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Feb 24 2005 Adrian Reber <adrian@lisas.de> - 5.15-1
- update to 5.15
- moved motif and gtk2 frontend to subpackages
- build with pam support
- added .desktop file

* Sun Dec 12 2004 Dries Verachtert <dries@ulyssis.org> 5.14.1-1
- Update to release 5.14.1.

* Thu Oct 28 2004 Dries Verachtert <dries@ulyssis.org> 5.13-1
- update to release 5.13

* Thu May 27 2004 Dries Verachtert <dries@ulyssis.org> 5.12-1
- update to 5.12

* Sun Jan 11 2004 Dries Verachtert <dries@ulyssis.org> 5.10-2
- cleanup of spec file

* Thu Dec 25 2003 Dries Verachtert <dries@ulyssis.org> 5.10-1
- first packaging for Fedora Core 1
