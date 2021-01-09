%if 0%{?rhel} && 0%{?rhel} <= 7
%global boost_suffix 169
%global cmake_suffix 3
%global cmake %%cmake%{?cmake_suffix}
%global cmake_build %%cmake%{?cmake_suffix}_build
%global cmake_install %%cmake%{?cmake_suffix}_install
%global ctest %%ctest%{?cmake_suffix}
%endif

%global min_boost 1.54
%global min_cmake 3.2.2

# Makes sure an SONAME bump does not catch us by surprise. Currently, there is
# no ABI stability even across patch releases, and the SONAME comes from the
# complete version number.
%global so_version 0.2.2

Name:           cpp-hocon
Version:        0.2.2
Release:        1%{?dist}
Summary:        C++ support for the HOCON configuration file format

License:        ASL 2.0
URL:            https://github.com/puppetlabs/%{name}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
# https://github.com/puppetlabs/cpp-hocon/pull/124
Patch0:         %{name}-missing-headers.patch

BuildRequires:  cmake%{?cmake_suffix} >= %{min_cmake}
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  boost%{?boost_suffix}-devel >= %{min_boost}
BuildRequires:  leatherman-devel
BuildRequires:  gettext

BuildRequires:  doxygen

# See facter, which has the same workaround.
# autoreq is not picking this one up so be specific
Requires:       leatherman%{?_isa}

%description
This is a port of the TypesafeConfig library to C++.

The library provides C++ support for the HOCON configuration file format.


%package devel
Summary:        Development files for the %{name} library
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       boost%{?boost_suffix}-devel%{?_isa} >= %{min_boost}
Requires:       leatherman-devel%{?_isa}

%description devel
Libraries and headers to link against %{name}.


%package doc
Summary:    Documentation for the %{name} library

%description doc
Documentation for the %{name} library.


%prep
%autosetup -p1


%build
%cmake \
  -DBOOST_INCLUDEDIR=%{_includedir}/boost%{?boost_suffix} \
  -DBOOST_LIBRARYDIR=%{_libdir}/boost%{?boost_suffix} \
  -DLeatherman_DIR=%{_libdir}/cmake%{?cmake_suffix}/leatherman \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  %{nil}
%cmake_build

pushd lib
doxygen Doxyfile
popd


%install
%cmake_install


%check
%ctest


# Required for EL7 only:
%ldconfig_scriptlets


%files
%license LICENSE
%{_libdir}/lib%{name}.so.%{so_version}


%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/hocon/


%files doc
%license LICENSE
%doc CONTRIBUTING.md
%doc README.md
%doc lib/html


%changelog
* Sat Jan  9 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.2-1
- Update to 0.2.2 (SONAME bump)
- Drop patch for upstream commit caab275509826dc5fe5ab2632582abb8f83ea2b3, now
  released

* Sat Jan  9 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.1-7
- Drop downstream pkg-config support (no .pc file)

* Fri Jan  8 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.1-6
- Use %%{name} macro in several places
- Use %%cmake_* macros consistently
- Add a %%check section to run the tests
- Build HTML documentation with Doxygen, and add a new -doc subpackage
- Add top-level documentation files (README.md etc.)
- Try to add necessary libs to the .pc file, and remove unnecessary -I

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Jonathan Wakely <jwakely@redhat.com> - 0.2.1-4
- Rebuilt for leatherman-1.12.0
- Link tests to libboost_filesystem

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

