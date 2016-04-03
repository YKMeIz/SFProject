Summary:   Command-line program to read and set MPEG-4 tags compatible with iPod/iTunes 
URL:       http://atomicparsley.sourceforge.net/
Name:      AtomicParsley
Version:   0.9.5
Release:   2%{?dist}
License:   GPLv2+
Group:     Applications/Multimedia
Source0:   https://bitbucket.org/wez/atomicparsley/overview/%{name}-%{version}.tar.gz
#Patch0:    %{name}-fix_bad_math.patch
BuildRequires: autoconf
BuildRequires: automake

# Need the following to not fail on Koji build on x86_64
BuildRequires: zlib-devel



%description
AtomicParsley is a command line program for reading, parsing and setting
tags and meta-data into MPEG-4 files supporting these styles of meta-data:

* iTunes-style meta-data into .mp4, .m4a, .m4p, .m4v, .m4b files
* 3gp-style assets (3GPP TS 26.444 version 6.4.0 Release 6 specification
  conforming) in 3GPP, 3GPP2, MobileMP4 & derivatives
* ISO copyright notices at movie & track level for MPEG-4 & derivative files
* uuid private user extension text & file embedding for MPEG-4 & derivative
  files


%prep
%setup -q

%build
./autogen.sh
%configure --prefix=%{_prefix}
#OPTFLAGS="%{optflags} -Wall -Wno-parentheses -Wno-unused-result -Wno-write-strings -Wno-deprecated -fno-strict-aliasing" \
make %{?_smp_mflags}

%install
make install install DESTDIR=%{buildroot} BINDIR=%{_bindir}
#install -D -m0755 AtomicParsley "%{buildroot}%{_bindir}/AtomicParsley"


%files
%doc COPYING Changes.txt tools/iTunMOVI-1.1.pl
%{_bindir}/AtomicParsley

%changelog
* Wed Jan 29 2014 Avi Alkalay <avi@unix.sh> 0.9.5-2
- Updated from new upstream on https://bitbucket.org/wez/atomicparsley
- Added BuildRequires for zlib-devel, for Koji

* Tue Jan 28 2014 Avi Alkalay <avi@unix.sh> 0.9.0-13
- Reduced warnings
- Adapted SPEC to build on Fedora 20

* Mon Oct 01 2012 Avi Alkalay <avi@unix.sh> 0.9.0-12
- Editing with comments from https://bugzilla.redhat.com/show_bug.cgi?id=800284#c7

* Mon Oct 01 2012 Avi Alkalay <avi@unix.sh> 0.9.0-11
- Editing with comments from https://bugzilla.redhat.com/show_bug.cgi?id=800284#c5

* Tue Sep 25 2012 Avi Alkalay <avi@unix.sh> 0.9.0-10
- Editing with comments from https://bugzilla.redhat.com/show_bug.cgi?id=800284#c3

* Fri Mar 02 2012 Avi Alkalay <avi@unix.sh> 0.9.0-9
- Editing with comments from https://bugzilla.rpmfusion.org/show_bug.cgi?id=2190#c1

* Wed Feb 22 2012 Avi Alkalay <avi@unix.sh> 0.9.0-7
- RPM and patches adapted and built for Fedora 16 based on Madriva SRPM

* Thu Jul 22 2010 pascal@links2linux.de
- initial package (0.9.0)

