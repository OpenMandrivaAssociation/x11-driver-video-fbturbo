%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir %{moduledir}/drivers
%define gitdate 20160730
%define gitrev .%{gitdate}

%undefine _hardened_build

Summary:   Xorg X11 fbturbo driver
Name:	   x11-driver-video-fbturbo
Version:   0.5.1
Release:   0.1%{?gitrev}
URL:       https://github.com/ssvb/xf86-video-fbturbo
License:   MIT and GPLv2
Group:     System/X11

Source0:    xf86-video-fbturbo-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh

BuildRequires:	pkgconfig(libdrm)
BuildRequires:	x11-proto-devel >= 1.0.0
BuildRequires:	x11-server-devel >= 1.0.1
BuildRequires:	x11-util-macros >= 1.0.1
Requires:	x11-server-common %(xserver-sdk-abi-requires videodrv)

%description 
Xorg DDX driver for ARM devices (Allwinner, RPi and others), it's
based on the fbdev driver so will work in all places it does
but has NEON optimised code paths to improve ARM

%if 0%{?gitdate}
%define dirsuffix %{gitdate}
%else
%define dirsuffix %{version}
%endif

%prep
%setup -q -n xf86-video-fbturbo-%{?gitdate:%{gitdate}}%{!?gitdate:%{dirsuffix}} 
touch AUTHORS

%build
%{?gitdate:autoreconf -v --install}

%configure --disable-static  --libdir=%{_libdir} --mandir=%{_mandir}
%make V=1

%install
make install DESTDIR=%{buildroot}

# Remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README
%{driverdir}/fbturbo_drv.so
%{_mandir}/man4/fbturbo.4*
