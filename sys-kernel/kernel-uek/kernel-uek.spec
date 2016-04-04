%define kernel_git_commit 662aa19f86032cc12b39abb102a54cb1695f8cca
%define kernel_git_commit 74c661676446c010ea6f46dab7231d98761d66a5
%global __spec_install_pre %{___build_pre}

# Errors in specfile are causing builds to fail. Adding workarounds.
%define _unpackaged_files_terminate_build       0
%define _missing_doc_files_terminate_build      0

Summary: The Linux kernel

# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%define released_kernel 1
# Versions of various parts

# Polite request for people who spin their own kernel rpms:
# please modify the "buildid" define in a way that identifies
# that the kernel isn't the stock distribution kernel, for example,
# by setting the define to ".local" or ".bz123456"
#
# % define buildid .local

%define distro_build 0
%define signmodules 1

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 2.6.22-rc7-git1 starts with a 2.6.21 base,
# which yields a base_sublevel of 21.
%define base_sublevel 12

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%define stable_update 0
# Is it a -stable RC?
%define stable_rc 0
# Set rpm version accordingly
%if 0%{?stable_update}
%define stablerev .%{stable_update}
%define stable_base %{stable_update}
%if 0%{?stable_rc}
# stable RCs are incremental patches, so we need the previous stable patch
%define stable_base %(echo $((%{stable_update} - 1)))
%endif
%endif
%define rpmversion 4.1.12

## The not-released-kernel case ##
%else
# The next upstream release sublevel (base_sublevel+1)
%define upstream_sublevel %(echo $((%{base_sublevel} + 1)))
# The rc snapshot level
%define rcrev 0
# The git snapshot level
%define gitrev 0
# Set rpm version accordingly
%define rpmversion 4.1.%{upstream_sublevel}
%endif
# Nb: The above rcrev and gitrev values automagically define Patch00 and Patch01 below.

# What parts do we want to build?  We must build at least one kernel.
# These are the kernels that are built IF the architecture allows it.
# All should default to 1 (enabled) and be flipped to 0 (disabled)
# by later arch-specific checks.

# The following build options are enabled by default.
# Use either --without <opt> in your rpmbuild command or force values
# to 0 in here to disable them.
#
# standard kernel
%define with_up        1
# kernel-smp (only valid for ppc 32-bit, sparc64)
%define with_smp       1
# kernel-kdump
%define with_kdump     0
# kernel-debug
%define with_debug     1
# kernel-doc
%define with_doc       1
# kernel-headers
%define with_headers   0
# dtrace
%define with_dtrace    0
# kernel-firmware
%define with_firmware  0
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo: 0} %{?!_without_debuginfo: 1}
# kernel-bootwrapper (for creating zImages from kernel + initrd)
%define with_bootwrapper %{?_without_bootwrapper: 0} %{?!_without_bootwrapper: 1}
# Want to build a the vsdo directories installed
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}

# Build the kernel-doc package, but don't fail the build if it botches.
# Here "true" means "continue" and "false" means "fail the build".
%if 0%{?released_kernel}
%define doc_build_fail false
%else
%define doc_build_fail true
%endif

# Control whether we perform a compat. check against published ABI.
%ifarch sparc64
%define with_kabichk 0
%define fancy_debuginfo 0
%else
%define with_kabichk 1
%define fancy_debuginfo 0
%endif

# Control whether we build the hmac for fips mode.
%define with_fips      %{?_without_fips:      0} %{?!_without_fips:      1}

%if %{fancy_debuginfo}
BuildRequires: rpm-build >= 4.4.2.1-4
%define debuginfo_args --strict-build-id
%endif

# Additional options for user-friendly one-off kernel building:
#
# Only build the base kernel (--with baseonly):
%define with_baseonly  %{?_with_baseonly:     1} %{?!_with_baseonly:     0}
# Only build the smp kernel (--with smponly):
%define with_smponly   %{?_with_smponly:      1} %{?!_with_smponly:      0}

# should we do C=1 builds with sparse
%define with_sparse	%{?_with_sparse:      1} %{?!_with_sparse:      0}

# Set debugbuildsenabled to 1 for production (build separate debug kernels)
#  and 0 for rawhide (all kernels are debug kernels).
# See also 'make debug' and 'make release'.
%define debugbuildsenabled 1

# Want to build a vanilla kernel build without any non-upstream patches?
# (well, almost none, we need nonintconfig for build purposes). Default to 0 (off).
%define with_vanilla %{?_with_vanilla: 1} %{?!_with_vanilla: 0}

# pkg_release is what we'll fill in for the rpm Release: field
%if 0%{?released_kernel}

%if 0%{?stable_rc}
%define stable_rctag .rc%{stable_rc}
%endif
%define pkg_release 32.2.3%{?dist}uek%{?buildid}

%else

# non-released_kernel
%if 0%{?rcrev}
%define rctag .rc%rcrev
%else
%define rctag .rc0
%endif
%if 0%{?gitrev}
%define gittag .git%gitrev
%else
%define gittag .git0
%endif
%define pkg_release 32.2.3%{?dist}uek%{?buildid}

%endif

# The kernel tarball/base version
#%define kversion 4.1.12
%define kversion 4.1.12

%define make_target bzImage

%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%if 0%{!?nopatches:1}
%define nopatches 0
%endif

%if %{with_vanilla}
%define nopatches 1
%endif

%define with_bootwrapper 0

%define pkg_release 32.2.3%{?dist}uek%{?buildid}

%define KVERREL %{rpmversion}-%{pkg_release}.%{_target_cpu}

%if !%{debugbuildsenabled}
%define with_debug 0
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug

%define with_pae 0

# if requested, only build base kernel
%if %{with_baseonly}
%define with_smp 0
%define with_kdump 0
%define with_debug 0
%endif

# if requested, only build smp kernel
%if %{with_smponly}
%define with_up 0
%define with_kdump 0
%define with_debug 0
%endif

%define all_x86 i386 i686

%if %{with_vdso_install}
# These arches install vdso/ directories.
%define vdso_arches %{all_x86} x86_64 ppc ppc64
%endif

# Overrides for generic default options

# only ppc need separate smp kernels
%ifnarch ppc alphaev56
%define with_smp 0
%endif

# only build kernel-kdump on ppc64
# (no relocatable kernel support upstream yet)
#FIXME: Temporarily disabled to speed up builds.
#ifnarch ppc64
%define with_kdump 0
#endif

# don't do debug builds on anything but i686 and x86_64
%ifnarch i686 x86_64
%define with_debug 0
%endif

# only package docs noarch
%ifnarch noarch
%define with_doc 0
%endif

# no need to build headers again for these arches,
# they can just use i586 and ppc64 headers
%ifarch ppc64iseries
%define with_headers 0
%endif

# don't build noarch kernels or headers (duh)
%ifarch noarch
%define with_up 0
%define with_headers 0
%define with_paravirt 0
%define with_paravirt_debug 0
%define all_arch_configs kernel-%{version}-*.config
%define with_firmware  %{?_without_firmware:  0} %{?!_without_firmware:  1}
%endif

# bootwrapper is only on ppc
%ifnarch ppc ppc64
%define with_bootwrapper 0
%endif

# sparse blows up on ppc64 alpha and sparc64
%ifarch ppc64 ppc alpha sparc64
%define with_sparse 0
%endif

# Only x86_64 does dtrace
%ifarch x86_64
%define with_dtrace 1
%endif

# Per-arch tweaks

%ifarch %{all_x86}
%define asmarch x86
%define hdrarch i386
%define all_arch_configs kernel-%{version}-i?86*.config
%define image_install_path boot
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch x86_64
%define asmarch x86
#%define all_arch_configs kernel-%{version}-x86_64*.config
%define image_install_path boot
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch ppc64
%define asmarch powerpc
%define hdrarch powerpc
%define all_arch_configs kernel-%{version}-ppc64*.config
%define image_install_path boot
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%endif

%ifarch s390x
%define asmarch s390
%define hdrarch s390
%define all_arch_configs kernel-%{version}-s390x.config
%define image_install_path boot
%define make_target image
%define kernel_image arch/s390/boot/image
%endif

%ifarch sparc
# We only build sparc headers since we dont support sparc32 hardware
%endif

%ifarch sparc64
%define asmarch sparc
%define all_arch_configs kernel-%{version}-sparc64*.config
%define make_target image
%define kernel_image arch/sparc/boot/image
%define image_install_path boot
%endif

%ifarch ppc
%define asmarch powerpc
%define hdrarch powerpc
%define all_arch_configs kernel-%{version}-ppc{-,.}*config
%define image_install_path boot
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%endif

%ifarch ia64
%define all_arch_configs kernel-%{version}-ia64*.config
%define image_install_path boot/efi/EFI/redhat
%define make_target compressed
%define kernel_image vmlinux.gz
%endif

%ifarch alpha alphaev56
%define all_arch_configs kernel-%{version}-alpha*.config
%define image_install_path boot
%define make_target vmlinux
%define kernel_image vmlinux
%endif

%ifarch %{arm}
%define all_arch_configs kernel-%{version}-arm*.config
%define image_install_path boot
%define hdrarch arm
%define make_target vmlinux
%define kernel_image vmlinux
%endif

%if %{nopatches}
# XXX temporary until last vdso patches are upstream
%define vdso_arches ppc ppc64
%endif

%define oldconfig_target oldnoconfig

# To temporarily exclude an architecture from being built, add it to
# %nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# We don't build a kernel on i386; we only do kernel-headers there,
# and we no longer build for 31bit S390. Same for 32bit sparc and arm.
##%define nobuildarches i386 s390 sparc %{arm}
%define nobuildarches s390 sparc %{arm}

%ifarch %nobuildarches
%define with_up 0
%define with_smp 0
%define with_pae 0
%define with_kdump 0
%define with_debuginfo 0
%define _enable_debug_packages 0
%define with_paravirt 0
%define with_paravirt_debug 0
%endif

%define with_pae_debug 0
%if %{with_pae}
%define with_pae_debug %{with_debug}
%endif

#
# Three sets of minimum package version requirements in the form of Conflicts:
# to versions below the minimum
#

#
# First the general kernel 2.6 required versions as per
# Documentation/Changes
#
%define kernel_dot_org_conflicts  ppp < 2.4.3-3, isdn4k-utils < 3.2-32, nfs-utils < 1.0.7-12, e2fsprogs < 1.37-4, util-linux < 2.12, jfsutils < 1.1.7-2, reiserfs-utils < 3.6.19-2, xfsprogs < 2.6.13-4, procps < 3.2.5-6.3, oprofile < 0.9.1-2

#
# Then a series of requirements that are distribution specific, either
# because we add patches for something, or the older versions have
# problems with the newer kernel or lack certain things that make
# integration in the distro harder than needed.
#
##%define package_conflicts initscripts < 7.23, udev < 063-6, iptables < 1.3.2-1, ipw2200-firmware < 2.4, iwl4965-firmware < 228.57.2, selinux-policy-targeted < 1.25.3-14, squashfs-tools < 4.0, wireless-tools < 29-3
%define package_conflicts initscripts < 7.23, udev < 063-6, iptables < 1.3.2-1, ipw2200-firmware < 2.4, selinux-policy-targeted < 1.25.3-14, device-mapper-multipath < 0.4.9-64, dracut < 004-303.0.3

#
# The ld.so.conf.d file we install uses syntax older ldconfig's don't grok.
#
%define kernel_xen_conflicts glibc < 2.3.5-1, xen < 3.0.1

# upto and including kernel 2.4.9 rpms, the 4Gb+ kernel was called kernel-enterprise
# now that the smp kernel offers this capability, obsolete the old kernel
%define kernel_smp_obsoletes kernel-enterprise < 2.4.10
%define kernel_PAE_obsoletes kernel-smp < 2.6.17, kernel-xen <= 2.6.27-0.2.rc0.git6.fc10
%define kernel_PAE_provides kernel-xen = %{rpmversion}-%{pkg_release}

%ifarch x86_64
%define kernel_obsoletes kernel-xen <= 2.6.27-0.2.rc0.git6.fc10
%define kernel_provides kernel%{?variant}-xen = %{rpmversion}-%{pkg_release}
%endif

# We moved the drm include files into kernel-headers, make sure there's
# a recent enough libdrm-devel on the system that doesn't have those.
%define kernel_headers_conflicts libdrm-devel < 2.4.0-0.15

#
# Packages that need to be installed before the kernel is, because the %post
# scripts use them.
#
%define kernel_prereq  fileutils, module-init-tools, initscripts >= 8.11.1-1, kernel-firmware = %{rpmversion}-%{pkg_release}, %{_sbindir}/new-kernel-pkg
%define initrd_prereq  dracut-kernel >= 004-242.0.3

#
# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#	%%kernel_reqprovconf <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
#
%define kernel_reqprovconf \
Provides: kernel%{?variant} = %{rpmversion}-%{pkg_release}\
Provides: kernel%{?variant}-%{_target_cpu} = %{rpmversion}-%{pkg_release}%{?1:.%{1}}\
Provides: kernel%{?variant}-drm = 4.3.0\
Provides: kernel%{?variant}-drm-nouveau = 12\
Provides: kernel%{?variant}-modeset = 1\
Provides: kernel%{?variant}-uname-r = %{KVERREL}%{?1:.%{1}}\
Provides: oracleasm = 2.0.5\
%ifnarch sparc64\
Provides: x86_energy_perf_policy = %{KVERREL}%{?1:.%{1}}\
Provides: turbostat = %{KVERREL}%{?1:.%{1}}\
%endif\
Provides: perf = %{KVERREL}%{?1:.%{1}}\
#Provides: libperf.a = %{KVERREL}%{?1:.%{1}}\
%ifarch sparc64\
Provides: kernel = %{rpmversion}-%{pkg_release}\
%endif\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(pre): linux-firmware >= 20140911-0.1.git365e80c.0.5\
Requires(post): %{_sbindir}/new-kernel-pkg\
Requires(preun): %{_sbindir}/new-kernel-pkg\
Conflicts: %{kernel_dot_org_conflicts}\
Conflicts: %{package_conflicts}\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# We can't let RPM do the dependencies automatic because it'll then pick up\
# a correct but undesirable perl dependency from the module headers which\
# isn't required for the kernel proper to function\
AutoReq: no\
AutoProv: yes\
%{nil}

%define variant %{?build_variant:%{build_variant}}%{!?build_variant:-uek}
Name: kernel%{?variant}
Group: System Environment/Kernel
License: GPLv2
URL: http://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
ExclusiveArch: noarch %{all_x86} x86_64 paravirt paravirt-debug ppc ppc64 ia64 sparc sparc64 s390x alpha alphaev56 %{arm}
ExclusiveOS: Linux

%kernel_reqprovconf
%ifarch x86_64
Obsoletes: kernel-smp
%endif


#
# List the packages used during the kernel build
#
BuildRequires: module-init-tools, patch >= 2.5.4, bash >= 2.03, sh-utils, tar
BuildRequires: bzip2, findutils, gzip, m4, perl, make >= 3.78, diffutils, gawk
BuildRequires: gcc >= 3.4.2, binutils >= 2.12
BuildRequires: net-tools
BuildRequires: elfutils-libelf-devel
BuildRequires: python, python-devel
BuildRequires: flex >= 2.5.19, bison >= 2.3
BuildRequires: pkgconfig
BuildRequires: glib2-devel
BuildRequires: elfutils-devel
BuildRequires: bc
%if %{with_doc}
BuildRequires: xmlto
%endif
%if %{with_sparse}
BuildRequires: sparse >= 0.4.1
%endif
%if %{signmodules}
BuildRequires: openssl
BuildRequires: gnupg
BuildRequires: pesign >= 0.10-4
%endif
%if %{with_fips}
BuildRequires: hmaccalc
%endif
%if %{with_dtrace}
BuildRequires: libdtrace-ctf-devel >= 0.5.0
%endif
BuildConflicts: rhbuildsys(DiskFree) < 500Mb

Source0: ftp://ftp.kernel.org/pub/linux/kernel/v2.6/linux-%{kversion}.tar.bz2

%if %{signmodules}
Source10: x509.genkey
%endif

Source13: mod-sign.sh
%define modsign_cmd %{SOURCE13}

Source14: find-provides
Source16: perf
Source17: kabitool
Source18: check-kabi
Source20: x86_energy_perf_policy
Source21: securebootca.cer
Source22: secureboot.cer
Source23: turbostat

Source1000: config-x86_64
Source1001: config-x86_64-debug
#Source1004: config-sparc
#Source1005: config-sparc-debug

Source25: Module.kabi_x86_64debug
Source26: Module.kabi_x86_64

Source200: kabi_whitelist_x86_64debug
Source201: kabi_whitelist_x86_64
Source202: ksplice_signing_key.x509

Source300: debuginfo-g1.diff
Source301: debuginfo-g1-minusr-old-elfutils.diff

# Here should be only the patches up to the upstream canonical Linus tree.

# For a stable release kernel
%if 0%{?stable_update}
%if 0%{?stable_base}
%define    stable_patch_00  patch-2.6.%{base_sublevel}.%{stable_base}.bz2
Patch00: %{stable_patch_00}
%endif
%if 0%{?stable_rc}
%define    stable_patch_01  patch-2.6.%{base_sublevel}.%{stable_update}-rc%{stable_rc}.bz2
Patch01: %{stable_patch_01}
%endif

# non-released_kernel case
# These are automagically defined by the rcrev and gitrev values set up
# near the top of this spec file.
%else
%if 0%{?rcrev}
Patch00: patch-2.6.%{upstream_sublevel}-rc%{rcrev}.bz2
%if 0%{?gitrev}
Patch01: patch-2.6.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}.bz2
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
Patch00: patch-2.6.%{base_sublevel}-git%{gitrev}.bz2
%endif
%endif
%endif

%if !%{nopatches}
# revert patches place holder
%endif


BuildRoot: %{_tmppath}/kernel-%{KVERREL}-root

# Override find_provides to use a script that provides "kernel(symbol) = hash".
# Pass path of the RPM temp dir containing kabideps to find-provides script.
%global _use_internal_dependency_generator 0
%define __find_provides %_sourcedir/find-provides %{_tmppath}
%define __find_requires /usr/lib/rpm/redhat/find-requires kernel

%description
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.


%package doc
Summary: Various documentation bits found in the kernel source
Group: Documentation
Obsoletes: kernel-doc
Provides: kernel-doc
%description doc
This package contains documentation files from the kernel
source. Various bits of information about the Linux kernel and the
device drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to Linux kernel modules at load time.


%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: glibc-kernheaders
Obsoletes: kernel-headers
Provides: kernel-headers
Provides: glibc-kernheaders = 3.0-46
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package firmware
Summary: Firmware files used by the Linux kernel
Group: Development/System
# This is... complicated.
# Look at the WHENCE file.
License: GPL+ and GPLv2+ and MIT and Redistributable, no modification permitted
%if "x%{?variant}" != "x"
Provides: kernel-firmware = %{rpmversion}-%{pkg_release}
%endif
%ifarch sparc64
Provides: kernel-firmware = %{rpmversion}-%{pkg_release}
%endif
%description firmware
Kernel firmware includes firmware files required for some devices to
operate.

%package bootwrapper
Summary: Boot wrapper files for generating combined kernel + initrd images
Group: Development/System
Requires: gzip
%description bootwrapper
Kernel-bootwrapper contains the wrapper code which makes bootable "zImage"
files combining both kernel and initial ramdisk.

%package debuginfo-common
Summary: Kernel source files used by %{name}-debuginfo packages
Group: Development/Debug
Provides: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
%description debuginfo-common
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.


#
# This macro creates a kernel-<subpackage>-debuginfo package.
#	%%kernel_debuginfo_package <subpackage>
#
%define kernel_debuginfo_package() \
%package %{?1:%{1}-}debuginfo\
Summary: Debug information for package %{name}%{?1:-%{1}}\
Group: Development/Debug\
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}\
Provides: %{name}%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{version}-%{release}\
AutoReqProv: no\
%description -n %{name}%{?1:-%{1}}-debuginfo\
This package provides debug information for package %{name}%{?1:-%{1}}.\
This is required to use SystemTap with %{name}%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global debuginfo_args %{?debuginfo_args} -p '/.*/%%{KVERREL}%{?1:\.%{1}}/.*|/.*%%{KVERREL}%{?1:\.%{1}}(\.debug)?' -o debuginfo%{?1}.list}\
%{nil}

#
# This macro creates a kernel-<subpackage>-devel package.
#	%%kernel_devel_package <subpackage> <pretty-name>
#
%define kernel_devel_package() \
%package %{?1:%{1}-}devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: kernel%{?variant}%{?1:-%{1}}-devel-%{_target_cpu} = %{version}-%{release}\
Provides: kernel%{?variant}-xen-devel = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel%{?variant}-devel-%{_target_cpu} = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel%{?variant}-devel = %{version}-%{release}%{?1:.%{1}}\
Provides: kernel%{?variant}-devel-uname-r = %{KVERREL}%{?1:.%{1}}\
%ifarch sparc64\
Provides: kernel-devel = %{version}-%{release}%{?1:.%{1}}\
%endif\
AutoReqProv: no\
Requires(pre): /usr/bin/find\
Requires: elfutils-libelf >= 0.160\
Requires: elfutils-libs >= 0.160\
%if %{with_dtrace}\
Requires: libdtrace-ctf >= 0.5.0\
%endif\
%description -n kernel%{?variant}%{?1:-%{1}}-devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#	%%define variant_summary The Linux kernel compiled for <configuration>
#	%%kernel_variant_package [-n <pretty-name>] <subpackage>
#
%define kernel_variant_package(n:) \
%package %1\
Summary: %{variant_summary}\
Group: System Environment/Kernel\
%kernel_reqprovconf\
%{expand:%%kernel_devel_package %1 %{!?-n:%1}%{?-n:%{-n*}}}\
%{expand:%%kernel_debuginfo_package %1}\
%{nil}


# First the auxiliary packages of the main kernel package.
%kernel_devel_package
%kernel_debuginfo_package


# Now, each variant package.

%define variant_summary The Linux kernel compiled for SMP machines
%kernel_variant_package -n SMP smp
%description smp
This package includes a SMP version of the Linux kernel. It is
required only on machines with two or more CPUs as well as machines with
hyperthreading technology.

Install the kernel-smp package if your machine uses two or more CPUs.


%define variant_summary The Linux kernel compiled for PAE capable machines
%kernel_variant_package PAE
%description PAE
This package includes a version of the Linux kernel with support for up to
64GB of high memory. It requires a CPU with Physical Address Extensions (PAE).
The non-PAE kernel can only address up to 4GB of memory.
Install the kernel-PAE package if your machine has more than 4GB of memory.


%define variant_summary The Linux kernel compiled with extra debugging enabled for PAE capable machines
%kernel_variant_package PAEdebug
Obsoletes: kernel-PAE-debug
%description PAEdebug
This package includes a version of the Linux kernel with support for up to
64GB of high memory. It requires a CPU with Physical Address Extensions (PAE).
The non-PAE kernel can only address up to 4GB of memory.
Install the kernel-PAE package if your machine has more than 4GB of memory.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.


%define variant_summary The Linux kernel compiled with extra debugging enabled
%kernel_variant_package debug
%description debug
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.


%define variant_summary A minimal Linux kernel compiled for crash dumps
%kernel_variant_package kdump
%description kdump
This package includes a kdump version of the Linux kernel. It is
required only on machines which will use the kexec-based kernel crash dump
mechanism.


%prep
# do a few sanity-checks for --with *only builds
%if %{with_baseonly}
%if !%{with_up}%{with_pae}
echo "Cannot build --with baseonly, up build is disabled"
exit 1
%endif
%endif

%if %{with_smponly}
%if !%{with_smp}
echo "Cannot build --with smponly, smp build is disabled"
exit 1
%endif
%endif

patch_command='patch -p1 -F1 -s'
ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1;
  fi
  if ! egrep "^Patch[0-9]+: $patch\$" %{_specdir}/%{name}*.spec ; then
    [ "${patch:0:10}" != "patch-2.6." ] && echo "Patch $patch not listed in specfile" && exit 1;
  fi
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz) gunzip < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

test_config_file()
{
  TestConfig=$1
  Arch=`head -n 3 .config |grep -e "Linux.*Kernel" |cut -d '/' -f 2 | cut -d ' ' -f 1`
  if [ `make ARCH=$Arch listnewconfig 2>/dev/null | grep -c CONFIG`  -ne 0 ]; then
	echo "Following config options are unconfigured"
	make ARCH=$Arch listnewconfig 2> /dev/null
	echo "WARNING: Kernel version and config file missmatch"
	echo "WARNING: This options will be unset by default in config file"
  fi
}

# First we unpack the kernel tarball.
# If this isn't the first make prep, we use links to the existing clean tarball
# which speeds things up quite a bit.

# Update to latest upstream.
%if 0%{?released_kernel}
%define vanillaversion 2.6.%{base_sublevel}
# non-released_kernel case
%else
%if 0%{?rcrev}
%define vanillaversion 2.6.%{upstream_sublevel}-rc%{rcrev}
%if 0%{?gitrev}
%define vanillaversion 2.6.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
%define vanillaversion 2.6.%{base_sublevel}-git%{gitrev}
%endif
%endif
%endif

# We can share hardlinked source trees by putting a list of
# directory names of the CVS checkouts that we want to share
# with in .shared-srctree. (Full pathnames are required.)
[ -f .shared-srctree ] && sharedirs=$(cat .shared-srctree)

if [ ! -d kernel-%{kversion}/vanilla-%{vanillaversion} ]; then

  if [ -d kernel-%{kversion}/vanilla-%{kversion} ]; then

    cd kernel-%{kversion}

    # Any vanilla-* directories other than the base one are stale.
    for dir in vanilla-*; do
      [ "$dir" = vanilla-%{kversion} ] || rm -rf $dir &
    done

  else

    # Ok, first time we do a make prep.
    rm -f pax_global_header
    for sharedir in $sharedirs ; do
      if [[ ! -z $sharedir  &&  -d $sharedir/kernel-%{kversion}/vanilla-%{kversion} ]] ; then
        break
      fi
    done
    if [[ ! -z $sharedir  &&  -d $sharedir/kernel-%{kversion}/vanilla-%{kversion} ]] ; then
%setup -q -n kernel-%{kversion} -c -T
      cp -rl $sharedir/kernel-%{kversion}/vanilla-%{kversion} .
    else
%setup -q -n kernel-%{kversion} -c
      mv linux-%{kversion} vanilla-%{kversion}
    fi

  fi

%if "%{kversion}" != "%{vanillaversion}"

  for sharedir in $sharedirs ; do
    if [[ ! -z $sharedir  &&  -d $sharedir/kernel-%{kversion}/vanilla-%{vanillaversion} ]] ; then
      break
    fi
  done
  if [[ ! -z $sharedir  &&  -d $sharedir/kernel-%{kversion}/vanilla-%{vanillaversion} ]] ; then

    cp -rl $sharedir/kernel-%{kversion}/vanilla-%{vanillaversion} .

  else

    cp -rl vanilla-%{kversion} vanilla-%{vanillaversion}
    cd vanilla-%{vanillaversion}

# Update vanilla to the latest upstream.
# (non-released_kernel case only)
%if 0%{?rcrev}
    ApplyPatch patch-2.6.%{upstream_sublevel}-rc%{rcrev}.bz2
%if 0%{?gitrev}
    ApplyPatch patch-2.6.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}.bz2
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
    ApplyPatch patch-2.6.%{base_sublevel}-git%{gitrev}.bz2
%endif
%endif

    cd ..

  fi

%endif

else
  # We already have a vanilla dir.
  cd kernel-%{kversion}
fi

if [ -d linux-%{kversion}.%{_target_cpu} ]; then
  # Just in case we ctrl-c'd a prep already
  rm -rf deleteme.%{_target_cpu}
  # Move away the stale away, and delete in background.
  mv linux-%{kversion}.%{_target_cpu} deleteme.%{_target_cpu}
  rm -rf deleteme.%{_target_cpu} &
fi

cp -rl vanilla-%{vanillaversion} linux-%{kversion}-%{release}
cd linux-%{kversion}-%{release}

# released_kernel with possible stable updates
%if 0%{?stable_base}
ApplyPatch %{stable_patch_00}
%endif
%if 0%{?stable_rc}
ApplyPatch %{stable_patch_01}
%endif

# Copy the RPM find-debuginfo.sh into the buildroot and patch it
# to support -g1.  (This is a patch of *RPM*, not of the kernel,
# so it is not governed by nopatches.)
cp %{_rpmconfigdir}/find-debuginfo.sh %{_builddir}
patch %{_builddir}/find-debuginfo.sh %{SOURCE300} || \
      { mv -f %{_builddir}/find-debuginfo.sh.orig %{_builddir}/find-debuginfo.sh && \
        patch %{_builddir}/find-debuginfo.sh %{SOURCE301}; }
chmod +x %{_builddir}/find-debuginfo.sh

# only deal with configs if we are going to build for the arch
# %ifnarch %nobuildarches

mkdir -p configs
%ifarch x86_64
	cp %{SOURCE1001} configs/config-debug
	cp %{SOURCE1000} configs/config
%endif #ifarch x86_64

%ifarch i686
	cp %{SOURCE1003} configs/config-debug
	cp %{SOURCE1002} configs/config
%endif #ifarch i686

%ifarch sparc64
	cp %{SOURCE1005} configs/config-debug
	cp %{SOURCE1004} configs/config
%endif #ifarch sparc

cp %{SOURCE202} ksplice_signing_key.x509

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -exec rm -f {} \; >/dev/null

###
### build
###
%build

%if %{with_sparse}
%define sparse_mflags	C=1
%endif

%if %{fancy_debuginfo}
# This override tweaks the kernel makefiles so that we run debugedit on an
# object before embedding it.  When we later run find-debuginfo.sh, it will
# run debugedit again.  The edits it does change the build ID bits embedded
# in the stripped object, but repeating debugedit is a no-op.  We do it
# beforehand to get the proper final build ID bits into the embedded image.
# This affects the vDSO images in vmlinux, and the vmlinux image in bzImage.
export AFTER_LINK=\
'sh -xc "/usr/lib/rpm/debugedit -b $$RPM_BUILD_DIR -d /usr/src/debug \
				-i $@ > $@.id"'
%endif

cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    Flavour=$3
    InstallName=${4:-vmlinuz}

    # Pick the right config file for the kernel we're building
    Config=kernel-%{version}-%{_target_cpu}${Flavour:+-${Flavour}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Flavour:+.${Flavour}}

    # When the bootable image is just the ELF kernel, strip it.
    # We already copy the unstripped file into the debuginfo package.
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

    KernelVer=%{version}-%{release}.%{_target_cpu}${Flavour:+.${Flavour}}
    echo BUILDING A KERNEL FOR ${Flavour} %{_target_cpu}...

    # make sure EXTRAVERSION says what we want it to say
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = %{?stablerev}-%{release}.%{_target_cpu}${Flavour:+.${Flavour}}/" Makefile
    #perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{base_sublevel}/" Makefile

    make -s mrproper

    %if %{signmodules}
	cp %{SOURCE10} .
	chmod +x scripts/sign-file
    %endif

    if [ "$Flavour" == "debug" ]; then
	cp configs/config-debug .config
    else
	cp configs/config .config
    fi

    Arch=`head -n 3 .config |grep -e "Linux.*Kernel" |cut -d '/' -f 2 | cut -d ' ' -f 1`
    echo USING ARCH=$Arch
    make -s ARCH=$Arch %{oldconfig_target} > /dev/null
    make -s ARCH=$Arch V=1 %{?_smp_mflags} $MakeTarget %{?sparse_mflags}
    make -s ARCH=$Arch V=1 %{?_smp_mflags} modules %{?sparse_mflags} || exit 1

    # Start installing the results
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/boot
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer
    touch $RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img
    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
    fi
    %if %{signmodules}
    %ifarch x86_64
	# Sign the image if we're using EFI
        %pesign -s -i $KernelImage -o $KernelImage.signed -a %{SOURCE21} -c %{SOURCE22} -n oraclesecureboot
        mv $KernelImage.signed $KernelImage
    %endif
    %endif
    $CopyKernel $KernelImage \
		$RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer

%if %{with_fips}
    # hmac sign the kernel for FIPS
    echo "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    sha512hmac $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer | sed -e "s,$RPM_BUILD_ROOT,," > $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac;
%endif

    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    # Override $(mod-fw) because we don't want it to install any firmware
    # We'll do that ourselves with 'make firmware_install'
    make -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=
    # check if the modules are being signed

%ifarch %{vdso_arches}
    make -s ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
    if grep '^CONFIG_XEN=y$' .config >/dev/null; then
      echo > ldconfig-kernel.conf "\
# This directive teaches ldconfig to search in nosegneg subdirectories
# and cache the DSOs there with extra bit 0 set in their hwcap match
# fields.  In Xen guest kernels, the vDSO tells the dynamic linker to
# search in nosegneg subdirectories and to match this extra hwcap bit
# in the ld.so.cache file.
hwcap 0 nosegneg"
    fi
    if [ ! -s ldconfig-kernel.conf ]; then
      echo > ldconfig-kernel.conf "\
# Placeholder file, no vDSO hwcap entries used in this kernel."
    fi
    %{__install} -D -m 444 ldconfig-kernel.conf \
        $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
%endif
%ifarch %{vdso_arches} sparc64
%ifnarch noarch
# build tools/perf:
    if [ -d tools/perf ]; then
	cd tools/perf
	make all
# and install it:
#	mkdir -p $RPM_BUILD_ROOT/usr/bin/$KernelVer/
	mkdir -p $RPM_BUILD_ROOT/usr/libexec/
	install -m 755 perf $RPM_BUILD_ROOT/usr/libexec/perf.$KernelVer
	#install -m 755 libperf.a $RPM_BUILD_ROOT/lib/modules/$KernelVer/bin/%{_target_cpu}/libperf.a
	cd ../..
    fi
%endif
%ifarch x86_64 %{all_x86}
# build tools/power/x86/x86_energy_perf_policy:
    if [ -d tools/power/x86/x86_energy_perf_policy ]; then
       cd tools/power/x86/x86_energy_perf_policy
       make
# and install it:
       mkdir -p $RPM_BUILD_ROOT/usr/libexec/
       install -m 755 x86_energy_perf_policy $RPM_BUILD_ROOT/usr/libexec/x86_energy_perf_policy.$KernelVer
       cd ../../../../
    fi
# build tools/power/x86/turbostat:
    if [ -d tools/power/x86/turbostat ]; then
       cd tools/power/x86/turbostat
       make
# and install it:
       mkdir -p $RPM_BUILD_ROOT/usr/libexec/
       install -m 755 turbostat $RPM_BUILD_ROOT/usr/libexec/turbostat.$KernelVer
       cd ../../../../
    fi
%endif
%endif

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/extra
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/weak-updates
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi

    # create the kABI metadata for use in packaging
    echo "**** GENERATING kernel ABI metadata ****"
    gzip -c9 < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-$KernelVer.gz
    chmod 0755 %_sourcedir/kabitool
    if [ -e $RPM_SOURCE_DIR/kabi_whitelist_%{_target_cpu}$Flavour ]; then
       cp $RPM_SOURCE_DIR/kabi_whitelist_%{_target_cpu}$Flavour $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/kabi_whitelist
    fi
    rm -f %{_tmppath}/kernel-$KernelVer-kabideps
    %_sourcedir/kabitool -s Module.symvers -o %{_tmppath}/kernel-$KernelVer-kabideps

%if %{with_kabichk}
    echo "**** kABI checking is enabled in kernel SPEC file. ****"
    chmod 0755 $RPM_SOURCE_DIR/check-kabi
    if [ -e $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Flavour ]; then
       cp $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Flavour $RPM_BUILD_ROOT/Module.kabi
       $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
       rm $RPM_BUILD_ROOT/Module.kabi # for now, don't keep it around.
    else
       echo "**** NOTE: Cannot find reference Module.kabi file. ****"
    fi
%endif

    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*.o
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*/*.o
%ifarch ppc
    cp -a --parents arch/powerpc/lib/crtsavres.[So] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    cp -a --parents Kbuild $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents kernel/bounds.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/%{asmarch}/kernel/asm-offsets.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%ifnarch %{sparc}
    cp -a --parents arch/%{asmarch}/kernel/asm-offsets_64.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    cp -a --parents security/selinux/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/

    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cd include
    cp -a acpi asm-generic clocksource config crypto drm dt-bindings generated keys kvm linux math-emu media memory misc net pcmcia ras rdma rxrpc scsi soc sound target trace uapi video xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    asmdir=../arch/%{asmarch}/include/asm
    cp -a $asmdir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/
    cd $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    ln -s $asmdir asm
    cd -
    # Make sure the Makefile and version.h have a matching timestamp so that
    # external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h
    # Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
    cp $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf
    cd ..

%if %{fancy_debuginfo}
    if test -s vmlinux.id; then
      cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id
    else
      echo >&2 "*** ERROR *** no vmlinux build ID! ***"
      exit 1
    fi
%endif

    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
%endif

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.

    fgrep /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
      LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
    }

    collect_modules_list networking \
			 'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|register_netdevice'
    collect_modules_list block \
			 'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size'
    collect_modules_list drm \
			 'drm_open|drm_init'
    collect_modules_list modesetting \
			 'drm_crtc_init'

    # detect missing or incorrect license tags
    rm -f modinfo
    while read i
    do
      echo -n "${i#$RPM_BUILD_ROOT/lib/modules/$KernelVer/} " >> modinfo
      /sbin/modinfo -l $i >> modinfo
    done < modnames

    egrep -v \
	  'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' \
	  modinfo && exit 1

    rm -f modinfo modnames

%if %{signmodules}
    # Save off the .tmp_versions/ directory.  We'll use it in the
    # __debug_install_post macro below to sign the right things
    # Also save the signing keys so we actually sign the modules with the
    # right key.
    cp -r .tmp_versions .tmp_versions.sign${Flavour:+.${Flavour}}
    cp signing_key.priv signing_key.priv.sign${Flavour:+.${Flavour}}
    cp signing_key.x509 signing_key.x509.sign${Flavour:+.${Flavour}}
%endif

    # remove files that will be auto generated by depmod at rpm -i time
    for i in alias ccwmap dep ieee1394map inputmap isapnpmap ofmap pcimap seriomap symbols usbmap
    do
      rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$i
    done

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir
    ln -sf $DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot

cd linux-%{version}-%{release}

%if %{with_debug}
%if %{with_up}
BuildKernel %make_target %kernel_image debug
%endif
%if %{with_pae}
BuildKernel %make_target %kernel_image PAEdebug
%endif
%endif

%if %{with_pae}
BuildKernel %make_target %kernel_image PAE
%endif

%if %{with_up}
BuildKernel %make_target %kernel_image
%endif

%if %{with_smp}
BuildKernel %make_target %kernel_image smp
%endif

%if %{with_kdump}
BuildKernel vmlinux vmlinux kdump vmlinux
%endif

%if %{with_doc}
# Make the HTML and man pages.
make -j1  htmldocs mandocs || %{doc_build_fail}

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a=rX Documentation
find Documentation -type d | xargs chmod u+w
%endif

%define dgst $((grep '^CONFIG_MODULE_SIG_SHA512=y$' .config >/dev/null && grep '^CONFIG_MODULE_SIG_HASH=\"sha512\"$' .config >/dev/null && echo sha512) || (grep '^CONFIG_MODULE_SIG_SHA256=y$' .config >/dev/null && grep '^CONFIG_MODULE_SIG_HASH=\"sha256\"$' .config >/dev/null && echo sha256))

%define __modsign_install_post \
  if [ "%{signmodules}" == "1" ]; then \
    if [ "%{with_pae}" != "0" ]; then \
      mv signing_key.priv.sign.PAE signing_key.priv \
      mv signing_key.x509.sign.PAE signing_key.x509 \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}.PAE/ %{dgst} \
    fi \
    if [ "%{with_debug}" != "0" ]; then \
      mv signing_key.priv.sign.debug signing_key.priv \
      mv signing_key.x509.sign.debug signing_key.x509 \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}.debug/ %{dgst} \
    fi \
    if [ "%{with_pae_debug}" != "0" ]; then \
      mv signing_key.priv.sign.PAEdebug signing_key.priv \
      mv signing_key.x509.sign.PAEdebug signing_key.x509 \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}.PAEdebug/ %{dgst} \
    fi \
    if [ "%{with_up}" != "0" ]; then \
      mv signing_key.priv.sign signing_key.priv \
      mv signing_key.x509.sign signing_key.x509 \
      %{modsign_cmd} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/ %{dgst} \
    fi \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
# TEMPORARY HACK: use the debuginfo in the build tree, passing it -g1 so as
# to strip out only debugging sections.
%define debug_package %{nil}

%if %{with_debuginfo}

%define __debug_install_post \
  %{_builddir}/find-debuginfo.sh %{debuginfo_args} -g1 %{_builddir}/%{?buildsubdir}\
%{nil}

%ifnarch noarch
%global __debug_package 1
%files debuginfo-common
%defattr(-,root,root)
%dir /usr/src/debug
/usr/src/debug/kernel-%{version}/linux-%{kversion}-%{release}
%dir %{debuginfodir}
%dir %{debuginfodir}/%{image_install_path}
%dir %{debuginfodir}/lib
%dir %{debuginfodir}/lib/modules
%dir %{debuginfodir}/usr/src/kernels
%endif
%endif

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modsign_install_post}

###
### install
###

%install
cd linux-%{version}-%{release}

%if %{with_doc}
docdir=$RPM_BUILD_ROOT%{_datadir}/doc/kernel-doc-%{rpmversion}
man9dir=$RPM_BUILD_ROOT%{_datadir}/man/man9

# copy the source over
mkdir -p $docdir
tar -f - --exclude=man --exclude='.*' -c Documentation | tar xf - -C $docdir

# Install man pages for the kernel API.
mkdir -p $man9dir
find Documentation/DocBook/man -name '*.9.gz' -print0 |
xargs -0 --no-run-if-empty %{__install} -m 444 -t $man9dir $m
ls $man9dir | grep -q '' || > $man9dir/BROKEN
%endif

%ifnarch noarch
# perf shell wrapper
mkdir -p $RPM_BUILD_ROOT/usr/sbin/
cp $RPM_SOURCE_DIR/perf $RPM_BUILD_ROOT/usr/sbin/perf
chmod 0755 $RPM_BUILD_ROOT/usr/sbin/perf
%endif

%ifarch x86_64 %{all_x86}
# x86_energy_perf_policy shell wrapper
mkdir -p $RPM_BUILD_ROOT/usr/sbin/
cp $RPM_SOURCE_DIR/x86_energy_perf_policy $RPM_BUILD_ROOT/usr/sbin/x86_energy_perf_policy
chmod 0755 $RPM_BUILD_ROOT/usr/sbin/x86_energy_perf_policy
# turbostat shell wrapper
mkdir -p $RPM_BUILD_ROOT/usr/sbin/
cp $RPM_SOURCE_DIR/turbostat $RPM_BUILD_ROOT/usr/sbin/turbostat
chmod 0755 $RPM_BUILD_ROOT/usr/sbin/turbostat
%endif


%if %{with_headers}
# Install kernel headers
make ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

# Do headers_check but don't die if it fails.
make ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_check \
     > hdrwarnings.txt || :
if grep -q exist hdrwarnings.txt; then
   sed s:^$RPM_BUILD_ROOT/usr/include/:: hdrwarnings.txt
   # Temporarily cause a build failure if header inconsistencies.
   # exit 1
fi

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
	-name ..install.cmd -o -name ..check.cmd \) | xargs rm -f

# glibc provides scsi headers for itself, for now
rm -rf $RPM_BUILD_ROOT/usr/include/scsi
rm -f $RPM_BUILD_ROOT/usr/include/asm*/atomic.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/io.h
rm -f $RPM_BUILD_ROOT/usr/include/asm*/irq.h

# these are provided by drm-devel
rm -rf $RPM_BUILD_ROOT/usr/include/drm
%endif

%if %{with_firmware}
mkdir -p $RPM_BUILD_ROOT/lib/firmware/%{rpmversion}-%{pkg_release}
make INSTALL_FW_PATH=$RPM_BUILD_ROOT/lib/firmware/%{rpmversion}-%{pkg_release} firmware_install
%endif

%if %{with_bootwrapper}
make DESTDIR=$RPM_BUILD_ROOT bootwrapper_install WRAPPER_OBJDIR=%{_libdir}/kernel-wrapper WRAPPER_DTSDIR=%{_libdir}/kernel-wrapper/dts
%endif

###
### clean
###

%clean
rm -rf $RPM_BUILD_ROOT

###
### scripts
###

#
# This macro defines a %%post script for a kernel*-devel package.
#	%%kernel_devel_post [<subpackage>]
#
%define kernel_devel_post() \
%{expand:%%post %{?1:%{1}-}devel}\
if [ -f /etc/sysconfig/kernel ]\
then\
    . /etc/sysconfig/kernel || exit $?\
fi\
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]\
then\
    (cd /usr/src/kernels/%{kversion}-%{release}.%{_arch}%{?1:.%{1}} &&\
     /usr/bin/find . -type f | while read f; do\
       hardlink -c /usr/src/kernels/*.fc*.*/$f $f\
     done)\
fi\
%{nil}

# This macro defines a %%posttrans script for a kernel package.
#	%%kernel_variant_posttrans [<subpackage>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans() \
%{expand:%%posttrans %{?1}}\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --mkinitrd --dracut --depmod --update %{KVERREL}%{?1:.%{1}} || exit $?\
%{_sbindir}/new-kernel-pkg --package kernel%{?1:-%{1}} --rpmposttrans %{KVERREL}%{?1:.%{1}} || exit $?\
if [ -x /sbin/weak-modules ]\
then\
    /sbin/weak-modules --add-kernel %{KVERREL}%{?1:.%{1}} || exit $?\
fi\
%{nil}

#
# This macro defines a %%post script for a kernel package and its devel package.
#	%%kernel_variant_post [-v <subpackage>] [-r <replace>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(uv:r:) \
%{expand:%%kernel_devel_post %{!-u:%{?-v*}}}\
%{expand:%%kernel_variant_posttrans %{!-u:%{?-v*}}}\
%{expand:%%post %{!-u:%{?-v*}}}\
%{-r:\
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&\
   [ -f /etc/sysconfig/kernel ]; then\
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=%{-r*}$/DEFAULTKERNEL=kernel%{?-v:-%{-v*}}/' /etc/sysconfig/kernel || exit $?\
fi}\
if grep --silent '^hwcap 0 nosegneg$' /etc/ld.so.conf.d/kernel-*.conf 2> /dev/null; then\
  sed -i '/^hwcap 0 nosegneg$/ s/0/1/' /etc/ld.so.conf.d/kernel-*.conf\
fi\
%{_sbindir}/new-kernel-pkg --package kernel%{?-v:-%{-v*}} --install %{KVERREL}%{!-u:%{?-v:.%{-v*}}} || exit $?\
ln -sf /lib/firmware/%{rpmversion}-%{pkg_release} /lib/firmware/%{rpmversion}-%{pkg_release}.%{_target_cpu} \
%{nil}

#
# This macro defines a %%preun script for a kernel package.
#	%%kernel_variant_preun <subpackage>
#
%define kernel_variant_preun() \
%{expand:%%preun %{?1}}\
%{_sbindir}/new-kernel-pkg --rminitrd --rmmoddep --remove %{KVERREL}%{?1:.%{1}} || exit $?\
if [ -x /sbin/weak-modules ]\
then\
    /sbin/weak-modules --remove-kernel %{KVERREL}%{?1:.%{1}} || exit $?\
   rm -f /lib/firmware/%{rpmversion}-%{pkg_release}.%{_target_cpu} \
fi\
%{nil}

#
# This macro defines a %%pre script for a kernel package.
#	%%kernel_variant_pre <subpackage>
#
%define kernel_variant_pre() \
%{expand:%%pre %{?1}}\
message="Change references of /dev/hd in /etc/fstab to disk label"\
if [ -f /etc/fstab ]\
then\
awk '($2=="/boot")&&/^\\/dev\\/hd/{print $1}' /etc/fstab | egrep -q "^/dev/hd"\
bdretval=$?\
awk '($2=="/")&&/^\\/dev\\/hd/{print $1}' /etc/fstab | egrep -q "^/dev/hd"\
rdretval=$?\
awk '($2=="/boot")&&/^LABEL=/{print $1}' /etc/fstab | egrep -q "^LABEL="\
blretval=$?\
awk '($2=="/")&&/^LABEL=/{print $1}' /etc/fstab | egrep -q "^LABEL="\
rlretval=$?\
if [ $bdretval == 0 ] || [ $rdretval == 0 ]\
then\
echo -e $message\
exit 1\
elif [ $blretval == 0 ] && [ $rlretval == 0 ]\
then\
grep -v "^#" /etc/fstab | egrep -q "/dev/hd"\
if [ $? == 0 ]\
then\
echo -e $message\
fi\
elif [ $blretval == 0 ] && [ $rdretval != 0 ]\
then\
grep -v "^#" /etc/fstab | egrep -q "/dev/hd"\
if [ $? == 0 ]\
then\
echo -e $message\
fi\
elif [ $bdretval != 0 ] && [ $rlretval == 0 ]\
then\
grep -v "^#" /etc/fstab | egrep -q "/dev/hd"\
if [ $? == 0 ]\
then\
echo -e $message\
fi\
elif [ $bdretval != 0 ] && [ $rdretval != 0 ]\
then\
grep -v "^#" /etc/fstab | egrep -q "/dev/hd"\
if [ $? == 0 ]\
then\
echo -e $message\
fi\
fi\
fi\
%{nil}

%kernel_variant_pre
%kernel_variant_preun
%ifarch x86_64
%kernel_variant_post -u -v uek -r (kernel%{variant}|kernel%{variant}-debug|kernel-ovs)
%else
%kernel_variant_post -u -v uek -r (kernel%{variant}|kernel%{variant}-debug|kernel-ovs)
%endif

%kernel_variant_pre smp
%kernel_variant_preun smp
%kernel_variant_post -v smp

%kernel_variant_pre PAE
%kernel_variant_preun PAE
%kernel_variant_post -v PAE -r (kernel|kernel-smp|kernel-xen)

%kernel_variant_pre debug
%kernel_variant_preun debug
%kernel_variant_post -v debug

%kernel_variant_post -v PAEdebug -r (kernel|kernel-smp|kernel-xen)
%kernel_variant_preun PAEdebug
%kernel_variant_pre PAEdebug

if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

###
### file lists
###

%if %{with_headers}
%files headers
%defattr(-,root,root)
/usr/include/*
%endif

%if %{with_firmware}
%files firmware
%defattr(-,root,root)
/lib/firmware/*
%doc linux-%{version}-%{release}/firmware/WHENCE
%endif

%if %{with_bootwrapper}
%files bootwrapper
%defattr(-,root,root)
/usr/sbin/*
%{_libdir}/kernel-wrapper
%endif

# only some architecture builds need kernel-doc
%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation/*
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}/Documentation
%dir %{_datadir}/doc/kernel-doc-%{rpmversion}
%{_datadir}/man/man9/*
%endif

# This is %{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#	%%kernel_variant_files [-k vmlinux] <condition> <subpackage>
#
%define kernel_variant_files(k:) \
%if %{1}\
%{expand:%%files %{?2}}\
%defattr(-,root,root)\
/%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?2:.%{2}}\
%if %{with_fips} \
/%{image_install_path}/.vmlinuz-%{KVERREL}%{?2:.%{2}}.hmac \
%endif \
/boot/System.map-%{KVERREL}%{?2:.%{2}}\
/boot/symvers-%{KVERREL}%{?2:.%{2}}.gz\
/boot/config-%{KVERREL}%{?2:.%{2}}\
%dir /lib/modules/%{KVERREL}%{?2:.%{2}}\
/lib/modules/%{KVERREL}%{?2:.%{2}}/kernel\
/lib/modules/%{KVERREL}%{?2:.%{2}}/build\
/lib/modules/%{KVERREL}%{?2:.%{2}}/source\
/lib/modules/%{KVERREL}%{?2:.%{2}}/extra\
/lib/modules/%{KVERREL}%{?2:.%{2}}/updates\
/lib/modules/%{KVERREL}%{?2:.%{2}}/weak-updates\
%ifarch %{vdso_arches}\
/lib/modules/%{KVERREL}%{?2:.%{2}}/vdso\
/etc/ld.so.conf.d/kernel-%{KVERREL}%{?2:.%{2}}.conf\
%endif\
/lib/modules/%{KVERREL}%{?2:.%{2}}/modules.*\
/usr/libexec/perf.%{KVERREL}%{?2:.%{2}}\
/usr/sbin/perf\
%ifnarch sparc64\
/usr/libexec/x86_energy_perf_policy.%{KVERREL}%{?2:.%{2}}\
/usr/sbin/x86_energy_perf_policy\
/usr/libexec/turbostat.%{KVERREL}%{?2:.%{2}}\
/usr/sbin/turbostat\
%endif\
%ghost /boot/initramfs-%{KVERREL}%{?2:.%{2}}.img\
%{expand:%%files %{?2:%{2}-}devel}\
%defattr(-,root,root)\
%dir /usr/src/kernels\
%verify(not mtime) /usr/src/kernels/%{KVERREL}%{?2:.%{2}}\
/usr/src/kernels/%{KVERREL}%{?2:.%{2}}\
%if %{with_debuginfo}\
%ifnarch noarch\
%if %{fancy_debuginfo}\
%{expand:%%files -f debuginfo%{?2}.list %{?2:%{2}-}debuginfo}\
%else\
%{expand:%%files %{?2:%{2}-}debuginfo}\
%endif\
%defattr(-,root,root)\
%if !%{fancy_debuginfo}\
%if "%{elf_image_install_path}" != ""\
%{debuginfodir}/%{elf_image_install_path}/*-%{KVERREL}%{?2:.%{2}}.debug\
%endif\
%{debuginfodir}/lib/modules/%{KVERREL}%{?2:.%{2}}\
%{debuginfodir}/usr/src/kernels/%{KVERREL}%{?2:.%{2}}\
# % {debuginfodir}/usr/bin/%{KVERREL}%{?2:.%{2}}\
%endif\
%endif\
%endif\
%endif\
%{nil}


%kernel_variant_files %{with_up}
%kernel_variant_files %{with_smp} smp
%if %{with_up}
%kernel_variant_files %{with_debug} debug
%endif
%kernel_variant_files %{with_pae} PAE
%kernel_variant_files %{with_pae_debug} PAEdebug
%kernel_variant_files -k vmlinux %{with_kdump} kdump

%changelog
* Fri Mar 25 2016 Chuck Anderson <chuck.anderson@oracle.com> [4.1.12-32.2.3.el7uek] 
 - rebuild bumping release 

* Thu Mar 24 2016 Chuck Anderson <chuck.anderson@oracle.com> [4.1.12-32.2.2.el7uek] 
- x86/iopl/64: properly context-switch IOPL on Xen PV (Andy Lutomirski)  [Orabug: 22997978]  {CVE-2016-3157}
- fs/hugetlbfs/inode.c: fix bugs in hugetlb_vmtruncate_list() (Mike Kravetz)  [Orabug: 22667863]

* Sun Jan 31 2016 Chuck Anderson <chuck.anderson@oracle.com> [4.1.12-32.2.1.el7uek] 
 - rebuild bumping release 

* Fri Jan 29 2016 Chuck Anderson <chuck.anderson@oracle.com> [4.1.12-32.1.3.el7uek] 
- IPoIB: Protect tx_outstanding from parallel access (Wengang Wang)  [Orabug: 22217400]  
- xprtrdma: xprt_rdma_free() must not release backchannel reqs (Chuck Lever)  [Orabug: 22365704]  
- Revert "i40e: Set defport behavior for the Main VSI when in promiscuous mode" (Brian Maly)  [Orabug: 22519254]  
- block: bump BLK_DEF_MAX_SECTORS to 2560 (Jeff Moyer)  [Orabug: 22611290]  
- Revert "block: remove artifical max_hw_sectors cap" (Jeff Moyer)  [Orabug: 22611290]  

* Tue Jan 19 2016 Chuck Anderson <chuck.anderson@oracle.com> [4.1.12-32.1.2.el7uek] 
- KEYS: Fix keyring ref leak in join_session_keyring() (Yevgeny Pats)  [Orabug: 22563965]  {CVE-2016-0728} 

* Fri Jan 8 2016 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-32.1.1.el7uek] 
- ocfs2: return non-zero st_blocks for inline data (John Haxby)  [Orabug: 22218243]  
- xen/events/fifo: Consume unprocessed events when a CPU dies (Ross Lagerwall)  [Orabug: 22498877]  
- Revert "xen/fb: allow xenfb initialization for hvm guests" (Konrad Rzeszutek Wilk)   
- xen/pciback: Don't allow MSI-X ops if PCI_COMMAND_MEMORY is not set. (Konrad Rzeszutek Wilk)   
- xen/pciback: For XEN_PCI_OP_disable_msi[|x] only disable if device has MSI(X) enabled. (Konrad Rzeszutek Wilk)   
- xen/pciback: Do not install an IRQ handler for MSI interrupts. (Konrad Rzeszutek Wilk)   
- xen/pciback: Return error on XEN_PCI_OP_enable_msix when device has MSI or MSI-X enabled (Konrad Rzeszutek Wilk)   
- xen/pciback: Return error on XEN_PCI_OP_enable_msi when device has MSI or MSI-X enabled (Konrad Rzeszutek Wilk)   
- xen/pciback: Save xen_pci_op commands before processing it (Konrad Rzeszutek Wilk)   
- xen-scsiback: safely copy requests (David Vrabel)   
- xen-blkback: read from indirect descriptors only once (Roger Pau Monné)   
- xen-blkback: only read request operation from shared ring once (Roger Pau Monné)   
- xen-netback: use RING_COPY_REQUEST() throughout (David Vrabel)   
- xen-netback: don't use last request to determine minimum Tx credit (David Vrabel)   
- xen: Add RING_COPY_REQUEST() (David Vrabel)   

* Thu Dec 17 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-32.el7uek] 
- KEYS: Fix crash when attempt to garbage collect an uninstantiated keyring (David Howells)  [Orabug: 22373388]  {CVE-2015-7872} 
- KEYS: Fix race between key destruction and finding a keyring by name (David Howells)  [Orabug: 22373388]  

* Mon Dec 14 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-31.el7uek] 
- x86/efi: back-out bug fix 22353360 which causes efi regression (Dan Duval)  [Orabug: 22363222]  

* Sat Dec 12 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-30.el7uek] 
- conditionalize Secure Boot initialization on x86 platform (Dan Duval)  [Orabug: 22353360]  
- x86/efi: Set securelevel when loaded without efi stub (Dan Duval)  [Orabug: 22353360]  
- KVM: svm: unconditionally intercept #DB (Paolo Bonzini)  [Orabug: 22333633]  {CVE-2015-8104} 
- KVM: x86: work around infinite loop in microcode when #AC is delivered (Eric Northup)  [Orabug: 22333632]  {CVE-2015-5307} {CVE-2015-5307} 

* Fri Dec 11 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-29.el7uek] 
- uek-rpm: module signing key verification on sparc (Allen Pais)  [Orabug: 21900415]  
- scsi: Fix a bdi reregistration race (Bart Van Assche)  [Orabug: 22250360]  
- i40e: Fix for recursive RTNL lock during PROMISC change (Anjali Singhai)  [Orabug: 22328907]  
- KABI: padding optimization (Manjunath Govindashetty)   
- uek-rpm: rebuild module kabi list (Guru Anbalagane)   
- ib_core: Add udata argument to alloc_shpd() (Mukesh Kacker)  [Orabug: 21884873]  
- Revert "netlink: Fix autobind race condition that leads to zero port ID" (Dan Duval)  [Orabug: 22284865]  
- Revert "netlink: Replace rhash_portid with bound" (Dan Duval)  [Orabug: 22284865]  

* Wed Dec 9 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-28.el7uek] 
- ixgbe: make a workaround to tx hang issue under dom (Ethan Zhao)  [Orabug: 22171500]  
- mm-hugetlb-resv-map-memory-leak-for-placeholder-entries-v2 (Mike Kravetz)  [Orabug: 22302415]  
- mm/hugetlb.c: fix resv map memory leak for placeholder entries (Mike Kravetz)  [Orabug: 22302415]  
- Prevent syncing frozen file system (Tariq Saeed)  [Orabug: 22332381]  
- ocfs2: fix SGID not inherited issue (Junxiao Bi)   
- kbuild: Set objects.builtin dependency to bzImage for CONFIG_CTF (Jerry Snitselaar)  [Orabug: 17510915] [Orabug: 22329011]  

* Mon Dec 7 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-27.el7uek] 
- Do not execute i40e_macaddr_init if the macaddr is default (Sowmini Varadhan)   

* Wed Dec 2 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-26.el7uek] 
- dtrace: ensure return value of access_process_vm() is > 0 (Todd Vierling)  [Orabug: 22295336]  
- ocfs2: fix umask ignored issue (Junxiao Bi)   
- ksplice: correctly clear garbage on signal handling. (Jamie Iles)  [Orabug: 22194459]  

* Wed Nov 25 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-25.el7uek] 
- NFSoRDMA: for local permissions, pull lkey value from the correct ib_mr (Todd Vierling)  [Orabug: 22202841]  
- Revert "nfs: take extra reference to fl->fl_file when running a LOCKU operation" (Dan Duval)  [Orabug: 22186705]  

* Fri Nov 20 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-24.el7uek] 
- uek-rpm: builds: Enable kabi check (Manjunath Govindashetty)  [Orabug: 21882206]  
- uek-rpm: builds: generate module kabi files (Guru Anbalagane)  [Orabug: 17437969]  
- uek-rpm: builds: add kabi whitelist debug version (Santosh Shilimkar)   
- uek-rpm: builds: add kabi name tags (Guru Anbalagane)  [Orabug: 17437969]  
- uek-rpm: builds: Add kabi whitelist (Guru Anbalagane)  [Orabug: 17437969]  
- mm-hugetlbfs-fix-bugs-in-fallocate-hole-punch-of-areas-with-holes-v3 (Mike Kravetz)  [Orabug: 22220400]  
- mm/hugetlbfs: fix bugs in fallocate hole punch of areas with holes (Mike Kravetz)  [Orabug: 22220400]  
- btrfs: Print Warning only if ENOSPC_DEBUG is enabled (Ashish Samant)  [Orabug: 21626666]  
- rtnetlink: RTEXT_FILTER_SKIP_STATS support to avoid dumping inet/inet6 stats (Sowmini Varadhan)  [Orabug: 21857538]  
- pci: Limit VPD length for megaraid_sas adapter (Babu Moger)  [Orabug: 22104511]  
- uek-rpm: configs: change the x86_64 default governor to ondemand (Todd Vierling)  [Orabug: 21910845]  
- uek-rpm: configs: sync up the EFIVAR_FS between ol6 and ol7 (Santosh Shilimkar)  [Orabug: 21806900]  
- KABI Padding to allow future extensions (Manjunath Govindashetty)  [Orabug: 22227652]  
- uek-rpm: use the latest 0.5 version of linux-firmware (Santosh Shilimkar)  [Orabug: 22227047]  
- dtrace: fire proc:::signal-send for queued signals too (Nick Alcock)  [Orabug: 22027302]  
- dtrace: correct signal-handle probe semantics (Kris Van Hees)  [Orabug: 21974641]  
- dtrace: remove trailing space in psargs (Kris Van Hees)  [Orabug: 21974606]  

* Fri Nov 13 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-23.el7uek] 
- mm: do not ignore mapping_gfp_mask in page cache allocation paths (Michal Hocko)  [Orabug: 22066703]  
- PCI: Set SR-IOV NumVFs to zero after enumeration (Bjorn Helgaas)  [Orabug: 21547430]  
- virtio-net: drop NETIF_F_FRAGLIST (Jason Wang)  [Orabug: 22154074]  {CVE-2015-5156} 
- blk-mq: avoid excessive boot delays with large lun counts (Jeff Moyer)  [Orabug: 21879600]  
- RDS: establish connection for legitimate remote RDMA message (Santosh Shilimkar)  [Orabug: 22139696]  
- rds: remove the _reuse_ rds ib pool statistics (Wengang Wang)  [Orabug: 22124214]  
- RDS: Add support for per socket SO_TIMESTAMP for incoming messages (Santosh Shilimkar)  [Orabug: 22190837]  
- KABI PADDING FOR ORACLE SPECIFIC FUTURE EXTENSIONS (Manjunath Govindashetty)   
- uek-rpm: configs: Sparc64: enable RDS modules (Allen Pais)  [Orabug: 22194248]  
-     SPARC64: UEK4 LDOMS DOMAIN SERVICES UPDATE 1 (Aaron Young)  [Orabug: 22185080]  
- i40e: Look up MAC address in Open Firmware or IDPROM (Sowmini Varadhan)   
- RDS: Fix out-of-order RDS_CMSG_RDMA_SEND_STATUS (Wei Lin Guay)  [Orabug: 22126982]  
- uek-rpm: ol7: update linux-firmware dependency to 20140911-0.1.git365e80c.0.4 (Dan Duval)  [Orabug: 22146380]  
- uek-rpm: configs: disable PS2_VMMOUSE to avoid vmware platform breakage (Santosh Shilimkar)  [Orabug: 22166599]  
- uek-rpm: configs: ol7: don't set EFI_VARS_PSTORE_DEFAULT_DISABLE (Santosh Shilimkar)  [Orabug: 21806900]  
- Disable VLAN 0 tagging for none VLAN traffic (Brian Maly)  [Orabug: 22074114]  
- Integrate Uvnic functionality into uek-4.1 Revision 8008 (Pradeep Gopanapalli)   
- 1) S_IRWXU causing kernel soft crash changing to 0644 WARNING: CPU: 0 PID: 20907 at fs/sysfs/group.c:61 create_files+0x171/0x180() Oct 12 21:43:14 ovn87-180 kernel: [252606.588541] Attribute vhba_default_scsi_timeout: Invalid permissions 0700 [Rev 8008] (Pradeep Gopanapalli)   
- 1) Support vnic for EDR based platform(uVnic) 2) Supported Types now Type 0 - XSMP_XCM_OVN - Xsigo VP780/OSDN standalone Chassis, (add pvi) Type 1 - XSMP_XCM_NOUPLINK - EDR Without uplink (add public-network) Type 2 - XSMP_XCM_UPLINK -EDR with uplink (add public-network <with -if> 3) Intelligence in driver to support all the modes 4) Added Code for printing Multicast LID [Revision 8008] 5) removed style errors (Pradeep Gopanapalli)   
- sparc64, vdso: update the CLOCK_MONOTONIC_COARSE clock (Nick Alcock)  [Orabug: 22137842]  
- net/rds: start rdma listening after ib/iw initialization is done (Qing Huang)  [Orabug: 21684447]  

* Tue Nov 3 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.12-22.el7uek] 
- uek-rpm: builds: add dependency on latest linux-firmware package (Dan Duval)  [Orabug: 22084583]  
- uek-rpm: build: Update the base release to 12 with stable v4.1.12 (Santosh Shilimkar)   
- Linux 4.1.12 (Greg Kroah-Hartman)   
- sched/preempt, powerpc, kvm: Use need_resched() instead of should_resched() (Konstantin Khlebnikov)   
- sched/preempt, xen: Use need_resched() instead of should_resched() (Konstantin Khlebnikov)   
- nfs4: have do_vfs_lock take an inode pointer (Jeff Layton)   
- locks: inline posix_lock_file_wait and flock_lock_file_wait (Jeff Layton)   
- locks: new helpers - flock_lock_inode_wait and posix_lock_inode_wait (Jeff Layton)   
- locks: have flock_lock_file take an inode pointer instead of a filp (Jeff Layton)   
- svcrdma: handle rdma read with a non-zero initial page offset (Steve Wise)   
- arm64: Fix THP protection change logic (Steve Capper)   
- pinctrl: imx25: ensure that a pin with id i is at position i in the info array (Uwe Kleine-König)   
- sched/preempt: Fix cond_resched_lock() and cond_resched_softirq() (Konstantin Khlebnikov)   
- sched/preempt: Rename PREEMPT_CHECK_OFFSET to PREEMPT_DISABLE_OFFSET (Frederic Weisbecker)   
- rbd: fix double free on rbd_dev->header_name (Ilya Dryomov)   
- dm thin: fix missing pool reference count decrement in pool_ctr error path (Mike Snitzer)   
- drm/radeon: add pm sysfs files late (Alex Deucher)   
- drm/radeon: attach tile property to mst connector (Dave Airlie)   
- drm/dp/mst: make mst i2c transfer code more robust. (Dave Airlie)   
- drm/nouveau/fbcon: take runpm reference when userspace has an open fd (Ben Skeggs)   
- workqueue: make sure delayed work run in local cpu (Shaohua Li)   
- i2c: designware-platdrv: enable RuntimePM before registering to the core (Wolfram Sang)   
- i2c: designware: Do not use parameters from ACPI on Dell Inspiron 7348 (Mika Westerberg)   
- i2c: s3c2410: enable RuntimePM before registering to the core (Wolfram Sang)   
- i2c: rcar: enable RuntimePM before registering to the core (Wolfram Sang)   
- mfd: max77843: Fix max77843_chg_init() return on error (Javier Martinez Canillas)   
- nfsd/blocklayout: accept any minlength (Christoph Hellwig)   
- arm64: errata: use KBUILD_CFLAGS_MODULE for erratum #843419 (Will Deacon)   
- btrfs: fix use after free iterating extrefs (Chris Mason)   
- btrfs: check unsupported filters in balance arguments (David Sterba)   
- memcg: convert threshold to bytes (Shaohua Li)   
- crypto: ahash - ensure statesize is non-zero (Russell King)   
- crypto: sparc - initialize blkcipher.ivsize (Dave Kleikamp)   
- drm: Fix locking for sysfs dpms file (Daniel Vetter)   
- net/unix: fix logic about sk_peek_offset (Andrey Vagin)   
- af_unix: return data from multiple SKBs on recv() with MSG_PEEK flag (Aaron Conole)   
- af_unix: Convert the unix_sk macro to an inline function for type safety (Aaron Conole)   
- netlink: Trim skb to alloc size to avoid MSG_TRUNC (Arad, Ronen)   
- tipc: move fragment importance field to new header position (Jon Paul Maloy)   
- ethtool: Use kcalloc instead of kmalloc for ethtool_get_strings (Joe Perches)   
- act_mirred: clear sender cpu before sending to tx (WANG Cong)   
- ovs: do not allocate memory from offline numa node (Konstantin Khlebnikov)   
- bpf: fix panic in SO_GET_FILTER with native ebpf programs (Daniel Borkmann)   
- inet: fix race in reqsk_queue_unlink() (Eric Dumazet)   
- ppp: don't override sk->sk_state in pppoe_flush_dev() (Guillaume Nault)   
- net: add pfmemalloc check in sk_add_backlog() (Eric Dumazet)   
- inet: fix races in reqsk_queue_hash_req() (Eric Dumazet)   
- skbuff: Fix skb checksum partial check. (Pravin B Shelar)   
- skbuff: Fix skb checksum flag on skb pull (Pravin B Shelar)   
- l2tp: protect tunnel->del_work by ref_count (Alexander Couzens)   
- net/ibm/emac: bump version numbers for correct work with ethtool (Ivan Mikhaylov)   
- Linux 4.1.11 (Greg Kroah-Hartman)   
- 3w-9xxx: don't unmap bounce buffered commands (Christoph Hellwig)   
- MIPS: Fix console output for Fulong2e system (Guenter Roeck)   
- mm/slab: fix unexpected index mapping result of kmalloc_size(INDEX_NODE+1) (Joonsoo Kim)   
- intel_pstate: Fix overflow in busy_scaled due to long delay (Prarit Bhargava)   
- serial: atmel: fix error path of probe function (Uwe Kleine-König)   
- serial: 8250: add uart_config entry for PORT_RT2880 (Mans Rullgard)   
- drivers/tty: require read access for controlling terminal (Jann Horn)   
- tty: fix stall caused by missing memory barrier in drivers/tty/n_tty.c (Kosuke Tatsukawa)   
- staging: speakup: fix speakup-r regression (covici@ccs.covici.com)   
- dm cache: fix NULL pointer when switching from cleaner policy (Joe Thornber)   
- dm: fix AB-BA deadlock in __dm_destroy() (Junichi Nomura)   
- namei: results of d_is_negative() should be checked after dentry revalidation (Trond Myklebust)   
- clk: ti: fix dual-registration of uart4_ick (Ben Dooks)   
- nfs/filelayout: Fix NULL reference caused by double freeing of fh_array (Kinglong Mee)   
- fix a braino in ovl_d_select_inode() (Al Viro)   
- overlayfs: Make f_path always point to the overlay and f_inode to the underlay (David Howells)   
- overlay: Call ovl_drop_write() earlier in ovl_dentry_open() (David Howells)   
- md/bitmap: don't pass -1 to bitmap_storage_alloc. (NeilBrown)   
- genirq: Fix race in register_irq_proc() (Ben Hutchings)   
- igb: do not re-init SR-IOV during probe (Stefan Assmann)   
- net/xen-netfront: only napi_synchronize() if running (Chas Williams)   
- m68k: Define asmlinkage_protect (Andreas Schwab)   
- arm64: readahead: fault retry breaks mmap file read random detection (Mark Salyzyn)   
- arm64: ftrace: fix function_graph tracer panic (Li Bin)   
- arm64/efi: Fix boot crash by not padding between EFI_MEMORY_RUNTIME regions (Ard Biesheuvel)   
- vfs: Test for and handle paths that are unreachable from their mnt_root (Eric W. Biederman)   
- dcache: Handle escaped paths in prepend_path (Eric W. Biederman)   
- mmc: core: Don't return an error for CD/WP GPIOs when GPIOLIB is unset (Ulf Hansson)   
- mmc: sdhci: fix dma memory leak in sdhci_pre_req() (Haibo Chen)   
- UBI: return ENOSPC if no enough space available (shengyong)   
- UBI: Validate data_size (Richard Weinberger)   
- UBIFS: Kill unneeded locking in ubifs_init_security (Richard Weinberger)   
- inet: fix potential deadlock in reqsk_queue_unlink() (Eric Dumazet)   
- rsi: Fix possible leak when loading firmware (Christian Engelmayer)   
- powerpc/MSI: Fix race condition in tearing down MSI interrupts (Paul Mackerras)   
- tools lib traceevent: Fix string handling in heterogeneous arch environments (Kapileshwar Singh)   
- batman-adv: Fix potentially broken skb network header access (Linus Lüssing)   
- batman-adv: Fix potential synchronization issues in mcast tvlv handler (Linus Lüssing)   
- batman-adv: Make MCAST capability changes atomic (Linus Lüssing)   
- batman-adv: Make TT capability changes atomic (Linus Lüssing)   
- batman-adv: Make NC capability changes atomic (Linus Lüssing)   
- MIPS: dma-default: Fix 32-bit fall back to GFP_DMA (James Hogan)   
- cpufreq: dt: Tolerance applies on both sides of target voltage (Viresh Kumar)   
- cpu/cacheinfo: Fix teardown path (Borislav Petkov)   
- USB: Add reset-resume quirk for two Plantronics usb headphones. (Yao-Wen Mao)   
- usb: Add device quirk for Logitech PTZ cameras (Vincent Palatin)   
- USB: chaoskey read offset bug (Alexander Inyukhin)   
- usb: musb: cppi41: allow it to work again (Felipe Balbi)   
- usb: phy: phy-generic: Fix reset behaviour on legacy boot (Roger Quadros)   
- usb: Use the USB_SS_MULT() macro to get the burst multiplier. (Mathias Nyman)   
- usb: chipidea: udc: using the correct stall implementation (Peter Chen)   
- usb: musb: dsps: fix polling in device-only mode (Bin Liu)   
- security: fix typo in security_task_prctl (Jann Horn)   
- regmap: debugfs: Don't bother actually printing when calculating max length (Mark Brown)   
- regmap: debugfs: Ensure we don't underflow when printing access masks (Mark Brown)   
- ipr: Enable SIS pipe commands for SIS-32 devices. (Gabriel Krisman Bertazi)   
- pcmcia: sa11x0: fix missing clk_put() in sa11x0 socket drivers (Russell King)   
- ath10k: reject 11b tx fragmentation configuration (Michal Kazior)   
- device property: fix potential NULL pointer dereference (Andy Shevchenko)   
- PM / AVS: rockchip-io: depend on CONFIG_POWER_AVS (Heiko Stuebner)   
- mtd: nand: sunxi: fix OOB handling in ->write_xxx() functions (Boris BREZILLON)   
- mtd: nand: sunxi: fix sunxi_nand_chips_cleanup() (Boris BREZILLON)   
- mtd: pxa3xx_nand: add a default chunk size (Antoine Ténart)   
- docs: update HOWTO for 3.x -> 4.x versioning (Mario Carrillo)   
- irqchip/gic-v3-its: Add missing cache flushes (Marc Zyngier)   
- irqchip/atmel-aic5: Use per chip mask caches in mask/unmask() (Ludovic Desroches)   
- cifs: use server timestamp for ntlmv2 authentication (Peter Seiderer)   
- usb: chipidea: imx: fix a typo for imx6sx (Li Jun)   
- dts: imx25: fix sd card gpio polarity specified in device tree (Dong Aisheng)   
- dts: imx53: fix sd card gpio polarity specified in device tree (Dong Aisheng)   
- dts: imx51: fix sd card gpio polarity specified in device tree (Dong Aisheng)   
- mmc: sdhci-esdhc-imx: fix cd regression for dt platform (Dong Aisheng)   
- mmc: sdhci-esdhc-imx: Do not break platform data boards (Fabio Estevam)   
- mmc: sdhci-esdhc-imx: Move mmc_of_parse() to the dt probe (Fabio Estevam)   
- mmc: dw_mmc: handle data blocks > than 4kB if IDMAC is used (Alexey Brodkin)   
- batman-adv: Make DAT capability changes atomic (Linus Lüssing)   
- batman-adv: protect tt_local_entry from concurrent delete events (Marek Lindner)   
- batman-adv: fix kernel crash due to missing NULL checks (Marek Lindner)   
- fbdev: select versatile helpers for the integrator (Linus Walleij)   
- ipvs: call skb_sender_cpu_clear (Julian Anastasov)   
- ipvs: fix crash with sync protocol v0 and FTP (Julian Anastasov)   
- ipvs: skb_orphan in case of forwarding (Alex Gartrell)   
- ipvs: fix crash if scheduler is changed (Julian Anastasov)   
- ipvs: do not use random local source address for tunnels (Julian Anastasov)   
- serial/amba-pl011: Disable interrupts around TX softirq (Dave Martin)   
- sched/fair: Prevent throttling in early pick_next_task_fair() (Ben Segall)   
- Initialize msg/shm IPC objects before doing ipc_addid() (Linus Torvalds)   
- usb: xhci: Add support for URB_ZERO_PACKET to bulk/sg transfers (Reyad Attiyat)   
- xhci: init command timeout timer earlier to avoid deleting it uninitialized (Mathias Nyman)   
- xhci: change xhci 1.0 only restrictions to support xhci 1.1 (Mathias Nyman)   
- usb: xhci: exit early in xhci_setup_device() if we're halted or dying (Roger Quadros)   
- usb: xhci: Clear XHCI_STATE_DYING on start (Roger Quadros)   
- usb: xhci: lock mutex on xhci_stop (Roger Quadros)   
- xhci: give command abortion one more chance before killing xhci (Mathias Nyman)   
- USB: whiteheat: fix potential null-deref at probe (Johan Hovold)   {CVE-2015-5257} 
- drm/dp/mst: drop cancel work sync in the mstb destroy path (v2) (Dave Airlie)   
- drm/radeon: Restore LCD backlight level on resume (>= R5xx) (Michel Dänzer)   
- drm: Reject DRI1 hw lock ioctl functions for kms drivers (Daniel Vetter)   
- drm/i915/bios: handle MIPI Sequence Block v3+ gracefully (Jani Nikula)   
- drm/qxl: recreate the primary surface when the bo is not primary (Fabiano Fidêncio)   
- drm/qxl: only report first monitor as connected if we have no state (Dave Airlie)   
- Do not fall back to SMBWriteX in set_file_size error cases (Steve French)   
- disabling oplocks/leases via module parm enable_oplocks broken for SMB3 (Steve French)   
- Fix sec=krb5 on smb3 mounts (Steve French)   
- NFS: Fix a write performance regression (Trond Myklebust)   
- nfs: fix pg_test page count calculation (Peng Tao)   
- NFS: Do cleanup before resetting pageio read/write to mds (Kinglong Mee)   
- Bluetooth: Delay check for conn->smp in smp_conn_security() (Johan Hedberg)   
- netfilter: nf_log: don't zap all loggers on unregister (Florian Westphal)   
- netfilter: nft_compat: skip family comparison in case of NFPROTO_UNSPEC (Pablo Neira Ayuso)   
- netfilter: nf_log: wait for rcu grace after logger unregistration (Pablo Neira Ayuso)   
- netfilter: nftables: Do not run chains in the wrong network namespace (Eric W. Biederman)   
- netfilter: nf_qeueue: Drop queue entries on nf_unregister_hook (Eric W. Biederman)   
- netfilter: ctnetlink: put back references to master ct and expect objects (Pablo Neira Ayuso)   
- netfilter: nf_conntrack: Support expectations in different zones (Joe Stringer)   
- netfilter: nf_tables: Use 32 bit addressing register from nft_type_to_reg() (Pablo Neira Ayuso)   
- netfilter: nfnetlink: work around wrong endianess in res_id field (Pablo Neira Ayuso)   
- dm raid: fix round up of default region size (Mikulas Patocka)   
- md/raid0: apply base queue limits *before* disk_stack_limits (NeilBrown)   
- md/raid0: update queue parameter in a safer location. (NeilBrown)   
- USB: option: add ZTE PIDs (Liu.Zhao)   
- staging: ion: fix corruption of ion_import_dma_buf (Shawn Lin)   
- dm btree: add ref counting ops for the leaves of top level btrees (Joe Thornber)   
- svcrdma: Fix send_reply() scatter/gather set-up (Chuck Lever)   
- ath10k: fix dma_mapping_error() handling (Michal Kazior)   
- dm crypt: constrain crypt device's max_segment_size to PAGE_SIZE (Mike Snitzer)   
- PCI: Clear IORESOURCE_UNSET when clipping a bridge window (Bjorn Helgaas)   
- PCI: Use function 0 VPD for identical functions, regular VPD for others (Alex Williamson)   
- PCI: Fix devfn for VPD access through function 0 (Alex Williamson)   
- Btrfs: update fix for read corruption of compressed and shared extents (Filipe Manana)   
- Btrfs: fix read corruption of compressed and shared extents (Filipe Manana)   
- btrfs: skip waiting on ordered range for special files (Jeff Mahoney)   
- ASoC: sgtl5000: fix wrong register MIC_BIAS_VOLTAGE setup on probe (Gianluca Renzi)   
- ASoC: db1200: Fix DAI link format for db1300 and db1550 (Lars-Peter Clausen)   
- ASoC: dwc: correct irq clear method (Yitian Bu)   
- ASoC: fix broken pxa SoC support (Robert Jarzmik)   
- ASoC: pxa: pxa2xx-ac97: fix dma requestor lines (Robert Jarzmik)   
- ALSA: hda - Disable power_save_node for IDT 92HD73xx chips (Takashi Iwai)   
- ALSA: hda - Apply SPDIF pin ctl to MacBookPro 12,1 (John Flatness)   
- ALSA: hda: Add dock support for ThinkPad T550 (Laura Abbott)   
- ALSA: synth: Fix conflicting OSS device registration on AWE32 (Takashi Iwai)   
- ALSA: hda - Disable power_save_node for Thinkpads (Takashi Iwai)   
- mm: hugetlbfs: skip shared VMAs when unmapping private pages to satisfy a fault (Mel Gorman)   
- ocfs2/dlm: fix deadlock when dispatch assert master (Joseph Qi)   
- lib/iommu-common.c: do not try to deref a null iommu->lazy_flush() pointer when n < pool->hint (Sowmini Varadhan)   
- mm: migrate: hugetlb: putback destination hugepage to active list (Naoya Horiguchi)   
- spi: spidev: fix possible NULL dereference (Sudip Mukherjee)   
- spi: spi-pxa2xx: Check status register to determine if SSSR_TINT is disabled (Tan, Jui Nee)   
- spi: xtensa-xtfpga: fix register endianness (Max Filippov)   
- spi: Fix documentation of spi_alloc_master() (Guenter Roeck)   
- s390/boot/decompression: disable floating point in decompressor (Christian Borntraeger)   
- s390/compat: correct uc_sigmask of the compat signal frame (Martin Schwidefsky)   
- sched/core: Fix TASK_DEAD race in finish_task_switch() (Peter Zijlstra)   
- leds/led-class: Add missing put_device() (Ricardo Ribalda Delgado)   
- x86/xen: Support kexec/kdump in HVM guests by doing a soft reset (Vitaly Kuznetsov)   
- x86/mm: Set NX on gap between __ex_table and rodata (Stephen Smalley)   
- x86/process: Add proper bound checks in 64bit get_wchan() (Thomas Gleixner)   
- x86/kexec: Fix kexec crash in syscall kexec_file_load() (Lee, Chun-Yi)   
- x86/efi: Fix boot crash by mapping EFI memmap entries bottom-up at runtime, instead of top-down (Matt Fleming)   
- Use WARN_ON_ONCE for missing X86_FEATURE_NRIPS (Dirk Müller)   
- x86/nmi/64: Fix a paravirt stack-clobbering bug in the NMI code (Andy Lutomirski)   
- x86/paravirt: Replace the paravirt nop with a bona fide empty function (Andy Lutomirski)   
- x86/platform: Fix Geode LX timekeeping in the generic x86 build (David Woodhouse)   
- x86/alternatives: Make optimize_nops() interrupt safe and synced (Thomas Gleixner)   
- x86/apic: Serialize LVTT and TSC_DEADLINE writes (Shaohua Li)   
- dmaengine: dw: properly read DWC_PARAMS register (Andy Shevchenko)   
- blockdev: don't set S_DAX for misaligned partitions (Jeff Moyer)   
- ARM: dts: fix usb pin control for imx-rex dts (Felipe F. Tonello)   
- ARM: EXYNOS: reset Little cores when cpu is up (Chanho Park)   
- ARM: dts: omap3-beagle: make i2c3, ddc and tfp410 gpio work again (Carl Frederik Werner)   
- ARM: dts: omap5-uevm.dts: fix i2c5 pinctrl offsets (Grazvydas Ignotas)   
- ARM: 8425/1: kgdb: Don't try to stop the machine when setting breakpoints (Doug Anderson)   
- windfarm: decrement client count when unregistering (Paul Bolle)   
- ARM: 8429/1: disable GCC SRA optimization (Ard Biesheuvel)   
- ARM: fix Thumb2 signal handling when ARMv6 is enabled (Russell King)   
- hwmon: (nct6775) Swap STEP_UP_TIME and STEP_DOWN_TIME registers for most chips (Guenter Roeck)   
- sched: access local runqueue directly in single_task_running (Dominik Dingel)   
- watchdog: sunxi: fix activation of system reset (Francesco Lavra)   
- perf: Fix AUX buffer refcounting (Peter Zijlstra)   
- perf header: Fixup reading of HEADER_NRCPUS feature (Arnaldo Carvalho de Melo)   
- perf tools: Add empty Build files for architectures lacking them (Ben Hutchings)   
- perf stat: Get correct cpu id for print_aggr (Kan Liang)   
- perf hists: Update the column width for the "srcline" sort key (Arnaldo Carvalho de Melo)   
- perf tools: Fix copying of /proc/kcore (Adrian Hunter)   
- perf/x86/intel: Fix constraint access (Peter Zijlstra)   
- toshiba_acpi: Fix hotkeys registration on some toshiba models (Azael Avalos)   
- target: Fix v4.1 UNIT_ATTENTION se_node_acl->device_list[] NULL pointer (Nicholas Bellinger)   
- iser-target: Put the reference on commands waiting for unsol data (Jenny Derzhavetz)   
- iser-target: remove command with state ISTATE_REMOVE (Jenny Derzhavetz)   
- target: Attach EXTENDED_COPY local I/O descriptors to xcopy_pt_sess (Nicholas Bellinger)   
- scsi: fix scsi_error_handler vs. scsi_host_dev_release race (Michal Hocko)   
- target/iscsi: Fix np_ip bracket issue by removing np_ip (Andy Grover)   
- time: Fix timekeeping_freqadjust()'s incorrect use of abs() instead of abs64() (John Stultz)   
- KVM: PPC: Book3S HV: Pass the correct trap argument to kvmhv_commence_exit (Gautham R. Shenoy)   
- KVM: PPC: Book3S: Take the kvm->srcu lock in kvmppc_h_logical_ci_load/store() (Thomas Huth)   
- arm: KVM: Disable virtual timer even if the guest is not using it (Marc Zyngier)   
- kvm: fix double free for fast mmio eventfd (Jason Wang)   
- kvm: factor out core eventfd assign/deassign logic (Jason Wang)   
- kvm: fix zero length mmio searching (Jason Wang)   
- kvm: don't try to register to KVM_FAST_MMIO_BUS for non mmio eventfd (Jason Wang)   
- KVM: vmx: fix VPID is 0000H in non-root operation (Wanpeng Li)   
- arm: KVM: Fix incorrect device to IPA mapping (Marek Majtyka)   

* Fri Oct 30 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.10-21.el7uek] 
- IB/mlx4: Use vmalloc for WR buffers when needed (Wengang Wang)  [Orabug: 22025570]  
- i40e: relax fw api minor version for fortville 4 nvm image (Brian Maly)  [Orabug: 22074738]  
- crypto: testmgr - Disable fips-allowed for authenc() and des() ciphers (John Haxby)  [Orabug: 21863123]  
- Revert "ocfs2: change ip_unaligned_aio to of type mutex from atomit_t" (Ryan Ding)   
- ocfs2: fix a performance issue with synced buffer io (Ryan Ding)   
- xen-netfront: update num_queues to real created (Joe Jin)  [Orabug: 22069665]  
- xen-blkfront: check for null drvdata in blkback_changed (XenbusStateClosing) (Cathy Avery)  [Orabug: 21935345]  

* Fri Oct 23 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.10-20.el7uek] 
- qlcnic: Fix mailbox completion handling in spurious interrupt (Rajesh Borundia)  [Orabug: 22066190]  
- qlcnic: Update version to 5.3.63 (Shahed Shaikh)  [Orabug: 22066190]  
- qlcnic: Don't use kzalloc unncecessarily for allocating large chunk of memory (Shahed Shaikh)  [Orabug: 22066190]  
- qlcnic: Add new VF device ID 0x8C30 (Shahed Shaikh)  [Orabug: 22066190]  
- qlcnic: Print firmware minidump buffer and template header addresses (Shahed Shaikh)  [Orabug: 22066190]  
- qlcnic: Add support to enable capability to extend minidump for iSCSI (Shahed Shaikh)  [Orabug: 22066190]  
- qlcnic: Rearrange ordering of header files inclusion (Harish Patil)  [Orabug: 22066190]  
- qlcnic: Fix corruption while copying (Shahed Shaikh)  [Orabug: 22066190]  
- net: qlcnic: Deletion of unnecessary memset (Christophe Jaillet)  [Orabug: 22066190]  
- net: qlcnic: clean up sysfs error codes (Vladimir Zapolskiy)  [Orabug: 22066190]  
- qlcnic: sysfs interface for PCI BAR access (Sony Chacko)  [Orabug: 22066190]  
- bnx2fc: Update driver version to 2.9.6. (Chad Dupuis)  [Orabug: 22013781]  
- bnx2fc: Add HZ to task management timeout. (Chad Dupuis)  [Orabug: 22013781]  
- bnx2fc: Remove explicit logouts. (Chad Dupuis)  [Orabug: 22013781]  
- bnx2fc: Fix FCP RSP residual parsing. (Chad Dupuis)  [Orabug: 22013781]  
- bnx2fc: Set ELS transfer length correctly for middle path commands. (Chad Dupuis)  [Orabug: 22013781]  
- bnx2fc: Remove 'NetXtreme II' from source files. (Chad Dupuis)  [Orabug: 22013781]  
- bnx2fc: Update copyright for 2015. (Chad Dupuis)  [Orabug: 22013781]  
- bnx2fc: Read npiv table from nvram and create vports. (Chad Dupuis)  [Orabug: 22013781]  
- cnic: Add the interfaces to get FC-NPIV table. (Chad Dupuis)  [Orabug: 22013781]  

* Thu Oct 22 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.10-19.el7uek] 
- bonding: fix merge issue introduced by 21844825. (Rama Nichanamatlu)  [Orabug: 22025692]  
- bnx2i: Fix call trace while device reset (Nilesh Javali)  [Orabug: 22066191]  
- bnx2i: Fixed firmware assert, during target logout. (Tej Parkash)  [Orabug: 22066191]  
- export host-only net/core and net/ipv4 parameters to a container as read-only (Thomas Tanaka)  [Orabug: 21880402]  
- net/rds: start rdma listening after ib/iw initialization is done (Qing Huang)  [Orabug: 21684447]  
- fnic: Updating fnic driver version. (Jason Luo)  [Orabug: 22049739]  
- fnic: fix for fnic crash when blk-mq enabled in UEK4 (Jason Luo)  [Orabug: 22049739]  
- sparc: Accommodate mem64_offset != mem_offset in pbm configuration (Allen Pais)  [Orabug: 21826746]  
- RDS-TCP: Reset tcp callbacks if re-using an outgoing socket in rds_tcp_accept_one() (Sowmini Varadhan)  [Orabug: 22012202]  
- RDS: Invoke ->laddr_check() in rds_bind() for explicitly bound transports. (Sowmini Varadhan)  [Orabug: 22012202]  
- RDS: rds_conn_lookup() should factor in the struct net for a match (Sowmini Varadhan)  [Orabug: 22012202]  
- RDS: Use a single TCP socket for both send and receive. (Sowmini Varadhan)  [Orabug: 22012202]  
- RDS-TCP: Do not bloat sndbuf/rcvbuf in rds_tcp_tune (Sowmini Varadhan)  [Orabug: 22012202]  
- RDS-TCP: Set up MSG_MORE and MSG_SENDPAGE_NOTLAST as appropriate in rds_tcp_ (Sowmini Varadhan)  [Orabug: 22012202]  
- Revert "rds_rdma: rds_sendmsg should return EAGAIN if connection not setup" (Rama Nichanamatlu)  [Orabug: 21664735]  
- rds: make sure base connection is up on both sides (Ajaykumar Hotchandani)  [Orabug: 21675157]  
- rds_ib/iw: fixed big endianness conversion issue for dp->dp_ack_seq (Qing Huang)  [Orabug: 21684819]  
- RDS: fix race condition when sending a message on unbound socket. (Quentin Casasnovas)   {CVE-2015-6937} 
- RDS: verify the underlying transport exists before creating a connection (Sasha Levin)  [Orabug: 22010933]  
- mlx4: indicate memory resource exhaustion (Ajaykumar Hotchandani)  [Orabug: 21549767]  
- IB/mlx4: Use correct order of variables in log message (Wengang Wang)  [Orabug: 21906781]  
- mlx4_core: Introduce restrictions for PD update (Ajaykumar Hotchandani)   
- uek-rpm: configs: sparc64: enable rds module (Allen Pais)  [Orabug: 22068201]  
- uek-rpm: configs: sparc64: enable dtrace support (Allen Pais)   
- mpt3sas : Bump mpt3sas driver version to 9.100.00.00 (Sreekanth Reddy)   
- mpt3sas: When device is blocked followed by unblock fails, unfreeze the I/Os (Sreekanth Reddy)   
- mpt3sas: Call dma_mapping_error() API after mapping an address with dma_map_single() API (Sreekanth Reddy)   
- mpt3sas: Use alloc_ordered_workqueue() API instead of create_singlethread_workqueue() API (Sreekanth Reddy)   
- mpt3sas: Added support for customer specific branding (Sreekanth Reddy)   
- mpt3sas: Return host busy error status to SML when DMA mapping of scatter gather list fails for a SCSI command (Sreekanth Reddy)   
- mpt3sas: Complete the SCSI command with DID_RESET status for log_info value 0x0x32010081 (Sreekanth Reddy)   
- mpt3sas: MPI 2.5 Rev K (2.5.6) specifications (Sreekanth Reddy)   
- mpt3sas: Bump mpt3sas driver version to v6.100.00.00 (Sreekanth Reddy)   
- mpt3sas: Add branding string support for OEM custom HBA (Sreekanth Reddy)   
- mpt3sas: Add branding string support for OEM's HBA (Sreekanth Reddy)   
- mpt3sas: MPI 2.5 Rev J (2.5.5) specification and 2.00.34 header files (Sreekanth Reddy)   
- mpt3sas: Update MPI2 strings to MPI2.5 (Sreekanth Reddy)   
- mpt3sas: Bump mpt3sas Driver version to v5.100.00.00 (Sreekanth Reddy)   
- mpt3sas: Provides the physical location of sas drives (Sreekanth Reddy)   
- mpt3sas: MPI 2.5 Rev I (2.5.4) specifications. (Sreekanth Reddy)   
- mpt3sas: Remove redundancy code while freeing the controller resources. (Sreekanth Reddy)   
- mpt3sas: Don't block the drive when drive addition under the control of SML (Sreekanth Reddy)   
- mpt3sas: Get IOC_FACTS information using handshake protocol only after HBA card gets into READY or Operational state. (Sreekanth Reddy)   
- mpt3sas: Added Combined Reply Queue feature to extend up-to 96 MSIX vector support (Sreekanth Reddy)   
- mpt2sas: Refcount fw_events and fix unsafe list usage (Calvin Owens)   
- mpt2sas: Refcount sas_device objects and fix unsafe list usage (Calvin Owens)   
- mpt2sas, mpt3sas: Abort initialization if no memory I/O resources detected (Sreekanth Reddy)   
- cnic: Add the interfaces to get FC-NPIV table. (Adheer Chandravanshi)  [Orabug: 22066196]  
- cnic: Populate upper layer driver state in MFW (Tej Parkash)  [Orabug: 22066196]  
- bnx2x: Prevent UDP 4-tuple configurations on older adapters (Yuval Mintz)  [Orabug: 22066196]  
- drivers/net: get rid of unnecessary initializations in .get_drvinfo() (Ivan Vecera)  [Orabug: 22066196]  
- bnx2x: byte swap rss_key to comply to Toeplitz specs (Eric Dumazet)  [Orabug: 22066196]  
- bnx2x: track vxlan port count (Jiri Benc)  [Orabug: 22066196]  
- bnx2x: use ktime_get_seconds() for timestamp (Arnd Bergmann)  [Orabug: 22066196]  
- bnx2x: Add new device ids under the Qlogic vendor (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Fix vxlan endianity issue (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Add vxlan RSS support (Rajesh Borundia)  [Orabug: 22066196]  
- bnx2: Fix bandwidth allocation for some MF modes (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Free NVRAM lock at end of each page (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Prevent null pointer dereference on SKB release (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Add BD support for storage (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Correct logic for pvid configuration. (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Fix compilation when CONFIG_BNX2X_SRIOV is not set (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: add vlan filtering offload (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Bump up driver version to 1.712.30 (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Add MFW dump support (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: new Multi-function mode - BD (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Add 84858 phy support (Yaniv Rosner)  [Orabug: 22066196]  
- bnx2x: Rebrand from 'broadcom' into 'qlogic' (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Utilize FW 7.12.30 (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: only report most generic filters in get_ts_info (Jacob Keller)  [Orabug: 22066196]  
- bnx2x: fix DMA API usage (Michal Schmidt)  [Orabug: 22066196]  
- bnx2x: Fix linearization for encapsulated packets (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Release nvram lock on error flow (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Fix statistics gathering on link change (Ariel Elior)  [Orabug: 22066196]  
- bnx2x: Fix self-test for 20g devices (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Fix VF MAC removal (Shahed Shaikh)  [Orabug: 22066196]  
- bnx2x: Don't notify about scratchpad parities (Manish Chopra)  [Orabug: 22066196]  
- bnx2x: Prevent false warning when accessing MACs (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Correct speed from baseT into KR. (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Correct asymmetric flow-control (Yuval Mintz)  [Orabug: 22066196]  
- bnx2x: Alloc 4k fragment for each rx ring buffer element (Gabriel Krisman Bertazi)  [Orabug: 22066196]  
- This is the revsion change for lpfc 11.0.0.3 for UEK4 4.2.x release. (rkennedy)  [Orabug: 22029622]  
- lpfc: Fix default RA_TOV and ED_TOV in the FC/FCoE driver for all topologies (rkennedy)  [Orabug: 22029622]  
- lpfc: The linux driver does not reinitiate discovery after a failed FLOGI (rkennedy)  [Orabug: 22029622]  
- lpfc: Fix for discovery failure in PT2PT when FLOGI's ELS ACC response gets aborted (rkennedy)  [Orabug: 22029622]  
- lpfc: Add support for Lancer G6 and 32G FC links (rkennedy)  [Orabug: 22029622]  
- fix: lpfc_send_rscn_event sends bigger buffer size (rkennedy)  [Orabug: 22029622]  
- lpfc: Fix possible use-after-free and double free in lpfc_mbx_cmpl_rdp_page_a2() (rkennedy)  [Orabug: 22029622]  
- lpfc: remove set but not used variables (rkennedy)  [Orabug: 22029622]  
- lpfc:Make the function lpfc_sli4_mbox_completions_pending static in order to comply wi (rkennedy)  [Orabug: 22029622]  
- Fix kmalloc overflow in LPFC driver at large core count (rkennedy)  [Orabug: 22029622]  
- lpfc: Destroy lpfc_hba_index IDR on module exit (rkennedy)  [Orabug: 22029622]  
- lpfc: in sli3 use configured sg_seg_cnt for sg_tablesize (rkennedy)  [Orabug: 22029622]  
- lpfc: Remove unnessary cast (rkennedy)  [Orabug: 22029622]  
- lpfc: fix model description (rkennedy)  [Orabug: 22029622]  
- lpfc: Check for active portpeerbeacon. (James Smart)  [Orabug: 22029622]  
- lpfc: Fix vport deletion failure. (James Smart)  [Orabug: 22029622]  
- lpfc: Devices are not discovered during takeaway/giveback testing (James Smart)  [Orabug: 22029622]  
- lpfc: Add support for using block multi-queue (James Smart)  [Orabug: 22029622]  
- lpfc: Fix scsi prep dma buf error. (James Smart)  [Orabug: 22029622]  
- lpfc: Fix cq_id masking problem. (James Smart)  [Orabug: 22029622]  
- lpfc: Fix scsi task management error message. (James Smart)  [Orabug: 22029622]  
- lpfc: Fix to drop PLOGIs from fabric node till LOGO processing completes (James Smart)  [Orabug: 22029622]  
- lpfc: The lpfc driver does not issue RFF_ID and RFT_ID in the correct sequence (James Smart)  [Orabug: 22029622]  
- lpfc: Correct loss of target discovery after cable swap. (James Smart)  [Orabug: 22029622]  
- lpfc: Add support for ELS LCB. (James Smart)  [Orabug: 22029622]  
- lpfc: Correct reference counting of rport (James Smart)  [Orabug: 22029622]  
- lpfc: Fix ABORTs WQ selection in terminate_rport_io (James Smart)  [Orabug: 22029622]  
- lpfc: Add support for RDP ELS command. (James Smart)  [Orabug: 22029622]  
- lpfc: Correct reporting of vport state on fdisc command failure. (James Smart)  [Orabug: 22029622]  
- lpfc: Fix discovery issue when changing from Pt2Pt to Fabric. (James Smart)  [Orabug: 22029622]  
- lpfc: Fix to remove IRQF_SHARED flag for MSI/MSI-X vectors. (James Smart)  [Orabug: 22029622]  
- lpfc: Fix crash in vport_delete. (James Smart)  [Orabug: 22029622]  
- lpfc: Correct loss of RSCNs during array takeaway/giveback testing. (James Smart)  [Orabug: 22029622]  
- lpfc: Fix incorrect log message reported for empty FCF record. (James Smart)  [Orabug: 22029622]  
- lpfc: Change buffer pool empty message to miscellaneous category (James Smart)  [Orabug: 22029622]  

* Mon Oct 19 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.10-18.el7uek] 
- be2net: bump up the driver version to 10.6.0.4 (Suresh Reddy)  [Orabug: 21862339]  
- RDS: fix race condition when sending a message on unbound socket. (Quentin Casasnovas)   {CVE-2015-6937} 
- uek-rpm: unset CONFIG_NFS_USE_LEGACY_DNS for OL7 debug kernel too (Todd Vierling)  [Orabug: 21483381]  
- uek-rpm: build: Update the base release to 9 with stable v4.1.10 (Santosh Shilimkar)   
- PCI: Restore pref MMIO allocation logic for host bridge without mmio64 (Yinghai Lu)  [Orabug: 21826746]  
- PCI: Only treat non-pref mmio64 as pref if host bridge has mmio64 (Yinghai Lu)  [Orabug: 21826746]  
- PCI: Add has_mem64 for struct host_bridge (Yinghai Lu)  [Orabug: 21826746]  
- PCI: Only treat non-pref mmio64 as pref if all bridges have MEM_64 (Yinghai Lu)  [Orabug: 21826746]  
- PCI: Check pref compatible bit for mem64 resource of PCIe device (Yinghai Lu)  [Orabug: 21826746]  
- OF/PCI: Add IORESOURCE_MEM_64 for 64-bit resource (Yinghai Lu)  [Orabug: 21826746]  
- PCI: kill wrong quirk about M7101 (Yinghai Lu)  [Orabug: 21826746]  
- sparc/PCI: Keep resource idx order with bridge register number (Yinghai Lu)  [Orabug: 21826746]  
- sparc/PCI: Add IORESOURCE_MEM_64 for 64-bit resource in OF parsing (Yinghai Lu)  [Orabug: 21826746]  
- sparc/PCI: Reserve legacy mmio after PCI mmio (Yinghai Lu)  [Orabug: 21826746]  
- sparc/PCI: Unify pci_register_region() (Yinghai Lu)  [Orabug: 21826746]  
- sparc/PCI: Use correct bus address to resource offset (Yinghai Lu)  [Orabug: 21826746]  
- sparc/PCI: Add mem64 resource parsing for root bus (Yinghai Lu)  [Orabug: 21826746]  
- sparc: Revert commits that broke ixgbe and igb drivers on T7 (Khalid Aziz)  [Orabug: 21826746]  
- sparc: vdso: lockdep fixes (Dave Kleikamp)   
- SPARC64: LDoms suspend domain service. (Bijan Mottahedeh)  [Orabug: 21970743]  
- enic: do hang reset only in case of tx timeout (Sujith Sankar)   
- enic: handle spurious error interrupt (Sujith Sankar)   
- enic: reduce ioread in devcmd2 (Sujith Sankar)   
- enic: Fix build failure with SRIOV disabled. (Sujith Sankar)   
- enic: Fix namespace pollution causing build errors. (Sujith Sankar)   
- enic: Fix sparse warning in vnic_devcmd_init(). (Sujith Sankar)   
- enic: add devcmd2 (Sujith Sankar)   
- enic: add devcmd2 resources (Sujith Sankar)   
- enic: use netdev_<foo> or dev_<foo> instead of pr_<foo> (Sujith Sankar)   
- enic: move struct definition from .c to .h file (Sujith Sankar)   
- enic: allow adaptive coalesce setting for msi/legacy intr (Sujith Sankar)   
- enic: add adaptive coalescing intr for intx and msi poll (Sujith Sankar)   
- enic: fix issues in enic_poll (Sujith Sankar)   
- enic: use atomic_t instead of spin_lock in busy poll (Sujith Sankar)   
- drivers/net: remove all references to obsolete Ethernet-HOWTO (Sujith Sankar)   
- enic: Grammar s/an negative/a negative/ (Sujith Sankar)   
- uek-rpm: configs: sparc: Enable VCC as a module (Santosh Shilimkar)   
- uek-rpm: configs: sparc64: enable i40e modules (Allen Pais)   
- uek-rpm: configs: sparc64: synced config files (Allen Pais)   
- qla2xxx: Update driver version to 8.07.00.26.39.0-k. (Sawan Chandak)  [Orabug: 21946579]  
- be2net: remove vlan promisc capability from VF's profile descriptors (Kalesh AP)   
- be2net: set pci_func_num while issuing GET_PROFILE_CONFIG cmd (Somnath Kotur)   
- be2net: pad skb to meet minimum TX pkt size in BE3 (Suresh Reddy)   
- be2net: release mcc-lock in a failure case in be_cmd_notify_wait() (Suresh Reddy)   
- be2net: fix BE3-R FW download compatibility check (Kalesh AP)   
- be2net: allow offloading with the same port for IPv4 and IPv6 (Jiri Benc)   
- be2net: avoid vxlan offloading on multichannel configs (Ivan Vecera)   
- be2net: protect eqo->affinity_mask from getting freed twice (Kalesh AP)   
- be2net: post buffers before destroying RXQs in Lancer (Kalesh AP)   
- be2net: enable IFACE filters only after creating RXQs (Kalesh AP)   
- be2net: Support vxlan offload stats in the driver (Sriharsha Basavapatna)   
- be2net: support ndo_get_phys_port_id() (Sriharsha Basavapatna)   
- be2net: bump up the driver version to 10.6.0.3 (Sathya Perla)   
- be2net: make SET_LOOPBACK_MODE cmd asynchrounous (Suresh Reddy)   
- be2net: return error status from be_mcc_notify() (Suresh Reddy)   
- be2net: convert dest field in udp-hdr to host-endian (Venkat Duvvuru)   
- be2net: fix wrong return value in be_check_ufi_compatibility() (Vasundhara Volam)   
- be2net: remove redundant D0 power state set (Kalesh Purayil)   
- be2net: query FW to check if EVB is enabled (Kalesh Purayil)   
- be2net: remove duplicate code in be_setup_wol() (Kalesh Purayil)   
- be2net: make hwmon interface optional (Arnd Bergmann)   
- be2net: Support for OS2BMC. (Venkata Duvvuru)   
- be2net: Report a "link down" to the stack when a fatal error or fw reset happens. (Venkata Duvvuru)   
- be2net: Export board temperature using hwmon-sysfs interface. (Venkata Duvvuru)   
- be2net: update copyright year to 2015 (Vasundhara Volam)   
- be2net: use be_virtfn() instead of !be_physfn() (Kalesh AP)   
- be2net: simplify UFI compatibility checking (Vasundhara Volam)   
- be2net: post full RXQ on interface enable (Suresh Reddy)   
- be2net: check for INSUFFICIENT_VLANS error (Kalesh AP)   
- be2net: receive pkts with L3, L4 errors on VFs (Somnath Kotur)   
- be2net: set interrupt moderation for Skyhawk-R using EQ-DB (Padmanabh Ratnakar)   
- be2net: add support for spoofchk setting (Kalesh AP)   
- be2net: log link status (Ivan Vecera)   
- qla2xxx: Add pci device id 0x2261. (Sawan Chandak)  [Orabug: 21946579]  
- qla2xxx: Fix missing device login retries. (Arun Easi)  [Orabug: 21946579]  
- qla2xxx: do not clear slot in outstanding cmd array (Himanshu Madhani)  [Orabug: 21946579]  
- qla2xxx: Remove decrement of sp reference count in abort handler. (Chad Dupuis)  [Orabug: 21946579]  
- qla2xxx: Add support to show MPI and PEP FW version for ISP27xx. (Sawan Chandak)  [Orabug: 21946579]  
- qla2xxx: Do not reset ISP for error entry with an out of range handle. (Chad Dupuis)  [Orabug: 21946579]  
- qla2xxx: Do not reset adapter if SRB handle is in range. (Chad Dupuis)  [Orabug: 21946579]  
- qla2xxx: Do not crash system for sp ref count zero (Hiral Patel)  [Orabug: 21946579]  
- qla2xxx: Add adapter checks for FAWWN functionality. (Saurav Kashyap)  [Orabug: 21946579]  
- qla2xxx: Pause risc before manipulating risc semaphore. (Joe Carnuccio)  [Orabug: 21946579]  
- qla2xxx: Use ssdid to gate semaphore manipulation. (Joe Carnuccio)  [Orabug: 21946579]  
- qla2xxx: Handle AEN8014 incoming port logout. (Joe Carnuccio)  [Orabug: 21946579]  
- qla2xxx: Add serdes register read/write support for ISP25xx. (Joe Carnuccio)  [Orabug: 21946579]  
- qla2xxx: Remove dead code (Bart Van Assche)  [Orabug: 21946579]  
- qla2xxx: Remove a superfluous test (Bart Van Assche)  [Orabug: 21946579]  
- qla2xxx: Avoid that sparse complains about duplicate [noderef] attributes (Bart Van Assche)  [Orabug: 21946579]  
- qla2xxx: Remove __constant_ prefix (Bart Van Assche)  [Orabug: 21946579]  
- qla2xxx: Replace two macros with an inline function (Bart Van Assche)  [Orabug: 21946579]  
- qla2xxx: Remove set-but-not-used variables (Bart Van Assche)  [Orabug: 21946579]  
- qla2xxx: Declare local functions static (Bart Van Assche)  [Orabug: 21946579]  
- tcp_cubic: better follow cubic curve after idle period (Eric Dumazet)  [Orabug: 21920285]  
- be2iscsi: Bump the driver version (Jitendra Bhivare)  [Orabug: 21862307]  
- be2iscsi: Fix updating the next pointer during WRB posting (Jitendra Bhivare)  [Orabug: 21862307]  
- be2iscsi: update MAINTAINERS list (Jitendra Bhivare)  [Orabug: 21862307]  
- be2iscsi: add obsolete warning messages (Jitendra Bhivare)  [Orabug: 21862307]  
- be2iscsi: ownership change (Jitendra Bhivare)  [Orabug: 21862307]  
- be2iscsi : Logout of FW Boot Session (Jitendra Bhivare)  [Orabug: 21862307]  
- be2iscsi : Fix memory check before unmapping. (Jitendra Bhivare)  [Orabug: 21862307]  
- Linux 4.1.10 (Greg Kroah-Hartman)   
- hp-wmi: limit hotkey enable (Kyle Evans)   
- zram: fix possible use after free in zcomp_create() (Luis Henriques)   
- netlink: Replace rhash_portid with bound (Herbert Xu)   
- netlink: Fix autobind race condition that leads to zero port ID (Herbert Xu)   
- mvneta: use inband status only when explicitly enabled (Stas Sergeev)   
- of_mdio: add new DT property 'managed' to specify the PHY management type (Stas Sergeev)   
- net: phy: fixed_phy: handle link-down case (Stas Sergeev)   
- net: dsa: bcm_sf2: Do not override speed settings (Florian Fainelli)   
- fib_rules: fix fib rule dumps across multiple skbs (Wilson Kok)   
- net: revert "net_sched: move tp->root allocation into fw_init()" (WANG Cong)   
- tcp: add proper TS val into RST packets (Eric Dumazet)   
- openvswitch: Zero flows on allocation. (Jesse Gross)   
- macvtap: fix TUNSETSNDBUF values > 64k (Michael S. Tsirkin)   
- net/mlx4_en: really allow to change RSS key (Eric Dumazet)   
- bridge: fix igmpv3 / mldv2 report parsing (Linus Lüssing)   
- sctp: fix race on protocol/netns initialization (Marcelo Ricardo Leitner)   
- netlink, mmap: transform mmap skb into full skb on taps (Daniel Borkmann)   
- net: dsa: bcm_sf2: Fix 64-bits register writes (Florian Fainelli)   
- ipv6: fix multipath route replace error recovery (Roopa Prabhu)   
- net: dsa: bcm_sf2: Fix ageing conditions and operation (Florian Fainelli)   
- net/ipv6: Correct PIM6 mrt_lock handling (Richard Laing)   
- net: eth: altera: fix napi poll_list corruption (Atsushi Nemoto)   
- net: fec: clear receive interrupts before processing a packet (Russell King)   
- ipv6: fix exthdrs offload registration in out_rt path (Daniel Borkmann)   
- sock, diag: fix panic in sock_diag_put_filterinfo (Daniel Borkmann)   
- usbnet: Get EVENT_NO_RUNTIME_PM bit before it is cleared (Eugene Shatokhin)   
- cls_u32: complete the check for non-forced case in u32_destroy() (WANG Cong)   
- vxlan: re-ignore EADDRINUSE from igmp_join (Marcelo Ricardo Leitner)   
- ip6_gre: release cached dst on tunnel removal (huaibin Wang)   
- i40e/i40evf: Bump i40e to 1.3.21 and i40evf to 1.3.13 (Catherine Sullivan)  [Orabug: 21764569]  
- i40e/i40evf: add get AQ result command to nvmupdate utility (Shannon Nelson)  [Orabug: 21764569]  
- i40e/i40evf: add exec_aq command to nvmupdate utility (Shannon Nelson)  [Orabug: 21764569]  
- i40e/i40evf: add wait states to NVM state machine (Shannon Nelson)  [Orabug: 21764569]  
- i40e/i40evf: add GetStatus command for nvmupdate (Shannon Nelson)  [Orabug: 21764569]  
- i40e/i40evf: add handling of writeback descriptor (Shannon Nelson)  [Orabug: 21764569]  
- i40e/i40evf: save aq writeback for future inspection (Shannon Nelson)  [Orabug: 21764569]  
- i40e: rename variable to prevent clash of understanding (Shannon Nelson)  [Orabug: 21764569]  
- i40e: Set defport behavior for the Main VSI when in promiscuous mode (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e/i40evf: Bump i40e to 1.3.9 and i40evf to 1.3.5 (Catherine Sullivan)  [Orabug: 21764569]  
- i40e/i40evf: Cache the CEE TLV status returned from firmware (Neerav Parikh)  [Orabug: 21764569]  
- i40e/i40evf: add VIRTCHNL_VF_OFFLOAD flag (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e: Remove redundant and unneeded messages (Greg Rose)  [Orabug: 21764569]  
- i40evf: Remove PF specific register definitions from the VF (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40evf: Use the correct defines to match the VF registers (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e: correct spelling error (Mitch Williams)  [Orabug: 21764569]  
- i40e: Fix comment for ethtool diagnostic link test (Greg Rose)  [Orabug: 21764569]  
- i40e/i40evf: Add capability to gather VEB per TC stats (Neerav Parikh)  [Orabug: 21764569]  
- i40e: Fix ethtool offline diagnostic with netqueues (Greg Rose)  [Orabug: 21764569]  
- i40e: Fix legacy interrupt mode in the driver (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e: Move function calls to i40e_shutdown instead of i40e_suspend (Catherine Sullivan)  [Orabug: 21764569]  
- i40e: add RX to port CRC errors label (Shannon Nelson)  [Orabug: 21764569]  
- i40e: don't degrade __le16 (Mitch Williams)  [Orabug: 21764569]  
- i40e: Add AQ commands for NVM Update for X722 (Shannon Nelson)  [Orabug: 21764569]  
- i40e/i40evf: Add ATR HW eviction support for X722 (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e: Add IWARP support for X722 (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e/i40evf: Add TX/RX outer UDP checksum support for X722 (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e/i40evf: Add support for writeback on ITR feature for X722 (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e/i40evf: RSS changes for X722 (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e/i40evf: Update register.h file for X722 (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e/i40evf: Update FW API with X722 support (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e/i40evf: Add flags for X722 capabilities (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e/i40evf: Add device ids for X722 (Anjali Singhai Jain)  [Orabug: 21764569]  
- i40e: use BIT and BIT_ULL macros (Jesse Brandeburg)  [Orabug: 21764569]  
- i40e: clean up error status messages (Shannon Nelson)  [Orabug: 21764569]  
- i40e: provide correct API version to older VF drivers (Mitch Williams)  [Orabug: 21764569]  
- i40evf: support virtual channel API version 1.1 (Mitch Williams)  [Orabug: 21764569]  
- i40evf: handle big resets (Mitch Williams)  [Orabug: 21764569]  
- i40e: support virtual channel API 1.1 (Mitch Williams)  [Orabug: 21764569]  
- i40e/i40evf: add macros for virtual channel API version and device capability (Mitch Williams)  [Orabug: 21764569]  
- i40e: add VF capabilities to virtual channel interface (Mitch Williams)  [Orabug: 21764569]  
- i40e: clean up unneeded gotos (Shannon Nelson)  [Orabug: 21764569]  
- i40e/i40evf: Fix and refactor dynamic ITR code (Carolyn Wyborny)  [Orabug: 21764569]  
- i40e: only report generic filters in get_ts_info (Jacob Keller)  [Orabug: 21764569]  

* Wed Oct 14 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.9-17.el7uek] 
- RDS: make send_batch_count tunable effective (Santosh Shilimkar)  [Orabug: 22010933]  
- RDS: make use of kfree_rcu() and avoid the call_rcu() chain (Santosh Shilimkar)  [Orabug: 22010933]  
- RDS: verify the underlying transport exists before creating a connection (Sasha Levin)  [Orabug: 22010933]  
- uek-rpm: build: update ol7 specs with linux-firmware deps (Santosh Shilimkar)  [Orabug: 21983616]  
- RDS/IB: print string constants in more places (Zach Brown)   
- ib/rds: runtime debuggability enhancement (Qing Huang)   
- mpt2sas: setpci reset kernel oops fix (Nagarajkumar Narayanan)  [Orabug: 21960460]  
- ixgbe: Advance version to 4.2.1 (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: X540 thermal warning interrupt not a GPI (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Fix FCRTH value in VM-to-VM loopback mode (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Only clear adapter_stopped if ixgbe_setup_fc succeeded (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Correct several flaws with with DCA setup (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Add new X550EM SFP+ device ID (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Update ixgbe_disable_pcie_master flow for X550* (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Add small packet padding support for X550 (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Correct setting of RDRXCTL register for X550* devices (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Correct error path in semaphore handling (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Add I2C bus mux support (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Limit SFP polling rate (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Allow SFP+ on more than 82598 and 82599 (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Add logic to reset CS4227 when needed (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Fix 1G and 10G link stability for X550EM_x SFP+ (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Add X550EM_x dual-speed SFP+ support (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Allow reduced delays during SFP detection (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Clear I2C destination location (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Enable bit-banging mode on X550 (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Set lan_id before first I2C eeprom access (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Provide unlocked I2C methods (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Provide I2C combined on X550EM (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Add X550EM support for SFP insertion interrupt (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Accept SFP not present errors on all devices (Mark Rustad)  [Orabug: 21918732]  
- ixgbevf: Enables TSO for stacked VLAN (Toshiaki Makita)  [Orabug: 21918732]  
- ixgbe: Add fdir support for SCTP on X550 (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: Add SFP+ detection for X550 hardware (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: Limit lowest interrupt rate for adaptive interrupt moderation to 12K (Alexander Duyck)  [Orabug: 21918732]  
- ixgbe: Teardown SR-IOV before unregister_netdev() (Alex Williamson)  [Orabug: 21918732]  
- ixgbe: fix issue with SFP events with new X550 devices (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: Resolve "initialized field overwritten" warnings (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Remove bimodal SR-IOV disabling (Alex Williamson)  [Orabug: 21918732]  
- ixgbe: Add support for reporting 2.5G link speed (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: fix bounds checking in ixgbe_setup_tc for 82598 (Emil Tantilov)  [Orabug: 21918732]  
- ixgbe: support for ethtool set_rxfh (Tom Barbette)  [Orabug: 21918732]  
- ixgbe: Avoid needless PHY access on copper phys (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: cleanup to use cached mask value (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: Remove second instance of lan_id variable (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: use kzalloc for allocating one thing (Maninder Singh)  [Orabug: 21918732]  
- ixgbe: Remove unused PCI bus types (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: add new bus type for intergrated I/O interface (IOSF) (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: add get_bus_info method for X550 (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: Add support for entering low power link up state (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: Add support for VXLAN RX offloads (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Add support for UDP-encapsulated tx checksum offload (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Check whether FDIRCMD writes actually complete (Mark Rustad)  [Orabug: 21918732]  
- ixgbe: Assign set_phy_power dynamically where needed (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: add new function to check for management presence (Don Skidmore)  [Orabug: 21918732]  
- ixgbe: do not set low power mode (Brian Maly)  [Orabug: 21823210]  

* Thu Oct 8 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.9-16.el7uek] 
- uek-rpm: configs: sync up configs with v4.1.9 (Santosh Shilimkar)   
- uek-rpm: Enable config for OVN xsigo drivers (Mukesh Kacker)   
- Add Oracle virtual Networking Drivers for uek4 kernel (Pradeep Gopanapalli)   
- xen-netfront: respect user provided max_queues (Wei Liu)   
- net/xen-netfront: only napi_synchronize() if running (Chas Williams)   
- net/xen-netfront: only clean up queues if present (Chas Williams)   
- xen-netback: respect user provided max_queues (Wei Liu)   
- xen-netback: require fewer guest Rx slots when not using GSO (David Vrabel)   
- xen-netback: add support for multicast control (Paul Durrant)   
- xen/netback: Wake dealloc thread after completing zerocopy work (Ross Lagerwall)   
- xen-netback: Allocate fraglist early to avoid complex rollback (Ross Lagerwall)   
- net/xen-netback: off by one in BUG_ON() condition (Dan Carpenter)   
- xen-netback: remove duplicated function definition (Li, Liang Z)   
- net/xen-netback: Don't mix hexa and decimal with 0x in the printf format (Julien Grall)   
- net/xen-netback: Remove unused code in xenvif_rx_action (Julien Grall)   
- ib_sdp/cma: readd SDP support to cma_save_net_info (Qing Huang)   
- ib/sdp: Enable usermode FMR (Dotan Barak)   
- ib/sdp: fix null dereference of sk->sk_wq in sdp_rx_irq() (Chuck Anderson)  [Orabug: 20070989]  
- sdp: fix keepalive functionality (shamir rabinovitch)  [Orabug: 18728784]  
- ib_sdp: fix deadlock when sdp_cma_handler is called while socket is being closed (Saeed Mahameed)   
- ib_sdp: add unhandled events to rdma_cm_event_str (Saeed Mahameed)   
- ib_sdp/uek-rpm: configs: enable compilation for sdp (Qing Huang)   
- ib_sdp: porting sdp from uek2 to uek-4.1 (Qing Huang)   
- ib_sdp: remove APM code (Qing Huang)   
- sdp: Kconfig and Makefile changes (Ajaykumar Hotchandani)   
- sdp: port the code to uek2 (Dotan Barak)   
- sdp: added debug print for the event: RDMA_CM_EVENT_ALT_PATH_LOADED (Dotan Barak)   
- sdp: prepare support to kernel 2.6.39-200.1.1.el5uek: add macro to get sk_sleep (Dotan Barak)   
- sdp: add support to kernel 2.6.39-200.1.1.el5uek (Dotan Barak)   
- sdp: add [rt]x_bytes counters to sdpstats (Amir Vadai)   
- sdp: Fix Bug 114242 - Multi connection net_perf causes server to hang (Moran Perets)   
- FMR: remove FMR failure messages (Eli Cohen)   
- sdp: make sdp memory leak print a debug (Amir Vadai)   
- sdp: changed memory accounting warning into debug (Amir Vadai)   
- sdp: Fix issues in sdpprf (Amir Vadai)   
- sdp: Remove protection before sleep on RX (Amir Vadai)   
- sdp: Enable automatic path migration support also in the passive side of the connection. (Moni Shoua)   
- sdp: Fixed some coverity issues (Amir Vadai)   
- Flatten the entire tree fixes (Eli Cohen)   
- sdp: Fixed compilation error on 2.6.18 RH5.5 (Amir Vadai)   
- sdp: fix memory leak. sockets_allocated wasn't freed (Amir Vadai)   
- sdp: Removed spaces and tabs at end of lines (Amir Vadai)   
- sdp: fix sdpprf (Amir Vadai)   
- sdp: Fixed bcopy statistics (Amir Vadai)   
- sdp: Bad behaviour when setting low rcvbuf size (Amir Vadai)   
- sdp: Fixed a typo (Amir Vadai)   
- sdp: Limit total memory consumed by rcvbuf (Amir Vadai)   
- sdp: fix "sdpprf empty after a long run" (Amir Vadai)   
- sdp: make SDP_RX_SIZE a module parameter (Amir Vadai)   
- sdp: Rollback credit limit during ZCopy transaction. (Amir Vadai)   
- sdp: get per socket memory statistics at socket's sysfs file (Amir Vadai)   
- sdp: fix a hole in rx memory limit (Amir Vadai)   
- sdp: make sure memory is reclaimed (Amir Vadai)   
- sdp: send packets without payload when credits=1 (Amir Vadai)   
- sdp: removed some prints to sdpprf (Amir Vadai)   
- sdp: remove unused rcvbuf_scale module parameter (Amir Vadai)   
- sdp: fix memory socket accounting (Amir Vadai)   
- sdp: fix sdp_sendmsg counters in sdpstats (Amir Vadai)   
- sdp: make retry count a module parameter (Amir Vadai)   
- sdp: BUG2217 - fix sdpstats negative values (Amir Vadai)   
- sdp: do not abort connection on RDMA_CM_EVENT_ADDR_CHANGE (Amir Vadai)   
- rdma_cm, sdp: bug fixes and some changes to APM logic (Amir Vadai)   
- sdp: removed debug print (Amir Vadai)   
- sdp: use APM support in rdma_cm (Amir Vadai)   
- sdp: do not reenter sdp_abort_rx_srcavail (Amir Vadai)   
- sdp: Abort rx SrcAvail when out of credits (Amir Vadai)   
- sdp: Fixed BUG2207 - EINVAL when connect after IPv6 bind (Amir Vadai)   
- sdp: check address family before connecting (Amir Vadai)   
- sdp: Do not ignore scope_id in IPv6 (Amir Vadai)   
- sdp: make backport sk_inet()->xxx simpler (Amir Vadai)   
- sdp: Fix get getsockname/getpeername in IPv6 (Amir Vadai)   
- sdp: Allow bind to address with family AF_INETx_SDP (Amir Vadai)   
- sdp: Use %pI4 + %pI6 in new kernels (Amir Vadai)   
- sdp: fix connect to IPv4 over IPv6 (Amir Vadai)   
- sdp: Fix some issues in ipv6 support (Amir Vadai)   
- sdp: ipv6 support (Amir Vadai)   
- sdp: move histogram allocation from stack to heap (Amir Vadai)   
- sdp: print error value when ib_umem_get fails (Amir Vadai)   
- sdp: remove 'reading beyond SKB' warning (Amir Vadai)   
- sdp: RdmaRdCompl not sent sometimes (Amir Vadai)   
- sdp: make sdp_prf index atomic (Amir Vadai)   
- sdp: handle failed RDMA read (Amir Vadai)   
- sdp: Fix compilation error when SDP_DEBUG_DATA is off (Amir Vadai)   
- sdp: Enable set zcopy threshold to 0 using setsockopt (Amir Vadai)   
- sdp: BUG2161 - hanging sockets are left (Amir Vadai)   
- sdp: Take into account HW inline capabilities (Amir Vadai)   
- sdp: Send small sends using inline (Amir Vadai)   
- sdp: access socket history from debugfs (Amir Vadai)   
- sdp: use a macro to convert ssk into sk (Amir Vadai)   
- sdp: Initialize remote credits when sending Hello (Amir Vadai)   
- sdp: BUG2158 - do not send SrcAvail too small (Amir Vadai)   
- sdp: add a sanity check for sg_len (Eldad Zinger)   
- sdp: fix socket_allocated counter (Eldad Zinger)   
- sdp: no point of waiting for data if remote host can't send (Eldad Zinger)   
- sdp: fix support for a case of no locking capabilities (Eldad Zinger)   
- sdp: if can not allocate memory - no point of waiting (Eldad Zinger)   
- sdp: cosmetics (Eldad Zinger)   
- sdp: fix for CMA reference count (Eldad Zinger)   
- sdp: add ability to set a maximum memory usage for the entire module (Eldad Zinger)   
- sdp: Accept AF_INET_SDP in address supplied to connect() (Amir Vadai)   
- sdp: fix RDMA read completion with error (Amir Vadai)   
- sdp: sdp_post_rdma_read() should clean up its mess (Amir Vadai)   
- sdp: fix compilation error when compiling without debug flags (Eldad Zinger)   
- sdp: treat unfinished RDMA operation as a fatal error (Eldad Zinger)   
- sdp: fix for race condition with SrcAvailCancel handling (Eldad Zinger)   
- sdp: call ib_umem_get with the right access (Amir Vadai)   
- sdp: Improve the look of packet dump (Amir Vadai)   
- sdp: cosmetics, debug messages, error codes (Eldad Zinger)   
- sdp: SrcAvailCancel should not be processed during RDMA read (Eldad Zinger)   
- sdp: BUG2082 - fix orphan counter reading (Eldad Zinger)   
- sdp: when aborting SrcAvail, should check if it wasn't aborted already (Eldad Zinger)   
- sdp: ZCopy doesn't support multithreading - warning & kernel panic protection (Eldad Zinger)   
- sdp: Enable RoCE by default (Amir Vadai)   
- sdp: SrcAvailCancel should be processed even if SrcAvail was partly processed (Eldad Zinger)   
- sdp: BUG2144 - first free rx_sa before sending SendSM (Eldad Zinger)   
- sdp: fix code readability (Eldad Zinger)   
- sdp: BUG2141 - fix refcnt bug (Eldad Zinger)   
- sdp: refcnt debug tool (Eldad Zinger)   
- sdp: cosmetics & add/remove warning messages (Eldad Zinger)   
- sdp: extend socket locking scope in dreq timeout function (Eldad Zinger)   
- sdp: sdp_poll() should not excessively poll rx_cq (Eldad Zinger)   
- sdp: postpone rx timer when arming rx_cq (Eldad Zinger)   
- sdp: fix for timestamping values in debug messages (Eldad Zinger)   
- sdp: better sequence-number handling and cosmetic updates (Eldad Zinger)   
- sdp: add some checking & protection for enum values in debug utilities (Eldad Zinger)   
- sdp: BUG2138 - 32bit hosts can't devide 64bit variables (Eldad Zinger)   
- sdp: remove recursion in tx_ring processing (Eldad Zinger)   
- sdp: fix keepalive timer setup for server-sockets (Eldad Zinger)   
- sdp: fix logarithmic histogram index (Eldad Zinger)   
- sdp: fix compilation on ia64 and ppc (Eldad Zinger)   
- sdp: Some improvements to multistream BW (Amir Vadai)   
- sdp: add support for no recv polling at all (Eldad Zinger)   
- sdp: BUG1923 - fix support for MSG_OOB (Eldad Zinger)   
- sdp: remove unused variables (Eldad Zinger)   
- sdp: fixed for error code in sendmsg-BZCopy (Eldad Zinger)   
- sdp: fixed skbs-control-queue memory leak (Eldad Zinger)   
- sdp: fixed device removal issues (Eldad Zinger)   
- sdp: added the ability to use sdpprf for any debug message (Eldad Zinger)   
- sdp: fixed a deadlock when tx_timer calls sdp_reset that tries to del the timer (Eldad Zinger)   
- sdp: fixed SrcAvail memory leak (Eldad Zinger)   
- sdp: removed unnecessary variable 'vm_wait' (Eldad Zinger)   
- sdp: stability improvements for ZCopy (Eldad Zinger)   
- sdp: properly kill nagle_timer on socket reset (Eldad Zinger)   
- sdp: BUG2092 - ib_device field in sdp_sock is reset not in user-context (Eldad Zinger)   
- sdp: fix for stopping tx timer/tasklet when socket state is TCP_CLOSE (Eldad Zinger)   
- sdp: BUG1403 - last sk_refcnt is called while cma handler is invoked (Eldad Zinger)   
- sdp: bug fix for a case of no memory to allocate for rx_sa (Eldad Zinger)   
- sdp: rx_irq should use tasklet instead of timer due to latency issue (Eldad Zinger)   
- sdp: better handling of page-allocation-failure (Eldad Zinger)   
- sdp: reduce size of sdp_buf to what is really being used (Eldad Zinger)   
- sdp: remove the relation between qp_active and sdp_free_fmr() (Eldad Zinger)   
- sdp: small fix to support device removal during traffic (Eldad Zinger)   
- sdp: bug fix for a case of no memory to allocate for tx_sa (Eldad Zinger)   
- sdp: fix behavior when a skb allocation fails (Eldad Zinger)   
- sdp: some small non-behavioral changes in sdp_dreq_wait_timeout_work() (Eldad Zinger)   
- sdp: rewrite orphan count logic (Eldad Zinger)   
- sdp: change socket reference semantics: keepalive != alive (Eldad Zinger)   
- sdp: remove unnecessary argument from sdp_connected_handler. (Eldad Zinger)   
- sdp: removed extra debug message and comment. (Eldad Zinger)   
- sdp: fix for socket refcnt when error is marked while in TCP_TIME_WAIT state (Eldad Zinger)   
- sdp: enable support for ib devices that do not support fmr (Eldad Zinger)   
- sdp: before activating rx_ring timer, need to check that qp is still active. (Eldad Zinger)   
- sdp: fix compilation warnings (Eldad Zinger)   
- sdp: define SDP_MAX_PAYLOAD as ulong instead of int, to comply with PAGE_SIZE (Eldad Zinger)   
- sdp: some small non-functional changes. (Eldad Zinger)   
- sdp: enable rx_cq arming when no one polls. (Eldad Zinger)   
- sdp: before arming cq, need to check if cq was not destroyed already. (Eldad Zinger)   
- sdp: When purging tx_ring, rdma_inflight accountings should be disregarded, so the number of skbs to free is just (posted=head-tail). (Eldad Zinger)   
- sdp: tx_ring timer should not be scheduled if the qp is not active anymore. (Eldad Zinger)   
- sdp: if can't recv or send, and the qp is not active, return -EPIPE instead of 0 (Eldad Zinger)   
- sdp: rx completions workqueue should be flushed after qp destruction and before the socket is freed. (Eldad Zinger)   
- sdp: rx/tx tasklets should be properly killed when destroying qp. (Eldad Zinger)   
- sdp: some annoying whitespaces removed. (Eldad Zinger)   
- sdp: remove white spaces in the end of some lines. (Eldad Zinger)   
- sdp: device_removal_lock should not be a spinlock because module removal takes a long time. (Eldad Zinger)   
- sdp: error value for sdp_set_error() should be negative. (Eldad Zinger)   
- sdp: Fix for deadlock between sdp_connect and sdp_destroy_work. (Eldad Zinger)   
- sdp: cleanup ssk->rx_sa when aborting incoming SrcAvail (Amir Vadai)   
- sdp: fix compilation warnings in RH (Amir Vadai)   
- sdp: sdp_destroy_qp should be protected in destroy work (Amir Vadai)   
- sdp: don't double free fmr (Amir Vadai)   
- sdp: Limit FMR resources (Amir Vadai)   
- sdp: Fix for hangs/crashes in rare cases (Amir Vadai)   
- sdp: Fix for warning message when receiving with MSG_PEEK flag, and free skb that is not needed any more after all data was read from it. (Eldad Zinger)   
- sdp: On MSG_PEEK, no rdma_rd_complete should be sent. (Eldad Zinger)   
- sdp: update for sdp_cma_handler() events debug messages. (Eldad Zinger)   
- sdp: fix for handling multi iov's in ZCOPY. (Eldad Zinger)   
- sdp: Fix iperf multistream hanging (Amir Vadai)   
- sdp: Fix wrong use of ssk->sdp_disconnect (Amir Vadai)   
- sdp: protect sdp_auto_moderation from device removal (Amir Vadai)   
- sdp: sdp_recvmsg() shouldn't handle SDP_MID_DISCONN when MSG_PEEK flag is up. (Eldad Zinger)   
- sdp: added lock_sock() to sdp_poll() (Eldad Zinger)   
- sdp: Cleanedup some commented lines (Amir Vadai)   
- sdp: Fix bad handling of small rcvbuf size in zcopy (Amir Vadai)   
- sdp: fix issues in orphan count (Amir Vadai)   
- sdp: protect rx_ring access with a lock (Amir Vadai)   
- sdp: cleanup skb allocations (Amir Vadai)   
- sdp: Reuse buffers in rx ring (Amir Vadai)   
- sdp: cpu affinity in sdpstats (Amir Vadai)   
- sdp: use polling in rx (Amir Vadai)   
- sdp: fix for a bug of lost refcnt in TCP_TIME_WAIT state. (Eldad Zinger)   
- sdp: BUG2038 - transmission goal size won't exceed SDP_MAX_PAYLOAD (Eldad Zinger)   
- sdp: SDP_WARN_ON defined to be used instead of WARN_ON, for better compatibility (Eldad Zinger)   
- sdp: new debug function added, minor debug message change. (Eldad Zinger)   
- sdp: device removal rewritten for a stability improvement. (Eldad Zinger)   
- sdp: unnecessary local variable removed, 'const' declarations added (Eldad Zinger)   
- sdp: tx timer is deleted when sockets goes to TCP_CLOSE (Eldad Zinger)   
- sdp: canceled a call to sdp_desroy_work() on send completion with error (Eldad Zinger)   
- sdp: unnecessary wait-queue removed from sdp_sock structure. (Eldad Zinger)   
- sdp: unnecessary local variable removed. (Eldad Zinger)   
- sdp: debug message for reference count changed from CM_TW to CMA (Eldad Zinger)   
- sdp: BUG2031 - sdp_cma_handler() won't be invoked after last ref count removed (Eldad Zinger)   
- sdp: fix a leak when ib_post_xxx fail + small fixes (Amir Vadai)   
- sdp: on device removal, ref count taken so that socket won't be destructed (Eldad Zinger)   
- sdp: use max number of SGE from HW capabilities (Amir Vadai)   
- sdp: Fix a hang when ib_post_recv is failed (Amir Vadai)   
- sdp: fix compilation warning on debug prints (Amir Vadai)   
- sdp: sdp_bzcopy_thresh module parameter removal (Eldad Zinger)   
- sdp: BUG2017 - better initialization implementation for ssk->nagle_timer (Eldad Zinger)   
- sdp: fix for brutal device removing (Eldad Zinger)   
- sdp: Don't try to allocate FMR larger than RLIMIT_MEMLOCK (Amir Vadai)   
- sdp: Don't count sdp header twice when calculating size_goal (Amir Vadai)   
- sdp: timeout for abortive close updated (Eldad Zinger)   
- sdp: module parameter to disable SDP over ROCEE (Amir Vadai)   
- sdp: added differentiation between bind failures of sdp. (Eldad Zinger)   
- sdp: BUG1727 - there is no point of using zcopy when credits are not available. (Eldad Zinger)   
- sdp: BUG1992 - enable transmission of credits update when tx_credits == 1 (Eldad Zinger)   
- sdp: unnecessary 'if' statement canceled. (Eldad Zinger)   
- sdp: BUG1727 - fixed select(2) behavior on a new nonblocking socket. (Eldad Zinger)   
- sdp: BUG1727 - sdp_destroy_work() and sdp_connect() interfere with each other. (Eldad Zinger)   
- sdp: support iovlen > 1 in zcopy (Amir Vadai)   
- sdp: make sdp_socket.h available to user applications (Amir Vadai)   
- sdp: enable FMR pool cache (Amir Vadai)   
- sdp: Stop SA Cancel timeout when getting SendSM/RdmaRdCompl (Amir Vadai)   
- sdp: SendSM wasn't sent sometimes after getting SrcAvailCancel (Amir Vadai)   
- sdp: Send SendSM from recvmsg context and not from interrupt (Amir Vadai)   
- sdp: Fix bug in crossing SrcAvail (Amir Vadai)   
- sdp: Add detailed ZCopy aborted send statistics (Amir Vadai)   
- sdp: Prevent kernel crash if device init fails (plus bonus fix) (Amir Vadai)   
- sdp: Fix crossing SrcAvail handling (Amir Vadai)   
- sdp: Fix bugs in huge paged HW's (Amir Vadai)   
- sdp: BUG1899 - fix warnings on RH4.8 by avoiding multiple deletions on the same timer. (Amir Vadai)   
- sdp: must use ib_sg_dma_*, not sg_dma_* for mapping (Amir Vadai)   
- sdp: use IB_CQ_VECTOR_LEAST_ATTACHED for cq's (Amir Vadai)   
- sdp: make statistics per cpu (Amir Vadai)   
- sdp: added statistics instead of prints (Amir Vadai)   
- sdp: Fix partial ZCopy send bug + recvmsg with MSG_PEEK support (Amir Vadai)   
- sdp: Set a lower limit to ZCopy threshold (Amir Vadai)   
- sdp: Fix ZCopy sink not working (Amir Vadai)   
- sdp: fixed compilation warning (Amir Vadai)   
- sdp: ZCopy SrcAvail payload size limit fixed + fix ZCopy rx for small packets (Amir Vadai)   
- sdp: small spec compliancy fixes in code (Amir Vadai)   
- sdp: fix lockup on mthca cards (Amir Vadai)   
- sdp: fix a warning in RH4.0 (Amir Vadai)   
- sdp: Fix Hello Ack Header to be according to spec (Amir Vadai)   
- sdp: make /proc/net/sdpprf on only if debug data is on (Amir Vadai)   
- sdp: Cleanup ZCopy page registrations (Amir Vadai)   
- sdp: cancel_work_sync on 2.6.22 didn't return a value (Amir Vadai)   
- sdp: changed important prints in zcopy to warning instead of debug (Amir Vadai)   
- sdp: flush rx_comp_work before destroying socket + make dreq_wait_timeout_work flushing synced (Amir Vadai)   
- sdp: cleaned up debug prints (Amir Vadai)   
- sdp: take a reference during zcopy_send (Amir Vadai)   
- sdp: Disable BZcopy + Enable ZCopy (Amir Vadai)   
- sdp: changed some warnings into debug prints (Amir Vadai)   
- sdp: fixed BUG1826 part 1 - schedule while atomic (Amir Vadai)   
- sdp: Fixed annoying warning by memtrack (Amir Vadai)   
- sdp: fixed BUG1796 - running out of memory on rx (Amir Vadai)   
- sdp: fixed sparse warnings (Amir Vadai)   
- sdp: removed unneeded list initialization - percpu_counter might not have this memeber (Amir Vadai)   
- sdp: get max send sge from device capabilities instead of hard coded (Amir Vadai)   
- sdp: incorrect SDP_FMR_SIZE on 32-bit machines (Jack Morgenstein)   
- sdp: check if sdp device is actually present in sdp_remove_one (Jack Morgenstein)   
- sdp: Process tx completions from sendmsg context. arm tx cq when needed (Amir Vadai)   
- sdp: More code cleanup and ZCopy bugs fixes (Amir Vadai)   
- sdp: code cleanup (Amir Vadai)   
- sdp: fix cross SrcAvail deadlock (Amir Vadai)   
- sdp: Fix ZCopy compatability issues (Amir Vadai)   
- sdp: fix memory leak in bzcopy (Amir Vadai)   
- sdp: fixed signedness warning in compilation + don't use getnstimeofday (Amir Vadai)   
- sdp: split very big tx buffer into smaller sends (Amir Vadai)   
- sdp: QP should be destroyed before its CQs (Amir Vadai)   
- sdp: fix driver to accept credit updates after RCV_SHUTDOWN (Amir Vadai)   
- sdp: Add support for ZCopy combined mode - RDMA Read (Amir Vadai)   
- sdp: removed unnecessary statistics that caused compilation errors on powerpc (Amir Vadai)   
- sdp: fix some warning and bugs in porting to ofed 1.5 (Amir Vadai)   
- sdp: fix bad credits advertised when connection initiated (Amir Vadai)   
- sdp: Fix memory leak in bzcopy (Amir Vadai)   
- sdp: fix wrong credit advertised in Hello MID (Amir Vadai)   
- sdp: fix compilation error on 2.6.30 (Amir Vadai)   
- sdp: fixed coding style (Amir Vadai)   
- sdp: IB_CQ_VECTOR_LEAST_ATTACHED is not supported yet in 1.5 tree (Amir Vadai)   
- sdp: fixed div by zero in sdpstats (Amir Vadai)   
- sdp: make interrupt moderation adaptive (Amir Vadai)   
- sdp: arm nagle timer on not sent packet instead of on sent packet (Amir Vadai)   
- sdp: two bug fixes (Amir Vadai)   
- sdp: make bzcopy poll timeout in jiffies instead of iterations count (Amir Vadai)   
- sdp: fix bad handling for not aligned buffers in bzcopy + removed poll at end of send (Amir Vadai)   
- sdp: fix RX to work well on sink side + cosmetics changes (Amir Vadai)   
- sdp: TX from 1 context only. RX with minimal context switches (Amir Vadai)   
- sdp: don't arm nagle timer for every sent packet (Amir Vadai)   
- sdp: remove leftover from debugging (Amir Vadai)   
- sdp: Do not nagle BZCopy packets (Amir Vadai)   
- sdp: don't do nagle on first packet (Amir Vadai)   
- sdp: fix backports (Amir Vadai)   
- sdp: process RX CQ from interrupt (Amir Vadai)   
- sdp: created sdp_rx and sdp_tx (Amir Vadai)   
- sdp: /proc/net/sdpprf - performance utilities (Amir Vadai)   
- sdp: no tx interrupts (Amir Vadai)   
- sdp: move tx_ring into dedicated structre + many cosmetic fixes (Amir Vadai)   
- sdp: fixed compilation error when statistics turned off (Amir Vadai)   
- sdp: cosmetics changes (Amir Vadai)   
- sdp: Interrupts performance fixes (Amir Vadai)   
- sdp: added /proc/net/sdpstats + packets dump (Amir Vadai)   
- sdp: BUG1311 Netpipe fails with a IB_WC_LOC_LEN_ERR. (Amir Vadai)   
- sdp: change orphan_count and sockets_allocated from atomic_t to percpu_counter (Nicolas Morey-Chaisemartin)   
- sdp: BUG1472 - clean socket timeouts and refcount when device is removed (Amir Vadai)   
- sdp: fixed typo Signed-off-by: Amir Vadai <amirv@mellanox.co.il> (Amir Vadai)   
- sdp: BUG1502 - scheduling while atomic (Amir Vadai)   
- sdp: small typo fixed (Amir Vadai)   
- SDP: BUG1309 - SDP close is slow + fix recv buffer initial size setting (Amir Vadai)   
- SDP: BUG1087 - fixed recovery from failing rdma_create_qp() (Amir Vadai)   
- SDP: Fix to limit max buffer size in sdp_resize_buffers on IA64 (Amir Vadai)   
- sdp: BUG1429 - Sdp doesnt close resources (Amir Vadai)   
- sdp: BUG1047 - crash in sdp_destroy_qp() when no memory (Amir Vadai)   
- SDP: BUG1391 - bugs in the zero-copy send code (Amir Vadai)   
- SDP: BUG1348 - a socket is left after netper on the server side (Amir Vadai)   
- SDP: BUG1348 - sockets are left in CLOSE state with ref count > 0 (Amir Vadai)   
- SDP: BUG1402 - kernel panic when sdp_fin arrive in the middle of closing a socket (Amir Vadai)   
- SDP: BUG1343 - Polygraph test crashes machine (Amir Vadai)   
- sdp: timeout when waiting for sdp_fin (Amir Vadai)   
- sdp: fixed sparse warning Signed-off-by: Amir Vadai <amirv@mellanox.co.il> (Amir Vadai)   
- sdp: do nothing when getting FIN after IB teardown started (Amir Vadai)   
- sdp: Limit skb frag size to 64K-1 (Amir Vadai)   
- sdp: more verbose debugging messages for sock_put and sock_head (Amir Vadai)   
- sdp: BUG1282 - ref count not taken during sdp_shutdown (Amir Vadai)   
- SDP: print socket tcp-state in /proc/net/sdp (Amir Vadai)   
- SDP: fix initial recv buffer size (Amir Vadai)   
- support for 2.6.27 + backports (Amir Vadai)   
- SDP: RDMA_CM_EVENT_TIMWAIT_EXIT renamed into RDMA_CM_EVENT_TIMEWAIT_EXIT. (Vladimir Sokolovsky)   
- SDP: Don't allow destruct socket when having sdp_destroy_work in workqueue (Amir Vadai)   
- SDP: do gracefull close instead of always doing abortive close. (Amir Vadai)   
- SDP: Split sdp_handle_wc() to smaller functions (Amir Vadai)   
- SDP: Use sdp_set_state() (Amir Vadai)   
- Commited old fixes from kernel_patches/fixes/cma_established1.patch into git (Amir Vadai)   
- Modifies SDP to support the updated 2.6.26-rc2 kernel APIs. (Amir Vadai)   
- SDP - Fix compile problem on 2.6.24 ia64 (Jim Mott)   
- SDP: Enable bzcopy by default (Jim Mott)   
- SDP - Bug837: executing netperf with TCP_CORK enabled never ends (Jim Mott)   
- SDP - Bug829: poll() always returns POLLOUT on non-blocking socket (Jim Mott)   
- SDP - Bug294: SDP connect() only allows AF_INET (2), not AF_INET_SDP (27) (Jim Mott)   
- SDP: various bzcopy fixes V2 (Jim Mott)   
- Applied 'kernel_patches/fixes/sdp_skbuff_offset.patch'. (Vladimir Sokolovsky)   
- Applied 'kernel_patches/fixes/sdp_post_credits.patch' (Vladimir Sokolovsky)   
- SDP: Applied 'kernel_patches/fixes/sdp_cq_param.patch' (Vladimir Sokolovsky)   
- SDP: Disable Zcopy. (Jim Mott)   
- Modifies SDP to support the updated 2.6.24-rc2 kernel APIs. (Jim Mott)   
- SDP: A better fix of a potential memory leak in the new bzcopy code. (Dotan Barak)   
- sdp: Fix data corretness regression test failure. (Jim Mott)   
- SDP - Fix reference count locking bug (Jim Mott)   
- SDP - Make bzcopy defualt for 2K and larger transfer size (Jim Mott)   
- SDP - Fix reference count bug that prevents mlx4_ib and ib_sdp unload (Jim Mott)   
- SDP - Add note on where linux bits in sdp_main come from. (Michael S. Tsirkin)   
- SDP - Zero copy bcopy support (Jim Mott)   
- SDP - Method used to allocate socket buffers may cause node to hang (Jim Mott)   
- SDP bug647 - Validate ChRcvBuf range and add comments (Jim Mott)   
- SDP bug646 - Do not send DisConn if there is only 1 credit (Jim Mott)   
- SDP bug644 - DisConn, ChRcvBuf, and ChRcvBufAck sent solicited (Jim Mott)   
- SDP: Add keepalive support (Jim Mott)   
- Fix SDP build issue in 2.6.22-rc7 kernel. There are skbuff.h changes. (Jim Mott)   
- IB/sdp: move the socket to accept queue (Ami Perlmutter)   
- IB/sdp: resize data should be added to skb via skb_put (bugzilla 620) (Ami Perlmutter)   
- IB/sdp: fix problem with sles9 backport (bugzilla 621) (Ami Perlmutter)   
- IB/sdp: slow start recv buffer sizes, and try to resize if out of credits (bugzilla 556) (Ami Perlmutter)   
- IB/sdp: print queued rx and tx status to proc_fs implement SIOCOUTQ ioctl (Ami Perlmutter)   
- IB/sdp: Cleanup compilation warnings. (Michael S. Tsirkin)   
- IB/sdp: Fix to be compliant with CA4-119 (bugzilla 596) (Ami Perlmutter)   
- IB/sdp: adjust module parameter to improve 8K message BW (Ami Perlmutter)   
- IB/sdp: prevent removal of ib device before cleanup (Ami Perlmutter)   
- IB/sdp: fix dma mapping direction (bugzzila num. 556) (Ami Perlmutter)   
- IB/sdp - use the ib_dma interface (Ami Perlmutter)   
- IB/sdp: cm disconnect should wake up any sleeping processes (bugzzila num. 492) (Ami Perlmutter)   
- IB/sdp: add uid and inode to proc_fs info (Amiram Perlmutter)   
- IB/sdp: fix dma leak (Ami Parlmuter)   
- IB/sdp: fix BSDH len field for HH/HAH login messages. (Amiram Perlmutter)   
- IB/sdp: try to send after push mark is set (Ami Parlmuter)   
- IB/sdp: allow users via module parameter to bound SDP's memory use (Amiram Perlmutter)   
- IB/sdp: fix NULL pointer dereference (Amiram Perlmutter)   
- IB/sdp: add proc_fs support (Amiram Perlmutter)   
- IB/sdp: handle shutdown recv on listening socket (Amiram Perlmutter)   
- Update for API changes merged for 2.6.20. (Michael S. Tsirkin)   
- IB/sdp: fill required login fields (Amiram Perlmutter)   
- IB/sdp: poll cq in sendmsg only when sent size is larger than (Amiram Perlmutter)   
- IB/sdp: fixed compilation error (Amiram Perlmutter)   
- IB/sdp: fixed typo in module parameter description (Amiram Perlmutter)   
- IB/sdp: merge small skbs on receive side into larger ones. (Amiram Perlmutter)   
- IB/sdp: modify buffer use calculation to eliminate credit starvation (Amiram Perlmutter)   
- IB/sdp: handle immediate errors on post_send/post_receive (Michael S. Tsirkin)   
- IB/sdp: disable timewait on close if socket has been disconnected (Michael S. Tsirkin)   
- IB/sdp: emulate completion with error if packet queued after disconnect. (Michael S. Tsirkin)   
- IB/sdp: add receive buffer size scale factor (Michael S. Tsirkin)   
- IB/sdp: improve urgent data latency (Amiram Perlmutter)   
- IB/sdp: fix data corruption on SLES10 (should affect other systems as well). (Michael S. Tsirkin)   
- IB/sdp: fix a crash when child is disconnected while parent is being destroyed (Michael S. Tsirkin)   
- CMA should check backlog_queue, not accept_queue, since accept_queue could be changed by accept(). (Michael S. Tsirkin)   
- IB/sdp: request notification only if CQ exists. (Michael S. Tsirkin)   
- IB/sdp: do not kill the child socket in accept queue (Michael S. Tsirkin)   
- IB/sdp: implement SIOCINQ (FIONREAD) (Michael S. Tsirkin)   
- IB/sdp: set inet's daddr and dport on active side as part of connect (Amiram Perlmutter)   
- IB/sdp: Fix skb truesize calculation for the RX skb (Michael S. Tsirkin)   
- IB/sdp: increment seq in case of fin (Amiram Perlmutter)   
- IB/sdp: do not reset offsets on disconnect (Amiram Perlmutter)   
- IB/sdp: Use inet_sk for portability. (Michael S. Tsirkin)   
- IB/sdp: fill in source address in inet_sock when it is available (Amiram Perlmutter)   
- IB/sdp: add support for MSG_OOB (Ami Parlmuter)   
- IB/sdp: Add CQ polling, weight configurable globally. (Michael S. Tsirkin)   
- IB/sdp: Three bugfixes in SDP sockets. (Michael S. Tsirkin)   
- IB/sdp: remove unused include (Michael S. Tsirkin)   
- IB/sdp: Two bugfixes in SDP (Michael S. Tsirkin)   
- IB/sdp: Change PFN_INDEX -> PAGE_INDEX (Michael S. Tsirkin)   
- IB/sdp: Thinko fix: must update nr frags. (Michael S. Tsirkin)   
- IB/sdp:Free unused pages. (Michael S. Tsirkin)   
- IB/sdp: set sport on autobind (Michael S. Tsirkin)   
- IB/sdp: Use high memory for receive buffers (Michael S. Tsirkin)   
- IB/sdp: Fix typo in code (Michael S. Tsirkin)   
- IB/sdp: Implement Nagle algorithm. (Michael S. Tsirkin)   
- IB/sdp:Split data path debug from not (Michael S. Tsirkin)   
- IB/sdp: Fix error handling for case when mr allocation fails (Michael S. Tsirkin)   
- IB/sdp: Comment out gso_seg initialization. (Michael S. Tsirkin)   
- IB/sdp: Fix memory leak in SDP (Michael S. Tsirkin)   
- sdp: Add SDP - lone SDP from SVN 8227 (Michael S. Tsirkin)   
- mlx4_ib: Memory leak on Dom0 with SRIOV. (Venkat Venkatsubra)  [Orabug: 21675211]  
- RDS: Handle RDMA_CM_EVENT_TIMEWAIT_EXIT event. (Venkat Venkatsubra)  [Orabug: 21675221]  
- uek-rpm: build: Update the base release to 9 with stable v4.1.9 (Santosh Shilimkar)   
- uek-rpm: sparc: update FW_LOADER_USER and TRUSTED_KEYRING (Allen Pais)  [Orabug: 21880958] [Orabug: 21900415]  
- Revert "sparc/PCI: Add mem64 resource parsing for root bus" (Santosh Shilimkar)  [Orabug: 21937193]  
- Revert "PCI: Set under_pref for mem64 resource of pcie device" (Santosh Shilimkar)  [Orabug: 21937193]  
- sparc/crypto: initialize blkcipher.ivsize (Dave Kleikamp)   
- Linux 4.1.9 (Greg Kroah-Hartman)   
- cxl: Don't remove AFUs/vPHBs in cxl_reset (Daniel Axtens)   
- ipv4: off-by-one in continuation handling in /proc/net/route (Andy Whitcroft)   
- net: dsa: Do not override PHY interface if already configured (Florian Fainelli)   
- inet: fix races with reqsk timers (Eric Dumazet)   
- inet: fix possible request socket leak (Eric Dumazet)   
- netlink: make sure -EBUSY won't escape from netlink_insert (Daniel Borkmann)   
- bna: fix interrupts storm caused by erroneous packets (Ivan Vecera)   
- bridge: netlink: account for the IFLA_BRPORT_PROXYARP_WIFI attribute size and policy (Nikolay Aleksandrov)   
- bridge: netlink: account for the IFLA_BRPORT_PROXYARP attribute size and policy (Nikolay Aleksandrov)   
- udp: fix dst races with multicast early demux (Eric Dumazet)   
- rds: fix an integer overflow test in rds_info_getsockopt() (Dan Carpenter)   
- rocker: free netdevice during netdevice removal (Ido Schimmel)   
- net: sched: fix refcount imbalance in actions (Daniel Borkmann)   
- act_bpf: fix memory leaks when replacing bpf programs (Daniel Borkmann)   
- packet: tpacket_snd(): fix signed/unsigned comparison (Alexander Drozdov)   
- packet: missing dev_put() in packet_do_bind() (Lars Westerhoff)   
- fib_trie: Drop unnecessary calls to leaf_pull_suffix (Alexander Duyck)   
- net/mlx4_core: Fix wrong index in propagating port change event to VFs (Jack Morgenstein)   
- bridge: netlink: fix slave_changelink/br_setport race conditions (Nikolay Aleksandrov)   
- virtio_net: don't require ANY_LAYOUT with VERSION_1 (Michael S. Tsirkin)   
- netlink: don't hold mutex in rcu callback when releasing mmapd ring (Florian Westphal)   
- inet: frags: fix defragmented packet's IP header for af_packet (Edward Hyunkoo Jee)   
- sched: cls_flow: fix panic on filter replace (Daniel Borkmann)   
- sched: cls_bpf: fix panic on filter replace (Daniel Borkmann)   
- bonding: correct the MAC address for "follow" fail_over_mac policy (dingtianhong)   
- Revert "sit: Add gro callbacks to sit_offload" (Herbert Xu)   
- bonding: fix destruction of bond with devices different from arphrd_ether (Nikolay Aleksandrov)   
- ipv6: lock socket in ip6_datagram_connect() (Eric Dumazet)   
- isdn/gigaset: reset tty->receive_room when attaching ser_gigaset (Tilman Schmidt)   
- fq_codel: fix a use-after-free (WANG Cong)   
- bridge: mdb: fix double add notification (Nikolay Aleksandrov)   
- net: Fix skb_set_peeked use-after-free bug (Herbert Xu)   
- net: Fix skb csum races when peeking (Herbert Xu)   
- net: Clone skb before setting peeked flag (Herbert Xu)   
- net/xen-netback: off by one in BUG_ON() condition (Dan Carpenter)   
- net: call rcu_read_lock early in process_backlog (Julian Anastasov)   
- net: do not process device backlog during unregistration (Julian Anastasov)   
- bridge: fix potential crash in __netdev_pick_tx() (Eric Dumazet)   
- net: pktgen: fix race between pktgen_thread_worker() and kthread_stop() (Oleg Nesterov)   
- bridge: mdb: zero out the local br_ip variable before use (Nikolay Aleksandrov)   
- net/tipc: initialize security state for new connection socket (Stephen Smalley)   
- ip_tunnel: fix ipv4 pmtu check to honor inner ip header df (Timo Teräs)   
- rtnetlink: verify IFLA_VF_INFO attributes before passing them to driver (Daniel Borkmann)   
- Revert "dev: set iflink to 0 for virtual interfaces" (Nicolas Dichtel)   
- net: graceful exit from netif_alloc_netdev_queues() (Eric Dumazet)   
- rhashtable: fix for resize events during table walk (Phil Sutter)   
- ipv6: Make MLD packets to only be processed locally (Angga)   
- jbd2: avoid infinite loop when destroying aborted journal (Jan Kara)   
- lib/decompressors: use real out buf size for gunzip with kernel (Yinghai Lu)   
- hfs,hfsplus: cache pages correctly between bnode_create and bnode_free (Hin-Tak Leung)   
- net: stmmac: dwmac-rk: Fix clk rate when provided by soc (Heiko Stübner)   
- stmmac: troubleshoot unexpected bits in des0 & des1 (Alexey Brodkin)   
- stmmac: fix check for phydev being open (Alexey Brodkin)   
- IB/mlx4: Fix incorrect cq flushing in error state (Ariel Nahum)   
- IB/mlx4: Use correct SL on AH query under RoCE (Noa Osherovich)   
- IB/mlx4: Forbid using sysfs to change RoCE pkeys (Jack Morgenstein)   
- IB/mlx4: Fix potential deadlock when sending mad to wire (Jack Morgenstein)   
- IB/mlx5: avoid destroying a NULL mr in reg_user_mr error flow (Haggai Eran)   
- IB/iser: Fix possible bogus DMA unmapping (Sagi Grimberg)   
- IB/iser: Fix missing return status check in iser_send_data_out (Sagi Grimberg)   
- IB/uverbs: Fix race between ib_uverbs_open and remove_one (Yishai Hadas)   
- IB/uverbs: reject invalid or unknown opcodes (Christoph Hellwig)   
- IB/qib: Change lkey table allocation to support more MRs (Mike Marciniszyn)   
- IB/srp: Stop the scsi_eh_<n> and scsi_tmf_<n> threads if login fails (Bart Van Assche)   
- IB/srp: Handle partial connection success correctly (Bart Van Assche)   
- ideapad-laptop: Add Lenovo Yoga 3 14 to no_hw_rfkill dmi list (Hans de Goede)   
- hfs: fix B-tree corruption after insertion at position 0 (Hin-Tak Leung)   
- eCryptfs: Invalidate dcache entries when lower i_nlink is zero (Tyler Hicks)   
- iommu/vt-d: Really use upper context table when necessary (Joerg Roedel)   
- iommu/tegra-smmu: Parameterize number of TLB lines (Thierry Reding)   
- iommu/io-pgtable-arm: Unmap and free table when overwriting with block (Will Deacon)   
- iommu/fsl: Really fix init section(s) content (Emil Medve)   
- md: flush ->event_work before stopping array. (NeilBrown)   
- md/raid10: always set reshape_safe when initializing reshape_position. (NeilBrown)   
- md/raid5: don't let shrink_slab shrink too far. (NeilBrown)   
- md/raid5: avoid races when changing cache size. (NeilBrown)   
- mmc: core: fix race condition in mmc_wait_data_done (Jialing Fu)   
- mmc: sdhci: also get preset value and driver type for MMC_DDR52 (Jisheng Zhang)   
- mmc: sdhci-pci: set the clear transfer mode register quirk for O2Micro (Adam Lee)   
- fs: Don't dump core if the corefile would become world-readable. (Jann Horn)   
- fs: if a coredump already exists, unlink and recreate with O_EXCL (Jann Horn)   
- vmscan: fix increasing nr_isolated incurred by putback unevictable pages (Jaewon Kim)   
- parisc: Filter out spurious interrupts in PA-RISC irq handler (Helge Deller)   
- parisc: Use double word condition in 64bit CAS operation (John David Anglin)   
- PCI,parisc: Enable 64-bit bus addresses on PA-RISC (Helge Deller)   
- rtc: abx80x: fix RTC write bit (Mitja Spes)   
- rtc: s5m: fix to update ctrl register (Joonyoung Shim)   
- rtc: s3c: fix disabled clocks for alarm (Joonyoung Shim)   
- SUNRPC: Lock the transport layer on shutdown (Trond Myklebust)   
- SUNRPC: Ensure that we wait for connections to complete before retrying (Trond Myklebust)   
- SUNRPC: xs_reset_transport must mark the connection as disconnected (Trond Myklebust)   
- SUNRPC: Fix a thinko in xs_connect() (Trond Myklebust)   
- net: sunrpc: fix tracepoint Warning: unknown op '->' (Pratyush Anand)   
- Revert "NFSv4: Remove incorrect check in can_open_delegated()" (Trond Myklebust)   
- NFSv4.1: Fix a protocol issue with CLOSE stateids (Trond Myklebust)   
- NFSv4.1/flexfiles: Fix a protocol error in layoutreturn (Trond Myklebust)   
- NFS41/flexfiles: zero out DS write wcc (Peng Tao)   
- NFSv4: Force a post-op attribute update when holding a delegation (Trond Myklebust)   
- NFS41/flexfiles: update inode after write finishes (Peng Tao)   
- NFS: nfs_set_pgio_error sometimes misses errors (Trond Myklebust)   
- NFS: Fix a NULL pointer dereference of migration recovery ops for v4.2 client (Kinglong Mee)   
- NFSv4.1/pNFS: Fix borken function _same_data_server_addrs_locked() (Trond Myklebust)   
- NFS: Don't let the ctime override attribute barriers. (Trond Myklebust)   
- NFSv4: don't set SETATTR for O_RDONLY|O_EXCL (NeilBrown)   
- nfsd: ensure that delegation stateid hash references are only put once (Jeff Layton)   
- nfsd: ensure that the ol stateid hash reference is only put once (Jeff Layton)   
- nfsd: Fix an FS_LAYOUT_TYPES/LAYOUT_TYPES encode bug (Kinglong Mee)   
- NFSv4/pnfs: Ensure we don't miss a file extension (Trond Myklebust)   
- Btrfs: check if previous transaction aborted to avoid fs corruption (Filipe Manana)   
- media: am437x-vpfe: Fix a race condition during release (Benoit Parrot)   
- media: am437x-vpfe: Requested frame size and fmt overwritten by current sensor setting (Benoit Parrot)   
- v4l: omap3isp: Fix sub-device power management code (Sakari Ailus)   
- rc-core: fix remove uevent generation (David Härdeman)   
- mm: make page pfmemalloc check more robust (Michal Hocko)   
- x86/mm: Initialize pmd_idx in page_table_range_init_count() (Minfei Huang)   
- mm: check if section present during memory block registering (Yinghai Lu)   
- Add radeon suspend/resume quirk for HP Compaq dc5750. (Jeffery Miller)   
- CIFS: fix type confusion in copy offload ioctl (Jann Horn)   
- powerpc/mm: Recompute hash value after a failed update (Aneesh Kumar K.V)   
- powerpc/boot: Specify ABI v2 when building an LE boot wrapper (Benjamin Herrenschmidt)   
- crypto: vmx - Adding enable_kernel_vsx() to access VSX instructions (Leonidas Da Silva Barbosa)   
- powerpc: Uncomment and make enable_kernel_vsx() routine available (Leonidas Da Silva Barbosa)   
- powerpc/rtas: Introduce rtas_get_sensor_fast() for IRQ handlers (Thomas Huth)   
- powerpc/mm: Fix pte_pagesize_index() crash on 4K w/64K hash (Michael Ellerman)   
- powerpc/eeh: Fix fenced PHB caused by eeh_slot_error_detail() (Gavin Shan)   
- powerpc/eeh: Probe after unbalanced kref check (Daniel Axtens)   
- powerpc/pseries: Fix corrupted pdn list (Gavin Shan)   
- pinctrl: at91: fix null pointer dereference (David Dueck)   
- ALSA: hda - Fix white noise on Dell M3800 (Niranjan Sivakumar)   
- ALSA: hda - Add some FIXUP quirks for white noise on Dell laptop. (Woodrow Shen)   
- ALSA: hda - Use ALC880_FIXUP_FUJITSU for FSC Amilo M1437 (Takashi Iwai)   
- ALSA: hda - Enable headphone jack detect on old Fujitsu laptops (Takashi Iwai)   
- ALSA: usb-audio: correct the value cache check. (Yao-Wen Mao)   
- Input: evdev - do not report errors form flush() (Takashi Iwai)   
- arm64: KVM: Disable virtual timer even if the guest is not using it (Marc Zyngier)   
- KVM: arm64: add workaround for Cortex-A57 erratum #852523 (Will Deacon)   
- arm/arm64: KVM: vgic: Check for !irqchip_in_kernel() when mapping resources (Pavel Fedin)   
- arm64: errata: add module build workaround for erratum #843419 (Will Deacon)   
- arm64: head.S: initialise mdcr_el2 in el2_setup (Will Deacon)   
- arm64: compat: fix vfp save/restore across signal handlers in big-endian (Will Deacon)   
- arm64: set MAX_MEMBLOCK_ADDR according to linear region size (Ard Biesheuvel)   
- of/fdt: make memblock maximum physical address arch configurable (Ard Biesheuvel)   
- arm64: flush FP/SIMD state correctly after execve() (Ard Biesheuvel)   
- arm64: kconfig: Move LIST_POISON to a safe value (Jeff Vander Stoep)   
- Revert "ext4: remove block_device_ejected" (Theodore Ts'o)   
- ext4: don't manipulate recovery flag when freezing no-journal fs (Eric Sandeen)   
- cxl: Fix unbalanced pci_dev_get in cxl_probe (Daniel Axtens)   
- cxl: Remove racy attempt to force EEH invocation in reset (Daniel Axtens)   
- mac80211: enable assoc check for mesh interfaces (Bob Copeland)   
- MIPS: math-emu: Emulate missing BC1{EQ,NE}Z instructions (Markos Chandras)   
- MIPS: math-emu: Allow m{f,t}hc emulation on MIPS R6 (Markos Chandras)   
- tg3: Fix temperature reporting (Jean Delvare)   
- igb: Fix oops caused by missing queue pairing (Shota Suzuki)   
- rtlwifi: rtl8821ae: Fix an expression that is always false (Larry Finger)   
- rtlwifi: rtl8192cu: Add new device ID (Adrien Schildknecht)   
- unshare: Unsharing a thread does not require unsharing a vm (Eric W. Biederman)   
- blk-mq: fix buffer overflow when reading sysfs file of 'pending' (Ming Lei)   
- nfc: nci: hci: Add check on skb nci_hci_send_cmd parameter (Christophe Ricard)   
- NFC: st21nfca: fix use of uninitialized variables in error path (Christophe Ricard)   
- uek-rpm: configs: Rationalise CRYPTO config for OL6 (John Haxby)   
- igb: bump version to igb-5.3.0 (Todd Fujinaka)  [Orabug: 21792102]  
- igb: use ARRAY_SIZE to replace calculating sizeof(a)/sizeof(a[0]) (Todd Fujinaka)  [Orabug: 21792102]  
- igb: report unsupported ethtool settings in set_coalesce (Todd Fujinaka)  [Orabug: 21792102]  
- igb: Fix i354 88E1112 PHY on RCC boards using AutoMediaDetect (Todd Fujinaka)  [Orabug: 21792102]  
- igb: Pull timestamp from fragment before adding it to skb (Alexander Duyck)  [Orabug: 21792102]  
- igb: only report generic filters in get_ts_info (Jacob Keller)  [Orabug: 21792102]  
- igb: bump version of igb to 5.2.18 (Todd Fujinaka)  [Orabug: 21792102]  
- igb: disable IPv6 extension header processing (Todd Fujinaka)  [Orabug: 21792102]  
- igb: Don't use NETDEV_FRAG_PAGE_MAX_SIZE in descriptor calculation (Alexander Duyck)  [Orabug: 21792102]  
- igb: simplify and clean up igb_enable_mas() (Todd Fujinaka)  [Orabug: 21792102]  
- e1000e: Increase driver version number (Raanan Avargil)  [Orabug: 21792108]  
- e1000e: Fix tight loop implementation of systime read algorithm (Raanan Avargil)  [Orabug: 21792108]  
- e1000e: Fix incorrect ASPM locking (Raanan Avargil)  [Orabug: 21792108]  
- e1000e: Cosmetic changes (Raanan Avargil)  [Orabug: 21792108]  
- e1000e: Fix EEE in Sx implementation (Raanan Avargil)  [Orabug: 21792108]  
- e1000e: Cleanup qos request in error handling of e1000_open (Jia-Ju Bai)  [Orabug: 21792108]  
- e1000e: i219 - k1 workaround for LPT is not required for SPT (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: i219 - Increase minimum FIFO read/write min gap (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: i219 - increase IPG for speed 10/100 full duplex (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: i219 - fix to enable both ULP and EEE in Sx state (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: synchronization of MAC-PHY interface only on non- ME systems (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: fix locking issue with e1000e_disable_aspm (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: Bump the version to 3.2.5 (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: fix unit hang during loopback test (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: fix systim issues (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: fix legacy interrupt handling in i219 (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: fix flush_desc_ring implementation (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: fix logical error in flush_desc_rings (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: remove call to do_div and sign mismatch warning (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: i219 execute unit hang fix on every reset or power state transition (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: i219 fix unit hang on reset and runtime D3 (Yanir Lubetkin)  [Orabug: 21792108]  
- e1000e: fix call to do_div() to use u64 arg (Jeff Kirsher)  [Orabug: 21792108]  
- e1000e: Do not allow CRC stripping to be disabled on 82579 w/ jumbo frames (Alexander Duyck)  [Orabug: 21792108]  

* Mon Oct 5 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.8-15.1.el7uek] 
- uek-rpm: sparc: update FW_LOADER_USER and TRUSTED_KEYRING (Allen Pais)  [Orabug: 21880958] [Orabug: 21900415]  
- Revert "sparc/PCI: Add mem64 resource parsing for root bus" (Santosh Shilimkar)  [Orabug: 21937193]  
- Revert "PCI: Set under_pref for mem64 resource of pcie device" (Santosh Shilimkar)  [Orabug: 21937193]  

* Fri Sep 25 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.8-15.el7uek] 
- use SET_NETDEV_DEV() to set up the vdev in vnet_new() (Sowmini Varadhan)   
- lib/iommu-common.c: do not try to deref a null iommu->lazy_flush() pointer when n < pool->hint (Sowmini Varadhan)   
- uek-rpm: configs: sparc64: enable dtrace support (Nick Alcock)   
- uek-rpm: build: Update the base release to 8 with stable v4.1.8 (Santosh Shilimkar)   
- uek-rpm: config: sxge/sxgevf: enable driver (Brian Maly)  [Orabug: 20509061]  
- revert commit ff8fb335221e2c446b0d4cbea26be371fd2feb64 (Tariq Saeed)  [Orabug: 21696932]  
- sxge/sxgevf: port to uek4 (Joyce Yu)  [Orabug: 20509061]  
- block: loop: don't enable direct-io unless the filesystem supports it (Dave Kleikamp)   
- Linux 4.1.8 (Greg Kroah-Hartman)   
- ARM: rockchip: fix broken build (Caesar Wang)   
- fs: create and use seq_show_option for escaping (Kees Cook)   
- hpfs: update ctime and mtime on directory modification (Mikulas Patocka)   
- fs: Set the size of empty dirs to 0. (Eric W. Biederman)   
- drivercore: Fix unregistration path of platform devices (Grant Likely)   
- ACPI, PCI: Penalize legacy IRQ used by ACPI SCI (Jiang Liu)   
- ARM: dts: rockchip: fix rk3288 watchdog irq (Heiko Stuebner)   
- ARM: rockchip: fix the CPU soft reset (Caesar Wang)   
- ARM: OMAP2+: DRA7: clockdomain: change l4per2_7xx_clkdm to SW_WKUP (Vignesh R)   
- ARM: dts: fix clock-frequency of display timing0 for exynos3250-rinato (Hyungwon Hwang)   
- ARM: orion5x: fix legacy orion5x IRQ numbers (Benjamin Cama)   
- of/address: Don't loop forever in of_find_matching_node_by_address(). (David Daney)   
- soc/tegra: pmc: Avoid usage of uninitialized variable (Thierry Reding)   
- x86/mce: Reenable CMCI banks when swiching back to interrupt mode (Xie XiuQi)   
- regulator: pbias: Fix broken pbias disable functionality (Kishon Vijay Abraham I)   
- auxdisplay: ks0108: fix refcount (Sudip Mukherjee)   
- spi/spi-xilinx: Fix mixed poll/irq mode (Ricardo Ribalda Delgado)   
- spi/spi-xilinx: Fix spurious IRQ ACK on irq mode (Ricardo Ribalda Delgado)   
- Doc: ABI: testing: configfs-usb-gadget-sourcesink (Peter Chen)   
- Doc: ABI: testing: configfs-usb-gadget-loopback (Peter Chen)   
- devres: fix devres_get() (Masahiro Yamada)   
- xtensa: fix kernel register spilling (Max Filippov)   
- xtensa: fix threadptr reload on return to userspace (Max Filippov)   
- KVM: x86: Use adjustment in guest cycles when handling MSR_IA32_TSC_ADJUST (Haozhong Zhang)   
- KVM: PPC: Book3S HV: Fix race in reading change bit when removing HPTE (Paul Mackerras)   
- KVM: PPC: Book3S HV: Exit on H_DOORBELL if HOST_IPI is set (Gautham R. Shenoy)   
- KVM: MMU: fix validation of mmio page fault (Xiao Guangrong)   
- HID: cp2112: fix I2C_SMBUS_BYTE write (Ellen Wang)   
- HID: cp2112: fix byte order in SMBUS operations (Ellen Wang)   
- HID: usbhid: Fix the check for HID_RESET_PENDING in hid_io_error (Don Zickus)   
- crypto: ghash-clmulni: specify context size for ghash async algorithm (Andrey Ryabinin)   
- crypto: vmx - Fixing GHASH Key issue on little endian (Leonidas Da Silva Barbosa)   
- serial: samsung: fix DMA for FIFO smaller than cache line size (Robert Baldyga)   
- serial: samsung: fix DMA mode enter condition for small FIFO sizes (Marek Szyprowski)   
- serial: 8250_pci: Add support for Pericom PI7C9X795[1248] (Adam Lee)   
- serial: 8250: bind to ALi Fast Infrared Controller (ALI5123) (Maciej S. Szmigiero)   
- serial: 8250: don't bind to SMSC IrCC IR port (Maciej S. Szmigiero)   
- ASoC: arizona: Poll for FLL clock OK rather than use interrupts (Charles Keepax)   
- ASoC: arizona: Fix gain settings of FLL in free-run mode (Nikesh Oswal)   
- ASoC: adav80x: Remove .read_flag_mask setting from adav80x_regmap_config (Axel Lin)   
- ASoC: samsung: Remove redundant arndale_audio_remove (Vaishali Thakkar)   
- ASoC: rt5640: fix line out no sound issue (John Lin)   
- tty: serial: men_z135_uart.c: Fix race between IRQ and set_termios() (Johannes Thumshirn)   
- usb: host: ehci-sys: delete useless bus_to_hcd conversion (Peter Chen)   
- usb: gadget: f_uac2: finalize wMaxPacketSize according to bandwidth (Peter Chen)   
- usb: dwc3: ep0: Fix mem corruption on OUT transfers of more than 512 bytes (Kishon Vijay Abraham I)   
- doc: usb: gadget-testing: using the updated testusb.c (Peter Chen)   
- usb: gadget: m66592-udc: forever loop in set_feature() (Dan Carpenter)   
- xfs: Fix file type directory corruption for btree directories (Jan Kara)   
- xfs: Fix xfs_attr_leafblock definition (Jan Kara)   
- libxfs: readahead of dir3 data blocks should use the read verifier (Darrick J. Wong)   
- USB: pl2303: fix baud-rate divisor calculations (Michał Pecio)   
- USB: ftdi_sio: Added custom PID for CustomWare products (Matthijs Kooijman)   
- USB: qcserial: add HP lt4111 LTE/EV-DO/HSPA+ Gobi 4G Module (David Ward)   
- USB: symbolserial: Use usb_get_serial_port_data (Philipp Hachtmann)   
- spi: dw: Allow interface drivers to limit data I/O to word sizes (Michael van der Westhuizen)   
- spi: img-spfi: fix kbuild test robot warning (Sifan Naeem)   
- spi: img-spfi: fix multiple calls to request gpio (Sifan Naeem)   
- spi: img-spfi: check for timeout error before proceeding (Sifan Naeem)   
- spi: sh-msiof: Fix FIFO size to 64 word from 256 word (Koji Matsuoka)   
- spi: Fix regression in spi-bitbang-txrx.h (Lars Persson)   
- spi: bcm2835: set up spi-mode before asserting cs-gpio (Martin Sperl)   
- PCI: Disable async suspend/resume for JMicron multi-function SATA/AHCI (Zhang Rui)   
- PCI: Add VPD function 0 quirk for Intel Ethernet devices (Mark Rustad)   
- PCI: Add dev_flags bit to access VPD through function 0 (Mark Rustad)   
- PCI: Fix TI816X class code quirk (Bjorn Helgaas)   
- clk: qcom: Fix MSM8916 prng clock enable bit (Georgi Djakov)   
- clk: qcom: Set CLK_SET_RATE_PARENT on ce1 clocks (Stephen Boyd)   
- clk: pxa: fix core frequency reporting unit (Robert Jarzmik)   
- clk: versatile: off by one in clk_sp810_timerclken_of_get() (Dan Carpenter)   
- clk: pistachio: correct critical clock list (Damien.Horsley)   
- clk: pistachio: Fix override of clk-pll settings from boot loader (Zdenko Pulitika)   
- clk: s5pv210: add missing call to samsung_clk_of_add_provider() (Marek Szyprowski)   
- clk: exynos4: Fix wrong clock for Exynos4x12 ADC (Krzysztof Kozlowski)   
- clk: rockchip: rk3288: add CLK_SET_RATE_PARENT to sclk_mac (Heiko Stuebner)   
- PM / clk: don't return int on __pm_clk_enable() (Colin Ian King)   
- staging: comedi: usbduxsigma: don't clobber ao_timer in command test (Ian Abbott)   
- staging: comedi: usbduxsigma: don't clobber ai_timer in command test (Ian Abbott)   
- staging: comedi: adl_pci7x3x: fix digital output on PCI-7230 (Ian Abbott)   
- sched: Fix cpu_active_mask/cpu_online_mask race (Jan H. Schönherr)   
- iio: adis16480: Fix scale factors (Lars-Peter Clausen)   
- iio: Add inverse unit conversion macros (Lars-Peter Clausen)   
- iio: adis16400: Fix adis16448 gyroscope scale (Lars-Peter Clausen)   
- iio: industrialio-buffer: Fix iio_buffer_poll return value (Cristina Opriceana)   
- iio: event: Remove negative error code from iio_event_poll (Cristina Opriceana)   
- iio: bmg160: IIO_BUFFER and IIO_TRIGGERED_BUFFER are required (Markus Pargmann)   
- s390/setup: fix novx parameter (Martin Schwidefsky)   
- s390/sclp: fix compile error (Sebastian Ott)   
- drm/i915: Limit the number of loops for reading a split 64bit register (Chris Wilson)   
- drm/i915: Always mark the object as dirty when used by the GPU (Chris Wilson)   
- drm/i915: Allow DSI dual link to be configured on any pipe (Gaurav K Singh)   
- drm/qxl: validate monitors config modes (Jonathon Jongsma)   
- drm/i915: Preserve SSC earlier (Lukas Wunner)   
- drm/radeon: fix HDMI quantization_range for pre-DCE5 asics (Alex Deucher)   
- drm/radeon/native: Send out the full AUX address (Alex Deucher)   
- drm/radeon/atom: Send out the full AUX address (Ville Syrjälä)   
- drm/i915: Check DP link status on long hpd too (Ville Syrjälä)   
- drm/i915: apply the PCI_D0/D3 hibernation workaround everywhere on pre GEN6 (Imre Deak)   
- DRM - radeon: Don't link train DisplayPort on HPD until we get the dpcd (Stephen Chandler Paul)   
- x86/ldt: Further fix FPU emulation (Andy Lutomirski)   
- x86/ldt: Correct FPU emulation access to LDT (Juergen Gross)   
- x86/ldt: Correct LDT access in single stepping logic (Juergen Gross)   
- x86/ldt: Make modify_ldt synchronous (Andy Lutomirski)   {CVE-2015-5157} 
- Linux 4.1.7 (Greg Kroah-Hartman)   
- ARM: 8405/1: VDSO: fix regression with toolchains lacking ld.bfd executable (Nathan Lynch)   
- x86/idle: Restore trace_cpu_idle to mwait_idle() calls (Jisheng Zhang)   
- x86/apic: Fix fallout from x2apic cleanup (Thomas Gleixner)   
- x86/xen: make CONFIG_XEN depend on CONFIG_X86_LOCAL_APIC (David Vrabel)   
- arm64: perf: fix unassigned cpu_pmu->plat_device when probing PMU PPIs (Shannon Zhao)   
- arm64: KVM: Fix host crash when injecting a fault into a 32bit guest (Marc Zyngier)   
- fnic: Use the local variable instead of I/O flag to acquire io_req_lock in fnic_queuecommand() to avoid deadloack (Hiral Shah)   
- Add factory recertified Crucial M500s to blacklist (Guillermo A. Amaral)   
- can: pcan_usb: don't provide CAN FD bittimings by non-FD adapters (Marc Kleine-Budde)   
- SCSI: Fix NULL pointer dereference in runtime PM (Alan Stern)   
- genirq: Introduce irq_chip_set_type_parent() helper (Grygorii Strashko)   
- genirq: Don't return ENOSYS in irq_chip_retrigger_hierarchy (Grygorii Strashko)   
- ARM: OMAP: wakeupgen: Restore the irq_set_type() mechanism (Grygorii Strashko)   
- irqchip/crossbar: Restore set_wake functionality (Grygorii Strashko)   
- irqchip/crossbar: Restore the mask on suspend behaviour (Grygorii Strashko)   
- irqchip/crossbar: Restore the irq_set_type() mechanism (Grygorii Strashko)   
- 9p: ensure err is initialized to 0 in p9_client_read/write (Vincent Bernat)   
- drm/i915: Avoid TP3 on CHV (Thulasimani,Sivakumar)   
- drm/i915: remove HBR2 from chv supported list (Thulasimani,Sivakumar)   
- drm/i915: Flag the execlists context object as dirty after every use (Chris Wilson)   
- drm/atmel-hlcdc: Compile suspend/resume for PM_SLEEP only (Thierry Reding)   
- Input: gpio_keys_polled - request GPIO pin as input. (Vincent Pelletier)   
- PCI: Don't use 64-bit bus addresses on PA-RISC (Bjorn Helgaas)   
- target/iscsi: Fix double free of a TUR followed by a solicited NOPOUT (Alexei Potashnik)   
- mac80211: fix invalid read in minstrel_sort_best_tp_rates() (Adrien Schildknecht)   
- ALSA: hda: fix possible NULL dereference (Markus Osterhoff)   
- ALSA: hda - Fix path power activation (Takashi Iwai)   
- ALSA: hda - Check all inputs for is_active_nid_for_any() (Takashi Iwai)   
- ALSA: hda - Shutdown CX20722 on reboot/free to avoid spurious noises (David Henningsson)   
- ALSA: usb: Add native DSD support for Gustard DAC-X20U (Jurgen Kramer)   
- ALSA: hda - Fix the white noise on Dell laptop (Woodrow Shen)   
- ALSA: usb-audio: Fix runtime PM unbalance (Takashi Iwai)   
- cpuset: use trialcs->mems_allowed as a temp variable (Alban Crequy)   
- Revert "libata: Implement NCQ autosense" (Tejun Heo)   
- Revert "libata: Implement support for sense data reporting" (Tejun Heo)   
- Revert "libata-eh: Set 'information' field for autosense" (Tejun Heo)   
- crypto: caam - fix memory corruption in ahash_final_ctx (Horia Geant?)   
- crypto: nx - respect sg limit bounds when building sg lists for SHA (Jan Stancek)   
- sd: Fix maximum I/O size for BLOCK_PC requests (Martin K. Petersen)   
- libiscsi: Fix host busy blocking during connection teardown (John Soni Jose)   
- MIPS: Fix seccomp syscall argument for MIPS64 (Markos Chandras)   
- regmap: regcache-rbtree: Clean new present bits on present bitmap resize (Guenter Roeck)   
- Revert x86 sigcontext cleanups (Linus Torvalds)   
- mfd: arizona: Fix initialisation of the PM runtime (Charles Keepax)   
- ARM: invalidate L1 before enabling coherency (Russell King)   
- ARM: v7 setup function should invalidate L1 cache (Russell King)   
- ARM: 8384/1: VDSO: force use of BFD linker (Nathan Lynch)   
- ARM: 8385/1: VDSO: group link options (Nathan Lynch)   
- ARM: dts: OMAP5: Fix broken pbias device creation (Kishon Vijay Abraham I)   
- ARM: dts: OMAP4: Fix broken pbias device creation (Kishon Vijay Abraham I)   
- ARM: dts: dra7: Fix broken pbias device creation (Kishon Vijay Abraham I)   
- ARM: dts: omap243x: Fix broken pbias device creation (Kishon Vijay Abraham I)   
- ARM: imx6: correct i.MX6 PCIe interrupt routing (Lucas Stach)   
- libfc: Fix fc_fcp_cleanup_each_cmd() (Bart Van Assche)   
- libfc: Fix fc_exch_recv_req() error path (Bart Van Assche)   
- drm/vmwgfx: Fix execbuf locking issues (Thomas Hellstrom)   
- drm/radeon: add new OLAND pci id (Alex Deucher)   
- HID: uclogic: fix limit in uclogic_tablet_enable() (Dan Carpenter)   
- HID: hid-input: Fix accessing freed memory during device disconnect (Krzysztof Kozlowski)   
- EDAC, ppc4xx: Access mci->csrows array elements properly (Michael Walle)   
- localmodconfig: Use Kbuild files too (Richard Weinberger)   
- dm thin metadata: delete btrees when releasing metadata snapshot (Joe Thornber)   
- xen/xenbus: Don't leak memory when unmapping the ring on HVM backend (Julien Grall)   
- x86/xen: build "Xen PV" APIC driver for domU as well (Jason A. Donenfeld)   
- rtlwifi: Fix NULL dereference when PCI driver used as an AP (Luis Felipe Dominguez Vega)   
- rtlwifi: rtl8723be: Add module parameter for MSI interrupts (Larry Finger)   
- iwlwifi: pcie: fix prepare card flow (Emmanuel Grumbach)   
- perf: Fix PERF_EVENT_IOC_PERIOD migration race (Peter Zijlstra)   
- perf: Fix double-free of the AUX buffer (Ben Hutchings)   
- perf: Fix running time accounting (Peter Zijlstra)   
- perf: Fix fasync handling on inherited events (Peter Zijlstra)   
- rsi: Fix failure to load firmware after memory leak fix and fix the leak (Mike Looijmans)   
- xen-blkback: replace work_pending with work_busy in purge_persistent_gnt() (Bob Liu)   
- xen-blkfront: don't add indirect pages to list when !feature_persistent (Bob Liu)   
- clk: pxa: pxa3xx: fix CKEN register access (Robert Jarzmik)   
- mm/hwpoison: fix fail isolate hugetlbfs page w/ refcount held (Wanpeng Li)   
- mm/hwpoison: fix page refcount of unknown non LRU page (Wanpeng Li)   
- ipc/sem.c: update/correct memory barriers (Manfred Spraul)   
- ipc,sem: fix use after free on IPC_RMID after a task using same semaphore set exits (Herton R. Krzesinski)   
- block: loop: Enable directIO on nfs (Dave Kleikamp)   
- block: loop: Enable directIO whenever possible (Dave Kleikamp)   
- block: loop: support DIO & AIO (Ming Lei)   
- block: loop: prepare for supporing direct IO (Ming Lei)   
- block: loop: use kthread_work (Ming Lei)   
- block: loop: set QUEUE_FLAG_NOMERGES for request queue of loop (Ming Lei)   
- fs: direct-io: don't dirtying pages for ITER_BVEC/ITER_KVEC direct read (Ming Lei)   
- nfs: don't dirty kernel pages read by direct-io (Dave Kleikamp)   
- block: loop: avoiding too many pending per work I/O (Ming Lei)   
- block: loop: convert to per-device workqueue (Santosh Shilimkar)   

* Thu Sep 17 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.6-14.el7uek] 
- rtnetlink: RTEXT_FILTER_SKIP_STATS support to avoid dumping inet/inet6 stats (Sowmini Varadhan)  [Orabug: 21857538]  
- bonding: If IP route look-up to send an ARP fails, mark in bonding structure as no ARP sent. (Rama Nichanamatlu)  [Orabug: 21844825]  
- uek-rpm: build: sparc: Build sparc headers (Natalya Naumova)   
- RDS: change spin_lock to spin_lock_bh (Wengang Wang)  [Orabug: 21795851]  
- rds: add busy_list only when fmr allocated successfully (Wengang Wang)  [Orabug: 21795840]  
- rds: free ib_device related resource (Wengang Wang)  [Orabug: 21795824]  
- rds: srq initialization and cleanup (Wengang Wang)  [Orabug: 21795815]  
- uek-rpm: configs: Adjust config for new rpcrdma.ko module (Chuck Lever)   
- xen/fpu: stts() before the local_irq_enable(), and clts() after the local_irq_disable(). (Konrad Rzeszutek Wilk)  [Orabug: 20318090]  
- Revert "x86, fpu: Avoid possible error in math_state_restore()" (Konrad Rzeszutek Wilk)   
- uek-rpm: builds: sparc64: enable dtrace support (Allen Pais)   
- sparc64: vdso: simplify cpu_relax (Dave Kleikamp)  [Orabug: 20861959]  
- vdso: replace current_thread_info when building vDSO rather than diking it out (Nick Alcock)  [Orabug: 20861959]  
- sparc64, vdso: Add gettimeofday() and clock_gettime(). (Nick Alcock)  [Orabug: 20861959]  
- sparc64, vdso: sparc64 vDSO implementation. (Nick Alcock)  [Orabug: 20861959]  
- xprtrdma: Add class for RDMA backwards direction transport (Chuck Lever)   
- svcrdma: Add infrastructure to receive backwards direction RPC/RDMA replies (Chuck Lever)   
- svcrdma: Add infrastructure to send backwards direction RPC/RDMA calls (Chuck Lever)   
- svcrdma: Add svc_rdma_get_context() API that is allowed to fail (Chuck Lever)   
- svcrdma: Define maximum number of backchannel requests (Chuck Lever)   
- NFS: Enable client side NFSv4.1 backchannel to use other transports (Chuck Lever)   
- svcrdma: Add backward direction service for RPC/RDMA transport (Chuck Lever)   
- xprtrdma: Handle incoming backward direction RPC calls (Chuck Lever)   
- xprtrdma: Add support for sending backward direction RPC replies (Chuck Lever)   
- xprtrdma: Pre-allocate Work Requests for backchannel (Chuck Lever)   
- xprtrdma: Pre-allocate backward rpc_rqst and send/receive buffers (Chuck Lever)   
- SUNRPC: Abstract backchannel operations (Chuck Lever)   
- SUNRPC: xprt_complete_bc_request must also decrement the free slot count (Trond Myklebust)   
- SUNRPC: Fix a backchannel deadlock (Trond Myklebust)   
- SUNRPC: Fix a backchannel race (Trond Myklebust)   
- SUNRPC: Clean up allocation and freeing of back channel requests (Trond Myklebust)   
- xprtrdma: Replace send and receive arrays (Chuck Lever)   
- xprtrdma: Refactor reply handler error handling (Chuck Lever)   
- xprtrdma: Wait before destroying transport's queue pair (Chuck Lever)   
- xprtrdma: Remove completion polling budgets (Chuck Lever)   
- xprtrdma: Enable swap-on-NFS/RDMA (Chuck Lever)   
- xprtrdma: take HCA driver refcount at client (Devesh Sharma)   
- xprtrdma: Count RDMA_NOMSG type calls (Chuck Lever)   
- xprtrdma: Clean up xprt_rdma_print_stats() (Chuck Lever)   
- xprtrdma: Fix large NFS SYMLINK calls (Chuck Lever)   
- xprtrdma: Fix XDR tail buffer marshalling (Chuck Lever)   
- xprtrdma: Don't provide a reply chunk when expecting a short reply (Chuck Lever)   
- xprtrdma: Always provide a write list when sending NFS READ (Chuck Lever)   
- xprtrdma: Account for RPC/RDMA header size when deciding to inline (Chuck Lever)   
- xprtrdma: Remove logic that constructs RDMA_MSGP type calls (Chuck Lever)   
- xprtrdma: Clean up rpcrdma_ia_open() (Chuck Lever)   
- xprtrdma: Remove last ib_reg_phys_mr() call site (Chuck Lever)   
- xprtrdma: Don't fall back to PHYSICAL memory registration (Chuck Lever)   
- xprtrdma: Increase default credit limit (Chuck Lever)   
- xprtrdma: Raise maximum payload size to one megabyte (Chuck Lever)   
- xprtrdma: Make xprt_setup_rdma() agnostic to family of server address (Chuck Lever)   
- svcrdma: Change maximum server payload back to RPCSVC_MAXPAYLOAD (Chuck Lever)   
- svcrdma: Remove svc_rdma_fastreg() (Chuck Lever)   
- svcrdma: Clean up svc_rdma_get_reply_array() (Chuck Lever)   
- svcrdma: Fix send_reply() scatter/gather set-up (Chuck Lever)   
- NFS/RDMA Release resources in svcrdma when device is removed (Shirley Ma)   
- xprtrdma: Reduce per-transport MR allocation (Chuck Lever)   
- xprtrdma: Stack relief in fmr_op_map() (Chuck Lever)   
- xprtrdma: Split rb_lock (Chuck Lever)   
- xprtrdma: Remove rpcrdma_ia::ri_memreg_strategy (Chuck Lever)   
- xprtrdma: Remove ->ro_reset (Chuck Lever)   
- xprtrdma: Remove unused LOCAL_INV recovery logic (Chuck Lever)   
- xprtrdma: Acquire MRs in rpcrdma_register_external() (Chuck Lever)   
- xprtrdma: Introduce an FRMR recovery workqueue (Chuck Lever)   
- xprtrdma: Acquire FMRs in rpcrdma_fmr_register_external() (Chuck Lever)   
- xprtrdma: Introduce helpers for allocating MWs (Chuck Lever)   
- xprtrdma: Use ib_device pointer safely (Chuck Lever)   
- xprtrdma: Remove rr_func (Chuck Lever)   
- xprtrdma: Replace rpcrdma_rep::rr_buffer with rr_rxprt (Chuck Lever)   
- xprtrdma: Warn when there are orphaned IB objects (Chuck Lever)   
- SUNRPC: Address kbuild warning in net/sunrpc/debugfs.c (Chuck Lever)   
- SUNRPC: Transport fault injection (Chuck Lever)   
- sunrpc: turn swapper_enable/disable functions into rpc_xprt_ops (Jeff Layton)   
- sunrpc: lock xprt before trying to set memalloc on the sockets (Jeff Layton)   
- sunrpc: if we're closing down a socket, clear memalloc on it first (Jeff Layton)   
- sunrpc: make xprt->swapper an atomic_t (Jeff Layton)   
- sunrpc: keep a count of swapfiles associated with the rpc_clnt (Jeff Layton)   
- rpcrdma: Merge svcrdma and xprtrdma modules into one (Chuck Lever)   
- svcrdma: Add a separate "max data segs macro for svcrdma (Chuck Lever)   
- svcrdma: Replace GFP_KERNEL in a loop with GFP_NOFAIL (Chuck Lever)   
- svcrdma: Keep rpcrdma_msg fields in network byte-order (Chuck Lever)   
- svcrdma: Fix byte-swapping in svc_rdma_sendto.c (Chuck Lever)   
- svcrdma: Remove svc_rdma_xdr_decode_deferred_req() (Chuck Lever)   
- SUNRPC: Move EXPORT_SYMBOL for svc_process (Chuck Lever)   
- SUNRPC: Clean up bc_send() (Chuck Lever)   
- SUNRPC: Backchannel handle socket nospace (Trond Myklebust)   

* Fri Sep 11 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.6-13.el7uek] 
- ib_core: Usermode FMR config params (Dotan Barak)  [Orabug: 21517998]  
- ib_core: User mode FMR fixes 2012-06-11 (Dotan Barak)  [Orabug: 21517998]  
- ib/srp: Enable usermode FMR (Dotan Barak)  [Orabug: 21517998]  
- ib/iser: Enable usermode FMR (Dotan Barak)  [Orabug: 21517998]  
- ib/mlx4: Enable usermode FMR (Dotan Barak)  [Orabug: 21517998]  
- ib/core: Enable usermode FMR (Dotan Barak)   
- ib/core: init shared-pd ref count to 1, and add cleanup (Arun Kaimalettu)  [Orabug: 21496696]  
- IB/Shared PD support from Oracle (Eli Cohen)  [Orabug: 21496696]  
- sparc64: enable firmware build in kernel spec (Allen Pais)   
- sparc64: enable usb xhci/ehci pci configs (Allen Pais)   
- sparc64: enable a few configs required for proxyt (Allen Pais)   
- sparc64:perf: fix perf build crash (Allen Pais)   
- sparc64: enable dtrace support for sparc64 in the spec file (Allen Pais)   
- sparc64: kernel-uek.spec update to support sparc. (Allen Pais)   
- sparc64: uek4 debug config for sparc64 (Allen Pais)   
- sparc64: uek4 config for sparc64 (Allen Pais)   
- lib/iommu-common.c: do not use 0xffffffffffffffffl for computing align_mask (Sowmini Varadhan)   
- sparc64: use ENTRY/ENDPROC in VISsave (Sam Ravnborg)   
- SPARC64: PORT LDOMS TO UEK4 (Aaron Young)  [Orabug: 21644721]  
- Fix incorrect ASI_ST_BLKINIT_MRU_S value (Rob Gardner)   
- uek-rpm: config: add turbostat into kernel pakackage for OL6 and OL7 (Ethan Zhao)  [Orabug: 21613769]  
- uek-rom: config: Unset CONFIG_NFS_USE_LEGACY_DNS for OL7 (Todd Vierling)  [Orabug: 21483381]  
- NVMe: Setup max hardware sector count to 512KB (Santosh Shilimkar)  [Orabug: 21818316]  
- sparc64: perf: Use UREG_FP rather than UREG_I6 (David Ahern)   
- sparc64: perf: Add sanity checking on addresses in user stack (David Ahern)   
- sparc64: Convert BUG_ON to warning (David Ahern)   
- sparc: perf: Disable pagefaults while walking userspace stacks (David Ahern)   
- sparc: time: Replace update_persistent_clock() with CONFIG_RTC_SYSTOHC (Xunlei Pang)   
- PCI: Set under_pref for mem64 resource of pcie device (Yinghai Lu)   
- sparc/PCI: Add mem64 resource parsing for root bus (Yinghai Lu)   
- PCI: Add pci_bus_addr_t (Yinghai Lu)   
- sparc64: Fix userspace FPU register corruptions. (David S. Miller)   
- sparc64: using 2048 as default for number of CPUS (cherry picked from commit 578ddb2512a5c908cd17ef8cbc43ff78dd399afd) (Allen Pais)   
- sparc64: iommu-common build error fix (cherry picked from commit accb4c6276793b991c6382bf57a58b40ea17eb11) (Allen Pais)   
- sparc64: fix Setup sysfs to mark LDOM sockets build error (cherry picked from commit 59be02427bfcac6c904ddd1374c35d63155b82d4) (Allen Pais)   
- sparc64: mmap fixed and shared (bob picco)  [Orabug: 20426304]  
- sparc64: restore TIF_FREEZE flag for sparc (Allen Pais)   
- sparc64: Setup sysfs to mark LDOM sockets, cores and threads correctly (chris hyser)   
- sparc: Revert generic IOMMU allocator. (David S. Miller)   
- sparc: report correct hw capabilities for athena (Allen Pais)  [Orabug: 18314966]  
- sparc64: Setup sysfs to mark LDOM sockets, cores and threads correctly. (Allen Pais)  [Orabug: 17423360]  
- sparc64: prevent solaris control domain warnings about Domain Service handles (Allen Pais)  [Orabug: 18038829]  
- sparc64: retry domain service registration MIME-Version: 1.0 Content-Type: text/plain; charset=UTF-8 Content-Transfer-Encoding: 8bit (Allen Pais)  [Orabug: 17375532]  
- sparc64: __init code no longer called during non __init (Allen Pais)   
- add OCFS2_LOCK_RECURSIVE arg_flags to ocfs2_cluster_lock() to prevent hang (Tariq Saeed)  [Orabug: 21793017]  
- intel_pstate: enable HWP per CPU (Kristen Carlson Accardi)  [Orabug: 21325983]  
- ocfs2: direct write will call ocfs2_rw_unlock() twice when doing aio+dio (Ryan Ding)  [Orabug: 21612107]  
- uek-rpm: configs: Enbale X86_SYSFB on OL7 too (Santosh Shilimkar)  [Orabug: 21802188]  
- ocfs2_iop_set/get_acl() are also called from the VFS so we must take inode lock (Tariq Saeed)  [Orabug: 20189959]  
- BUG_ON(lockres->l_level != DLM_LOCK_EX && !checkpointed) tripped in ocfs2_ci_checkpointed (Tariq Saeed)  [Orabug: 20189959]  
- kallsyms: unbreak kallmodsyms after CONFIG_KALLMODSYMS addition (Nick Alcock)  [Orabug: 21539840]  
- kallsyms: de-ifdef kallmodsyms (Nick Alcock)  [Orabug: 21539840]  
- dtrace: use syscall_get_nr() to obtain syscall number (Kris Van Hees)  [Orabug: 21630345]  

* Fri Sep 4 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.6-12.el7uek] 
- DCA: fix over-warning in ioat3_dca_init (Jet Chen)  [Orabug: 21666295]  
- IB/rds_rdma: unloading of ofed stack causes page fault panic (Rama Nichanamatlu)  [Orabug: 20861212]  
- RDS-TCP: Support multiple RDS-TCP listen endpoints, one per netns. (Sowmini Varadhan)  [Orabug: 21437445]  
- RDS-TCP: Make RDS-TCP work correctly when it is set up in a netns other than init_net (Sowmini Varadhan)  [Orabug: 21437445]  
- net: sk_clone_lock() should only do get_net() if the parent is not a kernel socket (Sowmini Varadhan)  [Orabug: 21437445]  
- net: Modify sk_alloc to not reference count the netns of kernel sockets. (Sowmini Varadhan)   
- net: Pass kern from net_proto_family.create to sk_alloc (Sowmini Varadhan)   
- net: Add a struct net parameter to sock_create_kern (Sowmini Varadhan)  [Orabug: 21437445]  

* Fri Aug 28 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.6-11.el7uek] 
- nfs: take extra reference to fl->fl_file when running a LOCKU operation (Jeff Layton)  [Orabug: 21687670]  
- NFS hangs in __ocfs2_cluster_lock due to race with ocfs2_unblock_lock (Tariq Saeed)  [Orabug: 20933419]  
- i40e/i40evf: Bump version to 1.3.6 for i40e and 1.3.2 for i40evf (Catherine Sullivan)  [Orabug: 21570582]  
- i40e: Refine an error message to avoid confusion (Anjali Singhai Jain)  [Orabug: 21570582]  
- i40e/i40evf: Add support for pre-allocated pages for PD (Faisal Latif)  [Orabug: 21570582]  
- i40evf: add MAC address filter in open, not init (Mitch Williams)  [Orabug: 21570582]  
- i40evf: don't delete all the filters (Mitch Williams)  [Orabug: 21570582]  
- i40e: un-disable VF after reset (Mitch Williams)  [Orabug: 21570582]  
- i40e: do a proper reset when disabling a VF (Mitch Williams)  [Orabug: 21570582]  
- i40e: correctly program filters for VFs (Mitch Williams)  [Orabug: 21570582]  
- i40e/i40evf: Update the admin queue command header (Greg Rose)  [Orabug: 21570582]  
- i40e: Remove incorrect #ifdef's (Carolyn Wyborny)  [Orabug: 21570582]  
- i40e: ignore duplicate port VLAN requests (Mitch Williams)  [Orabug: 21570582]  
- i40evf: Allow for an abundance of vectors (Mitch Williams)  [Orabug: 21570582]  
- i40e/i40evf: improve Tx performance with a small tweak (Jesse Brandeburg)  [Orabug: 21570582]  
- i40e/i40evf: Update Flex-10 related device/function capabilities (Pawel Orlowski)  [Orabug: 21570582]  
- i40e/i40evf: Add stats to track FD ATR and SB dynamic enable state (Anjali Singhai Jain)  [Orabug: 21570582]  
- i40e: Implement ndo_features_check() (Joe Stringer)  [Orabug: 21570582]  
- i40evf: don't configure unused RSS queues (Mitch Williams)  [Orabug: 21570582]  
- i40evf: fix panic during MTU change (Mitch Williams)  [Orabug: 21570582]  
- i40e: Bump version to 1.3.4 (Catherine Sullivan)  [Orabug: 21570582]  
- i40e/i40evf: remove time_stamp member (Jesse Brandeburg)  [Orabug: 21570582]  
- i40e/i40evf: force inline transmit functions (Jesse Brandeburg)  [Orabug: 21570582]  
- i40evf: skb->xmit_more support (Jesse Brandeburg)  [Orabug: 21570582]  
- i40e: Move the FD ATR/SB messages to a higher debug level (Anjali Singhai Jain)  [Orabug: 21570582]  
- i40e: fix unrecognized FCOE EOF case (Vasu Dev)  [Orabug: 21570582]  
- i40e/i40evf: Remove unneeded TODO (Greg Rose)  [Orabug: 21570582]  
- i40e: Remove unnecessary pf members (Anjali Singhai Jain)  [Orabug: 21570582]  
- i40e/i40evf: Add stats to count Tunnel ATR hits (Anjali Singhai Jain)  [Orabug: 21570582]  
- i40e/i40evf: Add ATR support for tunneled TCP/IPv4/IPv6 packets. (Anjali Singhai Jain)  [Orabug: 21570582]  
- i40e: Disable offline diagnostics if VFs are enabled (Greg Rose)  [Orabug: 21570582]  
- i40e: Collect PFC XOFF RX stats even in single TC case (Neerav Parikh)  [Orabug: 21570582]  
- uek-rpm: configs: Enable Chelsio T4 and T5 NIC on OL6 (Santosh Shilimkar)  [Orabug: 21754829]  
- mm: madvise allow remove operation for hugetlbfs (Mike Kravetz)  [Orabug: 21652814]  
- mmotm: build fix hugetlbfs fallocate if not CONFIG_NUMA (Mike Kravetz)  [Orabug: 21652814]  
- hugetlbfs: add hugetlbfs_fallocate() (Mike Kravetz)  [Orabug: 21652814]  
- hugetlbfs: New huge_add_to_page_cache helper routine (Mike Kravetz)  [Orabug: 21652814]  
- mm/hugetlb: alloc_huge_page handle areas hole punched by fallocate (Mike Kravetz)  [Orabug: 21652814]  
- mm/hugetlb: vma_has_reserves() needs to handle fallocate hole punch (Mike Kravetz)  [Orabug: 21652814]  
- mm/hugetlb.c: make vma_has_reserves() return bool (Nicholas Krause)  [Orabug: 21652814]  
- hugetlbfs: truncate_hugepages() takes a range of pages (Mike Kravetz)  [Orabug: 21652814]  
- hugetlbfs: hugetlb_vmtruncate_list() needs to take a range to delete (Mike Kravetz)  [Orabug: 21652814]  
- mm/hugetlb: expose hugetlb fault mutex for use by fallocate (Mike Kravetz)  [Orabug: 21652814]  
- mm/hugetlb: add region_del() to delete a specific range of entries (Mike Kravetz)  [Orabug: 21652814]  
- mm-hugetlb-add-cache-of-descriptors-to-resv_map-for-region_add-fix (Andrew Morton)  [Orabug: 21652814]  
- mm/hugetlb: add cache of descriptors to resv_map for region_add (Mike Kravetz)  [Orabug: 21652814]  
- mm/hugetlb: handle races in alloc_huge_page and hugetlb_reserve_pages (Mike Kravetz)  [Orabug: 21652814]  
- mm/hugetlb: compute/return the number of regions added by region_add() (Mike Kravetz)  [Orabug: 21652814]  
- mm/hugetlb: document the reserve map/region tracking routines (Mike Kravetz)  [Orabug: 21652814]  
- ixgbe: TRIVIAL fix up double 'the' and comment style (Jacob Keller)  [Orabug: 21669416]  
- ixgbe: Simplify port-specific macros (Mark Rustad)  [Orabug: 21669416]  
- ixgbevf: add support for reporting RSS key and hash table for X550 (Emil Tantilov)  [Orabug: 21669416]  
- ixgbe: Don't report flow director filter's status (Fan Du)  [Orabug: 21669416]  
- ixgbevf: Set Rx hash type for ingress packets (Fan Du)  [Orabug: 21669416]  
- ixgbe: Specify Rx hash type WRT Rx desc RSS type (Fan Du)  [Orabug: 21669416]  
- ixgbevf: fold ixgbevf_pull_tail into ixgbevf_add_rx_frag (Alexander Duyck)  [Orabug: 21669416]  
- ixgbe: only report generic filters in get_ts_info (Jacob Keller)  [Orabug: 21669416]  
- ixgbe: Remember to write ixfi changes after modifying (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: fix X550 default set_phy_power method (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: Set lan_id before using I2C (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: add link check for X550 copper (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: Add support for another X550 device. (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: fix X550 PHY function pointers (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: fix X550 devices init flow (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: fix bug in not clearing counters for X550 devices (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: fix issue with sfp events with new X550 devices (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: add support for interrupts from X550 external PHY (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: Add const string for overheat message (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: Add reset for X550 device (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: add X550 support for external PHY and forced 1G/10G support (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: Restore ESDP settings after MAC reset (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: Add a PHY power state method (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: add define for X557 PHY ID (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: add support for WoL and autoneg FC for some X550 devices (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: add array of MAC type dependent values (Don Skidmore)  [Orabug: 21669416]  
- ixgbe: Allow flow director to use entire queue space (John Fastabend)  [Orabug: 21669416]  
- ethtool: Add helper routines to pass vf to rx_flow_spec (John Fastabend)  [Orabug: 21669416]  
- ixgbe: Use a signed type to hold error codes (Mark Rustad)  [Orabug: 21669416]  
- ixgbe: Release semaphore bits in the right order (Mark Rustad)  [Orabug: 21669416]  
- ixgbe: Fix IOSF SB access issues (Mark Rustad)  [Orabug: 21669416]  

* Wed Aug 26 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.6-10.el7uek] 
- rds: print vendor error on error induced disconnect/re-connect (Wengang Wang)  [Orabug: 21527137]  
- rds: re-entry of rds_ib_xmit/rds_iw_xmit (Wengang Wang)  [Orabug: 21324078]  
- selinux: enable setting security context in cgroup (Alexey Kodanev)  [Orabug: 21295765]  
- net/mlx4_vnic: Initialize new fields of mlx4_ib_qp (Yuval Shaia)  [Orabug: 21530835]  
- uek-rpm: configs: sync up config with v4.1.6 stable tag (Santosh Shilimkar)   
- uek-rpm: build: Update the base release to 6 with stable v4.1.6 (Santosh Shilimkar)   
- uek-rpm: configs: enable SNIC driver in kernel configs (Brian Maly)  [Orabug: 21674432]  
- snic: driver for Cisco SCSI HBA (Narsimhulu Musini)  [Orabug: 21674432]  
- CVE-2015-666: Revert "sched/x86_64: Don't save flags on context switch" (Santosh Shilimkar)  [Orabug: 21689349]  {CVE-2015-666} 
- Linux 4.1.6 (Greg Kroah-Hartman)   
- nfsd: do nfs4_check_fh in nfs4_check_file instead of nfs4_check_olstateid (Jeff Layton)   
- nfsd: refactor nfs4_preprocess_stateid_op (Christoph Hellwig)   
- kvm: x86: fix kvm_apic_has_events to check for NULL pointer (Paolo Bonzini)   
- signal: fix information leak in copy_siginfo_from_user32 (Amanieu d'Antras)   
- signal: fix information leak in copy_siginfo_to_user (Amanieu d'Antras)   
- signalfd: fix information leak in signalfd_copyinfo (Amanieu d'Antras)   
- mm, vmscan: Do not wait for page writeback for GFP_NOFS allocations (Michal Hocko)   
- thermal: exynos: Disable the regulator on probe failure (Krzysztof Kozlowski)   
- Input: alps - only Dell laptops have separate button bits for v2 dualpoint sticks (Hans de Goede)   
- mtd: nand: Fix NAND_USE_BOUNCE_BUFFER flag conflict (Scott Wood)   
- USB: qcserial: Add support for Dell Wireless 5809e 4G Modem (Pieter Hollants)   
- USB: qcserial/option: make AT URCs work for Sierra Wireless MC7305/MC7355 (Reinhard Speyerer)   
- usb: gadget: f_uac2: fix calculation of uac2->p_interval (Peter Chen)   
- staging: lustre: Include unaligned.h instead of access_ok.h (Guenter Roeck)   
- staging: vt6655: vnt_bss_info_changed check conf->beacon_rate is not NULL (Malcolm Priestley)   
- dm: fix dm_merge_bvec regression on 32 bit systems (Mike Snitzer)   
- md/raid1: extend spinlock to protect raid1_end_read_request against inconsistencies (NeilBrown)   
- PCI: Restore PCI_MSIX_FLAGS_BIRMASK definition (Michael S. Tsirkin)   
- nfsd: Drop BUG_ON and ignore SECLABEL on absent filesystem (Kinglong Mee)   
- ocfs2: fix shift left overflow (Joseph Qi)   
- ocfs2: fix BUG in ocfs2_downconvert_thread_do_work() (Joseph Qi)   
- ipc: modify message queue accounting to not take kernel data structures into account (Marcus Gelderie)   
- hwmon: (dell-smm) Blacklist Dell Studio XPS 8100 (Pali Rohár)   
- hwmon: (nct7904) Export I2C module alias information (Javier Martinez Canillas)   
- ALSA: fireworks/firewire-lib: add support for recent firmware quirk (Takashi Sakamoto)   
- ALSA: hda - one Dell machine needs the headphone white noise fixup (Hui Wang)   
- ALSA: hda - fix cs4210_spdif_automute() (Dan Carpenter)   
- ARM: OMAP2+: hwmod: Fix _wait_target_ready() for hwmods without sysc (Roger Quadros)   
- ARM: dts: i.MX35: Fix can support. (Denis Carikli)   
- rbd: fix copyup completion race (Ilya Dryomov)   
- crypto: ixp4xx - Remove bogus BUG_ON on scattered dst buffer (Herbert Xu)   
- crypto: qat - Fix invalid synchronization between register/unregister sym algs (Tadeusz Struk)   
- hwrng: core - correct error check of kthread_run call (Martin Schwidefsky)   
- xen/gntdevt: Fix race condition in gntdev_release() (Marek Marczykowski-Górecki)   
- x86/xen: Probe target addresses in set_aliased_prot() before the hypercall (Andy Lutomirski)   
- ASoC: dapm: Don't add prefix to widget stream name (Lars-Peter Clausen)   
- ASoC: dapm: Lock during userspace access (Lars-Peter Clausen)   
- ASoC: pcm1681: Fix setting de-emphasis sampling rate selection (Axel Lin)   
- ASoC: ssm4567: Keep TDM_BCLKS in ssm4567_set_dai_fmt (Ben Zhang)   
- ASoC: Intel: Get correct usage_count value to load firmware (Shilpa Sreeramalu)   
- ARM: dts: keystone: fix dt bindings to use post div register for mainpll (Murali Karicheri)   
- clk: keystone: add support for post divider register for main pll (Murali Karicheri)   
- sparc64: Fix userspace FPU register corruptions. (David S. Miller)   
- crypto: nx - Fix reentrancy bugs (Herbert Xu)   
- crypto: nx - Fixing SHA update bug (Leonidas Da Silva Barbosa)   
- crypto: nx - Fixing NX data alignment with nx_sg list (Leonidas Da Silva Barbosa)   
- dmaengine: at_xdmac: fix transfer data width in at_xdmac_prep_slave_sg() (Cyrille Pitchen)   
- x86/nmi/64: Use DF to avoid userspace RSP confusing nested NMI detection (Andy Lutomirski)   
- x86/nmi/64: Reorder nested NMI checks (Andy Lutomirski)   
- x86/nmi/64: Improve nested NMI comments (Andy Lutomirski)   
- x86/nmi/64: Switch stacks on userspace NMI entry (Andy Lutomirski)   
- x86/nmi/64: Remove asm code that saves CR2 (Andy Lutomirski)   
- x86/nmi: Enable nested do_nmi() handling for 64-bit kernels (Andy Lutomirski)   
- x86/asm/entry/64: Remove pointless jump to irq_return (Andy Lutomirski)   
- ath10k: fix qca61x4 hw2.1 support (Michal Kazior)   
- md: use kzalloc() when bitmap is disabled (Benjamin Randazzo)   
- phy: twl4030-usb: make runtime pm more reliable. (NeilBrown)   
- usb: chipidea: ehci_init_driver is intended to call one time (Peter Chen)   
- usb: udc: core: add device_del() call to error pathway (Alan Stern)   
- USB: sierra: add 1199:68AB device ID (Dirk Behme)   
- drivers/usb: Delete XHCI command timer if necessary (Gavin Shan)   
- xhci: fix off by one error in TRB DMA address boundary check (Mathias Nyman)   
- dmaengine: pl330: Really fix choppy sound because of wrong residue calculation (Krzysztof Kozlowski)   
- dmaengine: pl330: Fix overflow when reporting residue in memcpy (Krzysztof Kozlowski)   
- Bluetooth: Fix NULL pointer dereference in smp_conn_security (Johan Hedberg)   
- ipr: Fix invalid array indexing for HRRQ (Brian King)   
- ipr: Fix incorrect trace indexing (Brian King)   
- ipr: Fix locking for unit attention handling (Brian King)   
- drm/dp-mst: Remove debug WARN_ON (Daniel Vetter)   
- drm/radeon/combios: add some validation of lvds values (Alex Deucher)   
- drm/radeon: rework audio detect (v4) (Alex Deucher)   
- drm/i915: Replace WARN inside I915_READ64_2x32 with retry loop (Chris Wilson)   
- drm/i915: Declare the swizzling unknown for L-shaped configurations (Chris Wilson)   
- fsnotify: fix oops in fsnotify_clear_marks_by_group_flags() (Jan Kara)   
- MIPS: Make set_pte() SMP safe. (David Daney)   
- MIPS: Flush RPS on kernel entry with EVA (James Hogan)   
- Revert "MIPS: BCM63xx: Provide a plat_post_dma_flush hook" (Florian Fainelli)   
- MIPS: show_stack: Fix stack trace with EVA (James Hogan)   
- MIPS: do_mcheck: Fix kernel code dump with EVA (James Hogan)   
- MIPS: Export get_c0_perfcount_int() (Felix Fietkau)   
- MIPS: Fix sched_getaffinity with MT FPAFF enabled (Felix Fietkau)   
- MIPS: Malta: Don't reinitialise RTC (James Hogan)   
- MIPS: Replace add and sub instructions in relocate_kernel.S with addiu (James Cowgill)   
- MIPS: unaligned: Fix build error on big endian R6 kernels (James Cowgill)   

* Wed Aug 19 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.5-9.el7uek] 
- modsign: Add key for moodule signing (Alexey Petrenko)  [Orabug: 21659739]  
- uek-rpm: extrakeys.pub is not needed for the build (Alexey Petrenko)  [Orabug: 21249387]  
- uek-rpm: build: Fix the new-kernel-pkg path for ol7 (Santosh Shilimkar)   

* Mon Aug 17 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.5-8.el7uek] 
- dtrace: only call dtrace functions when CONFIG_DTRACE is set (Kris Van Hees)  [Orabug: 21647525]  
- uek-rpm: config: sync up the configs with 4.1.5 stable (Santosh Shilimkar)   
- uek-rpm: config: Enable OVM API (Zhigang Wang)  [Orabug: 20426111]  
- uek-rpm: config: enable some DRM options (Zhigang Wang)  [Orabug: 21615719]  
- OVMAPI: port ovmapi.ko to UEK4 from UEK3 (Zhigang Wang)  [Orabug: 20426111]  
- dtrace: ensure SDT module probes work with NORX (Kris Van Hees)  [Orabug: 21630297]  
- dtrace: prevent the stack protector from breaking syscall tracing. (Nick Alcock)  [Orabug: 21630345]  
- kallsyms: make it possible to disable /proc/kallmodsyms (Nick Alcock)  [Orabug: 21539840]  

* Thu Aug 13 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.5-7.el7uek] 
- intel_pstate: append more Oracle OEM table id to vendor bypass list (Ethan Zhao)  [Orabug: 21447179]  
- mlx4_vnic: Skip fip discover restart if pkey index not changed (Yuval Shaia)  [Orabug: 21446728]  
- rds: rds_ib_device.refcount overflow (Wengang Wang)  [Orabug: 21534438]  
- rds_rdma: rds_sendmsg should return EAGAIN if connection not setup (Wengang Wang)  [Orabug: 21551474]  
- rds_rdma: allocate FMR according to max_item_soft (Wengang Wang)  [Orabug: 21551548]  
- rds_rdma: do not dealloc fmrs in the pool under use (Wengang Wang)  [Orabug: 21551548]  
- rds: set fmr pool dirty_count correctly (Wengang Wang)  [Orabug: 21551548]  
- xen-netfront: Remove the meaningless code (Li, Liang Z)   
- net/xen-netfront: Correct printf format in xennet_get_responses (Julien Grall)   
- xen-netfront: Use setup_timer (Vaishali Thakkar)   
- xen/xenbus: Don't leak memory when unmapping the ring on HVM backend (Julien Grall)   
- Revert "xen/events/fifo: Handle linked events when closing a port" (David Vrabel)   
- x86/xen: build "Xen PV" APIC driver for domU as well (Jason A. Donenfeld)   
- xen/events/fifo: Handle linked events when closing a port (Ross Lagerwall)   
- xen: release lock occasionally during ballooning (Juergen Gross)   
- xen/gntdevt: Fix race condition in gntdev_release() (Marek Marczykowski-Górecki)   
- block/xen-blkback: s/nr_pages/nr_segs/ (Julien Grall)   
- block/xen-blkfront: Remove invalid comment (Julien Grall)   
- arm/xen: Drop duplicate define mfn_to_virt (Julien Grall)   
- xen/grant-table: Remove unused macro SPP (Julien Grall)   
- xen/xenbus: client: Fix call of virt_to_mfn in xenbus_grant_ring (Julien Grall)   
- xen: Include xen/page.h rather than asm/xen/page.h (Julien Grall)   
- kconfig: add xenconfig defconfig helper (Luis R. Rodriguez)   
- kconfig: clarify kvmconfig is for kvm (Luis R. Rodriguez)   
- xen/pcifront: Remove usage of struct timeval (Tina Ruchandani)   
- xen/tmem: use BUILD_BUG_ON() in favor of BUG_ON() (Jan Beulich)   
- hvc_xen: avoid uninitialized variable warning (Jan Beulich)   
- xenbus: avoid uninitialized variable warning (Jan Beulich)   
- xen/arm: allow console=hvc0 to be omitted for guests (Ard Biesheuvel)   
- arm,arm64/xen: move Xen initialization earlier (Stefano Stabellini)   
- arm/xen: Correctly check if the event channel interrupt is present (Julien Grall)   
- xen-blkback: replace work_pending with work_busy in purge_persistent_gnt() (Bob Liu)   
- xen-blkfront: don't add indirect pages to list when !feature_persistent (Bob Liu)   
- xen-blkfront: introduce blkfront_gather_backend_features() (Bob Liu)   
- drivers: xen-blkfront: only talk_to_blkback() when in XenbusStateInitialising (Bob Liu)   
- xen/block: add multi-page ring support (Bob Liu)   
- driver: xen-blkfront: move talk_to_blkback to a more suitable place (Bob Liu)   
- drivers: xen-blkback: delay pending_req allocation to connect_ring (Bob Liu)   

* Wed Aug 12 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.5-6.el7uek] 
- net/mlx4_core: need to call close fw if alloc icm is called twice (Carol Soto)  [Orabug: 21606315]  

* Tue Aug 11 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.5-5.el7uek] 
- uek-rpm: build: Update the base release to 5 with stable v4.1.45 (Santosh Shilimkar)   
- Linux 4.1.5 (Greg Kroah-Hartman)   
- perf symbols: Store if there is a filter in place (Arnaldo Carvalho de Melo)   
- xfs: remote attributes need to be considered data (Dave Chinner)   
- xfs: remote attribute headers contain an invalid LSN (Dave Chinner)   
- drm/nouveau/drm/nv04-nv40/instmem: protect access to priv->heap by mutex (Kamil Dudka)   
- drm/nouveau: hold mutex when calling nouveau_abi16_fini() (Kamil Dudka)   
- drm/nouveau/kms/nv50-: guard against enabling cursor on disabled heads (Ben Skeggs)   
- drm/nouveau/fbcon/nv11-: correctly account for ring space usage (Ilia Mirkin)   
- qla2xxx: kill sessions/log out initiator on RSCN and port down events (Roland Dreier)   
- qla2xxx: fix command initialization in target mode. (Kanoj Sarcar)   
- qla2xxx: Remove msleep in qlt_send_term_exchange (Himanshu Madhani)   
- qla2xxx: release request queue reservation. (Quinn Tran)   
- qla2xxx: Fix hardware lock/unlock issue causing kernel panic. (Saurav Kashyap)   
- intel_pstate: Add get_scaling cpu_defaults param to Knights Landing (Lukasz Anaczkowski)   
- iscsi-target: Fix iser explicit logout TX kthread leak (Nicholas Bellinger)   
- iscsi-target: Fix iscsit_start_kthreads failure OOPs (Nicholas Bellinger)   
- iscsi-target: Fix use-after-free during TPG session shutdown (Nicholas Bellinger)   
- IB/ipoib: Fix CONFIG_INFINIBAND_IPOIB_CM (Jason Gunthorpe)   
- NFS: Fix a memory leak in nfs_do_recoalesce (Trond Myklebust)   
- NFSv4: We must set NFS_OPEN_STATE flag in nfs_resync_open_stateid_locked (Trond Myklebust)   
- avr32: handle NULL as a valid clock object (Andy Shevchenko)   
- NFS: Don't revalidate the mapping if both size and change attr are up to date (Trond Myklebust)   
- hwmon: (nct7904) Rename pwm attributes to match hwmon ABI (Guenter Roeck)   
- hwmon: (nct7802) Fix integer overflow seen when writing voltage limits (Guenter Roeck)   
- vhost: actually track log eventfd file (Marc-André Lureau)   
- perf/x86/intel/cqm: Return cached counter value from IRQ context (Matt Fleming)   
- perf hists browser: Take the --comm, --dsos, etc filters into account (Arnaldo Carvalho de Melo)   
- blk-mq: set default timeout as 30 seconds (Ming Lei)   
- n_tty: signal and flush atomically (Peter Hurley)   
- rds: rds_ib_device.refcount overflow (Wengang Wang)   
- ARC: Make ARC bitops "safer" (add anti-optimization) (Vineet Gupta)   
- ARC: Reduce bitops lines of code using macros (Vineet Gupta)   
- x86/efi: Use all 64 bit of efi_memmap in setup_e820() (Dmitry Skorodumov)   
- efi: Check for NULL efi kernel parameters (Ricardo Neri)   
- arm64/efi: map the entire UEFI vendor string before reading it (Ard Biesheuvel)   
- efi: Handle memory error structures produced based on old versions of standard (Tony Luck)   
- x86/mm: Add parenthesis for TLB tracepoint size calculation (Dave Hansen)   
- mei: prevent unloading mei hw modules while the device is opened. (Tomas Winkler)   
- xhci: do not report PLC when link is in internal resume state (Zhuang Jin Can)   
- xhci: prevent bus_suspend if SS port resuming in phase 1 (Zhuang Jin Can)   
- xhci: report U3 when link is in resume state (Zhuang Jin Can)   
- xhci: Calculate old endpoints correctly on device reset (Brian Campbell)   
- serial: core: Fix crashes while echoing when closing (Peter Hurley)   
- Revert "serial: imx: initialized DMA w/o HW flow enabled" (David Jander)   
- usb-storage: ignore ZTE MF 823 card reader in mode 0x1225 (Oliver Neukum)   
- ata: pmp: add quirk for Marvell 4140 SATA PMP (Lior Amsalem)   
- regulator: s2mps11: Fix GPIO suspend enable shift wrapping bug (Krzysztof Kozlowski)   
- blkcg: fix gendisk reference leak in blkg_conf_prep() (Tejun Heo)   
- Input: usbtouchscreen - avoid unresponsive TSC-30 touch screen (Bernhard Bender)   
- tile: use free_bootmem_late() for initrd (Chris Metcalf)   
- spi: imx: Fix small DMA transfers (Sascha Hauer)   
- spi: img-spfi: fix support for speeds up to 1/4th input clock (Sifan Naeem)   
- md/raid1: fix test for 'was read error from last working device'. (NeilBrown)   
- iwlwifi: pcie: prepare the device before accessing it (Emmanuel Grumbach)   
- iwlwifi: nvm: remove mac address byte swapping in 8000 family (Liad Kaufman)   
- iwlwifi: mvm: fix antenna selection when BT is active (Emmanuel Grumbach)   
- HID: cp2112: fix to force single data-report reply (Antonio Borneo)   
- mmc: sdhci-pxav3: fix platform_data is not initialized (Jingju Hou)   
- mmc: sdhci-esdhc: Make 8BIT bus work (Joakim Tjernlund)   
- mmc: sdhci check parameters before call dma_free_coherent (Peng Fan)   
- mmc: omap_hsmmc: Fix DTO and DCRC handling (Kishon Vijay Abraham I)   
- iommu/vt-d: Fix VM domain ID leak (Alex Williamson)   
- ftrace: Fix breakage of set_ftrace_pid (Steven Rostedt (Red Hat))   
- mnt: In detach_mounts detach the appropriate unmounted mount (Eric W. Biederman)   
- mnt: Clarify and correct the disconnect logic in umount_tree (Eric W. Biederman)   
- Subject: pinctrl: imx1-core: Fix debug output in .pin_config_set callback (Uwe Kleine-König)   
- mac80211: clear subdir_stations when removing debugfs (Tom Hughes)   
- drivers: clk: st: Incorrect register offset used for lock_status (Pankaj Dev)   
- drivers: clk: st: Fix mux bit-setting for Cortex A9 clocks (Gabriel Fernandez)   
- drivers: clk: st: Fix flexgen lock init (Giuseppe Cavallaro)   
- st: null pointer dereference panic caused by use after kref_put by st_open (Seymour, Shane M)   
- scsi: fix memory leak with scsi-mq (Tony Battersby)   
- scsi: fix host max depth checking for the 'queue_depth' sysfs interface (Jens Axboe)   
- irqchip/gicv3-its: Fix mapping of LPIs to collections (Marc Zyngier)   
- Revert "dm: only run the queue on completion if congested or no requests pending" (Mike Snitzer)   
- x86, perf: Fix static_key bug in load_mm_cr4() (Peter Zijlstra)   
- ALSA: hda - Fix MacBook Pro 5,2 quirk (Takashi Iwai)   
- ALSA: usb-audio: add dB range mapping for some devices (Yao-Wen Mao)   
- ALSA: hda - Apply a fixup to Dell Vostro 5480 (Takashi Iwai)   
- ALSA: hda - Apply fixup for another Toshiba Satellite S50D (Takashi Iwai)   
- ALSA: hda - Add headset mic pin quirk for a Dell device (David Henningsson)   
- ALSA: hda - Add new GPU codec ID 0x10de007d to snd-hda (Aaron Plattner)   
- ALSA: hda: add new AMD PCI IDs with proper driver caps (Maruthi Srinivas Bayyavarapu)   
- ALSA: hda - Add headset mic support for Acer Aspire V5-573G (Mateusz Sylwestrzak)   
- ALSA: pcm: Fix lockdep warning with nonatomic PCM ops (Takashi Iwai)   
- ALSA: line6: Fix -EBUSY error during active monitoring (Takashi Iwai)   
- ALSA: usb-audio: Add MIDI support for Steinberg MI2/MI4 (Dominic Sacré)   
- genirq: Prevent resend to interrupts marked IRQ_NESTED_THREAD (Thomas Gleixner)   
- dma-debug: skip debug_dma_assert_idle() when disabled (Haggai Eran)   
- bio integrity: do not assume bio_integrity_pool exists if bioset exists (Mike Snitzer)   
- kbuild: Allow arch Makefiles to override {cpp,ld,c}flags (Michal Marek)   
- ARC: make sure instruction_pointer() returns unsigned value (Alexey Brodkin)   
- ARC: Override toplevel default -O2 with -O3 (Vineet Gupta)   
- s390/cachinfo: add missing facility check to init_cache_level() (Heiko Carstens)   
- s390/bpf: clear correct BPF accumulator register (Michael Holzheu)   
- s390/nmi: fix vector register corruption (Heiko Carstens)   
- s390/sclp: clear upper register halves in _sclp_print_early (Martin Schwidefsky)   
- s390/process: fix sfpc inline assembly (Heiko Carstens)   
- crypto: omap-des - Fix unmapping of dma channels (Vutla, Lokesh)   
- x86/kasan: Fix boot crash on AMD processors (Andrey Ryabinin)   
- x86/kasan: Flush TLBs after switching CR3 (Andrey Ryabinin)   
- x86/kasan: Fix KASAN shadow region page tables (Alexander Popov)   
- x86/init: Clear 'init_level4_pgt' earlier (Andrey Ryabinin)   
- freeing unlinked file indefinitely delayed (Al Viro)   
- can: mcp251x: fix resume when device is down (Stefan Agner)   
- can: rcar_can: print signed IRQ # (Sergei Shtylyov)   
- can: c_can: Fix default pinmux glitch at init (J.D. Schroeder)   
- can: rcar_can: fix IRQ check (Sergei Shtylyov)   
- can: replace timestamp as unique skb attribute (Oliver Hartkopp)   
- MIPS: fpu.h: Allow 64-bit FPU on a 64-bit MIPS R6 CPU (Markos Chandras)   
- MIPS: Require O32 FP64 support for MIPS64 with O32 compat (Paul Burton)   
- MIPS: c-r4k: Fix cache flushing for MT cores (Markos Chandras)   
- MIPS: Fix erroneous JR emulation for MIPS R6 (Markos Chandras)   
- ARM: imx6: gpc: always enable PU domain if CONFIG_PM is not set (Lucas Stach)   
- ARM: 8404/1: dma-mapping: fix off-by-one error in bitmap size check (Marek Szyprowski)   
- ARM: dts: am57xx-beagle-x15: Provide supply for usb2_phy2 (Roger Quadros)   
- ARM: dts: dra7x-evm: Prevent glitch on DCAN1 pinmux (Roger Quadros)   
- ARM: pxa: fix dm9000 platform data regression (Robert Jarzmik)   
- parisc: mm: Fix a memory leak related to pmd not attached to the pgd (Christophe Jaillet)   
- parisc: Fix some PTE/TLB race conditions and optimize __flush_tlb_range based on timing results (John David Anglin)   
- Revert "Input: synaptics - allocate 3 slots to keep stability in image sensors" (Dmitry Torokhov)   
- powerpc/powernv: Fix race in updating core_idle_state (Shreyas B. Prabhu)   
- cxl: Check if afu is not null in cxl_slbia (Daniel Axtens)   
- cxl: Fix off by one error allowing subsequent mmap page to be accessed (Ian Munsie)   
- uek-rpm: onfig: enable some secure boot features (Guangyu Sun)  [Orabug: 21539498]  
- efi: Disable secure boot if shim is in insecure mode (Josh Boyer)  [Orabug: 21539498]  
- hibernate: Disable in a signed modules environment (Josh Boyer)  [Orabug: 21539498]  
- efi: Add EFI_SECURE_BOOT bit (Josh Boyer)  [Orabug: 21539498]  
- Add option to automatically set securelevel when in Secure Boot mode (Matthew Garrett)  [Orabug: 21539498]  
- asus-wmi: Restrict debugfs interface when securelevel is set (Matthew Garrett)  [Orabug: 21539498]  
- x86: Restrict MSR access when securelevel is set (Matthew Garrett)  [Orabug: 21539498]  
- uswsusp: Disable when securelevel is set (Matthew Garrett)  [Orabug: 21539498]  
- kexec: Disable at runtime if securelevel has been set. (Matthew Garrett)  [Orabug: 21539498]  
- acpi: Ignore acpi_rsdp kernel parameter when securelevel is set (Matthew Garrett)  [Orabug: 21539498]  
- acpi: Limit access to custom_method if securelevel is set (Matthew Garrett)  [Orabug: 21539498]  
- Restrict /dev/mem and /dev/kmem when securelevel is set. (Matthew Garrett)  [Orabug: 21539498]  
- x86: Lock down IO port access when securelevel is enabled (Matthew Garrett)  [Orabug: 21539498]  
- PCI: Lock down BAR access when securelevel is enabled (Matthew Garrett)  [Orabug: 21539498]  
- Enforce module signatures when securelevel is greater than 0 (Matthew Garrett)  [Orabug: 21539498]  
- Add BSD-style securelevel support (Matthew Garrett)  [Orabug: 21539498]  
- MODSIGN: Support not importing certs from db (Josh Boyer)  [Orabug: 21539498]  
- MODSIGN: Import certificates from UEFI Secure Boot (Josh Boyer)  [Orabug: 21539498]  
- MODSIGN: Add module certificate blacklist keyring (Josh Boyer)  [Orabug: 21539498]  
- Add an EFI signature blob parser and key loader. (Dave Howells)  [Orabug: 21539498]  
- Add EFI signature data types (Dave Howells)  [Orabug: 21539498]  

* Fri Aug 7 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.4-4.el7uek] 
- NVMe: Fix filesystem deadlock on removal (Keith Busch)  [Orabug: 21569452]  
- NVMe: Failed controller initialization fixes (Keith Busch)  [Orabug: 21569452]  
- NVMe: Unify controller probe and resume (Santosh Shilimkar)  [Orabug: 21569452]  
- NVMe: Automatic namespace rescan (Keith Busch)   
- block: add blk_set_queue_dying() to blkdev.h (Jens Axboe)  [Orabug: 21569452]  
- NVMe: Don't use fake status on cancelled command (Keith Busch)  [Orabug: 21569452]  
- NVMe: Fix device cleanup on initialization failure (Keith Busch)  [Orabug: 21569452]  
- NVMe: add sysfs and ioctl controller reset (Keith Busch)  [Orabug: 21569452]  
- uek-rpm: configs: sync up configs with latest tag (Santosh Shilimkar)   
- NVMe: Return busy status on suspended queue (Keith Busch)  [Orabug: 21316131]  

* Tue Aug 4 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.4-3.el7uek] 
- Revert "block: loop: convert to per-device workqueue" (Santosh Shilimkar)  [Orabug: 21059915]  
- Revert "block: loop: avoiding too many pending per work I/O" (Santosh Shilimkar)  [Orabug: 21059915]  
- uek-rpm: build: Update the base release to 4 with stable v4.1.4 (Santosh Shilimkar)   
- Linux 4.1.4 (Greg Kroah-Hartman)   
- x86/mpx: Do not set ->vm_ops on MPX VMAs (Kirill A. Shutemov)   
- mm: avoid setting up anonymous pages into file mapping (Kirill A. Shutemov)   
- Fix firmware loader uevent buffer NULL pointer dereference (Linus Torvalds)   
- hpfs: hpfs_error: Remove static buffer, use vsprintf extension %pV instead (Joe Perches)   
- hpfs: kstrdup() out of memory handling (Sanidhya Kashyap)   
- ARM: 8397/1: fix vdsomunge not to depend on glibc specific error.h (Szabolcs Nagy)   
- ARM: 8393/1: smp: Fix suspicious RCU usage with ipi tracepoints (Stephen Boyd)   
- perf bench numa: Fix to show proper convergence stats (Srikar Dronamraju)   
- arm64: Don't report clear pmds and puds as huge (Christoffer Dall)   
- arm64: bpf: fix endianness conversion bugs (Xi Wang)   
- arm64: bpf: fix out-of-bounds read in bpf2a64_offset() (Xi Wang)   
- ARM64: smp: Fix suspicious RCU usage with ipi tracepoints (Stephen Boyd)   
- p9_client_write(): avoid double p9_free_req() (Al Viro)   
- EDAC, octeon: Fix broken build due to model helper renames (Aaro Koskinen)   
- ARM: dove: fix legacy dove IRQ numbers (Russell King)   
- agp/intel: Fix typo in needs_ilk_vtd_wa() (Chris Wilson)   
- rbd: use GFP_NOIO in rbd_obj_request_create() (Ilya Dryomov)   
- 9p: don't leave a half-initialized inode sitting around (Al Viro)   
- 9p: forgetting to cancel request on interrupted zero-copy RPC (Al Viro)   
- SUNRPC: Fix a memory leak in the backchannel code (Trond Myklebust)   
- nfs: always update creds in mirror, even when we have an already connected ds (Jeff Layton)   
- nfs: fix potential credential leak in ff_layout_update_mirror_cred (Jeff Layton)   
- NFS: Ensure we set NFS_CONTEXT_RESEND_WRITES when requeuing writes (Trond Myklebust)   
- nfs: increase size of EXCHANGE_ID name string buffer (Jeff Layton)   
- fixing infinite OPEN loop in 4.0 stateid recovery (Olga Kornievskaia)   
- NFS: Fix size of NFSACL SETACL operations (Chuck Lever)   
- pNFS/flexfiles: Fix the reset of struct pgio_header when resending (Trond Myklebust)   
- pNFS: Fix a memory leak when attempted pnfs fails (Trond Myklebust)   
- clk: qcom: Use parent rate when set rate to pixel RCG clock (Hai Li)   
- clk: ti: dra7-atl-clock: Fix possible ERR_PTR dereference (Krzysztof Kozlowski)   
- clk: Fix JSON output in debugfs (Stefan Wahren)   
- gpiolib: Add missing dummies for the unified device properties interface (Geert Uytterhoeven)   
- watchdog: omap: assert the counter being stopped before reprogramming (Uwe Kleine-König)   
- of: return NUMA_NO_NODE from fallback of_node_to_nid() (Konstantin Khlebnikov)   
- ovl: lookup whiteouts outside iterate_dir() (Miklos Szeredi)   
- dell-laptop: Fix allocating & freeing SMI buffer page (Pali Rohár)   
- of/address: use atomic allocation in pci_register_io_range() (Jingoo Han)   
- ideapad: fix software rfkill setting (Arnd Bergmann)   
- ideapad_laptop: Lenovo G50-30 fix rfkill reports wireless blocked (Dmitry Tunin)   
- clocksource: exynos_mct: Avoid blocking calls in the cpu hotplug notifier (Damian Eppel)   
- e1000e: Cleanup handling of VLAN_HLEN as a part of max frame size (Alexander Duyck)   
- mac80211: prevent possible crypto tx tailroom corruption (Michal Kazior)   
- cfg80211: ignore netif running state when changing iftype (Michal Kazior)   
- iwlwifi: mvm: fix ROC reference accounting (Eliad Peller)   
- mac80211: fix the beacon csa counter for mesh and ibss (Chun-Yeow Yeoh)   
- security_syslog() should be called once only (Vasily Averin)   
- __bitmap_parselist: fix bug in empty string handling (Chris Metcalf)   
- compiler-intel: fix wrong compiler barrier() macro (Daniel Borkmann)   
- firmware: dmi_scan: Only honor end-of-table for 64-bit tables (Jean Delvare)   
- PM / sleep: Increase default DPM watchdog timeout to 60 (Takashi Iwai)   
- mm/hugetlb: introduce minimum hugepage order (Naoya Horiguchi)   
- tty: remove platform_sysrq_reset_seq (Arnd Bergmann)   
- RDMA/ocrdma: fix double free on pd (Colin Ian King)   
- PM / clk: Fix clock error check in __pm_clk_add() (Geert Uytterhoeven)   
- mmc: sdhci: Restore behavior while creating OCR mask (Ulf Hansson)   
- mmc: card: Fixup request missing in mmc_blk_issue_rw_rq (Ding Wang)   
- serial: samsung: only use earlycon for console (Arnd Bergmann)   
- ACPI / PCI: Fix regressions caused by resource_size_t overflow with 32-bit kernel (Jiang Liu)   
- ACPICA: Tables: Enable default 64-bit FADT addresses favor (Lv Zheng)   
- ACPICA: Tables: Fix an issue that FACS initialization is performed twice (Lv Zheng)   
- ACPICA: Tables: Enable both 32-bit and 64-bit FACS (Lv Zheng)   
- ACPI / LPSS: Fix up acpi_lpss_create_device() (Rafael J. Wysocki)   
- ACPI / PNP: Reserve ACPI resources at the fs_initcall_sync stage (Rafael J. Wysocki)   
- ACPI / resources: free memory on error in add_region_before() (Dan Carpenter)   
- crush: fix a bug in tree bucket decode (Ilya Dryomov)   
- fuse: initialize fc->release before calling it (Miklos Szeredi)   
- selinux: fix mprotect PROT_EXEC regression caused by mm change (Stephen Smalley)   
- selinux: don't waste ebitmap space when importing NetLabel categories (Paul Moore)   
- Btrfs: fix file corruption after cloning inline extents (Filipe Manana)   
- Btrfs: fix list transaction->pending_ordered corruption (Filipe Manana)   
- Btrfs: fix memory leak in the extent_same ioctl (Filipe Manana)   
- Btrfs: fix fsync data loss after append write (Filipe Manana)   
- Btrfs: fix race between caching kthread and returning inode to inode cache (Filipe Manana)   
- Btrfs: use kmem_cache_free when freeing entry in inode cache (Filipe Manana)   
- md: fix a build warning (Firo Yang)   
- Btrfs: don't invalidate root dentry when subvolume deletion fails (Omar Sandoval)   
- ARM: dts: mx23: fix iio-hwmon support (Stefan Wahren)   
- hwmon: (nct7802) fix visibility of temp3 (Constantine Shulyupin)   
- hwmon: (mcp3021) Fix broken output scaling (Stevens, Nick)   
- md: Skip cluster setup for dm-raid (Goldwyn Rodrigues)   
- md: unlock mddev_lock on an error path. (NeilBrown)   
- md: clear mddev->private when it has been freed. (NeilBrown)   
- dmaengine: mv_xor: bug fix for racing condition in descriptors cleanup (Lior Amsalem)   
- tracing: Fix sample output of dynamic arrays (Steven Rostedt (Red Hat))   
- tracing: Have branch tracer use recursive field of task struct (Steven Rostedt (Red Hat))   
- tracing: Fix typo from "static inlin" to "static inline" (Steven Rostedt (Red Hat))   
- tracing/filter: Do not allow infix to exceed end of string (Steven Rostedt (Red Hat))   
- tracing/filter: Do not WARN on operand count going below zero (Steven Rostedt (Red Hat))   
- ima: update builtin policies (Mimi Zohar)   
- ima: extend "mask" policy matching support (Mimi Zohar)   
- ima: add support for new "euid" policy condition (Mimi Zohar)   
- ima: fix ima_show_template_data_ascii() (Mimi Zohar)   
- evm: labeling pseudo filesystems exception (Mimi Zohar)   
- ima: do not measure or appraise the NSFS filesystem (Mimi Zohar)   
- ima: cleanup ima_init_policy() a little (Dan Carpenter)   
- ima: skip measurement of cgroupfs files and update documentation (Roberto Sassu)   
- KEYS: ensure we free the assoc array edit if edit is valid (Colin Ian King)   {CVE-2015-1333} 
- KEYS: fix "ca_keys=" partial key matching (Mimi Zohar)   
- tpm, tpm_crb: fail when TPM2 ACPI table contents look corrupted (Jarkko Sakkinen)   
- tpm: Fix initialization of the cdev (Jason Gunthorpe)   
- vTPM: set virtual device before passing to ibmvtpm_reset_crq (Hon Ching \(Vicky\) Lo)   
- tpm, tpm_crb: fix le64_to_cpu conversions in crb_acpi_add() (Jarkko Sakkinen)   
- w1_therm reference count family data (David Fries)   
- xfs: don't truncate attribute extents if no extents exist (Brian Foster)   
- xfs: fix remote symlinks on V5/CRC filesystems (Eric Sandeen)   
- libata: Fix regression when the NCQ Send and Receive log page is absent (Martin K. Petersen)   
- drm: Stop resetting connector state to unknown (Daniel Vetter)   
- drm: Provide compat ioctl for addfb2.1 (Tvrtko Ursulin)   
- drm: add a check for x/y in drm_mode_setcrtc (Zhao Junwang)   
- drm/rockchip: use drm_gem_mmap helpers (Daniel Kurtz)   
- drm/radeon/ci: silence a harmless PCC warning (Alex Deucher)   
- drm/radeon: fix user ptr race condition (Christian König)   
- drm/radeon: add a dpm quirk for Sapphire Radeon R9 270X 2GB GDDR5 (Alex Deucher)   
- drm/radeon: Don't flush the GART TLB if rdev->gart.ptr == NULL (Michel Dänzer)   
- drm/radeon: unpin cursor BOs on suspend and pin them again on resume (v2) (Grigori Goronzy)   
- drm/radeon: Clean up reference counting and pinning of the cursor BOs (Michel Dänzer)   
- drm/radeon: Handle irqs only based on irq ring, not irq status regs. (Mario Kleiner)   
- drm/radeon: fix HDP flushing (Grigori Goronzy)   
- drm/radeon: only check the sink type on DP connectors (Alex Deucher)   
- Revert "drm/radeon: dont switch vt on suspend" (Alex Deucher)   
- drm/radeon: SDMA fix hibernation (CI GPU family). (Jérôme Glisse)   
- drm/radeon: compute ring fix hibernation (CI GPU family) v2. (Jérôme Glisse)   
- drm/i915: Use two 32bit reads for select 64bit REG_READ ioctls (Chris Wilson)   
- Revert "drm/i915: Declare the swizzling unknown for L-shaped configurations" (Daniel Vetter)   
- drm/i915: Forward all core DRM ioctls to core compat handling (Tvrtko Ursulin)   
- drm/i915: Snapshot seqno of most recently submitted request. (Tomas Elf)   
- drm/i915: Declare the swizzling unknown for L-shaped configurations (Chris Wilson)   
- drm/i915: fix backlight after resume on 855gm (Jani Nikula)   
- drm/i915: Fix IPS related flicker (Rodrigo Vivi)   
- drm/i915/ppgtt: Break loop in gen8_ppgtt_clear_range failure path (Michel Thierry)   
- drm/radeon: clean up radeon_audio_enable (Alex Deucher)   
- drm/radeon: take the mode_config mutex when dealing with hpds (v2) (Alex Deucher)   
- drm/atomic: fix out of bounds read in for_each_*_in_state helpers (Andrey Ryabinin)   
- drm/bridge: ptn3460: Include linux/gpio/consumer.h (Geert Uytterhoeven)   
- drm/qxl: Do not leak memory if qxl_release_list_add fails (Frediano Ziglio)   
- drm/qxl: Do not cause spice-server to clean our objects (Frediano Ziglio)   
- drm/tegra: dpaux: Fix transfers larger than 4 bytes (Thierry Reding)   
- drm/dp/mst: make sure mst_primary mstb is valid in work function (Daniel Vetter)   
- drm/dp/mst: take lock around looking up the branch device on hpd irq (Dave Airlie)   
- drm/dp/mst: close deadlock in connector destruction. (Dave Airlie)   
- drm/vgem: Set unique to "vgem" (Daniel Vetter)   
- bus: arm-ccn: Fix node->XP config conversion (Pawel Moll)   
- ARM: at91/dt: update udc compatible strings (Boris Brezillon)   
- ARM: at91/dt: trivial: fix USB udc compatible string (Nicolas Ferre)   
- tty/serial: at91: RS485 mode: 0 is valid for delay_rts_after_send (Nicolas Ferre)   
- ARM: at91/dt: sama5d4: fix dma conf for aes, sha and tdes nodes (ludovic.desroches@atmel.com)   
- ARM: at91/dt: sama5d4ek: mci0 uses slot 0 (Ludovic Desroches)   
- block: Do a full clone when splitting discard bios (Martin K. Petersen)   
- block: loop: avoiding too many pending per work I/O (Ming Lei)   
- block: loop: convert to per-device workqueue (Ming Lei)   
- mmc: block: Add missing mmc_blk_put() in power_ro_lock_show() (Tomas Winkler)   
- dm btree: silence lockdep lock inversion in dm_btree_del() (Joe Thornber)   
- dm thin: allocate the cell_sort_array dynamically (Joe Thornber)   
- dm btree remove: fix bug in redistribute3 (Dennis Yang)   
- dm space map metadata: fix occasional leak of a metadata block on resize (Joe Thornber)   
- dm stats: fix divide by zero if 'number_of_areas' arg is zero (Mikulas Patocka)   
- dm cache: fix race when issuing a POLICY_REPLACE operation (Joe Thornber)   
- usb: xhci: Bugfix for NULL pointer deference in xhci_endpoint_init() function (AMAN DEEP)   
- usb: core: lpm: set lpm_capable for root hub device (Lu Baolu)   
- USB: OHCI: Fix race between ED unlink and URB submission (Alan Stern)   
- USB: serial: Destroy serial_minors IDR on module exit (Johannes Thumshirn)   
- USB: option: add 2020:4000 ID (Claudio Cappelli)   
- USB: cp210x: add ID for Aruba Networks controllers (Peter Sanford)   
- usb: musb: host: rely on port_mode to call musb_start() (Felipe Balbi)   
- usb: f_mass_storage: limit number of reported LUNs (Michal Nazarewicz)   
- usb: gadget: mv_udc_core: fix phy_regs I/O memory leak (Alexey Khoroshilov)   
- usb: gadget: f_fs: do not set cancel function on synchronous {read,write} (Rui Miguel Silva)   
- usb: gadget: composite: Fix NULL pointer dereference (Kishon Vijay Abraham I)   
- phy: berlin-usb: fix divider for BG2CD (Thomas Hebb)   
- usb: phy: mxs: suspend to RAM causes NULL pointer dereference (Stefan Wahren)   
- phy: twl4030-usb: remove incorrect pm_runtime_get_sync() in probe function. (NeilBrown)   
- USB: devio: fix a condition in async_completed() (Dan Carpenter)   
- usb: core: Fix USB 3.0 devices lost in NOTATTACHED state after a hub port reset (Robert Schlabbach)   
- usb: dwc3: Reset the transfer resource index on SET_INTERFACE (John Youn)   
- usb: dwc3: gadget: don't clear EP_BUSY too early (Felipe Balbi)   
- usb: dwc3: gadget: return error if command sent to DEPCMD register fails (Subbaraya Sundeep Bhatta)   
- usb: dwc3: gadget: return error if command sent to DGCMD register fails (Subbaraya Sundeep Bhatta)   
- libata: force disable trim for SuperSSpeed S238 (Arne Fitzenreiter)   
- libata: Do not blacklist M510DC (Martin K. Petersen)   
- libata: add ATA_HORKAGE_MAX_SEC_1024 to revert back to previous max_sectors limit (David Milburn)   
- libata: add ATA_HORKAGE_NOTRIM (Arne Fitzenreiter)   
- libata: Expose TRIM capability in sysfs (Martin K. Petersen)   
- libata: Fall back to unqueued READ LOG EXT if the DMA variant fails (Martin K. Petersen)   
- libata: increase the timeout when setting transfer mode (Mikulas Patocka)   
- libata: add ATA_HORKAGE_BROKEN_FPDMA_AA quirk for HP 250GB SATA disk VB0250EAVER (Aleksei Mamlin)   
- libata: Do not blacklist Micron M500DC (Martin K. Petersen)   
- ASoC: tas2552: Fix kernel crash caused by wrong kcontrol entry (Peter Ujfalusi)   
- ASoC: tas2552: Fix kernel crash when the codec is loaded but not part of a card (Peter Ujfalusi)   
- ASoC: wm8960: the enum of "DAC Polarity" should be wm8960_enum[1] (Zidan Wang)   
- ASoC: wm8903: Fix define for WM8903_VMID_RES_250K (Axel Lin)   
- ASoC: wm8955: Fix setting wrong register for WM8955_K_8_0_MASK bits (Axel Lin)   
- ASoC: wm8737: Fixup setting VMID Impedance control register (Axel Lin)   
- ASoC: omap: fix up SND_OMAP_SOC_OMAP_ABE_TWL6040 dependency, again (Arnd Bergmann)   
- ASoC: imx-wm8962: Add a missing error check (Dan Carpenter)   
- ASoC: qcom: remove incorrect dependencies (Arnd Bergmann)   
- ASoC: max98925: Fix mask for setting DAI invert mode (Axel Lin)   
- ASoC: rt5645: Init jack_detect_work before registering irq (Nicolas Boichat)   
- ASoC: arizona: Fix noise generator gain TLV (Richard Fitzgerald)   
- cx24116: fix a buffer overflow when checking userspace params (Mauro Carvalho Chehab)   
- s5h1420: fix a buffer overflow when checking userspace params (Mauro Carvalho Chehab)   
- saa7164: fix querycap warning (Hans Verkuil)   
- af9013: Don't accept invalid bandwidth (Mauro Carvalho Chehab)   
- cx24117: fix a buffer overflow when checking userspace params (Mauro Carvalho Chehab)   
- cx18: add missing caps for the PCM video device (Hans Verkuil)   
- rc-core: fix dib0700 scancode generation for RC5 (David Härdeman)   
- media: Fix regression in some more dib0700 based devices (Thomas Reitmayr)   
- vb2: Don't WARN when v4l2_buffer.bytesused is 0 for multiplanar buffers (Laurent Pinchart)   
- iio: adc: at91_adc: allow to use full range of startup time (Jan Leupold)   
- iio: adc: rockchip_saradc: add missing MODULE_* data (Heiko Stuebner)   
- iio: proximity: sx9500: Fix proximity value (Daniel Baluta)   
- iio: ABI: Clarify proximity output value (Daniel Baluta)   
- iio: twl4030-madc: Pass the IRQF_ONESHOT flag (Fabio Estevam)   
- iio: tmp006: Check channel info on write (Peter Meerwald)   
- iio: inv-mpu: Specify the expected format/precision for write channels (Adriana Reus)   
- iio: DAC: ad5624r_spi: fix bit shift of output data value (JM Friedt)   
- iio: light: tcs3414: Fix bug preventing to set integration time (Peter Meerwald)   
- iio:accel:bmc150-accel: fix counting direction (Hartmut Knaack)   
- iio:adc:cc10001_adc: fix Kconfig dependency (Hartmut Knaack)   
- iio:light:cm3323: clear bitmask before set (Hartmut Knaack)   
- i2c: use parent adapter quirks in mux (Alexander Sverdlin)   
- i2c: mux: pca954x: Use __i2c_transfer because of quirks (Alexander Sverdlin)   
- i2c: mux: Use __i2c_transfer() instead of calling parent's master_xfer() (Alexander Sverdlin)   
- i2c: at91: fix a race condition when using the DMA controller (Cyrille Pitchen)   
- rtc: snvs: fix wakealarm by call enable_irq_wake earlier (Stefan Agner)   
- NFC: st21nfcb: remove st21nfcb_nci_i2c_disable (Christophe Ricard)   
- NFC: st21nfcb: Do not remove header once the payload is sent (Christophe Ricard)   
- NFC: st21nfcb: Remove inappropriate kfree on a devm_kzalloc pointer (Firo Yang)   
- jbd2: fix ocfs2 corrupt when updating journal superblock fails (Joseph Qi)   
- jbd2: use GFP_NOFS in jbd2_cleanup_journal_tail() (Dmitry Monakhov)   
- ext4: replace open coded nofail allocation in ext4_free_blocks() (Michal Hocko)   
- ext4: correctly migrate a file with a hole at the beginning (Eryu Guan)   
- ext4: be more strict when migrating to non-extent based file (Eryu Guan)   
- ext4: fix reservation release on invalidatepage for delalloc fs (Lukas Czerner)   
- ext4: avoid deadlocks in the writeback path by using sb_getblk_gfp (Nikolay Borisov)   
- bufferhead: Add _gfp version for sb_getblk() (Nikolay Borisov)   
- ext4: fix fencepost error in lazytime optimization (Theodore Ts'o)   
- ext4: set lazytime on remount if MS_LAZYTIME is set by mount (Theodore Ts'o)   
- ext4: don't retry file block mapping on bigalloc fs with non-extent file (Darrick J. Wong)   
- ext4: call sync_blockdev() before invalidate_bdev() in put_super() (Theodore Ts'o)   
- ext4: fix race between truncate and __ext4_journalled_writepage() (Theodore Ts'o)   
- hid-sensor: Fix suspend/resume delay (Srinivas Pandruvada)   
- staging: comedi: cb_pcimdas: fix handlers for DI and DO subdevices (Ian Abbott)   
- staging: rtl8712: prevent buffer overrun in recvbuf2recvframe (Haggai Eran)   
- staging: vt6655: device_rx_srv check sk_buff is NULL (Malcolm Priestley)   
- staging: vt6655: check ieee80211_bss_conf bssid not NULL (Malcolm Priestley)   
- staging: vt6656: check ieee80211_bss_conf bssid not NULL (Malcolm Priestley)   
- ieee802154: Fix sockaddr_ieee802154 implicit padding information leak. (Lennert Buytenhek)   
- rtlwifi: Remove the clear interrupt routine from all drivers (Vincent Fann)   
- ath9k_htc: memory corruption calling set_bit() (Dan Carpenter)   
- ath9k: fix DMA stop sequence for AR9003+ (Felix Fietkau)   
- Bluetooth: btbcm: allow btbcm_read_verbose_config to fail on Apple (Chris Mason)   
- Bluetooth: btusb: Correct typo in Roper Class 1 Bluetooth Dongle (Aleksei Volkov)   
- Bluetooth: btusb: Fix secure send command length alignment on Intel 8260 (Marcel Holtmann)   
- Bluetooth: btusb: Fix memory leak in Intel setup routine (Marcel Holtmann)   
- Bluetooth: Fix race condition with user channel and setup stage (Marcel Holtmann)   
- m68knommu: force setting of CONFIG_CLOCK_FREQ for ColdFire (Greg Ungerer)   
- m68knommu: make ColdFire SoC selection a choice (Greg Ungerer)   
- openrisc: fix CONFIG_UID16 setting (Andrew Morton)   
- pinctrl: mvebu: armada-xp: fix functions of MPP48 (Thomas Petazzoni)   
- pinctrl: mvebu: armada-xp: remove non-existing VDD cpu_pd functions (Thomas Petazzoni)   
- pinctrl: mvebu: armada-xp: remove non-existing NAND pins (Thomas Petazzoni)   
- pinctrl: mvebu: armada-39x: fix incorrect total number of GPIOs (Thomas Petazzoni)   
- pinctrl: mvebu: armada-38x: fix incorrect total number of GPIOs (Thomas Petazzoni)   
- pinctrl: mvebu: armada-38x: fix PCIe functions (Thomas Petazzoni)   
- pinctrl: mvebu: armada-375: remove non-existing NAND re/we pins (Thomas Petazzoni)   
- pinctrl: mvebu: armada-375: remove incorrect space in pin description (Thomas Petazzoni)   
- pinctrl: mvebu: armada-370: fix spi0 pin description (Thomas Petazzoni)   
- pinctrl: zynq: fix offset address for {SD0,SD1}_WP_CD_SEL (Masahiro Yamada)   
- pinctrl: zynq: fix DEFINE_ZYNQ_PINMUX_FUNCTION_MUX macro (Masahiro Yamada)   
- dtrace: accomodate changes in the 4.1 kernel for sparc64 (Kris Van Hees)   
- dtrace: implement dtrace_handle_badaddr() for x86 (Kris Van Hees)   
- dtrace: ignore any and all PFs during NOFAULT memory acceses (Kris Van Hees)   
- dtrace: do not allocate space for trampolines when probec = 0 (Kris Van Hees)   
- dtrace: convert from sdt_instr_t to asm_instr_t 2of2 (Kris Van Hees)  [Orabug: 21220305]  
- dtrace: convert from sdt_instr_t to asm_instr_t 1of2 (Kris Van Hees)  [Orabug: 21220305]  
- dtrace: allocate space for SDT trampolines using module_alloc (Kris Van Hees)  [Orabug: 21220344]  
- dtrace: accomodate changes in the 4.1 kernels (Kris Van Hees)   
- kallsyms: fix /proc/kallmodsyms to not be misled by const variables (Nick Alcock)  [Orabug: 21257163]  
- kallsyms: fix /proc/kallmodsyms to not be misled by external symbols (Nick Alcock)  [Orabug: 21172433]  
- wait: change waitfd() to use wait4(), not waitid(); reduce invasiveness (Nick Alcock)  [Orabug: 21245371]  
- dtrace: use a nonzero reference count on the fake module (Nick Alcock)   
- dtrace: percpu: move from __get_cpu_var() to this_cpu_ptr() (Nick Alcock)   
- dtrace: x86: Cater for new instruction size limit in instruction decoder (Nick Alcock)   
- mm: memcontrol: adjust prototype to allow for poll_wait_fixed() changes. (Nick Alcock)   
- dtrace: zero-initialize the fake vmlinux module's pdata space (Nick Alcock)  [Orabug: 19005031]  
- dtrace: remove obsolete function (Kris Van Hees)  [Orabug: 20456825]  
- dtrace: make it possible to call do_sigaltstack() (Kris Van Hees)  [Orabug: 20456825]  
- dtrace: do not vmalloc/vfree from probe context (Kris Van Hees)  [Orabug: 20456889]  
- dtrace: fix dtrace_sdt.sh for UEK4 (Kris Van Hees)  [Orabug: 20456825]  
- ctf: update dwarf2ctf documentation. (Nick Alcock)  [Orabug: 20229506]  
- ctf: speed up dwarf2ctf by avoiding ctf_update() calls (Nick Alcock)  [Orabug: 20229506]  
- ctf: move the module->ctf_file info into a structure. (Nick Alcock)  [Orabug: 20229506]  
- ctf: duplicate-detect dependent types properly (Nick Alcock)  [Orabug: 20229431]  
- Remove BUILD_BUG_ON for epitem size code to compile. (Nick Alcock)  [Orabug: 20456825]  
- dtrace: stub syscall fixes for 3.18. (Nick Alcock)  [Orabug: 20456825]  
- ctf: Prohibit a bunch of debug info options we don't support. (Nick Alcock)  [Orabug: 20456825]  
- dtrace: add support for sparc64 3of3 (Kris Van Hees)  [Orabug: 19005031]  
- dtrace: add support for sparc64 2of3 (Kris Van Hees)  [Orabug: 19005031]  
- dtrace: add support for sparc64 1of3 (Kris Van Hees)  [Orabug: 19005031]  
- dtrace: restructuring for multi-arch support (Kris Van Hees)  [Orabug: 20262965]  
- dtrace: set ARCH_SUPPORTS_DTRACE for x86_64 (Kris Van Hees)  [Orabug: 20262965]  
- dwarf2ctf: don't use O_PATH in rel_abs_file_name(). (Jamie Iles)  [Orabug: 19957565]  
- dwarf2ctf: don't leak directory fd. (Jamie Iles)  [Orabug: 19957565]  
- ctf: handle srcdir-relative paths properly. (Nick Alcock)  [Orabug: 19712731]  
- kbuild/ctf: Fix out-of-tree module build when CONFIG_CTF=n. (Nick Alcock)  [Orabug: 19078361]  
- dtrace: support order-only-prerequisites for sdtstub generation (Kris Van Hees)  [Orabug: 18906444]  
- dtrace: ensure that building outside src tree works (Kris Van Hees)  [Orabug: 18691341]  
- dtrace: ensure one can try to get user pages without locking or faulting (Kris Van Hees)  [Orabug: 18653173]  
- mm / dtrace: Allow DTrace to entirely disable page faults. (Nick Alcock)  [Orabug: 18412802]  
- mm: allow __get_user_pages() callers to avoid triggering page faults. (Nick Alcock)  [Orabug: 18412802]  
- dtrace: implement omni-present cyclics (Kris Van Hees)  [Orabug: 18323501]  
- gitignore: update .gitignore with generated SDT files (Nick Alcock)  [Orabug: 17851716]  
- dtrace: avoid unreliable entries in stack() output (Kris Van Hees)  [Orabug: 18323450]  
- dtrace: fix leaking psinfo objects (Kris Van Hees)  [Orabug: 18383027]  
- ctf: spot non-struct/union/enum children of DW_TAG_structure_type (Nick Alcock)  [Orabug: 18117464]  
- ctf: capture all DIEs with structs/enums as their ultimate supertype (Nick Alcock)  [Orabug: 18117464]  
- ctf: handle structure and union offsets in form DW_FORM_data1 (Nick Alcock)  [Orabug: 18117464]  
- ctf: cater for elfutils 0.156 change in dwfl_report_elf() prototype (Nick Alcock)  [Orabug: 18117421]  
- dtrace: vtimestamp implementation (Kris Van Hees)  [Orabug: 17741477]  
- dtrace: implement SDT in kernel modules (Kris Van Hees)  [Orabug: 17851716]  
- dtrace: remove functionality of dtrace_os_exit() as deprecated (Kris Van Hees)  [Orabug: 17717401]  
- dtrace: fix mutex_owned() implementation (Kris Van Hees)  [Orabug: 17624236]  
- dtrace: new cyclic implementation (Kris Van Hees)  [Orabug: 17553446]  
- dtrace: Use tasklet_hrtimer_*() instead of hrtimer_*() for cyclics (Kris Van Hees)  [Orabug: 17553446]  
- dtrace: fix for psinfo allocation during execve (Kris Van Hees)  [Orabug: 17407069]  
- kbuild/ctf: Use shell expansion, not $(wildcard ...), for CTF section copying. (Nick Alcock)  [Orabug: 17445637]  
- kbuild/ctf: always build vmlinux when building CTF. (Jamie Iles)  [Orabug: 17397200]  
- dtrace: remove unnecessary exported symbol (Kris Van Hees)  [Orabug: 17346878]  
- dtrace: Ensure that USDT probes are carried over correctly across fork(). (Kris Van Hees)  [Orabug: 17346878]  
- dtrace: fix retrieval of arg5 through arg9 (Kris Van Hees)  [Orabug: 17368166]  
- dtrace: Ensure that task_struct members are initialized correctly (Kris Van Hees)   
- dtrace: ensure that builds in a separate objdir work (Kris Van Hees)  [Orabug: 17369799]  
- ctf: ensure the CTF directory exists before writing the filelist (Nick Alcock)  [Orabug: 17363469]  
- ctf: avoid command-line length limits by passing .o filenames via a file (Nick Alcock)  [Orabug: 17363469]  
- dtrace: DT_FASTTRAP should select UPROBE_EVENT (Jerry Snitselaar)  [Orabug: 17325699]  
- dtrace: Fix for the argument validation code. (Kris Van Hees)  [Orabug: 17313687]  
- dtrace: Include asm/current.h for the mutex_owned() fucntion. (Kris Van Hees)  [Orabug: 17313687]  
- dtrace: Bug fix for logic to determine the (inode, offset) pair for uprobes. (Kris Van Hees)   
- dtrace: ensure memory allocation results are checked throughout the code (Kris Van Hees)   
- dtrace: remove pre-alpha features for release (Kris Van Hees)   
- dtrace: CONFIG_UPROBES is needed by CONFIG_DT_FASTTRAP, not CONFIG_DTRACE (Nick Alcock)   
- dtrace: CONFIG_DTRACE should depend on CONFIG_UPROBES (Nick Alcock)   
- wait: fix loss of error code from waitid() when info is provided (Nick Alcock)   
- waitfd selftest: dike out some dead code. (Nick Alcock)   
- epoll, wait: introduce poll_wait_fixed(), and use it in waitfds (Nick Alcock)   
- ctf: no longer reference 'ctf.ko.unsigned' in CTF debuginfo stripping machinery (Nick Alcock)   
- wait: add waitfd(), and a testcase for it (Nick Alcock)   
- dtrace: ensure that arg6 through arg9 get retrieved correctly for USDT probes (Kris Van Hees)   
- dtrace: finish the implementation of is-enabled USDT probes (Kris Van Hees)   
- dtrace: fixes for tracepoint cleanup (Kris Van Hees)   
- dtrace: update syscall tracing in view of Linux 3.8 changes (Kris Van Hees)   
- dtrace: USDT implementation (phase 2) (Kris Van Hees)   
- dtrace: revamp and split up DTrace headers; add ioctl() debugging machinery (Nick Alcock)   
- ctf: blacklist certain structure members entirely (Nick Alcock)   
- ctf: repair faulty indentation (Nick Alcock)   
- ctf: split the absolute-file-name caching machinery out of type_id() (Nick Alcock)   
- ctf: sentinelize str_appendn() (Nick Alcock)   
- ptrace: Add PTRACE_GETMAPFD. (Nick Alcock)   
- dtrace: update execve() syscall probe support (Kris Van Hees)   
- dtrace: add support for an SDT probe getting called from multiple functions (Kris Van Hees)   
- dtrace: move SDT call location for surrender probe (Kris Van Hees)   
- dtrace: USDT implementation (Phase 1) (Kris Van Hees)   
- dtrace: remove incorrect FBT support code (Kris Van Hees)   
- dtrace: move psinfo to its own header file (Kris Van Hees)   
- dtrace: update copyright statements (Kris Van Hees)   
- ctf: update the shared CTF file right after initialization (Nick Alcock)   
- ctf: Improve debugging and indentation fixes (Nick Alcock)   
- ctf: dwarf2ctf doc revisions (Nick Alcock)   
- dtrace: internal performance measurement support code (Kris Van Hees)   
- kvm / dtrace: disable KVM steal-time accounting when DTrace is in use (Nick Alcock)   
- ctf: cosmetic improvements to CTF linking (Nick Alcock)   
- dtrace: remove a few obsolete probes (Kris Van Hees)   
- dtrace: cater for changes in the way the kernel is linked (Kris Van Hees)   
- dtrace: miscellaneous 3.6 porting work (Kris Van Hees)   
- dtrace: fix up rq.dtrace_cpu_info member (Kris Van Hees)   
- gitignore: Ignore objects.builtin and dwarf2ctf. (Nick Alcock)   
- dtrace: fix outright typos in the 3.6 forward-port. (Nick Alcock)   
- dtrace: remove obsolete static probe documentation (Kris Van Hees)   
- ctf: DTrace-independent CTF (Nick Alcock)   
- ctf: do not build in CTF data for no-longer-built-in modules (Nick Alcock)   
- ctf: document dwarf2ctf (Nick Alcock)   
- ctf: Extend the deduplication blacklist (Nick Alcock)   
- ctf: Improve error message on internal deduplication error (Nick Alcock)   
- ctf: Note a future enhancement (Nick Alcock)   
- ctf: document parameters to die_to_ctf() (Nick Alcock)   
- ctf: do not construct objects.builtin if CTF is not being built (Nick Alcock)   
- ctf: do not build dwarf2ctf nor attempt to use it if !CONFIG_DTRACE (Nick Alcock)   
- dtrace: additional action support (and bug fixes) (Kris Van Hees)   
- dtrace: add psinfo/cpuinfo OS level support (Kris Van Hees)   
- dtrace: change the DTrace startup handling (at boot time) for SDT (Kris Van Hees)   
- dtrace: cleanup (and adding) of SDT probe points (Kris Van Hees)   
- ctf: write the CTF files for standalone modules to a subdir of the module dir (Nick Alcock)   
- ctf: unnamed structure/union support (Nick Alcock)   
- ctf: recurse_ctf() -> die_to_ctf() (Nick Alcock)   
- ctf: fix the signed-modules case (Nick Alcock)   
- ctf: correctly propagate IDs for array types (Nick Alcock)   
- ctf: fix off-by-one in emitted array bounds (Nick Alcock)   
- dtrace: fix tiny comment typo (Nick Alcock)   
- ctf: blacklist certain modules from deduplication (Nick Alcock)   
- ctf: include enumeration types inside functions (Nick Alcock)   
- dtrace: new IO and sched provider probes (Kris Van Hees)   
- dtrace: fix to handle multiple SDT-based probes in a single function (Kris Van Hees)   
- dtrace: require assembler symbol stripping and debug info (Nick Alcock)   
- ctf: fix array dimensions (Nick Alcock)   
- ctf: change the name of the CTF section in kernel modules (Nick Alcock)   
- dtrace: fix a bug in the SDT probe location generator (Kris Van Hees)   
- ctf: major duplicate detection fixes (Nick Alcock)   
- ctf: optimize type_id() and fix array dimension lookup (Nick Alcock)   
- dtrace: changed the logic for determining SDT probe point locations (Kris Van Hees)   
- ctf: store away the types and names of non-static global variables (Nick Alcock)   
- ctf: set the name of the parent of child modules to "dtrace_ctf" (Nick Alcock)   
- ctf: clarify comments, improve a type name (Nick Alcock)   
- ctf: force dtrace_ctf.ko to be loaded whenever dtrace.ko is (Nick Alcock)   
- ctf: generate CTF information for the kernel (Nick Alcock)   
- kallsyms: provide symbol sizes in /proc/kallmodsyms (Nick Alcock)   
- ctf: add a dummy dtrace_ctf.ko module (Nick Alcock)   
- kallsyms: fix /proc/kallmodsyms population bugs (Nick Alcock)   
- kallsyms: work in a clean tree, and a non-modular tree. (Nick Alcock)   
- kallsyms: work with older glibc. (Nick Alcock)   
- kallsyms: add /proc/kallmodsyms (Nick Alcock)   
- dtrace: add sched-tick SDT probe and FBT probe point discovery/creation (Kris Van Hees)   
- dtrace: use new mutex_owned(), not mutex_is_locked() (Kris Van Hees)   
- dtrace: fix signed division and modulo operations in DIF (Kris Van Hees)   
- dtrace: initialize the insn length in the right branch of the die notifier (Nick Alcock)   
- dtrace: ensure that the trap handler is regisstered only once (Kris Van Hees)   
- dtrace: install the die notifier hook whenever DTrace is enabled (Kris Van Hees)   
- dtrace: support for page fault and general protection fault detection (Kris Van Hees)   
- dtrace: fix incorrect probe point name (Kris Van Hees)   
- dtrace: add lwp-exit and lwp-create SDT probe points (Kris Van Hees)   
- dtrace: SDT implementation (Kris Van Hees)   
- dtrace: process the SDT probe point info early in boot (Kris Van Hees)   
- dtrace: fix resolving addresses of relocation records for SDT probe points (Kris Van Hees)   
- dtrace: fix cyclic allocation (Kris Van Hees)   
- dtrace: stub-based syscall tracing (Kris Van Hees)   
- dtrace: migrate stacktrace dumping and move headers about: fix reloc overrun (Kris Van Hees)   
- dtrace: move cyclic.h into include/linux (Nick Alcock)   
- dtrace: finish GPL/CDDL splitting work (Nick Alcock)   
- dtrace: fix GPL and CDDL copyright notices (Nick Alcock)   
- dtrace: Migrate to a standalone module, situated at the top level of the tree (Nick Alcock)   
- dtrace: changes in how we collect the names of system calls (Kris Van Hees)   
- dtrace: add dtrace_gethrtime() and fix walltimestamp. (Kris Van Hees)  [Orabug: 18376038]  
- dtrace: syscall entry/return probes. (Kris Van Hees)   
- dtrace: conflict with CONFIG_DEBUG_LOCK_ALLOC (Nick Alcock)   
- dtrace: update sdt provider (sdt_mod.c) with lots of functions (Randy Dunlap)   
- dtrace: add dtrace_module_loaded() and dtrace_module_unloaded() (Randy Dunlap)   
- dtrace: added CONFIG_DT_DEBUG_MUTEX option (Kris Van Hees)   
- dtrace: turn on gcov profiling in the kernel/dtrace directory by default (Nick Alcock)   
- dtrace: add dt_test provider. (Kris Van Hees)   
- dtrace: add Documentation/dtrace_static_probes.txt (Randy Dunlap)   
- dtrace: remove incorrect header comments and copyright (Randy Dunlap)   
- dtrace: build sdt_register.c into the kernel (Nick Alcock)   
- dtrace: add missing include needed for DTrace probes (Nick Alcock)   
- dtrace: convert relative probepoint relocation addresses to absolute (Randy Dunlap)   
- dtrace: add some dtrace static probes that are easy to trigger (Randy Dunlap)   
- dtrace: add FTRACE dependency (Kris Van Hees)   
- dtrace: Remove debugging statements (Kris Van Hees)   
- dtrace: fix unintended dependency on section ordering (Randy Dunlap)   
- dtrace: minimal cyclic implementation and debug code. (Kris Van Hees)   
- dtrace: DT_SYSTRACE should not depend on FTRACE_SYSCALLS. (Kris Van Hees)   
- dtrace: fix off-by-one reading relocation info. (Randy Dunlap)   
- dtrace: use _stext in dtrace_relocs. (Randy Dunlap)   
- dtrace: Fix compilation when modular. (Kris Van Hees)   
- dtrace: systrace should depend on FTRACE_SYSCALLS. (Randy Dunlap)   
- dtrace: Initial import of kernelspace code. (Nick Alcock)   

* Thu Jul 30 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.3-2.el7uek] 
- uek-rpm: build: Update the base release to 3 with stable v4.1.3 (Santosh Shilimkar)   
- Linux 4.1.3 (Greg Kroah-Hartman)   
- Input: pixcir_i2c_ts - fix receive error (Frodo Lai)   
- of/pci: Fix pci_address_to_pio() conversion of CPU address to I/O port (Zhichang Yuan)   
- PCI: pciehp: Wait for hotplug command completion where necessary (Alex Williamson)   
- PCI: Add pci_bus_addr_t (Yinghai Lu)   
- PCI: Propagate the "ignore hotplug" setting to parent (Rafael J. Wysocki)   
- mtd: dc21285: use raw spinlock functions for nw_gpio_lock (Uwe Kleine-König)   
- mtd: fix: avoid race condition when accessing mtd->usecount (Brian Norris)   
- leds / PM: fix hibernation on arm when gpio-led used with CPU led trigger (Grygorii Strashko)   
- video: mxsfb: Make sure axi clock is enabled when accessing registers (Liu Ying)   
- genirq: devres: Fix testing return value of request_any_context_irq() (Axel Lin)   
- IB/srp: Fix reconnection failure handling (Bart Van Assche)   
- IB/srp: Fix connection state tracking (Bart Van Assche)   
- IB/srp: Fix a connection setup race (Bart Van Assche)   
- IB/srp: Remove an extraneous scsi_host_put() from an error path (Bart Van Assche)   
- scsi_transport_srp: Fix a race condition (Bart Van Assche)   
- scsi_transport_srp: Introduce srp_wait_for_queuecommand() (Bart Van Assche)   
- spi: pl022: Specify 'num-cs' property as required in devicetree binding (Ezequiel Garcia)   
- spi: orion: Fix maximum baud rates for Armada 370/XP (Gregory CLEMENT)   
- spi: fix race freeing dummy_tx/rx before it is unmapped (Martin Sperl)   
- livepatch: add module locking around kallsyms calls (Miroslav Benes)   
- regulator: core: fix constraints output buffer (Stefan Wahren)   
- regulator: max77686: fix gpio_enabled shift wrapping bug (Joe Perches)   
- regmap: Fix possible shift overflow in regmap_field_init() (Maxime Coquelin)   
- regmap: Fix regmap_bulk_read in BE mode (Arun Chandran)   
- mm, thp: respect MPOL_PREFERRED policy with non-local node (Vlastimil Babka)   
- mm: kmemleak_alloc_percpu() should follow the gfp from per_alloc() (Larry Finger)   
- mm: kmemleak: allow safe memory scanning during kmemleak disabling (Catalin Marinas)   
- arm64: vdso: work-around broken ELF toolchains in Makefile (Will Deacon)   
- arm64: mm: Fix freeing of the wrong memmap entries with !SPARSEMEM_VMEMMAP (Dave P Martin)   
- arm64: entry: fix context tracking for el0_sp_pc (Mark Rutland)   
- arm64: Do not attempt to use init_mm in reset_context() (Catalin Marinas)   
- mei: txe: reduce suspend/resume time (Tomas Winkler)   
- mei: me: wait for power gating exit confirmation (Alexander Usyskin)   
- power_supply: Fix possible NULL pointer dereference on early uevent (Krzysztof Kozlowski)   
- power_supply: Fix NULL pointer dereference during bq27x00_battery probe (Krzysztof Kozlowski)   
- arc: fix use of uninitialized arc_pmu (Max Filippov)   
- ARC: add compiler barrier to LLSC based cmpxchg (Vineet Gupta)   
- ARC: add smp barriers around atomics per Documentation/atomic_ops.txt (Vineet Gupta)   
- tools selftests: Fix 'clean' target with make 3.81 (Arnaldo Carvalho de Melo)   
- iio: accel: kxcjk-1013: add the "KXCJ9000" ACPI id (Antonio Ospite)   
- ACPI / PNP: Avoid conflicting resource reservations (Rafael J. Wysocki)   
- ACPI / PM: Add missing pm_generic_complete() invocation (Rafael J. Wysocki)   
- ACPI / init: Switch over platform to the ACPI mode later (Rafael J. Wysocki)   
- ALSA: hda - Add a fixup for Dell E7450 (Takashi Iwai)   
- ALSA: hda - Fix the dock headphone output on Fujitsu Lifebook E780 (Takashi Iwai)   
- ALSA: hda - Add headset support to Acer Aspire V5 (Takashi Iwai)   
- ALSA: hda - restore the MIC FIXUP for some Dell machines (Hui Wang)   
- ALSA: hda - Disable widget power-save for VIA codecs (Takashi Iwai)   
- ALSA: hda - set proper caps for newer AMD hda audio in KB/KV (Alex Deucher)   
- ALSA: hda - Fix Dock Headphone on Thinkpad X250 seen as a Line Out (David Henningsson)   
- ALSA: pcm: Fix pcm_class sysfs output (Takashi Iwai)   
- Disable write buffering on Toshiba ToPIC95 (Ryan Underwood)   
- ipr: Increase default adapter init stage change timeout (Brian King)   
- rcu: Correctly handle non-empty Tiny RCU callback list with none ready (Paul E. McKenney)   
- gpio: rcar: Check for irq_set_irq_wake() failures (Geert Uytterhoeven)   
- gpio: crystalcove: set IRQCHIP_SKIP_SET_WAKE for the irqchip (Aaron Lu)   
- mnt: Modify fs_fully_visible to deal with locked ro nodev and atime (Eric W. Biederman)   
- mnt: Refactor the logic for mounting sysfs and proc in a user namespace (Eric W. Biederman)   
- mnt: Update fs_fully_visible to test for permanently empty directories (Eric W. Biederman)   
- sysfs: Create mountpoints with sysfs_create_mount_point (Eric W. Biederman)   
- sysfs: Add support for permanently empty directories to serve as mount points. (Eric W. Biederman)   
- kernfs: Add support for always empty directories. (Eric W. Biederman)   
- proc: Allow creating permanently empty directories that serve as mount points (Eric W. Biederman)   
- sysctl: Allow creating permanently empty directories that serve as mountpoints. (Eric W. Biederman)   
- fs: Add helper functions for permanently empty directories. (Eric W. Biederman)   
- Linux 4.1.2 (Greg Kroah-Hartman)   
- fs/ufs: restore s_lock mutex_init() (Fabian Frederick)   
- ufs: Fix possible deadlock when looking up directories (Jan Kara)   
- ufs: Fix warning from unlock_new_inode() (Jan Kara)   
- vfs: Ignore unlocked mounts in fs_fully_visible (Eric W. Biederman)   
- vfs: Remove incorrect debugging WARN in prepend_path (Eric W. Biederman)   
- fs/ufs: restore s_lock mutex (Fabian Frederick)   
- fs/ufs: revert "ufs: fix deadlocks introduced by sb mutex merge" (Fabian Frederick)   
- fs: Fix S_NOSEC handling (Jan Kara)   
- KVM: x86: make vapics_in_nmi_mode atomic (Radim Krčmář)   
- KVM: x86: properly restore LVT0 (Radim Krčmář)   
- KVM: arm/arm64: vgic: Avoid injecting reserved IRQ numbers (Marc Zyngier)   
- KVM: s390: virtio-ccw: don't overwrite config space values (Cornelia Huck)   
- s390/kdump: fix REGSET_VX_LOW vector register ELF notes (Michael Holzheu)   
- s390/bpf: Fix backward jumps (Michael Holzheu)   
- KVM: s390: clear floating interrupt bitmap and parameters (Jens Freimann)   
- KVM: s390: fix external call injection without sigp interpretation (David Hildenbrand)   
- MIPS: Fix KVM guest fixmap address (James Hogan)   
- KVM: mips: use id_to_memslot correctly (Paolo Bonzini)   
- x86/PCI: Use host bridge _CRS info on Foxconn K8M890-8237A (Bjorn Helgaas)   
- x86/PCI: Use host bridge _CRS info on systems with >32 bit addressing (Bjorn Helgaas)   
- powerpc/perf: Fix book3s kernel to userspace backtraces (Anton Blanchard)   
- tick/idle/powerpc: Do not register idle states with CPUIDLE_FLAG_TIMER_STOP set in periodic mode (preeti)   
- ARM: mvebu: fix suspend to RAM on big-endian configurations (Thomas Petazzoni)   
- ARM: tegra20: Store CPU "resettable" status in IRAM (Dmitry Osipenko)   
- ARM: kvm: psci: fix handling of unimplemented functions (Lorenzo Pieralisi)   
- arm: KVM: force execution of HCPTR access on VM exit (Marc Zyngier)   
- selinux: fix setting of security labels on NFS (J. Bruce Fields)   
- intel_pstate: set BYT MSR with wrmsrl_on_cpu() (Joe Konno)   
- mmc: sdhci: fix low memory corruption (Jiri Slaby)   
- iommu/amd: Handle large pages correctly in free_pagetable (Joerg Roedel)   
- iommu/arm-smmu: Fix broken ATOS check (Will Deacon)   
- Revert "crypto: talitos - convert to use be16_add_cpu()" (Horia Geant?)   
- crypto: talitos - avoid memleak in talitos_alg_alloc() (Horia Geant?)   
- usb: gadget: f_fs: add extra check before unregister_gadget_item (Rui Miguel Silva)   
- net: mvneta: disable IP checksum with jumbo frames for Armada 370 (Simon Guinot)   
- ARM: mvebu: update Ethernet compatible string for Armada XP (Simon Guinot)   
- net: mvneta: introduce compatible string "marvell, armada-xp-neta" (Simon Guinot)   
- amd-xgbe: Add the __GFP_NOWARN flag to Rx buffer allocation (Tom Lendacky)   
- sctp: Fix race between OOTB responce and route removal (Alexander Sverdlin)   
- bnx2x: fix lockdep splat (Eric Dumazet)   
- net: phy: fix phy link up when limiting speed via device tree (Mugunthan V N)   
- mlx4: Disable HA for SRIOV PF RoCE devices (Or Gerlitz)   
- net/mlx4_en: Fix wrong csum complete report when rxvlan offload is disabled (Ido Shamay)   
- net/mlx4_en: Wake TX queues only when there's enough room (Ido Shamay)   
- net/mlx4_en: Release TX QP when destroying TX ring (Eran Ben Elisha)   
- ip: report the original address of ICMP messages (Julian Anastasov)   
- xen-netback: fix a BUG() during initialization (Palik, Imre)   
- tcp: Do not call tcp_fastopen_reset_cipher from interrupt context (Christoph Paasch)   
- mvneta: add forgotten initialization of autonegotiation bits (Stas Sergeev)   
- mac80211: fix locking in update_vlan_tailroom_need_count() (Johannes Berg)   
- neigh: do not modify unlinked entries (Julian Anastasov)   
- packet: avoid out of bounds read in round robin fanout (Willem de Bruijn)   
- packet: read num_members once in packet_rcv_fanout() (Eric Dumazet)   
- bridge: fix br_stp_set_bridge_priority race conditions (Nikolay Aleksandrov)   
- sctp: fix ASCONF list handling (Marcelo Ricardo Leitner)   
- can: fix loss of CAN frames in raw_rcv (Oliver Hartkopp)   
- KVM: nSVM: Check for NRIPS support before updating control field (Bandan Das)   
- ARM: clk-imx6q: refine sata's parent (Sebastien Szymanski)   
- ARM: dts: sunxi: Adjust touchscreen compatible for sun5i and later (Hans de Goede)   
- Linux 4.1.1 (Greg Kroah-Hartman)   
- cdc-acm: Add support of ATOL FPrint fiscal printers (Alexey Sokolov)   
- b43: fix support for 14e4:4321 PCI dev with BCM4321 chipset (Rafał Miłecki)   
- ath3k: add support of 13d3:3474 AR3012 device (Dmitry Tunin)   
- ath3k: Add support of 0489:e076 AR3012 device (Dmitry Tunin)   
- Bluetooth: ath3k: Add support of 04ca:300d AR3012 device (Dmitry Tunin)   
- perf tools: Fix build breakage if prefix= is specified (Lukas Wunner)   
- perf/x86: Honor the architectural performance monitoring version (Palik, Imre)   
- perf/x86/intel/bts: Fix DS area sharing with x86_pmu events (Alexander Shishkin)   
- perf/x86: Add more Broadwell model numbers (Andi Kleen)   
- perf: Fix ring_buffer_attach() RCU sync, again (Oleg Nesterov)   
- x86/boot: Fix overflow warning with 32-bit binutils (Borislav Petkov)   

* Wed Jul 29 2015 Santosh Shilimkar <santosh.shilimkar@oracle.com> [4.1.0-1.el7uek] 
- block: loop: Enable directIO on nfs (Dave Kleikamp)   
- block: loop: Enable directIO whenever possible (Dave Kleikamp)   
- uek-rpm: configs: enable compilation for RDS (Ajaykumar Hotchandani)   
- uek-rpm: enable mlx4_vnic module config (Qing Huang)   
- Add getsockopt support for SO_RDS_TRANSPORT (Sowmini Varadhan)  [Orabug: 21061146]  
- Add setsockopt support for SO_RDS_TRANSPORT (Sowmini Varadhan)  [Orabug: 21061146]  
- Declare SO_RDS_TRANSPORT and RDS_TRANS_* constants in uapi/linux/rds.h (Sowmini Varadhan)  [Orabug: 21061146]  
- RDS-TCP: only initiate reconnect attempt on outgoing TCP socket. (Sowmini Varadhan)  [Orabug: 20930687]  
- RDS-TCP: Always create a new rds_sock for an incoming connection. (Sowmini Varadhan)  [Orabug: 20930687]  
- rds: directly include header for vmalloc/vfree in ib_recv.c (Mukesh Kacker)  [Orabug: 21059667]  
- rds: return EMSGSIZE for oversize requests before processing/queueing (Mukesh Kacker)  [Orabug: 20971222]  
- net: rds: use correct size for max unacked packets and bytes (Sasha Levin)  [Orabug: 20585918]  
- RDS/IP: RDS takes 10 seconds to plumb the second IP back (Mukesh Kacker)  [Orabug: 20231857]  
- RDS/IB: Tune failover-on-reboot scheduling (Mukesh Kacker)  [Orabug: 20063740]  
- RDS: mark netdev UP for intfs added post module load (Mukesh Kacker)  [Orabug: 20130536]  
- RDS: Enable use of user named pkey devices (Mukesh Kacker)  [Orabug: 19064704]  
- rds: fix list corruption and tx hang when netfilter is used (shamir rabinovitch)  [Orabug: 18963548]  
- RDS: move more queing for loopback connections to separate queue (Mukesh Kacker)  [Orabug: 18977932]  
- RDS: add module parameter to allow module unload or not (Wengang Wang)   
- rds: fix NULL pointer dereference panic during rds module unload (Rama Nichanamatlu)  [Orabug: 18952475]  
- RDS:active bonding: disable failover across HCAs(failover groups) (Mukesh Kacker)  [Orabug: 19430773]  
- RDS/IB: active bonding - failover down interfaces on reboot. (Mukesh Kacker)  [Orabug: 18697678]  
- RDS/IB: Remove dangling rcu_read_unlock() and other cleanups (Mukesh Kacker)  [Orabug: 18995395]  
- rds: new extension header: rdma bytes (Shamir Rabinovitch)  [Orabug: 18468180]  
- RDS: Ensure non-zero SL uses correct path before lane 0 connection is dropped (Ajaykumar Hotchandani)  [Orabug: 19133664]  
- rds: Lost locking in loop connection freeing (Pavel Emelyanov)  [Orabug: 19265200]  
- RDS: active bonding - failover/failback only to matching pkey (Mukesh Kacker)  [Orabug: 18681364]  
- RDS: active bonding - ports may not failback if all ports go down (Mukesh Kacker)  [Orabug: 18875563]  
- RDS: Use rds_local_wq for loopback connections in rds_conn_connect_if_down() (Chien-Hua Yen)  [Orabug: 18892380]  
- RDS: add workqueue for local loopback connections (Chien-Hua Yen)  [Orabug: 18892366]  
- RDS: SA query optimization (Bang Nguyen)  [Orabug: 18801977]  
- RDS: Remove cond_resched() in RX tasklet (Bang Nguyen)  [Orabug: 18801937]  
- RDS: Replace queue_work() by cond_resched() in the tasklet to breakup RX stream (Bang Nguyen)  [Orabug: 18801931]  
- RDS: looping to reap cq recv queue in rds_conn_shutdown (Chien-Hua Yen)  [Orabug: 18501034]  
- rds: Fix regression in dynamic active bonding configuration (Bang Nguyen)   
- rds/rdma_cm: send RDMA_CM_EVENT_ADDR_CHANGE event for active bonding (Bang Nguyen)  [Orabug: 18421516]  
- RDS: Idle QoS connections during remote peer reboot causing application brownout (Chien-Hua Yen)  [Orabug: 18443194]  
- rds: dynamic active bonding configuration (Bang Nguyen)   
- RDS: Fix slowdown when doing massively parallel workload (Bang Nguyen)  [Orabug: 18362838]  
- RDS: active bonding needs to set brcast and mask for its primary interface (Chien-Hua Yen)  [Orabug: 18479088]  
- RDS: bind hash table size increase, add per-bucket rw lock (Bang Nguyen)  [Orabug: 18071861]  
- RDMA CM: Add reason code for IB_CM_REJ_CONSUMER_DEFINED (Bang Nguyen)  [Orabug: 17484682]  
- RDS: protocol negotiation fails during reconnect (Bang Nguyen)  [Orabug: 17375389]  
- RDS: double free rdma_cm_id (Bang Nguyen)  [Orabug: 17192816]  
- RDS: ActiveBonding IP exclusion filter (Bang Nguyen)  [Orabug: 17075950]  
- RDS: Reconnect stalls for 15s (Bang Nguyen)  [Orabug: 17277974]  
- RDS: Reconnect causes panic at completion phase (Bang Nguyen)  [Orabug: 17213597]  
- RDS: added stats to track and display receive side memory usage (Venkat Venkatsubra)  [Orabug: 17045536]  
- RDS: RDS reconnect stalls (Bang Nguyen)  [Orabug: 1731355]  
- RDS: disable IP failover if device removed (Bang Nguyen)  [Orabug: 17206167]  
- RDS: Fix a bug in QoS protocol negotiation (Bang Nguyen)  [Orabug: 17079972]  
- RDS: alias failover is not working properly (Bang Nguyen)  [Orabug: 17177994]  
- add NETFILTER suppport (Ahmed Abbas)  [Orabug: 17082619]  
- RDS: Local address resolution may be delayed after IP has moved. RDS to update local ARP cache directly to speed it up. (Bang Nguyen)  [Orabug: 16979994]  
- RDS: restore two-sided reconnect with the lower IP node having a constant 100 ms backoff. (Bang Nguyen)  [Orabug: 16710287]  
- rds: set correct msg_namelen (Weiping Pan)   {CVE-2012-3430} 
- RDS: IP config needs to be updated when network/rdma service restarted. (Bang Nguyen)  [Orabug: 16963884]  
- RDS: check for valid rdma id before initiating connection (Bang Nguyen)  [Orabug: 16857341]  
- RDS: reduce slab memory usage (Bang Nguyen)  [Orabug: 16935507]  
- RDS: Move connection along with IP when failing over/back. (Bang Nguyen)  [Orabug: 16916648]  
- RDS: Rename HAIP parameters to Active Bonding (Bang Nguyen)  [Orabug: 16810395]  
- rds shouldn't release fmr when ib_device was already released. (Zheng Li)  [Orabug: 16605377]  
- rds remove dev race. (Zheng Li)  [Orabug: 16605377]  
- reinit ip_config when service rdma restart. (Zheng Li)  [Orabug: 16605377]  
- rds: limit the size allocated by rds_message_alloc() (Cong Wang)  [Orabug: 16837486]  
- RDS: Fixes to improve throughput performance (Bang Nguyen)  [Orabug: 16571410]  
- RDS: fix rds-ping spinlock recursion (jeff.liu)  [Orabug: 16223050]  
- rds: Congestion flag does not get cleared causing the connection to hang (Bang Nguyen)  [Orabug: 16424692]  
- Add SIOCRDSGETTOS to get the current TOS for the socket (Bang Nguyen)  [Orabug: 16397197]  
- Changes to connect/TOS interface (Bang Nguyen)  [Orabug: 16397197]  
- rds: this resolved crash while removing rds_rdma module. orabug: 16268201 (Bang Nguyen)   
- rds: scheduling while atomic on failover orabug: 16275095 (Bang Nguyen)   
- rds: unregister IB event handler on shutdown (Bang Nguyen)   
- rds: HAIP support child interface (Bang Nguyen)   
- RDS HAIP misc fixes (Bang Nguyen)   
- Ignore failover groups if HAIP is disabled (Bang Nguyen)   
- RDS: RDS rolling upgrade (Saeed Mahameed)   
- RDS: Fixes warning while rds-info. spin_lock_irqsave() is changed to spin_lock_bh(). (Ajaykumar Hotchandani)   
- rds: UNDO reverts done for rebase code to compile with Linux 4.1 APIs (Mukesh Kacker)   
- rds: port to UEK4, Linux-3.18* (Ajaykumar Hotchandani)   
- rds: disable APM support (Ajaykumar Hotchandani)   
- rds: disable cq balance (Ajaykumar Hotchandani)   
- rds: move linux/rds.h to uapi/linux/rds.h (Ajaykumar Hotchandani)   
- RDS: Kconfig and Makefile changes (Ajaykumar Hotchandani)   
- RDS merge for UEK2 (Bang Nguyen)  [Orabug: 15997083]  
- rds: Misc Async Send fixes (Bang Nguyen)   
- rds: call unregister_netdevice_notifier for rds_ib_nb in rds_ib_exit (Saeed Mahameed)   
- rds: flush and destroy workqueue rds_aux_wq and fix creation order. (Saeed Mahameed)   
- rds : fix compilation warning (Saeed Mahameed)   
- rds: port the code to uek2 (Dotan Barak)   
- rds: CQ balance (Bang Nguyen)   
- rds: HAIP across HCAs (Bang Nguyen)   
- rds: Misc HAIP fixes (Bang Nguyen)   
- rds: off by one fixes (Dotan Barak)   
- rds: Add Automatic Path Migration support (Dotan Barak)   
- IB/ipoib: CSUM support in connected mode (Yuval Shaia)  [Orabug: 20559068]  
- IB/ipoib: Scatter-Gather support in connected mode (Yuval Shaia)  [Orabug: 20422840]  
- ib_uverbs: Support for kernel implementation of XRC calls from user space (Knut Omang)  [Orabug: 20930262]  
- ib_{uverbs/core}: add new ib_create_qp_ex with udata arg (Knut Omang)  [Orabug: 20930262]  
- ib_uverbs: Avoid vendor specific masking of attributes in query_qp (Knut Omang)  [Orabug: 20930262]  
- ib_uverbs: Add padding to end align ib_uverbs_reg_mr_resp (Knut Omang)  [Orabug: 20930262]  
- ib: Add udata argument to create_ah (Knut Omang)  [Orabug: 20930262]  
- ib_umem: Add a new, more generic ib_umem_get_attrs (Knut Omang)  [Orabug: 20930262]  
- ib_mad: incoming sminfo SMPs gets discarded if no process_mad function is registered (Dag Moxnes)  [Orabug: 20930262]  
- mlx4_core: More support for automatically scaling profile parameters (Mukesh Kacker)   
- ipoib: rfe- enable pkey and device name decoupling (Mukesh Kacker)  [Orabug: 19064704]  
- ib_sdp: adding sdp socket support to rdma_cm (Qing Huang)   
- rds: fix error flow handling (Dotan Barak)   
- net/rds: prevent memory leak in case of error flow (Dotan Barak)   
- rds: prepare support to kernel 2.6.39-200.1.1.el5uek: add the macro NIPQUAD_* (Dotan Barak)   
- rds: fixed wrong condition in case of error (Dotan Barak)   
- rds: fixed kernel oops in case of error flow (Dotan Barak)   
- RDS: fixed compilation warnings (Dotan Barak)   
- RDS SRQ optional (Bang Nguyen)   
- RDS Async send support revised (Bang Nguyen)   
- RDS Asynchronous Send support (Bang Nguyen)   
- rds: fix compilation warnings (Dotan Barak)   
- RDS: cleanup checkpatch errors (Bang Nguyen)   
- RDS Quality Of Service (Bang Nguyen)   
- RDS: Use IB_CQ_NEXT_COMP instead of IB_CQ_SOLICITED for TX CQ (Bang Nguyen)   
- RDS: make sure rds_send_xmit doesn't loop forever (Chris Mason)   
- RDS: issue warning if re-connect stalling for more than 1 min. (Bang Nguyen)   
- RDS: don't test ring_empty or ring_low without locks held (Chris Mason)   
- RDS: don't use RCU for the bind hash table (Chris Mason)   
- RDS: avoid double destory of cm_id when rdms_resolve_route fails (Venkat Venkatsubra)   
- RDS: make sure rds_send_drop_to properly takes the m_rs_lock (Chris Mason)   
- RDS: kick krdsd to send congestion map updates (Chris Mason)   
- RDS: add debuging code around sock_hold and sock_put. (Chris Mason)   
- RDS: Don't destroy the rdma id until after we're dong using it (Chris Mason)   
- RDS: adjust BUG()s for irqs disabled. (Chris Mason)   
- rds: make sure we don't deref a null cm_id->device during address checks (Chris Mason)   
- RDS: don't use GFP_ATOMIC for sk_alloc in rds_create (Chris Mason)   
- RDS: Make sure we do a signaled send at least once per large send (Chris Mason)   
- RDS: Fix an rcu race with rds_bin_lookup (Tina Yang)   
- RDS: Fix RDS_MSG_MAPPED usage. (Chris Mason)   
- RDS: add a sock_destruct callback with debugging (Chris Mason)   
- RDS: add a sock_destruct callback with debugging (Tina Yang)   
- RDS: limit the number of times we loop in rds_send_xmit (Chris Mason)   
- RDS Make sure we check for congestion updates during rds_send_xmit (Chris Mason)   
- Make sure to kick rds_send_xmit for both LL_SEND_FULL and for the congestion map updates. (Chris Mason)   
- RDS: make sure we post recv buffers (Chris Mason)   
- RDS: don't trust the LL_SEND_FULL bit (Chris Mason)   
- RDS: give up on half formed connections after 15s (Chris Mason)   
- rds_send_xmit is called uner a spinlock, lets not do a cond_resched() (Chris Mason)   
- RDS: make sure not to loop forever inside rds_send_xmit (Chris Mason)   
- rds: check for excessive looping in rds_send_xmit (Andy Grover)   
- rds: don't update ipaddress tables if the address hasn't changed (Chris Mason)   
- change ib default retry to 1 (Andy Grover)   
- This patch adds the modparam to rds.ko. (Andy Grover)   
- RDS: only use passive connections when addresses match (Zach Brown)   
- RDS: destroy the ib state that generates call back earlier during shutdown (Chris Mason)   
- RDS: check access on pages before doing copy_to_user (Chris Mason)   
- RDS/IB: always free recv frag as we free its ring entry (Zach Brown)   
- RDS/IB: Quiet warnings when leaking frags (Andy Grover)   
- Fix loopback connection reference counts (Zach Brown)   
- RDS: cancel connection work structs as we shut down (Zach Brown)   
- RDS: don't call rds_conn_shutdown() from rds_conn_destroy() (Zach Brown)   
- RDS: have sockets get transport module references (Zach Brown)   
- RDS: remove old rs_transport comment (Zach Brown)   
- RDS: lock rds_conn_count decrement in rds_conn_destroy() (Zach Brown)   
- Use CQ_NEXT_COMP for recv completions (Andy Grover)   
- RDS/IB: protect the list of IB devices (Zach Brown)   
- RDS/IB: print IB event strings as well as their number (Zach Brown)   
- RDS: flush the FMR pool less often. (Chris Mason)   
- RDS: make sure the ring is really full before we return with ENOMEM (Chris Mason)   
- RDS: use different cq handlers for send and recv (Andy Grover)   
- RDS/IB: track signaled sends (Zach Brown)   
- RDS: remove __init and __exit annotation (Zach Brown)   
- RDS: fix races and other problems with rmmod and device removal (Zach Brown)   
- RDS: properly init the sg table in our frags (Chris Mason)   
- RDS: add support for atomic messages over the wire (Andy Grover)   
- rds: fix compilation warnings (Dotan Barak)   
- Fix backports for rds (Eli Cohen)   
- RDS: Fix BUG_ONs to not fire when in a tasklet (Andy Grover)   
- RDS: Enable per-cpu workqueue threads (Tina Yang)   
- RDS: Do not call set_page_dirty() with irqs off (Andy Grover)   
- RDS: Properly unmap when getting a remote access error (Sherman Pun)   
- RDS: only put sockets that have seen congestion on the poll_waitq (Andy Grover)   
- RDS: Fix locking in rds_send_drop_to() (Tina Yang)   
- RDS: Turn down alarming reconnect messages (Andy Grover)   
- RDS: Workaround for in-use MRs on close causing crash (Andy Grover)   
- RDS: Fix send locking issue (Tina Yang)   
- RDS: Fix congestion issues for loopback (Andy Grover)   
- RDS/TCP: Wait to wake thread when write space available (Andy Grover)   
- RDS: use IB_CQ_VECTOR_LEAST_ATTACHED for cq's (Andy Grover)   
- RDS: update copy_to_user state in tcp transport (Andy Grover)   
- RDS: sendmsg() should check sndtimeo, not rcvtimeo (Andy Grover)   
- RDS: Do not BUG() on error returned from ib_post_send (Andy Grover)   
- RDS: Re-add pf/sol access via sysctl (Andy Grover)   
- RDS/IB+IW: Move recv processing to a tasklet (Andy Grover)   
- RDS: Do not send congestion updates to loopback connections (Andy Grover)   
- RDS: Fix panic on unload (Andy Grover)   
- RDS: Fix potential race around rds_i[bw]_allocation (Andy Grover)   
- RDS: Add GET_MR_FOR_DEST sockopt (Andy Grover)   
- RDS: Add a debug message suggesting to load transport modules (Andy Grover)   
- RDS: Track transports via an array, not a list (Andy Grover)   
- RDS: Modularize RDMA and TCP transports (Andy Grover)   
- RDS: Export symbols from core RDS (Andy Grover)   
- RDS: Re-add TCP transport to RDS (Andy Grover)   
- RDS/IB: Drop connection when a fatal QP event is received (Andy Grover)   
- RDS/IB: Disable flow control in sysctl and explain why (Andy Grover)   
- RDS/IB: Move tx/rx ring init and refill to later (Andy Grover)   
- RDS: Don't set c_version in __rds_conn_create() (Andy Grover)   
- RDS/IB: Rename byte_len to data_len to enhance readability (Andy Grover)   
- RDS/RDMA: Fix cut-n-paste errors in printks in rdma_transport.c (Andy Grover)   
- RDS/IB: Fix printk to indicate remote IP, not local (Andy Grover)   
- RDS/IB: Handle connections using RDS 3.0 wire protocol (Andy Grover)   
- RDS/IB: Improve RDS protocol version checking (Andy Grover)   
- RDS: Set retry_count to 2 and make modifiable via modparam (Andy Grover)   
- RDS: Refactor end of __conn_create for readability (Andy Grover)   
- RDS/IW: Remove dead code (Andy Grover)   
- RDS/IW: Remove page_shift variable from iwarp transport (Andy Grover)   
- RDS/IB: Always use PAGE_SIZE for FMR page size (Andy Grover)   
- RDS: Fix completion notifications on blocking sockets (Andy Grover)   
- FRV: Fix the section attribute on UP DECLARE_PER_CPU() (David Howells)   
- rds: revert RDS code to 8cbd960 commit to rebase UEK commits (Mukesh Kacker)   
- mlx4_vnic: set mod param "lro_num" default value to 0 to disable LRO feature (Qing Huang)   
- mlx4_vnic: Add correct typecasting to pointers in vnic_get_frag_header() (Ashish Samant)  [Orabug: 19824501]  
- rdma_cm: CMA_QUERY_HANDLER: BAD STATUS -110 and -22 (Chien-Hua Yen)  [Orabug: 16708786]  
- RDMA CM: Avoid possible SEGV during connection shutdown (Bang Nguyen)  [Orabug: 16750726]  
- rdma_cm: extend debug for remote mapping (Ajaykumar Hotchandani)   
- mlx4_core: supporting 64b counters (Vu Pham)  [Orabug: 21094165]  
- ib_core: supporting 64b counters using PMA_COUNTERS_EXT mad (Vu Pham)  [Orabug: 21094165]  
- net/mlx4: When issuing commands use rwsem insteam of rw spinlocks (Matan Barak)   
- mlx4_ib: Make sure that PSN does not overflow. (Majd Dibbiny)   
- ib_core: Make sure that PSN does not overflow. (Majd Dibbiny)   
- IB/CMA: Make sure that PSN is not over max allowed (Moni Shoua)   
- IB/mlx4: Mark user mr as writable if actual virtual memory is writable (Moshe Lazer)   
- mlx4_ib: Report proper BDF for IB MSI-X vectors (Yevgeny Petrilin)   
- IB/core: Fix memory leak in cm_req_handler error flows (Matan Barak)   
- mlx4_core: enable msi_x module parameter for SRIOV VFs to limit number MSI-X interrupts per VF (Tal Alon)   
- mlx4_ib: Fix endianness in blueflame post_send. (Jack Morgenstein)   
- net/mlx4: Switching between sending commands via polling and events may results in hung tasks (Matan Barak)   
- IB/mlx4: Put non zero value in max_ah (Eli Cohen)   
- IB/core: Add debugging prints to ib_uverbs_write (Haggai Eran)   
- IB/core: add debugging prints to explain -EINVAL in ib_uverbs_reg_mr (Majd Dibbiny)   
- fix warning about bitwise or between u32 and size_t (Haggai Eran)   
- IB/mlx4: Don't update QP1 for native functions (Matan Barak)   
- IB/ipoib: Check gso size prior to ib_send (Erez Shitrit)   
- mlx4_vnic: fix may be used uninitialized compilation warnings (Saeed Mahameed)   
- mlx4_vnic: fix potential data corruption in sprintf (Saeed Mahameed)   
- mlx4_core: Fix resource tracker memory leak after Reset Flow (Hadar Hen Zion)   
- IB/mlx4: Check port_num before using it in mlx4_ib_port_link_layer (Moshe Lazer)   
- IB/mlx4: Fix wrong calculation of link layer (Moni Shoua)   
- IB/mlx4: Copy SL from correct place in address path (Shani Michaelli)   
- mlx4_core: Check return status of rdma_resolve_ip (Shani Michaelli)   
- mlx4: Clean IRQ affinity hint when freeing it (Ido Shamay)   
- IB/core: Fix QP attr mask when resolving smac (Moni Shoua)   
- mlx4_vnic: fix typo in log messages (Saeed Mahameed)   
- mlx4_vnic: print vnic keep alive info in mlx4_vnic_info (Saeed Mahameed)   
- IB/mlx4: default gid should respect dev_id (Matan Barak)   
- mlx4_core: Change the name of the num_mtt in mlx4_profile to be num_mtt_segs. (Majd Dibbiny)   
- IB/mlx4: Print error messages when GID table update failed (Moni Shoua)   
- IB/mlx4: Remove unnecessary warning message (Moni Shoua)   
- ib_core: Check that caches exist before accessing them (Jack Morgenstein)   
- rdma_cm/cma: Cache broadcast domain record. (Erez Shitrit)   
- ipoib: added an error message when trying to change mtu to 2K-4K (Noa Osherovich)   
- ib_core: Do not transition MC groups to error on SM_CHANGE event (Jack Morgenstein)   
- ipoib: Do not flush mcast groups on SM_CHANGE event (Jack Morgenstein)   
- rdma_cm: add debug functions and module parameter (Saeed Mahameed)   
- rdma_cm: garbage-collection thread for rdma_destroy_id() (Saeed Mahameed)   
- mlx4_vnic: always remove child macs in vnic_parent_update remove request (Saeed Mahameed)   
- mlx4_vnic: set default moderation values in vnic_alloc_netdev (Saeed Mahameed)   
- mlx4: Handle memory region deregistration failure (Shani Michaeli)   
- ib_core: More fixes to ib_sa_add_one error flow (Jack Morgenstein)   
- IB/ipoib: Set mode only when needed. (Erez Shitrit)   
- mlx4_core: Use div_u64 to avoid unresolved symbol on 32-bit OSes (Vladimir Sokolovsky)   
- ib_core: Safely unregister mad agent when necessary. (Majd Dibbiny)   
- mlx4_vnic: use netif_set_real_num_tx_queues to dynamically change tx queue size (Saeed Mahameed)   
- mlx4_core: Extend num_mtt in dev caps to avoid overflow. (Majd Dibbiny)   
- mlx4_core: fix FMR unmapping to allow remapping afterward (Moshe Lazer)   
- ib/ipoib: unlock dev_start_xmit() on ipoib_cm_rep_handler() (Tal Alon)   
- ib_core: fixed resource leak in case of error (Saeed Mahameed)   
- ib/ipoib: fix illegal locking on ipoib_cm_rep_handler (Tal Alon)   
- ib/ipoib: ipoib_cm_rep_handler lock skb queue while dequeue before xmit (Tal Alon)   
- mlx4_core: resolvs kernel panic when connectx_port_config fail to set ports (Moshe Lazer)   
- mlx4_core: Avoid setting ports for auto when only one port type is supported (Moshe Lazer)   
- mlx4_core: sysfs, fix usage of log_num_mtt module parameter (Yishai Hadas)   
- mlx4_core: fix ib_uverbs_get_context flow (Yishai Hadas)   
- mlx4_core: Fix Coverity issues. (Hadar Hen Zion)   
- IB/mlx4: Fix Coverity issues (Hadar Hen Zion)   
- IB/core: Fix Coverity issues for rdma_cm (Hadar Hen Zion)   
- Release Date is updated to __DATE__ instead of a static string (Alex Markuze)   
- mlx4_core: use msi_x module param to limit num of MSI-X irqs (Moshe Lazer)   
- Seting ring size to default when module param set incorrectly (Alex Markuze)   
- ib/core: change error prints in cm module to debug prints. (Jack Morgenstein)   
- mlx4_core: Add more info to mlx4_cmd_post failure error messages (Jack Morgenstein)   
- mlx4_core: disable mlx4_QP_ATTACH calls from guests if master is doing flow steering. (Jack Morgenstein)   
- mlx4_core: change resource quotas to enable supporting upstream-kernel guests (Jack Morgenstein)   
- mlx4_core: device revision support (Yishai Hadas)   
- mlx4_core: print more info when command times out (Jack Morgenstein)   
- mlx4_core: move out label to the right place (Eugenia Emantayev)   
- IB/mlx4: deprecate "failed to alloc bf reg" message from err to debug (Jack Morgenstein)   
- mlx4_core: Do not allow mlx4_bitmap_init to reserve more slots than available (Amir Vadai)   
- ib/ipoib: Fix deadlock between rmmod and set_mode (Erez Shitrit)   
- ib/ipoib: getout whenever failed to load port. (Erez Shitrit)   
- ib_ipoib: Fixing issue with delayed work running after child is killed. (Erez Shitrit)   
- mlx4_core: set device to use extended counters (Yishai Hadas)   
- ib/ipoib: debug prints instead of warn in tx_wc function (Erez Shitrit)   
- ib/ipoib: add detailed error message on dev_queue_xmit (Erez Shitrit)   
- ib/ipoib: Fix removing call for update_pmtu from spin-lock context. (Erez Shitrit)   
- ipoib: fixed NULL dereferencing in case of error flow (Dotan Barak)   
- mlx4_core: Update minimum size for log_num_qp to 18 (Moshe Lazer)   
- mlx4_core, mlx4_ib: Have enough room in steering range for pkey interfaces (Amir Vadai)   
- net/mlx4: return bad error status to caller function in case of error (Dotan Barak)   
- ib/core: Remove annoying message. (Erez Shitrit)   
- mlx4_ib: fix memory leak if QP creation failed (Dotan Barak)   
- ib/core: add prints to the cm module. (Erez Shitrit)   
- mlx4/IB: add a message print when the logical link goes up/down (Dotan Barak)   
- mlx4/ib: clean memory for EQs in case of error flow (Dotan Barak)   
- net/mlx4_core: set used number of MTTs when using auto-detection (Dotan Barak)   
- net/mlx4_core: the number of MTTs should consider log_mtts_per_seg (Dotan Barak)   
- net/mlx4_core: limit to 4TB of memory registration (Yishai Hadas)   
- net/mlx4_core: num mtt issues (Yishai Hadas)   
- mlx4_vnic: Kconfig and Makefile changes (Qing Huang)   
- mlx4_vnic: add mlx4_vnic (Saeed Mahameed)   
- mlx4_ib: add blue flame support for kernel consumers (Eli Cohen)   
- net/mlx4_core: add sanity check when creating bitmap structure (Dotan Barak)   
- net/mlx4_core: unmap clear register in case of error flow (Dotan Barak)   
- ib_core: fix NULL pointer dereference (Dotan Barak)   
- mlx4_ib: contig support for control objects (Yishai Hadas)   
- mlx4_core: fix wrong comment about the reason of subtract one from the max_cqes (Dotan Barak)   
- IB/core - Don't modify outgoing DR SMP if first part is LID routed (Ralph Campbell)   
- net/mlx4: adjust initial value of vl_cap in mlx4_SET_PORT (Or Gerlitz)   
- mlx4_core: Error message on mtt allocation failure (Marcel Apfelbaum)   
- IB/core: Control number of retries for SA to leave an MCG (Dotan Barak)   
- mlx4: reducing wait during SW reset for 500 msecs (Dotan Barak)   
- mlx4_ib: Do not enable blueflame sends if write combining is not available (Jack Morgenstein)   
- IB/core: Fix create_qp issue relates to qp group type (Yishai Hadas)   
- mlx4_core: log_num_mtt handling (Yishai Hadas)   
- mlx4_ib: Fix the SQ size of an RC QP to support masked atomic operation (Dotan Barak)   
- mlx4_ib: Use optimal numbers of MTT entries. (Yishai Hadas)   
- mlx4_ib: set write-combining flag for userspace blueflame pages (Dotan Barak)   
- mlx4_core: limit min profile numbers (Dotan Barak)   
- mlx4_core: allow to use 0 in log_mtts_per_seg (Dotan Barak)   
- mlx4_core: enable changing default max HCA resource limits. (Dotan Barak)   
- cma: add module parameter to the response timeout (Arlin Davis)   
- ocfs2: call ocfs2_journal_access_di() before ocfs2_journal_dirty() in ocfs2_write_end_nolock() (yangwenfang)   
- ocfs2: avoid access invalid address when read o2dlm debug messages (jiangyiwen)   
- ocfs2: make 'buffered' as the default coherency option (Wengang Wang)  [Orabug: 17988729]  
- xen/microcode: Use dummy microcode_ops for non initial domain guest (Zhenzhong Duan)  [Orabug: 19053626]  
- xen/microcode: Fix compile warning. (Konrad Rzeszutek Wilk)   
- microcode_xen: Add support for AMD family >= 15h (Ian Campbell)   
- x86/microcode: check proper return code. (Ben Guthro)   
- xen: add CPU microcode update driver (Jeremy Fitzhardinge)   
- x86/xen: Disable APIC PM for Xen PV guests (Boris Ostrovsky)   
- xen/pvhvm: Support more than 32 VCPUs when migrating (v3). (Konrad Rzeszutek Wilk)   
- cdc-acm: Increase number of devices to 64 (Joe Jin)  [Orabug: 21219170]  
- ipmi: make kcs timeout parameters as module options (Pavel Bures)  [Orabug: 21219155]  
- x86: perf: prevent spurious PMU NMIs on Haswell systems (Dan Duval)  [Orabug: 20996846]  
- x86/simplefb: simplefb was broken on Oracle and HP system, skip VIDEO_TYPE_EFI (Ethan Zhao)  [Orabug: 20961435]  
- x86, fpu: Avoid possible error in math_state_restore() (Annie Li)  [Orabug: 20270524]  
- kernel: freezer: restore TIF_FREEZE (Sasha Levin)   
- ksplice: Clear garbage data on the kernel stack when handling signals (Sasha Levin)   
- sched: Disable default sched_autogroup to avoid the DBA performance regression (Santosh Shilimkar)  [Orabug: 20476603]  
- x86: add support for crashkernel=auto (Brian Maly)  [Orabug: 20351819]  
- uek-rpm: configs: Enabel Oracle HXGE and ASM driver (Santosh Shilimkar)   
- uek-rpm: build: Add rpm build environment for ol6/ol7 (Santosh Shilimkar)  [Orabug: 20892775] [Orabug: 21102340] [Orabug: 20687425]  
- uek-rpm: configs: Create baseline config for uek4[ol6/ol7] (Santosh Shilimkar)  [Orabug: 20064118] [Orabug: 20343801] [Orabug: 20343138] [Orabug: 20064118] [Orabug: 20064118] [Orabug: 20064118] [Orabug: 20064118] [Orabug: 20473608] [Orabug: 20516347] [Orabug: 20611390] [Orabug: 21233074] [Orabug: 20687425]  
- oracleasm: Fix trace output for warn_asm_ioc and check_asm_ioc (Martin K. Petersen)   
- oracleasm: Fix occasional I/O stall due to merge error (Martin K. Petersen)   
- oracleasm: Classify device connectivity issues as global errors (Martin K. Petersen)  [Orabug: 20117903]  
- oracleasm: Deprecate mlog and implement support for tracepoints (Martin K. Petersen)   
- oracleasm: Abolish mlog usage in integrity.c and clean up error printing. (Martin K. Petersen)   
- oracleasm: Various code and whitespace cleanups. (Martin K. Petersen)   
- oracleasm: 4.0 compat changes (Martin K. Petersen)   
- oracleasm: Compat changes for 3.18 (Martin K. Petersen)   
- oracleasm: claim FMODE_EXCL access on disk during asm_open (Srinivas Eeda)  [Orabug: 19454829]  
- oracleasm: Restrict logical block size reporting (Martin K. Petersen)   
- oracleasm: Report logical block size (Martin K. Petersen)   
- oracleasm: Compat changes for 3.10 (Martin K. Petersen)   
- oracleasm: Add support for new error return codes from block/SCSI (Martin K. Petersen)  [Orabug: 17484923]  
- oracleasm: Compat changes for 3.8 (Martin K. Petersen)   
- oracleasm: Compat changes for 3.5 (Dwight Engen)   
- oracleasm: Introduce module parameter for block size selection (Martin K. Petersen)  [Orabug: 15924773]  
- oracleasm: Data integrity support (Martin K. Petersen)   
- oracleasm: Fix two merge errors (Martin K. Petersen)   
- Oracle ASM Kernel Driver (Martin K. Petersen)   
- block: loop: support DIO & AIO (Ming Lei)   
- block: loop: prepare for supporing direct IO (Ming Lei)   
- block: loop: use kthread_work (Ming Lei)   
- block: loop: set QUEUE_FLAG_NOMERGES for request queue of loop (Ming Lei)   
- fs: direct-io: don't dirtying pages for ITER_BVEC/ITER_KVEC direct read (Ming Lei)   
- nfs: don't dirty kernel pages read by direct-io (Dave Kleikamp)   
- block: loop: avoiding too many pending per work I/O (Ming Lei)   
- block: loop: convert to per-device workqueue (Santosh Shilimkar)   
- megaraid_sas: Permit large RAID0/1 requests (Martin K. Petersen)  [Orabug: 19625877]  
- megaraid_sas : Modify return value of megasas_issue_blocked_cmd() and wait_and_poll() to consider command status returned by firmware (Sumit.Saxena@avagotech.com)   
- megaraid_sas : swap whole register in megasas_register_aen (Christoph Hellwig)   
- megaraid_sas : fix megasas_fire_cmd_fusion calling convention (Christoph Hellwig)   
- megaraid_sas : add missing byte swaps to the sriov code (Christoph Hellwig)   
- megaraid_sas : bytewise or should be done on native endian variables (Christoph Hellwig)   
- megaraid_sas : move endianness conversion into caller of megasas_get_seq_num (Christoph Hellwig)   
- megaraid_sas : add endianness conversions for all ones (Christoph Hellwig)   
- megaraid_sas : add endianness annotations (Christoph Hellwig)   
- megaraid_sas : add missing __iomem annotations (Christoph Hellwig)   
- megaraid_sas : megasas_complete_outstanding_ioctls() can be static (kbuild test robot)   
- megaraid_sas : Support for Avago's Single server High Availability product (Sumit.Saxena@avagotech.com)   
- megaraid_sas : Add release date and update driver version (Sumit.Saxena@avagotech.com)   
- megaraid_sas : Modify driver's meta data to reflect Avago (Sumit.Saxena@avagotech.com)   
- megaraid_sas : Use Block layer tag support for internal command indexing (Sumit.Saxena@avagotech.com)   
- megaraid_sas : Enhanced few prints (Sumit.Saxena@avagotech.com)   
- megaraid_sas : Move controller's queue depth calculation in adapter specific function (Sumit.Saxena@avagotech.com)   
- megaraid_sas : Add separate functions for building sysPD IOs and non RW LDIOs (Sumit.Saxena@avagotech.com)   
- megaraid_sas : Add separate function for refiring MFI commands (Sumit.Saxena@avagotech.com)   
- megaraid_sas : Add separate function for setting up IRQs (Sumit.Saxena@avagotech.com)   
- bnx2x: update fw to 7.8.2 (Yuval Mintz)  [Orabug: 21036509]  
- bnx2: Update driver to use new mips firmware. (Joe Jin)  [Orabug: 21036509]  
- Revert "i40e: Add FW check to disable DCB and wrap autoneg workaround with FW check" (Brian Maly)  [Orabug: 21111674]  
- net: Adding the hxge driver (James Puthukattukaran)   
- fuse: fix typo while displaying fuse numa mount option (Ashish Samant)   
- fuse: add numa mount option (Ashish Samant)   
- fuse: modify queues, allocation and locking for multiple nodes (Ashish Samant)   
- fuse: add spinlock to protect fc reqctr (Ashish Samant)   
- fuse: add fuse node struct (Ashish Samant)   
- ocfs2: Suppress the error message from being printed in ocfs2_rename (Xiaowei.Hu)  [Orabug: 16790405]  
- ocfs2: Tighten free bit calculation in the global bitmap (Sunil Mushran)  [Orabug: 17342255]  
- ocfs2/trivial: Limit unaligned aio+dio write messages to once per day (Sunil Mushran)  [Orabug: 17342255]  
- ocfs2/trivial: Print message indicating unaligned aio+dio write (Sunil Mushran)  [Orabug: 17342255]  
- Linux 4.1 (Linus Torvalds)   

