######################################################
# SpecFile: tvmaxe.spec 
# Generated: http://www.mandrivausers.ro/
# MRB-Ghiunhan Mamut
######################################################
%define use_ccache	1
%define ccachedir	~/.ccache-OOo%{mdvsuffix}
%{?_with_ccache: %global use_ccache 1}
%{?_without_ccache:	%global use_ccache 0}
%define debug_package	%{nil}
%define oname tvmaxe
%define name tv-maxe
%define version 0.11
%define release 1
%define iconsdir /usr/share/icons

Name:			%{name}
Summary:		Free television for your Linux system
Version:    	    	%{version}
Release:		%{release}%{?dist}
Source0:        	tv-maxe-0.11.tar.gz
#Patch1:			PIL.patch
Requires(post):		desktop-file-utils
Requires(postun):	desktop-file-utils
URL:            	http://code.google.com/p/tv-maxe/
Group:          	Applications/Multimedia
BuildRoot:      	%{_tmppath}/%{name}-%{version}-%{release}-buildroot 
License:        	GPLv3
Requires:       	python 
Requires:		pygtk2
Requires:		sp-auth
Requires:		libstdc++ 
Requires:		vlc 
Requires:		mplayer
Requires:		gstreamer-python
Requires:		ffmpeg
Requires:		python-imaging
Buildrequires:		ImageMagick
BuildRequires:		jpackage-utils
BuildArch:		noarch
# tvmaxe-clu in upstream now
Obsoletes:		tvmaxe-clu

%description
Free television for your Linux system

%prep 
%setup -q -n %{name}-%{version}

#%patch1 -p1 -b .PIL

%build

%install
rm -rf $RPM_BUILD_ROOT


# binaries
install -d -m 755 %{buildroot}%{_bindir}
cp %{oname} %{buildroot}%{_bindir}/%{oname}

#data
install -d -m 755 %{buildroot}%{_datadir}/%{name}
cp -avx %{name}/*?[!CHANGELOG] %{buildroot}%{_datadir}/%{name}/

#changelog
install -d -m 755 %{buildroot}%{_docdir}/%{name}
cp -avx %{name}/CHANGELOG %{buildroot}%{_docdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/
convert %{name}/%{oname}.png -size 32x32 $RPM_BUILD_ROOT%{_datadir}/icons/%{oname}.png
%__install -d -m755 %{buildroot}%{_datadir}/applications

# menu entry
cat << EOF > %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]                                                                                                                                                                                                                               
Version=1.0                                                                                                                                                                                                                                   
Encoding=UTF-8                                                                                                                                                                                                                                
Type=Application                                                                                                                                                                                                                              
Categories=AudioVideo                                                                                                                                                                                                                         
Name=TV-MAXE                                                                                                                                                                                                                                  
Comment=Free television for your Linux system.                                                                                                                                                                                                
Exec=tvmaxe                                                                                                                                                                                                                                   
Icon=/usr/share/tv-maxe/tvmaxe.png                                                                                                                                                                                                            
StartupNotify=true                                                                                                                                                                                                                            
Terminal=false    
EOF


%clean 
rm -rf $RPM_BUILD_ROOT 

%files 
%defattr(-, root, root, -)
%attr(0755,root,root) %{_bindir}/%{oname}
%{_docdir}/%{name}/CHANGELOG
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/*
%{_datadir}/icons/%{oname}.png




%changelog 
* Sat Jan 24 2015 Nux <rpm@li.nux.ro> - 0.11-1
- update to 0.11

* Sat May 03 2014 Nux <rpm@li.nux.ro> - 0.09-2
- build for EL7, add PIL patch

* Sun Jun 16 2013 Nux <rpm@li.nux.ro> - 0.09
- TV-Maxe 0.09 brings new features such:
- Theming support
- Recording (alpha stage)
- Scheduling
- Auto turn off
- Better support for .m3u8 files
- Improved UI
- Other fixes and minor improvements

* Tue Jun 12 2012 Falticska Florin <symbianflo@fastwebnet.it> 0.08-69.1stella
- new upstream release
- rebuild for stella project
- MRB-Mandriva Users.Ro

* Sat Apr 28 2012 Falticska Florin <symbianflo@fastwebnet.it> 0.07-69.1stella
- new upstream release
- rebuild for stella project
- MRB-Mandriva Users.Ro

* Fri Apr 27 2012 Mamut Ghiunhan <venerix@gmail.com> 0.07-69.1-mrb2011.0
- new upstream release
- HTTP remote control
- Separation of protocol engines and multimedia backends
- Removed recording options
- GStreamer backend support
- Faster startup ;)
- Support for streams with multiple audio tracks
- Support for multiple media sources per channel
- Channel list filtering
- Feature: saving the current channellist
- Management for deleted channels
- Auto aspect ratio option
- Extended support for RTMP streams
- Improvements in fullscreen bar info

* Sat Jan 28 2012  Falticska Florin <symbianflo@fastwebnet.it> 0.06.5-69.1stella
- new upstream release
- rebuild for stella project
- MRB-Mandriva Users.Ro

* Sat Jan 28 2012 Mamut Ghiunhan <venerix@gmail.com> 0.06.5-69.1-mrb2011.0
- new upstream release
- MRB-Mandriva Users.Ro

* Fri Jan 27 2012 Falticska Florin <symbianflo@fastwebnet.it> 0.06.4-69.1stella
- rebuild for stella project
- MRB-Mandriva Users.Ro

* Thu Aug 11 2011 Mamut Ghiunhan <venerix@gmail.com> 0.06.4-69.1-mrb2011.0
- new release
- tvmaxe now uses offline local channel lists
- added a script to update local channel lists
- added danish, russian and spanish translations
- MRB-Mandriva Users.Ro

* Tue Aug 09 2011 Mamut Ghiunhan <venerix@gmail.com> 0.06.3-69.2-mrb2011.0
- some spec improvements by symbianflo
- added mini , normal and large icons for application menu entry
- changelog is now installed in _docdir
- rebuild for 2011.0
- MRB-Mandriva Users.Ro

* Mon Aug 08 2011 Mamut Ghiunhan <venerix@gmail.com> 0.06.3-69.1-mrb2011.0
- New release
- Fixed channel lists, again
- Fixed spec with proper application naming
- MRB-Mandriva Users.Ro

* Fri Aug 05 2011 Mamut Ghiunhan <venerix@gmail.com> 0.06.2-69.1-mrb2011.0
- Rebuild for 2011.0
- MRB-Mandriva Users.Ro

* Sun Jul 24 2011 Mamut Ghiunhan <venerix@gmail.com> 0.06.2-69.1mrb2010.2
- Fixed romanian translations
- Fixed channel lists
- MRB-Mandriva Users.Ro

* Sun Jun 26 2011 Mamut Ghiunhan <venerix@gmail.com> 0.06-69.1mrb2010.2
- New release
- MRB-Mandriva Users.Ro

* Fri May 27 2011 Mamut Ghiunhan <venerix@gmail.com> 0.05-69.1mrb2010.2
- New release
- MRB-Mandriva Users.Ro

* Thu Mar 03 2011 Falticska Florin <symbianflo@fastwebnet.it> 0.04.1mrb2010.2
- New release
- MRB-Mandriva Users.Ro

* Fri Dec 03 2010 Ghiunhan Mamut  <venerix@blug.ro> tvmaxe-0.01-69.1mrb2010.1
- First release tvmaxe-0.01-69.1mrb2010.1
- Build for 2010.1 noarch
- MRB-Mandriva Users.Ro

