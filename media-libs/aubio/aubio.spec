%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}


Name:           aubio
Version:        0.3.2
Release:        16%{?dist}
Summary:        An audio labelling library

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://aubio.org/
Source0:        http://aubio.org/pub/aubio-%{version}.tar.gz
# Fix byte-compilation error. Borrowed from Debian
Patch0:         aubio-numarray-gnuplot.patch
# Fix DSO-linking failure
Patch1:         aubio-linking.patch
Patch2:         aubio-format-security.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libsndfile-devel libsamplerate-devel fftw-devel
BuildRequires:  lash-devel jack-audio-connection-kit-devel
BuildRequires:  python-devel

%description
aubio is a library for audio labelling. Its features include
segmenting a sound file before each of its attacks, performing pitch
detection, tapping the beat and producing midi streams from live
audio. The name aubio comes from 'audio' with a typo: several
transcription errors are likely to be found in the results too.

The aim of this project is to provide these automatic labelling
features to other audio softwares. Functions can be used offline in
sound editors and software samplers, or online in audio effects and
virtual instruments.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package	python
Summary:        Python language bindings for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       python
BuildRequires:  python swig

%description    python
The %{name}-python package contains the Python language bindings for %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .linking
%patch2 -p1

%build
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
# Move everything to sitearch...
if [ %{python_sitearch} != %{python_sitelib} ]; then
  mkdir -p $RPM_BUILD_ROOT%{python_sitearch}
  mv $RPM_BUILD_ROOT%{python_sitelib}/%{name} $RPM_BUILD_ROOT%{python_sitearch}
fi

%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README THANKS
%{_libdir}/*.so.*
%{_bindir}/*
%{_datadir}/sounds/%{name}

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/aubio

%files python
%defattr(-,root,root,-)
%{python_sitearch}/%{name}

%changelog
* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Feb 10 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.2-8
- Fix DSO-linking failure
- Fix byte-compilation failure

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.2-5
- Rebuild for Python 2.6

* Sun Jul 13 2008 Anthony Green <green@redhat.com> 0.3.2-4
- BuildRequire python-devel.

* Sun Jul 13 2008 Anthony Green <green@redhat.com> 0.3.2-3
- Fix python package installation.

* Sun Jul 13 2008 Anthony Green <green@redhat.com> 0.3.2-2
- Untabify.
- Don't use rpath.
- Add python subpackage.

* Thu Jul 10 2008 Anthony Green <green@redhat.com> 0.3.2-1
- Created.
