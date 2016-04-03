Name:           mate-vino
Version:        0.2
Release:        1
Summary:        A solution to use Vino from mate

Group:          MATE
License:        GPL
URL:            http://diomedia.be
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       python,vino,pygobject3,pygobject3-base,gsettings-desktop-schemas

Source0:	%{name}-%{version}.tar.gz

%description
A solution to use Vino from mate


%prep
%setup -q -n %{name}-%{version}

%build

%install

install -dm 744 $RPM_BUILD_ROOT/usr/bin
install -dm 744 $RPM_BUILD_ROOT/usr/share/applications

install -pm 755 mate-vino.py $RPM_BUILD_ROOT/usr/bin/%{name}
install -pm 755 mate-vino-preferences.desktop $RPM_BUILD_ROOT/usr/share/applications/mate-vino-preferences.desktop




%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/mate-vino
%{_datadir}/applications/mate-vino-preferences.desktop

%changelog
* Tue Dec 30 2014 Nux <rpm@li.nux.ro> - 0.2-1
- initial build

