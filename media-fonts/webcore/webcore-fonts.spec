Name: webcore-fonts
Summary: Collection of minimum popular high quality TrueType fonts
Version: 3.0
Release: 1
License: Microsoft
Group: User Interface/X
Source: http://avi.alkalay.net/software/webcore-fonts/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/build-root-%{name}
BuildArch: noarch
Packager: Avi Alkalay <avi at unix dot sh>
#Distribution:
Prefix: /usr/share/fonts
Url: http://avi.alkalay.net/linux/docs/font-howto/Font.html#msfonts
#Url: http://microsoft.com/typography
Obsoletes: msfonts

%description
Collection of high quality TrueType fonts, default in any MS Windows installation. These are also the main webfonts as specified in microsoft.com/typography
The fonts:
Andale Mono, Arial, Arial Black, Comic, Courier New, Georgia, Impact, Lucida Sans, Lucida Console, Microsoft Sans Serif, Symbol, Tahoma, Times New Roman, Trebuchet, Verdana, Webdings, Wingdings, Wingding 2, Wingding 3.



%package vista
Summary:      Collection of popular fonts distributed with MS Office 2007
Group:        User Interface/X


%description vista
Collection of high quality TrueType (OpenType) fonts available on MS Windows Vista and MS Office 2007 installations.
This fonts are usefull for document interoperability between platforms, because Microsoft is pushing them as new defaults for Office 2007 documents.

Read more at: http://neosmart.net/blog/2006/a-comprehensive-look-at-the-new-microsoft-fonts/

The fonts:
Calibri, Cambria, Candara, Consolas, Constantia, Corbel.


%prep
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT

