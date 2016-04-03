Name:           html2text
Version:        1.3.2a
Release:        14%{?dist}
Summary:        HTML-to-text converter

Group:          Applications/Text
License:        GPL+
URL:            http://www.mbayer.de/html2text/
Source0:        ftp://ftp.ibiblio.org/pub/linux/apps/www/converters/%{name}-%{version}.tar.gz
# patches from http://patch-tracking.debian.net/package/html2text/1.3.2a-10
#
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=381184
# Close every file after processing, not at the end of program.
Patch0:         200-close-files-inside-main-loop.patch
# http://bugs.donarmstrong.com/cgi-bin/bugreport.cgi?bug=285378
# Remove limited built-in http support.
Patch1:         400-remove-builtin-http-support.patch
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=178684
# Support UTF-8 encoding when processing input.
Patch2:         500-utf8-support.patch
# Don't use backspaces.
Patch3:         510-disable-backspaces.patch
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=496226
# Recognize all <meta> tags, not just one.
Patch4:         600-multiple-meta-tags.patch
# Recode input according to 'meta http-equiv' in html document.
Patch5:         611-recognize-input-encoding.patch
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=498797
# Convert output to user's locale charset.
Patch6:         630-recode-output-to-locale-charset.patch
# Correctly specify NULLs for 64-bit architectures.
Patch7:         800-replace-zeroes-with-null.patch
# Substituted 'char*' with 'const char*' in needed places to avoid
# 'deprecated conversion from string constant to ‘char*’' warnings.
Patch8:         810-fix-deprecated-conversion-warnings.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
html2text is a command line utility that converts HTML documents into
plain text.
Each HTML document is read from standard input or a (local or remote)
URI, and formatted into a stream of plain text characters that is written
to standard output or into an output-file. The program preserves the
original positions of table fields and accepts also syntactically
incorrect input, attempting to interpret it "reasonably". The rendering
is largely customisable through an RC file.


%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1


%build
%configure
make %{?_smp_mflags} DEBUG="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_mandir}/{man1,man5}
rm -rf __dist_docs
mkdir -p __dist_docs
for file in README  ; do
  iconv -f latin1 -t utf8 $file -o $file.new
  mv -f $file.new $file
done
for file in html2text.1.gz html2textrc.5.gz; do
  basefile=`basename $file .gz`
  gunzip -c $file > __dist_docs/$basefile
  touch -r $file __dist_docs/$basefile
done
install -m0644 -p __dist_docs/html2text.1  $RPM_BUILD_ROOT%{_mandir}/man1
install -m0644 -p __dist_docs/html2textrc.5  $RPM_BUILD_ROOT%{_mandir}/man5
install -m0755 html2text $RPM_BUILD_ROOT%{_bindir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README CHANGES COPYING TODO CREDITS KNOWN_BUGS RELEASE_NOTES
%{_bindir}/html2text
%{_mandir}/man1/html2text.1*
%{_mandir}/man5/html2textrc.5*


%changelog
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-9
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2a-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009  Leigh Scott <leigh123linux@googlemail.com> - 1.3.2a-4
- Rebuild using patches from Debian patch tracking system 

* Thu Jul 31 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2a-3
- Convert README to UTF8 , change license to GPL+ and fix compiling flags

* Tue Jul 29 2008 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2a-2
- Rebuild & patch sgml

* Thu Jul 19 2007 Patrice Dumas <pertusus@free.fr> 1.3.2a-1
- initial packaging
