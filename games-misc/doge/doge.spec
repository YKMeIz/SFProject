Name:           doge
Version:        3.5.0
Release:        1%{?dist}
Summary:        MOTD script based on the doge meme

License:        MIT
URL:            https://github.com/thiderman/doge
Source0:        https://pypi.python.org/packages/source/d/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
doge is a simple motd script based on the doge meme. It prints random
grammatically incorrect statements that are sometimes based on things from your
computer.


%prep
%setup -q
# such shebangs wow
sed -i -e '/^#!\//, 1d' doge/*.py


%build
%py3_build


%install
%py3_install

 
%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/*


%changelog
* Sun Feb 07 2016 Miro Hrončok <mhroncok@redhat.com> - 3.5.0-1
- wow many developments
- such modern
- very python 3
- much wow
- very %%license

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 05 2013 Ian Weller <iweller@redhat.com> - 2.2.0-1
- wow many developments

* Sun Oct 20 2013 Ian Weller <iweller@redhat.com> - 0.7.1-1
- such new version, many less traceback

* Sun Oct 20 2013 Ian Weller <iweller@redhat.com> - 0.6.1-2
- boo rm -rf buildroot
- such python macros

* Sat Oct 19 2013 Ian Weller <iweller@redhat.com> - 0.6.1-1
- beautiful initial package build wow
