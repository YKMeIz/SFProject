Name:           homebank
Version:        5.0.0
Release:        1%{?dist}
Summary:        Free easy personal accounting for all  

Group:          Applications/Productivity
License:        GPLv2+
URL:            http://homebank.free.fr
Source0:        http://homebank.free.fr/public/%{name}-%{version}.tar.gz
BuildRequires:  gtk3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  perl(XML::Parser)
BuildRequires:  gettext
BuildRequires:  libofx-devel
BuildRequires:  cairo-devel
BuildRequires:  atk-devel
BuildRequires:  intltool

%description
HomeBank is the free software you have always wanted to manage your personal
accounts at home. The main concept is to be light, simple and very easy to use.
It brings you many features that allows you to analyze your finances in a
detailed way instantly and dynamically with powerful report tools based on
filtering and graphical charts.

%package doc
Summary: Documentation files for homebank
Group: Applications/Productivity
Requires: %{name} = %{version}-%{release}
%description doc
Documentation files for homebank


%prep
%setup -q
chmod -x NEWS
chmod -x ChangeLog
chmod -x README
chmod -x AUTHORS
chmod -x COPYING
chmod -x doc/TODO
chmod -x src/*.*

%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install                                    \
        --delete-original                               \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --mode 0644                                     \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
%find_lang %{name}


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ]; then
touch --no-create %{_datadir}/icons/hicolor &>/dev/null
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &> /dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/images
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/datas
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/mime-info/%{name}.*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/application-registry/%{name}.applications

%files doc
%doc doc/TODO
%{_datadir}/%{name}/help

%changelog
* Sat Feb 21 2015 Filipe Rosset <rosset.filipe@gmail.com> - 5.0.0-1
- Rebuilt for new upstream version 5.0.0, fixes rhbz #1190745

* Thu Oct 02 2014 Rex Dieter <rdieter@fedoraproject.org> 4.6.3-3
- update icon/mime scriptlets

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Filipe Rosset <rosset.filipe@gmail.com> - 4.6.3-1
- Rebuilt for new upstream version 4.6.3, list of fixed bugs http://homebank.free.fr/ChangeLog

* Sun Jul 27 2014 Filipe Rosset <rosset.filipe@gmail.com> - 4.6.2-1
- Rebuilt for new upstream version 4.6.2, list of fixed bugs http://homebank.free.fr/ChangeLog

* Thu Jun 26 2014 Filipe Rosset <rosset.filipe@gmail.com> - 4.6.1-1
- Rebuilt for new upstream version 4.6.1

* Mon Jun 23 2014 Filipe Rosset <rosset.filipe@gmail.com> - 4.6-1
- Rebuilt for new upstream version 4.6, spec cleanup

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 03 2014 Filipe Rosset <rosset.filipe@gmail.com> - 4.5.6-1
- New upstream version 4.5.6, fix rhbz #1071915 and spec cleanup

* Wed Feb 19 2014 Filipe Rosset <rosset.filipe@gmail.com> - 4.5.5-1
- New upstream version 4.5.5

* Thu Nov 14 2013 Filipe Rosset <rosset.filipe@gmail.com> - 4.5.4-1
- New upstream version 4.5.4
- Fixes bz #1009081 and bz #1014951

* Mon Sep 23 2013 Bill Nottingham <notting@redhat.com> - 4.5-3
- Rebuild against new libofx

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Filipe Rosset <rosset.filipe@gmail.com> - 4.5-1
- Upgraded to upstream version 4.5

* Wed Apr 24 2013 Jon Ciesla <limburgher@gmail.com> - 4.4-7
- Drop desktop vendor tag.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Bill Nottingham <notting@redhat.com> - 4.4-4
- rebuild for libofx ABI bump

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 4.4-2
- Rebuild for new libpng

* Sun May 01 2011 Filipe Rosset <rosset.filipe@gmail.com> - 4.4-1
- Upgraded to upstream version 4.4
- This build include the fix for https://bugs.launchpad.net/homebank/+bug/695790

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 31 2010 Filipe Rosset <rosset.filipe@gmail.com> - 4.3-2
- Enabled deprecated gtk to build on Fedora 15 Rawhide
- Opened bug report upstream https://bugs.launchpad.net/homebank/+bug/695790

* Thu Jul 15 2010 Johan Cwiklinski <johan AT x-tnd DOT be> - 4.3-1
- 4.3

* Sat Mar 06 2010 Johan Cwiklinski <johan AT x-tnd DOT be> - 4.2.1-1
- 4.2.1
- Remove dso link patch (fixed upstream)

* Fri Feb 12 2010 Johan Cwiklinski <johan AT x-tnd DOT be> - 4.2-2
- Fix DSO link bug

* Thu Feb 11 2010 Johan Cwiklinski <johan AT x-tnd DOT be> - 4.2-1
- 4.2

* Fri Jan 01 2010 Johan Cwiklinski <johan AT x-tnd DOT be> - 4.1-1
- 4.1
