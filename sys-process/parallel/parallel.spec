Summary:	Shell tool for executing jobs in parallel
Name:		parallel
Version:	20160222
Release:	1%{?dist}
License:	GPLv3+
Group:		Applications/Productivity
URL:		http://www.gnu.org/software/parallel/
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.bz2
BuildArch:	noarch

# Due to a naming conflict, both packages cannot be installed in parallel
# To prevent user confusion, GNU parallel is installed in a compatibility
# mode to be commandline compatible to moreutils' parallel.
# This mode can be turned off system wide or on a per-user base.
Conflicts: moreutils-parallel

%description
GNU Parallel is a shell tool for executing jobs in parallel using one or more
machines. A job is typically a single command or a small script that has to be
run for each of the lines in the input. The typical input is a list of files, a
list of hosts, a list of users, or a list of tables.

If you use xargs today you will find GNU Parallel very easy to use. If you
write loops in shell, you will find GNU Parallel may be able to replace most of
the loops and make them run faster by running jobs in parallel. If you use ppss
or pexec you will find GNU Parallel will often make the command easier to read.

GNU Parallel also makes sure output from the commands is the same output as you
would get had you run the commands sequentially. This makes it possible to use
output from GNU Parallel as input for other programs.

GNU Parallel is command-line-compatible with moreutils' parallel, but offers
additional features.

%prep

%setup -q

%build

%configure 
make %{?_smp_mflags}

%install

make install DESTDIR=%{buildroot}

find %{buildroot} -iname "*.html" -delete
find %{buildroot} -iname "*.texi" -delete
find %{buildroot} -iname "*.pod" -delete
find %{buildroot} -iname "*.pdf" -delete
mv %{buildroot}%{_mandir}/man1/sql.1 %{buildroot}%{_mandir}/man1/parallel-sql.1

%files

%{_bindir}/parallel
%{_bindir}/sem
%{_bindir}/sql
%{_bindir}/niceload
%{_mandir}/man*/niceload.*.*
%{_mandir}/man*/parallel.*.*
%{_mandir}/man*/sem.*.*
%{_mandir}/man*/parallel-sql.*.*
%{_mandir}/man*/parallel_tutorial.*.*
%{_mandir}/man*/parallel_design.*.gz

%doc README NEWS COPYING src/parallel.html src/sem.html src/sql.html 
%doc src/niceload.html src/*.texi
%doc src/niceload.pdf src/parallel.pdf src/parallel_tutorial.pdf src/sem.pdf src/sql.pdf

%changelog
* Mon Apr 04 2016 Golo Fuchert <packages@golotop.de> 20160222-1
- Update to version 20160222-1 to fix bugs (#1285888,1307846,1320511,1320956,1320958)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20141122-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20141122-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 03 2014 Golo Fuchert <packages@golotop.de> 20141122-1
- Updated to newest version 20141122

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20131222-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan 22 2014 Golo Fuchert <packages@golotop.de> 20131222-2
- Corrected typo in changelog
- Removed directory, which is no longer needed

* Sun Jan 19 2014 Golo Fuchert <packages@golotop.de> 20131222-1
- Updated to newest versoin 20131222
- Removed patches that are no longer needed (see below for details)
- Remvoal of parallel-config, feature deprecated
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130522-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 20130522-3
- Perl 5.18 rebuild
* Thu Jun 13 2013 Golo Fuchert <packages@golotop.de> - 20130522-2
- Patch of parallel.pod due to new syntax 
* Wed May 22 2013 Golo Fuchert <packages@golotop.de> - 20130522-1
- Updated to newest version 20130522 
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20121222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
* Wed Jan 16 2013 Golo Fuchert <packages@golotop.de> - 20121222-1
- Updated to newest version 20121222 (due to #895971)
* Wed Mar 21 2012 Golo Fuchert <packages@golotop.de> - 20120222-1
- Updated to newest version 20120222
- renamed manpage sql to parallel-sql (naming conflict, bug 797823)
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20110722-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Fri Sep 09 2011 Golo Fuchert <packages@golotop.de> - 20110722-3
- Added niceload.html to doc
* Fri Sep 09 2011 Golo Fuchert <packages@golotop.de> - 20110722-2
- Minor cosmetic changes and consistent macro usage
* Sat Aug 13 2011 Golo Fuchert <packages@golotop.de> - 20110722-1
- Updated to newest version 20110722
* Sun May 22 2011 Golo Fuchert <packages@golotop.de> - 20110522-1
- Update to version 20110522
- Conflict with moreutils-parallel
- Incl. config file to make gnu parallel compatible with moreutils' by default
- Added a comment to the description, concerning the moreutils compatibility
* Sun Feb 6 2011 Golo Fuchert <packages@golotop.de> - 20110205-1
- Initial package. Based on a package by Ole Tange and Markus Ammer.
