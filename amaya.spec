Name:		amaya
Version: 	9.55
Release: 	%mkrel 1
Summary: 	W3C's browser/web authoring tool
Group:   	Networking/WWW
Source0: 	http://www.w3.org/Amaya/Distribution/amaya-sources-%{version}-2.tgz
Source1: 	%name.1.bz2
Patch0:		amaya-0.9.1-fix-build.patch
Patch1:		amaya-9.53-fix-build-x86_64.patch
Patch2:		amaya-9.53-png_fix.patch
# enable to link with system libw3c-libwww lib:
# BuildConflicts: w3c-libwww-devel
# Patch2:		amaya-0.9.1-fix-link.patch.bz2
License: 	W3C License
Url:     	http://www.w3.org/Amaya/
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires: 	ungif-devel jpeg-devel png-devel libz-devel
BuildRequires: 	perl bison flex
BuildRequires:	libx11-devel freetype2-devel
BuildRequires:	redland-devel wxgtku2.6-devel
Obsoletes:	amaya-common amaya-gtk amaya-lesstif
Provides:	amaya-common amaya-wx 

%description
Amaya is a WYSIWYG browser/web authoring tool from the W3C.

This graphical HTML Editor supports many of the latest
draft standards for HTML/XHTML.

%prep
%setup -q -n Amaya%{version}
#%patch0 -p0
#%patch1 -p0
#%patch2 -p0

%build
cd Amaya
export CFLAGS="$RPM_OPT_FLAGS"
mkdir -p wx-build
cd wx-build
../configure --prefix=$RPM_BUILD_ROOT%_libdir --exec-prefix=$RPM_BUILD_ROOT/%_prefix --libdir=%_libdir --enable-system-redland --enable-system-wx --with-gl
# make -j2 fails
make

%install
cd Amaya
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_mandir/man1
cd wx-build
make install

pushd $RPM_BUILD_ROOT/%_bindir/
ln -sf ../../usr/%_lib/Amaya-*/wx/bin/amaya amaya-wx
ln -sf ../../usr/%_lib/Amaya-*/wx/bin/amaya amaya
popd

# Mandriva menu entry
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{name}
Comment=%{summary}
Exec=%{_bindir}/%{name} 
Icon=networking_www_section
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;Network;WebBrowser;WebDevelopment;X-MandrivaLinux-Internet-WebBrowsers;
EOF

# Man pages
bzcat %SOURCE1 > $RPM_BUILD_ROOT%_mandir/man1/%name.1

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus

%postun
%clean_menus

%files
%defattr(-,root,root)
%doc Amaya/README* Amaya/amaya/COPYRIGHT*
%_libdir/Amaya*
%_mandir/man1/%name.*
%_bindir/%name
%_bindir/%name-wx
%{_datadir}/applications/mandriva-%{name}.desktop


