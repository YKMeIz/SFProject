Summary:        Feature rich, easy to use tag editor
Name:           puddletag
Version:        1.0.5
Release:        1%{?dist}
Group:          Applications/Multimedia
License:        GPLv2 and GPLv3+
URL:            http://puddletag.sourceforge.net
Source0:        http://downloads.sourceforge.net/puddletag/puddletag-%{version}.tar.gz
Patch0:         puddletag-0.10.6-xdg.patch
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
Buildrequires:  desktop-file-utils
Requires:       PyQt4
Requires:       pyparsing >= 1.5.5
Requires:       python-acoustid
Requires:       python-mutagen
Requires:       python-configobj
Requires:       python-musicbrainz2 
#Requires:       quodlibet

%description
Puddletag is an audio tag editor.

Unlike most taggers, it uses a spreadsheet-like layout so that all the
tags you want to edit by hand are visible and easily editable.

The usual tag editor features are supported like extracting tag
information from filenames, renaming files based on their tags by
using patterns (that you define, not crappy, uneditable ones).

Then there're Functions, which can do things like replace text, trim,
change the case of tags, etc. Actions can automate repetitive
tasks. You can import your QuodLibet library, lookup tags using
AcoustID, MusicBrainz, FreeDB or Amazon (though it's only good for
cover art) and more.

Supported formats: ID3v1, ID3v2 (mp3), MP4 (mp4, m4a, etc.),
VorbisComments (ogg, flac), Musepack (mpc), Monkey's Audio (.ape) and
WavPack (wv).

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
chmod 0644 NEWS
sed -i  '/^#![ ]*\/usr\/bin\/env/d' \
    puddlestuff/{webdb,puddlesettings,puddletag,puddleobjects,releasewidget}.py

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc copyright HACKING NEWS README THANKS TODO 
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{python_sitelib}/puddlestuff/
%{python_sitelib}/%{name}-%{version}-py*.egg-info
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Sat Jan 20 2015 Terje Rosten <terje.rosten@ntnu.no> - 1.0.5-1
- 1.0.5

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 03 2014 Terje Rosten <terje.rosten@ntnu.no> - 1.0.3-1
- 1.0.3

* Mon Nov 18 2013 Terje Rosten <terje.rosten@ntnu.no> - 1.0.2-1
- 1.0.2

* Mon Aug 05 2013 Terje Rosten <terje.rosten@ntnu.no> - 1.0.2-0.1.rc1
- 1.0.2RC1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 23 2013 Terje Rosten <terje.rosten@ntnu.no> - 1.0.1-3
- Fix req (bz #895788)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Terje Rosten <terje.rosten@ntnu.no> - 1.0.1-1
- 1.0.1

* Thu Aug 23 2012 Terje Rosten <terje.rosten@ntnu.no> - 1.0.0-1
- 1.0.0

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 07 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.10.6-2
- Fix typo in xdg-open patch

* Tue Jun 14 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.10.6-1
- 0.10.6

* Mon Mar 28 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.10.3-1
- 0.10.3

* Sun Mar 13 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.10.0-1
- 0.10.0

* Mon Feb 28 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.9.12-1
- 0.9.12

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Terje Rosten <terje.rosten@ntnu.no> - 0.9.11-2
- add dep on quodlibet
- add xdg-open patch

* Mon Dec 27 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.9.11-1
- 0.9.11
- fix license
- add comment about py reqs
- add slash to dir in files
- fix typo in description
- remove buildroot tag
- remove define of python macro
- remove python req
- fix sed expression

* Mon Dec  6 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.9.7-1
- 0.9.7

* Thu Oct 21 2010 Terje Rosten <terje.rosten@ntnu.no> - 0.9.6-1
- initial build
