# $Id$
# Authority: dag
# Upstream: Tony Bowden <tony$tmtm,com>

%define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)

%define real_name CGI-Untaint-date

Summary: Perl module to validate a date
Name: perl-CGI-Untaint-date
Version: 1.00
Release: 1%{?dist}
License: Artistic
Group: Applications/CPAN
URL: http://search.cpan.org/dist/CGI-Untaint-date/

Source: http://www.cpan.org/modules/by-module/CGI/CGI-Untaint-date-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch: noarch
BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)
Requires: perl

%description
CGI-Untaint-date is a Perl module to validate a date.

%prep
%setup -n %{real_name}-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install

### Clean up buildroot
find %{buildroot} -name .packlist -exec %{__rm} {} \;

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes MANIFEST META.yml README
%doc %{_mandir}/man3/CGI::Untaint::date.3pm*
%dir %{perl_vendorlib}/CGI/
%dir %{perl_vendorlib}/CGI/Untaint/
%{perl_vendorlib}/CGI/Untaint/date.pm

%changelog
* Mon Apr 30 2007 Dag Wieers <dag@wieers.com> - 1.00-1
- Initial package. (using DAR)
