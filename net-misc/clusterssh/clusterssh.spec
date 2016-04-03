Name:          clusterssh
Version:       3.28
Release:       8%{?dist}
Summary:       Secure concurrent multiple server terminal control

Group:         Applications/Productivity
License:       GPLv2+
URL:           http://clusterssh.sourceforge.net
Source0:       http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildArch:     noarch
BuildRequires: desktop-file-utils perl-Pod-Checker
Requires:      xterm

%description
Control multiple terminals open on different servers to perform administration
tasks, for example multiple hosts requiring the same configuration within a 
cluster. Not limited to use with clusters, however.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        %{name}.desktop
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
install -p -m 644 %{name}-48x48.png \
        %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/
install -p -m 644 %{name}-32x32.png \
        %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/
install -p -m 644 %{name}-24x24.png \
        %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc COPYING AUTHORS README NEWS THANKS ChangeLog
%{_bindir}/cssh
%{_mandir}/man1/*.1*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Fri Feb 15 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 3.28-8
- add perl-Pod-Checker as BR to fix the build failure
- podchecker has moved from perl-Pod-Parser to above package

* Fri Feb 15 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 3.28-7
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 17 2010 Filipe Rosset <filiperosset@fedoraproject.org> - 3.28-2
- Updated to upstream version 3.28

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Patrick "Jima" Laughton <jima@beer.tclug.org> 3.26-1
- Much newer upstream version
- Add dependency on xterm (BZ#506909)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 24 2008 Patrick "Jima" Laughton <jima@beer.tclug.org> 3.22-1
- New upstream version

* Tue Sep 18 2007 Patrick "Jima" Laughton <jima@beer.tclug.org> 3.19.1-3
- License clarification
- Switch back to unmodified, upstream-provided tarball

* Tue Aug 15 2006 Duncan Ferguson <duncan_ferguson@users.sf.net> - 3.19.1-2
- Tidyups as per https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=199173

* Mon Jul 24 2006 Duncan Ferguson <duncan_ferguson@users.sf.net> - 3.19.1-1
- Update Changelog, commit all branch changes and release

* Tue Jul 18 2006 Duncan Ferguson <duncan_ferguson@users.sf.net> - 3.18.2.10-2
- Correct download URL (Source0)

* Mon Jul 17 2006 Duncan Ferguson <duncan_ferguson@users.sf.net> - 3.18.2.10-1
- Lots of amendments and fixes to clusterssh code
- Added icons and desktop file
- Submitted to Fedora Extras for review

* Mon Nov 28 2005 Duncan Ferguson <duncan_ferguson@users.sf.net> - 3.18.1-1
- Updates and bugfixes to cssh
- Updates to man page
- Re-engineer spec file

* Tue Aug 30 2005 Duncan Ferguson <duncan_ferguson@users.sf.net> - 3.17.1-2
- spec file tidyups

* Mon Apr 25 2005 Duncan Ferguson <duncan_ferguson@users.sf.net> - 3.0
- Please see ChangeLog in documentation area

