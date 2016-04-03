# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           gdevilspie
Version:        0.5
Release:        2%{?dist}
Summary:        A user friendly interface to the devilspie window matching daemon

Group:          User Interface/Desktops
License:        GPLv3+
URL:            http://code.google.com/p/gdevilspie/
Source0:        http://gdevilspie.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       devilspie pyxdg

%description
gdevilspie is a user friendly interface to the devilspie window matching
daemon which allows you to create window management rules easily. 

%prep
%setup -q

%build
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#don't include these twice
rm -rf $RPM_BUILD_ROOT%{_docdir}/gdevilspie
 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changelog COPYING README TODO
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/gdevilspie
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%changelog
* Fri Jan 06 2012 Nux <rpm@li.nux.ro> - 0.5-2
- adding Requires pyxdg

* Thu Oct 20 2011 Nux <nux@li.nux.ro> - 0.5-1
- Update to 0.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.31-3
- Rebuild for Python 2.6

* Tue Mar 18 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.31-1
- Initial build

