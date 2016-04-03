%define foo2zjs_ver 20130618

Name:           foo2zjs
Version:        0.%{foo2zjs_ver}
Release:        1%{?dist}
Summary:        Linux printer driver for ZjStream protocol

Group:          System Environment/Libraries
License:        GPLv2
URL:            http://foo2zjs.rkkda.com/

# command : wget -O foo2zjs-20130122.tar.gz http://foo2zjs.rkkda.com/foo2zjs.tar.gz
# command : wget -O foo2zjs-20130618.tar.gz http://foo2zjs.rkkda.com/foo2zjs.tar.gz
Source0:        foo2zjs-%{foo2zjs_ver}.tar.gz
Patch0:         foo2zjs-dynamic-jbig.patch
Patch1:         foo2zjs-device-ids.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  jbigkit-devel groff ghostscript
BuildRequires:  bc
# For the psdriver autoprovides
BuildRequires:  python-cups
Requires:       lcms2
Requires:       argyllcms
Requires(post): /bin/rm

%package -n foo2hp
Summary:        Linux printer driver for HP 1600, HP 2600n
Group:          System Environment/Libraries
Requires:       lcms2 foo2zjs
Requires(post): /bin/rm

%package -n foo2hbpl2
Summary:        Linux printer driver for Dell 1355 and Xerox WorkCentre 6015
Group:          System Environment/Libraries
Requires:       lcms2 foo2zjs
Requires(post): /bin/rm

%package -n foo2xqx
Summary:        Linux printer driver for HP LaserJet M1005 MFP
Group:          System Environment/Libraries
Requires:       lcms2 foo2zjs
Requires(post): /bin/rm

%package -n foo2lava
Summary:        Linux printer driver for Zenographics LAVAFLOW protocol
Group:          System Environment/Libraries
Requires:       lcms2 foo2zjs
Requires(post): /bin/rm

%package -n foo2qpdl
Summary:        Linux printer driver for Samsung CLP-300, CLP-600, CLP-3160
Group:          System Environment/Libraries
Requires:       lcms2 foo2zjs
Requires(post): /bin/rm

%package -n foo2slx
Summary:        Linux printer driver for SLX protocol (Lexmark C500n etc.)
Group:          System Environment/Libraries
Requires:       lcms2 foo2zjs
Requires(post): /bin/rm

%package -n foo2hiperc
Summary:        Linux printer driver for HIPERC protocol (Oki C3400n etc.)
Group:          System Environment/Libraries
Requires:       lcms2 foo2zjs
Requires(post): /bin/rm

%package -n foo2oak
Summary:        Linux printer driver for OAKT protocol (HPLJ1500 etc.)
Group:          System Environment/Libraries
Requires:       lcms2 foo2zjs
Requires(post): /bin/rm

%description
foo2zjs is an open source printer driver for printers that use the
Zenographics ZjStream wire protocol for their print data, such as the
Minolta/QMS magicolor 2300 DL or Konica Minolta magicolor 2430
DL. These printers are often erroneously referred to as winprinters or
GDI printers. However, Microsoft GDI only mandates the API between an
application and the printer driver, not the protocol on the wire
between the printer driver and the printer. In fact, ZjStream printers
are raster printers which happen to use a very efficient wire protocol
which was developed by Zenographics and licensed by most major printer
manufacturers for at least some of their product lines. ZjStream is
just one of many wire protocols that are in use today, such as
Postscript, PCL, Epson, etc.

Users of this package are requested to visit the author's web page at
http://foo2zjs.rkkda.com/ and consider contributing.

%description -n foo2hp
foo2hp is an open source printer driver for printers that use the
Zenographics ZjStream wire protocol for their print data, such as the
HP Color LaserJet 2600n. These printers are often erroneously referred
to as winprinters or GDI printers. However, Microsoft GDI only
mandates the API between an application and the printer driver, not
the protocol on the wire between the printer driver and the
printer. In fact, ZjStream printers are raster printers which happen
to use a very efficient wire protocol which was developed by
Zenographics and licensed by most major printer manufacturers for at
least some of their product lines. ZjStream is just one of many wire
protocols that are in use today, such as Postscript, PCL, Epson, etc.

Users of this package are requested to visit the author's web page at
http://foo2hp.rkkda.com/ and consider contributing.

