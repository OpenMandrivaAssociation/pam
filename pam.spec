%define major 0
%define libname %mklibname %{name} %{major}
%define libnamec %mklibname %{name}c %{major}
%define libname_misc %mklibname %{name}_misc %{major}
%define devname %mklibname %{name} -d
%global optflags %{optflags} -Oz

%bcond_with prelude
%bcond_with bootstrap

%define pam_redhat_version 1.1.4

Summary:	A security tool which provides authentication for applications
Name:		pam
Epoch:		1
Version:	1.5.1
Release:	2
# The library is BSD licensed with option to relicense as GPLv2+ - this option is redundant
# as the BSD license allows that anyway. pam_timestamp and pam_console modules are GPLv2+,
License:	BSD and GPLv2+
Group:		System/Libraries
Url:		http://linux-pam.org/
Source0:	http://www.linux-pam.org/library/Linux-PAM-%{version}.tar.xz
Source2:	https://releases.pagure.org/pam-redhat/pam-redhat-%{pam_redhat_version}.tar.bz2

Source5:	other.pamd
Source6:	system-auth.pamd
Source8:	fingerprint-auth.pamd
Source9:	smartcard-auth.pamd
Source10:	config-util.pamd
Source11:	dlopen.sh
Source12:	system-auth.5
Source13:	config-util.5
Source15:	pam-tmpfiles.conf
Source16:	postlogin.pamd
Source17:	postlogin.5

# RedHat patches
Patch1:		https://src.fedoraproject.org/rpms/pam/raw/master/f/pam-1.5.0-redhat-modules.patch
Patch2:		https://src.fedoraproject.org/rpms/pam/raw/master/f/pam-1.5.0-noflex.patch
Patch3:		https://src.fedoraproject.org/rpms/pam/raw/master/f/pam-1.3.0-unix-nomsg.patch
Patch22:	http://svnweb.mageia.org/packages/cauldron/pam/current/SOURCES/pam-1.1.7-unix-build.patch

# OpenMandriva specific sources/patches
# (fl) fix infinite loop
Patch507:	pam-0.74-loop.patch
# (fc) 0.75-29mdk don't complain when / is owned by root.adm
Patch508:	Linux-PAM-0.99.3.0-pamtimestampadm.patch
Patch509:	Linux-PAM-0.99.3.0-pbuild-rh.patch
# (fl) pam_xauth: set extra groups because in high security levels
#      access to /usr/X11R6/bin dir is controlled by a group
Patch512:	Linux-PAM-1.1.1-xauth-groups.patch

Patch700:	pam_fix_static_pam_console.patch
# (proyvind): add missing constant that went with rpc removal from glibc 2.14
Patch702:	Linux-PAM-1.1.4-add-now-missing-nis-constant.patch
# (akdengi> add user to default group users which need for Samba
Patch801:	Linux-PAM-1.1.4-group_add_users.patch

BuildRequires:	bison
BuildRequires:	flex
%if !%{with bootstrap}
# this pulls in the mega texlive load
BuildRequires:	linuxdoc-tools
%endif
BuildRequires:	db-devel >= 18.1
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(libxcrypt)
BuildRequires:	glibc-devel
BuildRequires:	pkgconfig(libtirpc)
BuildRequires:	pkgconfig(libnsl)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	xauth
# For _tmpfilesdir macro
BuildRequires:	systemd-macros
%if %{with prelude}
BuildRequires:	pkgconfig(libprelude)
%else
BuildConflicts:	pkgconfig(libprelude)
%endif
# Following deps are necessary only to build the pam library documentation.
BuildRequires:	xsltproc
BuildRequires:	html2text
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtds

Requires:	setup >= 2.7.12-2
Requires:	filesystem
Conflicts:	%{_lib}pam0 < 1.1.4-5
%rename %{name}-cracklib

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

%package doc
Summary:	Additional documentation for %{name}
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description doc
This is the documentation package of %{name}.

%package -n %{libname}
Summary:	Library for %{name}
Group:		System/Libraries
Conflicts:	pam < 1.1.4-5

%description -n %{libname}
This package contains the library libpam for %{name}.

