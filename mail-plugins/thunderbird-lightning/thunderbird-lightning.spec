%global nspr_version 4.9
%global nss_version 3.13.3
%global cairo_version 1.8.8
%global freetype_version 2.1.9
%global sqlite_version 3.6.14
%global libnotify_version 0.4
%global libvpx_version 1.0.0
# Update these two as a pair - see calendar/lightning/install.rdf and mail/config/version.txt
%global thunderbird_version 24.5.0
%global thunderbird_next_version 25.0
%global lightning_version 2.6.5
# Bump one with each minor lightning release
%global gdata_version 0.25
# Compatible versions are listed in:
# comm-release/calendar/lightning/install.rdf.rej
# comm-release/calendar/providers/gdata/install.rdf.rej
%global moz_objdir objdir
%global lightning_extname %{_libdir}/mozilla/extensions/{3550f703-e582-4d05-9a08-453d09bdfdc6}/{e2fda1a4-762b-4020-b5ad-a41df1933103}
%global gdata_extname %{_libdir}/mozilla/extensions/{3550f703-e582-4d05-9a08-453d09bdfdc6}/{a62ef8ec-5fdc-40c2-873c-223b8a6925cc}

# The tarball is pretty inconsistent with directory structure.
# Sometimes there is a top level directory.  That goes here.
#
# IMPORTANT: If there is no top level directory, this should be
# set to the cwd, ie: '.'
#global tarballdir .
%global tarballdir comm-esr24

%global version_internal  2
%global mozappdir         %{_libdir}/%{name}-%{version_internal}

Name:           thunderbird-lightning
Summary:        The calendar extension to Thunderbird
Version:        %{lightning_version}
# Must bump release unless gdata_version is increased too
Release:        9%{?dist}
URL:            http://www.mozilla.org/projects/calendar/lightning/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
Group:          Applications/Productivity
Source0:        http://ftp.mozilla.org/pub/mozilla.org/calendar/lightning/releases/%{version}/source/lightning-%{version}.source.tar.bz2
#Source0:        http://releases.mozilla.org/pub/mozilla.org/thunderbird/releases/%{thunderbird_version}/source/thunderbird-%{thunderbird_version}.source.tar.bz2
# This script will generate the language source below
Source1:        mklangsource.sh
Source2:        l10n-%{version}.tar.xz
# Config file for compilation
Source10:       thunderbird-mozconfig
# Finds requirements provided outside of the current file set
Source100:      find-external-requires

