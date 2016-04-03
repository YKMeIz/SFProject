Name:           xtreemfs
Version:        1.5.1
Release:        1%{?dist}
License:        BSD-3-Clause
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Group:          System/Filesystems
URL:            http://www.XtreemFS.org
Summary:        XtreemFS base package
Source0:        XtreemFS-%{version}.tar.gz

BuildRequires:  ant >= 1.6.5
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  gcc-c++ >= 4.1
BuildRequires:  fuse >= 2.6
BuildRequires:  fuse-devel >= 2.6
BuildRequires:  openssl-devel >= 0.9.8
BuildRequires:  cmake >= 2.6
BuildRequires:  boost-devel >= 1.35
BuildRequires:  libattr-devel >= 2
BuildRequires:  redhat-rpm-config


%description
XtreemFS is a distributed and replicated file system for the internet. For more details, visit www.xtreemfs.org.

%package client
Summary:        XtreemFS client
Group:          System/Filesystems
Requires:       fuse >= 2.6
Requires:       attr >= 2
Obsoletes:      XtreemFS-client < %{version}-%{release}

%description client
XtreemFS is a distributed and replicated file system for the internet. For more details, visit www.xtreemfs.org.
This package contains the XtreemFS client module.

%package backend
Summary:        XtreemFS backend modules and libraries
Group:          System/Filesystems
Requires:       jre >= 1.6.0

%description backend
XtreemFS is a distributed and replicated file system for the internet. For more details, visit www.xtreemfs.org.
This package contains the backend modules and libraries shared between the server and tools sub-packages.

%package server
Summary:        XtreemFS server components (DIR, MRC, OSD)
Group:          System/Filesystems
Requires:       %{name}-backend == %{version}-%{release}
Requires:       grep
Requires:       jre >= 1.6.0
Requires:       initscripts
Obsoletes:      XtreemFS-server < %{version}
Requires(post): util-linux

%description server
XtreemFS is a distributed and replicated file system for the internet. For more details, visit www.xtreemfs.org.
This package contains the XtreemFS server components (DIR, MRC, OSD).

%package tools
Summary:        XtreemFS administration tools
Group:          System/Filesystems
Requires:       %{name}-backend == %{version}-%{release}
Requires:       attr >= 2
Requires:       jre >= 1.6.0
Obsoletes:      XtreemFS-tools < %{version}

%description tools
XtreemFS is a distributed and replicated file system for the internet. For more details, visit www.xtreemfs.org.
This package contains XtreemFS administration tools.

%prep
%setup -q -n XtreemFS-%{version}


%build
export ANT_OPTS=-D"file.encoding=UTF-8"
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CXXFLAGS=$CFLAGS

make %{?jobs:-j%jobs}

%install
export NO_BRP_CHECK_BYTECODE_VERSION=true

make install DESTDIR=$RPM_BUILD_ROOT
ln -sf /usr/bin/mount.xtreemfs ${RPM_BUILD_ROOT}/sbin/mount.xtreemfs
ln -sf /usr/bin/umount.xtreemfs ${RPM_BUILD_ROOT}/sbin/umount.xtreemfs

# add /etc/xos/xtreemfs/truststore/certs/ folder used for storing certificates
mkdir -p $RPM_BUILD_ROOT/etc/xos/xtreemfs/truststore/certs/

# Create log directory.
mkdir -p $RPM_BUILD_ROOT/var/log/xtreemfs

# remove copyright notes (let rpm handle that)
rm $RPM_BUILD_ROOT/usr/share/doc/xtreemfs-client/LICENSE
rmdir $RPM_BUILD_ROOT/usr/share/doc/xtreemfs-client
rm $RPM_BUILD_ROOT/usr/share/doc/xtreemfs-server/LICENSE
rmdir $RPM_BUILD_ROOT/usr/share/doc/xtreemfs-server
rm $RPM_BUILD_ROOT/usr/share/doc/xtreemfs-tools/LICENSE
rmdir $RPM_BUILD_ROOT/usr/share/doc/xtreemfs-tools

