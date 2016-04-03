Name:		pdfchain
# Need epoch since upstream changed versioning style
Epoch:		1
Version:	0.3.3
Release:	5%{?dist}
Summary:	A GUI for pdftk
Group:		Applications/Productivity
License:	GPLv3+
URL:		http://sourceforge.net/projects/pdfchain
Source0:	http://downloads.sourceforge.net/pdfchain/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Patch to make desktop file conform to standards
Patch0:		pdfchain-desktop.patch

BuildRequires:	desktop-file-utils
BuildRequires:	gtkmm30-devel
BuildRequires:	intltool

# For dir ownership
Requires:		hicolor-icon-theme
Requires:		pdftk
Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils

%description
PDF Chain is a GUI for pdftk written with gtkmm. You can merge some pdf files
to one pdf file or split. There are also some options and tools.

%prep
%setup -q
%patch0 -p1
# Stop if files acquire content
[ -s NEWS ] && exit 1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot} 
make install DESTDIR=%{buildroot}
# Remove doc dir
rm -rf %{buildroot}%{_prefix}/doc/pdfchain
# Validate desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
# Update mime types
update-desktop-database &> /dev/null || :
# Update icon cache
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
# Update mime types
update-desktop-database &> /dev/null || :

# Update icon cache
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
# Update icon cache
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{_bindir}/pdfchain
%{_datadir}/applications/pdfchain.desktop
%{_datadir}/icons/hicolor/*/apps/pdfchain.png
%{_datadir}/pixmaps/pdfchain.png

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.3-2
- Rebuilt for c++ ABI breakage

* Sun Jan 08 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1:0.3.3-1
- Update to 0.3.3.
- Fix BZ #772434.

* Sun Nov 13 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1:0.3.2-1
- Update to 0.3.2 (BZ #753593), based on Nicholas Kudriavtsev's patch.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.123-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.123-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.123-1
- Update to 0.123.

* Wed May 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.99-3
- Added missing BR: desktop-file-utils.
- Set license as GPLv3 for now.

* Wed May 27 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.99-2
- Clean up spec file for inclusion into Fedora.

* Wed May 6 2009  Leigh Scott <leigh123linux@googlemail.com> - 0.99-1
- Initial build
