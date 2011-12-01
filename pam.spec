%define libname %mklibname %name 0
%define develname %mklibname %name -d

%define with_prelude 0
%{?_without_prelude: %{expand: %%global with_prelude 0}}
%{?_with_prelude: %{expand: %%global with_prelude 1}}

%define pam_redhat_version 0.99.10-1

Summary:	A security tool which provides authentication for applications
Name:		pam
Version:	1.1.4
Release:	2
# The library is BSD licensed with option to relicense as GPLv2+ - this option is redundant
# as the BSD license allows that anyway. pam_timestamp and pam_console modules are GPLv2+,
License:	BSD and GPLv2+
Group:		System/Libraries
Source0:	ftp://ftp.kernel.org/pub/linux/libs/pam/library/Linux-PAM-%{version}.tar.bz2
Source1:	ftp://ftp.kernel.org/pub/linux/libs/pam/library/Linux-PAM-%{version}.tar.bz2.sign
Source2:	pam-redhat-%{pam_redhat_version}.tar.bz2
Source3:	pam-0.99.3.0-README.update
Source4:	pam-0.99.8.1-11mdv2009.0-README.update
Source5:	other.pamd
Source6:	system-auth.pamd
Source7:	config-util.pamd
Source8:	dlopen.sh
Source9:	system-auth.5
Source10:	config-util.5

# RedHat patches
Patch1:  pam-1.0.90-redhat-modules.patch
Patch2:  pam-1.0.91-std-noclose.patch
Patch4:  pam-1.1.0-console-nochmod.patch
Patch5:  pam-1.1.0-notally.patch
Patch7:  pam-1.1.0-console-fixes.patch
Patch9:  pam-1.1.2-noflex.patch
Patch10: pam-1.1.3-nouserenv.patch
Patch11: pam-1.1.3-console-abstract.patch

# Mandriva specific sources/patches
# (fl) fix infinite loop
Patch507:	pam-0.74-loop.patch
# (fc) 0.75-29mdk don't complain when / is owned by root.adm
Patch508:	Linux-PAM-0.99.3.0-pamtimestampadm.patch
# (fl) pam_xauth: set extra groups because in high security levels
#      access to /usr/X11R6/bin dir is controlled by a group
Patch512:	Linux-PAM-1.1.1-xauth-groups.patch
# (tv/blino) add defaults for nice/rtprio in /etc/security/limits.conf
Patch517:	Linux-PAM-0.99.3.0-enable_rt.patch
# (blino) fix parallel build (pam_console)
Patch521:	Linux-PAM-0.99.3.0-pbuild-rh.patch

Patch700:	pam_fix_static_pam_console.patch
# (fc) do not output error when no file is in /etc/security/console.perms.d/
Patch701:	pam-1.1.0-console-nopermsd.patch
# (proyvind): add missing constant that went with rpc removal from glibc 2.14
Patch702:	Linux-PAM-1.1.4-add-now-missing-nis-constant.patch

#add missing documentation
Source501: 	pam_tty_audit.8
Source502:	README
Requires:	cracklib-dicts
Requires:	setup >= 2.7.12-2
Requires:	pam_tcb >= 1.0.2-16
Conflicts:	initscripts < 3.94
Requires(pre):	rpm-helper
Requires(post):	coreutils
Requires(post):	tcb >= 1.0.2-16
BuildRequires:	bison cracklib-devel flex
BuildRequires:	linuxdoc-tools
BuildRequires:	db_nss-devel >= 4.6
BuildRequires:	openssl-devel
BuildRequires:	libaudit-devel
BuildRequires:	glibc-crypt_blowfish-devel
%if %with_prelude
BuildRequires:	prelude-devel >= 0.9.0
%else
BuildConflicts:	prelude-devel
%endif
Obsoletes:	pamconfig
Provides:	pamconfig
Url:		http://www.kernel.org/pub/linux/libs/pam/index.html

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
Conflicts:	%{name} < 0.99.8.1-10mdv
Conflicts:	pam_tcb < 1.0.2-16

%description -n	%{libname}
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the librairies for %{name}

%package -n	%{develname}
Summary:	Development headers and libraries for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{name}-devel <= 0.77-9mdk
Obsoletes:	%{mklibname %name 0 -d} <= 0.99.8.1

%description -n	%{develname}
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the development librairies for %{name}

%prep
%setup -q -n Linux-PAM-%{version} -a 2

# Add custom modules.
mv pam-redhat-%{pam_redhat_version}/* modules

# (RH)
%patch1 -p1 -b .redhat-modules
%patch2 -p1 -b .std-noclose
%patch4 -p1 -b .nochmod
%patch5 -p1 -b .notally
%patch7 -p1 -b .console-fixes
%patch9 -p1 -b .noflex
%patch10 -p1 -b .nouserenv
%patch11 -p1 -b .abstract

# (Mandriva)
%patch507 -p1 -b .loop
%patch508 -p1 -b .pamtimestampadm
%patch512 -p0 -b .xauth-groups
%patch517 -p1 -b .enable_rt
%patch521 -p1 -b .pbuild-rh
%patch700 -p1 -b .static
%patch701 -p1 -b .nopermsd
%patch702 -p1 -b .nis_const~

# 08/08/2008 - vdanen - make pam provide pam_unix until we can work out all the issues in pam_tcb; this
# just makes things easier but is not meant to be a permanent solution
## Remove unwanted modules; pam_tcb provides pam_unix now
#for d in pam_unix; do
#    rm -rf modules/$d
#    sed -i "s,modules/$d/Makefile,," configure.in
#    sed -i "s/ $d / /" modules/Makefile.am
#done


install -m644 %{SOURCE501} %{SOURCE502} modules/pam_tty_audit/

mkdir -p doc/txts
for readme in modules/pam_*/README ; do
	cp -f ${readme} doc/txts/README.`dirname ${readme} | sed -e 's|^modules/||'`