%setup -q -n webcore-fonts

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{prefix}/webcore
mkdir -p $RPM_BUILD_ROOT/%{prefix}/webcore-vista
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/webcore-fonts
mv fonts/* $RPM_BUILD_ROOT/%{prefix}/webcore
mv vista/* $RPM_BUILD_ROOT/%{prefix}/webcore-vista
mv doc/* $RPM_BUILD_ROOT/usr/share/doc/webcore-fonts

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,0755)
%{prefix}/webcore
%doc /usr/share/doc/webcore-fonts

%files vista
%defattr(-,root,root,0755)
%{prefix}/webcore-vista


%post
{
	if test -x /sbin/conf.d/SuSEconfig.fonts ; then
		# This is a SUSE system. Use proprietary SuSE tools...
		if test "$YAST_IS_RUNNING" != "instsys" ; then
			if test -x /sbin/SuSEconfig -a -f /sbin/conf.d/SuSEconfig.fonts ; then
				/sbin/SuSEconfig --module fonts
			else
				echo -e "\nERROR: SuSEconfig or requested SuSEconfig module not present!\n" ; exit 1
			fi
		fi

		if test -x /sbin/conf.d/SuSEconfig.pango ; then
			if test "$YAST_IS_RUNNING" != "instsys" ; then 
				if test -x /sbin/SuSEconfig -a -f /sbin/conf.d/SuSEconfig.pango ; then 
					/sbin/SuSEconfig --module pango 
				else
					echo -e "\nERROR: SuSEconfig or requested SuSEconfig module not present!\n" ; exit 1 
				fi
			fi
		fi
	else
		# Use regular open standards methods...
		ttmkfdir -d %{prefix}/webcore -o %{prefix}/webcore/fonts.scale
		umask 133
		/usr/X11R6/bin/mkfontdir %{prefix}/webcore
		/usr/sbin/chkfontpath -q -a %{prefix}/webcore
		[ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache
	fi
} &> /dev/null || :
echo "See file:/usr/share/doc/webcore-fonts/index.html to get the most from this fonts"

%preun
{
	if [ "$1" = "0" ]; then
		cd %{prefix}/webcore
		rm -f fonts.dir fonts.scale fonts.cache*
	fi
} &> /dev/null || :

%postun
{
	if test -x /sbin/conf.d/SuSEconfig.fonts ; then
		# This is a SUSE system. Use proprietary SuSE tools...
		if test "$YAST_IS_RUNNING" != "instsys" ; then
			if test -x /sbin/SuSEconfig -a -f /sbin/conf.d/SuSEconfig.fonts ; then
				/sbin/SuSEconfig --module fonts
			else
				echo -e "\nERROR: SuSEconfig or requested SuSEconfig module not present!\n" ; exit 1
			fi
		fi

		if test -x /sbin/conf.d/SuSEconfig.pango ; then
			if test "$YAST_IS_RUNNING" != "instsys" ; then 
				if test -x /sbin/SuSEconfig -a -f /sbin/conf.d/SuSEconfig.pango ; then 
					/sbin/SuSEconfig --module pango 
				else
					echo -e "\nERROR: SuSEconfig or requested SuSEconfig module not present!\n" ; exit 1 
				fi
			fi
		fi
	else
		# Use regular open standards methods...
		if [ "$1" = "0" ]; then
			/usr/sbin/chkfontpath -q -r %{prefix}/webcore
		fi
		[ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache
	fi
} &> /dev/null || :









%post vista
{
	if test -x /sbin/conf.d/SuSEconfig.fonts ; then
		# This is a SUSE system. Use proprietary SuSE tools...
		if test "$YAST_IS_RUNNING" != "instsys" ; then
			if test -x /sbin/SuSEconfig -a -f /sbin/conf.d/SuSEconfig.fonts ; then
				/sbin/SuSEconfig --module fonts
			else
				echo -e "\nERROR: SuSEconfig or requested SuSEconfig module not present!\n" ; exit 1
			fi
		fi

		if test -x /sbin/conf.d/SuSEconfig.pango ; then
			if test "$YAST_IS_RUNNING" != "instsys" ; then 
				if test -x /sbin/SuSEconfig -a -f /sbin/conf.d/SuSEconfig.pango ; then 
					/sbin/SuSEconfig --module pango 
				else
					echo -e "\nERROR: SuSEconfig or requested SuSEconfig module not present!\n" ; exit 1 
				fi
			fi
		fi
	else
		# Use regular open standards methods...
		ttmkfdir -d %{prefix}/webcore-vista -o %{prefix}/webcore-vista/fonts.scale
		umask 133
		/usr/X11R6/bin/mkfontdir %{prefix}/webcore-vista
		/usr/sbin/chkfontpath -q -a %{prefix}/webcore-vista
		[ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache
	fi
} &> /dev/null || :




%preun vista
{
	if [ "$1" = "0" ]; then
		cd %{prefix}/webcore-vista
		rm -f fonts.dir fonts.scale fonts.cache*
	fi
} &> /dev/null || :




%postun vista
{
	if test -x /sbin/conf.d/SuSEconfig.fonts ; then
		# This is a SUSE system. Use proprietary SuSE tools...
		if test "$YAST_IS_RUNNING" != "instsys" ; then
			if test -x /sbin/SuSEconfig -a -f /sbin/conf.d/SuSEconfig.fonts ; then
				/sbin/SuSEconfig --module fonts
			else
				echo -e "\nERROR: SuSEconfig or requested SuSEconfig module not present!\n" ; exit 1
			fi
		fi

		if test -x /sbin/conf.d/SuSEconfig.pango ; then
			if test "$YAST_IS_RUNNING" != "instsys" ; then 
				if test -x /sbin/SuSEconfig -a -f /sbin/conf.d/SuSEconfig.pango ; then 
					/sbin/SuSEconfig --module pango 
				else
					echo -e "\nERROR: SuSEconfig or requested SuSEconfig module not present!\n" ; exit 1 
				fi
			fi
		fi
	else
		# Use regular open standards methods...
		if [ "$1" = "0" ]; then
			/usr/sbin/chkfontpath -q -r %{prefix}/webcore-vista
		fi
		[ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache
	fi
} &> /dev/null || :














%changelog
* Mon May 14 2007 Avi Alkalay <avi@unix.sh> 3.0
- Inclusion of MS Office 2007/Vista fonts
* Sun Apr 15 2007 Avi Alkalay <avi@unix.sh> 2.0
- Updated scriptlets to support installation on SUSE
- Inclusion of Wingding 2 and Wingding 3 fonts
* Mon May 31 2005 Avi Alkalay <avi@unix.sh> 1.3
- Renamed to webcore-fonts
- Completely disassociated with the -style package
* Thu Dec 14 2002 Avi Alkalay <avi@unix.sh> 1.2.1
- Included screenshots for international text
- Small fixes in the documentation
* Thu Dec 10 2002 Avi Alkalay <avi@unix.sh> 1.2
- Included documentation for public release
* Thu Oct 27 2002 Avi Alkalay <avi@unix.sh> 1.1-5
- Better support for upgrades
- Support for Red Hat 8.0 with Xft
* Thu Apr 21 2002 Avi Alkalay <avi@unix.sh> 1.1
- Added screenshots
* Thu Mar 28 2002 Avi Alkalay <avi@unix.sh> 0.6
- First packaging

