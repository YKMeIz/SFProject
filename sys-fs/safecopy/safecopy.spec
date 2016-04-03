Name:           safecopy
Version:        1.7
Release:        6%{?dist}
Summary:        Safe copying of files and partitions

Group:          Applications/System
License:        GPL+
URL:            http://safecopy.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
safecopy is a data recovery tool which tries to extract as much data
as possible from a problematic (i.e. damaged sectors) source - like
floppy drives, harddisk partitions, CDs, tape devices, ..., where
other tools like dd would fail doe to I/O errors.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags} 


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_mandir}/man*/%{name}*.*
%{_bindir}/%{name}


%changelog
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 15 2012 Fabian Affolter <mail@fabian-affolter.ch> - 1.7-1
- Updated to new upstream version 1.7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Fabian Affolter <mail@fabian-affolter.ch> - 1.4-1
- Updated to new upstream version 1.4

* Fri Jul 10 2009 Fabian Affolter <mail@fabian-affolter.ch> - 1.3-1
- Updated to new upstream version 1.3

* Fri Apr 18 2009 Fabian Affolter <mail@fabian-affolter.ch> - 1.2-2
- Added COPYING to doc and included only index.html
- Changed license to GPL+

* Wed Apr 15 2009 Fabian Affolter <mail@fabian-affolter.ch> - 1.2-1
- Initial spec for Fedora
