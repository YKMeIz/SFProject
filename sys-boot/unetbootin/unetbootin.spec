%global rel 581

Name:		unetbootin
Version:	0
Release:	14.%{rel}bzr%{?dist}
Summary:	Create bootable Live USB drives for a variety of Linux distributions
Group:		System Environment/Base
License:	GPLv2+
URL:		http://unetbootin.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-source-%{rel}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# Syslinux is only available on x86 architectures
ExclusiveArch:	%{ix86} x86_64

BuildRequires:	desktop-file-utils
BuildRequires:	qt4-devel
# Not picked up automatically, required for operation
Requires:	p7zip-plugins
Requires:	syslinux
Requires:	syslinux-extlinux

%description
UNetbootin allows you to create bootable Live USB drives for a variety of
Linux distributions from Windows or Linux, without requiring you to burn a CD.
You can either let it download one of the many distributions supported
out-of-the-box for you, or supply your own Linux .iso file if you've already
downloaded one or your preferred distribution isn't on the list.

%prep
%setup -q -c 
# Fix EOL encoding
for file in README.TXT; do
 sed "s|\r||g" $file > $file.new && \
 touch -r $file $file.new && \
 mv $file.new $file
done
# Fix desktop file
sed -i '/^Version/d' unetbootin.desktop
sed -i '/\[en_US\]/d' unetbootin.desktop
sed -i 's|/usr/bin/unetbootin|unetbootin|g' unetbootin.desktop

%build

# Ugh, there's no macro for running lrelease and on RHEL the default is qt-3.3
%if 0%{?rhel} == 5
# Generate .qm files
%{_libdir}/qt4/bin/lrelease unetbootin.pro
%{_libdir}/qt4/bin/qmake
%else
# Generate .qm files
lrelease-qt4 unetbootin.pro
qmake-qt4
%endif

make %{?_smp_mflags}

%install
rm -rf %{buildroot} 
install -D -p -m 755 unetbootin %{buildroot}%{_bindir}/unetbootin
# Install desktop file
desktop-file-install --vendor="" --remove-category=Application --dir=%{buildroot}%{_datadir}/applications unetbootin.desktop
# Install localization files
install -d %{buildroot}%{_datadir}/unetbootin
install -c -p -m 644 unetbootin_*.qm %{buildroot}%{_datadir}/unetbootin/

# Install pixmap
install -D -p -m 644 unetbootin_512.png %{buildroot}%{_datadir}/pixmaps/unetbootin.png

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.TXT
%{_bindir}/unetbootin
%{_datadir}/unetbootin/
%{_datadir}/applications/unetbootin.desktop
%{_datadir}/pixmaps/unetbootin.png

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-14.581bzr
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-13.581bzr
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-11.581bzr
- Update to 581.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-12.577bzr
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-11.577bzr
- Update to 577.

* Tue Jun 12 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-11.575bzr
- Update to 575.

* Fri Apr 06 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-11.568bzr
- Added missing syslinux-extlinux dependency (BZ #810411).
- Update to 568.

* Fri Feb 03 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-11.565bzr
- Update to revision 565.
- Added icons (BZ #787202).

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-11.555bzr
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 01 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-10.555bzr
- Update to revision 555.

* Mon May 09 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-10.549bzr
- Bump spec.

* Thu Apr 28 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-9.549bzr
- Update to revision 549.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-9.494bzr
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 15 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-8.494bzr
- Update to revision 494. 

* Tue Jun 22 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-8.485bzr
- Update to revision 485.

* Tue Jun 22 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-8.471bzr
- Update to revision 471.

* Mon Mar 29 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-8.419bzr
- Update to revision 419.

* Wed Feb 03 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-8.393bzr
- Update to revision 393.

* Sun Dec 06 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-7.377bzr
- Update to revision 377.

* Fri Oct 23 2009 Milos Jakubicek <xjakub@fi.muni.cz> 0-6.358bzr
- Fix FTBFS: bump release to be able to tag in new branch and sync source name

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-6.357bzr
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-6.356bzr
- Add ExclusiveArch to prevent build on architectures lacking syslinux.

* Fri Jul 10 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-5.356bzr
- Fix EPEL install.

* Fri Jul 10 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-4.356bzr
- Fix EPEL build.

* Fri Jul 10 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-3.356bzr
- Added localizations.

* Fri Jul 10 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-2.356bzr
- Fixed source URL.
- Changed Req: p7zip to p7zip-plugins.
- Use included desktop file.

* Fri Jul 10 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0-1.356bzr
- First release.
