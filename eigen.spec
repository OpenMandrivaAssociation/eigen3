# For now -- since C code (built with clang) and
# Fortran code (built with gfortran) are linked
# together, LTO object files don't work
%global _disable_lto 0

# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}

%bcond doc		1
%bcond sparsehash	1
%bcond SuperLU		1
%bcond scotch		1
%bcond metis		1
%bcond tests		0

%global blaslib flexiblas
%global cmake_blas_flags -DBLA_VENDOR=FlexiBLAS

%global optflags %{optflags} -O3

Summary:	Lightweight C++ template library for vector and matrix math
Name:		eigen
Version:	3.4.0
Release:	4
Group:		System/Libraries
License:	LGPLv3+ or GPLv2+
URL:		https://eigen.tuxfamily.org/
Source0:	https://gitlab.com/libeigen/eigen/-/archive/%{version}/%{name}-%{version}.tar.bz2
BuildRequires:	cmake ninja
BuildRequires:	boost-devel
BuildRequires:	gmp-devel
%if %{with SuperLU}
BuildRequires:	cmake(superlu)
%endif
%if %{with metis}
BuildRequires:	metis-devel
%endif
BuildRequires:	pkgconfig(gsl)
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(flexiblas)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(libsparsehash)
BuildRequires:	pkgconfig(mpfr)
BuildRequires:	pkgconfig(xmu)
%if %{with scotch}
BuildRequires:	cmake(scotch)
%endif
%if %{with suitesparse}
BuildRequires:	cholmod-devel
BuildRequires:	libspqr-devel
BuildRequires:	umfpack-devel
%endif
%if %{with doc}
BuildRequires:	doxygen
BuildRequires:	ghostscript-common
BuildRequires:	graphviz
BuildRequires:	texlive
%endif

%description
Eigen is a lightweight C++ template library for vector and matrix
math, a.k.a. linear algebra.

#---------------------------------------------------------------------------

%package devel
Summary:	Lightweight C++ template library for vector and matrix math
Group:		Development/C++
BuildArch:	noarch
Obsoletes:	%{name}3 <= %{EVRD}
# not *strictly* a -static pkg, but the results are the same
Provides:	%{name}-static = %{version}-%{release}

%description devel
Eigen is a lightweight C++ template library for vector and matrix
math, a.k.a. linear algebra.

%files devel
%license COPYING*
%dir %{_includedir}/eigen3/
%if %{with doc}
%doc %{_vpath_builddir}/doc/html
%endif
%{_includedir}/eigen3/*
%{_datadir}/pkgconfig/*.pc
%dir %{_datadir}/cmake/%{name}/
%{_datadir}/cmake/%{name}/*

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
#ifarch %arm
#export CC=gcc
#export CXX=g++
#endif
export FC=gfortran


%cmake -Wno-dev \
	-DCMAKEPACKAGE_INSTALL_DIR=%{_datadir}/cmake/%{name} \
	-DBLAS_LIBRARIES="%{blaslib}" \
	-DBLA_VENDOR=-DBLA_VENDOR=FlexiBLAS \
	-DBUILD_TESTING:BOOL=%{?with_tests:ON}%{?!with_tests:OFF} \
	-DEIGEN_BUILD_DOC:BOOL=%{?with_doc:ON}%{?!with_doc:OFF} \
	-GNinja
cd ..
%ninja_build -C ./build

%if %{with doc}
%ninja_build -C ./build doc
%endif

rm -f doc/html/installdox
rm -f doc/html/unsupported/installdox

%install
%ninja_install -C build

%check
%if %{with tests}
pushd build
ctest
done
%endif

