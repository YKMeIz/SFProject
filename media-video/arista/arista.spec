%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           arista
Version:       	0.9.7 
Release:        2%{?dist}
Summary:        An easy to use multimedia transcoder for the GNOME Desktop

Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://programmer-art.org/projects/arista-transcoder
Source0:        http://programmer-art.org/media/releases/arista-transcoder/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
Requires:       dbus-python
Requires:	pygtk2
Requires:	gnome-python2-gconf
Requires:	gstreamer-python
Requires:	pycairo
Requires:	gnome-python2-rsvg
Requires:       gstreamer-python
Requires:       gstreamer-ffmpeg
Requires:       gstreamer-plugins-base
Requires:       gstreamer-plugins-good
Requires:       gstreamer-plugins-bad
Requires:       gstreamer-plugins-ugly
Requires:	python-gudev

%description
An easy to use multimedia transcoder for the GNOME Desktop. Arista
focuses on being easy to use by making the complex task of encoding
for various devices simple. Pick your input, pick your target device,
choose a file to save to and go.

%prep
%setup -q


%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -f %{buildroot}%{python_sitelib}/%{name}/*.pyc

%find_lang arista

desktop-file-install --vendor Nux --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --remove-category Application \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT


%files -f arista.lang
%defattr(-,root,root,-)
%{_docdir}/%{name}/*
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/applications/*
%{_datadir}/%{name}/*
%{_datadir}/locale/templates/%{name}.pot
%{_datadir}/nautilus-python/extensions/*

%changelog
* Thu Jul 18 2014 Nux <rpm@li.nux.ro> - 0.9.7-2
- added requiers for python-gudev

* Thu Aug 18 2011 Nux <rpm@li.nux.ro> - 0.9.7-1
- initial build for EL6

