#
# Conditional build:
%bcond_with	mpi		# MPI support
%bcond_without	openmp		# OpenMP support
#
Summary:	High performance preconditioners and solvers library
Summary(pl.UTF-8):	Biblioteka preconditionerów i rozwiązywania układów równań o wysokiej wydajności
Name:		hypre
Version:	2.27.0
Release:	0.1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/hypre-space/hypre/releases
Source0:	https://github.com/hypre-space/hypre/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0fc4d98040c2232e753464ab3fed66aa
#Patch0:	%{name}-what.patch
URL:		https://computing.llnl.gov/projects/hypre-scalable-linear-solvers-multigrid-methods
BuildRequires:	cmake >= 3.13
%if %{with mpi}
BuildRequires:	mpich-devel
%endif
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	rpmbuild(macros) >= 1.605
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	intltool
#BuildRequires:	libtool
# if using noarch subpackages:
#BuildRequires:	rpm-build >= 4.6
#Requires(postun):	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires:	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HYPRE is a library of high performance preconditioners and solvers
featuring multigrid methods for the solution of large, sparse linear
systems of equations on massively parallel computers.

%description -l pl.UTF-8
HYPRE to biblioteka wysoko wydajnych preconditionerów oraz procesdur
rozwiązywania dużych, rzadkich układów równań liniowych z
zastosowaniem metod wielosiatkowych na bardzo zrównoleglonych
komputerach.

%package devel
Summary:	Header files for HYPRE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HYPRE
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for HYPRE library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HYPRE.

%prep
%setup -q

%build
%cmake -B build -S src \
	-DCMAKE_INSTALL_INCLUDEDIR=%{_includedir}/HYPRE \
	-DHYPRE_ENABLE_HYPRE_BLAS=OFF \
	-DHYPRE_ENABLE_HYPRE_LAPACK=OFF \
	-DHYPRE_ENABLE_SHARED=ON \
	%{!?with_mpi:-DHYPRE_WITH_MPI=OFF} \
	%{?with_openmp:-DHYPRE_WITH_OPENMP=ON} \

# HYPRE_ENABLE_HOPSCOTCH?
# HYPRE_WITH_SUPERLU?
# HYPRE_WITH_DSUPERLU?
# HYPRE_WITH_CALIPER?
# HYPRE_WITH_CUDA on bcond + other CUDA options
# HYPRE_WITH_SYCL?
# oneMKL

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG COPYRIGHT LICENSE-MIT NOTICE README.md SUPPORT.md
%attr(755,root,root) %{_libdir}/libHYPRE.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/HYPRE
%{_libdir}/cmake/HYPRE
