# Thin HIP RNG wrapper over rocRAND (TheRock 10.0)

Name:		hiprand
Version:	10.0.0
Release:	1
Summary:	HIP random number generation (rocRAND wrapper)
License:	MIT
Group:		System/Libraries
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-10.0/hiprand.tar.gz#/hiprand-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocminfo
BuildRequires:	clang-tools
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}
BuildRequires:	rocrand-devel


%description
hipRAND is a thin HIP API wrapper over rocRAND. Built for GPU targets
including gfx803 on OpenMandriva.

%package devel
Summary:	Development files for hiprand
Group:		Development/C++
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	rocm-hip-devel
Requires:	rocrand-devel
Provides:	hiprand-devel = %{EVRD}

%description devel
Headers and CMake package for hiprand.

%prep
%autosetup -n hiprand

export CXX=hipcc
export CC=clang
export ROCM_PATH=%{_prefix}
export HIP_PATH=%{_prefix}
CXXFLAGS=$(printf '%s' "%{optflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
export LDFLAGS=$(printf '%s' "%{?__global_ldflags}" | sed -E 's/-mfpmath=[^ ]+//g; s/ -m[a-z0-9+.=]+//g')
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_prim} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DBUILD_TEST=OFF \
	-DBUILD_BENCHMARK=OFF \
	-DBUILD_SHARED_LIBS=ON \
	-DBUILD_WITH_LIB=ROCM \
	-DROCRAND_FETCH_METHOD=PACKAGE \
	-DDOWNLOAD_ROCRAND=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
if [ -d %{buildroot}/usr/lib/cmake/hiprand ] && [ ! -d %{buildroot}%{_libdir}/cmake/hiprand ]; then
	mkdir -p %{buildroot}%{_libdir}/cmake
	mv %{buildroot}/usr/lib/cmake/hiprand %{buildroot}%{_libdir}/cmake/
	rmdir %{buildroot}/usr/lib/cmake 2>/dev/null || true
	rmdir %{buildroot}/usr/lib 2>/dev/null || true
fi

%files
%license LICENSE.md
%doc README.md
%exclude %{_docdir}/hiprand/LICENSE.md
%{_libdir}/libhiprand.so.*

%files devel
%{_includedir}/hiprand/
%{_libdir}/libhiprand.so
%{_libdir}/cmake/hiprand/
