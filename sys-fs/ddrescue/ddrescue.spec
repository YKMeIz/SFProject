Name:           ddrescue
Version:        1.17
Release:        1%{?dist}
Summary:        Data recovery tool trying hard to rescue data in case of read errors
Group:          Applications/System
License:        GPLv3+
URL:            http://www.gnu.org/software/ddrescue/ddrescue.html
# rpmbuild doesn't support lzip format
#Source0:        http://ftp.gnu.org/gnu/ddrescue/ddrescue-%{version}.tar.lz
# so the file has ben decompressed and recompressed to xz
Source0:        ddrescue-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   lzip
Requires(post):  info
Requires(preun): info

%description
GNU ddrescue is a data recovery tool. It copies data from one file or block
device (hard disc, cd-rom, etc) to another, trying hard to rescue data in 
case of read errors. GNU ddrescue does not truncate the output file if not
asked to. So, every time you run it on the same output file, it tries to 
fill in the gaps.

%prep
%setup -q

%build
# not a real autotools configure script, flags need to be passed specially
%configure CFLAGS="%{optflags}" CXXFLAGS="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%check
make check

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/ddrescue
%{_bindir}/ddrescuelog
%{_mandir}/man1/ddrescue.1*
%{_mandir}/man1/ddrescuelog.1*
%{_infodir}/%{name}.info*

%changelog
* Thu Sep 05 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.17-1
- Update to 1.17.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 02 2012 Michal Ambroz <rebus AT_ seznam.cz> - 1.16-1
- Update to 1.16.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.13-1
- Update to 1.13.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 22 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.8-5
- Build with $RPM_OPT_FLAGS (#497152).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.8-3
- fix license tag

* Mon Feb 25 2008 Andreas Thienemann <athienem@redhat.com> - 1.8-2
- Fix info-page installation

* Mon Feb 25 2008 Andreas Thienemann <athienem@redhat.com> - 1.8-1
- Initial fedora release of GNU ddrescue
