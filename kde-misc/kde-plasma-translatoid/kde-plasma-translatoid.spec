Name:           kde-plasma-translatoid
Version:        1.30
Release:        11.svn01092011%{?dist}
Summary:        Translator Using Google Translator

Group:          User Interface/Desktops
License:        GPLv2
URL:            http://www.kde-look.org/content/show.php/translatoid?content=97511
Source0:        http://kde-look.org/CONTENT/content-files/97511-translatoid-%{version}.svn01092011.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gettext
BuildRequires:  kdelibs4-devel
BuildRequires:  pkgconfig(QJson)

Requires: kde-runtime%{?_kde4_version: >= %{_kde4_version}}

%description
Translator plasmoid using Google Translator.


%prep
%setup -qn translatoid-%{version}

chmod 644 README


%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# unpackaged files
rm -fv %{buildroot}%{_datadir}/kde4/apps/cmake/modules/FindQJSON.cmake


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%files
%doc README licence.txt
%{_kde4_libdir}/kde4/plasma_applet_translatoid.so
%{_kde4_datadir}/kde4/services/plasma-applet-translatoid.desktop
%{_kde4_appsdir}/translatoid/
%{_kde4_iconsdir}/hicolor/*/apps/*
# this almost certainly ought to be a private app resource -- rex
%{_kde4_iconsdir}/kbflags/


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-11.svn01092011
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-10.svn01092011
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-9.svn01092011
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Rex Dieter <rdieter@fedoraproject.org> 1.30-8.svn01092011
- rebuild (qjson)

* Sat Nov 24 2012 Rex Dieter <rdieter@fedoraproject.org> 1.30-7.svn01092011
- rebuild (qjson)

* Thu Aug 09 2012 Rex Dieter <rdieter@fedoraproject.org> 1.30-6.svn01092011
- give some packaging love

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-5.svn01092011
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-4.svn01092011
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.30-3.svn01092011
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Eli Wapniarski <eli@orbsky.homelinux.org> 1.30
-1.30-2.svn01092011
- Fix for new Google Api.

* Sun Jun 13 2010 Eli Wapniarski <eli@orbsky.homelinux.org> 1.30
-1.30
- Version upgrade
- Correct Json parser with new Google Api.

* Sun Jun 13 2010 Eli Wapniarski <eli@orbsky.homelinux.org> 1.21
-1.21
- Correct text color in remind area

* Sun Jun 6 2010 Eli Wapniarski <eli@orbsky.homelinux.org> 1.20
-1.20
- Fixed versioning

* Sun Jun 6 2010 Eli Wapniarski <eli@orbsky.homelinux.org> 1.2
-1.2
- Correct Html rending
-1.12
- fix Icon installation

* Thu Feb 26 2010 Eli Wapniarski <eli@orbsky.homelinux.org> 1.1.90_20100122svn
-1.1.90
- Additonal bug fix enabling tranlation of more than 1 sentence

* Thu Jan 22 2010 Eli Wapniarski <eli@orbsky.homelinux.org> 1.1.90_20100122svn
-1.1.90
-  Remove trailing </hr> tag in KDE 4.4
-  Fix enabling translation of more than one sentence
-  Corrected listing of Requirments in SPEC file

* Tue Dec 22 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 1.1
-1.1
- 1.1beta - MAJOR CORRECTION
-   Now Translatoid use extender
-   Add Reminder extender to remind you some word after clicking on the star
-   Replace parsing by Json parsing. YOU NEED TO INSTALL libqjson
-   Clear some code and probably add some new bug.. :)
-   If you have some probs, contact me!
-1.1
-  Add new language
-  Afrikaans
-  Albanais
-  Albanais
-  Belarusian
-  Irish
-  Icelandic
-  Macedonian
-  Malaysia
-  Maltese
-  Persan
-  Swahili
-  Turkish

* Fri Aug 7 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 1.0-1
-1.0
- Build Requirement Changed from kdebase-workspace-devel >= 4.2.0
-     to 4.3.0
- Change icon
- Change a lot by aseigo , use KJob, nice animation during translate.
- change the structure of translatoid
- Will remove voice button, because KTTSD do the same job.
- Add estonishlanguage
- Set text color with theme color
- save your automaticaly last languages in use.


* Wed Feb 25 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.9-1
-0.9
- Add new flags list ! Use a plasma::treeview with a QAbstractModel
- copy from the clipboard! Now, you just have to select a source
- text from anywhere, and active the popup, by cliking on the popup,
- or by a plasma shortcut.
- Change QTextEdit source event. Now, press Enter to translate,
- and press Shift+Enter to add a new line.
-0.8
- IMPORTANT RELEASE :
- change the algorithm of source translation. Now it use Post Method.
- It means that you can translate big text. And if you type 1 word,
-it get you the dictionnary result
- Thanks lexnewton.
-0.7 
- add New popup icon which can change his flags
- use KConfigGroup for save favorite language
- add FavoriteLanguage config dialog
- some update of the code
-0.6.1
- Add new Icon
- change name : translatoid to plasma-applet-translatoid

* Wed Feb 25 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6-2
-Fix Build Requirement

* Wed Feb 25 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.6-1
-Removed patch that builds the package without flags.They are not need.
-AutoPaste the copy selection and autotranslate when you active Popup.
-GrabKeyboard when you active Popup
-Add "Clear Button"
-remove Cancel Button from DialogBox
-Add Po language file. 
- Change inverse language icon
- Add Fedora Package without flags

* Fri Feb 13 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.5-1
- Update to Version 0.5
- Update allows translated text to be spoken.

* Mon Feb 08 2009 Jaroslav Reznik <jreznik@redhat.com> 0.4.1-6
- Finally correct one URL
- Description clarification

* Fri Feb 06 2009 Jaroslav Reznik <jreznik@redhat.com> 0.4.1-5
- Fixed URL
- Country flags removed

* Mon Feb 02 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.4.1-4
- Added command to remove non Fedora GCC compilation flags

* Mon Feb 02 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.4.1-3
- Corrected reference to Google as per Fedora's Guidelines

* Mon Feb 02 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.4.1-2
- Corrected Name of SPEC File
- Corrected packaging errors

* Mon Feb 02 2009 Eli Wapniarski <eli@orbsky.homelinux.org> 0.4.1-1
- Initial package
