Name:		amaya
Version: 	10.0
Release: 	%mkrel 3
Summary: 	W3C's browser/web authoring tool
Group:   	Networking/WWW
Source0: 	http://www.w3.org/Amaya/Distribution/amaya-sources-%{version}.tgz
Source1: 	%name.1.bz2
Patch0:		amaya-0.9.1-fix-build.patch
Patch1:		amaya-9.55-fix-build-x86_64.patch
# enable to link with system libw3c-libwww lib:
# BuildConflicts: w3c-libwww-devel
# Patch2:		amaya-0.9.1-fix-link.patch.bz2
License: 	W3C License
Url:     	http://www.w3.org/Amaya/
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires: 	ungif-devel jpeg-devel png-devel libz-devel
BuildRequires: 	perl bison flex
BuildRequires:	libx11-devel freetype2-devel
BuildRequires:	redland-devel wxgtku2.8-devel
Obsoletes:	amaya-common amaya-gtk amaya-lesstif
Provides:	amaya-common amaya-wx 

%description
Amaya is a WYSIWYG browser/web authoring tool from the W3C.

This graphical HTML Editor supports many of the latest
draft standards for HTML/XHTML.

%prep
%setup -q -n Amaya%{version}

%build
cd Amaya
export CFLAGS="$RPM_OPT_FLAGS"
mkdir -p wx-build
cd wx-build
../configure --prefix=%_libdir --exec=%_libdir --libdir=%_libdir --enable-system-redland --enable-system-wx --with-gl
# make -j2 fails
make

%install
cd Amaya
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_mandir/man1
mkdir -p $RPM_BUILD_ROOT/%_bindir
cd wx-build
make install prefix=$RPM_BUILD_ROOT%_libdir

pushd $RPM_BUILD_ROOT/%_bindir/
ln -sf ../../usr/%_lib/Amaya/wx/bin/amaya amaya-wx
ln -sf ../../usr/%_lib/Amaya/wx/bin/amaya amaya
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

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%files
%defattr(-,root,root)
%doc Amaya/README* Amaya/amaya/COPYRIGHT*
%_libdir/Amaya*
%_mandir/man1/%name.*
%_bindir/%name
%_bindir/%name-wx
%{_datadir}/applications/mandriva-%{name}.desktop


