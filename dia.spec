%define pre 0
%if %pre
%define rel 1
%define fname %name-%version-%pre
%else 
%define rel 1
%define fname %name-%version
%endif
Summary: A gtk+ based diagram creation program
Name: dia
Version: 0.97.2
Release: %mkrel %rel
License: GPLv2+
Group: Office
Source: ftp://ftp.gnome.org/pub/GNOME/sources/%name/%{fname}.tar.xz
Patch0: dia-0.97.1-use-own-gtkrc.patch
#gw quick hack to find the gnome documentation
Patch1: dia-0.97.1-help.patch
Patch2: dia-0.97.2-fix-glib-includes.patch
Patch3: dia-0.97.2-vdx-fix-includes.patch
URL: http://www.gnome.org/projects/dia 
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires:	docbook-utils
BuildRequires:	pygtk2.0
BuildRequires:	python-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	png-devel
BuildRequires:	libxslt-devel
BuildRequires:	cairo-devel
BuildRequires:	intltool
BuildRequires:	autoconf2.5
BuildRequires:  PyXML
BuildRequires:	libxslt-proc
BuildRequires:	scrollkeeper
BuildRequires:	docbook-style-xsl
BuildRequires:	desktop-file-utils
#gw if we run aclocal or autogen.sh
BuildRequires:	libtool gnome-common
Requires:	pygtk2.0
#gw help viewer also for non-GNOME
Suggests:	yelp
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
Dia is a program designed to be much like the Windows
program 'Visio'. It can be used to draw different kind of diagrams. In
this first version there is support for UML static structure diagrams
(class diagrams) and Network diagrams. It can currently load and save
diagrams to a custom fileformat and export to postscript.

%prep
%setup -q -n %fname
%apply_patches

# gw fix doctype
perl -pi -e "s^../../dtd/docbookx.dtd^http://www.oasis-open.org/docbook/xml/4.2/docbookx.dtd^" doc/*/dia.xml

# Let it find python libraries gracefully
perl -pi -e "s,/lib/(python),/%{_lib}/\1,g" configure

%build
%configure2_5x --enable-gnome --with-python --with-cairo

%make libdia_la_LIBADD="\$(GTK_LIBS)"

%install
rm -fr %{buildroot}

%makeinstall_std

# fix en documentation directory name
rm -f %buildroot%_datadir/gnome/help/%name/C
mv %buildroot%_datadir/gnome/help/%name/en %buildroot%_datadir/gnome/help/%name/C

#fix icon and invalid version in bugzilla field
sed -i -e 's/@\(%{version}\)@/\1/g' -e 's/Icon=dia_gnome_icon.png/Icon=dia_gnome_icon/g' %{buildroot}%{_datadir}/applications/dia.desktop

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GTK" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/dia.desktop


#for i in %{buildroot}%{_datadir}/dia/sheets/{ER,GRAFCET,Istar,KAOS,Jackson}/*.xpm ; do
# convert $i `dirname $i`/`basename $i .xpm`.png
#done

%{find_lang} %{name} --with-gnome
for omf in %buildroot%_datadir/omf/*/*-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done


chmod 644 %buildroot%_libdir/%name/*.la

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README TODO NEWS INSTALL COPYING ChangeLog AUTHORS
%{_bindir}/*
%{_libdir}/dia
%{_mandir}/*/*
%{_datadir}/dia
%{_datadir}/mime-info/*
%{_datadir}/applications/dia.desktop
%_datadir/icons/hicolor/*/*/*
%dir %_datadir/omf/%name
%_datadir/omf/%name/%name-C.omf
