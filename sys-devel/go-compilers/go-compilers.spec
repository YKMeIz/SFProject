Name:           go-compilers
Version:        1
Release:        6%{?dist}
Summary:        Go language compilers for various architectures
Group:          Development/Tools
License:        GPLv3+
Source0:        macros.golang-compiler
Source1:        macros.gcc-go-compiler

ExclusiveArch:  %{go_arches}

# for install, cut and rm commands
BuildRequires:  coreutils
# for go specific macros
BuildRequires:  go-srpm-macros

%description
The package provides correct golang language compiler
base on an architectures.

%ifarch %{golang_arches}
%package golang-compiler
Summary:       compiler for golang

Requires:      golang

Provides:      compiler(go-compiler) = 2
Provides:      compiler(golang)

%description golang-compiler
Compiler for golang.
%endif

%ifarch %{gccgo_arches}
%package gcc-go-compiler
Summary:       compiler for gcc-go

# GCC>=5 holds in Fedora now
Requires:      gcc-go

Provides:      compiler(go-compiler) = 1
Provides:      compiler(gcc-go)

%description gcc-go-compiler
Compiler for gcc-go.
%endif

%prep
# nothing to prep, just for hooks

%build
# nothing to build, just for hooks

%install
%ifarch %{golang_arches}
install -m 644 -D %{SOURCE0} %{buildroot}%{_rpmconfigdir}/macros.d/macros.golang-compiler
%endif

%ifarch %{gccgo_arches}
install -m 644 -D %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.gcc-go-compiler
%endif

%ifarch %{golang_arches}
%files golang-compiler
%{_rpmconfigdir}/macros.d/macros.golang-compiler
%endif

%ifarch %{gccgo_arches}
%files gcc-go-compiler
%{_rpmconfigdir}/macros.d/macros.gcc-go-compiler
%endif

%changelog
* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Jakub Čajka <jcajka@redhat.com> - 1-5
- Build for {power64} switch to golang

* Fri Jan 22 2016 Jakub Čajka <jcajka@redhat.com> - 1-4
- version provides to make seamless transition between compilers possible
- Resolves: bz#1300717

* Thu Nov 12 2015 Jakub Čajka <jcajka@redhat.com> - 1-3
- remove version requirement from gcc-go subpackage to avoid cyclic
  dependency due to macro declaration in subpackage

* Thu Sep 10 2015 jchaloup <jchaloup@redhat.com> - 1-2
- go_compiler macro must be in go-srpm-macros package as it is used
  to pick compiler(go-compiler) which would provide go_compiler

* Tue Jul 07 2015 Jan Chaloupka <jchaloup@redhat.com> - 1-1
- Initial commit
  resolves: #1258182
