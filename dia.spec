%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)
%define libname %mklibname %{name}

Summary:	A gtk+ based diagram creation program
Name:		dia
Version:	0.98.0
Release:	6
License:	GPLv2+
Group:		Office
Url:		http://www.gnome.org/projects/dia
Source0:	http://ftp.gnome.org/pub/GNOME/sources/dia/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		revert-xpm-loader-replacement.patch
Patch1:		dia-0.98.0-vdx-fix-includes.patch
Patch2:		fix-libdia-install-dir.patch
BuildRequires:	intltool
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(graphene-1.0)
BuildRequires:	pkgconfig(libart-2.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	xmlto docbook-dtds
Suggests:	yelp
Requires(post,postun):	desktop-file-utils

%description
Dia is a program designed to be much like the Windows
program 'Visio'. It can be used to draw different kind of diagrams. In
this first version there is support for UML static structure diagrams
(class diagrams) and Network diagrams. It can currently load and save
diagrams to a custom fileformat and export to postscript.

%prep
%autosetup -p1
# gw fix doctype
chmod +x %{_builddir}/%{buildsubdir}/plug-ins/python/doxrev.py
chmod +x %{_builddir}/%{buildsubdir}/plug-ins/python/python-startup.py
sed -i -e "s^../../dtd/docbookx.dtd^http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd^" doc/*/dia.xml
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
%meson 	

%build 
export LIBS=-lgmodule-2.0
chmod -x %{_builddir}/%{buildsubdir}/shapes/Civil/civil_aerator.shape

%meson_build -v

%meson_install

%find_lang %{name} --with-gnome --all-name --with-html

%files -f %{name}.lang
%doc  TODO NEWS COPYING AUTHORS
%{_bindir}/*
%{_libdir}/*
%{_datadir}/dia/python
%{_datadir}/dia/shapes
%{_datadir}/dia/ui
%{_datadir}/dia/sheets
%{_datadir}/dia/xslt
%{_datadir}/dia/python-startup.py
%{_datadir}/metainfo/*.xml
%{_datadir}/thumbnailers/*.thumbnailer
%{_datadir}/applications/org.gnome.Dia.desktop
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/*/*

%lang(en) %doc %{_datadir}/dia/help/en/
%lang(eu) %doc %{_datadir}/dia/help/eu/
%lang(fr) %doc %{_datadir}/dia/help/fr/
%lang(de) %doc %{_datadir}/dia/help/de/
