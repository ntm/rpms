# $Id$
# Authority: dag

%{?rh9:%define _without_tcltk_devel 1}
%{?rh8:%define _without_tcltk_devel 1}
%{?rh7:%define _without_tcltk_devel 1}
%{?el2:%define _without_tcltk_devel 1}

Summary: Graph Visualization Tools
Name: graphviz
Version: 2.2
Release: 1
License: CPL
Group: Applications/Multimedia
URL: http://www.graphviz.org/

Source: http://www.graphviz.org/pub/graphviz/ARCHIVE/graphviz-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: XFree86-devel, freetype-devel >= 2.0, bison, m4, flex
BuildRequires: libjpeg-devel, libpng-devel, zlib-devel, expat-devel, gcc-c++
#BuildRequires: /bin/ksh
%{!?_without_tcltk_devel:BuildRequires: tcl-devel >= 8.3, tk-devel}
%{?_without_tcltk_devel:BuildRequires: tcl >= 8.3, tk}
# needs version 2.0.29 of gdlib but fc3 contains 2.0.28
# BuildRequires: gd-progs, gd-devel

%description
A collection of tools and tcl packages for the manipulation and layout
of graphs (as in nodes and edges, not as in barcharts).

%package tcl
Group: Applications/Multimedia
Summary: Tcl extension tools for version %{version} of %{name}
Requires: %{name} = %{version}-%{release}, tk

%description tcl
The %{name}-tcl package contains the various tcl packages (extensions)
for version %{version} of the %{name} tools.

%package devel
Summary: Header files, libraries and development documentation for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}.

%package doc
Summary: PDF and HTML documents for %{name}
Group: Documentation

%description doc
Provides some additional PDF and HTML documentation for %{name}.

%package graphs
Summary: Demo graphs for %{name}
Group: Applications/Multimedia

%description graphs
Some demo graphs for %{name}.

%prep
%setup

%build
%{expand: %%define optflags %{optflags} -ffast-math}
%configure \
	--with-mylibgd \
	--with-x
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}" \
	pkgconfigdir=%{_libdir}/pkgconfig \
	transform='s,x,x,'
%{__mv} %{buildroot}%{_datadir}/graphviz/doc rpmdoc
%{__chmod} -x %{buildroot}%{_datadir}/graphviz/lefty/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README *.txt
%doc %{_mandir}/man1/*
%{_bindir}/*
%dir %{_datadir}/graphviz/
%{_datadir}/graphviz/lefty/
%{_libdir}/graphviz/*.so.*
%exclude %{_libdir}/graphviz/lib*tcl*.so.*
%exclude %{_libdir}/graphviz/libtk*.so.*
%exclude %{_bindir}/dotneato-config
%exclude %{_mandir}/man1/dotneato-config.1*

%files tcl
%defattr(-, root, root, 0755)
#%doc doc/tcldot.html
%doc %{_mandir}/mann/*
%{_datadir}/graphviz/demo/
%{_libdir}/graphviz/lib*tcl*.so.*
%{_libdir}/graphviz/libtk*.so.*
%{_libdir}/graphviz/pkgIndex.tcl
%exclude %{_libdir}/%{name}/lib*tcl*.so.?
%exclude %{_libdir}/%{name}/libtk*.so.?

%files devel
%defattr(-, root, root, 0755)
%doc %{_mandir}/man1/dotneato-config.1*
%doc %{_mandir}/man3/*
%{_bindir}/dotneato-config
%{_includedir}/graphviz/
%{_libdir}/graphviz/*.so
%{_libdir}/pkgconfig/*.pc
%exclude %{_libdir}/graphviz/*.la

%files graphs
%defattr(-, root, root, 0755)
%dir %{_datadir}/graphviz/
%{_datadir}/graphviz/graphs/

%files doc
%defattr(-, root, root, 0755)
%doc rpmdoc/*

%changelog
* Fri Mar 11 2005 Dag Wieers <dag@wieers.com> - 2.2-1
- Updated to release 2.2.

* Fri Dec 10 2004 Dries Verachtert <dries@ulyssis.org> 1.16-1
- Updated to release 1.16.

* Tue May 06 2003 Dag Wieers <dag@wieers.com> - 1.8.10-6
- Fixed includedir. (Reported by Thomas Moschny)

* Sun Jan 04 2003 Dag Wieers <dag@wieers.com> - 1.8.10-0
- Initial package. (using DAR)
