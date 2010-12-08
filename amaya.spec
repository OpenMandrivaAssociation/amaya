%define	name amaya
%define version 11.3.1
%define release %mkrel 2
%define wxwidgets_version 2.9.0

%define system_libwww	0
%define system_raptor	0
%define system_wx	0
%define build_gl	0
%{?_with_system_libwww:	%global system_libwww 1}
%{?_with_system_raptor:	%global system_raptor 1}
%{?_with_system_wx:	%global system_wx 1}
%{?_with_gl:		%global build_gl 1}

Name:		%{name}
Version: 	%{version}
Release: 	%{release}
Summary: 	Web Browser/Editor from the World Wide Web Consortium
Group:   	Networking/WWW
Source0: 	http://www.w3.org/Amaya/Distribution/amaya-fullsrc-%{version}.tgz
Source1: 	%name.1.bz2
#2010-01-06
Source10:	http://www.w3.org/Amaya/Distribution/Dutch.tgz
Source11:	http://www.w3.org/Amaya/Distribution/English.tgz
Source12:	http://www.w3.org/Amaya/Distribution/French.tgz
Source13:	http://www.w3.org/Amaya/Distribution/German.tgz
Source14:	http://www.w3.org/Amaya/Distribution/Italian.tgz
Source15:	http://www.w3.org/Amaya/Distribution/Spanish.tgz
Source16:	http://www.w3.org/Amaya/Distribution/Swedish.tgz
#Source17:	http://downloads.sourceforge.net/project/wxwindows/wxAll/%{wxwidgets_version}/wxWidgets-%{wxwidgets_version}.tar.bz2
Patch0:		amaya-0.9.1-fix-build.patch
Patch1:		amaya-9.55-fix-build-x86_64.patch
# enable to link with system libw3c-libwww lib:
# BuildConflicts: w3c-libwww-devel
# Patch2:		amaya-0.9.1-fix-link.patch.bz2
License: 	W3C License
Url:     	http://www.w3.org/Amaya/
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	freetype-devel, gtk2-devel, imlib-devel
BuildRequires: 	libstdc++-devel, jpeg-devel, png-devel, libz-devel
BuildRequires: 	perl, bison, flex
%if %{system_raptor}
BuildRequires:	raptor-devel
%endif
BuildRequires:	libx11-devel, mesagl-devel, mesaglu-devel
BuildRequires:	redland-devel
%if %{system_wx}
BuildRequires:	libwxgtk2.8-devel, wxgtku-devel
%endif
%if %{system_libwww}
BuildRequires:	w3c-libwww-devel
%endif
Obsoletes:	amaya-common amaya-gtk amaya-lesstif
Provides:	amaya-common amaya-wx 

%description
Amaya is a complete Web authoring tool with some browsing 
funtionalities and comes equipped with a WYSIWYG style of
interface, similar to that of the most popular commercial
browsers. With such an interface, users do not need to 
well know the HTML, MathML or CSS languages.

This graphical HTML Editor supports many of the latest
draft standards for HTML/XHTML.

%prep
%setup -q -n Amaya
#%setup -q -n wxWidgets-%{wxwidgets_version} -T -b 17
#%setup -q -n Amaya%{version}/Amaya -D -T
#rm -rf ../wxWidgets
#ln -s ../wxWidgets-%{wxwidgets_version} ../wxWidgets

%build
#cd Amaya
#%ifarch x86_64
#	cp ../Mesa/configs/linux-x86-64-static ../Mesa/configs/current
#%endif
autoconf

mkdir -p WX
cd WX
touch ./configure.in
ln -s ./../configure ./configure
%configure2_5x \
	--with-dav \
%if %{system_wx}
	--enable-system-wx \
%else
	--disable-system-wx \
%endif
%if %{system_libwww}
        --enable-system-libwww \
%else
        --disable-system-libwww \
%endif
%if %{system_raptor}
        --enable-system-raptor \
%else
        --disable-system-raptor \
%endif
%if build_gl
	--with-gl
%else
	--with-mesa
%endif
#%make depend
%make -j1

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%_mandir/man1
mkdir -p %{buildroot}/%_bindir
#make install prefix=%{buildroot}%{_libdir}
%makeinstall
#./script_install %{builddir}/Amaya/WX/bin/ %{buildroot}/%{_prefix} %{buildroot}/%{_bindir} 

pushd %{buildroot}/%_bindir/
	ln -sf ../../%{_libdir}/Amaya/wx/bin/amaya-mesa amaya
	#ln -sf ../../%{_libdir}/Amaya/wx/bin/amaya amaya
popd
./script_install_gnomekde ./bin %{buildroot}/%{_datadir} %{_datadir}

# Man pages
bzcat %{source1} > %{buildroot}/%{_mandir}/man1/%{name}.1

mkdir %{buildroot}/%{libdir}/Amaya/discopar
for T_FILE in %{source10} %{source11} %{source12} %{source13} %{source14} %{source15} %{source16} ; do
	cp ${T_FILE} %{buildroot}/%{libdir}/Amaya/discopar/
	T_FILE2='ls *.tar | sed "s/tar$/dic"'
	gunzip *.tzg
	tar xf *.tar
	cp Wprinc.dic ${T_FILE2}
done

%clean
rm -rf %{buildroot}

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
%{_libdir}/Amaya*
%{_mandir}/man1/%{name}.*
%{_bindir}/%{name}-mesa
%{_bindir}/%{name}-gl
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
