%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           notify-python
Version:        0.1.1
Release:        25%{?dist}
Summary:        Python bindings for libnotify

Group:          Development/Languages
# No version specified, just COPYING.
License:        LGPLv2+
URL:            http://www.galago-project.org
Source0:        http://www.galago-project.org/files/releases/source/notify-python/notify-python-%{version}.tar.bz2
Patch0:         notify-python-0.1.1-fix-GTK-symbols.patch
Patch1:         libnotify07.patch

BuildRequires:  python-devel, pkgconfig
BuildRequires:  libnotify-devel >= 0.7.0
BuildRequires:  pygtk2-devel
BuildRequires:  gtk2-devel, dbus-devel, dbus-glib-devel
BuildRequires:  autoconf

Requires:   libnotify >= 0.4.3
Requires:   desktop-notification-daemon

%global pypkgname pynotify

%description
Python bindings for libnotify

%prep
%setup -q
%patch0 -p1 -b .fix-GTK-symbols
%patch1 -p1 -b .libnotify07

# WARNING - we touch src/pynotify.override in build because upstream did not rebuild pynotify.c
# from the input definitions, this forces pynotify.c to be regenerated, at some point this can be removed

%build
export PYTHON=%{__python}
autoconf

%configure
touch src/pynotify.override
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# remove unnecessary la file
rm $RPM_BUILD_ROOT/%{python_sitearch}/gtk-2.0/%{pypkgname}/_%{pypkgname}.la
mkdir -p examples
install -m 0644 -t examples tests/*.py tests/*.png

 
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS ChangeLog
%doc examples
%{python_sitearch}/gtk-2.0/%{pypkgname}
%{_datadir}/pygtk/2.0/defs/%{pypkgname}.defs
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Aug 15 2013 Paul W. Frields <stickster@gmail.com> - 0.1.1-25
- Fix missing BuildRequires: autoconf

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Paul W. Frields <stickster@gmail.com> - 0.1.1-23
- Use autoreconf to fix for aarch64 (#926243)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 0.1.1-19
- Rebuild to break bogus libpng dep

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Paul W. Frields <stickster@gmail.com> - 0.1.1-17
- Add tests to package as API examples

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.1-16
- Rebuild against libnotify 0.7.0. API change!

* Thu Sep  9 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1.1-15
- fix init.py so that it is able to load the needed GTK2 symbols from pygtk (bz 626852)

* Fri Jul 30 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.1-14
- Remove the previous workaround (no longer needed)

* Fri Jul 30 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.1.1-13
- Workaround for bug 618944

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Feb 25 2010 John Dennis <jdennis@redhat.com> - 0.1.1-10
- spec file clean-ups reported during RHEL-6 import review
  replace define with global
  remove URL tag, there is no project URL, it had been pointing to a page with package specification
  remove unnecessary use of CFLAGS
  export PYTHON environment variable pointing to interpreter
  install COPYING AUTHORS NEWS README ChangeLog into docdir

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.1.1-9
- Use bzipped upstream tarball.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  1 2009 John Dennis <jdennis@redhat.com> - 0.1.1-7
- change requires of notification-daemon to desktop-notification-daemon as per bug #500586

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1.1-5
- Rebuild for Python 2.6

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.1.1-4
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.1.1-3
- Autorebuild for GCC 4.3

* Fri Jan  4 2008  <jdennis@redhat.com> - 0.1.1-2
- Resolves bug# 427499: attach_to_status_icon not created
  force regeneration of pynotify.c

* Wed Jan  2 2008 John Dennis <jdennis@redhat.com> - 0.1.1-1
- upgrade to current upstream
- no longer remove package config file (notify-python.pc), resolves bug #427001

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.1.0-4
- rebuild for python 2.5

* Tue Aug 15 2006 Luke Macken <lmacken@redhat.com> - 0.1.0-3
- Add notify-python-0.1.0-attach_to_status_icon.patch to allow the attaching
  notifications to status icons.

* Thu Jul 20 2006 John Dennis <jdennis@redhat.com> - 0.1.0-2
- change use of python_sitelib to python_sitearch, add BuildRequires

* Wed Jul 19 2006 John Dennis <jdennis@redhat.com> - 0.1.0-1
- Initial build

