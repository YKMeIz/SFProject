%bcond_without bdb
%bcond_without ldap
%bcond_without mysql
%bcond_without postgres
%bcond_without mdb
%bcond_without java

%global apiver  5.0
%global libgda4_obsoletes_version 1:4.2.13-3

Name:           libgda
Epoch:          1
Version:        5.1.2
Release:        4%{?dist}
Summary:        Library for writing gnome database programs

License:        LGPLv2+
URL:            http://www.gnome-db.org/
Source:         http://ftp.gnome.org/pub/GNOME/sources/%{name}/5.1/%{name}-%{version}.tar.xz
# Build system workaround
# https://bugzilla.redhat.com/show_bug.cgi?id=904790
Patch0:         0001-workaround-RHBZ-904790.patch

BuildRequires:    pkgconfig >= 0.8
BuildRequires:    glib2-devel >= 2.28.0
BuildRequires:    gtk3-devel >= 3.0.0
BuildRequires:    gtksourceview3-devel
BuildRequires:    goocanvas2-devel
BuildRequires:    graphviz-devel >= 2.26.0
BuildRequires:    iso-codes >= 3.15
BuildRequires:    libxslt-devel >= 1.0.9
BuildRequires:    sqlite-devel >= 3.6.11
BuildRequires:    libgcrypt-devel
BuildRequires:    gobject-introspection-devel >= 0.6.5
BuildRequires:    libxml2-devel readline-devel json-glib-devel
BuildRequires:    gtk-doc intltool gettext flex bison perl(XML::Parser)
BuildRequires:    libsoup-devel
BuildRequires:    gnome-doc-utils
BuildRequires:    openssl-devel
BuildRequires:    libgnome-keyring-devel
%{?with_bdb:BuildRequires:    libdb-devel, libdb-sql-devel}
%{?with_ldap:BuildRequires:    openldap-devel}
%{?with_mysql:BuildRequires:    mysql-devel}
%{?with_postgres:BuildRequires:    postgresql-devel}
%{?with_mdb:BuildRequires:    mdbtools-devel}
%{?with_java:BuildRequires:    java-devel >= 1:1.6.0}

%description
%{name} is a library that eases the task of writing Gtk3-based database
programs.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Obsoletes:      libgda-java-devel < %{libgda4_obsoletes_version}
Obsoletes:      libgda-ldap-devel < %{libgda4_obsoletes_version}
Obsoletes:      libgda-mdb-devel < %{libgda4_obsoletes_version}
Obsoletes:      libgda-mysql-devel < %{libgda4_obsoletes_version}
Obsoletes:      libgda-postgres-devel < %{libgda4_obsoletes_version}
Obsoletes:      libgda-sqlcipher-devel < %{libgda4_obsoletes_version}
Obsoletes:      libgda-sqlite-devel < %{libgda4_obsoletes_version}
Obsoletes:      libgda-web-devel < %{libgda4_obsoletes_version}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package ui
Summary:         UI extensions for %{name}
Group:           Development/Libraries
Requires:        %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description ui
%{name}-ui extends %{name} providing graphical widgets (Gtk+).

%package        ui-devel
Summary:        Development files for %{name}-ui
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-ui%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       gtk3-devel%{?_isa} >= 3.0.0

%description    ui-devel
The %{name}-ui-devel package contains libraries and header files for
developing applications that use %{name}-ui.

%package tools
Summary:         Graphical tools for %{name}
Group:           Applications/Databases
Requires:        %{name}-ui%{?_isa} = %{epoch}:%{version}-%{release}

%description tools
This %{name}-tools package provides graphical tools for %{name}.

%package sqlite
Summary:        SQLite provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}
Requires:       sqlite%{?isa} >= 3.6.11

%description sqlite
This %{name}-sqlite includes the %{name} SQLite provider.

%if 0%{with bdb}
%package bdb
Summary:        Berkeley DB provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}

%description bdb
This %{name}-bdb includes the %{name} Berkeley DB provider.
%endif

%if 0%{with ldap}
%package ldap
Summary:        Ldap provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}

%description ldap
This %{name}-ldap includes the %{name} Ldap provider.
%endif

%package sqlcipher
Summary:        SQLiteCipher provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}

%description sqlcipher
This %{name}-sqlcipher includes the %{name} SQLiteCipher provider.
%package web
Summary:        Web provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}

