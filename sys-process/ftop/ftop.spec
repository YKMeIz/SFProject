Name: ftop
Version: 1.0 
Release: 7%{?dist}
Summary: Utility that shows shows progress of open files and file systems

Group: Applications/System
License: GPLv3+
URL: http://code.google.com/p/ftop/
#SHA1 Checksum of Source0 tarball d3ef1b74825f50c7c442d299b29d23c2478f199b
Source0: http://ftop.googlecode.com/files/%{name}-%{version}.tar.bz2
#Patch from the upstream project site:
#http://code.google.com/p/ftop/issues/list
Patch0: ftop-fix_buffer_overflow.patch
Patch1: ftop-fix_printf_format.patch
BuildRequires: ncurses-devel


%description
Ftop is to files what top is to processes. The progress of all open files 
file systems can be monitored. 
The selection of which files to display is possible through 
a wide assortment of options. As with top, the items are displayed in 
order from most to least active. 

%prep
%setup -q

touch -r configure.ac configure.ac.stamp
%patch0 -p0 -b .fix_buffer_overflow
%patch1 -p0 -b .fix_printf_format
touch -r configure.ac.stamp configure.ac

%build

%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT



%files

%defattr(-,root,root,-)
%{_bindir}/*
%doc COPYING AUTHORS ChangeLog NEWS README
%{_mandir}/man1/*



%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Feb 26 2011 Sergio Belkin <sebelk@gmail.com> 1.0-3
- Fixed License tag
- Fixed changelog

* Thu Feb 24 2011 Sergio Belkin <sebelk@gmail.com> 1.0-2
- Upstream patches applied
- Fixed date changelog

* Tue Feb 22 2011 Sergio Belkin <sebelk@gmail.com> 1.0-1
- First public ftop RPM for fedora