%description -n foo2hbpl2
foo2hbpl2 is an open source printer driver (Experimental) for Printers: 
Dell 1355 and Xerox WorkCentre 6015 

%description -n foo2xqx 
foo2xqx is an open source printer driver for printers that use the
HP/Software Imaging "XQX" stream wire protocol for their print data,
such as the HP LaserJet M1005 MFP. These printers are often
erroneously referred to as winprinters or GDI printers. However,
Microsoft GDI only mandates the API between an application and the
printer driver, not the protocol on the wire between the printer
driver and the printer. In fact, "XQX" printers are raster printers
which happen to use a very efficient wire protocol which was developed
by HP/Software Imaging. "XQX" is just one of many wire protocols that
are in use today, such as Postscript, PCL, Epson, ZjStream, etc.

Users of this package are requested to visit the author's web page at
http://foo2xqx.rkkda.com/ and consider contributing.

%description -n foo2lava
foo2lava is an open source printer driver for printers that use the
Zenographics LAVAFLOW wire protocol for their print data, such as the
Konica Minolta magicolor 2530 DL or the Konica Minolta magicolor 2490
MF. These printers are often erroneously referred to as winprinters or
GDI printers. However, Microsoft GDI only mandates the API between an
application and the printer driver, not the protocol on the wire
between the printer driver and the printer. In fact, LAVAFLOW printers
are raster printers which happen to use a very efficient wire protocol
which was developed by Zenographics and licensed by most major printer
manufacturers for at least some of their product lines. LAVAFLOW is
just one of many wire protocols that are in use today, such as
Postscript, PCL, Epson, ZjStream, etc.

Users of this package are requested to visit the author's web page at
http://foo2lava.rkkda.com/ and consider contributing.

%description -n foo2qpdl
foo2qpdl is an open source printer driver for printers that use the
QPDL wire protocol for their print data, such as the Samsung CLP-300
or the Samsung CLP-600 or the Xerox Phaser 6110. These printers are
often erroneously referred to as winprinters or GDI printers. However,
Microsoft GDI only mandates the API between an application and the
printer driver, not the protocol on the wire between the printer
driver and the printer. In fact, QPDL printers are raster printers
which happen to use a very efficient wire protocol. QPDL is just one
of many wire protocols that are in use today, such as Postscript, PCL,
Epson, ZjStream, etc.

Users of this package are requested to visit the author's web page at
http://foo2qpdl.rkkda.com/ and consider contributing.

%description -n foo2slx
foo2slx is an open source printer driver for printers that use the
Software Imaging K.K. SLX wire protocol for their print data, such as
the Lexmark C500n. These printers are often erroneously referred to as
winprinters or GDI printers. However, Microsoft GDI only mandates the
API between an application and the printer driver, not the protocol on
the wire between the printer driver and the printer. In fact, SLX
printers are raster printers which happen to use a very efficient wire
protocol which was developed by Zenographics and cloned by Software
Imaging K.K. and licensed by most major printer manufacturers for at
least some of their product lines. SLX is just one of many wire
protocols that are in use today, such as Postscript, PCL, Epson,
ZjStream, etc.

Users of this package are requested to visit the author's web page at
http://foo2slx.rkkda.com/ and consider contributing.

%description -n foo2hiperc
foo2hiperc is an open source printer driver for printers that use the
HIPERC wire protocol for their print data, such as the Oki C3400n and
the Oki C5500n.

NOTE: This driver is currently in Alpha and supports uncompressed mode
only.

Users of this package are requested to visit the author's web page at
http://foo2hiperc.rkkda.com/ and consider contributing.

%description -n foo2oak
foo2oak is a printer driver for printers that use the Oak Technology
(now Zoran) OAKT protocol for their print data, such as the HP Color
LaserJet 1500, Kyocera KM-1635 and the Kyocera KM-2035. These printers
are often erroneously referred to as winprinters or GDI
printers. However, Microsoft GDI only mandates the API between an
application and the printer driver, not the protocol on the wire
between the printer driver and the printer. In fact, OAKT printers are
raster printers which happen to use a fairly efficient wire protocol
which was developed by Oak Technology and licensed by some printer
manufacturers for at least some of their product lines. OAKT is just
one of many wire protocols that are in use today, such as Postscript,
PCL, Epson, ZjStream, etc.

Users of this package are requested to visit the author's web page at
http://foo2oak.rkkda.com/ and consider contributing.

