Name:           nzbget
Version:        10.2
Release:        2%{?dist}
Summary:        Command-line based binary newsgrabber for nzb files

License:        GPLv2+
URL:            http://nzbget.sourceforge.net/
Source0:        http://downloads.sourceforge.net/project/%{name}/%{name}-stable/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  libxml2-devel
BuildRequires:  libpar2-devel
BuildRequires:  ncurses-devel
BuildRequires:  gnutls-devel

#to fix the line endings in nzbgetd
BuildRequires:  dos2unix

%description
NZBGet is a cross-platform binary newsgrabber for nzb files, written in C++.
It supports client/server mode, automatic par-check/-repair and web-interface. 
NZBGet requires low system resources and runs great on routers, 
NAS-devices and media players. 

NZBGet can be used in standalone and in server/client modes. 
In standalone mode you pass a nzb-file as parameter in command-line, 
NZBGet downloads listed files and then exits. 
In server/client mode NZBGet runs as server in background. 
Then you use client to send requests to server. The sample requests are: 
download nzb-file, list files in queue, etc.

Standalone-tool, server and client are all contained in only 
one executable file "nzbget". The mode in which the program works 
depends on command-line parameters passed to the program. 


%prep
%setup -q


%build
# No exception for linking against OpenSSL in nzbget's license.
%configure --with-tlslib=GnuTLS --docdir=%{_docdir}/%{name}-%{version}
make %{?_smp_mflags}


%install
%make_install

dos2unix %{buildroot}/%{_sbindir}/%{name}*


%files
%{_bindir}/%{name}*
%{_sbindir}/%{name}*
%{_datadir}/%{name}*
%{_docdir}/%{name}*
%doc AUTHORS

%changelog
* Tue May 14 2013 Marcel Wysocki <maci@satgnu.net> - 10.2-2
- removed unneeded configure option
- fix line endings in nzbgetd

* Tue Apr 23 2013 Marcel Wysocki <maci@satgnu.net> - 10.2-1
- update to version 10.2
- lots of fixes

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Pierre Carrier <prc@redhat.com> 0.7.0-1
- Initial packaging
