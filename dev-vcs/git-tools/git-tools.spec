%global commit d6d55b3200d2f066683438bf742c5adc24b11f2a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           git-tools
Version:        0
Release:        0.2.20160313git%{shortcommit}%{?dist}
Summary:        Assorted git-related scripts and tools

License:        GPLv3+
Group:          Development/Tools
URL:            https://github.com/MestreLion/%{name}
Source0:        https://github.com/MestreLion/%{name}/archive/%{commit}.tar.gz#/%{name}-%{shortcommit}.tar.gz

BuildArch:      noarch

Requires:       git python

%description
Assorted git-related scripts and tools:

git-branches-rename:
Batch renames branches with a matching prefix to another prefix

git-clone-subset:
Clones a subset of a git repository

git-find-uncommitted-repos:
Recursively list repos with uncommitted changes

git-rebase-theirs:
Resolve rebase conflicts and failed cherry-picks by favoring 'theirs' version

git-restore-mtime:
Restore original modification time of files based on the date of the most
recent commit that modified them

git-strip-merge:
A git-merge wrapper that deletes files on a "foreign" branch before merging

%prep
%setup -qn %{name}-%{commit}

%build

%install
mkdir -p %{buildroot}%{_bindir}
cp -p git-branches-rename %{buildroot}%{_bindir}/.
cp -p git-clone-subset %{buildroot}%{_bindir}/.
cp -p git-find-uncommitted-repos %{buildroot}%{_bindir}/.
cp -p git-rebase-theirs %{buildroot}%{_bindir}/.
cp -p git-restore-mtime %{buildroot}%{_bindir}/.
cp -p git-strip-merge %{buildroot}%{_bindir}/.
mkdir -p %{buildroot}%{_mandir}/man1
cp -p man1/git-* %{buildroot}%{_mandir}/man1/.

%files
%license gpl-3.0.txt
%doc README.md
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Sun Mar 13 2016 Greg Bailey <gbailey@lxpro.com> - 0-0.2.20160313gitd6d55b3
- New upstream snapshot with GPLv3 license file
- Remove unnecessary cleanup of buildroot
- Only copy and package the scripts that have manpages

* Mon Feb 15 2016 Greg Bailey <gbailey@lxpro.com> - 0-0.1.20160215gitea09519
- Initial package