done

cp %{SOURCE4} README.0.99.8.1.update.urpmi

#libtoolize -cf
autoreconf -I m4

%build
export BROWSER=""
CFLAGS="$RPM_OPT_FLAGS -fPIC -I%{_includedir}/db_nss -D_GNU_SOURCE" \
%configure2_5x \
	--sbindir=/sbin \
	--libdir=/%{_lib} \
	--includedir=%{_includedir}/security \
	--with-db-uniquename=_nss \
	--docdir=%{_docdir}/%{name} \
	--disable-selinux
%make

%install
mkdir -p %{buildroot}%{_includedir}/security
mkdir -p %{buildroot}/%{_lib}/security
make install DESTDIR=%{buildroot} LDCONFIG=:
install -d -m 755 %{buildroot}/etc/pam.d
install -m 644 %{SOURCE5} %{buildroot}/etc/pam.d/other
install -m 644 %{SOURCE6} %{buildroot}/etc/pam.d/system-auth
install -m 644 %{SOURCE7} %{buildroot}/etc/pam.d/config-util
install -m 600 /dev/null %{buildroot}%{_sysconfdir}/security/opasswd
install -d -m 755 %{buildroot}/var/log
install -m 600 /dev/null %{buildroot}/var/log/tallylog

# Install man pages.
install -m 644 %{SOURCE9} %{SOURCE10} %{buildroot}%{_mandir}/man5/

# remove unpackaged .la files
rm -rf %{buildroot}/%{_lib}/*.la %{buildroot}/%{_lib}/security/*.la

# no longer needed, handled by ACL in udev
for phase in auth acct passwd session ; do	 
	ln -sf pam_unix.so %{buildroot}/%{_lib}/security/pam_unix_${phase}.so	 
done

%find_lang Linux-PAM

%check
# (blino) we don't want to test if SE Linux is built, it's disabled
# Make sure every module subdirectory gave us a module.  Yes, this is hackish.
for dir in modules/pam_* ; do
if [ -d ${dir} ] && [ ${dir} != "modules/pam_selinux" && [ ${dir} != "modules/pam_sepermit"  ]; then
         [ ${dir} = "modules/pam_tally" ] && continue
	if ! ls -1 %{buildroot}/%{_lib}/security/`basename ${dir}`*.so ; then
		echo ERROR `basename ${dir}` did not build a module.
		exit 1
	fi
fi
done

# Check for module problems.  Specifically, check that every module we just
# installed can actually be loaded by a minimal PAM-aware application.
/sbin/ldconfig -n %{buildroot}/%{_lib}
for module in %{buildroot}/%{_lib}/security/pam*.so ; do
	if ! env LD_LIBRARY_PATH=%{buildroot}/%{_lib} \
		 %{SOURCE8} -ldl -lpam -L%{buildroot}/%{_lib} ${module} ; then
		echo ERROR module: ${module} cannot be loaded.
		exit 1
	fi
done

%posttrans
if [ ! -a /var/log/tallylog ] ; then
       install -m 600 /dev/null /var/log/tallylog
fi
if [ -f /etc/login.defs -a ! "$(grep -q USE_TCB /etc/login.defs)" ]; then
       /usr/sbin/set_tcb --auto --migrate
fi


%files -f Linux-PAM.lang
%doc NEWS README.0.99.8.1.update.urpmi
%docdir %{_docdir}/%{name}
%dir /etc/pam.d
%config(noreplace) /etc/environment
%config(noreplace) /etc/pam.d/other
%attr(0644,root,shadow) %config(noreplace) /etc/pam.d/system-auth
%config(noreplace) /etc/pam.d/config-util
/sbin/mkhomedir_helper
/sbin/pam_console_apply
/sbin/pam_tally2
/sbin/unix_chkpwd
/sbin/unix_update
%attr(4755,root,root) /sbin/pam_timestamp_check
%config(noreplace) %{_sysconfdir}/security/access.conf
%config(noreplace) %{_sysconfdir}/security/chroot.conf
%config(noreplace) %{_sysconfdir}/security/console.perms
%config(noreplace) %{_sysconfdir}/security/console.handlers
%config(noreplace) %{_sysconfdir}/security/group.conf
%config(noreplace) %{_sysconfdir}/security/limits.conf
%config(noreplace) %{_sysconfdir}/security/namespace.conf
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/security/namespace.init
%config(noreplace) %{_sysconfdir}/security/pam_env.conf
%config(noreplace) %{_sysconfdir}/security/time.conf
%config(noreplace) %{_sysconfdir}/security/opasswd
%dir %{_sysconfdir}/security/console.apps
%dir %{_sysconfdir}/security/console.perms.d
%dir /var/run/console
%ghost %verify(not md5 size mtime) /var/log/tallylog
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
/%{_lib}/libpam.so.*
/%{_lib}/libpamc.so.*
/%{_lib}/libpam_misc.so.*
/%{_lib}/security/*.so
/%{_lib}/security/pam_filter
%dir /%{_lib}/security

%files -n %{develname}
%doc Copyright
/%{_lib}/libpam.so
/%{_lib}/libpam_misc.so
/%{_lib}/libpamc.so
%{_includedir}/security/*.h
%{_mandir}/man3/*

%files doc
%doc doc/txts doc/specs/rfc86.0.txt Copyright