%description web
This %{name}-web includes the %{name} Web provider.

%if 0%{with mysql}
%package mysql
Summary:        Mysql provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}

%description mysql
This %{name}-mysql includes the %{name} Mysql provider.
%endif

%if 0%{with postgres}
%package postgres
Summary:        Postgres provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}

%description postgres
This %{name}-postgres includes the %{name} PostgreSQL provider.
%endif

%if 0%{with mdb}
%package mdb
Summary:        Mdb provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}

%description mdb
This %{name}-mdb includes the %{name} Mdb provider.
%endif

%if 0%{with java}
%package java
Summary:        Java provider for %{name}
Group:          System Environment/Libraries
Requires:       %{name}%{?isa} = %{epoch}:%{version}-%{release}

%description java
This %{name}-java includes the %{name} Java JDBC provider.
%endif


%prep
%setup -q
%patch0 -p1 -b .configure

# AUTHORS not in UTF-8
iconv --from=ISO-8859-1 --to=UTF-8 AUTHORS > AUTHORS.new && \
touch -r AUTHORS AUTHORS.new && mv AUTHORS.new AUTHORS

%build
# set LD_LIBRARY_PATH manually since it fails to find libjvm with java7
%if 0%{with java}
# this list should match the setup in java-1.7.0-openjdk.spec
# or getsp.java should be fixed
%ifarch x86_64
%global archinstall amd64
%endif
%ifarch %{ix86}
%global archinstall i386
%endif
%ifarch ppc
%global archinstall ppc
%endif
%ifarch ppc64
%global archinstall ppc64
%endif
%ifarch ia64
%global archinstall ia64
%endif
%ifarch s390
%global archinstall s390
%endif
%ifarch s390x
%global archinstall s390x
%endif
%ifarch %{arm}
%global archinstall arm
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archinstall sparc
%endif
# 64 bit sparc
%ifarch sparc64
%global archinstall sparcv9
%endif
export LD_LIBRARY_PATH=/usr/lib/jvm/java/jre/lib/%{archinstall}/server:$LD_LIBRARY_PATH
%endif
# vala support has not been tested yet so it is not enabled yet
# G-I-R is disabled since it's broken
%configure --disable-static --enable-vala=no \
           --disable-scrollkeeper \
           --with-libsoup  --with-gnome-keyring \
           --with-ui --with-gtksourceview \
           --with-goocanvas --with-graphviz \
           --enable-gda-gi \
           --enable-gdaui-gi \
           --enable-system-sqlite=yes \
           %{?with_bdb:--with-bdb=yes --with-bdb-libdir-name=%{_lib}} \
           %{!?with_ldap:--with-ldap=no} \
           %{!?with_mysql:--with-mysql=no} \
           %{!?with_postgres:--with-postgresql=no} \
           %{!?with_mdb:--with-mdb=no} \
           %{!?with_java:--with-java=no}
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
rm %{buildroot}/%{_sysconfdir}/%{name}-%{apiver}/sales_test.db

%find_lang libgda-5.0

%post -p /sbin/ldconfig
%post ui -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun ui -p /sbin/ldconfig

