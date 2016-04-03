%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pyrenamer
Version:        0.6.0
Release:        13%{?dist}
Summary:        A mass file renamer

Group:          Applications/File
License:        GPLv2+
URL:            http://www.infinicode.org/code/pyrenamer/
#Source URL is invalid, not present upstream.
Source0:        http://www.infinicode.org/code/pyrenamer/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:       noarch
BuildRequires:   gettext desktop-file-utils pygtk2-devel GConf2-devel
BuildRequires:   perl(XML::Parser) python-eyed3 python-exif
Requires:        pygtk2 python-eyed3 gnome-python2-gconf pygtk2-libglade
Requires:        python-exif
# TO-DO : Add requires to hachoir-{core,parser,metadata} that aren't package

Requires(pre):   GConf2
Requires(post):  GConf2
Requires(preun): GConf2

%description
With pyRenamer you can change the name of several files at the same time 
easily.
 - You can use patterns to rename files.
 - You can use search & replace to rename files.
 - You can use common substitutions.
 - You can manually rename selected files.
 - You can rename images using their EXIF tags.
 - You can rename MP3s using their ID3 tags.

%prep
%setup -q -n %{name}-0.6.0


%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
desktop-file-install \
  --delete-original                                        \
  --dir=%{buildroot}%{_datadir}/applications               \
  %{buildroot}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

 
%clean
rm -rf $RPM_BUILD_ROOT


%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}.schemas >/dev/null || :
fi


%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :


%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{python_sitelib}/%{name}
%config(noreplace) %{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_docdir}/%{name}
%{_mandir}/man1/%{name}.1.*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/%{name}


%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 11 2013 Jon Ciesla <limburgher@gmail.com> - 0.6.0-11
- Drop desktop vendor tag.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Jon Ciesla <limb@jcomserv.net> - 0.6.0-8
- Bump and rebuild for BZ 712251.

* Wed Apr 27 2011 Jon Ciesla <limb@jcomserv.net> - 0.6.0-7
- Revert to 0.6.0, 0.6.0.1 unavailable.  No Epoch bump, not in repo.
- Made .schemas noreplace.
- Wildcarded manpage compression format.

* Wed Apr 20 2011 Jon Ciesla <limb@jcomserv.net> - 0.6.0.1-6
- Dropped PyGTK from description.

* Tue Apr 19 2011 Jon Ciesla <limb@jcomserv.net> - 0.6.0.1-5
- Commented bad Source URL.
- Fixed macro in changelog.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar  4 2009 Caolán McNamara <caolanm@redhat.com> - 0.6.0.1-3
- unpacks into pyrenamer-0.6.0 not pyrenamer-%%{version}

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Jean-François Martin <lokthare@gmail.com> - 0.6.0.1-1
- Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.6.0-2
- Rebuild for Python 2.6

* Wed Oct  1 2008 Jean-François Martin <lokthare@gmail.com> 0.6.0-1
- Update to new upstream release

* Fri May 30 2008 Jean-François Martin <lokthare@gmail.com> 0.5.0-4
- Fix Requires : Add gnome-python2-gconf and pygtk2-libglade

* Wed May 28 2008 Jean-François Martin <lokthare@gmail.com> 0.5.0-3
- Fix BR: Add python-eyed3
- Reorder to match spec file convention

* Tue May 27 2008 Jean-François Martin <lokthare@gmail.com> 0.5.0-2
- Fix BR: Add perl(XML::Parser).

* Tue May 27 2008 Jean-François Martin <lokthare@gmail.com> 0.5.0-1
- First RPM release.
