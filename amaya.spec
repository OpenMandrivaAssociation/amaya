%define system_libwww	0
%{?_with_system_libwww:	%global system_libwww 1}

Name:		amaya
Version: 	11.4.4
Release: 	%mkrel 1
Summary: 	Web Browser/Editor from the World Wide Web Consortium
Group:   	Networking/WWW
License: 	W3C License
Url:		http://www.w3.org/Amaya/
Source0: 	http://www.w3.org/Amaya/Distribution/amaya-fullsrc-%{version}.tgz
Source1: 	%{name}.1.bz2
#2010-01-06
Source10:	http://www.w3.org/Amaya/Distribution/Dutch.tgz
Source11:	http://www.w3.org/Amaya/Distribution/English.tgz
Source12:	http://www.w3.org/Amaya/Distribution/French.tgz
Source13:	http://www.w3.org/Amaya/Distribution/German.tgz
Source14:	http://www.w3.org/Amaya/Distribution/Italian.tgz
Source15:	http://www.w3.org/Amaya/Distribution/Spanish.tgz
Source16:	http://www.w3.org/Amaya/Distribution/Swedish.tgz
Patch2:		amaya-fix-thotlib-png14.patch
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
%patch2 -p1

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
