Name:		fvwm
Version:	2.6.5
Release:	9%{?dist}
Summary:	Highly configurable multiple virtual desktop window manager

Group:		User Interface/X
License:	GPLv2+
URL:		http://www.fvwm.org/
Source0:	ftp://ftp.fvwm.org/pub/fvwm/version-2/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
# Initially taken from http://www.cl.cam.ac.uk/~pz215/fvwm-scripts/scripts/fvwm-xdg-menu.py
Source2:	fvwm-xdg-menu.py

Patch1:		fvwm-0001-Change-html-viewer-to-xdg-open.patch
Patch2:		fvwm-0002-Use-mimeopen-instead-of-EDITOR.patch
Patch3:		fvwm-0003-Enable-auto-generate-menus-in-the-Setup-Form-config-.patch
# This patch will NEVER be included in the official FVWM and that's why:
#
# https://bugs.gentoo.org/show_bug.cgi?id=411811#c7
# https://github.com/ThomasAdam/fvwm/pull/4#issuecomment-5712410
#
# In short - X-servers other than X.org and Xfree86 doesn't support so many
# mouse buttons so this is a distro-specific patch.
Patch4:		fvwm-0004-Increase-number-of-mouse-buttons-supported.patch
# https://github.com/ThomasAdam/fvwm/issues/5
Patch5:		fvwm-0005-FvwmPager-be-more-careful-with-window-labels.patch
# backported from upstream's CVS
Patch6:		fvwm-0006-Comply-with-Debian-s-hardening-rules.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext libX11-devel libXt-devel libXext-devel libXinerama-devel libXpm-devel
BuildRequires:	libXft-devel libXrender-devel
BuildRequires:	libstroke-devel readline-devel libpng-devel fribidi-devel
BuildRequires:	librsvg2-devel
Requires:	xterm %{_bindir}/mimeopen

# for fvwm-bug
Requires:	%{_sbindir}/sendmail

# for fvwm-menu-headlines
Requires:	xdg-utils

# for fvwm-menu-xlock
Requires:	xlockmore

# for auto-menu generation
Requires:	ImageMagick pyxdg


%description
Fvwm is a window manager for X11. It is designed to
minimize memory consumption, provide a 3D look to window frames,
and implement a virtual desktop.


%prep
%setup -q
%patch1 -p1 -b .xdg-open
%patch2 -p1 -b .mimeopen
%patch3 -p1 -b .menu-generate
%patch4 -p1 -b .more-mouse-buttons
%patch5 -p1 -b .fix_pager
%patch6 -p1 -b .fix_printf_fmt

# Filter out false Perl provides
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(FVWM::.*)\|perl(FvwmCommand)\|perl(General::FileSystem)\|perl(General::Parse)/d'
EOF

%global __perl_provides %{_builddir}/%{name}-%{version}/%{name}-prov
chmod +x %{__perl_provides}


# Filter false requires for old perl(Gtk) and for the above provides
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
  sed -e '/perl(Gtk)\|perl(FVWM::Module::Gtk)\|perl(FVWM::.*)\|perl(FvwmCommand)\|perl(General::FileSystem)\|perl(General::Parse)/d'
EOF

%global __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}


%build
aclocal --force
autoreconf -ivf
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %{name}
%find_lang FvwmScript
%find_lang FvwmTaskBar
cat FvwmScript.lang FvwmTaskBar.lang >> %{name}.lang

# Fedora doesn't have old Gtk Perl
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/perllib/FVWM/Module/Gtk.pm
rm $RPM_BUILD_ROOT%{_libexecdir}/%{name}/%{version}/FvwmGtkDebug

# xsession
install -D -m0644 -p %{SOURCE1} \
	$RPM_BUILD_ROOT%{_datadir}/xsessions/%{name}.desktop

# menus
install -D -m0755 -p %{SOURCE2} \
	$RPM_BUILD_ROOT%{_bindir}/fvwm-xdg-menu


%files -f %{name}.lang
%doc README AUTHORS NEWS ChangeLog COPYING
%{_bindir}/*
%{_libexecdir}/%{name}/
%{_datadir}/%{name}/
%{_mandir}/man1/*
%{_datadir}/xsessions/%{name}.desktop


%changelog
* Sun Nov 16 2014 Peter Lemenkov <lemenkov@gmail.com> - 2.6.5-9
- Fix FTBFS in Rawhide (rhbz #1106311)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.6.5-5
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 18 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.6.5-3
- Fix segfaults in FvwmPager

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.6.5-1
- Ver. 2.6.5

* Thu Apr 19 2012 Peter Lemenkov <lemenkov@gmail.com> - 2.6.4-1
- Ver. 2.6.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.5.30-5
- Rebuild for new libpng

* Sat Mar 05 2011 Peter Lemenkov <lemenkov@gmail.com> - 2.5.30-4
- Fixed FTBFS issue (rhbz #661049)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 12 2010 Adam Goode <adam@spicenitz.org> - 2.5.30-2
- Increase number of mouse buttons (#548534)

* Sun Jul 11 2010 Adam Goode <adam@spicenitz.org> - 2.5.30-1
- New upstream release, many changes, see http://www.fvwm.org/news/

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 30 2008 Adam Goode <adam@spicenitz.org> - 2.5.26-2
- RPM 4.6 fix for patch tag

* Wed Jun  4 2008 Adam Goode <adam@spicenitz.org> - 2.5.26-1
- Upgrade to new release
- Remove module_list patch, fixed in upstream

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 2.5.24-2
- Really fix segfault (#382321)

* Sun Dec  2 2007 Adam Goode <adam@spicenitz.org> - 2.5.24-1
- New upstream release
- Fixes segfault (#382321)

* Tue Oct  2 2007 Adam Goode <adam@spicenitz.org> - 2.5.23-3
- Change htmlview to xdg-open (thanks, Ville Skyttä !)

* Mon Sep 10 2007 Adam Goode <adam@spicenitz.org> - 2.5.23-2
- Don't add gnome-libs-devel to BR (not on ppc64?)

* Mon Sep 10 2007 Adam Goode <adam@spicenitz.org> - 2.5.23-1
- New upstream release

* Tue Aug 21 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-5
- Update license tag
- Rebuild for buildid

* Thu Mar 15 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-4
- Don't patch configure, just patch a few files

* Thu Mar  8 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-3
- Rebuild configure with autoconf >= 2.60 (for datarootdir)
- Filter out local Perl libraries from provides and requires

* Wed Feb 28 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-2
- Shorten description
- Enable auto-generate menus in the Setup Form config generator
- Use htmlview instead of netscape
- Use mimeopen instead of EDITOR
- Add more Requires

* Sun Jan 21 2007 Adam Goode <adam@spicenitz.org> - 2.5.21-1
- New specfile for Fedora
