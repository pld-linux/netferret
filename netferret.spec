# (for rpm-2.3.9 and later)
# Predefined Macros:
# PACKAGE_VERSION
# PACKAGE_RELEASE
# 
# User-Defined Macros:
# %define <name> <expansion>
%define name                   netferret
%define version                0.1b2
%define release                1
%define prefix                 /usr

%define rpm_spec_dir           /usr/src/redhat/SPECS
%define missing_files_file     /tmp/files-missing-%{name}-%{version}-%{release}

Summary: GNOME toolbar app for querying web search engines.
Name: %{name}
Version: %{version}
Release: %{release}
Packager: Keith Amidon <camalot@picnicpark.org>
Copyright: GPL
Group: Applications/Internet
URL: http://www.pcc.net/alchemy/ferret/
Source0: http://www.pcc.net/alchemy/ferret/netferret-0.1b2.tar.gz
#Patch0:
Prefix: %{prefix}
BuildRoot: /tmp/%{name}-%{version}-root

%description
Net Ferret is a tool to help you get quicker results when searching
the internet.  It runs as an applet in the GNOME toolbar. Searching
is painful enough already without that pesky search engine front
page with seven hundred advertisements...


%prep
%setup
#%setup -n <non-standard-path>

# Create any necessary patches with diff -uNr <new-dist-dir> <old-dist-dir>
#%patch -P 1

%build

./configure --prefix="%{prefix}"
make

%install

function CheckSpecFiles() {
    # check all the files in the build-root against the files listed in
    # the spec file to ensure that files aren't missing. This isn't so
    # much needed for first-time builds as it is when you want to package
    # a new version of software you already have a spec file for without
    # having to think too much to make sure that new files haven't been
    # introduced, etc.
    #
    # The convention for this to work right is that the spec file name
    # is the software package name with .spec appended.
    #
    # Note: This is not foolproof. It is meant as a convenience. In
    # particular, files sent to /usr/doc from the source directory 
    # will obviously not be found. A good way around this is to manually
    # copy the files from the source to $RPM_BUILD_ROOT/usr/doc during
    # the install step. Then you will know that you at least got the
    # important ones... Plus, it also lets you setup your own subdirectories
    # in the doc directory.
    #
    # Note2: It also doesn't check for files in the files list that aren't
    # in the build directory... But then, rpm already does this for you!
    #
    echo "Checking spec file list of files against build root."
    olddir=`pwd`
    cd "${RPM_BUILD_ROOT}"
    missing_files="false"
    rm -f "%{missing_files_file}"
    for file in `find . -true ! -type d | cut -c2-`
    do
        if [ `grep -c $file "%{rpm_spec_dir}/%{name}.spec"` -eq 0 ]
        then
            missing_files="true"
            echo "$file" >>"%{missing_files_file}"
        fi
    done
    cd "$olddir"
    if [ $missing_files = "true" ]
    then
	cat << eof
----------------------------------------------------------------
FILES MISSING FROM SPEC FILE LISTED IN THE FILE:
%{missing_files_file}
----------------------------------------------------------------
eof
        cat "%{missing_files_file}"
        return -1
    else
        return 0
    fi
}

function CheckBuildRoot() {
    # do a few sanity checks on the BuildRoot
    # to make sure we don't damage a system
    case "${RPM_BUILD_ROOT}" in
        ''|' '|/|/bin|/boot|/dev|/etc|/home|/lib|/mnt|/root|/sbin|/tmp|/usr|/var)
            echo "Yikes!  Don't use '${RPM_BUILD_ROOT}' for a BuildRoot!"
            echo "The BuildRoot gets deleted when this package is rebuilt;"
            echo "something like '/tmp/build-blah' is a better choice."
            return 1
            ;;
        *)  return 0
            ;;
    esac
}
function CleanBuildRoot() {
    if CheckBuildRoot; then
        rm -rf "${RPM_BUILD_ROOT}"
    else
        exit 1
    fi
}
CleanBuildRoot

for i in \
    "/usr/bin" \
    "/usr/share/pixmaps" \
    "/usr/share/applets/Network" \
    "/etc/CORBA/servers" \
    "/usr/doc/%{name}-%{version}"
do
    mkdir -p "${RPM_BUILD_ROOT}${i}"
done

# Use the -n version to check that everything is properly going into
# the build root, then use the other to actually do the install
#make -n prefix="${RPM_BUILD_ROOT}%{prefix}" \
#        BINDIR="${RPM_BUILD_ROOT}/usr/bin" \
#        DESKTOPDIR="${RPM_BUILD_ROOT}/usr/share/applets/Network" \
#        CORBADIR="${RPM_BUILD_ROOT}/etc/CORBA/servers" \
#        PIXMAPDIR="${RPM_BUILD_ROOT}/usr/share/pixmaps" install; exit -1
make prefix="${RPM_BUILD_ROOT}%{prefix}" \
     BINDIR="${RPM_BUILD_ROOT}/usr/bin" \
     DESKTOPDIR="${RPM_BUILD_ROOT}/usr/share/applets/Network" \
     CORBADIR="${RPM_BUILD_ROOT}/etc/CORBA/servers" \
     PIXMAPDIR="${RPM_BUILD_ROOT}/usr/share/pixmaps" install

# Copy over any documentation you want to the build root
for i in \
    "AUTHORS" \
    "COPYING" \
    "ChangeLog" \
    "INSTALL" \
    "NEWS" \
    "README" \
    "TODO"

do
    install -o root -g root -m 444 "$i" "${RPM_BUILD_ROOT}/usr/doc/%{name}-%{version}/"
done

# The following should typically be the last line of the install section.
CheckSpecFiles

%clean
function CheckBuildRoot() {
    # do a few sanity checks on the BuildRoot
    # to make sure we don't damage a system
    case "${RPM_BUILD_ROOT}" in
        ''|' '|/|/bin|/boot|/dev|/etc|/home|/lib|/mnt|/root|/sbin|/tmp|/usr|/var)
            echo "Yikes!  Don't use '${RPM_BUILD_ROOT}' for a BuildRoot!"
            echo "The BuildRoot gets deleted when this package is rebuilt;"
            echo "something like '/tmp/build-blah' is a better choice."
            return 1
            ;;
        *)  return 0
            ;;
    esac
}
function CleanBuildRoot() {
    if CheckBuildRoot; then
        rm -rf "${RPM_BUILD_ROOT}"
    else
        exit 1
    fi
}
function CleanFilesMissing() {
    rm -f "%{missing_files_file}"
}

CleanBuildRoot
CleanFilesMissing

%files
/usr/bin/ferret_applet
/usr/share/pixmaps/ferret_logo.xpm
/usr/share/pixmaps/ferret_paw.xpm
/usr/share/applets/Network/ferret_applet.desktop
/etc/CORBA/servers/ferret_applet.gnorba
%doc /usr/doc/netferret-0.1b2/AUTHORS
%doc /usr/doc/netferret-0.1b2/COPYING
%doc /usr/doc/netferret-0.1b2/ChangeLog
%doc /usr/doc/netferret-0.1b2/INSTALL
%doc /usr/doc/netferret-0.1b2/NEWS
%doc /usr/doc/netferret-0.1b2/README
%doc /usr/doc/netferret-0.1b2/TODO
