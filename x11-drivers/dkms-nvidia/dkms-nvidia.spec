%global debug_package %{nil}
%global dkms_name nvidia

Name:           dkms-%{dkms_name}
Version:        352.79
Release:        1%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          2
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
# Package is not noarch as it contains pre-compiled binary code
ExclusiveArch:  %{ix86} x86_64 armv7hl

Source0:        %{dkms_name}-kmod-%{version}-i386.tar.xz
Source1:        %{dkms_name}-kmod-%{version}-x86_64.tar.xz
Source2:        %{dkms_name}-kmod-%{version}-armv7hl.tar.xz
Source3:        %{name}-multi.conf

BuildRequires:  sed

Provides:       %{dkms_name}-kmod = %{?epoch}:%{version}
Requires:       %{dkms_name}-driver = %{?epoch}:%{version}
Requires:       dkms

%description
This package provides the proprietary Nvidia kernel driver modules.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

To generate the multiple kernel modules variant, copy the DKMS configuration
file %{_usrsrc}/%{dkms_name}-%{version}/%{name}-multi.conf to %{_sysconfdir}/dkms/%{dkms_name}.conf
and rebuild the modules.

%prep
%ifarch %{ix86}
%setup -q -n %{dkms_name}-kmod-%{version}-i386
%endif

%ifarch x86_64
%setup -q -T -b 1 -n %{dkms_name}-kmod-%{version}-x86_64
%endif

%ifarch armv7hl
%setup -q -T -b 2 -n %{dkms_name}-kmod-%{version}-armv7hl
%endif

%ifnarch %{ix86}
cat kernel/uvm/dkms.conf.fragment >> kernel/dkms.conf
%endif

cp %{SOURCE3} kernel/

%build

%install
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr kernel/* %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}

%changelog
* Tue Jan 26 2016 Simone Caronni <negativo17@gmail.com> - 2:352.79-1
- Update to 352.79.

* Wed Dec 23 2015 Simone Caronni <negativo17@gmail.com> - 2:352.63-2
- Adjust DKMS config file for kernel source detection (thanks Daniel Miranda).

* Wed Nov 18 2015 Simone Caronni <negativo17@gmail.com> - 2:352.63-1
- Update to 352.63.

* Tue Oct 20 2015 Simone Caronni <negativo17@gmail.com> - 2:352.55-1
- Update to 352.55.

* Fri Aug 28 2015 Simone Caronni <negativo17@gmail.com> - 2:352.41-1
- Update to 352.41.

* Wed Jul 29 2015 Simone Caronni <negativo17@gmail.com> - 2:352.30-1
- Update to 352.30.

* Wed Jun 17 2015 Simone Caronni <negativo17@gmail.com> - 2:352.21-1
- Update to 352.21.

* Tue May 19 2015 Simone Caronni <negativo17@gmail.com> - 2:352.09-1
- Update to 352.09.

* Wed May 13 2015 Simone Caronni <negativo17@gmail.com> - 2:346.72-1
- Update to 346.72.

* Tue Apr 07 2015 Simone Caronni <negativo17@gmail.com> - 2:346.59-1
- Update to 346.59.
- Removed unused patch.

* Thu Mar 12 2015 Simone Caronni <negativo17@gmail.com> - 2:346.47-2
- Add patch for kernel 4.0.

* Wed Feb 25 2015 Simone Caronni <negativo17@gmail.com> - 2:346.47-1
- Update to 346.47.
- Removed upstream patch.

* Thu Jan 29 2015 Simone Caronni <negativo17@gmail.com> - 2:346.35-2
- Add kernel patch for 3.18.

* Sat Jan 17 2015 Simone Caronni <negativo17@gmail.com> - 2:346.35-1
- Update to 346.35.

* Tue Dec 09 2014 Simone Caronni <negativo17@gmail.com> - 2:346.22-1
- Update to 346.22.

* Fri Nov 14 2014 Simone Caronni <negativo17@gmail.com> - 2:346.16-1
- Update to 346.16.
- UVM kernel module is gone on i*86.

* Wed Oct 01 2014 Simone Caronni <negativo17@gmail.com> - 2:343.22-2
- Attempt building not only if Xen is enabled but also if RT is.

* Mon Sep 22 2014 Simone Caronni <negativo17@gmail.com> - 2:343.22-1
- Update to 343.22.

* Thu Aug 07 2014 Simone Caronni <negativo17@gmail.com> - 2:343.13-1
- Update to 343.13.

* Tue Jul 08 2014 Simone Caronni <negativo17@gmail.com> - 2:340.24-1
- Update to 340.24.

* Mon Jun 09 2014 Simone Caronni <negativo17@gmail.com> - 2:340.17-1
- Update to 340.17.

* Mon Jun 02 2014 Simone Caronni <negativo17@gmail.com> - 2:337.25-1
- Update to 337.25.

* Tue May 06 2014 Simone Caronni <negativo17@gmail.com> - 2:337.19-1
- Update to 337.19.

* Tue Apr 08 2014 Simone Caronni <negativo17@gmail.com> - 2:337.12-1
- Update to 337.12.

* Tue Mar 04 2014 Simone Caronni <negativo17@gmail.com> - 2:334.21-1
- Update to 334.21, update patch.

* Tue Feb 18 2014 Simone Caronni <negativo17@gmail.com> - 2:334.16-2
- Add kernel 3.14 patch.

* Sat Feb 08 2014 Simone Caronni <negativo17@gmail.com> - 2:334.16-1
- Update to 334.16.

* Tue Jan 14 2014 Simone Caronni <negativo17@gmail.com> - 2:331.38-1
- Update to 331.38.
- Create separate DKMS configuration file for multiple kernel modules.

* Tue Dec 03 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-3
- Move kernel modules under /kernel/drivers/video as the original Nvidia DKMS
  settings.

* Wed Nov 13 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-2
- Fix version in dkms.conf file.

* Thu Nov 07 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-1
- Update to 331.20.
- Removed upstreamed patch.

* Mon Nov 04 2013 Simone Caronni <negativo17@gmail.com> - 2:331.17-1
- Updated to 331.17.
- Use official patch from Nvidia for 3.11+ kernels.
- Added support for multiple kernel modules along with single one. The single
  one is loaded by default by X.org (typical desktop usage). For all other CUDA
  specific settings the separate modules can be loaded.

* Fri Oct 04 2013 Simone Caronni <negativo17@gmail.com> - 2:331.13-1
- Update to 331.13.

* Mon Sep 09 2013 Simone Caronni <negativo17@gmail.com> - 2:325.15-1
- Update to 325.15.

* Wed Aug 21 2013 Simone Caronni <negativo17@gmail.com> - 2:319.49-1
- Updated to 319.49.
- Remove RHEL 5 tags.
- Remove patch for kernel 3.10, add patch for kernel 3.11.

* Mon Jul 29 2013 Simone Caronni <negativo17@gmail.com> - 2:319.32-3
- Add patch for kernel 3.10.

* Wed Jul 03 2013 Simone Caronni <negativo17@gmail.com> - 2:319.32-2
- Add armv7hl support.

* Fri May 24 2013 Simone Caronni <negativo17@gmail.com> - 1:319.32-1
- Update to 319.32.
