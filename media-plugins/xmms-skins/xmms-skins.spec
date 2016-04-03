Summary: Skins for the X MultiMedia System
Name: xmms-skins
Version: 1.2.10
Release: 28
Epoch: 1
License: MIT and GPL+ and Copyright only and CC-BY
Group: Applications/Multimedia
URL: http://www.xmms.org/
# Yes, this is painful, but I need to do it for license tracking.
# Emailed author
# Source0: http://xmms.org/files/Skins/AbsoluteE_Xmms.zip
# GPL, according to author created Freshmeat page:
# http://themes.freshmeat.net/projects/arctic_/
Source1: http://xmms.org/files/Skins/arctic_Xmms.zip
# No idea who made these. No License.
# Source2: http://xmms.org/files/Skins/blackstar.zip
# Source3: http://xmms.org/files/Skins/BlackXMMS.zip
# Source4: http://xmms.org/files/Skins/BlueIce.zip
# MIT (derived from Enlightenment theme)
# See: http://www.erat.org/
Source5: http://xmms.org/files/Skins/BlueSteel.zip
# MIT (derived from Enlightenment theme)
Source6: http://xmms.org/files/Skins/BrushedMetal_Xmms.zip
# Derived from this work, where the author explicitly says not to redistribute.
# http://www.beyondconvention.com/ohussain/_oldsite/themes/chaos_README.txt
# Source7: http://xmms.org/files/Skins/chaos_XMMS.zip
# Copyright only
Source8: http://xmms.org/files/Skins/ColderXMMS.tar.gz
# Emailed author asking about license
# Source9: http://xmms.org/files/Skins/Covenant.zip
# GPL, according to freshmeat page created by author:
# http://freshmeat.net/projects/cyrus/
Source10: http://xmms.org/files/Skins/Cyrus-XMMS.zip
# Author (Thomas Seifried) says CC-BY is the License (confirmed via email)
Source11: http://xmms.org/files/Skins/detone_blue.zip
Source12: http://xmms.org/files/Skins/detone_green.zip
# Emailed author
# Source13: http://xmms.org/files/Skins/fyre.zip
# GPL+
Source14: http://xmms.org/files/Skins/GTK+.zip
# Author (Merlijn van der Mee) says CC-BY is the License (confirmed via email)
Source15: http://xmms.org/files/Skins/Inverse.zip
# Derived from E theme, which is under GPL
# http://ftp.univie.ac.at/pub/FreeBSD/ports/local-distfiles/vanilla/Marble.etheme
Source16: http://xmms.org/files/Skins/Marble.zip
# No idea who made this. No License.
# Source17: http://xmms.org/files/Skins/Panic.zip
# Author (Paul Rahme) gives permission for use under CC-BY (confirmed via email)
Source18: http://xmms.org/files/Skins/sinistar.zip
# Author (Anders Berg-Hansen) says CC-BY is the License (confirmed via email)
Source19: http://xmms.org/files/Skins/titanium.zip
# Author (James T. Mayled) says CC-BY is the License (confirmed via email)
Source20: http://xmms.org/files/Skins/Ultrafina-pw.zip
Source21: http://xmms.org/files/Skins/UltrafinaSE.zip
Source22: http://xmms.org/files/Skins/Ultrafina.zip
# Same author as Covenant skin (if he replies, I will ask about this one)
# Source23: http://xmms.org/files/Skins/Vulcan.zip
# Cannot find active email for Christopher Allen (copyright holder)
# http://web.archive.org/web/20050212133801/ruah.dyndns.org/~cpcallen/
# Source24: http://xmms.org/files/Skins/XawMMS.zip
# Same author as Covenant skin (if he replies, I will ask about this one)
# Source25: http://xmms.org/files/Skins/xmms-256.zip
# No idea who made these. No License.
# Source26: http://xmms.org/files/Skins/XMMS-Green.zip
# Source27: http://xmms.org/files/Skins/X-Tra.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
# Virtual provides from "compatible" players (e.g. audacious), not just xmms
Requires: xmms-gui
Obsoletes: xmmsskins <= 1.0-5

%description
This is a collection of skins for the xmms multimedia player. The
skins were obtained from http://www.xmms.org/skins.html .


%prep
%setup -q -T -c


%build


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_datadir}/xmms/Skins
%{__install} -p -m 0644 \
    %{SOURCE1}  %{SOURCE5}  %{SOURCE6}  %{SOURCE8}  %{SOURCE10} %{SOURCE11} \
    %{SOURCE12} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE18} %{SOURCE19} \
    %{SOURCE20} %{SOURCE21} %{SOURCE22} \
    %{buildroot}%{_datadir}/xmms/Skins/


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,0755)
%{_datadir}/xmms/Skins/


%changelog
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Matthias Saou <http://freshrpms.net/> 1:1.2.10-21
- Replace "xmms" requirement with "xmms-gui" which other players can provide,
  audacious for instance (#470135).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 24 2008 Matthias Saou <http://freshrpms.net/> 1:1.2.10-19
- Don't copy zip files unnecessarily during build.

* Thu Sep 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:1.2.10-18
- Ultrafina author says we can use them under CC-BY

* Tue Sep  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:1.2.10-17
- got some responses from skin creators, readded some of the removed skins

* Sat Sep  6 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:1.2.10-16
- fix license tag, remove skins where licensing is unclear

* Thu Apr 14 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-15
- Split off xmms-skins sub-package of xmms to its own package.
- Become "noarch" at last, fixes #65614.
- Add version to the xmmsskins obsoletes (1.0-5 w/o epoch was the last seen).

