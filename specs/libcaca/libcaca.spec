# $Id$
# Authority: dag
# Upstream: Sam Hocevar <sam$zoy,org>

%{!?ruby_sitearchdir: %global ruby_sitearchdir %(ruby -rrbconfig -e "puts Config::CONFIG['sitearchdir']")}
%{!?ruby_sitelibdir: %global ruby_sitelibdir %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"] ')}

%define _without_java 1

%{?el4:%define _without_modxorg 1}
%{?el4:%define _without_ruby_abi 1}
%{?el3:%define _without_glut 1}
%{?el3:%define _without_modxorg 1}
%{?el3:%define _without_ruby 1}

%define version_beta .beta17

Summary: Library for Colour AsCii Art, text mode graphics
Name: libcaca
Version: 0.99
Release: 0.1%{?version_beta}%{?dist}
License: LGPLv2
Group: System Environment/Libraries
URL: http://caca.zoy.org/

Source: http://caca.zoy.org/files/libcaca/libcaca-%{version}%{?version_beta}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: doxygen
BuildRequires: cppunit-devel
BuildRequires: imlib2-devel
BuildRequires: ncurses-devel >= 5
BuildRequires: pango-devel
BuildRequires: slang-devel
BuildRequires: tetex-dvips
BuildRequires: tetex-latex
BuildRequires: zlib-devel
%{!?_without_ruby:BuildRequires: ruby >= 1.8, ruby-devel >= 1.8}
%{!?_without_glut:BuildRequires: glut-devel}
%{?_without_modxorg:BuildRequires: XFree86-devel}
%{!?_without_modxorg:BuildRequires: libX11-devel, libXt-devel}

%description
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

%package devel
Summary: Development files for libcaca, the library for Colour AsCii Art
Group: Development/Libraries
Requires: ncurses-devel >= 5
Requires: slang-devel
%{?_without_modxorg:Requires: XFree86-devel}

%description devel
libcaca is the Colour AsCii Art library. It provides high level functions
for colour text drawing, simple primitives for line, polygon and ellipse
drawing, as well as powerful image to text conversion routines.

This package contains the header files and static libraries needed to
compile applications or shared objects that use libcaca.

%package -n caca-utils
Summary: Colour AsCii Art Text mode graphics utilities based on libcaca
Group: Amusements/Graphics

%description -n caca-utils
This package contains utilities and demonstration programs for libcaca, the
Colour AsCii Art library.

cacaview is a simple image viewer for the terminal. It opens most image
formats such as JPEG, PNG, GIF etc. and renders them on the terminal using
ASCII art. The user can zoom and scroll the image, set the dithering method
or enable anti-aliasing.

cacaball is a tiny graphic program that renders animated ASCII metaballs on
the screen, cacafire is a port of AALib's aafire and displays burning ASCII
art flames, and cacademo is a simple application that shows the libcaca
rendering features such as line and ellipses drawing, triangle filling and
sprite blitting.

%package -n ruby-caca
Summary: Ruby bindings for libcaca
Group: Development/Languages
Requires: %{name} = %{version}-%{release}
Requires: ruby >= 1.8
%{!?_without_ruby_abi:Requires: ruby(abi) >= 1.8}

%description -n ruby-caca
This package contains Ruby bindings for libcaca.

%prep
%setup -n %{name}-%{version}%{?version_beta}

%build
%configure \
    --program-prefix="%{?_program_prefix}" \
    --x-libraries="%{_prefix}/X11R6/%{_lib}" \
%{?_without_java:--disable-java} \
    --disable-rpath \
%{?_without_ruby:--disable-ruby} \
    --disable-static \
    --enable-imlib2 \
    --enable-ncurses \
    --enable-slang \
    --enable-x11
%{__perl} -pi.orig -e '
        s|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g;
        s|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g;
    ' libtool
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%{_libdir}/libcaca.so.*
%{_libdir}/libcaca++.so.*
%{_libdir}/libcucul.so.*
%{_libdir}/libcucul++.so.*

%files devel
%defattr(-, root, root, 0755)
%doc ChangeLog COPYING
%doc %{_mandir}/man1/caca-config.1*
%doc %{_mandir}/man3/*.3*
%doc %{_docdir}/libcaca-dev/*
%doc %{_docdir}/libcucul-dev
%{_bindir}/caca-config
%{_includedir}/caca.h
%{_includedir}/caca0.h
%{_includedir}/caca++.h
%{_includedir}/caca_conio.h
%{_includedir}/caca_types.h
%{_includedir}/cucul.h
%{_libdir}/libcaca.so
%{_libdir}/libcaca++.so
%{_libdir}/libcucul.so
%{_libdir}/libcucul++.so
%{_libdir}/pkgconfig/caca.pc
%{_libdir}/pkgconfig/caca++.pc
%{_libdir}/pkgconfig/cucul.pc
%{_libdir}/pkgconfig/cucul++.pc
%exclude %{_libdir}/libcaca.la
%exclude %{_libdir}/libcaca++.la
%exclude %{_libdir}/libcucul.la
%exclude %{_libdir}/libcucul++.la
%exclude %{_libdir}/libcaca.la
%exclude %{_libdir}/libcucul.la

%files -n caca-utils
%defattr(-, root, root, 0755)
%doc AUTHORS COPYING NEWS NOTES README THANKS
%doc %{_mandir}/man1/cacademo.1*
%doc %{_mandir}/man1/cacafire.1*
%doc %{_mandir}/man1/cacaplay.1*
%doc %{_mandir}/man1/cacaserver.1*
%doc %{_mandir}/man1/cacaview.1*
%doc %{_mandir}/man1/img2txt.1*
%{_bindir}/cacademo
%{_bindir}/cacafire
%{_bindir}/cacaplay
%{_bindir}/cacaserver
%{_bindir}/cacaview
%{_bindir}/img2txt
%{_datadir}/libcaca/

%if %{!?_without_ruby:1}0
%files -n ruby-caca
%defattr(-, root, root, 0755)
%{ruby_sitearchdir}/caca.so
%{ruby_sitelibdir}/caca.rb
%exclude %{ruby_sitearchdir}/caca.la
%endif

%changelog
* Sat Jun 12 2010 Yury V. Zaytsev <yury@shurup.com> - 0.99-0.1.beta17
- Updates from Bjarne Saltbaek.
- Minor fixes.

* Tue May 26 2009 Dag Wieers <dag@wieers.com> - 0.99-0.1.beta16
- Updated to release 0.99.beta16.

* Fri May 04 2007 Dag Wieers <dag@wieers.com> - 0.99-0.1.beta11
- Updated to release 0.99.beta11.

* Wed Nov  3 2004 Matthias Saou <http://freshrpms.net/> 0.9-4
- Disable man3 pages, they don't build on FC3, this needs fixing.
- Fix to not get the debuginfo files go into the devel package.

* Wed May 19 2004 Matthias Saou <http://freshrpms.net/> 0.9-3
- Rebuild for Fedora Core 2.

* Tue Feb 24 2004 Matthias Saou <http://freshrpms.net/> 0.9-2
- Fix License tag from GPL to LGPL.

* Mon Feb  9 2004 Matthias Saou <http://freshrpms.net/> 0.9-1
- Update to 0.9.
- Added cacamoir and cacaplas.

* Fri Jan  9 2004 Matthias Saou <http://freshrpms.net/> 0.7-1
- Spec file cleanup for Fedora Core 1.

* Sat Jan 7 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.7-1
- new release

* Sat Jan 4 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.6-2
- install documentation into {doc}/package-version instead of {doc}/package
- added tetex-dvips to the build dependencies

* Sat Jan 3 2004 Sam Hocevar (RPM packages) <sam+rpm@zoy.org> 0.6-1
- new release
- more detailed descriptions
- split the RPM into libcaca-devel and caca-utils
- packages are rpmlint clean

* Mon Dec 29 2003 Richard Zidlicky <rz@linux-m68k.org> 0.5-1
- created specfile

