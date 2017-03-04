#
# Conditional build:
%bcond_with	tests	# test target [no tests are run with python2, some tests are not ready for python3???]
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	doc	# HTML documentation (sphinx-based)

%define		module	pyOpenSSL
Summary:	Python 2 interface to the OpenSSL library
Summary(pl.UTF-8):	Interfejs Pythona 2 do biblioteki OpenSSL
Name:		python-%{module}
Version:	16.2.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/pyopenssl/
Source0:	https://files.pythonhosted.org/packages/source/p/pyOpenSSL/%{module}-%{version}.tar.gz
# Source0-md5:	6635503758c65ea6f70d18d1b18e46d5
URL:		https://github.com/pyca/pyopenssl
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-cryptography >= 1.3.4
BuildRequires:	python-six >= 1.5.2
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cryptography >= 1.3.4
BuildRequires:	python3-six >= 1.5.2
%endif
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg
%endif
Requires:	python-cryptography >= 1.3.4
Requires:	python-six >= 1.5.2
Obsoletes:	python-OpenSSL
Obsoletes:	python-pyOpenSSL-doc
Obsoletes:	python-pyOpenSSL-doc-html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
High-level wrapper around a subset of the OpenSSL library, includes:
 - SSL.Connection objects, wrapping the methods of Python's portable
   sockets
 - Callbacks written in Python
 - Extensive error-handling mechanism, mirroring OpenSSL's error codes
...and much more.

This package contains Python 2 modules.

%description -l pl.UTF-8
Wysokopoziomowe obudowanie podzbioru biblioteki OpenSSL, zawierające:
 - obiekty SSL.Connection, obudowujący metody przenośnych gniazd
   Pythona
 - wywołania zwrotne napisane w Pythonie
 - obszerny mechanizm obsługi błędów odzwierciedlający kody błędów
   OpenSSL-a
...i wiele więcej.

Ten pakiet zawiera moduły Pythona 2.

%package -n python3-pyOpenSSL
Summary:	Python 2 interface to the OpenSSL library
Summary(pl.UTF-8):	Interfejs Pythona 2 do biblioteki OpenSSL
Group:		Libraries/Python
Requires:	python3-cryptography >= 1.3.4
Requires:	python3-six >= 1.5.2

%description -n python3-pyOpenSSL
High-level wrapper around a subset of the OpenSSL library, includes:
 - SSL.Connection objects, wrapping the methods of Python's portable
   sockets
 - Callbacks written in Python
 - Extensive error-handling mechanism, mirroring OpenSSL's error codes
...and much more.

This package contains Python 3 modules.

%description -n python3-pyOpenSSL -l pl.UTF-8
Wysokopoziomowe obudowanie podzbioru biblioteki OpenSSL, zawierające:
 - obiekty SSL.Connection, obudowujący metody przenośnych gniazd
   Pythona
 - wywołania zwrotne napisane w Pythonie
 - obszerny mechanizm obsługi błędów odzwierciedlający kody błędów
   OpenSSL-a
...i wiele więcej.

Ten pakiet zawiera moduły Pythona 3.

%package examples
Summary:	Examples for pyOpenSSL module
Summary(pl.UTF-8):	Przykłady do modułu pyOpenSSL
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description examples
This package contains example files for pyOpenSSL Python module.

%description examples -l pl.UTF-8
Pakiet zawierający przykładowe skrypty dla modułu Pythona pyOpenSSL.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
LC_ALL=C.UTF-8 \
%py_build %{?with_tests:test}
%endif
%if %{with python3}
LC_ALL=C.UTF-8 \
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
%{__make} -C doc html
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%dir %{py_sitescriptdir}/OpenSSL
%{py_sitescriptdir}/OpenSSL/*.py[co]
%{py_sitescriptdir}/pyOpenSSL-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-pyOpenSSL
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%dir %{py3_sitescriptdir}/OpenSSL
%{py3_sitescriptdir}/OpenSSL/*.py
%{py3_sitescriptdir}/OpenSSL/__pycache__
%{py3_sitescriptdir}/pyOpenSSL-%{version}-py*.egg-info
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/{*.html,_static,api}
%endif