%package -n %{libnamec}
Summary:	Library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}pam0 < 1.1.4-5

%description -n %{libnamec}
This package contains the library libpamc for %{name}.

%package -n %{libname_misc}
Summary:	Library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}pam0 < 1.1.4-5

%description -n %{libname_misc}
This package contains the library libpam_misc for %{name}.

%package -n %{devname}
Summary:	Development headers and libraries for %{name}
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Requires:	%{libnamec} = %{EVRD}
Requires:	%{libname_misc} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the development libraries for %{name}.

%prep
%setup -q -n Linux-PAM-%{version} -a 2

# Add custom modules.
mv pam-redhat-%{pam_redhat_version}/* modules

%autopatch -p1

mkdir -p doc/txts
for readme in modules/pam_*/README ; do
    cp -f ${readme} doc/txts/README.$(dirname ${readme} | sed -e 's|^modules/||')
done

touch ChangeLog # to make autoreconf happy
# (tpg) adjust service dir
sed -i -e 's#servicedir = $(prefix)/lib/systemd/system#servicedir = %{_unitdir}#g' modules/pam_namespace/Makefile.*

autoreconf -fi -I m4

%build
export BROWSER=""
%configure \
	--sbindir=/sbin \
	--libdir=/%{_lib} \
	--includedir=%{_includedir}/security \
	--enable-vendordir=%{_datadir} \
	--docdir=%{_docdir}/%{name} \
	--enable-docu \
	--enable-regenerate-docu \
	--disable-selinux \
	--disable-audit

%make_build

%install
mkdir -p %{buildroot}%{_includedir}/security
mkdir -p %{buildroot}/%{_lib}/security
%make_install LDCONFIG=:
install -d -m 755 %{buildroot}%{_datadir}/pam.d
install -d -m 755 %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/pam.d/other
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/pam.d/system-auth
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/fingerprint-auth
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/pam.d/smartcard-auth
install -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/pam.d/config-util
install -m 644 %{SOURCE16} %{buildroot}%{_sysconfdir}/pam.d/postlogin
install -m 600 /dev/null %{buildroot}%{_sysconfdir}/security/opasswd
install -d -m 755 %{buildroot}/var/log
install -d -m 755 %{buildroot}/var/run/faillock
install -d -m 755 %{buildroot}%{_sysconfdir}/motd.d
install -d -m 755 %{buildroot}/usr/lib/motd.d
install -d -m 755 %{buildroot}/run/motd.d
install -D -p -m 644 %{SOURCE15} %{buildroot}%{_tmpfilesdir}/%{name}.conf

# Install man pages.
install -m 644 %{SOURCE12} %{SOURCE13} %{SOURCE17} %{buildroot}%{_mandir}/man5/
for phase in auth acct passwd session ; do
    ln -sf pam_unix.so %{buildroot}/%{_lib}/security/pam_unix_${phase}.so
done

%find_lang Linux-PAM

%check
# (blino) we don't want to test if SE Linux is built, it's disabled
# Make sure every module subdirectory gave us a module.  Yes, this is hackish.
for dir in modules/pam_* ; do
if [ -d ${dir} ] ; then
    [ ${dir} = "modules/pam_selinux" ] && continue
    [ ${dir} = "modules/pam_sepermit" ] && continue
    [ ${dir} = "modules/pam_tty_audit" ] && continue
    if ! ls -1 %{buildroot}/%{_lib}/security/$(basename ${dir})*.so ; then
	echo ERROR $(basename ${dir}) did not build a module.
	exit 1
    fi
fi
done

# Check for module problems.  Specifically, check that every module we just
# installed can actually be loaded by a minimal PAM-aware application.
/sbin/ldconfig -n %{buildroot}/%{_lib}
chmod +x %{SOURCE11}
for module in %{buildroot}/%{_lib}/security/pam*.so ; do
    if ! env LD_LIBRARY_PATH=%{buildroot}/%{_lib} \
	sh %{SOURCE11} -ldl -lpam -L%{buildroot}/%{_lib} ${module} ; then
	echo ERROR module: ${module} cannot be loaded.
	exit 1
    fi
