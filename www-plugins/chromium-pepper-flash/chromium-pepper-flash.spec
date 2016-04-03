%define debug_package %{nil}

Summary:        Chromium Flash player plugin
Name:           chromium-pepper-flash
Version:        20.0.0.286
Release:        1%{?dist}

License:        Proprietary
Url:            http://www.google.com/chrome
Group:          Applications/Internet
Source:		http://www.google.com/chrome/intl/en/eula_text.html

BuildRequires:  rpm cpio wget
%if 0%{?rhel} == 6
Requires : chrome-deps
%endif

Obsoletes: chromium-pepper-flash-chromium-pdf-plugin

%description
Pepper API based Adobe Flash plugin for Google's Open Source browser Chromium.


%prep
%setup -c -T
%ifarch x86_64
wget -c -P %{_builddir}/%{name}-%{version} https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
%else
wget -c -P %{_builddir}/%{name}-%{version} https://dl.google.com/linux/direct/google-chrome-stable_current_i386.rpm
%endif

%build
%ifarch x86_64
rpm2cpio %{_builddir}/%{name}-%{version}/google-chrome-stable_current_x86_64.rpm | cpio -idmv
%else
rpm2cpio %{_builddir}/%{name}-%{version}/google-chrome-stable_current_i386.rpm | cpio -idmv
%endif


%install
install -dm 755 %{buildroot}%{_libdir}/chromium/PepperFlash/
install -dm 755 %{buildroot}/usr/share/licenses/%{name}/
install -m644 %{_builddir}/%{name}-%{version}/opt/google/chrome/PepperFlash/* %{buildroot}%{_libdir}/chromium/PepperFlash/ 

# License
install -m644 %{SOURCE0} %{buildroot}/%{_datadir}/licenses/%{name}/

%files
%dir %{_libdir}/chromium/
%{_libdir}/chromium/PepperFlash/
%{_datadir}/licenses/%{name}/eula_text.html


%changelog

* Wed Jan 27 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 20.0.0.286-1
- Updated to 20.0.0.286

* Wed Jan 06 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 20.0.0.228-1
- Updated to 20.0.0.228

* Fri Nov 06 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 19.0.0.226-1
- Updated to 19.0.0.226

* Mon Sep 28 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 19.0.0.185-1
- Updated to 19.0.0.185

* Sun Jun 28 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 18.0.0.194-1
- Updated to 18.0.0.194

* Wed Mar 11 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 17.0.0.134-1
- Updated to 17.0.0.134

* Mon Dec 08 2014 David Vásquez <davidjeremias82 AT gmail DOT com> - 16.0.0.257-1
- Updated to 16.0.0.257

* Mon Dec 08 2014 David Vásquez <davidjeremias82 AT gmail DOT com> - 15.0.0.239
- initial build 
