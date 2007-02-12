Summary:	Support for Annodex.net media as CGI handler
Summary(pl.UTF-8):   Obsługa mediów Annodex.net jako skrypt obsługujący CGI
Name:		phpannodex-cgi
Version:	0.4
Release:	1
License:	BSD
Group:		Applications/Networking
Source0:	http://www.annodex.net/software/phpannodex/download/%{name}-%{version}.tar.gz
# Source0-md5:	cfd4844e32331e02a0b9522e66d45134
URL:		http://www.annodex.net/software/phpannodex/index.html
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	php-annodex >= 0.4
Requires:	php-cgi >= 3:5.0.0
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{name}

%description
phpannodex-cgi is a CGI handler for type application/x-annodex. It
provides the following features:
 - dynamic generation of Annodex media from CMML files.
 - handling of timed query offsets, such as
        http://media.example.com/fish.anx?t=npt:01:20.8
   or
        http://media.example.com/fish.anx?id=Preparation
 - dynamic retrieval of CMML summaries, if the Accept: header prefers
   type text/x-cmml over application/x-annodex.


%description -l pl.UTF-8
phpannodex-cgi to skrypt CGI obsługujący typ application/x-annodex. Ma
następujące możliwości:
 - dynamiczne generowanie mediów Annodex z plików CMML
 - obsługę czasowych offsetów zapytań, takich jak
        http://media.example.com/fish.anx?t=npt:01:20.8
   albo
        http://media.example.com/fish.anx?id=Preparation
 - dynamiczne odtwarzanie podsumowań CMML, jeśli nagłówek Accept:
   preferuje typ text/x-cmml ponad application/x-annodex

%prep
%setup -q

sed -i -e 's,/usr/bin/env php,/usr/bin/php.cgi,' phpannodex.cgi

cat >> phpannodex-cgi.conf <<EOF
ScriptAlias /cgi-bin/phpannodex.cgi %{_appdir}/phpannodex.cgi
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

install phpannodex-cgi.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install phpannodex-cgi.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install phpannodex.cgi $RPM_BUILD_ROOT%{_appdir}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc LICENCE README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%dir %{_appdir}
%attr(755,root,root) %{_appdir}/phpannodex.cgi
