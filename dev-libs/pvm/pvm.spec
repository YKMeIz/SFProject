Name:           pvm 
Version:        3.4.6
Release:        9%{?dist}
Summary:        Libraries for distributed computing.
# Includes regex code which is under GPLv2+
License:        MIT and GPLv2+
Group:          Development/Libraries

URL:            http://www.csm.ornl.gov/pvm/pvm_home.html
Source0:        http://www.netlib.org/pvm3/pvm%{version}.tgz
Source1:        http://www.netlib.org/pvm3/xpvm/XPVM.src.1.2.5.tgz
Source2:        xpvm.sh
Source3:        pvm.sh
Source4:        README.RedHat

Patch0:         xpvm-tcltk.patch
Patch1:         pvm3-vaargfix.patch
Patch2:         pvm-s390.patch
Patch3:         pvm3.4.5-strerror.patch
Patch4:         pvm3.4.4-envvars.patch
Patch5:         xpvm-1.2.5-envvars.patch
Patch6:         pvm3.4.5-x86_64-segfault.patch
Patch7:         pvm-3.4.5-bug_147337.patch
Patch8:         pvm-3.4.5-Pvmtev.patch
Patch9:         pvm-3.4.5-ppc64arch.patch
Patch10:        pvm-arch.patch
Patch11:        xpvm-tk8.6.patch

BuildRequires: tk-devel tcl-devel tcl tk m4
Requires: initscripts >= 5.54, bash >= 2

%description
PVM3 (Parallel Virtual Machine) is a library and daemon that allows
distributed processing environments to be constructed on heterogeneous
machines and architectures.


%package gui
Requires:       pvm
Summary:        TCL/TK graphical frontend to monitor and manage a PVM cluster.
Group:          Applications/System

%description gui
Xpvm is a TCL/TK based tool that allows full manageability of the PVM cluster
as well as the ability to monitor cluster performance.


%prep
%setup -q -T -c -n pvm
install -m 0644 %SOURCE4 .

rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/
cd %{buildroot}/usr/share
tar -xzf %{SOURCE0}
cd pvm3
tar -xzf %{SOURCE1}
%patch0 -p0
#patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
#patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
# Work around change in tcl. Needs to be fixed in PVM long term.
# http://www.tcl.tk/cgi-bin/tct/tip/330.html
%if 0%{?fedora} && 0%{?fedora} >= 21
%patch11 -p1
%endif

find . -name \*.orig | xargs rm -f

# Patch the LINUX*64.def files to look in lib64 dirs as well for libraries.
perl -p -i -e "s|ARCHDLIB[	\ ]*=|ARCHDLIB	= -L/usr/lib64 -L/usr/X11R6/lib64|" conf/LINUX64.def
perl -p -i -e "s|ARCHLIB[	\ ]*=|ARCHLIB	= -L/usr/lib64 -L/usr/X11R6/lib64|" conf/LINUX64.def
%ifarch x86_64
echo 'ARCHCFLAGS += -fPIC' >> conf/LINUX64.def
%endif

cp conf/LINUX.def conf/LINUXS390.def
cp conf/LINUX.m4 conf/LINUXS390.m4
cp conf/LINUX.def conf/LINUXI386.def
cp conf/LINUX.m4 conf/LINUXI386.m4
cp conf/LINUX64.def conf/LINUXS390X.def
cp conf/LINUX64.m4 conf/LINUXS390X.m4
cp conf/LINUX64.def conf/LINUXIA64.def
cp conf/LINUX64.m4 conf/LINUXIA64.m4
cp conf/LINUX64.def conf/LINUXX86_64.def
cp conf/LINUX64.m4 conf/LINUXX86_64.m4
cp conf/LINUX64.def conf/LINUXPPC64.def
cp conf/LINUX64.m4 conf/LINUXPPC64.m4


#%define pvm_arch %(echo %{_os}%{_target_cpu} | tr 'a-z' 'A-Z')
%build

PVM_ROOT=%{buildroot}/usr/share/pvm3 \
	PVM_ARCH=`/var/tmp/pvm-3.4.5-root/usr/share/pvm3/lib/pvmgetarch` \
	PVM_DPATH=%{buildroot}/usr/share/pvm3/lib/pvmd \
	CFLAGS=-fPIC \
	make -C %{buildroot}/usr/share/pvm3 

PVM_ROOT=%{buildroot}/usr/share/pvm3 \
	PVM_ARCH=`/var/tmp/pvm-3.4.5-root/usr/share/pvm3/lib/pvmgetarch` \
	XPVM_ROOT=%{buildroot}/usr/share/pvm3/xpvm \
	make -C %{buildroot}/usr/share/pvm3/xpvm XLIBDIR=-L%{_prefix}/X11R6/%{_lib} TCLTKHOME=%{_libdir} 

