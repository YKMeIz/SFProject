%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           qt-recordmydesktop
Version:        0.3.8
Release:        9%{?dist}
Summary:        KDE Desktop session recorder with audio and video

Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://recordmydesktop.sourceforge.net/
Source0:        http://downloads.sourceforge.net/recordmydesktop/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch

BuildRequires:  desktop-file-utils, gettext, PyQt4-devel
Requires:       recordmydesktop >= %{version}, PyQt4


%description
Graphical KDE frontend for the recordmydesktop desktop session recorder.

recordMyDesktop is a desktop session recorder for linux that attempts to be 
easy to use, yet also effective at it's primary task.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"

%find_lang qt-recordMyDesktop

desktop-file-install --delete-original  \
%if (0%{?fedora} && 0%{?fedora} < 19) || (0%{?rhel} && 0%{?rhel} < 7)
        --vendor fedora \
%endif
        --dir $RPM_BUILD_ROOT%{_datadir}/applications   \
        --remove-category Application \
        $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%files -f qt-recordMyDesktop.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README ChangeLog
%{_bindir}/*
%{python_sitelib}/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 0.3.8-8
- Remove --vendor from desktop-file-install in F19+ https://fedorahosted.org/fesco/ticket/1077

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.3.8-1
- New upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.3.7.2-3
- Rebuild for Python 2.6

* Wed May 28 2008 Sindre Pedersen Bjørdal <sindrepb@fedoraproject.org> - 0.3.7.2-2
- New upstream release

* Wed Jan 23 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 0.3.7-1
- Update to latest upstream 0.3.7 to match recordmydesktop

* Sun Oct 21 2007 Sindre Pedersen Bjørdal <foolish@guezz.net> - 0.3.6-4
- Fix Source0 url
* Sun Oct 21 2007 Sindre Pedersen Bjørdal <foolish@guezz.net> - 0.3.6-2
- Add Missing PyQt4 dependency
- Fix License tag
* Sun Oct 21 2007 Roland Wolters <wolters.liste@gmx.net> - 0.3.6-1
- initially build
- adopted spec file from gtk-version


