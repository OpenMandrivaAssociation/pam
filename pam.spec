%define pam_redhat_version 0.99.7-1

%define libname %mklibname %name 0

%define with_prelude 0
%{?_without_prelude: %{expand: %%global with_prelude 0}}
%{?_with_prelude: %{expand: %%global with_prelude 1}}

Summary:	A security tool which provides authentication for applications
Name:		pam
Version:	0.99.8.1
Release:	%mkrel 1
License:	GPL or BSD
Group:		System/Libraries
Source0:	ftp://ftp.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-%{version}.tar.bz2
Source2:	pam-redhat-%{pam_redhat_version}.tar.bz2
Source4:	pam-0.99.3.0-README.update
Source5:	other.pamd
Source6:	system-auth.pamd
Source7:	config-util.pamd
Source9:	system-auth.5
Source10:	config-util.5

# RedHat patches
Patch01:	pam-0.99.7.0-redhat-modules.patch
Patch24:	pam-0.99.8.1-unix-update-helper.patch
Patch25:	pam-0.99.7.1-unix-hpux-aging.patch
Patch31:	pam-0.99.3.0-cracklib-try-first-pass.patch
Patch32:	pam-0.99.3.0-tally-fail-close.patch
Patch40:	pam-0.99.7.1-namespace-temp-logon.patch

# Mandriva specific sources/patches

# (blino) default permission set in Mandriva
#         use /etc/security/console.perms.d/50-mandriva.perms whenever possible
Source500:	pam-mandriva.perms
#         else patch 50-default.perms
Patch500:	Linux-PAM-0.99.6.0-mdvperms.patch

# (fl) fix infinite loop
Patch501:	pam-0.74-loop.patch
# (fc) 0.75-29mdk don't complain when / is owned by root.adm
Patch508:	Linux-PAM-0.99.3.0-pamtimestampadm.patch
Patch511:	Linux-PAM-0.99.3.0-verbose-limits.patch
# (fl) pam_xauth: set extra groups because in high security levels
#      access to /usr/X11R6/bin dir is controlled by a group
Patch512:	Linux-PAM-0.99.3.0-xauth-groups.patch
# (tv/blino) add defaults for nice/rtprio in /etc/security/limits.conf
Patch517:	Linux-PAM-0.99.3.0-enable_rt.patch
# (blino) fix parallel build (pam_console)
Patch521:	Linux-PAM-0.99.3.0-pbuild-rh.patch

Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	cracklib-dicts
Conflicts:	initscripts < 3.94
Requires(pre):	rpm-helper
BuildRequires:	bison cracklib-devel flex
BuildRequires:	linuxdoc-tools db4.2-devel automake1.8
BuildRequires:	openssl-devel
# (blino) we don't want SE Linux, so conflicts since there is no configure switch
BuildConflicts:	libselinux-devel
%if %with_prelude
BuildRequires:	prelude-devel
%else
BuildConflicts:	prelude-devel
%endif

Obsoletes:	pamconfig
Provides:	pamconfig
Url:		http://www.us.kernel.org/pub/linux/libs/pam/index.html

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

%package	doc
Summary:	Additional documentation for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}

%description	doc
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This is the documentation package of %{name}

