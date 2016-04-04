Name:           rxvt-unicode
Version:        9.22
Release:        1%{?dist}
Summary:        Unicode version of rxvt

Group:          User Interface/X
License:        GPLv3
URL:            http://software.schmorp.de/
Source0:        http://dist.schmorp.de/%{name}/%{name}-%{version}.tar.bz2
Source1:        rxvt-unicode.desktop
Source2:        rxvt-unicode-ml.desktop
Source3:        rxvt-unicode-256color.desktop
Source4:        rxvt-unicode-256color-ml.desktop
Patch0:         rxvt-unicode-9.21-Fix-hard-coded-wrong-path-to-xsubpp.patch
Patch1:         rxvt-unicode-0001-Prefer-XDG_RUNTIME_DIR-over-the-HOME.patch

BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glib2-devel
BuildRequires:  ncurses ncurses-base ncurses-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libX11-devel
BuildRequires:  libXft-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXt-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  perl-devel, perl(ExtUtils::Embed)
%if 0%{?fedora} > 13 || !0%{?rhel}
BuildRequires:  gdk-pixbuf2-devel
%endif
%if 0%{?fedora} >= 15
BuildRequires:  libev-source
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       ncurses-base

%description
rxvt-unicode is a clone of the well known terminal emulator rxvt, modified to
store text in Unicode (either UCS-2 or UCS-4) and to use locale-correct input
and output. It also supports mixing multiple fonts at the same time, including
Xft fonts.

%package ml
Summary:        Multi-language version of rxvt-unicode
Group:          User Interface/X
Requires:       %{name} = %{version}-%{release}

%description ml
Version of rxvt-unicode with enhanced multi-language support.

%package 256color
Summary:        256 color version of rxvt-unicode
Group:          User Interface/X
Requires:       %{name} = %{version}-%{release}

%description 256color
256 color version of rxvt-unicode

%package 256color-ml
Summary:        256 color multi-language version of rxvt-unicode
Group:          User Interface/X
Requires:       %{name} = %{version}-%{release}

%description 256color-ml
Version of rxvt-unicode with 256color and enhanced multi-language support.

%prep
%setup -q -c %{name}-%{version}
pushd %{name}-%{version}
%patch0 -p1
%patch1 -p1 -b .runtime_dir
popd

cp -r %{name}-%{version} %{name}-%{version}-ml
cp -r %{name}-%{version} %{name}-%{version}-256color
cp -r %{name}-%{version} %{name}-%{version}-256color-ml

%if 0%{?fedora} >= 15
rm -rf %{name}-%{version}/libev
ln -s %{_datadir}/libev-source %{name}-%{version}/libev

rm -rf %{name}-%{version}-ml/libev
ln -s %{_datadir}/libev-source %{name}-%{version}-ml/libev

rm -rf %{name}-%{version}-256color/libev
ln -s %{_datadir}/libev-source %{name}-%{version}-256color/libev

rm -rf %{name}-%{version}-256color-ml/libev
ln -s %{_datadir}/libev-source %{name}-%{version}-256color-ml/libev
%endif

%build
# standard version
pushd %{name}-%{version}
%configure \
 --enable-keepscrolling \
 --enable-selectionscrolling \
 --enable-pointer-blank \
 --enable-utmp \
 --enable-wtmp \
 --enable-lastlog \
 --enable-xft \
 --enable-font-styles \
%if 0%{?fedora} > 13
 --enable-pixbuf \
%endif
 --enable-transparency \
 --enable-fading \
 --enable-rxvt-scroll \
 --enable-next-scroll \
 --enable-xterm-scroll \
 --enable-perl \
 --enable-mousewheel \
 --enable-slipwheeling \
 --enable-smart-resize \
 --enable-frills \
 --disable-iso14755 \
 --with-term=rxvt-unicode

make %{?_smp_mflags}
popd