%prep
%setup -q -n foo2zjs

# Patch to use jbigkit-devel package instead of static jbig source code
%patch0 -p1

# add missing 1284 Device IDs
%patch1 -p1

# Remove jbig source code, jbigkit-devel package is used in BuildRequires
#rm -f jbig*

sed -i -e s/foo2zjs-icc2ps/icc2ps/g *wrapper*
sed -i -e s/775/755/ Makefile
chmod -x COPYING

# Xerox-Phaser_6110 not needed files because already in foomatic-db package
rm foomatic-db/printer/Xerox-Phaser_6110.xml
rm PPD/Xerox-Phaser_6110.ppd

# Samsung CLP-310 already included in foomatic-db package
rm foomatic-db/printer/Samsung-CLP-310.xml

# KONICA_MINOLTA-magicolor_2430_DL already included in foomatic-db package
rm foomatic-db/printer/KONICA_MINOLTA-magicolor_2430_DL.xml

%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/foomatic/db/source/driver
mkdir -p $RPM_BUILD_ROOT%{_datadir}/foomatic/db/source/printer
mkdir -p $RPM_BUILD_ROOT%{_datadir}/foomatic/db/source/opt
mkdir -p $RPM_BUILD_ROOT%{_datadir}/cups/model

make PREFIX=$RPM_BUILD_ROOT%{_prefix} BINPROGS= install-prog \
     FOODB=$RPM_BUILD_ROOT%{_datadir}/foomatic/db/source \
     MODEL=$RPM_BUILD_ROOT/usr/share/cups/model \
     PPD=$RPM_BUILD_ROOT/usr/share/ppd \
     install-extra install-crd install-man install-foo install-ppd 

