Name:           docker-storage-setup
Version:        0.5
Release:        3%{?dist}
Summary:        A simple service to setup docker storage devices

License:        ASL 2.0
URL:            http://github.com/projectatomic/docker-storage-setup/
# Created by `git archive`
Source0:        %{name}-%{version}.tar.xz

BuildArch:      noarch
BuildRequires:  pkgconfig(systemd)

Requires:       lvm2
Requires:       systemd-units
Requires:       xfsprogs
# systemd_requires macro doesn't work here because the srpm build fails?
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
This is a simple service to configure Docker to use an LVM-managed
thin pool.  It also supports auto-growing both the pool as well
as the root logical volume and partition table. 

%prep
%setup -q

%build

%install
install -d %{buildroot}%{_bindir}
install -p -m 755 docker-storage-setup.sh %{buildroot}%{_bindir}/docker-storage-setup
install -d %{buildroot}%{_unitdir}
install -p -m 644 docker-storage-setup.service %{buildroot}%{_unitdir}
install -d %{buildroot}%{_prefix}/lib/docker-storage-setup/
install -p -m 644 docker-storage-setup.conf %{buildroot}%{_prefix}/lib/docker-storage-setup/docker-storage-setup

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%{_unitdir}/docker-storage-setup.service
%{_bindir}/docker-storage-setup
%{_prefix}/lib/docker-storage-setup/docker-storage-setup

%changelog
* Fri May 22 2015 Colin Walters <walters@redhat.com> - 0.5-3
- The conf file actually goes in /usr/lib/ always,
  because this is a noarch package.

* Fri May 22 2015 Colin Walters <walters@redhat.com> - 0.5-2
- New upstream release
- Drop requirement on cloud-utils-growpart; anyone who wants this
  functionality must install it manually

* Fri Apr 17 2015 Colin Walters <walters@redhat.com> - 0.0.4-4
- Merge https://github.com/projectatomic/docker-storage-setup/pull/8
  Add requirement on xfsprogs (Jason DeTiberus)

* Tue Jan 20 2015 Colin Walters <walters@redhat.com> - 0.0.4-2
- On new installs, use an LVM managed thin pool by default,
  increasing efficiency.  (Vivek Goyal)

* Wed Oct 29 2014 Andy Grimm <agrimm@redhat.com> - 0.0.3-1
- Initial build

