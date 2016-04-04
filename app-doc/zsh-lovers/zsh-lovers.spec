Name:           zsh-lovers
Version:        0.9.0
Release:        1%{?dist}
Summary:        A collection of tips, tricks and examples for the Z shell
License:        GPLv2
URL:            http://grml.org/zsh/#zshlovers
Source0:        http://deb.grml.org/pool/main/z/zsh-lovers/zsh-lovers_%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  asciidoc

%description
zsh-lovers is a small project which tries to collect tips, tricks and examples
for the Z shell. 

This package only ships a manpage of the collection.

%prep
%setup -q

%build
a2x -vv -L -f manpage zsh-lovers.1.txt

%install
install -pDm644 zsh-lovers.1 %{buildroot}%{_mandir}/man1/zsh-lovers.1

%files
%doc COPYING README
%{_mandir}/man1/zsh-lovers.1*

%changelog
* Mon Apr 21 2014 Christopher Meng <rpm@cicku.me> - 0.9.0-1
- Initial Package.
