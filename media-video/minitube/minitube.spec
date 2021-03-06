Name:           minitube
Version:        2.3
Release:        1%{?dist}
Summary:        A YouTube desktop client
Group:          Applications/Multimedia

# License info:
#
# LGPLv2.1 with exceptions or GPLv3:
# src/iconloader/qticonloader.h
# src/iconloader/qticonloader.cpp
# src/searchlineedit.h
# src/searchlineedit.cpp
#
# LGPLv2 with exceptions or GPLv3:
# src/urllineedit.h
# src/urllineedit.cpp
#
# GPLv2 or GPLv3:
# src/flickcharm.cpp
# src/flickcharm.h
#
# LGPLv2.1:
# src/minisplitter.h
# src/minisplitter.cpp
#
# All other files are GPLv3+ as per INSTALL file
#
# End Of License info.
# The source files combined together into minitube binary are GPLv3, and the .qm files are GPLv3+

License:        GPLv3 and GPLv3+
URL:            http://flavio.tordini.org/minitube
Source0:        http://flavio.tordini.org/files/%{name}/%{name}.tar.gz
# fixes requirement on bundled qtsingleapplication
#Patch0:         minitube-qtsingleapp.patch
#Patch1:         minitube-2.0-1-disable-update-check.patch
#Patch0:         minitube-2.0-1_disable-update_qtsingleapp.patch

BuildRequires:  qt4-devel
BuildRequires:  desktop-file-utils
BuildRequires:  phonon-devel
BuildRequires:  qtsingleapplication-devel
BuildRequires:  gettext
Requires:       hicolor-icon-theme
Requires:       gstreamer-ffmpeg

%{?_qt4_version:Requires: qt4 >= %{_qt4_version}}
%description
Minitube is a YouTube desktop client.
With it you can watch YouTube videos in a new way:
you type a keyword, Minitube gives you an endless video stream.
Minitube is not about cloning the original YouTube web interface,
it aims to create a new TV-like experience.

%prep
%setup -q -n %{name}

# remove bundled copy of qtsingleapplication
#rm -rf src/qtsingleapplication

#%patch0 -p 1
#%%patch1 -p 0

%build

%{_qt4_qmake} PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications/ \
  --delete-original \
        %{buildroot}%{_datadir}/applications/%{name}.desktop

# %%find_lang 
# There is a bug in find-lang.sh (see BZ #729336)                                    
# heavily borrowed from /usr/lib/rpm/find-lang.sh                                    
find %{buildroot} -type f -o -type l|sort|sed '                                      
s:'"%{buildroot}"'::                                                                 
s:\(.*/locale/\)\([^/_]\+\)\(.*\.qm$\):%lang(\2) \1\2\3:                             
s:^\([^%].*\)::                                                                      
/^$/d' > %{name}.lang

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
%doc AUTHORS COPYING INSTALL CHANGES TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/locale

%changelog
* Mon Dec 29 2014 Nux <rpm@li.nux.ro> - 2.3-1
- update to 2.3

* Sun Aug 31 2014 S??rgio Basto <sergio@serjux.com> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Feb 06 2013 Magnus Tuominen <magnus.tuominen@gmail.com> - 2.0-1
- 2.0
- update patches

* Sun Sep 30 2012 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.9.0-1
- update to 1.9.0-1

* Fri Aug 24 2012 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.8.0-1
- 1.8.0
- clean spec file
- disable-update-patch borrowed from debian

* Fri Apr 12 2012 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.7.1-1
- 1.7.1
- removed INSTALL
- own dir
- removed legacy stuff from spec

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.7-2
- Rebuilt for c++ ABI breakage

* Fri Jan 06 2012 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.7-1
- 1.7
- new translation patch
- remove updatechecking bits

* Sat Dec 17 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.6-4
- more translation fixes

* Sun Nov 27 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.6-3
- clean spec file
- make translations work
- special thanks to killefiz @ #fedora-kde
- remove uneccesary patches

* Sat Oct 29 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.6-2
- fixed source url

* Sat Oct 29 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.6-1
- 1.6

* Sat Aug 06 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.5-1
- 1.5 to the rescue

* Thu May 19 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.4.3-1
- version bump

* Tue Apr 19 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.4.2-1
- version bump

* Wed Mar 30 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.4.1-2
- version bump
- new lang patch
- cleaned spec of comments and old patches
- update Requires to match f-15 gstreamer defaults

* Fri Feb 11 2011 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.4-1
- version bump

* Mon Dec 13 2010 Magnus Tuominen <magnus.tuominen@gmai.com> - 1.3-1
- version 1.3
- rename macedonian language code to mk_MK.ts

* Sun Oct 13 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.2-1
- version 1.2
- QString patch dropped

* Sat Aug 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.1-8
- rebuilt

* Sun Aug 15 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-7
- drop minitube-QString.patch

* Wed Aug 11 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-6
- add BR qt4-devel
- use better naming for patches
- own directories
- sort license information

* Wed Aug 11 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-5
- add lang patch by Leigh Scott
- rename locale/lat.ts to locale/lv.ts

* Mon Aug 09 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-4
- add Req: xine-lib-extras-freeworld
- add license information
- add INSTALL file
- use %%find_lang + magic on locale files
- patch to use system qtsingleapplication
- del bundled qtsingleapplication

* Wed Aug 04 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-3
- add %%post %%postun %%posttrans as suggested by Leigh Scott
- validate desktop file
- remove Req: xine-lib-extras-freeworld
- add Req: desktop-file-utils

* Wed Aug 04 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-2
- add Req: xine-lib-extras-freeworld

* Sun Aug 01 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-1
- initial build
