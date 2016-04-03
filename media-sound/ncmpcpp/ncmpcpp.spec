Name:           ncmpcpp
Version:        0.5.10
Release:        3%{?dist}
Summary:        Clone of ncmpc with new features and written in C++
Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://unkart.ovh.org/ncmpcpp
Source0:        http://unkart.ovh.org/ncmpcpp/%{name}-%{version}.tar.bz2

BuildRequires:  curl-devel
BuildRequires:  taglib-devel
BuildRequires:  ncurses-devel
BuildRequires:  libmpdclient-devel


%description
Ncmpcpp is almost exact clone of ncmpc but it contains some new 
features ncmpc doesn't have. It's been also rewritten from scratch 
in C++. New features include: tag editor, playlists editor, easy to 
use search screen, media library screen, lyrics screen and more.


%prep
%setup -q


%build
%configure --disable-static --enable-clock --with-taglib --with-curl --enable-visualizer  --enable-outputs
make %{?_smp_mflags}


%install

make DESTDIR="%{buildroot}" INSTALL="install -p" docdir="%{_docdir}/%{name}-%{version}" install


%files
%defattr(-,root,root,-)
%doc doc/config doc/keys AUTHORS NEWS COPYING
%{_bindir}/ncmpcpp
%{_mandir}/man1/%{name}*


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 02 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 0.5.10-1
- New upstream release: ncmpcpp 0.5.10

* Thu Mar 29 2012 Dominic Hopf <dmaphy@fedoraproject.org> - 0.5.9-1
- New upstream release: ncmpcpp 0.5.9

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 15 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.5.8-1
- New upstream release: ncmpcpp 0.5.8

* Mon Jun 13 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.5.7-1
- New upstream release: ncmpcpp 0.5.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 07 2011 Dominic Hopf <dmaphy@fedoraproject.org> - 0.5.6-1
- New upstream release: ncmpcpp 0.5.6

* Tue Jun 08 2010 Rahul Sundaram <sundaram@fedoraproject.org> - 0.5.4-1
- update to 0.5.4
- enable visualizer option. Resolves rhbz#593205
- enable outputs screen
- update spec to match current guidelines

* Sat Feb 27 2010 Michal Nowak <mnowak@redhat.com> - 0.5.2-1
- 0.5.2

* Wed Jan  6 2010 Michal Nowak <mnowak@redhat.com> - 0.5-1
- 0.5
- dependency on libmpdclient (version 2.1+)

* Mon Oct  5 2009 Michal Nowak <mnowak@redhat.com> - 0.4.1-1
- 0.4.1

* Fri Sep 11 2009 Michal Nowak <mnowak@redhat.com> - 0.4-1
- 0.4

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Michal Nowak <mnowak@redhat.com> - 0.3.5-1
- 0.3.5
- new feature: custom command execution on song change
- new feature: allow for physical files and directories deletion
- new feature: add local directories recursively
- new feature: add random songs to playlist
- new feature: mouse support
- new screen: outputs
- text scrolling in header was made optional
- some bugfixes

* Sat Jun 13 2009 Michal Nowak <mnowak@redhat.com> - 0.3.4-1
- 0.3.4

* Mon Apr 06 2009 Michal Nowak <mnowak@redhat.com> - 0.3.3-1
- dumped ncmpcpp-0.3.2-charset.patch -- upstream already 
- 0.3.3

* Wed Mar 18 2009 Michal Nowak <mnowak@redhat.com> - 0.3.2-1
- 0.3.2
- added ncmpcpp man page

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Michal Nowak <mnowak@redhat.com> 0.3.1-1
- 0.3.1

* Tue Feb  3 2009 Michal Nowak <mnowak@redhat.com> 0.3-1
- 0.3
- enable clock

* Thu Jan 15 2009 Michal Nowak <mnowak@redhat.com> 0.2.5-4
- disable building static archives

* Tue Jan 13 2009 Michal Nowak <mnowak@redhat.com> 0.2.5-3
- minor SPEC file changes

* Thu Dec 11 2008 Michal Nowak <mnowak@redhat.com> 0.2.5-2
- added ncurses-devel as BuildRequires

* Tue Dec  9 2008 Michal Nowak <mnowak@redhat.com> 0.2.5-1
- 0.2.5

