%if 0%{?rhel} && 0%{?rhel} <= 7
%global boost_suffix 169
%global cmake_suffix 3
%global cmake %%cmake%{?cmake_suffix}
%endif

Name:       cpp-hocon
Version:    0.2.1
Release:    3%{?dist}
Summary:    C++ support for the HOCON configuration file format

License:    ASL 2.0
URL:        https://github.com/puppetlabs/cpp-hocon
Source0:    %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:    cpphocon.pc.in
Patch0:     %{name}-missing-headers.patch

BuildRequires:  cmake%{?cmake_suffix} >= 3.2.2
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  boost%{?boost_suffix}-devel >= 1.54
BuildRequires:  leatherman-devel
BuildRequires:  gettext

%description
This is a port of the TypesafeConfig library to C++.

The library provides C++ support for the HOCON configuration file format.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary:    Development files for the cpp-hocon library

%description devel
Libraries and headers to links against cpp-hocon.

%prep
%autosetup -p1

%build
%cmake . -B%{_target_platform} \
  -DBOOST_INCLUDEDIR=%{_includedir}/boost%{?boost_suffix} \
  -DBOOST_LIBRARYDIR=%{_libdir}/boost%{?boost_suffix} \
  -DLeatherman_DIR=%{_libdir}/cmake%{?cmake_suffix}/leatherman \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  %{nil}
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}

# upstream doesn't provide a cmake or pkgconfig file so write one ourselves
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -p %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/cpphocon.pc
sed -i 's#@@PREFIX@@#%{_prefix}#' %{buildroot}%{_libdir}/pkgconfig/cpphocon.pc
sed -i 's#@@VERSION@@#%{version}#' %{buildroot}%{_libdir}/pkgconfig/cpphocon.pc
sed -i 's#@@LIBDIR@@#%{_lib}#' %{buildroot}%{_libdir}/pkgconfig/cpphocon.pc

%ldconfig_scriptlets

%files
%license LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/hocon/
%{_libdir}/pkgconfig/cpphocon.pc

%changelog
* Wed Jun 03 2020 Jonathan Wakely <jwakely@redhat.com> - 0.2.1-3
- Rebuild for Boost 1.73.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

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

