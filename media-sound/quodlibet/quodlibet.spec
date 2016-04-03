%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:		quodlibet
Version:	3.2.2
Release:	1%{?dist}
Summary:	A music management program

Group:		Applications/Multimedia
License:	GPLv2
URL:	http://code.google.com/p/quodlibet/
Source0:	https://bitbucket.org/lazka/quodlibet-files/raw/default/releases/quodlibet-%{version}.tar.gz
Source1:	README.fedora

BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig
BuildRequires:	python >= 2.6
# needed for gtk-update-icon-cache
BuildRequires:	gtk2 >= 2.6.0
# needed for py_byte_compile
BuildRequires:	python3-devel

Requires:	exfalso = %{version}-%{release}
Requires:	python-feedparser
Requires:	media-player-info
Requires:	libgpod
Requires:	udisks2
Requires:	dbus-python
Requires:	gstreamer1
Requires:	gstreamer1-plugins-base
Requires:	gstreamer1-plugins-good

%description
Quod Libet is a music management program. It provides several different ways
to view your audio library, as well as support for Internet radio and
audio feeds. It has extremely flexible metadata tag editing and searching
capabilities.
Supported file formats include Ogg Vorbis, MP3, FLAC, MOD/XM/IT, Musepack,
Wavpack, and MPEG-4 AAC.


%package -n exfalso
Summary: Tag editor for various music files
Group: Applications/Multimedia

Requires:	pkgconfig
Requires:	hicolor-icon-theme
Requires:	python >= 2.7
Requires:	python-mutagen >= 1.14
Requires:	pygobject3 >= 3.2
Requires:	gtk3 >= 3.2
Requires:	gnome-icon-theme-symbolic	

# for CDDB plugin
Requires:	python-CDDB

# for musicbrainz plugin
Requires:	python-musicbrainz2


%description -n exfalso
Ex Falso is a tag editor with the same tag editing interface as Quod Libet,
but it does not play files.
Supported file formats include Ogg Vorbis, MP3, FLAC, MOD/XM/IT, Musepack,
Wavpack, and MPEG-4 AAC.

%prep
%setup -q -n quodlibet-%{version}
cp %{S:1} .

%build
python setup.py build

%install
rm -rf %{buildroot}

%py_byte_compile %{__python} %{buildroot}%{python_sitelib}/quodlibet/plugins
python setup.py install --root=%{buildroot} --prefix=%{_prefix}

desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
	--vendor fedora				\
%endif
	--dir %{buildroot}%{_datadir}/applications		\
	--delete-original					\
	%{buildroot}%{_datadir}/applications/quodlibet.desktop
desktop-file-install \
%if 0%{?fedora} && 0%{?fedora} < 19
	--vendor fedora				\
%endif
	--dir %{buildroot}%{_datadir}/applications		\
	--delete-original					\
	%{buildroot}%{_datadir}/applications/exfalso.desktop

%{find_lang} quodlibet
%post 
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun 
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.fedora
%{_bindir}/quodlibet
%if 0%{?fedora} && 0%{?fedora} < 19
%{_datadir}/applications/fedora-quodlibet.desktop
%else
%{_datadir}/applications/quodlibet.desktop
%endif
%{_datadir}/gnome-shell/search-providers/quodlibet-search-provider.ini
%{_datadir}/pixmaps/quodlibet.png
%{_datadir}/appdata/quodlibet.appdata.xml
%{_datadir}/dbus-1/services/net.sacredchao.QuodLibet.service
%{_mandir}/man1/quodlibet.1*


%files -n exfalso -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_bindir}/exfalso
%{_bindir}/operon
%if 0%{?fedora} && 0%{?fedora} < 19
%{_datadir}/applications/fedora-exfalso.desktop
%else
%{_datadir}/applications/exfalso.desktop
%endif
%{_datadir}/pixmaps/exfalso.png
%{_mandir}/man1/exfalso.1*
%{_mandir}/man1/operon.1*
%{_datadir}/icons/hicolor/64x64/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/appdata/exfalso.appdata.xml

%{python_sitelib}/quodlibet-%{version}-py2.7.egg-info
%{python_sitelib}/quodlibet

%changelog
* Sat Oct 04 2014 Johannes Lips <hannes@fedoraproject.org> - 3.2.2-1
- update to recent upstream bugfix release 3.2.2

* Sun Aug 17 2014 Johannes Lips <hannes@fedoraproject.org> - 3.2.1-1
- update to recent upstream bugfix release 3.2.1

* Sat Aug 02 2014 Johannes Lips <hannes@fedoraproject.org> - 3.2-1
- update to recent upstream release 3.2

