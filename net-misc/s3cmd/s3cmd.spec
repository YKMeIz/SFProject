%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

#%global commit b196faa51948a9c7894578389eea4e7fff76c48a
#%global shortcommit b196faa5

Name:           s3cmd
Version:        1.5.1.2
Release:        5%{dist}
Summary:        Tool for accessing Amazon Simple Storage Service

Group:          Applications/Internet
License:        GPLv2
URL:            http://s3tools.org
# git clone https://github.com/s3tools/s3cmd
# python setup.py sdist
Source0:        http://downloads.sourceforge.net/project/s3tools/s3cmd/%{version}/s3cmd-%{version}.tar.gz
Patch0:         remove-ezsetup.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%if %{!?fedora:16}%{?fedora} < 16 || %{!?rhel:7}%{?rhel} < 7
BuildRequires:  python-devel
%else
BuildRequires:  python2-devel
%endif
%if %{!?fedora:8}%{?fedora} < 8 || %{!?rhel:6}%{?rhel} < 6
# This is in standard library since 2.5
Requires:       python-elementtree
%endif
BuildRequires: python-dateutil
BuildRequires: python-setuptools
Requires: python-dateutil
Requires: python-magic

%description
S3cmd lets you copy files from/to Amazon S3
(Simple Storage Service) using a simple to use
command line client.


%prep
%setup -q -n s3cmd-%{version}
%patch0 -p1

%build


%install
rm -rf $RPM_BUILD_ROOT
S3CMD_PACKAGING=Yes python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 s3cmd.1 $RPM_BUILD_ROOT%{_mandir}/man1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/s3cmd
%{_mandir}/man1/s3cmd.1*
%{python_sitelib}/S3
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
%{python_sitelib}/s3cmd*.egg-info
%endif
%doc NEWS README.md


%changelog
* Thu Feb  5 2015 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.1.2-5
- add Requires: python-magic

* Wed Feb  4 2015 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.1.2-4
- upstream 1.5.1.2, mostly bug fixes
- remove ez_setup, add dependency on python-setuptools

* Mon Jan 12 2015 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.0-1
- upstream 1.5.0 final

* Tue Jul  1 2014 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.0-0.7.rc1
- put back dropped dist tag

* Tue Jul  1 2014 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.0-0.6.rc1
- upstream 1.5.0-rc1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.0-0.5.gitb196faa5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Mar 23 2014 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.0-0.4.git
- upstream 1.5.0-beta1 plus even newer upstream fixes

* Sun Feb 02 2014 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.0-0.3.git
- upstream 1.5.0-beta1 plus newer upstream fixes

* Wed May 29 2013 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.0-0.2.gita122d97
- more upstream bugfixes
- drop pyxattr dep, that codepath got dropped in this release

* Mon May 20 2013 Matt Domsch <mdomsch@fedoraproject.org> - 1.5.0-0.1.gitb1ae0fbe
- upstream 1.5.0-alpha3 plus fixes
- add dep on pyxattr for the --xattr option

* Tue Jun 19 2012 Matt Domsch <mdomsch@fedoraproject.org> - 1.1.0-0.4.git11e5755e
- add local MD5 cache

* Mon Jun 18 2012 Matt Domsch <mdomsch@fedoraproject.org> - 1.1.0-0.3.git7de0789d
- parallelize local->remote syncs

* Mon Jun 18 2012 Matt Domsch <mdomsch@fedoraproject.org> - 1.1.0-0.2.gitf881b162
- add hardlink / duplicate file detection support

* Fri Mar  9 2012 Matt Domsch <mdomsch@fedoraproject.org> - 1.1.0-0.1.git2dfe4a65
- build from git for mdomsch patches to s3cmd sync

* Thu Feb 23 2012 Dennis Gilmore <dennis@ausil.us> - 1.0.1-1
- update to 1.0.1 release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May 05 2011 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.0.0-3
- No hashlib hackery

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 1.0.0-1
- New upstream release

* Mon Nov 29 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.9.9.91-3
- Patch for broken f14 httplib

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.9.91-2.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Apr 28 2010 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 0.9.9.91-1.1
- Do not use sha1 from hashlib

* Sun Feb 21 2010 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.9.91-1
- New upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.9-1
- New upstream release

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.8.4-2
- Rebuild for Python 2.6

* Tue Nov 11 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.4-1
- New upstream release, URI encoding patch upstreamed

* Fri Sep 26 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.3-4
- Try 3/65536

* Fri Sep 26 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.3-3
- Whoops, forgot to actually apply the patch.

* Fri Sep 26 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.3-2
- Fix listing of directories with special characters in names

* Thu Jul 31 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.3-1
- New upstream release: Avoid running out-of-memory in MD5'ing large files.

* Fri Jul 25 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.2-1.1
- Fix a typo

* Tue Jul 15 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.2-1
- New upstream

* Fri Jul 04 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.1-3
- Be satisfied with ET provided by 2.5 python

* Fri Jul 04 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.1-2
- Added missing python-devel BR, thanks to Marek Mahut
- Packaged the Python egg file

* Wed Jul 02 2008 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 0.9.8.1-1
- Initial packaging attempt
