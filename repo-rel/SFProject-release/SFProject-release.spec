Summary: SFProject Repo release file
Name: SFProject-release
Version: 0.2
Release: 2%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://sfproject.org/

Source0: SFProject.repo
Source1: RPM-GPG-KEY-el7-SFProject

BuildArch: noarch

Requires: epel-release

%description
This package contains yum/dnf configuration for the SFProject Repository, and the public GPG keys used to sign packages.

%prep
%setup -c -T
%{__cp} -a %{SOURCE1} .

# %build

%install
%{__rm} -rf %{buildroot}
%{__install} -Dpm 0644 %{SOURCE0} %{buildroot}%{_sysconfdir}/yum.repos.d/SFProject.repo
%{__install} -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-el7-SFProject

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%pubkey RPM-GPG-KEY-el7-SFProject
%dir %{_sysconfdir}/yum.repos.d/
%{_sysconfdir}/yum.repos.d/SFProject.repo
%dir %{_sysconfdir}/pki/rpm-gpg/
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-el7-SFProject

%changelog
* Sat Apr 2 2016  Néil Ge <neil@gyz.io> - 0.2-2
- Add repo "debug" and "source".

* Wed Mar 30 2016  Néil Ge <neil@gyz.io> - 0.2-1
- Add repo "extra".

* Wed Mar 30 2016  Néil Ge <neil@gyz.io> - 0.1-2
- Fix "Bad id for repo".

* Tue Mar 29 2016  Néil Ge <neil@gyz.io> - 0.1-1
- Initial release.
