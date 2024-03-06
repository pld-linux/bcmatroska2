#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Matroska2 library for Belledonne Communications projects
Summary(pl.UTF-8):	Biblioteka Matroska2 do projektów Belledonne Communications
Name:		bcmatroska2
Version:	5.3.26
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bcmatroska2/-/tags
Source0:	https://gitlab.linphone.org/BC/public/bcmatroska2/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	3a01147f051a1a05a97382cf84eabae3
URL:		https://linphone.org/
BuildRequires:	bctoolbox-devel >= 5.3.0
BuildRequires:	cmake >= 3.1
BuildRequires:	rpmbuild(macros) >= 1.605
Requires:	bctoolbox >= 5.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Matroska2 library for Belledonne Communications projects.

%description -l pl.UTF-8
Biblioteka Matroska2 do projektów Belledonne Communications.

%package devel
Summary:	Header files for bcmatroska2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki bcmatroska2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bctoolbox-devel >= 5.3.0
Obsoletes:	matroska-foundation-devel < 0.1

%description devel
Header files for bcmatroska2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki bcmatroska2.

%package static
Summary:	Static bcmatroska2 library
Summary(pl.UTF-8):	Statyczna biblioteka bcmatroska2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static bcmatroska2 library.

%description static -l pl.UTF-8
Statyczna biblioteka bcmatroska2.

%prep
%setup -q

%build
%if %{with static_libs}
install -d builddir-static
cd builddir-static
%cmake .. \
	-DBUILD_SHARED_LIBS=OFF

%{__make}
cd ..
%endif

install -d builddir
cd builddir
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbcmatroska2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbcmatroska2.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbcmatroska2.so
%{_includedir}/corec
%{_includedir}/ebml
%{_includedir}/matroska
%dir %{_datadir}/BCMatroska2
%{_datadir}/BCMatroska2/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbcmatroska2.a
%endif
