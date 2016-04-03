%global debug_package %{nil}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:           lv2
Version:        1.8.0
Release:        1%{?dist}
Summary:        Audio Plugin Standard
Group:          System Environment/Libraries

# lv2specgen template.html is CC-AT-SA
License:        ISC
URL:            http://lv2plug.in
Source:         http://lv2plug.in/spec/lv2-%{version}.tar.bz2

BuildRequires:  doxygen graphviz python-rdflib
# TODO: it complains about missing this, 
# (Error importing pygments, syntax highlighting disabled)
# but the syntax-highlighting in the generated docs looks strange
#BuildRequires: python-pygments

# this package replaces lv2core 
Provides:       lv2core = 6.0-4
Obsoletes:      lv2core < 6.0-4
Provides:       lv2-ui = 2.4-5
Obsoletes:      lv2-ui < 2.4-5

%description
LV2 is a standard for plugins and matching host applications, mainly
targeted at audio processing and generation.  

There are a large number of open source and free software synthesis
packages in use or development at this time. This API ('LV2') attempts
to give programmers the ability to write simple 'plugin' audio
processors in C/C++ and link them dynamically ('plug') into a range of
these packages ('hosts').  It should be possible for any host and any
plugin to communicate completely through this interface.

LV2 is a successor to LADSPA, created to address the limitations of
LADSPA which many hosts have outgrown.

%package        devel
Summary:        API for the LV2 Audio Plugin Standard
Group:          Development/Libraries

Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       lv2core-devel = 6.0-4
Obsoletes:      lv2core-devel < 6.0-4
Provides:       lv2-ui-devel = 2.4-5
Obsoletes:      lv2-ui-devel < 2.4-5

%description    devel
lv2-devel contains the lv2.h header file and headers for all of the
LV@ specification extensions and bundles.

Definitive technical documentation on LV2 plug-ins for both the host
and plug-in is contained within copious comments within the lv2.h
header file.

%package        doc
Summary:        Documentation for the LV2 Audio Plugin Standard
Group:          Documentation
BuildArch:      noarch
Obsoletes:      %{name}-docs < 1.6.0-2
Provides:       %{name}-docs = %{version}-%{release}

%description    doc
Documentation for the LV2 plugin API.

%package        example-plugins
Summary:        Examples of the LV2 Audio Plugin Standard
Group:          Audio/Multimedia

%description    example-plugins
Example LV2 audio plugins

%prep
%setup -q

%build
export CFLAGS="%{optflags}"
./waf configure -vv --prefix=%{_prefix} --libdir=%{_libdir} --debug \
  --docs --docdir=%{_pkgdocdir}
./waf -vv %{?_smp_mflags}

%install
rm -rf %buildroot
DESTDIR=%buildroot ./waf -vv install
mv %{buildroot}%{_pkgdocdir}/%{name}/lv2plug.in/* %{buildroot}%{_pkgdocdir}
find %{buildroot}%{_pkgdocdir} -type d -empty | xargs rmdir
for f in COPYING NEWS README ; do
    install -p -m0644 $f %{buildroot}%{_pkgdocdir}
done

%clean
rm -rf %buildroot

%files
# don't include doc files via %%doc here (bz 913540)
%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING
%{_pkgdocdir}/NEWS
%{_pkgdocdir}/README
%{_libdir}/%{name}/

%exclude %{_libdir}/%{name}/*/*.[ch]

%files devel
%{_bindir}/lv2specgen.py
%{_datadir}/lv2specgen
%{_includedir}/%{name}.h
%{_includedir}/%{name}/
%{_libdir}/%{name}/eg-*
%{_libdir}/%{name}/*/*.[hc]
%{_libdir}/pkgconfig/lv2core.pc
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%{_pkgdocdir}/

%changelog
* Thu Jan 09 2014 Brendan Jones <brendan.jones.it@gmail.com> 1.8.0-1
- Upstream maintenance release
- Add example plugins

* Sun Sep 22 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.6.0-2
- Don't duplicate -doc package contents in base package (#913540).
- Define and use %%_pkgdocdir as suggested by the Unversioned Docdirs
  change for Fedora 20 (#993908).
- Pass --docdir= to waf.
- Use Group Documentation in -doc subpackage.
- Rename -docs package to -doc as recommended in the guidelines.
- The documentation subpackage does not need the base package.

* Fri Aug 23 2013 Brendan Jones <brendan.jones.it@gmail.com> 1.6.0-1
- Update to 1.6.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 21 2013 Brendan Jones <brendan.jones.it@gmail.com> 1.4.0-1
- New upstream release 

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Oct 20 2012 Brendan Jones <brendan.jones.it@gmail.com> 1.2.0-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Brendan Jones <brendan.jones.it@gmail.com> 1.0.0-7
- Remove date from doxygen footers

* Sat Apr 21 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-6
- Re-suppress debuginfo

* Sat Apr 21 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-5
- libsndfile no longer required

* Sat Apr 21 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-4
- remove examples 

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-3
- dd libsndfile BR

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-2
- Remove debuginfo supression, correct changelog

* Fri Apr 20 2012 Brendan Jones <brendan.jones.it@gmail.com> - 1.0.0-1
- Created

