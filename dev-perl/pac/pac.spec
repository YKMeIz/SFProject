Name:     pac
License:  GPL v3
Group:    Applications/System
Version:  4.5.5.5
Release:  1.1%{?dist}
Summary:  PAC Perl Auto Connector
URL:      https://sourceforge.net/projects/pacmanager
#URl:     http://opendesktop.org/content/show.php/PAC+Manager?content=125533
Source0:  %{name}-%{version}-all.tar.gz
Source1:  pac.desktop
Source2:  pac.1
Source3:  pac.png
BuildRequires: ImageMagick
AutoReqProv: no
Requires: perl-Expect perl-Gnome2-GConf perl-Gtk2 perl-Gtk2-Ex-Simple-List perl-Gtk2-GladeXML perl-Net-ARP uuid-perl 
Requires: perl-YAML perl-Crypt-Blowfish perl-IO-Stty perl-Crypt-CBC perl-Crypt-Rijndael vte perl-Socket6
BuildRoot: %{_tmppath}/%{name}-%{version}-build  

%description  
Copyright: 2010 by David Torrejón Vaquerizas, released under the GNU GPLv3 license
Gnome's SecureCRT/Putty/blah blah... equivalent (on steroids!) written in Perl/GTK.
PAC is a telnet/ssh/rsh/etc connection manager/automator written in Perl GTK
aimed at making both administrators and switchers (from Windoze) live easier.

%prep
%setup -q -n %{name}
%ifarch %{ix86}
rm -rf pac/lib/ex/vte64
%endif
%ifarch x86_64
rm -f pac/lib/ex/vte32
%endif


%build
rm -rf $RPM_BUILD_ROOT

%install
mkdir -p $RPM_BUILD_ROOT/{opt/pac,%{_bindir},%{_datadir}/{applications,man/man1}}
cp -r * $RPM_BUILD_ROOT/opt/pac
install -D -m 0644 %{S:1} $RPM_BUILD_ROOT%{_datadir}/applications/pac.desktop
install -D -m 0644 %{S:2} $RPM_BUILD_ROOT%{_datadir}/man/man1/pac.1
ln -s /opt/pac/pac $RPM_BUILD_ROOT%{_bindir}/pac

# Install icon
for res in 16x16 22x22 24x24 32x32 36x36 48x48 64x64 72x72 96x96; do \
  %{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/{${res},scalable}/apps
  convert -size 64x64 %{S:3} -resize ${res} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${res}/apps/%{name}.png
done;

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%defattr(-,root,root)
%doc README LICENSE
/opt/pac
%{_bindir}/pac
%{_datadir}/applications/pac.desktop
%{_datadir}/man/man1/pac*
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Sat Oct 10 2015 Nux <rpm@li.nux.ro> - 4.5.5.5-1
- update to 4.5.5.5

* Sat Dec 28 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 4.5.3.4-1
- update

* Sat Sep 21 2013 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 4.5.3.2-1
- update

* Tue Sep 25 2012 Muhammad Shaban <Mr.Muhammad@linuxac.org> - 4.3-2
- Initial build