* Sun Jun 22 2014 Johannes Lips <hannes@fedoraproject.org> - 3.1.2-1
- update to recent upstream release 3.1.2

* Fri Jun 13 2014 Johannes Lips <hannes@fedoraproject.org> - 3.1.1-3
- fixed bug #1109275 by moving quodlibet-search-provider.ini

* Mon Apr 28 2014 Johannes Lips <hannes@fedoraproject.org> - 3.1.1-1
- update to recent upstream release 3.1.1

* Sat Apr 12 2014 Johannes Lips <hannes@fedoraproject.org> - 3.1.0-1
- update to recent upstream release 3.1.0

* Sat Aug 24 2013 Johannes Lips <hannes@fedoraproject.org> - 3.0.2-1
- update to recent upstream release 3.0.2
- switch to gtk3

* Sun Aug 04 2013 Johannes Lips <hannes@fedoraproject.org> - 2.6.2-1
- update to recent upstream release 2.6.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 23 2013 Johannes Lips <hannes@fedoraproject.org> - 2.6.0-1
- update to recent upstream release 2.6.0

* Wed Apr 24 2013 Johannes Lips <hannes@fedoraproject.org> - 2.5.1-1
- update to recent upstream release 2.5.1

* Sat Feb 23 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2.5-4
- Remove --vendor from desktop-file-install for F19 https://fedorahosted.org/fesco/ticket/107

* Sat Feb 23 2013 Johannes Lips <hannes@fedoraproject.org> - 2.5-3
- add patch to fix bug #891776

* Wed Feb 06 2013 Johannes Lips <hannes@fedoraproject.org> - 2.5-2
- add udisks as requirement to fix bug #904212

* Sat Dec 22 2012 Johannes Lips <hannes@fedoraproject.org> - 2.5-1
- update to recent upstream release 2.5

* Mon Jul 30 2012 Johannes Lips <hannes@fedoraproject.org> - 2.4.1-1
- Update to recent upstream release 2.4.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 18 2012 Johannes Lips <hannes@fedoraproject.org> - 2.4-1
- Update to recent upstream release

* Tue Jan 17 2012 Johannes Lips <hannes@fedoraproject.org> - 2.3.92-1
- Update to recent upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Johannes Lips <hannes@fedoraproject.org> - 2.3.2-1
- Update to recent upstream release

* Sun Jul 17 2011 Johannes Lips <hannes@fedoraproject.org> - 2.3.1-1
- Update to recent upstream release

* Sat Apr 02 2011 Johannes Lips <hannes@fedoraproject.org> - 2.3-2
- split the package into quodlibet and an exfalso subpackage

* Sat Apr 02 2011 Johannes Lips <hannes@fedoraproject.org> - 2.3-1
- Update to 2.3
- added the requirements python-feedparser, media-player-info and python-musicbrainz2 #688602

* Fri Jul 23 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.1-3
- Fix issue building with Python 2.7

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Apr 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.2.1-1
- Update to 2.2.1

* Wed Oct 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1-3
- Require gstreamer-plugins-good - BZ#531664

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 2.1-1
- Update to 2.1 based on patches to spec by Andrew Nayenko

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0-5
- Rebuild for Python 2.6

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-4
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-3
- Autorebuild for GCC 4.3

* Mon Jul 09 2007 Todd Zullinger <tmz@pobox.com> - 1.0-2
- Small fix for changes in python-gpod-0.5.2
- Fix some desktop-file-install warning and errors

* Thu May 10 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0-1
- Update to 1.0

* Sat Apr 14 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.24-7
- Add requires on gnome-python2-canvas, fixes #236468

* Sun Mar  4 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.24-6
- Update plugins

* Mon Jan 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.24-5
- Build iPod support on FC-6

* Tue Dec 12 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.24-4
- Require python-CDDB for CDDB plugin
- Conditionalize python-gpod support

* Mon Dec 11 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.24-2
- Require python-gpod for iPod device support

* Tue Nov 21 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.24-1
- Update to 0.24

* Mon Aug 28 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.23.1-1
- Update to 0.23.1

* Thu Aug 24 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.23-5
- Include a README.fedora

* Thu Aug 17 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.23-4
- Instead of manually copying all of the plugins, pack them into a
  tarball and include a script for generating the tarball

* Wed Aug 16 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.23-3
- Make sure that %%{_libdir}/quodlibet/ is owned

* Tue Aug 15 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.23-2
- Convert tabs to spaces.
- Add shell plugin
- Get rid of some shebang lines.
- Add Google search plugin

* Fri Aug 11 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 0.23-1
- First version for Fedora Extras
