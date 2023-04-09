#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Matroska2 library for Belledonne Communications projects
Summary(pl.UTF-8):	Biblioteka Matroska2 do projektów Belledonne Communications
Name:		bcmatroska2
Version:	5.2.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bcmatroska2/-/tags
Source0:	https://gitlab.linphone.org/BC/public/bcmatroska2/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	dc8602f20ca33c6e3e6b08fd6b527abc
Patch0:		%{name}-static.patch
Patch1:		%{name}-link.patch
URL:		https://linphone.org/
BuildRequires:	cmake >= 3.1
BuildRequires:	rpmbuild(macros) >= 1.605
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
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_static_libs:-DENABLE_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_datadir}/bcmatroska2/cmake/BcMatroska2Targets.cmake

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
%dir %{_datadir}/bcmatroska2
%{_datadir}/bcmatroska2/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbcmatroska2.a
%endif
