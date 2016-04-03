Name:           youtube-dl
Version:        2014.11.13
Release:        1%{?dist}
Summary:        A small command-line program to download online videos
License:        Public Domain
URL:            https://yt-dl.org
Source0:        https://yt-dl.org/downloads/%{version}/%{name}-%{version}.tar.gz
Source1:        https://yt-dl.org/downloads/%{version}/youtube-dl-%{version}.tar.gz.sig
Source2:        gpgkey-7D33D762FD6C35130481347FDB4B54CBA4826A18.gpg
Source3:        %{name}.conf
BuildRequires:  python2
# Tests failed because of no connection in Koji.
# BuildRequires:  python-nose
Requires:       python
BuildArch:      noarch
# For source verification with gpgv
BuildRequires:  gpg

%description
Small command-line program to download videos from YouTube and other sites.

%prep
gpgv --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%setup -qn %{name}

%build
make %{?_smp_mflags}

%install
%make_install PREFIX=%{_prefix} \
              MANDIR=%{_mandir} \
              PYTHON=%{__python2}
mkdir -p %{buildroot}%{_sysconfdir}
install -pm644 %{S:3} %{buildroot}%{_sysconfdir}

%check
#make test

%files
%doc LICENSE README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/bash_completion.d/%{name}
%exclude %{_sysconfdir}/fish/completions/youtube-dl.fish
%{_datadir}/zsh/site-functions/_youtube-dl

%changelog
* Thu Nov 13 2014 Jon Ciesla <limburgher@gmail.com> - 2014.11.13-1
- Update to latest release.

* Mon Nov 03 2014 Till Maas <opensource@till.name> - 2014.11.02.1-1
- Update to latest release
- Add zsh completion file
- Add GPG key verification

* Tue Sep 23 2014 Till Maas <opensource@till.name> - 2014.09.22.1-1
- Update to latest release
- Exclude fish completion script

* Sun Sep 07 2014 Till Maas <opensource@till.name> - 2014.09.06-1
- Update to 2014-09-06
- Add GPG signature

* Sun Aug 31 2014 Till Maas <opensource@till.name> - 2014.08.29-1
- Update to 2014.08.29

* Tue Jul 29 2014 Christopher Meng <rpm@cicku.me> - 2014.07.25.1-1
- Update to 2014.07.25.1

* Mon Jul 21 2014 Matěj Cepl <mcepl@redhat.com> - 2014.07.20.2-1
- Update to 2014.07.20.2

* Sat Jul 12 2014 Christopher Meng <rpm@cicku.me> - 2014.07.11.3-1
- Update to 2014.07.11.3

* Tue Jun 24 2014 Christopher Meng <rpm@cicku.me> - 2014.06.24.1-1
- Update to 2014.06.24.1

* Mon Jun 09 2014 Christopher Meng <rpm@cicku.me> - 2014.06.07-1
- Update to 2014.06.07

* Tue May 06 2014 Christopher Meng <rpm@cicku.me> - 2014.05.05-1
- Update to 2014.05.05

* Fri Apr 11 2014 Christopher Meng <rpm@cicku.me> - 2014.04.11.1-1
- Update to 2014.04.11.1

* Mon Mar 17 2014 Matěj Cepl <mcepl@redhat.com> - 2014.03.12-1
- Update to 2014.03.12

* Sat Mar 08 2014 Christopher Meng <rpm@cicku.me> - 2014.03.07.1-1
- Update to 2014.03.07.1

* Tue Feb 25 2014 Christopher Meng <rpm@cicku.me> - 2014.02.25-1
- Update to 2014.02.25

* Thu Feb 20 2014 Christopher Meng <rpm@cicku.me> - 2014.02.19.1-1
- Update to 2014.02.19.1

* Tue Feb 11 2014 Christopher Meng <rpm@cicku.me> - 2014.02.10-1
- Update to 2014.02.10

* Fri Feb 07 2014 Christopher Meng <rpm@cicku.me> - 2014.02.06.3-1
- Update to 2014.02.06.3

