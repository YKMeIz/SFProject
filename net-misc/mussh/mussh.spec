Name:           mussh
Version:        1.0
Release:        6%{?dist}
Summary:        Multihost SSH wrapper

Group:          Applications/System
License:        GPL+
URL:            http://www.sourceforge.net/projects/mussh
Source0:        http://downloads.sourceforge.net/mussh/mussh-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       openssh-clients

%description
Mussh is a shell script that allows you to execute a command or script
over ssh on multiple hosts with one command. When possible mussh will use
ssh-agent and RSA/DSA keys to minimize the need to enter your password
more than once.

%prep
%setup -q -n mussh

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin/
install -p mussh $RPM_BUILD_ROOT/usr/bin/
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1/
gzip mussh.1
install -p mussh.1.gz ${RPM_BUILD_ROOT}%{_mandir}/man1/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc INSTALL README BUGS CHANGES EXAMPLES
%{_bindir}/mussh
%{_mandir}/man1/*

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Kevin Fenzi <kevin@scrye.com> - 1.0-3
- Add requires for openssh-clients. Fixes bug #842048

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Kevin Fenzi <kevin@scrye.com> - 1.0-0
- Update to new 1.0 upstream release. 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 27 2007 Kevin Fenzi <kevin@tummy.com> 0.7-2
- Update License tag

* Tue Dec 26 2006 Kevin Fenzi <kevin@tummy.com> 0.7-1
- Update to 0.7

* Sun Dec 10 2006 Kevin Fenzi <kevin@tummy.com> 0.6-1
- Initial version for Fedora Extras

* Thu Aug 11 2005 Dave Fogarty <dave@collegenet.com>
- Re-package for 0.6-1BETA
- Async mode added

* Tue Jul 30 2002 Dave Fogarty <dave@collegenet.com>
- Re-package for 0.5
