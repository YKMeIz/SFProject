Name:		luakit
# Upstream announces releases with dates and tarball links from github
Version:	2012.09.13.r1
Release:	1%{?dist}
Summary:	Micro-browser framework based on WebKit and GTK+

Group:		Applications/Internet
License:	GPLv3
URL:		http://luakit.org/
# From http://github.com/mason-larobina/luakit/tarball/2011.07.22-r1
Source0:	%{name}-%{version}.tar.gz
#Patch0:		luakit-glib.patch

BuildRequires:	webkitgtk-devel lua-devel help2man desktop-file-utils unique-devel libsqlite3x-devel
Requires:	lua-filesystem wget

%description
luakit is a highly configurable, micro-browser framework based on the WebKit
web content engine and the GTK+ toolkit. It is very fast, extensible by Lua
and licensed under the GNU GPLv3 license.

It is primarily targeted at power users, developers and any people with too
much time on their hands who want to have fine-grained control over their web
browsers behaviour and interface.

%prep
%setup -q -n mason-larobina-luakit-0d5f4ab
#%patch0 -p1 -b .glib
sed -i "s|-ggdb -W -Wall -Wextra|%{optflags}|g" config.mk


%build
PREFIX=%{_prefix} make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} make install
# Already available through %doc
rm -fr ${RPM_BUILD_ROOT}%{_datadir}/%{name}/docs
desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}
%{_mandir}/man1/*
%dir %{_sysconfdir}/xdg/%{name}/
%config(noreplace) %{_sysconfdir}/xdg/%{name}/*
# README.md is virtually empty as of v.2010.09.24
%doc COPYING COPYING.GPLv3 AUTHORS PATCHES

%changelog
* Thu Jul 31 2014 Nux <rpm@li.nux.ro> - 2012.09.13.r1-1
- update to 2012.09.13.r1

* Wed Aug 01 2012 Jon Ciesla <limburgher@gmail.com> - 2011.07.22.r1-5
- Tom Lane's glib fixes for libpng15 rebuild, BZ 843652.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.07.22.r1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.07.22.r1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2011.07.22.r1-2
- Rebuild for new libpng

* Tue Aug 02 2011 Pierre Carrier <pierre@spotify.com> 2011.07.22.r1-1
- New release 2011.07.22-r1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2010.09.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Pierre Carrier <prc@redhat.com> 2010.09.24-1
- Initial packaging