%post tools
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun tools
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans tools
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f libgda-5.0.lang
%doc AUTHORS COPYING ChangeLog README NEWS
%dir %{_sysconfdir}/%{name}-%{apiver}/
%config(noreplace) %{_sysconfdir}/%{name}-%{apiver}/config
%{_libdir}/%{name}-%{apiver}.so.*
%{_libdir}/%{name}-report-%{apiver}.so.*
%{_libdir}/%{name}-xslt-%{apiver}.so.*
%dir %{_libdir}/%{name}-%{apiver}/
%dir %{_libdir}/%{name}-%{apiver}/plugins/
%dir %{_libdir}/%{name}-%{apiver}/providers/
%{_libdir}/girepository-1.0/Gda-%{apiver}.typelib
%{_mandir}/man1/*
%dir %{_datadir}/%{name}-%{apiver}/
%dir %{_datadir}/%{name}-%{apiver}/dtd/
%{_datadir}/%{name}-%{apiver}/dtd/libgda-*.dtd
%{_datadir}/%{name}-%{apiver}/import_encodings.xml
%{_datadir}/%{name}-%{apiver}/information_schema.xml

%files devel
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%doc %{_datadir}/gtk-doc/html/%{name}-%{apiver}
%dir %{_datadir}/gnome/
%dir %{_datadir}/gnome/help/
%doc %{_datadir}/gnome/help/gda-sql/
%{_datadir}/gir-1.0/Gda-%{apiver}.gir
%dir %{_includedir}/%{name}-%{apiver}/
%{_includedir}/%{name}-%{apiver}/%{name}
%{_includedir}/%{name}-%{apiver}/%{name}-xslt
%{_includedir}/%{name}-%{apiver}/%{name}-report
%{_libdir}/%{name}-%{apiver}.so
%{_libdir}/%{name}-report-%{apiver}.so
%{_libdir}/%{name}-xslt-%{apiver}.so
%{_libdir}/pkgconfig/%{name}-%{apiver}.pc
%{_libdir}/pkgconfig/%{name}-*-%{apiver}.pc
%exclude %{_libdir}/pkgconfig/%{name}-ui-%{apiver}.pc

%files ui
%{_libdir}/%{name}-ui-%{apiver}.so.*
%{_libdir}/%{name}-%{apiver}/plugins/*.xml
%{_libdir}/girepository-1.0/Gdaui-%{apiver}.typelib
%{_datadir}/%{name}-%{apiver}/pixmaps
%{_datadir}/%{name}-%{apiver}/dtd/gdaui-layout.dtd
%{_datadir}/%{name}-%{apiver}/ui/
%{_datadir}/%{name}-%{apiver}/icons/
%{_datadir}/%{name}-%{apiver}/server_operation.glade
%{_datadir}/%{name}-%{apiver}/language-specs/gda-sql.lang

%files ui-devel
%{_includedir}/%{name}-%{apiver}/%{name}-ui
%{_libdir}/%{name}-ui-%{apiver}.so
%{_bindir}/gdaui-demo-%{apiver}
%{_libdir}/pkgconfig/%{name}-ui-%{apiver}.pc
%{_datadir}/%{name}-%{apiver}/demo/
%{_datadir}/gir-1.0/Gdaui-%{apiver}.gir
%{_libdir}/%{name}-%{apiver}/plugins/%{name}-ui-plugins.so

%files tools
%doc %{_datadir}/gnome/help/gda-browser/
%doc %{_datadir}/gtk-doc/html/gda-browser/
%{_bindir}/gda-*
%{_datadir}/%{name}-%{apiver}/gda_trml2html
%{_datadir}/%{name}-%{apiver}/gda_trml2pdf
%{_datadir}/applications/gda-browser-%{apiver}.desktop
%{_datadir}/applications/gda-control-center-%{apiver}.desktop
%{_datadir}/pixmaps/gda-browser-5.0.png
%{_datadir}/icons/hicolor/*

%files sqlite
%{_libdir}/%{name}-%{apiver}/providers/%{name}-sqlite.so
%{_datadir}/%{name}-%{apiver}/sqlite_specs*.xml

%if 0%{with bdb}
%files bdb
%{_libdir}/libgda-%{apiver}/providers/libgda-bdb.so
%{_libdir}/libgda-%{apiver}/providers/libgda-bdbsql.so
%{_datadir}/%{name}-%{apiver}/bdb_specs*.xml
%{_datadir}/%{name}-%{apiver}/bdbsql_specs*.xml
%endif

%if 0%{with ldap}
%files ldap
%{_libdir}/%{name}-%{apiver}/providers/%{name}-ldap.so
%{_datadir}/%{name}-%{apiver}/ldap_specs*.xml
%endif

%files sqlcipher
%{_libdir}/%{name}-%{apiver}/providers/%{name}-sqlcipher.so
%{_datadir}/%{name}-%{apiver}/sqlcipher_specs*.xml

%files web
%{_libdir}/%{name}-%{apiver}/providers/%{name}-web.so
%{_datadir}/%{name}-%{apiver}/php/
%{_datadir}/%{name}-%{apiver}/web/
%{_datadir}/%{name}-%{apiver}/web_specs*.xml

%if 0%{with mysql}
%files mysql
%{_libdir}/libgda-%{apiver}/providers/libgda-mysql.so
%{_datadir}/%{name}-%{apiver}/mysql_specs*.xml
%endif

%if 0%{with postgres}
%files postgres
%{_libdir}/libgda-%{apiver}/providers/libgda-postgres.so
%{_datadir}/%{name}-%{apiver}/postgres_specs*.xml
%endif

%if 0%{with mdb}
%files mdb
%{_libdir}/libgda-%{apiver}/providers/libgda-mdb.so
%{_datadir}/%{name}-%{apiver}/mdb_specs*.xml
%endif

%if 0%{with java}
%files java
%{_libdir}/libgda-%{apiver}/providers/%{name}-jdbc.so
%{_libdir}/libgda-%{apiver}/providers/gdaprovider-%{apiver}.jar
%{_datadir}/%{name}-%{apiver}/jdbc_specs*.xml
%endif

%changelog
* Tue Aug  6 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 1:5.1.2-4
- fix FTBFS (RHBZ #992077)
- cleanup rpm conditionals

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 1:5.1.2-2
- Rebuilt for gtksourceview3 soname bump

* Tue Mar 19 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 1:5.1.2-1
- upstream 5.1.2
- dropped upstreamed patches

* Sun Feb 24 2013 Haïkel Guémar <hguemar@fedoraproject.org> - 1:5.1.1-6
- rebuilt against newer graphviz (RHBZ #914131)
- remove deprecated graphviz API calls in gda-browser
- build system workaround (RHBZ #904790)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Dan Horák <dan[at]danny.cz> - 1:5.1.1-4
- fix Java detection on secondary arches

* Wed Oct 24 2012 Kalev Lember <kalevlember@gmail.com> - 1:5.1.1-3
- Enable introspection (#869072)

* Mon Oct 22 2012 Kalev Lember <kalevlember@gmail.com> - 1:5.1.1-2
- Add back the epoch
- Build without scrollkeeper support
- Properly obsolete subpackages that got removed in v4->v5 transition
- Fix some rpm directory ownership issues
- Add icon cache scriptlets

* Sun Oct 21 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 5.1.1-1
- upstream 5.1.1 based on libgda5 review (RHBZ #788569)

* Sun Aug  5 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.13-1
- upstream 4.2.13
- bug fixes to MySQL and MDB providers and various minor issues

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 1:4.2.12-3
- switch to libdb-devel
- fix the build with OpenJDK7

* Sun Jan 22 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.12-2
- fix gobject-introspection support
- clean up spec (removed old obsoletes)

* Sun Jan 22 2012 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.12-1
- upstream 4.2.12

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 26 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.11-1
- upstream 4.1.11
- sqlite provider can load sqlite extensions using "SELECT load_extension ('xxx')"
- remove unused BR

* Thu Aug 25 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.8-1
- upstream 4.2.8
- ldap read-only support is back

* Mon Jul  4 2011 Mark Chappell <tremble@fedoraproject.org> - 1:4.2.5-2
- Rebuild for graphviz so name bump.

* Sun Apr 10 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.5-1
- upstream 4.2.5

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 1:4.2.4-3
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 22 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.4-2
- fix sqlite loading (RHBZ #673809)

* Thu Feb 17 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.4-1
- upstream 4.2.4

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan  8 2011  <builder@zangetsu.seireitei> - 1:4.2.2-2
- drop sqlite patch: should be fixed in latest xulrunner package

* Tue Nov 30 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.2-1
- Upstream 4.2.2
- Cleaned spec from deprecated providers support
- Fix sqlite3 shared library loading (RHBZ #658471)

* Tue Oct 26 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.2.0-1
- Update to upstream 4.2.0
- New provider: sqlcipher (SQLite encryption extension)
- New patch fixing 4.2.0 build issue
- Disable GObject introspection since it's broken

* Wed Jun 16 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.1.6-1
- Update to upstream 4.1.6
- Add new BR: gnome-doc-utils
- Dropped BR: gir-repository

* Tue Apr 27 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.1.4-1
- Update to upstream 4.1.4 (required by Glom)
- Added web provider and ui subpackages
- Added new BR (gtk2, unique, goocanvas, graphviz) for libgda-ui

* Thu Apr 22 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.0.8-2
- add gir descriptions files

* Thu Apr 22 2010 Haïkel Guémar <hguemar@fedoraproject.org> - 1:4.0.8-1
- Update to upstream 4.0.8

* Thu Feb 18 2010 Denis Leroy <denis@poolshark.org> - 1:4.0.7-1
- Update to upstream 4.0.7

* Mon Jan 18 2010 Denis Leroy <denis@poolshark.org> - 1:4.0.6-1
- Update to upstream 4.0.6
- Added Java JDBC provider subpackage

* Sat Nov  7 2009 Denis Leroy <denis@poolshark.org> - 1:4.0.5-1
- Update to upstream 4.0.5
- Source URL fix

* Tue Sep 15 2009 Denis Leroy <denis@poolshark.org> - 1:4.0.4-1
- Update to upstream version 4.0.4

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1:4.0.2-3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009 Denis Leroy <denis@poolshark.org> - 1:4.0.2-1
- Update to upstream 4.0.2
- Use system sqlite library

* Mon Mar 23 2009  <denis@poolshark.org> - 1:4.0.0-1
- Update to upstream 4.0.0

* Wed Mar  4 2009 Denis Leroy <denis@poolshark.org> - 1:3.99.12-1
- Update to upstream 3.99.12

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.99.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Denis Leroy <denis@poolshark.org> - 1:3.99.11-1
- Update to 3.99.11 (many bug fixes)

* Fri Jan 16 2009 Denis Leroy <denis@poolshark.org> - 1:3.99.8-1
- Switch to 4.0 ABI
- Update to upstream 3.99.8
- Patch updates (upstreamed and ported)
- Added JAVA package flag, currently disabled

* Mon Oct 27 2008 Denis Leroy <denis@poolshark.org> - 1:3.1.2-6
- Added patch to fix providers path on x86_64 (#468510)

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1:3.1.2-5
- Rebuild against new db4-4.7

* Tue Jun 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.1.2-4
- Rebuild against new freetds

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.1.2-3
- Autorebuild for GCC 4.3

* Sat Jan 26 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.1.2-2
- Rebuid now that the system sqlite has column metadata enabled, so that we
  use the system version instead of our own private copy (bz 430258)

* Fri Jan 25 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.1.2-1
- New upstream release 3.1.2 (needed for new gnumeric)
- Drop upstreamed / no longer needed patches

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 3.0.1-6
- Rebuild for deps

* Sun Oct 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-5
- Rebuild to fix untranslated strings on x86_64 in
  /usr/share/libgda-3.0/sqlite_specs_drop_index.xml
  which caused multilib problems (bz 342101)

* Fri Aug 17 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-4
- Fix building on ppc64 again (patch configure not configure.in, now we are
  no longer running autoconf)

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-3
- Enable microsoft access (mdb) support now that mdbtools is in Fedora
- Enable xBase (dBase, Clipper, FoxPro) support, it seems that xbase has been
  available for quite a while now
- Switch from using mysqlclient10 to using mysql-libs for the msql provider

* Wed Aug  8 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-2
- Build against system sqlite instead of own private copy (this is possible now
  that the system sqlite is of a high enough version)
- Enable FreeTDS provider (FreeTDS is in Fedora now)
- Update License tag for new Licensing Guidelines compliance

* Sun May 27 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:3.0.1-1
- New upstream release 3.0.1
- Remove mono bindings sub-package as upstream no longer includes them

* Thu May 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-12
- Don't build mono/sharp bits on ppc64
- Fixup packaging of sharp bindings to match the mono packaging guidelines

* Fri Dec 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-11
- Rebuild for new postgres

* Mon Aug 28 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-10
- FE6 Rebuild

* Tue Jun 20 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-9
- Add BuildRequires: libtool hopefully _really_ fixing building with the new
  stripped mock config. (Drop BR: autoconf which is implied by BR: automake).

* Thu Jun 15 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-8
- Add BuildRequires: automake, autoconf to fix building with the new even more
  stripped mock config.

* Sat Jun 10 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-7
- Add BuildRequires: gettext, bison, flex, gamin-devel to fix building with
  new stripped mock config.

* Thu May 11 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-6
- Move Obsoletes and Provides for plugins out of the plugins %%description,
  so that they actually Obsolete and Provide instead of showing up in rpm -qi
  (bug 191213).

* Thu May  4 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-5
- Add patch3 fixing a couple of x86_64 bugs (bz 190366)

* Mon Feb 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-4
- Bump release and rebuild for new gcc4.1 and glibc.
- Make sqlite plugin use system sqlite not build in version
- Make sqlite plugin a seperate package again
- Attempt to properly install C-sharp/mono bindings
- Add %%{?dist} for consistency with my other packages
- Remove static lib from -devel package

* Tue Jan 17 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-3
- Make -sharp package Require the main package.

* Mon Jan 16 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-2
- Remove unneeded requires (.so reqs are automaticly picked up by rpm).
- Add BuildRequires for building libgda-sharp

* Sun Nov 27 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.9.100-1
- New upstream version
- Drop 4 intergrated patches
- Removed sqlite configurability, it is now an internal part of the upstream
  sources.

* Fri Aug  5 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.2.0-8
- Remove libgda.la file from devel package.

* Sat Jun 25 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.2.0-7
- Added Patch4: libgda-1.2.0-libdir.patch which fixes loading of
  database providers on platforms with a lib64 dir. Thanks to:
  Bas Driessen <bas.driessen@xobas.com> for the patch.
- Enabled building of libgda-ldap and libgda-sqlite by default.

* Tue Jun 21 2005 Hans de Goede <j.w.r.degoede@hhs.nl> 1:1.2.0-6
- rebuild so that we depend on the proper version of libpq.so (#160917)
- change names of database providers from gda-xxx to libgda-xxx (#160917)

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 1:1.2.0-5
- rebuild with gcc4

* Fri Feb 11 2005 Caolan McNamara <caolanm@redhat.com> 1:1.2.0-4
- well, that was moronic

* Thu Feb 10 2005 Caolan McNamara <caolanm@redhat.com> 1:1.2.0-3
- bandaid

* Wed Feb  9 2005 Jeremy Katz <katzj@redhat.com> - 1:1.2.0-2
- rebuild to try to fix broken dep

* Fri Feb 4 2005 Caolan McNamara <caolanm@redhat.com> 1:1.2.0-1
- bump to latest version
- drop integrated break warning patch
- update configure patch

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 1:1.0.4-5
- Rebuilt for new readline.

* Sat Oct 30 2004 Caolan McNamara <caolanm@redhat.com> 1:1.0.4-4
- Use mysqlclient10

* Fri Oct  8 2004 Caolan McNamara <caolanm@redhat.com> 1:1.0.4-3
- #rh135043# Extra BuildRequires

* Thu Sep  9 2004 Bill Nottingham <notting@redhat.com> 1:1.0.4-2
- %%defattr

* Thu Aug 12 2004 Caolan McNamara <caolanm@redhat.com> 1:1.0.4-1
- Initial Red Hat import
- patch for missing break statement
- fixup devel package requirement pickiness
- autoconf patch to pick up correct mysql path from mysql_config (e.g. x64)
- autoconf patch to just look in the normal place for postgres first

* Tue Mar 11 2003 David Hollis <dhollis@davehollis.com>
- Fix --with-tds & --without-tds to match what configure wants

* Tue Jan 28 2003 Yanko Kaneti <yaneti@declera.com>
- Remove the idl path
- Include gda-config man page
- add --without-* for disabled providers
- package and use the omf/scrollkeeper bits

* Tue Dec 31 2002 David Hollis <dhollis@davehollis.com>
- Added sqlite-devel buildreq
- Include gda-config-tool man page

* Mon Aug 19 2002 Ben Liblit <liblit@acm.org>
- Fixed version number substitutions

- Removed some explicit "Requires:" prerequisites that RPM will figure
  out on its own.  Removed explicit dependency on older MySQL client
  libraries

- Required that the ODBC development package be installed if we are
  building the ODBC provider

- Created distinct subpackages for each provider, conditional on that
  provider actually being enabled; some of these will need to be
  updated as the family of available providers changes

- Updated files list to match what "make install" actually installs

- Added URL tag pointing to GNOME-DB project's web site

* Tue Feb 26 2002 Chris Chabot <chabotc@reviewboard.com>
- Added defines and configure flags for all supported DB types

* Mon Feb 25 2002 Chris Chabot <chabotc@reviewboard.com>
- Cleaned up formatting
- Added Requirements
- Added defines for postgres, mysql, odbc support

* Thu Feb 21 2002 Chris Chabot <chabotc@reviewboard.com>
- Initial spec file
