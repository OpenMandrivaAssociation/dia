%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

Summary:	A gtk+ based diagram creation program
Name:		dia
Version:	0.97.2
Release:	3
License:	GPLv2+
Group:		Office
Url:		http://www.gnome.org/projects/dia
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/dia/%{url_ver}/%{name}-%{version}.tar.xz
Patch0:		dia-0.97.1-use-own-gtkrc.patch
#gw quick hack to find the gnome documentation
Patch1:		dia-0.97.1-help.patch
Patch2:		dia-0.97.2-fix-glib-includes.patch
Patch3:		dia-0.97.2-vdx-fix-includes.patch

BuildRequires:	intltool
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libpng15)
BuildRequires:	pkgconfig(pangocairo)
Suggests:	yelp
Requires(post,postun):	desktop-file-utils

%description
Dia is a program designed to be much like the Windows
program 'Visio'. It can be used to draw different kind of diagrams. In
this first version there is support for UML static structure diagrams
(class diagrams) and Network diagrams. It can currently load and save
diagrams to a custom fileformat and export to postscript.

%prep
%setup -q
%apply_patches

# gw fix doctype
perl -pi -e "s^../../dtd/docbookx.dtd^http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd^" doc/*/dia.xml

%build
%configure2_5x \
	--enable-gnome \
	--with-cairo

%make libdia_la_LIBADD="\$(GTK_LIBS)"

%install
%makeinstall_std

# fix en documentation directory name
rm -f %{buildroot}%{_datadir}/gnome/help/%{name}/C
mv %{buildroot}%{_datadir}/gnome/help/%{name}/en %{buildroot}%{_datadir}/gnome/help/%{name}/C

#fix icon and invalid version in bugzilla field
sed -i -e 's/@\(%{version}\)@/\1/g' \
	-e 's/Icon=dia_gnome_icon.png/Icon=dia_gnome_icon/g' \
	%{buildroot}%{_datadir}/applications/dia.desktop

desktop-file-install \
	--vendor="" \
	--remove-category="Application" \
	--add-category="GTK" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/dia.desktop

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc README TODO NEWS INSTALL COPYING ChangeLog AUTHORS
%{_bindir}/*
%{_libdir}/dia
%{_datadir}/dia
%{_datadir}/mime-info/*
%{_datadir}/applications/dia.desktop
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/*/*