rm $RPM_BUILD_ROOT/etc/xos/xtreemfs/postinstall_setup.sh

%pre server
/usr/sbin/groupadd xtreemfs 2>/dev/null || :
/usr/sbin/useradd -r --home /var/lib/xtreemfs -g xtreemfs xtreemfs 2>/dev/null || :
/usr/sbin/usermod -g xtreemfs xtreemfs 2>/dev/null || :


%post server
#$XTREEMFS_CONFIG_DIR/postinstall_setup.sh
#!/bin/bash
set -e

XTREEMFS_LOG_DIR=/var/log/xtreemfs
XTREEMFS_HOME=/var/lib/xtreemfs
XTREEMFS_ETC=/etc/xos/xtreemfs
XTREEMFS_USER=xtreemfs
XTREEMFS_GROUP=xtreemfs
XTREEMFS_GENERATE_UUID_SCRIPT="${XTREEMFS_ETC}/generate_uuid"

# When executed during POST installation, do not be verbose.
VERBOSE=0
script_name=$(basename "$0")
if [ "$script_name" = "postinstall_setup.sh" ]
then
  VERBOSE=1
fi

# generate UUIDs
if [ -x "$XTREEMFS_GENERATE_UUID_SCRIPT" ]; then
  for service in dir mrc osd; do
    "$XTREEMFS_GENERATE_UUID_SCRIPT" "${XTREEMFS_ETC}/${service}config.properties"
    [ $VERBOSE -eq 1 ] && echo "Generated UUID for service: $service"
  done
else
  echo "UUID can't be generated automatically. Please enter a correct UUID in each config file of an XtreemFS service."
fi


group_exists=`grep -c $XTREEMFS_GROUP /etc/group || true`
if [ $group_exists -eq 0 ]; then
    groupadd $XTREEMFS_GROUP
    [ $VERBOSE -eq 1 ] && echo "created group $XTREEMFS_GROUP"
fi
exists=`grep -c $XTREEMFS_USER /etc/passwd || true`
if [ $exists -eq 0 ]; then
    mkdir $XTREEMFS_HOME
    useradd -r --home $XTREEMFS_HOME -g $XTREEMFS_GROUP $XTREEMFS_USER
    chown $XTREEMFS_USER $XTREEMFS_HOME
    [ $VERBOSE -eq 1 ] && echo "created user $XTREEMFS_USER and data directory $XTREEMFS_HOME"
fi
if [ ! -d $XTREEMFS_HOME ]; then
    mkdir -m750 $XTREEMFS_HOME
    chown $XTREEMFS_USER $XTREEMFS_HOME
    [ $VERBOSE -eq 1 ] && echo "user $XTREEMFS_USER exists but data directory $XTREEMFS_HOME had to be created"
fi
owner=`stat -c %U $XTREEMFS_HOME`
if [ "$owner" != "$XTREEMFS_USER" ]; then
    [ $VERBOSE -eq 1 ] && echo "directory $XTREEMFS_HOME is not owned by $XTREEMFS_USER, executing chown"
    chown $XTREEMFS_USER $XTREEMFS_HOME
fi

if [ ! -e $XTREEMFS_LOG_DIR ]; then
    mkdir $XTREEMFS_LOG_DIR
    chown -R $XTREEMFS_USER $XTREEMFS_LOG_DIR
fi

