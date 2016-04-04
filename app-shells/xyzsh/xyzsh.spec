%global		repoid	60140
%undefine		_docdir_fmt

Name:			xyzsh
Version:		1.5.8
Release:		5%{?dist}
Summary:		Interactive shell and text processing tool

License:		MIT
URL:			http://sourceforge.jp/projects/xyzsh/
Source0:		http://dl.sourceforge.jp/xyzsh/%{repoid}/%{name}-%{version}.tgz

BuildRequires:	cmigemo-devel
BuildRequires:	oniguruma-devel
BuildRequires:	libedit-devel

%description
xyzsh is an interactive shell and a text processing tool.
It contains a text processing inner commands like Perl or Ruby, 
and can be used as a simple objective oriented script language.

%package		devel
Summary:		Development files for cmigemo
Group:		Development/Libraries

Requires:		%{name}%{?isa} = %{version}-%{release}

%description	devel
This package  contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

# Embed soname anyway
SOVER=$(cat configure.in | sed -n -e 's|^SO_VERSION=\([^\.][^\.]*\)\..*$|\1|p')
sed -i.soname \
	-e "/[ \t]/s|\( -o libxyzsh\.so\)| -Wl,-soname,libxyzsh.so.$SOVER \1|" \
	Makefile.in

# Don't strip binary
sed -i.strip -e '/INSTALL/s|-s -m |-m |' Makefile.in

# CRLF line terminators
touch -r README{,.stamp}
sed -i -e 's|\r||g' README
touch -r README{.stamp,}
rm -f README.stamp

# Change docdir
sed -i.docdir \
	-e '/^CFLAGS=.*DATAROOTDIR=/s|doc/xyzsh/|doc/xyzsh-%{version}/|' \
	configure

# Kill -O3
sed -i.optflags \
	-e 's|-O3|-O2|' \
	configure

%build
%configure \
	--with-migemo \
	--with-system-migemodir=%{_datadir}/cmigemo/

make %{?_smp_mflags} -k \
	CC="gcc %optflags" \
	docdir=%{_datadir}/doc/%{name}-%{version} \
	libxyzsh.so

make %{?_smp_mflags} -k \
	CC="gcc %optflags" \
	docdir=%{_datadir}/doc/%{name}-%{version} \


%install
make install \
	DESTDIR=%{buildroot} \
	INSTALL="install -p" \
	docdir=%{_datadir}/doc/%{name}-%{version}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc	AUTHORS
%doc	CHANGELOG
%doc	LICENSE
%doc	README
%lang(ja)	%doc	README.ja
%doc	USAGE
%lang(ja)	%doc	USAGE.ja

%dir	%{_sysconfdir}/%{name}
%config(noreplace)	%{_sysconfdir}/%{name}/*.xyzsh

%{_bindir}/xyzsh
%{_libdir}/libxyzsh.so.2*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/migemo.so
%{_libdir}/%{name}/migemo.xyzsh
%{_mandir}/man1/xyzsh.1*

%files	devel
%{_libdir}/libxyzsh.so
%{_includedir}/%{name}/

%changelog
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 30 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.8-1
- 1.5.8

* Thu Dec 19 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.7-1
- 1.5.7

* Tue Nov 26 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.6-1
- 1.5.6

* Wed Oct  9 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.5-1
- 1.5.5

* Tue Oct  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.4-1
- 1.5.4

* Mon Oct  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.3-1
- 1.5.3

* Thu Oct  3 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.2-1
- 1.5.2

* Wed Sep 25 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.5.1-1
- 1.5.1

* Tue Aug  6 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.8-1
- 1.4.8

* Mon Jul 22 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.5-1
- 1.4.5

* Mon Jul  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.3-1
- 1.4.3

* Tue Apr  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.2-1
- 1.4.2

* Mon Mar 18 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.1-1
- 1.4.1

* Sun Mar 10 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.4.0-1
- 1.4.0

* Fri Mar  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.9-1
- 1.3.9

* Sun Feb 10 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.8-1
- 1.3.7

* Thu Jan 24 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.2-1
- 1.3.2

* Fri Jan 18 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.3.1-1
- 1.3.1

* Tue Jan  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.9-1
- 1.2.9

* Wed Jan  2 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.7-1
- 1.2.7

* Sun Dec  9 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.5-1
- 1.2.5

* Wed Nov 14 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.2.0-1
- 1.2.0

* Sun Nov 11 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.9-1
- 1.1.9

* Wed Nov 07 2012 Mamoru TASAKA <mtasaka@fedoraproject.org> - 1.1.8-1
- Initial packaging
