Name:		mmv
Version:	1.01b
Release:	16%{?dist}
Summary:	Move/copy/append/link multiple files

Group:          Applications/File
License:	GPL+
URL:		http://packages.qa.debian.org/m/mmv.html
Source0:	http://ftp.debian.org/debian/pool/main/m/mmv/mmv_1.01b.orig.tar.gz
Source1:	copyright
Source2:	changelog
Patch0:		mmv-1.01b-debian.patch
Patch1:		mmv-1.01b-makefile.patch
Patch2:		mmv-1.01b-debian-14.patch
Patch3:		mmv-1.01b-debian-15.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is mmv, a program to move/copy/append/link multiple files
according to a set of wildcard patterns. This multiple action is
performed safely, i.e. without any unexpected deletion of files due to
collisions of target names with existing filenames or with other
target names. Furthermore, before doing anything, mmv attempts to
detect any errors that would result from the entire set of actions
specified and gives the user the choice of either aborting before
beginning, or proceeding by avoiding the offending parts.

%prep
%setup -q -n mmv-1.01b.orig
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
cp -p %{SOURCE1} . 
cp -p %{SOURCE2} .

%build
make CONF="$RPM_OPT_FLAGS -fpie $(getconf LFS_CFLAGS)" LDCONF="-pie" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
ln -s mmv $RPM_BUILD_ROOT/%{_bindir}/mcp
ln -s mmv $RPM_BUILD_ROOT/%{_bindir}/mad
ln -s mmv $RPM_BUILD_ROOT/%{_bindir}/mln
ln -s mmv.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1/mcp.1.gz
ln -s mmv.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1/mad.1.gz
ln -s mmv.1.gz $RPM_BUILD_ROOT/%{_mandir}/man1/mln.1.gz

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%doc copyright changelog
%defattr(-,root,root,-)
%doc ANNOUNCE ARTICLE READ.ME
%{_bindir}/mmv
%{_bindir}/mcp
%{_bindir}/mad
%{_bindir}/mln
%{_mandir}/man1/*

%changelog
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01b-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01b-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01b-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  2 2009 Zing <zing@fastmail.fm> - 1.01b-13
- enable LFS support
- updated changelog and copyright files

* Mon Jun  1 2009 Zing <zing@fastmail.fm> - 1.01b-12
- sync with debian mmv_1.01b-15
-     man page formatting fixes
-     wrap cmdname in basename() (debian: #452989)
-     initialize tv_usec (debian: #452993)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01b-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.01b-10
- Autorebuild for GCC 4.3

* Thu Aug 16 2007 Zing <zing@fastmail.fm> - 1.01b-9
- conform to Fedora Licensing Guidelines

* Fri Sep  8 2006 Zing <zing@fastmail.fm> - 1.01b-8
- fix perms on man page
- rebuild for FE6

* Mon Apr 10 2006 Zing <shishz@hotpop.com> - 1.01b-7
- ok, now fix busted perms on doc directory

* Mon Mar 20 2006 Zing <shishz@hotpop.com> - 1.01b-6
- fix permissions on doc files

* Mon Feb 13 2006 Zing <shishz@hotpop.com> - 1.01b-5
- sync with debian mmv_1.01b-14
- symlink man page for mcp/mad/mln

* Sat Oct  1 2005 Zing <shishz@hotpop.com> - 1.01b-4
- use dist tag

* Sat Oct  1 2005 Zing <shishz@hotpop.com> - 1.01b-3
- cleanup changelog

* Wed Sep 28 2005 Zing <shishz@hotpop.com> - 1.01b-2
- don't change source name
- symlink mcp/mad/mln 

* Tue Aug 23 2005 Zing <shishz@hotpop.com> - 1.01b-1
- initial RPM release
- pull from debian mmv_1.01b-12.2
- build executable as a PIE
