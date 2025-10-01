#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	doc	# HTML documentation (sphinx-based)

%define		module	pyOpenSSL
Summary:	Python 3 interface to the OpenSSL library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki OpenSSL
Name:		python3-%{module}
Version:	25.3.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pyopenssl/
Source0:	https://files.pythonhosted.org/packages/source/p/pyopenssl/pyopenssl-%{version}.tar.gz
# Source0-md5:	d755732945157fb8ca98c2d66a55755d
URL:		https://github.com/pyca/pyopenssl
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cryptography >= 41.0.5
BuildRequires:	python3-cryptography < 46
BuildRequires:	python3-pretend
BuildRequires:	python3-pytest >= 3.0.1
BuildRequires:	python3-pytest-rerunfailures
%if "%{py3_ver}" != "3.13"
BuildRequires:	python3-typing_extensions >= 4.9
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
High-level wrapper around a subset of the OpenSSL library, includes:
 - SSL.Connection objects, wrapping the methods of Python's portable
   sockets
 - Callbacks written in Python
 - Extensive error-handling mechanism, mirroring OpenSSL's error codes
...and much more.

This package contains Python 3 modules.

%description -l pl.UTF-8
Wysokopoziomowe obudowanie podzbioru biblioteki OpenSSL, zawierające:
 - obiekty SSL.Connection, obudowujący metody przenośnych gniazd
   Pythona
 - wywołania zwrotne napisane w Pythonie
 - obszerny mechanizm obsługi błędów odzwierciedlający kody błędów
   OpenSSL-a
...i wiele więcej.

Ten pakiet zawiera moduły Pythona 3.

%package apidocs
Summary:	API documentation for Python pyOpenSSL module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pyOpenSSL
Group:		Documentation

%description apidocs
API documentation for Python pyOpenSSL module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pyOpenSSL.

%prep
%setup -q -n pyopenssl-%{version}

%build
%py3_build

%if %{with tests}
# test_verify_with_time test fails with 32-bit time_t(?)
# the rest require localhost networking (not working with unshare --net)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_rerunfailures" \
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m pytest -v tests -k "\
not test_verify_with_time \
and not test_set_info_callback and not test_set_keylog_callback \
and not test_set_proto_version \
and not test_load_verify_bytes_cafile and not test_load_verify_unicode_cafile and not test_load_verify_directory_capath \
and not test_set_verify_callback_exception and not test_set_verify_callback_reference and not test_set_verify_default_callback \
and not test_add_extra_chain_cert and not test_use_certificate_chain_file_bytes and not test_use_certificate_chain_file_unicode \
and not TestConnection and not TestConnectionRecvInto and not TestConnectionSendAll \
and not test_socket_connect and not test_unexpected_EOF"
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/build-3/lib \
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%{py3_sitescriptdir}/OpenSSL
%{py3_sitescriptdir}/pyOpenSSL-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{*.html,_static,api}
%endif