## FIXME: 'install' section used to start here
## We don't have a separate install section as the spec relied on old behaviour
## of rpm which didn't automatically remove the buildroot
mkdir -p %{buildroot}%{_mandir}/man{1,3}
install -m 644 %{buildroot}/usr/share/pvm3/man/man1/* %{buildroot}%{_mandir}/man1
install -m 644 %{buildroot}/usr/share/pvm3/man/man3/* %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}/usr/bin
install -m 0755 %{SOURCE2} %{buildroot}/usr/bin/xpvm
PVM_ROOT=%{buildroot}/usr/share/pvm3 \
	PVM_ARCH=`/var/tmp/pvm-3.4.5-root/usr/share/pvm3/lib/pvmgetarch` \
	XPVM_ROOT=%{buildroot}/usr/share/pvm3/xpvm \
	make -C %{buildroot}/usr/share/pvm3/xpvm install

mkdir -p %{buildroot}/usr/bin
install -m 0755 %{SOURCE3} %{buildroot}/usr/bin/pvm

# Move the documentation the directory RPM thinks it's using, so we
# can classify it as documentation files

mv %{buildroot}/usr/share/pvm3/doc/* $RPM_BUILD_DIR/pvm/
rmdir %{buildroot}/usr/share/pvm3/doc

# Use /var/run/pvm for state files

mkdir -p %{buildroot}/var/run/pvm3

# build the file list
find %{buildroot} -type f -o -type l | \
	sed -e "s|%{buildroot}||g" | \
	grep -v -i win32 | \
	grep -v "/pvm3/man/man" | \
        grep -v "usr/man" | \
        grep -v "xpvm" | \
	grep -v "example" | \
	grep -v "conf/" | \
	grep -v "\.o$" > files.list
find %{buildroot} -type f -o -type l | \
	sed -e "s|%{buildroot}||g" | \
	grep "conf/LINUX" >> files.list
find %{buildroot} -type f -o -type l | \
	grep example | \
	sed -e "s|%{buildroot}|%doc |g" >> files.list
find %{buildroot}/usr/share/pvm3  -type d | \
	sed -e "s|%{buildroot}|%dir |g" | \
	grep -v "xpvm" >> files.list

# Remove man pages from list
grep -v "%{_mandir}" files.list > files.list2
mv files.list2 files.list

#Fix broken man pages
pushd %{buildroot}/%{_mandir}
rm man1/PVM.1 man1/pvmd.1
ln -sf pvm_intro.1 man1/PVM.1
ln -sf pvmd3.1 man1/pvmd.1
popd

# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_datadir}/pvm3/Readme.Win32
rm -f `find %{buildroot} -name "*.o"`
rm -rf %{buildroot}%{_datadir}/pvm3/WIN32/*
rm -rf %{buildroot}%{_datadir}/pvm3/libfpvm/WIN32/*
rm -f %{buildroot}%{_datadir}/pvm3/man/WIN32/*
rm -f %{buildroot}%{_datadir}/pvm3/lib/xpvm
pushd %{buildroot}%{_datadir}/pvm3/conf
rm -rf `find . -not -name "LINUX*"` ||:
popd

pushd %{buildroot}%{_datadir}/pvm3/man
rm -f `find . -type f` 
popd

%clean
rm -rf %{buildroot}
rm -f files.list

%pre
if [ $1 -eq 1 ]; then
    /usr/sbin/groupadd -g 24 -r -f pvm > /dev/null 2>&1
    /usr/sbin/useradd -u 24 -g 24 -d /usr/share/pvm3 -r -s /bin/bash pvm > /dev/null 2>&1 ||:
fi

%preun
if [ $1 -eq 0 ]; then
    /usr/sbin/userdel pvm > /dev/null 2>&1
    /usr/sbin/groupdel pvm > /dev/null 2>&1 ||:
fi

%triggerun -- pvm <= 3.4.3-25
/sbin/chkconfig --del pvmd

%files -f files.list
%doc arches  bugreport  example.pvmrc  release-notes README.RedHat
%{_mandir}/*/*
%dir %attr(755,pvm,pvm) /var/run/pvm3

%files gui
%dir %{_datadir}/pvm3/xpvm
%{_bindir}/xpvm
%{_datadir}/pvm3/bin/*/xpvm
%{_datadir}/pvm3/xpvm/*

%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Richard Shaw <hobbes1069@gmail.com> - 3.4.6-7
- Rebuilt for updated tcl.
- Workaround for change in tcl interp pointer access see:
  http://www.tcl.tk/cgi-bin/tct/tip/330.html

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Richard Shaw <hobbes1069@gmail.com> - 3.4.6-1
- Update to 3.4.6.
- Initial release for EL6.