# multi-language version
pushd %{name}-%{version}-ml
%configure \
 --enable-keepscrolling \
 --enable-selectionscrolling \
 --enable-pointer-blank \
 --enable-utmp \
 --enable-wtmp \
 --enable-lastlog \
 --enable-unicode3 \
 --enable-combining \
 --enable-xft \
 --enable-font-styles \
%if 0%{?fedora} > 13
 --enable-pixbuf \
%endif
 --enable-transparency \
 --enable-fading \
 --enable-rxvt-scroll \
 --enable-next-scroll \
 --enable-xterm-scroll \
 --enable-perl \
 --enable-xim \
 --enable-iso14755 \
 --with-codesets=all \
 --enable-frills \
 --enable-mousewheel \
 --enable-slipwheeling \
 --enable-smart-resize \
 --with-term=rxvt-unicode \
 --with-name=urxvt-ml

make %{?_smp_mflags}
popd

# 256 color version
pushd %{name}-%{version}-256color
%configure \
 --enable-keepscrolling \
 --enable-selectionscrolling \
 --enable-pointer-blank \
 --enable-utmp \
 --enable-wtmp \
 --enable-lastlog \
 --enable-xft \
 --enable-font-styles \
%if 0%{?fedora} > 13
 --enable-pixbuf \
%endif
 --enable-transparency \
 --enable-fading \
 --enable-rxvt-scroll \
 --enable-next-scroll \
 --enable-xterm-scroll \
 --enable-perl \
 --enable-mousewheel \
 --enable-slipwheeling \
 --enable-smart-resize \
 --enable-frills \
 --disable-iso14755 \
 --with-term=rxvt-unicode-256color \
 --with-name=urxvt256c \
 --enable-256-color

make %{?_smp_mflags}
popd

# multi-language version with 256color
pushd %{name}-%{version}-256color-ml
%configure \
 --enable-keepscrolling \
 --enable-selectionscrolling \
 --enable-pointer-blank \
 --enable-utmp \
 --enable-wtmp \
 --enable-lastlog \
 --enable-unicode3 \
 --enable-combining \
 --enable-xft \
 --enable-font-styles \
%if 0%{?fedora} > 13
 --enable-pixbuf \
%endif
 --enable-transparency \
 --enable-fading \
 --enable-rxvt-scroll \
 --enable-next-scroll \
 --enable-xterm-scroll \
 --enable-perl \
 --enable-xim \
 --enable-iso14755 \
 --with-codesets=all \
 --enable-frills \
 --enable-mousewheel \
 --enable-slipwheeling \
 --enable-smart-resize \
 --with-term=rxvt-unicode-256color \
 --with-name=urxvt256c-ml \
 --enable-256-color

make %{?_smp_mflags}
popd

%install
for ver in \
 %{name}-%{version} %{name}-%{version}-ml \
 %{name}-%{version}-256color %{name}-%{version}-256color-ml;
do
    pushd ${ver}
    make install DESTDIR=%{buildroot}
    popd
done;

# create links for man pages
pushd %{buildroot}%{_mandir}/man1
for ver in -ml 256c 256c-ml;
do
    ln -s urxvt.1.gz urxvt${ver}.1.gz
    ln -s urxvtc.1.gz urxvt${ver}c.1.gz
    ln -s urxvtd.1.gz urxvt${ver}d.1.gz
done;
popd

# install desktop files
desktop-file-install \
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
  --vendor=fedora \
%endif
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE1}

desktop-file-install \
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
  --vendor=fedora \
%endif
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE2}

desktop-file-install \
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
  --vendor=fedora \
%endif
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE3}

desktop-file-install \
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
  --vendor=fedora \
%endif
  --dir=%{buildroot}%{_datadir}/applications \
  %{SOURCE4}

# install terminfo for 256color
mkdir -p %{buildroot}%{_datadir}/terminfo/r/
tic -e rxvt-unicode-256color -s -o %{buildroot}%{_datadir}/terminfo/ \
 %{name}-%{version}/doc/etc/rxvt-unicode.terminfo