%package -n	%{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Conflicts:	%{name} < 0.77-10mdk

%description -n	%{libname}
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the librairies for %{name}

%package -n	%{libname}-devel
Summary:	Development headers and libraries for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel <= 0.77-9mdk

%description -n	%{libname}-devel
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the development librairies for %{name}

%prep
%setup -q -n Linux-PAM-%{version} -a 2

# (RH)
%patch01 -p1 -b .redhat-modules
%patch24 -p1 -b .update-helper
%patch25 -p1 -b .unix-hpux-aging
%patch31 -p1 -b .try-first-pass
%patch32 -p1 -b .fail-close
%patch40 -p1 -b .temp-logon

# (Mandriva)
%patch500 -p1 -b .mdvperms
%patch501 -p1 -b .loop
%patch508 -p1 -b .pamtimestampadm
%patch511 -p1 -b .verbose-limits
%patch512 -p1 -b .xauth-groups
%patch517 -p1 -b .enable_rt
%patch521 -p1 -b .pbuild-rh

mkdir -p doc/txts
for readme in modules/pam_*/README ; do
	cp -f ${readme} doc/txts/README.`dirname ${readme} | sed -e 's|^modules/||'`
done

cp %{SOURCE4} README.update.urpmi

autoreconf

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC -I%{_includedir}/db4" \
%configure \
	--sbindir=/sbin \
	--libdir=/%{_lib} \
	--includedir=%{_includedir}/security \
	--docdir=%{_docdir}/%{name}
%make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_includedir}/security
mkdir -p $RPM_BUILD_ROOT/%{_lib}/security
make install DESTDIR=$RPM_BUILD_ROOT LDCONFIG=:
install -d -m 755 $RPM_BUILD_ROOT/etc/pam.d
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT/etc/pam.d/other
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/system-auth
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/pam.d/config-util

# Install man pages.
install -m 644 %{SOURCE9} %{SOURCE10} $RPM_BUILD_ROOT%{_mandir}/man5/

# (blino) we don't want to test if SE Linux is built, it's disabled
# Make sure every module subdirectory gave us a module.  Yes, this is hackish.
for dir in modules/pam_* ; do
if [ -d ${dir} ] && [ ${dir} != "modules/pam_selinux" ]; then
	if ! ls -1 $RPM_BUILD_ROOT/%{_lib}/security/`basename ${dir}`*.so ; then
		echo ERROR `basename ${dir}` did not build a module.
		exit 1
	fi
fi
done

install -m 644 %{SOURCE500} $RPM_BUILD_ROOT/etc/security/console.perms.d/50-mandriva.perms

# remove unpackaged .la files
rm -rf $RPM_BUILD_ROOT/%{_lib}/*.la $RPM_BUILD_ROOT/%{_lib}/security/*.la

touch $RPM_BUILD_ROOT%{_sysconfdir}/environment

%find_lang Linux-PAM

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -f Linux-PAM.lang
%defattr(-,root,root)
%doc NEWS README.update.urpmi
%docdir %{_docdir}/%{name}
%dir /etc/pam.d
%config(noreplace) /etc/environment
%config(noreplace) /etc/pam.d/config-util
%config(noreplace) /etc/pam.d/other
%config(noreplace) /etc/pam.d/system-auth
%config(noreplace) /etc/security/access.conf
%config(noreplace) /etc/security/chroot.conf
%config(noreplace) /etc/security/time.conf
%config(noreplace) /etc/security/group.conf
%config(noreplace) /etc/security/limits.conf
%config(noreplace) %{_sysconfdir}/security/namespace.conf
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/security/namespace.init
%config(noreplace) /etc/security/pam_env.conf
%config(noreplace) /etc/security/console.perms
%config(noreplace) /etc/security/console.handlers
%dir %{_sysconfdir}/security/console.perms.d
%config(noreplace) /etc/security/console.perms.d/50-default.perms
%config(noreplace) /etc/security/console.perms.d/50-mandriva.perms
/sbin/pam_console_apply
/sbin/pam_tally
/sbin/pam_tally2
%attr(4755,root,root) /sbin/pam_timestamp_check
%attr(4755,root,root) /sbin/unix_chkpwd
%attr(0700,root,root) /sbin/unix_update
%dir /etc/security/console.apps
%dir /var/run/console
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
/%{_lib}/libpam.so.*
/%{_lib}/libpamc.so.*
/%{_lib}/libpam_misc.so.*
/%{_lib}/security/*.so
/%{_lib}/security/pam_filter
%dir /%{_lib}/security

%files -n %{libname}-devel
%defattr(-,root,root)
%doc Copyright
/%{_lib}/libpam.so
/%{_lib}/libpam_misc.so
/%{_lib}/libpamc.so
%{_includedir}/security/*.h
%{_mandir}/man3/*

%files doc
%defattr(-,root,root)
%doc doc/txts doc/specs/rfc86.0.txt Copyright



