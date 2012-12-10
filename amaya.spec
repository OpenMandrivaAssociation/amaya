%define system_libwww	0
%{?_with_system_libwww:	%global system_libwww 1}

Name:		amaya
Version:	11.4.4
Release:	%mkrel 1
Summary:	Web Browser/Editor from the World Wide Web Consortium
Group:		Networking/WWW
License:	W3C License
Url:		http://www.w3.org/Amaya/
Source0:	http://www.w3.org/Amaya/Distribution/amaya-fullsrc-%{version}.tgz
Source1:	%{name}.1.bz2
#2010-01-06
Source10:	http://www.w3.org/Amaya/Distribution/Dutch.tgz
Source11:	http://www.w3.org/Amaya/Distribution/English.tgz
Source12:	http://www.w3.org/Amaya/Distribution/French.tgz
Source13:	http://www.w3.org/Amaya/Distribution/German.tgz
Source14:	http://www.w3.org/Amaya/Distribution/Italian.tgz
Source15:	http://www.w3.org/Amaya/Distribution/Spanish.tgz
Source16:	http://www.w3.org/Amaya/Distribution/Swedish.tgz
Patch0:		amaya-11.4.4-dso.patch
Patch1:		amaya-11.4.4-gzfile.patch
Patch2:		amaya-11.4.4-libpng15.patch
Patch3:		amaya-11.4.4-desktop.patch
BuildRequires:	freetype-devel
BuildRequires:	gtk2-devel
BuildRequires:	imlib-devel
BuildRequires:	libstdc++-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	zlib-devel
BuildRequires:	perl
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	raptor-devel
BuildRequires:	X11-devel
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	redland-devel
BuildRequires:	wxgtku-devel
%if %{system_libwww}
BuildRequires:	w3c-libwww-devel
%else
BuildConflicts:	w3c-libwww-devel
%endif

%description
Amaya is a complete Web authoring tool with some browsing 
funtionalities and comes equipped with a WYSIWYG style of
interface, similar to that of the most popular commercial
browsers. With such an interface, users do not need to 
well know the HTML, MathML or CSS languages.

This graphical HTML Editor supports many of the latest
draft standards for HTML/XHTML.

%prep
%setup -q -n Amaya -c
%if %{mdvver} >= 201200
%patch0 -p0
%endif
%patch1 -p0
%patch2 -p1
%patch3 -p0

%build
# use system mesa
rm -f Mesa/Makefile

mkdir Amaya/WX
cd Amaya/WX

ln -s ../configure ./configure
%configure2_5x --enable-system-raptor --enable-system-wx --prefix=%{_libdir}
cp Options.orig Options
%__make

%install
rm -rf %{buildroot}
cd Amaya/WX
mkdir -p %{buildroot}%{_prefix}
%makeinstall_std

mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}/
	ln -sf ../..%{_libdir}/Amaya/wx/bin/amaya amaya
popd

# install .desktop file, pixmap etc
./script_install_gnomekde ./bin %{buildroot}%{_datadir} %{_datadir}

# install man pages
mkdir -p %{buildroot}%{_mandir}/man1
bzcat %{SOURCE1} > %{buildroot}%{_mandir}/man1/%{name}.1

# install dictionaries
cp %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{buildroot}%{_libdir}/Amaya/dicopar/
pushd %{buildroot}%{_libdir}/Amaya/dicopar/
gunzip *.tgz
for tarfile in *.tar
do
	tar xf $tarfile
done
%__rm -f *.tar
popd

%clean
rm -rf %{buildroot}

%files
%doc Amaya/README* Amaya/amaya/COPYRIGHT*
%{_libdir}/Amaya
%{_mandir}/man1/%{name}.*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png


%changelog
* Sat Feb 25 2012 Andrey Bondrov <abondrov@mandriva.org> 11.4.4-1mdv2012.0
+ Revision: 780723
- Add more patches to fix build errors in Cooker and patch to fix .desktop file
- Replace patch for libpng with better one (adds libpng15 support)
- Drop old unused patches, add patch for new png lib support
- New version 11.4.4, spec cleanup

  + Oden Eriksson <oeriksson@mandriva.com>
    - the mass rebuild of 2010.0 packages

  + Lonyai Gergely <aleph@mandriva.org>
    - Add new spellcheck files.
    - 11.3

* Wed Sep 02 2009 Thierry Vignaud <tv@mandriva.org> 10.0-3mdv2010.0
+ Revision: 424101
- rebuild

* Tue Sep 01 2009 Thierry Vignaud <tv@mandriva.org> 10.0-2mdv2010.0
+ Revision: 423944
- rebuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 10.0-1mdv2009.0
+ Revision: 218429
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Feb 27 2008 Frederik Himpe <fhimpe@mandriva.org> 10.0-1mdv2008.1
+ Revision: 175926
- Final version 10.0

* Sat Feb 02 2008 Funda Wang <fwang@mandriva.org> 10.0-0.pre.1mdv2008.1
+ Revision: 161333
- New version 10.0 pre

* Thu Jan 31 2008 Thierry Vignaud <tv@mandriva.org> 9.99-3mdv2008.1
+ Revision: 160819
- reverse dep fix (amaya-0.99.9 seems fixed regarding this)

* Tue Jan 29 2008 Thierry Vignaud <tv@mandriva.org> 9.99-2mdv2008.1
+ Revision: 159763
- add missing require on lib64wxgtkglu2.6 (#35671)

* Thu Jan 17 2008 Crispin Boylan <crisb@mandriva.org> 9.99-1mdv2008.1
+ Revision: 154503
- New release#
- New release

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Nov 13 2007 Crispin Boylan <crisb@mandriva.org> 9.55-3mdv2008.1
+ Revision: 108560
- Drop patch 2
- Fix symbolic links (#34539)

  + Thierry Vignaud <tv@mandriva.org>
    - fix paths in helper scripts
    - fix links

* Sat Oct 13 2007 Crispin Boylan <crisb@mandriva.org> 9.55-1mdv2008.1
+ Revision: 97993
- Update patch1 (amd64 fixes)
- New version

  + Thierry Vignaud <tv@mandriva.org>
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'
    - fix man pages


* Sat Jan 06 2007 Crispin Boylan <crisb@mandriva.org> 9.53-1mdv2007.0
+ Revision: 104990
- Respin patch 1
- Various spec fixes
- XDG Menu
- New version
- Import amaya

* Wed Nov 30 2005 Thierry Vignaud <tvignaud@mandriva.com> 9.2.2-1mdk
- new release
- use system redland library
- patch 0: fix build with current redland
- patch 1: 64bit fixes for x86_64
- patch 2: first bits toward using system w3c library
- fix binary link on x86_64 (blino)

* Tue Aug 17 2004 Thierry Vignaud <tvignaud@mandrakesoft.com> 8.6-1mdk
- new release

* Thu May 20 2004 Austin Acton <austin@mandrake.org> 8.5-1mdk
- 8.5
- disable bookmarks (redlan mayhem)