* Thu Jan 23 2014 Christopher Meng <rpm@cicku.me> - 2014.01.23-1
- Update to 2014.01.23

* Mon Jan 20 2014 Christopher Meng <rpm@cicku.me> - 2014.01.17.2-1
- Update to 2014.01.17.2

* Thu Jan 09 2014 Christopher Meng <rpm@cicku.me> - 2014.01.08-1
- Update to 2014.01.08

* Sat Jan 04 2014 Christopher Meng <rpm@cicku.me> - 2014.01.03-1
- Update to 2014.01.03

* Fri Dec 27 2013 Christopher Meng <rpm@cicku.me> - 2013.12.26-1
- Update to 2013.12.26

* Sun Dec 22 2013 Christopher Meng <rpm@cicku.me> - 2013.12.20-1
- Update to 2013.12.20

* Thu Dec 19 2013 Christopher Meng <rpm@cicku.me> - 2013.12.17.2-1
- Update to 2013.12.17.2

* Tue Dec 03 2013 Christopher Meng <rpm@cicku.me> - 2013.12.09.4-1
- Update to 2013.12.09.4

* Tue Dec 03 2013 Christopher Meng <rpm@cicku.me> - 2013.12.04-1
- Update to 2013.12.04

* Tue Dec 03 2013 Christopher Meng <rpm@cicku.me> - 2013.12.02-1
- Update to 2013.12.02

