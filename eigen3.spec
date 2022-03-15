# The (empty) main package is arch, to have the package built and tests run
# on all arches, but the actual result package is the noarch -devel subpackge.
# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}

%global commit 323c052e1731

%global optflags %{optflags} -O3

Summary: Lightweight C++ template library for vector and matrix math
Name: eigen3
Version: 3.4.0
Release: 2
Group: System/Libraries
License: LGPLv3+ or GPLv2+
URL: http://eigen.tuxfamily.org/
Source0: https://gitlab.com/libeigen/eigen/-/archive/%{version}/eigen-%{version}.tar.bz2
BuildRequires: cmake >= 2.6.1
BuildRequires: doxygen
BuildRequires: pkgconfig(fftw3)
BuildRequires: pkgconfig(glew)
BuildRequires: pkgconfig(glut)
BuildRequires: gmp-devel
BuildRequires: umfpack-devel
BuildRequires: cholmod-devel
BuildRequires: libspqr-devel
BuildRequires: boost-devel
BuildRequires: ghostscript-common
BuildRequires: graphviz
BuildRequires: pkgconfig(gsl)
BuildRequires: pkgconfig(atlas)
BuildRequires: pkgconfig(mpfr)
BuildRequires: SuperLU-devel
BuildRequires: texlive
BuildRequires: pkgconfig(xmu)

%description
Eigen is a lightweight C++ template library for vector and matrix
math, a.k.a. linear algebra.

%package devel
Summary: Lightweight C++ template library for vector and matrix math
Group: Development/C++
BuildArch: noarch
%rename %name
# not *strictly* a -static pkg, but the results are the same
Provides: %{name}-static = %{version}-%{release}

%description devel
Eigen is a lightweight C++ template library for vector and matrix
math, a.k.a. linear algebra.

%prep
%autosetup -p1 -n eigen-%{version}

%build
%ifarch %arm
export CC=gcc
export CXX=g++
%endif

%cmake -DBLAS_LIBRARIES="cblas" -DSUPERLU_INCLUDES=%{_includedir}/SuperLU

%make_build

rm -f doc/html/installdox
rm -f doc/html/unsupported/installdox

%install
%make_install -C build

%files devel
%doc COPYING*
%dir %{_includedir}/eigen3/
%{_includedir}/eigen3/*
%{_datadir}/pkgconfig/*.pc
%{_datadir}/eigen3