# Mozilla (XULRunner) patches
Patch0:         thunderbird-version.patch
Patch1:         mozilla-build-arm.patch
# Fix build on secondary arches (patches copied from xulrunner)
Patch2:         xulrunner-10.0-secondary-ipc.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  nspr-devel >= %{nspr_version}
BuildRequires:  nss-devel >= %{nss_version}
%if 0%{?fedora} > 15
BuildRequires:  nss-static
%endif
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  libnotify-devel >= %{libnotify_version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  zlib-devel
BuildRequires:  libIDL-devel
BuildRequires:  gtk2-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  libgnome-devel
BuildRequires:  libgnomeui-devel
BuildRequires:  krb5-devel
BuildRequires:  pango-devel
BuildRequires:  freetype-devel >= %{freetype_version}
BuildRequires:  libXt-devel
BuildRequires:  libXrender-devel
BuildRequires:  hunspell-devel
BuildRequires:  sqlite-devel >= %{sqlite_version}
BuildRequires:  startup-notification-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf213
BuildRequires:  desktop-file-utils
BuildRequires:  libcurl-devel
BuildRequires:  python
BuildRequires:  yasm
BuildRequires:  mesa-libGL-devel
BuildRequires:  libvpx-devel >= %{libvpx_version}
Requires:       thunderbird >= %{thunderbird_version}
Requires:       thunderbird < %{thunderbird_next_version}
Obsoletes:      thunderbird-lightning-wcap <= 0.8
Provides:       thunderbird-lightning-wcap = %{version}-%{release}
AutoProv: 0
%global _use_internal_dependency_generator 0
%global __find_requires %{SOURCE100}

 
%description
Lightning brings the Sunbird calendar to the popular email client,
Mozilla Thunderbird. Since it's an extension, Lightning is tightly
integrated with Thunderbird, allowing it to easily perform email-related
calendaring tasks.


%package gdata
Summary:        Lightning data provider for Google Calendar
Version:        %{gdata_version}
Requires:       %{name}%{?_isa} = %{lightning_version}-%{release}

%description gdata
This extension allows Lightning to read and write events to a Google Calendar.

Please read http://wiki.mozilla.org/Calendar:GDATA_Provider for more details
and before filing a bug. Also, be sure to visit the dicussion forums, maybe
your bug already has a solution!


%prep
%setup -q -c -a 2
cd %{tarballdir}

sed -e 's/__RPM_VERSION_INTERNAL__/%{version_internal}/' %{P:%%PATCH0} \
    > version.patch
%{__patch} -p1 -b --suffix .version --fuzz=0 < version.patch
cd mozilla
%patch1 -p2 -b .arm-fix
%patch2 -p3 -b .secondary-ipc
cd ..

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig

# s390(x) fails to start with jemalloc enabled
%ifarch s390 s390x
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

# Fix permissions
find -name \*.js -type f | xargs chmod -x

#===============================================================================

%build
cd %{tarballdir}

INTERNAL_GECKO=%{version_internal}
MOZ_APP_DIR=%{mozappdir}

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
# 
MOZ_OPT_FLAGS=$(echo "$RPM_OPT_FLAGS" | \
                      %{__sed} -e 's/-Wall//')
# https://bugzilla.redhat.com/show_bug.cgi?id=1037355
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat"
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

%global moz_make_flags -j1
%ifarch ppc ppc64 s390 s390x
%global moz_make_flags -j1
%else
# temp override of %global moz_make_flags %{?_smp_mflags}
%global moz_make_flags -j1
%endif

export LDFLAGS="-Wl,-rpath,%{mozappdir}"
export MAKE="gmake %{moz_make_flags}"
make -f client.mk build STRIP=/bin/true

# Package l10n files
cd %{moz_objdir}/calendar/lightning
#make AB_CD=all L10N_XPI_NAME=lightning-all repack-clobber-all
make AB_CD=all L10N_XPI_NAME=lightning-all repack-stage-all
grep -v 'osx' ../../../calendar/locales/shipped-locales | while read lang x
do
   # Skip cs for now
   [ $lang = cs ] && continue
   make AB_CD=all L10N_XPI_NAME=lightning-all libs-$lang
done

#===============================================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{tarballdir}

# Avoid "Chrome Registration Failed" message on first startup and extension installation
mkdir -p $RPM_BUILD_ROOT%{lightning_extname}
touch $RPM_BUILD_ROOT%{lightning_extname}/chrome.manifest
mkdir -p $RPM_BUILD_ROOT%{gdata_extname}
touch $RPM_BUILD_ROOT%{gdata_extname}/chrome.manifest

# Lightning and GData provider for it
unzip -qod $RPM_BUILD_ROOT%{lightning_extname} %{moz_objdir}/mozilla/dist/xpi-stage/lightning-%{lightning_version}.all.linux-*.xpi
unzip -qod $RPM_BUILD_ROOT%{gdata_extname} %{moz_objdir}/mozilla/dist/xpi-stage/gdata-provider-0.25.en-US.linux-*.xpi

# Fix up permissions
find $RPM_BUILD_ROOT -name \*.so | xargs chmod 0755

#===============================================================================

%clean
%{__rm} -rf $RPM_BUILD_ROOT

#===============================================================================

%files
%doc %{tarballdir}/mozilla/LEGAL %{tarballdir}/mozilla/LICENSE %{tarballdir}/mozilla/README.txt
%{lightning_extname}

%files gdata
%doc %{tarballdir}/mozilla/LEGAL %{tarballdir}/mozilla/LICENSE %{tarballdir}/mozilla/README.txt
%{gdata_extname}

#===============================================================================

%changelog
* Wed May 14 2014 Orion Poplawski <orion@cora.nwra.com> - 2.6.5-9
- Update to 2.6.5

* Fri Jan 31 2014 Orion Poplawski <orion@cora.nwra.com> - 2.6.4-8
- Fix build with -Werror=format-security (bug #1037355)

* Sat Dec 14 2013 Orion Poplawski <orion@cora.nwra.com> - 2.6.4-7
- Sync thunderbird-mozoptions from thunderbird package

* Wed Dec 11 2013 Orion Poplawski <orion@cora.nwra.com> - 2.6.4-6
- Update to 2.6.4
- Drop caldav patch
- Exclude cs locale for now - doesn't build

* Wed Nov 27 2013 Jan Horak <jhorak@redhat.com> - 2.6.2-5
- Enable arm arch

* Sun Nov 24 2013 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-4
- Use lightning 2.6.2 source

* Mon Nov 4 2013 Orion Poplawski <orion@cora.nwra.com> - 2.6.2-3
- Add upstream patch to fix caldav sync

* Wed Oct 30 2013 Jan Horak <jhorak@redhat.com> - 2.6.2-2
- Update to 2.6.2

* Fri Sep 20 2013 Orion Poplawski <orion@cora.nwra.com> - 2.6-1
- Drop alarm patch
- Drop -fpermissive
- Update to 2.6
- Exclude arm architecture

* Sat Aug 17 2013 Orion Poplawski <orion@cora.nwra.com> - 1.9.1-5
- Fix up gdata lightning version dependency

* Fri Aug 16 2013 Orion Poplawski <orion@cora.nwra.com> - 1.9.1-4
- Split Google data provider into a sub-package (bug #554113)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.1-2
- Only build WebRTC on x86 to fix FTBFS on other arches

* Tue Mar 19 2013 Orion Poplawski <orion@cora.nwra.com> - 1.9.1-1
- Update to 1.9.1
- Add patch to fix alarm handling after suspend (bug #910976)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Jan Horak <jhorak@redhat.com> - 1.9-1
- Update to 1.9

* Tue Oct  9 2012 Jan Horak <jhorak@redhat.com> - 1.8-1
- Update to 1.8

* Tue Aug 28 2012 Jan Horak <jhorak@redhat.com> - 1.7-2
- Update to 1.7

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Jan Horak <jhorak@redhat.com> - 1.6-1
- Update to 1.6

* Wed Jun 6 2012 Orion Poplawski <orion@cora.nwra.com> - 1.5-2
- Bump required TB version

* Mon Jun 4 2012 Orion Poplawski <orion@cora.nwra.com> - 1.5-1
- Update to 1.5
- Drop upstreamed patches

* Mon Apr 30 2012 Orion Poplawski <orion@cora.nwra.com> - 1.4-2
- Update l10n source (bug #817477)
- Re-enable sv-SE

* Tue Apr 24 2012 Jan Horak <jhorak@redhat.com> - 1.4-1
- Update to 1.4
- Skip sv-SE locale for now

* Fri Mar 16 2012 Martin Stransky <stransky@redhat.com> - 1.3-3
- Thunderbird dependency fix

* Fri Mar 16 2012 Martin Stransky <stransky@redhat.com> - 1.3-2
- gcc 4.7 build fix

* Wed Mar 14 2012 Martin Stransky <stransky@redhat.com> - 1.3-1
- Update to 1.3

* Mon Feb 6 2012 Orion Poplawski <orion@cora.nwra.com> - 1.2.1-1
- Update to 1.2.1

* Tue Jan 31 2012 Jan Horak <jhorak@redhat.com> - 1.2-1
- Update to 1.2

* Fri Jan 6 2012 Orion Poplawski <orion@cora.nwra.com> - 1.1.1-1
- Update to 1.1.1
- Re-enable eu locale

* Thu Jan 5 2012 Orion Poplawski <orion@cora.nwra.com> - 1.1-4
- Add patch to fixup gcc 4.7 build issues

* Thu Jan 5 2012 Orion Poplawski <orion@cora.nwra.com> - 1.1-3
- Update l10n source hopefully to 1.1 release (bug #771860)

* Thu Jan 05 2012 Dan Horák <dan[at]danny.cz> - 1.1-2
- fix build on secondary arches (cherry-picked from 13afcd4c097c)
- disable jemalloc on s390(x) (taken from xulrunner)

* Tue Dec 27 2011 Orion Poplawski <orion@cora.nwra.com> - 1.1-1
- Update to lightning 1.1 final (same as rc1)
- Update l10n source

* Tue Dec 20 2011 Orion Poplawski <orion@cora.nwra.com> - 1.1-0.1.rc1
- Update to lightning 1.1 rc1
- Update l10n source
- Skip eu locale for now

* Tue Dec 20 2011 Jan Horak <jhorak@redhat.com> - 1.0-2
- Rebuild due to Thunderbird 9.0

* Mon Nov 14 2011 Orion Poplawski <orion@cora.nwra.com> - 1.0-1
- Update to lightning 1.0
- Update l10n source

* Wed Nov  9 2011 Jan Horak <jhorak@redhat.com> - 1.0-0.52.r2
- Use lightning 1.0rc2 source for TB 8
- Update l10n source

* Wed Oct 12 2011 Dan Horák <dan[at]danny.cz> - 1.0-0.51.b7
- sync secondary arches support with xulrunner/thunderbird

* Wed Sep 28 2011 Orion Poplawski <orion@cora.nwra.com> - 1.0-0.50.b7
- Use lightning 1.0b7 source for TB 7
- Update l10n source
- Drop tbver patch

* Wed Aug 31 2011 Dan Horák <dan[at]danny.cz> - 1.0-0.49.b5
- sync secondary arches support with xulrunner/thunderbird

* Thu Aug 18 2011 Orion Poplawski <orion@cora.nwra.com> - 1.0-0.48.b5
- Use TB6 source
- Update l10n source, skipping si for now
- Drop patches fixed upstream
- Use Requires to match to thunderbird major version (bug #720709)
- Add patch to change tb version compatibility to 6.*

* Fri Jul 29 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.47.b5rc3
- Package l10n langpacks (bug #504994)

* Thu Jul 28 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.46.b5rc3
- Update to 1.0 b5 rc3
- Use lightning release sources

* Tue Jul 19 2011 Dan Horák <dan[at]danny.cz> - 1.0-0.45.b3pre
- add xulrunner patches for secondary arches

* Mon Jul 18 2011 Jan Horak <jhorak@redhat.com> - 1.0-0.44.b3pre
- Require nss-static only for Fedora 16+

* Thu Jul 14 2011 Jan Horak <jhorak@redhat.com> - 1.0-0.43.b3pre
- Update to thunderbird 5 source
- Removed obsolete patches
- Adopted mozconfig from thunderbird package

* Tue Jun 28 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.42.b3pre
- Update to thunderbird 3.1.11 source
- Drop notify patch, fixed upstream
- Change BR nss-devel to nss-static (Bug 717246)
- Add BR python

* Mon Apr 11 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.41.b3pre
- Fix debuginfo builds
- Remove official branding sections
- Don't unpack the .xpi

* Wed Apr 6 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.40.b3pre
- Fixup some file permissions
- Minor review cleanups

* Mon Apr 4 2011 Orion Poplawski <orion@cora.nwra.com> 1.0-0.39.b3pre
- Initial packaging, based on thunderbird 3.1.9