# Remove man page for usb_printerid which we don't ship
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/usb_printerid.1


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/*zjs*
%{_bindir}/printer-profile
%{_datadir}/foo2zjs
%{_mandir}/man1/*zjs*
%{_mandir}/man1/printer-profile.1.gz
%{_mandir}/man1/gipddecode.1.gz
%{_datadir}/foomatic/db/source/driver/foo2zjs.xml
%{_datadir}/foomatic/db/source/driver/foo2zjs-z1.xml
%{_datadir}/foomatic/db/source/driver/foo2zjs-z2.xml
%{_datadir}/foomatic/db/source/driver/foo2zjs-z3.xml
%{_datadir}/foomatic/db/source/opt/foo2zjs*.xml
%{_datadir}/foomatic/db/source/opt/foo2xxx*.xml
%{_datadir}/foomatic/db/source/printer/Generic-ZjStream_Printer.xml
%{_datadir}/foomatic/db/source/printer/HP-LaserJet_1*.xml
%{_datadir}/foomatic/db/source/printer/Minolta-Color_PageWorks_Pro_L.xml
%{_datadir}/foomatic/db/source/printer/Minolta-magicolor_2200_DL.xml
%{_datadir}/foomatic/db/source/printer/Minolta-magicolor_2300_DL.xml
%{_datadir}/foomatic/db/source/printer/Minolta-magicolor_2430_DL.xml
%{_datadir}/foomatic/db/source/printer/Olivetti-d-Color_P160W.xml
%{_datadir}/cups/model/Generic-ZjStream_Printer.ppd.gz
%{_datadir}/cups/model/HP-LaserJet_1*.ppd.gz
%{_datadir}/cups/model/Minolta-Color_PageWorks_Pro_L.ppd.gz
%{_datadir}/cups/model/Minolta-magicolor_2200_DL.ppd.gz
%{_datadir}/cups/model/Minolta-magicolor_2300_DL.ppd.gz
%{_datadir}/cups/model/Minolta-magicolor_2430_DL.ppd.gz
%{_datadir}/cups/model/Olivetti-d-Color_P160W.ppd.gz

%files -n foo2hp
%defattr(-,root,root,-)
%{_bindir}/*hp*
%{_mandir}/man1/*hp*
%{_datadir}/foomatic/db/source/driver/foo2hp.xml
%{_datadir}/foomatic/db/source/opt/foo2hp*.xml
%{_datadir}/foomatic/db/source/printer/HP-Color_LaserJet_1600.xml
%{_datadir}/foomatic/db/source/printer/HP-Color_LaserJet_2600n.xml
%{_datadir}/foomatic/db/source/printer/HP-Color_LaserJet_CP1215.xml
%{_datadir}/cups/model/HP-Color_LaserJet_CP1215.ppd.gz
%{_datadir}/cups/model/HP-Color_LaserJet_1600.ppd.gz
%{_datadir}/cups/model/HP-Color_LaserJet_2600n.ppd.gz

%files -n foo2hbpl2
%defattr(-,root,root,-)
%{_bindir}/foo2hbpl2*
%{_mandir}/man1/foo2hbpl2*
%{_datadir}/foomatic/db/source/driver/foo2hbpl2.xml
%{_datadir}/foomatic/db/source/opt/foo2hbpl2*.xml
%{_datadir}/foomatic/db/source/printer/Dell-1355.xml
%{_datadir}/foomatic/db/source/printer/Xerox-WorkCentre_6015.xml
%{_datadir}/foomatic/db/source/printer/Fuji_Xerox-DocuPrint_CM205.xml
%{_datadir}/cups/model/Dell-1355.ppd.gz
%{_datadir}/cups/model/Xerox-WorkCentre_6015.ppd.gz
%{_datadir}/cups/model/Fuji_Xerox-DocuPrint_CM205.ppd.gz
 
%files -n foo2xqx
%defattr(-,root,root,-)
%{_bindir}/*xqx*
%{_mandir}/man1/*xqx*
%{_datadir}/foomatic/db/source/driver/foo2xqx.xml
%{_datadir}/foomatic/db/source/opt/foo2xqx*.xml
%{_datadir}/foomatic/db/source/printer/HP-LaserJet_M*.xml
%{_datadir}/foomatic/db/source/printer/HP-LaserJet_P*.xml
%{_datadir}/cups/model/HP-LaserJet_M*.ppd.gz
%{_datadir}/cups/model/HP-LaserJet_P*.ppd.gz

%files -n foo2lava
%defattr(-,root,root,-)
%{_bindir}/*lava*
%{_bindir}/opldecode
%{_mandir}/man1/*lava*
%{_mandir}/man1/opldecode.1.gz
%{_datadir}/foomatic/db/source/driver/foo2lava.xml
%{_datadir}/foomatic/db/source/opt/foo2lava*.xml
%{_datadir}/foomatic/db/source/printer/KONICA_MINOLTA-magicolor_2480_MF.xml
%{_datadir}/foomatic/db/source/printer/KONICA_MINOLTA-magicolor_2490_MF.xml
%{_datadir}/foomatic/db/source/printer/KONICA_MINOLTA-magicolor_2530_DL.xml
%{_datadir}/foomatic/db/source/printer/KONICA_MINOLTA-magicolor_1600W.xml
%{_datadir}/foomatic/db/source/printer/KONICA_MINOLTA-magicolor_1680MF.xml
%{_datadir}/foomatic/db/source/printer/KONICA_MINOLTA-magicolor_1690MF.xml
%{_datadir}/foomatic/db/source/printer/KONICA_MINOLTA-magicolor_4690MF.xml
%{_datadir}/foomatic/db/source/printer/Xerox-Phaser_6121MFP.xml
%{_datadir}/cups/model/KONICA_MINOLTA-magicolor_2480_MF.ppd.gz
%{_datadir}/cups/model/KONICA_MINOLTA-magicolor_2490_MF.ppd.gz
%{_datadir}/cups/model/KONICA_MINOLTA-magicolor_2530_DL.ppd.gz
%{_datadir}/cups/model/KONICA_MINOLTA-magicolor_1600W.ppd.gz
%{_datadir}/cups/model/KONICA_MINOLTA-magicolor_1680MF.ppd.gz
%{_datadir}/cups/model/KONICA_MINOLTA-magicolor_1690MF.ppd.gz
%{_datadir}/cups/model/KONICA_MINOLTA-magicolor_4690MF.ppd.gz
%{_datadir}/cups/model/KONICA_MINOLTA-magicolor_2430_DL.ppd.gz
%{_datadir}/cups/model/Xerox-Phaser_6121MFP.ppd.gz


%files -n foo2qpdl
%defattr(-,root,root,-)
%{_bindir}/*qpdl*
%{_bindir}/hbpldecode
%{_mandir}/man1/*qpdl*
%{_mandir}/man1/hbpldecode*
%{_datadir}/foomatic/db/source/driver/foo2qpdl.xml
%{_datadir}/foomatic/db/source/opt/foo2qpdl*.xml
%{_datadir}/foomatic/db/source/printer/Samsung-CL*.xml
%{_datadir}/foomatic/db/source/printer/Xerox-Phaser_6115MFP.xml
%{_datadir}/cups/model/Samsung-CL*.ppd.gz
%{_datadir}/cups/model/Xerox-Phaser_6115MFP.ppd.gz
%{_datadir}/foo2qpdl/crd/

%files -n foo2slx
%defattr(-,root,root,-)
%{_bindir}/*slx*
%{_bindir}/gipddecode
%{_mandir}/man1/*slx*
%{_datadir}/foomatic/db/source/driver/foo2slx.xml
%{_datadir}/foomatic/db/source/opt/foo2slx*.xml
%{_datadir}/foomatic/db/source/printer/Lexmark-C500.xml
%{_datadir}/cups/model/Lexmark-C500.ppd.gz

%files -n foo2hiperc
%defattr(-,root,root,-)
%{_bindir}/*hiperc*
%{_mandir}/man1/*hiperc*
%{_datadir}/foomatic/db/source/driver/foo2hiperc.xml
%{_datadir}/foomatic/db/source/opt/foo2hiperc*.xml
%{_datadir}/foomatic/db/source/printer/Oki-C*.xml
%{_datadir}/cups/model/Oki-C*.ppd.gz

%files -n foo2oak
%defattr(-,root,root,-)
%{_bindir}/*oak*
%{_mandir}/man1/*oak*.1.gz
%{_datadir}/foomatic/db/source/opt/foo2oak*
%{_datadir}/foomatic/db/source/driver/foo2oak.xml
%{_datadir}/foomatic/db/source/driver/foo2oak-z1.xml
%{_datadir}/foomatic/db/source/printer/Generic-OAKT_Printer.xml
%{_datadir}/foomatic/db/source/printer/HP-Color_LaserJet_1500.xml
%{_datadir}/foomatic/db/source/printer/Kyocera-KM-1635.xml
%{_datadir}/foomatic/db/source/printer/Kyocera-KM-2035.xml
%{_datadir}/cups/model/Generic-OAKT_Printer.ppd.gz
%{_datadir}/cups/model/HP-Color_LaserJet_1500.ppd.gz
%{_datadir}/cups/model/Kyocera-KM-1635.ppd.gz
%{_datadir}/cups/model/Kyocera-KM-2035.ppd.gz

%doc COPYING ChangeLog INSTALL README manual.pdf

%post
/bin/rm -f /var/cache/foomatic/*

%post -n foo2hp
/bin/rm -f /var/cache/foomatic/*

%post -n foo2xqx
/bin/rm -f /var/cache/foomatic/*

%post -n foo2lava
/bin/rm -f /var/cache/foomatic/*

%post -n foo2qpdl
/bin/rm -f /var/cache/foomatic/*

%post -n foo2oak
/bin/rm -f /var/cache/foomatic/*

%post -n foo2slx
/bin/rm -f /var/cache/foomatic/*

%post -n foo2hiperc
/bin/rm -f /var/cache/foomatic/*

%changelog
* Wed Jul 31 2013 Cédric Olivier <cedric.olivier@free.fr> 0.20130618-1
- Update to lastest revision
- Add New printer support : Fuji_Xerox-DocuPrint_CM205

* Tue Nov 22 2011 Cédric Olivier <cedric.olivier@free.fr> 0.20111105-2
- Remove KONICA_MINOLTA-magicolor_2430 already in foomatic-db

* Sun Nov 6 2011 Cédric Olivier <cedric.olivier@free.fr> 0.20111105-1
- Update to latest release
- updated the C110 ieee1284 string
- foomatic-db, PPDs: New printer "KONICA_MINOLTA-magicolor_2430"
  like Minolta-magicolor_2430 except for Manufacturer
- hplj1000: make it work with usblp and CUPS (libusb)
- lavadecode: print the compression (JBIG or unknown)
- lavadecode: adjust for magicolor 3730

* Wed Oct 5 2011 David Woodhouse <dwmw2@infradead.org> 0.20110909-1
- Update to latest release
- Add Konica Minolta variant of 2430DL and 2300DL
- BR python-cups to get foomatic autodeps working

