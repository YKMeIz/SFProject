Name:		git-extras
Version:	4.1.0
Release:	2%{?dist}
Summary:	Little git extras
Group:		Development/Tools

License:	MIT
URL:		https://github.com/tj/%{name}
Source0:	https://github.com/tj/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	rubygem-ronn
Requires:	bash-completion git

%description
%{name} adds the following extra-commands to git:

alias, archive-file, bug, changelog, commits-since, contrib, count,
create-branch, delete-branch, delete-submodule, delete-tag, effort,
extras, feature, fresh-branch, gh-pages, graft, ignore, info,
local-commits, obliterate, promote, refactor, release, repl, setup,
squash, summary, touch, undo

For more information about the extra-commands, see the included
README.md, HTML, mark-down or man-pages.


%prep
%setup -q
# scripts already use bash
# remove `/usr/bin/env` from hashbang
sed -i -e "s/\/usr\/bin\/.*sh/\/bin\/bash/g" \
	bin/*

%build
# stop ruby split-method compaining about
# `invalid byte sequence in US-ASCII (ArgumentError)`
# by exporting UTF-8 encoding to C-locale.
export LC_CTYPE="en_US.UTF-8"
pushd man
# build manpages and HTML-doc
./manning-up.sh
# replace all (escaped-dots) (\.) with the proper
# escape-sequence for <dot> in manpages (\[char46])
# (rubygem-)ronn doesn't handle this correctly.
sed -ie "s/\\\\\./\\\\\[char46\]/g" *.1
popd


%install
%make_install PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d \
	 html md
install -pm 0644 man/*.html html
install -pm 0644 man/*.md md


%files
%config(noreplace) %{_sysconfdir}/bash_completion.d
%doc AUTHORS History.md Readme.md html/ md/
%license LICENSE
%{_bindir}/*
%{_mandir}/man*/*


%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 4.1.0-1
- Update to 4.1.0 (#1301413)

* Sat Jan 16 2016 Sérgio Basto <sergio@serjux.com> - 4.0.0-1
- Update git-extras to 4.0.0 (#1294644)
- Create unowned directory bash_completion.d and fix make install.
- New upstream source URL.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 16 2015 Sérgio Basto <sergio@serjux.com> - 2.2.0-3
- Readded troublesome URLs solution from
  https://fedoraproject.org/wiki/Packaging:SourceURL#Troublesome_URLs

* Mon Jun 15 2015 Sérgio Basto <sergio@serjux.com> - 2.2.0-2
- Added License tag

* Mon Jun 15 2015 Sérgio Basto <sergio@serjux.com> - 2.2.0-1
- Update to 2.2.0 .
- Drop git-extras-1.9.0_fixes.patch .

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Björn Esser <bjoern.esser@gmail.com> - 1.9.0-1
- new upstream-version

* Mon Jun 10 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.0-3
- nuked `BuildRequires: groff-base`; gets pulled by rubygem-ronn

* Fri Jun 07 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.0-2
- added missing %%{version} in Source0
- added missing %%{name} in `install etc/bash_completion.sh`-line

* Mon Jun 03 2013 Björn Esser <bjoern.esser@gmail.com> - 1.8.0-1
- Initial rpm release
