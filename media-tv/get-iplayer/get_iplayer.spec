Name:		get_iplayer
Version:	2.94
Release:	1%{?dist}
Summary:	Lists, Records and Streams BBC iPlayer TV and Radio programmes

Group:		Applications/Internet
License:	GPLv3+
URL:		http://www.infradead.org/get_iplayer/html/get_iplayer.html
Source0:	ftp://ftp.infradead.org/pub/get_iplayer/get_iplayer-%{version}.tar.gz
Source1:	options
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	sed 
BuildRequires:	perl(Cwd) perl(Env) perl(Fcntl) perl(File::Copy) 
BuildRequires:	perl(File::Path) perl(File::stat) perl(Getopt::Long)
BuildRequires:	perl(HTML::Entities) perl(HTTP::Cookies) perl(HTTP::Headers)
BuildRequires:	perl(IO::Seekable) perl(IO::Socket) perl(LWP::ConnCache)
BuildRequires:	perl(LWP::UserAgent) perl(POSIX) perl(Time::Local) perl(URI)
BuildRequires:	perl(HTML::Entities) perl(HTTP::Cookies)
BuildRequires:  file-libs
Requires:	rtmpdump ffmpeg id3v2 lame AtomicParsley
Requires:       perl(XML::Simple)

%{?filter_setup:
# https://bugzilla.redhat.com/show_bug.cgi?id=734244
%filter_from_requires /perl(Programme.*)/d; /perl(Streamer)/d;
%filter_setup
}

%description
get_iplayer is a tool for listing, recording and streaming BBC iPlayer TV 
programmes, and other programmes via 3rd-party plugins.

%prep
%setup -q

%build
./get_iplayer --manpage=get_iplayer.1 || :

%install
rm -rf $RPM_BUILD_ROOT
install -p -D -m0755 get_iplayer $RPM_BUILD_ROOT%{_bindir}/get_iplayer
install -p -D -m0644 get_iplayer.1 $RPM_BUILD_ROOT%{_mandir}/man1/get_iplayer.1
install -p -D -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/get_iplayer/options

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/get_iplayer
%{_mandir}/man1/get_iplayer.1.*
%dir %{_sysconfdir}/get_iplayer
%config(noreplace) %{_sysconfdir}/get_iplayer/options
%doc LICENSE.txt 
%doc README.md


%changelog
* Wed Jul 08 2015 Nux <rpm@li.nux.ro> - 2.94-1
- update to 2.94

* Sat Dec 27 2014 Peter Oliver <rpm@mavit.org.uk> - 2.91-1
- Update to 2.91.

* Mon Nov  3 2014 David Woodhouse <dwmw2@infradead.org> - 2.90-1
- Update to 2.90.

* Sun Apr 20 2014 Peter Oliver <rpm@mavit.org.uk> - 2.86-1
- Update to 2.86.

* Sat Mar  8 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-8
- Bump version number.

* Fri Feb 28 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-7
- Functionality is improved if XML::Simple is installed, so add it as a
  dependency.  Bug #3137.

* Fri Feb 28 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-6
- Restore dependency filtering, required again now that
  https://bugzilla.redhat.com/show_bug.cgi?id=1051598 is fixed.  Fixes
  bug #3181.

* Sun Feb 16 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-5
- Depend on AtomicParsley (now packaged for Fedora 20).

* Thu Jan 16 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-4
- Remove workaround for RHBZ#1051607, fixed in file-libs-5.14-14.

* Sun Jan 12 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-3
- Manually list Requires.  Works around
  https://bugzilla.redhat.com/show_bug.cgi?id=1051607 and fixes
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=3068.

* Sun Jan 12 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-2
- README.txt replaced by README.md.

* Sun Jan 12 2014 Peter Oliver <rpm@mavit.org.uk> - 2.85-1
- Update to 2.85.  Fixes bug #2862.

* Sun Jan 12 2014 Peter Oliver <rpm@mavit.org.uk> - 2.80-8
- Depend on package vlc-core (which contains cvlc), not vlc.  Fixes bug #2143.

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.80-7
- Rebuilt for x264/FFmpeg

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.80-6
- Mass rebuilt for Fedora 19 Features

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.80-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.80-4
- conditionalise %%filter_setup properly.

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.80-3
- Make the requires filtering work in rpmfusion build system

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.80-2
- Remove superfluous perl requires

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.80-1
- Update to 2.80
- Add 'packagemanager yum' to options file (#1270)

* Sun Jan 09 2011 David Woodhouse <dwmw2@infradead.org> 2.79-1
- Update to 2.79

* Fri May 28 2010 David Woodhouse <dwmw2@infradead.org> 2.78-1
- Update to 2.78 (proper fix for Akamai).

* Wed May 26 2010 David Woodhouse <dwmw2@infradead.org> 2.77-3
- Add all necessary perl BuildRequires so we can generate man page

* Wed May 26 2010 David Woodhouse <dwmw2@infradead.org> 2.77-2
- BR perl(HTML::Entities) for man page

* Wed May 26 2010 David Woodhouse <dwmw2@infradead.org> 2.77-1
- Update to 2.77 (fix Limelight and Akamai RTMP downloads).

* Tue Apr 20 2010 David Woodhouse <dwmw2@infradead.org> 2.76-1
- Initial package
