Name:           libtxc_dxtn
Version:        1.0.0
Release:        3%{?dist}
Epoch:          1
Summary:        Free implementation of the s3tc texture compression algorithm

Group:          System Environment/Libraries
License:        BSD
URL:            http://cgit.freedesktop.org/~mareko/libtxc_dxtn/
Source0:        http://cgit.freedesktop.org/~mareko/%{name}/snapshot/%{name}-%{version}.tar.bz2

BuildRequires:  mesa-libGL-devel       

%description
Free implementation of the s3tc texture compression algorithm


%prep
%setup -q
sed -i -e 's|/usr/lib|%{_libdir}|g;s|install -m|install -pm|g' Makefile
sed -i -e 's|pixerrorcolorbest\[3\]|pixerrorcolorbest[3]={0,0,0}|g' txc_compress_dxtn.c
sed -i -e 's|GLshort alphatest\[2\]|GLshort alphatest[2]={0,0}|g' txc_compress_dxtn.c

%build
make %{?_smp_mflags} OPT_CFLAGS="%{optflags} -Werror"


%install
make install DESTDIR=$RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changelog
%{_libdir}/*.so

%changelog
* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:1.0.0-3
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Hicham HAOUARI <hicham.haouari@gmail.com> - 1:1.0.0-1
- Update to 1.0.0 from Marek's branch

* Tue Oct 26 2010 Hicham HAOUARI <hicham.haouari@gmail.com> - 070518-1
- Initial package for Fedora.
