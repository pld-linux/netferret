Summary:	GNOME toolbar app for querying web search engines
Summary(pl):	Aplet GNOME do odpytywania wyszukiwarek sieciowych
Name:		netferret
Version:	0.1b2
Release:	6
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/netferret/%{name}-%{version}.tar.gz
# Source0-md5:	135058e9bed77fc93e89b39dc43fed54
Patch0:		%{name}-ac_am.patch
URL:		http://netferret.sourceforge.net/
BuildRequires:	ORBit-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gnome-core-devel >= 1.0
BuildRequires:	gtk+-devel >= 1.2.0
BuildRequires:	libghttp-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/X11/GNOME

%description
Net Ferret is a tool to help you get quicker results when searching
the Internet. It runs as an applet in the GNOME toolbar. Searching is
painful enough already without that pesky search engine front page
with seven hundred advertisements...

%description -l pl
Net Ferret to narzêdzie pomagaj±ce otrzymaæ szybciej rezultaty przy
przeszukiwaniu Internetu. Dzia³a jako aplet toolbaru GNOME. Szukanie
jest wystarczaj±co bolesne nawet bez tych wszystkich stron
pocz±tkowych wyszukiwarek z tysi±cami reklam...

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ferret_applet
%{_pixmapsdir}/ferret_logo.xpm
%{_pixmapsdir}/ferret_paw.xpm
%{_datadir}/applets/Network/ferret_applet.desktop
%{_sysconfdir}/CORBA/servers/*