%files
%doc %{name}-%{version}/README.FAQ
%doc %{name}-%{version}/INSTALL
%doc %{name}-%{version}/doc/README.xvt
%doc %{name}-%{version}/doc/etc
%doc %{name}-%{version}/doc/changes.txt
%license %{name}-%{version}/COPYING
%{_bindir}/urxvt
%{_bindir}/urxvtc
%{_bindir}/urxvtd
%{_mandir}/man1/urxvt.1*
%{_mandir}/man1/urxvtc.1*
%{_mandir}/man1/urxvtd.1*
%{_mandir}/man1/urxvt-background.1*
%{_mandir}/man1/urxvt-bell-command.1*
%{_mandir}/man1/urxvt-block-graphics-to-ascii.1*
%{_mandir}/man1/urxvt-clipboard-osc.1*
%{_mandir}/man1/urxvt-confirm-paste.1*
%{_mandir}/man1/urxvt-digital-clock.1*
%{_mandir}/man1/urxvt-eval.1*
%{_mandir}/man1/urxvt-example-refresh-hooks.1*
%{_mandir}/man1/urxvt-extensions.1*
%{_mandir}/man1/urxvt-keysym-list.1*
%{_mandir}/man1/urxvt-kuake.1*
%{_mandir}/man1/urxvt-matcher.1*
%{_mandir}/man1/urxvt-option-popup.1*
%{_mandir}/man1/urxvt-overlay-osc.1*
%{_mandir}/man1/urxvt-readline.1*
%{_mandir}/man1/urxvt-remote-clipboard.1*
%{_mandir}/man1/urxvt-searchable-scrollback.1*
%{_mandir}/man1/urxvt-selection-autotransform.1*
%{_mandir}/man1/urxvt-selection-pastebin.1*
%{_mandir}/man1/urxvt-selection-popup.1*
%{_mandir}/man1/urxvt-selection-to-clipboard.1*
%{_mandir}/man1/urxvt-selection.1*
%{_mandir}/man1/urxvt-tabbed.1*
%{_mandir}/man1/urxvt-xim-onthespot.1*
%{_mandir}/man3/urxvtperl.3*
%{_mandir}/man7/urxvt.7*
%{_datadir}/applications/*rxvt-unicode.desktop
%{_libdir}/urxvt
%{_datadir}/terminfo/r/rxvt-unicode-256color

%files ml
%{_bindir}/urxvt-ml
%{_bindir}/urxvt-mlc
%{_bindir}/urxvt-mld
%{_mandir}/man1/urxvt-ml.1*
%{_mandir}/man1/urxvt-mlc.1*
%{_mandir}/man1/urxvt-mld.1*
%{_mandir}/man1/urxvt-ml-background.1*
%{_mandir}/man1/urxvt-ml-bell-command.1*
%{_mandir}/man1/urxvt-ml-block-graphics-to-ascii.1*
%{_mandir}/man1/urxvt-ml-clipboard-osc.1*
%{_mandir}/man1/urxvt-ml-confirm-paste.1*
%{_mandir}/man1/urxvt-ml-digital-clock.1*
%{_mandir}/man1/urxvt-ml-eval.1*
%{_mandir}/man1/urxvt-ml-example-refresh-hooks.1*
%{_mandir}/man1/urxvt-ml-extensions.1*
%{_mandir}/man1/urxvt-ml-keysym-list.1*
%{_mandir}/man1/urxvt-ml-kuake.1*
%{_mandir}/man1/urxvt-ml-matcher.1*
%{_mandir}/man1/urxvt-ml-option-popup.1*
%{_mandir}/man1/urxvt-ml-overlay-osc.1*
%{_mandir}/man1/urxvt-ml-readline.1*
%{_mandir}/man1/urxvt-ml-remote-clipboard.1*
%{_mandir}/man1/urxvt-ml-searchable-scrollback.1*
%{_mandir}/man1/urxvt-ml-selection-autotransform.1*
%{_mandir}/man1/urxvt-ml-selection-pastebin.1*
%{_mandir}/man1/urxvt-ml-selection-popup.1*
%{_mandir}/man1/urxvt-ml-selection-to-clipboard.1*
%{_mandir}/man1/urxvt-ml-selection.1*
%{_mandir}/man1/urxvt-ml-tabbed.1*
%{_mandir}/man1/urxvt-ml-xim-onthespot.1*
%{_mandir}/man3/urxvt-mlperl.3*
%{_mandir}/man7/urxvt-ml.7*
%{_datadir}/applications/*rxvt-unicode-ml.desktop

%files 256color
%{_bindir}/urxvt256c
%{_bindir}/urxvt256cc
%{_bindir}/urxvt256cd
%{_mandir}/man1/urxvt256c.1*
%{_mandir}/man1/urxvt256cc.1*
%{_mandir}/man1/urxvt256cd.1*
%{_mandir}/man1/urxvt256c-background.1*
%{_mandir}/man1/urxvt256c-bell-command.1*
%{_mandir}/man1/urxvt256c-block-graphics-to-ascii.1*
%{_mandir}/man1/urxvt256c-clipboard-osc.1*
%{_mandir}/man1/urxvt256c-confirm-paste.1*
%{_mandir}/man1/urxvt256c-digital-clock.1*
%{_mandir}/man1/urxvt256c-eval.1*
%{_mandir}/man1/urxvt256c-example-refresh-hooks.1*
%{_mandir}/man1/urxvt256c-extensions.1*
%{_mandir}/man1/urxvt256c-keysym-list.1*
%{_mandir}/man1/urxvt256c-kuake.1*
%{_mandir}/man1/urxvt256c-matcher.1*
%{_mandir}/man1/urxvt256c-option-popup.1*
%{_mandir}/man1/urxvt256c-overlay-osc.1*
%{_mandir}/man1/urxvt256c-readline.1*
%{_mandir}/man1/urxvt256c-remote-clipboard.1*
%{_mandir}/man1/urxvt256c-searchable-scrollback.1*
%{_mandir}/man1/urxvt256c-selection-autotransform.1*
%{_mandir}/man1/urxvt256c-selection-pastebin.1*
%{_mandir}/man1/urxvt256c-selection-popup.1*
%{_mandir}/man1/urxvt256c-selection-to-clipboard.1*
%{_mandir}/man1/urxvt256c-selection.1*
%{_mandir}/man1/urxvt256c-tabbed.1*
%{_mandir}/man1/urxvt256c-xim-onthespot.1*
%{_mandir}/man3/urxvt256cperl.3*
%{_mandir}/man7/urxvt256c.7*
%{_datadir}/applications/*rxvt-unicode-256color.desktop

%files 256color-ml
%{_bindir}/urxvt256c-ml
%{_bindir}/urxvt256c-mlc
%{_bindir}/urxvt256c-mld
%{_mandir}/man1/urxvt256c-ml.1*
%{_mandir}/man1/urxvt256c-mlc.1*
%{_mandir}/man1/urxvt256c-mld.1*
%{_mandir}/man1/urxvt256c-ml-background.1*
%{_mandir}/man1/urxvt256c-ml-bell-command.1*
%{_mandir}/man1/urxvt256c-ml-block-graphics-to-ascii.1*
%{_mandir}/man1/urxvt256c-ml-clipboard-osc.1*
%{_mandir}/man1/urxvt256c-ml-confirm-paste.1*
%{_mandir}/man1/urxvt256c-ml-digital-clock.1*
%{_mandir}/man1/urxvt256c-ml-eval.1*
%{_mandir}/man1/urxvt256c-ml-example-refresh-hooks.1*
%{_mandir}/man1/urxvt256c-ml-extensions.1*
%{_mandir}/man1/urxvt256c-ml-keysym-list.1*
%{_mandir}/man1/urxvt256c-ml-kuake.1*
%{_mandir}/man1/urxvt256c-ml-matcher.1*
%{_mandir}/man1/urxvt256c-ml-option-popup.1*
%{_mandir}/man1/urxvt256c-ml-overlay-osc.1*
%{_mandir}/man1/urxvt256c-ml-readline.1*
%{_mandir}/man1/urxvt256c-ml-remote-clipboard.1*
%{_mandir}/man1/urxvt256c-ml-searchable-scrollback.1*
%{_mandir}/man1/urxvt256c-ml-selection-autotransform.1*
%{_mandir}/man1/urxvt256c-ml-selection-pastebin.1*
%{_mandir}/man1/urxvt256c-ml-selection-popup.1*
%{_mandir}/man1/urxvt256c-ml-selection-to-clipboard.1*
%{_mandir}/man1/urxvt256c-ml-selection.1*
%{_mandir}/man1/urxvt256c-ml-tabbed.1*
%{_mandir}/man1/urxvt256c-ml-xim-onthespot.1*
%{_mandir}/man3/urxvt256c-mlperl.3*
%{_mandir}/man7/urxvt256c-ml.7*
%{_datadir}/applications/*rxvt-unicode-256color-ml.desktop

%changelog
* Thu Feb 25 2016 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- version upgrade

* Wed Feb 17 2016 Till Maas <opensource@till.name> - 9.21-8
-  Do not overwrite CFLAGS or LDFLAGS with make, they are already set by
   %%configure and -lfontconfig is added in upstream Makefile. Overwriting
   LDFLAGS breaks hardening as PIE.
- Use %%license

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.21-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 9.21-5
- Perl 5.22 rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 9.21-4
- Rebuilt for GCC 5 C++11 ABI change

* Sat Jan 03 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 9.21-3
- update license to GPLv3

* Sat Jan 03 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 9.21-2
- add patch from Maciej Borzecki to fix gnome-shell matching
  (rhbz#1031368)

* Fri Jan 02 2015 Andreas Bierfert <andreas.bierfert@lowlatency.de>
- 9.21-1
- version upgrade (rhbz#830236)

* Wed Dec 17 2014 Peter Lemenkov <lemenkov@gmail.com> - 9.20-6
- Don't use HOME for storing control socket. Use XDG directory instead.

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 9.20-5
- Perl 5.20 rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 9.20-2
- There is no need for the patches below, as they change the behavior of our
  package and break the principle of least astonishment.
- Remove Fedora-specific patch to scroll up/down one line. Any users wanting
  this behavior can create their own key bindings.
- Remove Fedora-specific patch to open new tabs with Control-t. Any users
  wanting this behavior can create their own key bindings.
- The popular 'tabbed' extension can now work properly (#1096791).

* Thu May 01 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 9.20-1
- update to upstream release 9.20, which includes a fix for security bug
  CVE-2014-3121 (#1093287, #1093288, #1093289)
- include man pages for new extension (selection-to-clipboard)

* Thu Oct 31 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.19-1
- version upgrade

* Tue Sep 10 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.18-5
- fix tabbed extension

* Sun Aug 18 2013 Paul Howarth <paul@city-fan.org> - 9.18-4
- fix xsubpp path leading to FTBFS (#993374)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 9.18-2
- Perl 5.18 rebuild

* Tue Mar 26 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.18-1
- version upgrade

* Wed Mar 20 2013 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.17-1
- version upgrade

* Mon Feb 25 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 9.16-3
- Remove vendor from desktop files for F19+ https://fedorahosted.org/fesco/ticket/1077

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 30 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.16-1
- version upgrade
- cleanup manpages

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 9.15-2
- Perl 5.16 rebuild

* Sun Jan 22 2012 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.15-1
- version upgrade

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.14-1
- version ugprade
- drop screen patch (upstream)
- disable libAfterImage as it is deprecated

* Fri Nov 18 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.12-5
- use icon from fd.org standard (rhbz#754939)

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 9.12-4
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 9.12-3
- Perl mass rebuild

* Wed Jul 06 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.12-2
- fix segfault (rhbz#711137)

* Mon Jul 04 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.12-1
- version upgrade
- fix key definition (rhbz#718506)

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 9.10-4
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.10-2
- switch back to shift scroll (#667980)
- open new tab on Ctrl+t
- build with libev-source on f15+ (#672396)

* Sun Dec 19 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.10-1
- version upgrade

* Mon Nov 29 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.09-4
- include terminfo for 256color version for now

* Thu Nov 18 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.09-3
- re-add frills build option for standard versions
- bind scrolling actions to crtl+up/down/pgup/pgdown as shift will break the
  tabbing support

* Mon Nov 15 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.09-2
- Rework to provide four versions:
- standard (rxvt-unicode)
- multi-language support (rxvt-unicode-ml)
- 256color version (rxvt-unicode-256color)
- 256color multi-language (rxvt-unicode-256color-ml)

* Sun Nov 14 2010 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.09-1
- version upgrade (fixes #581373)
- allow scrolling with mod+up/down (#510944)
- fixup desktop file (#617519)
- spec file cleanups

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 9.07-2
- Mass rebuild with perl-5.12.0

* Thu Dec 31 2009 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.07-1
- version upgrade

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 9.06-5
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 25 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 9.06-3
- Fix FTBFS: added rxvt-unicode-gcc44.patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.06-1
- version upgrade

* Mon Jun 16 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.05-1
- version upgrade

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com>
- 9.02-2
- add Requires for versioned perl (libperl.so)

* Thu Feb 21 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.02-1
- version upgrade

* Mon Feb 11 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de> - 9.0-2
- Rebuilt for gcc43

* Sat Jan 26 2008 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 9.0-1
- version upgrade

* Thu Dec 27 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 8.9-1
- version upgrade

* Mon Dec 17 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 8.8-1
- version upgrade

* Wed Dec 12 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 8.5a-2
- remove utempter patch for now

* Thu Nov 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 8.5a-1
- version upgrade

* Wed Nov 07 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 8.4-2
- fix #368921 (Rxvt.backgroundPixmap needs libAfterImage support BR now)
- add patch for utempter support

* Sun Oct 28 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 8.4-1
- version upgrade

* Wed Aug 22 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- 8.3-1
- version upgrade
- new license tag

* Sat Jun 02 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
8.2-1
- version upgrade (#239421)

* Sun Jan 21 2007 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
8.1-2
- drop terminfo file it is included in ncurses now

* Fri Dec 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
8.1-1
- version upgrade

* Thu Nov 02 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
8.0-1
- version upgrade

* Fri Sep 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.9-2
- FE6 rebuild

* Tue Aug 08 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.9-1
- version upgrade

* Tue Jul 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.8-1
- version upgrade

* Tue Feb 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.7-1
- version upgrade

* Thu Feb 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.6-2
- Rebuild for Fedora Extras 5

* Fri Feb 10 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.6-1
- version upgrade

* Tue Jan 31 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.5-1
- version upgrade

* Sat Jan 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.4-1
- version upgrade

* Fri Jan 27 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.3a-1
- version upgrade

* Mon Jan 23 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.2-1
- version upgrade (should resolve #178561)

* Thu Jan 19 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.1-1
- version upgrade

* Sat Jan 14 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
7.0-1
- version upgrade

* Thu Jan 05 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
6.3-1
- version upgrade

* Tue Jan 03 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
6.2-1 
- version upgrade

* Wed Dec 28 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
6.1-1
- version upgrade

* Sun Dec 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
6.0-1
- version upgrade

* Sun Dec 18 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.9-1
- version upgrade

* Fri Nov 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.8-2
- modular xorg integration

* Tue Oct 25 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.8-1
- version upgrade

* Sun Oct 16 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.7-3
- enable frills (#170965)

* Sat Sep 17 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.7-2
- enable iso14755 (#168548)

* Tue Aug 23 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.7-1
- version upgrade

* Sun Jun 05 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.5-3
- add dist

* Thu Jun 02 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.5-2
- minor cleanups

* Thu May 12 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
5.5-1
- Version upgrade (5.5)

* Mon Mar 28 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0:5.3-1
- Version upgrade (5.3)

* Wed Feb 09 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- Initial RPM release.