* Fri Nov 29 2013 Christopher Meng <rpm@cicku.me> - 2013.11.29-1
- Update to 2013.11.29(BZ#1035738)

* Tue Nov 26 2013 Christopher Meng <rpm@cicku.me> - 2013.11.25.3-1
- Update to 2013.11.25.3(BZ#1034138)

* Sun Nov 24 2013 Christopher Meng <rpm@cicku.me> - 2013.11.22.2-1
- Update to 2013.11.22

* Thu Nov 21 2013 Christopher Meng <rpm@cicku.me> - 2013.11.20-1
- Update to 2013.11.20

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 2013.11.19-1
- Update to 2013.11.19

* Mon Nov 18 2013 Christopher Meng <rpm@cicku.me> - 2013.11.18.1-1
- Update to 2013.11.18.1

* Fri Nov 15 2013 Christopher Meng <rpm@cicku.me> - 2013.11.15-1
- Update to 2013.11.15

* Thu Nov 14 2013 Christopher Meng <rpm@cicku.me> - 2013.11.13-1
- Update to 2013.11.13

* Tue Nov 12 2013 Christopher Meng <rpm@cicku.me> - 2013.11.11-1
- Update to 2013.11.11

* Fri Nov 08 2013 Christopher Meng <rpm@cicku.me> - 2013.11.07-1
- Update to 2013.11.07(BZ#1027822)

* Thu Oct 31 2013 Christopher Meng <rpm@cicku.me> - 2013.11.02-1
- Update to 2013.11.02(BZ#1026034)

* Thu Oct 31 2013 Christopher Meng <rpm@cicku.me> - 2013.10.30-1
- Update to 2013.10.30(BZ#1024948)

* Mon Oct 28 2013 Christopher Meng <rpm@cicku.me> - 2013.10.28-1
- Update to 2013.10.28(BZ#1022706)

* Wed Oct 23 2013 Christopher Meng <rpm@cicku.me> - 2013.10.23-1
- Update to 2013.10.23

* Sun Oct 20 2013 Christopher Meng <rpm@cicku.me> - 2013.10.18.2-1
- Update to 2013.10.18.2(BZ#1020787)

* Thu Oct 17 2013 Christopher Meng <rpm@cicku.me> - 2013.10.17-1
- Update to 2013.10.17(BZ#1019694)

* Thu Oct 10 2013 Christopher Meng <rpm@cicku.me> - 2013.10.09-1
- Update to 2013.10.09(BZ#1017630)

* Mon Oct 07 2013 Christopher Meng <rpm@cicku.me> - 2013.10.07-1
- Update to 2013.10.07(BZ#1014266)

* Mon Sep 30 2013 Christopher Meng <rpm@cicku.me> - 2013.09.29-1
- Update to 2013.09.29(BZ#1013394)

* Wed Sep 25 2013 Christopher Meng <rpm@cicku.me> - 2013.09.24.2-1
- Update to 2013.09.24.2(BZ#1011845)

* Sat Sep 21 2013 Christopher Meng <rpm@cicku.me> - 2013.09.20.1-1
- Update to 2013.09.20.1(BZ#1009593)

* Mon Sep 16 2013 Christopher Meng <rpm@cicku.me> - 2013.09.16-1
- Update to 2013.09.16(BZ#1006829)

* Wed Sep 11 2013 Christopher Meng <rpm@cicku.me> - 2013.09.10-1
- Update to 2013.09.10(BZ#1006334)

* Mon Sep 09 2013 Christopher Meng <rpm@cicku.me> - 2013.09.07-1
- Update to 2013.09.07

* Thu Sep 05 2013 Christopher Meng <rpm@cicku.me> - 2013.09.04-1
- Update to 2013.09.04

* Mon Sep 02 2013 Christopher Meng <rpm@cicku.me> - 2013.08.30-1
- Update to 2013.08.30

* Fri Aug 30 2013 Christopher Meng <rpm@cicku.me> - 2013.08.29-1
- Update to 2013.08.29

* Tue Aug 27 2013 Christopher Meng <rpm@cicku.me> - 2013.08.27-1
- Update to 2013.08.27

* Sat Aug 24 2013 Christopher Meng <rpm@cicku.me> - 2013.08.23-1
- Update to 2013.08.23

* Sun Aug 18 2013 Christopher Meng <rpm@cicku.me> - 2013.08.17-1
- Update to 2013.08.17

* Tue Aug 13 2013 Christopher Meng <rpm@cicku.me> - 2013.08.09-1
- Update to 2013.08.09

* Sat Aug 03 2013 Christopher Meng <rpm@cicku.me> - 2013.08.02-1
- Update to 2013.08.02

* Mon Jul 22 2013 Christopher Meng <rpm@cicku.me> - 2013.07.25.2-1
- Update to 2013.07.25.2

* Mon Jul 22 2013 Christopher Meng <rpm@cicku.me> - 2013.07.19-1
- Update to 2013.07.19

* Thu Jul 18 2013 Christopher Meng <rpm@cicku.me> - 2013.07.17.1-1
- Update to 2013.07.17.1

* Tue Jul 16 2013 Christopher Meng <rpm@cicku.me> - 2013.07.12-1
- Update to 2013.07.12

* Thu Jul 11 2013 Christopher Meng <rpm@cicku.me> - 2013.07.10-1
- Update to 2013.07.10

* Tue Jul 02 2013 Christopher Meng <rpm@cicku.me> - 2013.07.02-1
- Update to 2013.07.02
- SPEC cleanup.

* Wed Jun 26 2013 Christopher Meng <rpm@cicku.me> - 2013.06.31-1
- Update to 2013.06.31

* Mon Jun 17 2013 Christopher Meng <rpm@cicku.me> - 2013.05.23-1
- Update to 2013.05.23 and cleanup the spec

* Tue May 14 2013 Christopher Meng <rpm@cicku.me> - 2013.05.14-1
- Update to 2013.05.14

* Wed May 08 2013 Christopher Meng <rpm@cicku.me> - 2013.05.07-1
- Update to 2013.05.07

* Thu Apr 18 2013 Till Maas <opensource@till.name> - 2013.04.18-1
- Update to new release.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2013.01.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Till Maas <opensource@till.name> - 2013.01.13-1
- Update to new release.

* Sun Jan 06 2013 Matěj Cepl <mcepl@redhat.com> - 2013.01.02-1
- Update to new release (fix #880270).

* Tue Oct 23 2012 Till Maas <opensource@till.name> - 2012.10.09-1
- Update to new release.
- Update BR: add pandoc.
- install make target.

* Tue Oct 02 2012 Till Maas <opensource@till.name> - 2012.09.27-3
- Add BR: python >= 2.6.

* Tue Oct 02 2012 Till Maas <opensource@till.name> - 2012.09.27-2
- Use noreplace for config file.
- Add BR: zip.

* Tue Oct  2 2012 Tim Landscheidt <tim@tim-landscheidt.de> - 2012.09.27-1
- Bump Python requirement to 2.6.
- Update to new release and GitHub tarballs.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.02.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 21 2012 Till Maas <opensource@till.name> - 2012.02.27-1
- Update to new release.

* Thu Jan 26 2012 Till Maas <opensource@till.name> - 2011.12.08-3
- Provide --prefer-free-formats in %%{_sysconfdir}/%%{name}.conf (RH #757577)
  (Patch by Jan Kratochvil)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.12.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 10 2011 Till Maas <opensource@till.name> - 2011.12.08-1
- Update to new release.

* Thu Dec 08 2011 Till Maas <opensource@till.name> - 2011.11.23-1
- Update to new release (fixed Red Hat Bug #758679).

* Fri Oct 21 2011 Till Maas <opensource@till.name> - 2011.10.19-1
- Update to latest release.

* Thu Aug 04 2011 Till Maas <opensource@till.name> - 2011.08.04-1
- Update to latest release to adjust to backend changes (Red Hat Bug
  #728378).

* Fri May 13 2011 Till Maas <opensource@till.name> - 2011.03.29-1
- Update to latest release.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.01.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 Till Maas <opensource@till.name> - 2010.01.30-1
- Update to latest release.

* Sun Dec 12 2010 Till Maas <opensource@till.name> - 2010.12.09-1
- Update to latest release to adjust with youtube changes.

* Sat Nov 06 2010 Till Maas <opensource@till.name> - 2010.10.24-1
- Update to latest release.
- Adjust to new upstream location at github instead of bitbucket.
- add -p to install.
- remove index.html

* Thu Oct 07 2010 Till Maas <opensource@till.name> - 2010.10.03-1
- Update to latest release.

* Thu Aug 05 2010 Till Maas <opensource@till.name> - 2010.08.04-1
- Update to latest release.

* Fri Jul 23 2010 Till Maas <opensource@till.name> - 2010.07.22-1
- Update to latest release.

* Thu Jul 15 2010 Till Maas <opensource@till.name> - 2010.07.14-1
- Update to latest release.

* Mon Jun 07 2010 Till Maas <opensource@till.name> - 2010.06.06-1
- Update to latest release.

* Thu Apr 29 2010 Till Maas <opensource@till.name> - 2010.04.04-1
- Update to latest release to fix some download issues RH #582372.

* Fri Oct 09 2009 Rafał Psota <rafalzaq@gmail.com> - 2009.09.13-2
- Small fix in %%prep.

* Sun Sep 27 2009 Rafał Psota <rafalzaq@gmail.com> - 2009.09.13-1
- Update to 2009.09.13.
- License change to Public Domain.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008.01.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2008.01.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 26 2008 Krzysztof Kurzawski <kurzawax at gmail.com> 2008.01.24-1
- Update to v2008.01.24
- Add polish summary and description.

* Wed Jan 02 2008 Krzysztof Kurzawski <kurzawax at gmail.com> 2007.10.12-5
- Correct install.
- Correct documentation.

* Sat Dec 29 2007 Krzysztof Kurzawski <kurzawax at gmail.com> 2007.10.12-4
- Correct requires.
- Add documentation.

* Sun Dec 23 2007 Krzysztof Kurzawski <kurzawax at gmail.com> 2007.10.12-3
- Correct version tag.

* Fri Dec 14 2007 Krzysztof Kurzawski <kurzawax at gmail.com> 1-2
- Update to v2007.10.12, correct license and update summary.

* Sun Dec 9 2007 Krzysztof Kurzawski <kurzawax at gmail.com> 1-1
- First release.
