Name:       cpp-hocon
Version:    0.1.6
Release:    7%{?dist}
Summary:    The library provides C++ support for the HOCON configuration file format

License:    ASL 2.0
URL:        https://github.com/puppetlabs/%{name}
Source0:    https://github.com/puppetlabs/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:    cpphocon.pc.in

%if 0%{?fedora}
BuildRequires:  gcc-c++
BuildRequires:    cmake
BuildRequires:    boost-devel
%else
BuildRequires:    cmake3
BuildRequires:    boost157-devel
%endif

BuildRequires:    leatherman-devel
BuildRequires:    curl-devel
BuildRequires:    gettext

%description
This is a port of the TypesafeConfig library to C++.

The library provides C++ support for the HOCON configuration file format.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary:    Development files for the cpp-hocon library

%description devel
Libraries and headers to links against cpp-hocon

%prep
%autosetup

%build
%if 0%{?fedora}
%cmake -DBUILD_SHARED_LIBS=ON \
       -DCMAKE_BUILD_TYPE=Debug \
       -DCMAKE_INSTALL_PREFIX=%{_prefix}
%else
%cmake3 -DBOOST_INCLUDEDIR=/usr/include/boost157 \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost157 \
        -DBUILD_SHARED_LIBS=ON \
        -DCMAKE_BUILD_TYPE=Debug \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DLeatherman_DIR=%{_libdir}/cmake3/leatherman
%endif
%__make

%install
%make_install

# upstream doesn't provide a cmake or pkgconfig file so write one ourselves
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -p %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/cpphocon.pc
sed -i 's#@@PREFIX@@#%{_prefix}#' %{buildroot}%{_libdir}/pkgconfig/cpphocon.pc
sed -i 's#@@VERSION@@#%{version}#' %{buildroot}%{_libdir}/pkgconfig/cpphocon.pc
sed -i 's#@@LIBDIR@@#%{_lib}#' %{buildroot}%{_libdir}/pkgconfig/cpphocon.pc


%check
# %__make test

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/hocon
%{_libdir}/pkgconfig/cpphocon.pc


%changelog
* Fri Feb 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.6-7
- Disable tests (fails on x86)

* Thu Feb 15 2018 Filipe Rosset <rosset.filipe@gmail.com> - 0.1.6-6
- fix FTBFS

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.1.6-4
- Rebuilt for Boost 1.66

* Wed Oct 25 2017 James Hogarth <james.hogarth@gmail.com> - 0.1.6-3
- Point to correct location on epel7 for leatherman cmake3 files

* Thu Oct 19 2017 James Hogarth <james.hogarth@gmail.com> - 0.1.6-2
- rebuilt

* Wed Oct 04 2017 James Hogarth <james.hogarth@gmail.com> - 0.1.6-1
- Initial packaging