if [ -e $XTREEMFS_ETC ]; then
    group=`stat -c %G $XTREEMFS_ETC 2>/dev/null`
    if [ $group != $XTREEMFS_GROUP ]; then
        [ $VERBOSE -eq 1 ] && echo "directory $XTREEMFS_ETC is owned by $group, should be owned by $XTREEMFS_GROUP, executing chgrp (may take some time)"
        chgrp -R $XTREEMFS_GROUP $XTREEMFS_ETC
    fi
    for file in `ls $XTREEMFS_ETC/*.properties 2>/dev/null`; do
      if [ -f $file -a "$(stat -c %a $file)" != "640" ]; then
          [ $VERBOSE -eq 1 ] && echo "setting $file 0640, executing chmod"
          chmod 0640 $file
      fi
    done
    if [ -d "$XTREEMFS_ETC/truststore/" ]
    then
        if [ "$(stat -c %a "$XTREEMFS_ETC/truststore/")" != "750" ]
        then
            [ $VERBOSE -eq 1 ] && echo "setting $XTREEMFS_ETC/truststore/ to 0750, executing chmod (may take some time)"
            chmod -R u=rwX,g=rX,o= $XTREEMFS_ETC/truststore/
        fi
    fi
fi

/sbin/chkconfig --add xtreemfs-dir
/sbin/chkconfig --add xtreemfs-mrc
/sbin/chkconfig --add xtreemfs-osd


%preun server
  if [ "$1" = "0" ] ; then
    /sbin/service xtreemfs-dir stop >/dev/null 2>&1
    /sbin/service xtreemfs-mrc stop >/dev/null 2>&1
    /sbin/service xtreemfs-osd stop >/dev/null 2>&1
    /sbin/chkconfig --del xtreemfs-dir
    /sbin/chkconfig --del xtreemfs-mrc
    /sbin/chkconfig --del xtreemfs-osd
  fi

%postun server
if [ "$1" -ge "1" ] ; then
  /sbin/service xtreemfs-dir try-restart >/dev/null 2>&1 || :
  /sbin/service xtreemfs-mrc try-restart >/dev/null 2>&1 || :
  /sbin/service xtreemfs-osd try-restart >/dev/null 2>&1 || :
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files client
%defattr(-,root,root,-)
/usr/bin/*.xtreemfs
/usr/bin/xtfsutil
/sbin/*.xtreemfs
/usr/share/man/man1/*.xtreemfs*
/usr/share/man/man1/xtfsutil*
%doc LICENSE

%files backend
%defattr(-,root,root,-)
/usr/share/java/XtreemFS.jar
/usr/share/java/Foundation.jar
/usr/share/java/protobuf-java-2.5.0.jar
/usr/share/java/Flease.jar
/usr/share/java/BabuDB.jar
/usr/share/java/BabuDB_replication_plugin.jar
/usr/share/java/jdmkrt.jar
/usr/share/java/jdmktk.jar
/usr/share/java/commons-codec-1.3.jar
%doc LICENSE

%files server
%defattr(-,root,xtreemfs,-)
%attr(-,root,root) /etc/init.d/xtreemfs-*
%dir %attr(-,root,root) /usr/share/xtreemfs
%attr(-,root,root) /usr/share/xtreemfs/xtreemfs-osd-farm
%dir /etc/xos/
%dir %attr(0750,root,xtreemfs) /etc/xos/xtreemfs/
%dir %attr(0750,root,xtreemfs) /etc/xos/xtreemfs/truststore/
%dir %attr(0750,root,xtreemfs) /etc/xos/xtreemfs/truststore/certs/
%config(noreplace) %attr(0640,root,xtreemfs) /etc/xos/xtreemfs/*.properties
/etc/xos/xtreemfs/generate_uuid
%dir /etc/xos/xtreemfs/server-repl-plugin/
%config(noreplace) %attr(0640,root,xtreemfs) /etc/xos/xtreemfs/server-repl-plugin/dir.properties
%config(noreplace) %attr(0640,root,xtreemfs) /etc/xos/xtreemfs/server-repl-plugin/mrc.properties
%dir %attr(0750,xtreemfs,xtreemfs) /var/log/xtreemfs
%doc LICENSE

%files tools
%defattr(-,root,root,-)
%config(noreplace) /etc/xos/xtreemfs/default_dir
/usr/bin/xtfs_*
/usr/share/man/man1/xtfs_*
%doc LICENSE

%changelog
* Sun Apr 3 2016 Neil Ge <neilgechn@gmail.com> - 1.5.1-1
- New package.
