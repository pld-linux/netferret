Summary:	GNOME toolbar app for querying web search engines
Summary(pl):	Aplet GNOME do odpytywania wyszukiwarek sieciowych
Name:		netferret
Version:	0.1b2
Release:	5
License:	GPL
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	http://www.pcc.net/alchemy/ferret/%{name}-%{version}.tar.gz
Patch0:		%{name}-ac_am.patch
URL:		http://www.pcc.net/alchemy/ferret/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME

%description
Net Ferret is a tool to help you get quicker results when searching
the Internet. It runs as an applet in the GNOME toolbar. Searching is
painful enough already without that pesky search engine front page
with seven hundred advertisements...

%description -l pl
Net Ferret to narzêdzie pomagaj±ce otrzymaæ szybciej rezultaty przy
przeszukawaniu Internetu. Dzia³a jako aplet toolbaru GNOME. Szukanie
jest systarczaj±co bolesne nawet bez tych wszystkich stron
pocz±tkowych wyszukiwarek z tysi±cami reklam...

%prep
%setup -q
%patch -p1

%build
aclocal
autoconf
rm -f install-sh missing mkinstalldirs
automake -a -c 
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ferret_applet
%{_pixmapsdir}/ferret_logo.xpm
%{_pixmapsdir}/ferret_paw.xpm
%{_datadir}/applets/Network/ferret_applet.desktop
%{_sysconfdir}/CORBA/servers/*
