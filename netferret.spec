Summary:	GNOME toolbar app for querying web search engines.
Name:		netferret
Version:	0.1b2
Release:	3
License:	GPL
Group:		X11/Applications/Networking
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	http://www.pcc.net/alchemy/ferret/%{name}-%{version}.tar.gz
Patch0:		netferret-ac_am.patch
URL:		http://www.pcc.net/alchemy/ferret/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11/GNOME

%description
Net Ferret is a tool to help you get quicker results when searching
the internet. It runs as an applet in the GNOME toolbar. Searching is
painful enough already without that pesky search engine front page
with seven hundred advertisements...

%prep
%setup -q
%patch -p1

%build
aclocal
autoconf
rm -f install-sh missing mkinstalldirs
automake --copy --add-missing
LDFLAGS="-s"; export LDFLAGS
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ferret_applet
%{_datadir}/pixmaps/ferret_logo.xpm
%{_datadir}/pixmaps/ferret_paw.xpm
%{_datadir}/applets/Network/ferret_applet.desktop
%{_sysconfdir}/CORBA/servers/*
