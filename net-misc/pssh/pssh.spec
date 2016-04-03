%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"
)}

Summary:   Parallel SSH tools
Name:      pssh
Version:   2.3.1
Release:   7%{?dist}
License:   BSD
Url:       http://code.google.com/p/parallel-ssh/
Group:     Applications/Productivity
Source0:   http://parallel-ssh.googlecode.com/files/pssh-%{version}.tar.gz
Requires:  openssh-clients
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-setuptools

%description
This package provides various parallel tools based on ssh and scp.
Parallell version includes:
 o ssh : pssh
 o scp : pscp
 o nuke : pnuke
 o rsync : prsync
 o slurp : pslurp

%prep 
%setup -q
%{__sed} -i -e '1 d' psshlib/askpass_{client,server}.py

%build
%{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__install} -D -m 0755 %{buildroot}%{_bindir}/pssh-askpass \
    %{buildroot}%{_libexecdir}/%{name}/pssh-askpass
%{__rm} -f %{buildroot}%{_bindir}/pssh-askpass
%{__install} -d %{buildroot}%{_mandir}
%{__mv} %{buildroot}%{_prefix}/man/man1 %{buildroot}%{_mandir}/man1
%{__rm} -rf %{buildroot}%{_prefix}/man 

%{__mv} %{buildroot}%{_bindir}/pscp %{buildroot}%{_bindir}/pscp.pssh
%{__mv} %{buildroot}%{_mandir}/man1/pscp.1 %{buildroot}%{_mandir}/man1/pscp.pssh.1 

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc AUTHORS ChangeLog COPYING
%{_bindir}/pnuke
%{_bindir}/prsync
%{_bindir}/pscp.pssh
%{_bindir}/pslurp
%{_bindir}/pssh
%{_mandir}/man1/pnuke.1*
%{_mandir}/man1/prsync.1*
%{_mandir}/man1/pscp.pssh.1*
%{_mandir}/man1/pslurp.1*
%{_mandir}/man1/pssh.1*
%{_libexecdir}/%{name}
%{python_sitelib}/%{name}-%{version}*
%{python_sitelib}/%{name}lib

%changelog
* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 2.3.1-7
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Feb 19 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.3.1-2
- Fix bz #794567

* Thu Feb 02 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.3.1-1
- 2.3.1
- Add man all pages

* Tue Jan 31 2012 Terje Rosten <terje.rosten@ntnu.no> - 2.3-1
- 2.3

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Terje Rosten <terje.rosten@ntnu.no> - 2.2.2-1
- 2.2.2

* Thu Jan 27 2011 Terje Rosten <terje.rosten@ntnu.no> - 2.2.1-1
- 2.2.1

* Sat Jan 22 2011 Terje Rosten <terje.rosten@ntnu.no> - 2.2-1
- 2.2

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Mar 26 2010 Terje Rosten <terje.rosten@ntnu.no> - 2.1.1-1
- 2.1.1

* Mon Mar 01 2010 Terje Rosten <terje.rosten@ntnu.no> - 2.1-1
- 2.1

* Sun Nov 01 2009 Terje Rosten <terje.rosten@ntnu.no> - 2.0-1
- 2.0
- Switch to new upstream
- Move pscp to pscp.pssh

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan  5 2009 Terje Rosten <terje.rosten@ntnu.no> - 1.4.3-1
- 1.4.3

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.4.0-2
- Rebuild for Python 2.6

* Mon Aug 25 2008 Terje Rosten <terje.rosten@ntnu.no> - 1.4.0-1
- initial build