done

%triggerin -- %{name} < 1:1.3.0-10
sed -i -re 's/(^auth[ \t]+sufficient[ \t]+pam_tcb.so.*)/auth        sufficient    pam_unix.so try_first_pass likeauth nullok/' /etc/pam.d/system-auth
sed -i -re 's/(^account[ \t]+required[ \t]+pam_tcb.so.*)/account     required      pam_unix.so/' /etc/pam.d/system-auth
sed -i -re 's/(^password[ \t]+sufficient[ \t]+pam_tcb.so.*)/password    sufficient    pam_unix.so try_first_pass use_authtok nullok sha512 shadow/' /etc/pam.d/system-auth
sed -i -re 's/(^session[ \t]+required[ \t]+pam_tcb.so)/session     required      pam_unix.so/' /etc/pam.d/system-auth
# (cg) Ensure that the pam_systemd.so is included for user ACLs under systemd
# Note: Only affects upgrades, but does no harm so always update if needed.
if ! grep -q "pam_systemd\.so" %{_sysconfdir}/pam.d/system-auth; then
	echo "-session    optional      pam_systemd.so" >>%{_sysconfdir}/pam.d/system-auth
fi

%files -f Linux-PAM.lang
%docdir %{_docdir}/%{name}
%dir %{_sysconfdir}/pam.d
%config(noreplace) %{_sysconfdir}/environment
%config %{_sysconfdir}/pam.d/other
%config %{_sysconfdir}/pam.d/system-auth
%config(noreplace) %{_sysconfdir}/pam.d/fingerprint-auth
%config(noreplace) %{_sysconfdir}/pam.d/smartcard-auth
%config %{_sysconfdir}/pam.d/config-util
%config(noreplace) %{_sysconfdir}/pam.d/postlogin
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/pam_namespace.service
/sbin/faillock
/sbin/mkhomedir_helper
/sbin/pam_console_apply
/sbin/pam_namespace_helper
%attr(0755,root,root) /sbin/pwhistory_helper
%attr(4755,root,root) /sbin/unix_chkpwd
%attr(4755,root,root) /sbin/unix_update
%attr(4755,root,root) /sbin/pam_timestamp_check
%attr(0755,root,root) /sbin/mkhomedir_helper
%config(noreplace) %{_sysconfdir}/security/access.conf
%config(noreplace) %{_sysconfdir}/security/chroot.conf
%config(noreplace) %{_sysconfdir}/security/console.perms
%config(noreplace) %{_sysconfdir}/security/console.handlers
%config(noreplace) %{_sysconfdir}/security/faillock.conf
%config(noreplace) %{_sysconfdir}/security/group.conf
%config(noreplace) %{_sysconfdir}/security/limits.conf
%dir %{_sysconfdir}/security/limits.d
%config(noreplace) %{_sysconfdir}/security/namespace.conf
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/security/namespace.init
%config(noreplace) %{_sysconfdir}/security/pam_env.conf
%config(noreplace) %{_sysconfdir}/security/time.conf
%config(noreplace) %{_sysconfdir}/security/opasswd
%dir %{_sysconfdir}/security/console.apps
%dir %{_sysconfdir}/security/console.perms.d
%dir /%{_lib}/security
/%{_lib}/security/*.so
/%{_lib}/security/pam_filter
%ghost %dir /run/console
%ghost %dir /run/faillock
%dir %{_sysconfdir}/motd.d
%dir /run/motd.d
%dir /usr/lib/motd.d
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
/%{_lib}/libpam.so.%{major}*

%files -n %{libnamec}
/%{_lib}/libpamc.so.%{major}*

%files -n %{libname_misc}
/%{_lib}/libpam_misc.so.%{major}*

%files -n %{devname}
/%{_lib}/libpam.so
/%{_lib}/libpam_misc.so
/%{_lib}/libpamc.so
%{_includedir}/security/*.h
%{_mandir}/man3/*

%files doc
%doc doc/txts doc/specs/rfc86.0.txt Copyright NEWS
%doc %{_docdir}/%{name}/*
