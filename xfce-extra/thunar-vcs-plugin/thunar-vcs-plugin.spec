# Review: https://bugzilla.redhat.com/show_bug.cgi?id=529465

Name:           thunar-vcs-plugin
Version:        0.1.4
Release:        11%{?dist}
Summary:        Version Contol System plugin for the Thunar filemanager

Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://goodies.xfce.org/projects/thunar-plugins/%{name}
Source0:        http://archive.xfce.org/src/thunar-plugins/%{name}/0.1/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  Thunar-devel >= 0.4.0
BuildRequires:  subversion-devel >= 1.5
BuildRequires:  apr-devel >= 0.9.7
BuildRequires:  e2fsprogs-devel
BuildRequires:  uuid-devel
%if 0%{?fedora} >= 12
BuildRequires:  libuuid-devel
%endif
BuildRequires:  gettext, intltool
%if 0%{?fedora} == 10
Requires:       Thunar >= 0.9.0
%else
Requires:       Thunar >= 1.0.0
%endif
Requires:       subversion
Requires:       git
# Obsolete thunar-svn-plugin for smooth upgrades
Provides:       thunar-svn-plugin = %{version}-%{release}
Obsoletes:      thunar-svn-plugin < 0.0.4-1

%description
The Thunar VCS Plugin adds Subversion and GIT actions to the context menu of 
Thunar. This gives a VCS integration to Thunar. The current features are:
* Most of the SVN actions: add, blame, checkout, cleanup, commit, copy, 
  delete, export, import, lock, log, move, properties, relocate, resolved, 
  revert, status, switch, unlock and update
* Subversion info in file properties dialog
* Basic GIT actions: add, blame, branch, clean, clone, log, move, reset, stash 
  and status

This project was formerly known as Thunar SVN Plugin.

%prep
%setup -q

%build
%configure --disable-static --enable-subversion --enable-git
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# remove libtool archive
rm $RPM_BUILD_ROOT%{_libdir}/thunarx-*/%{name}.la
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/thunarx-*/%{name}.so
%{_libexecdir}/tvp-svn-helper
%{_libexecdir}/tvp-git-helper
%{_datadir}/icons/hicolor/*/apps/subversion.png
%{_datadir}/icons/hicolor/*/apps/git.png


%changelog
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 01 2015 Kevin Fenzi <kevin@scrye.com> 0.1.4-9
- Rebuild for Xfce 4.12

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 05 2012 Kevin Fenzi <kevin@scrye.com> - 0.1.4-3
- Rebuild for Xfce 4.10

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 20 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.4-1
- Update to 0.1.4 (for Thunar >= 1.2.0)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 25 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-3
- Rebuild vor subversion 1.6

* Wed Nov 10 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-2
- Require git
- Rework description

* Tue Nov 10 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2

* Sat Oct 24 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1
- Include git icons

* Wed Sep 30 2009 Christoph Wickert <cwickert@fedoraproject.org> - 0.1.0-1
- Initial Fedora package
