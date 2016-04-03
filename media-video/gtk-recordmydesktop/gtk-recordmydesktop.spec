%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           gtk-recordmydesktop
Version:        0.3.8
Release:        10%{?dist}
Summary:        GUI Desktop session recorder with audio and video

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://recordmydesktop.sourceforge.net/
Source0:        http://dl.sourceforge.net/recordmydesktop/%{name}-%{version}.tar.gz        
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  python-devel, pygtk2-devel
BuildRequires:  desktop-file-utils, gettext
Requires:       recordmydesktop >= %{version}


%description
Graphical frontend for the recordmydesktop desktop session recorder.

recordMyDesktop is a desktop session recorder for linux that attempts to be 
easy to use, yet also effective at it's primary task.

As such, the program is separated in two parts; a simple command line tool that
performs the basic tasks of capturing and encoding and an interface that 
exposes the program functionality in a usable way.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"

%find_lang gtk-recordMyDesktop

desktop-file-install --delete-original  \
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --remove-category Application \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%files -f gtk-recordMyDesktop.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Apr 23 2013 Jon Ciesla <limburgher@gmail.com> - 0.3.8-9
- Drop desktop vendor tag.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 13 2011 Mat Booth <fedora@matbooth.co.uk> 0.3.8-5
- Fix URL.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.3.8-1
- New upstream release

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.7.2-3
- Rebuild for Python 2.6

* Wed May 28 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.3.7.2-2
- New upstream release

* Thu Jan 17 2008 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.7-1
- New upstream release
* Sun Oct 21 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.6-1
- New version
- Update URL
* Sat Jun 02 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.4-1
- New version 0.3.4
* Tue Mar 06 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.3.1-2 
- Preserve timestamps
* Mon Mar 05 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.3.1-2 
- Add missing BR
* Sun Mar 04 2007 Sindre Pedersen Bjørdal <foolish[AT]guezz.net> - 0.3.3.1-1
- Initial build
