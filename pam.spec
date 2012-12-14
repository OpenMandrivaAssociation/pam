%define major	0
%define libname %mklibname %{name} %{major}
%define libnamec %mklibname %{name}c %{major}
%define libname_misc %mklibname %{name}_misc %{major}
%define develname %mklibname %{name} -d

%define with_prelude 0
%{?_without_prelude: %{expand: %%global with_prelude 0}}
%{?_with_prelude: %{expand: %%global with_prelude 1}}

%define bootstrap 0
%{?_without_bootstrap: %global bootstrap 0}
%{?_with_bootstrap: %global bootstrap 1}

%define pam_redhat_version 0.99.10-1

Epoch:	1

Summary:	A security tool which provides authentication for applications
Name:		pam
Version:	1.1.6
Release:	1
# The library is BSD licensed with option to relicense as GPLv2+ - this option is redundant
# as the BSD license allows that anyway. pam_timestamp and pam_console modules are GPLv2+,
License:	BSD and GPLv2+
Group:		System/Libraries
Url:		http://www.kernel.org/pub/linux/libs/pam/index.html
#Source0:	ftp://ftp.kernel.org/pub/linux/libs/pam/library/Linux-PAM-%{version}.tar.bz2
#Source1:	ftp://ftp.kernel.org/pub/linux/libs/pam/library/Linux-PAM-%{version}.tar.bz2.sign
# (tpg) new url
Source0:	https://fedorahosted.org/releases/l/i/linux-pam/Linux-PAM-%{version}.tar.bz2
Source2:	pam-redhat-%{pam_redhat_version}.tar.bz2
Source3:	pam-0.99.3.0-README.update
Source4:	pam-0.99.8.1-11mdv2009.0-README.update
Source5:	other.pamd
Source6:	system-auth.pamd
Source7:	config-util.pamd
Source8:	dlopen.sh
Source9:	system-auth.5
Source10:	config-util.5
#add missing documentation
Source501: 	pam_tty_audit.8
Source502:	README

# RedHat patches
Patch1:		pam-1.0.90-redhat-modules.patch
Patch2:		pam-1.0.91-std-noclose.patch
Patch4:		pam-1.1.0-console-nochmod.patch
Patch5:		pam-1.1.0-notally.patch
Patch7:		pam-1.1.0-console-fixes.patch
Patch9:		pam-1.1.2-noflex.patch
Patch10:	pam-1.1.3-nouserenv.patch
Patch11:	pam-1.1.3-console-abstract.patch

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

# (akdengi> add user to default group users which need for Samba
Patch801:	Linux-PAM-1.1.4-group_add_users.patch

BuildRequires:	bison
BuildRequires:	cracklib-devel
BuildRequires:	flex
%if !%{bootstrap}
# this pulls in the mega texlive load
BuildRequires:	linuxdoc-tools
%endif
BuildRequires:	db_nss-devel
BuildRequires:	openssl-devel
BuildRequires:	libaudit-devel
BuildRequires:	glibc-crypt_blowfish-devel
%if %with_prelude
BuildRequires:	prelude-devel >= 0.9.0
%else
BuildConflicts:	prelude-devel
%endif
Requires:	cracklib-dicts
Requires:	setup >= 2.7.12-2
Requires:	pam_tcb >= 1.0.2-16
Requires(pre):	rpm-helper
Requires(post):	coreutils
Requires(post):	tcb >= 1.0.2-16
Conflicts:	%{_lib}pam0 < 1.1.4-5

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

%package	doc
Summary:	Additional documentation for %{name}
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description	doc
This is the documentation package of %{name}.

%package -n	%{libname}
Summary:	Library for %{name}
Group:		System/Libraries
Conflicts:	pam < 1.1.4-5

%description -n	%{libname}
This package contains the library libpam for %{name}.

%package -n	%{libnamec}
Summary:	Library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}pam0 < 1.1.4-5

%description -n	%{libnamec}
This package contains the library libpamc for %{name}.

%package -n	%{libname_misc}
Summary:	Library for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}pam0 < 1.1.4-5

%description -n	%{libname_misc}
This package contains the library libpam_misc for %{name}.

%package -n	%{develname}
Summary:	Development headers and libraries for %{name}
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Requires:	%{libnamec} = %{EVRD}
Requires:	%{libname_misc} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{develname}
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

This package contains the development libraries for %{name}.

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
%patch801 -p1 -b .group_users

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

libtoolize -cf
autoreconf -fi -I m4

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
%makeinstall_std LDCONFIG=:
install -d -m 755 %{buildroot}/etc/pam.d
install -m 644 %{SOURCE5} %{buildroot}/etc/pam.d/other
install -m 644 %{SOURCE6} %{buildroot}/etc/pam.d/system-auth
install -m 644 %{SOURCE7} %{buildroot}/etc/pam.d/config-util
install -m 600 /dev/null %{buildroot}%{_sysconfdir}/security/opasswd
install -d -m 755 %{buildroot}/var/log
install -m 600 /dev/null %{buildroot}/var/log/tallylog

# Install man pages.
install -m 644 %{SOURCE9} %{SOURCE10} %{buildroot}%{_mandir}/man5/

# no longer needed, handled by ACL in udev
for phase in auth acct passwd session ; do
	ln -sf pam_unix.so %{buildroot}/%{_lib}/security/pam_unix_${phase}.so
done

# cleanup
rm -f %{buildroot}/%{_lib}/security/*.la
rm -f %{buildroot}/%{_lib}/*.la

%find_lang Linux-PAM

%check
# (blino) we don't want to test if SE Linux is built, it's disabled
# Make sure every module subdirectory gave us a module.  Yes, this is hackish.
for dir in modules/pam_* ; do
if [ -d ${dir} ] && [[ "${dir}" != "modules/pam_selinux" ]] && [[ "${dir}" != "modules/pam_sepermit" ]]; then
         [[ "${dir}" = "modules/pam_tally" ]] && continue
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
		sh %{SOURCE8} -ldl -lpam -L%{buildroot}/%{_lib} ${module} ; then
		echo ERROR module: ${module} cannot be loaded.
		exit 1
	fi
done

%posttrans
# (cg) Ensure that the pam_systemd.so is included for user ACLs under systemd
# Note: Only affects upgrades, but does no harm so always update if needed.
if ! grep -q "pam_systemd\.so" /etc/pam.d/system-auth; then
	echo "-session    optional      pam_systemd.so" >>/etc/pam.d/system-auth
fi

if [ ! -a /var/log/tallylog ] ; then
       install -m 600 /dev/null /var/log/tallylog
fi
if [ -f /etc/login.defs ] && ! grep -q USE_TCB /etc/login.defs; then
       /usr/sbin/set_tcb --auto --migrate
fi

%files -f Linux-PAM.lang
%doc NEWS README.0.99.8.1.update.urpmi
%docdir %{_docdir}/%{name}
%dir /etc/pam.d
%config(noreplace) /etc/environment
%config /etc/pam.d/other
%attr(0644,root,shadow) %config /etc/pam.d/system-auth
%config /etc/pam.d/config-util
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
%dir /%{_lib}/security
/%{_lib}/security/*.so
/%{_lib}/security/pam_filter
%dir /var/run/console
%ghost %verify(not md5 size mtime) /var/log/tallylog
%{_mandir}/man5/*
%{_mandir}/man8/*

%files -n %{libname}
/%{_lib}/libpam.so.%{major}*

%files -n %{libnamec}
/%{_lib}/libpamc.so.%{major}*

%files -n %{libname_misc}
/%{_lib}/libpam_misc.so.%{major}*

%files -n %{develname}
%doc Copyright
/%{_lib}/libpam.so
/%{_lib}/libpam_misc.so
/%{_lib}/libpamc.so
%{_includedir}/security/*.h
%{_mandir}/man3/*

%files doc
%doc doc/txts doc/specs/rfc86.0.txt Copyright


%changelog
* Wed May 23 2012 Per Ãyvind Karlsen <peroyvind@mandriva.org> 1.1.4-9
+ Revision: 800224
- add a versioned conflicts to deal with pam modules having been moved out of
  library package, ensuring that the library package doesn't get upgraded
  independent of the pam package which now ships the modules which would lead
  to modules possibly missing and anything using pam left broken

* Sun Apr 29 2012 Per Ãyvind Karlsen <peroyvind@mandriva.org> 1.1.4-8
+ Revision: 794382
- pam files *really* shouldn't be config(noreplace) but rather %%config, otherwise
  upgrades where these files has changed between releases will very easily turn
  fugly (TODO: post RFC about this as a policy and implement rpmlint check to
  enforce it)

* Fri Mar 09 2012 Per Ãyvind Karlsen <peroyvind@mandriva.org> 1.1.4-7
+ Revision: 783687
- rebuild to get rid of false devel() dependency in main package

* Wed Mar 07 2012 Per Ãyvind Karlsen <peroyvind@mandriva.org> 1.1.4-6
+ Revision: 782601
- fix module subdirectory test
- fix assumption of dlopen.sh being executable (which will no longer be true as
  all files packaged with src.rpms are now always given 644 for attributes)
- rebuild with internal dependency generator

  + Matthew Dawkins <mattydaw@mandriva.org>
    - rebuild for db_nss
    - moved security modules to main pkg
    - split up libs into individual pkgs
    - cleaned up spec

* Tue Dec 13 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-4
+ Revision: 740745
- delete the libtool *.la files
- attempt to relink against db_nss-devel 5.2.x

  + Per Ãyvind Karlsen <peroyvind@mandriva.org>
    - no need for removing .la files, it's done automatically by spec-helper now
    - apply some cosmetics
    - use %%{EVRD} macro
    - drop obsolete obsoletes ;)
    - ditch bogus provides
    - fix broken check for USE_TCB in /etc/login.defs making script always run

* Sat Sep 03 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.4-2
+ Revision: 698188
- enable systemd pam suport (since udev-173 ther is no more udev_acl, and systemd takes over ACL)

* Tue Jul 19 2011 Per Ãyvind Karlsen <peroyvind@mandriva.org> 1.1.4-1
+ Revision: 690602
- new release

* Tue Jul 19 2011 Per Ãyvind Karlsen <peroyvind@mandriva.org> 1.1.3-4
+ Revision: 690600
- remove obsolete/deprecated rpm stuff
- check if /etc/login.defs exists before trying to open it in scriptlet

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.1.3-3
+ Revision: 666974
- mass rebuild

  + Per Ãyvind Karlsen <peroyvind@mandriva.org>
    - work around ordering issue by moving %%post script to %%posttrans

* Wed Nov 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.3-1mdv2011.0
+ Revision: 592873
- 1.1.3
- sync patches with pam-1.1.3-1.fc15.src.rpm
- rediffed P512

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.1-2mdv2010.1
+ Revision: 519980
- rebuilt against audit-2 libs

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.1-1mdv2010.1
+ Revision: 484161
- Update to new version 1.1.1
- Remove authok patch: integrated upstream
- Rediff xauth groups patch
- Don't run libtoolize: it breaks build
- drop tests for not pulling in libpthread like in Fedora (as NPTL
  should be safe and pam_userdb now links to libpthread on x86_64)

* Tue Oct 06 2009 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-6mdv2010.0
+ Revision: 454902
- Patch701: do not complain if there is no files in /etc/security/console.perms.d/

* Sun Sep 27 2009 Olivier Blin <blino@mandriva.org> 1.1.0-5mdv2010.0
+ Revision: 450211
- fix crash on some archs, pam is building with static all functions
  with is plain wrong, this tends to make pam_comsole_apply
  unhappy/crashing (from Arnaud Patard)

* Tue Sep 08 2009 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-4mdv2010.0
+ Revision: 433622
- Patch4 (Fedora): do not chmod tty on login/login with pam_console anymore
- Patch5 (Fedora): drop pam_tally, use pam_tally2 instead

* Thu Aug 27 2009 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-3mdv2010.0
+ Revision: 421690
- Patch3 (Fedora): fix for pam_cracklib from upstream

* Mon Jul 27 2009 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-2mdv2010.0
+ Revision: 400600
- remove default rules for console.perms, device ownership should not change anymore

* Mon Jul 27 2009 Frederic Crozat <fcrozat@mandriva.com> 1.1.0-1mdv2010.0
+ Revision: 400582
- Release 1.1.0
- no longer change devices ownership based on console privilege, handled by consolekit now (remove source500, patches 500, 501)

* Sun May 10 2009 Frederik Himpe <fhimpe@mandriva.org> 1.0.92-1mdv2010.0
+ Revision: 374099
- Remove verbose limits patch: a similar change was implemented upstream
- Update to new version Linux-PAM 1.0.92 and pam-redhat 0.99.10-1
- Resync patches with Fedora
- Rediff xauth-groups patch
- Remove man page typo fix, noselinux and bid 34010 patches
  (integrated upstream)
- Don't conflict with libselinux-devel and use --disable-selinux in
  configure call
- Disable verbose call patch for now, upstream code has changed too

* Thu Apr 16 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.8.1-20mdv2009.1
+ Revision: 367795
- Disable fork option for pam_tcb, to reflect the change made in set_tcb

* Mon Mar 30 2009 Frederic Crozat <fcrozat@mandriva.com> 0.99.8.1-19mdv2009.1
+ Revision: 362380
- Add console for raw1394 (Mdv bug #47622)

* Thu Mar 19 2009 Frederik Himpe <fhimpe@mandriva.org> 0.99.8.1-18mdv2009.1
+ Revision: 358110
- Add upstream patch fixing security issue (Bugtraq ID 34010)

* Sun Mar 08 2009 Michael Scherer <misc@mandriva.org> 0.99.8.1-17mdv2009.1
+ Revision: 352736
- fix build by updating libtool script
- update patch 32
- rediff patch 31

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Tue Aug 12 2008 Vincent Danen <vdanen@mandriva.com> 0.99.8.1-16mdv2009.0
+ Revision: 271144
- call set_tcb in %%post and require tcb itself as a result

* Tue Aug 12 2008 Olivier Blin <blino@mandriva.org> 0.99.8.1-15mdv2009.0
+ Revision: 271055
- move pam_tcb conflict in the proper lib package (#42709)

* Mon Aug 11 2008 Olivier Blin <blino@mandriva.org> 0.99.8.1-14mdv2009.0
+ Revision: 270658
- conflict with old tcb package that contained pam_unix

* Sat Aug 09 2008 Vincent Danen <vdanen@mandriva.com> 0.99.8.1-13mdv2009.0
+ Revision: 270079
- require new pam_tcb release
  require specific setup version for the shadow group
  restore old pam_unix and its symlinks
  ensure system-auth permissions and ownership

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.99.8.1-12mdv2009.0
+ Revision: 265321
- rebuild early 2009.0 package (before pixel changes)

  + Oden Eriksson <oeriksson@mandriva.com>
    - unset BROWSER

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 22 2008 Vincent Danen <vdanen@mandriva.com> 0.99.8.1-11mdv2009.0
+ Revision: 210056
- libpam conflicts with pam < 0.99.8.1-10mdv
- dropped the system-auth migration as per blino
- restored the 0.99.3.1 README
- renamed and trimmed the 0.99.8.1-11mdv README

* Tue May 20 2008 Vincent Danen <vdanen@mandriva.com> 0.99.8.1-10mdv2009.0
+ Revision: 209289
- gracefully handle non-standard system-auth configurations to replace pam_unix with pam_tcb (for instances like using ldap for auth, etc.) which, if not done correctly or immediately, could result in local accounts being locked out

* Mon May 19 2008 Vincent Danen <vdanen@mandriva.com> 0.99.8.1-9mdv2009.0
+ Revision: 209172
- add -D_GNU_SOURCE to $CFLAGS in order to compile pam_console and pam_timestamp
- requires pam_tcb
- buildrequires glibc-crypt_blowfish-devel
- don't build pam_unix; pam_tcb provides it
- unix_chkpwd and unix_update are no longer required without pam_unix
- clean up system-auth(5)
- update system-auth to use pam_tcb
- updated the Mandriva-specific README

* Fri Jan 18 2008 Frederic Crozat <fcrozat@mandriva.com> 0.99.8.1-8mdv2008.1
+ Revision: 154727
- Update license info based on fedora specfile
- Update patches 25, 44 with latest version from fedora
- Remove patch26, merged into patch25
- Patch42, 43 (Fedora): don't use pam_console to change device ownership, rely on HAL ACL now
- Patch46 (Fedora): fix in operator (Fedora #295151)
- Patch47 (Fedora): fix invalid free on xauth module
- Patch48 (Fedora): add support for substack include
- Patch49, 50 (Fedora): add tty_audio module
- Patch523: fix build when SELinux is disabled
- Source501, 502 : add missing documentation from tarball
- Resync system-auth file with Fedora

* Fri Dec 21 2007 Oden Eriksson <oeriksson@mandriva.com> 0.99.8.1-7mdv2008.1
+ Revision: 136256
- link against the bdb 4.6.x assembly-mutex-only db (buchan)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Marcelo Ricardo Leitner <mrl@mandriva.com>
    - As Blino pointed out, we can do Requires(post): coreutils as coreutils
      currently just "Requires: pam", with no specific order.
      This also fix a bug in the previous "fix" that would make the /dev/null
      device be copied instead of creating a blank file.
    - Do not use the install utility on %%post section because we can't require
      coreutils as coreutils already requires us. So replace install calls by
      cp -a and chmod ones, fixing without introducing a circular dependency.

* Thu Sep 20 2007 Frederic Crozat <fcrozat@mandriva.com> 0.99.8.1-6mdv2008.0
+ Revision: 91448
- Update patch24 with latest fedora version
- Patch25 (Fedora): do not ask for blank password when SELinux confined (Fedora #254044)

* Wed Sep 12 2007 Anssi Hannula <anssi@mandriva.org> 0.99.8.1-5mdv2008.0
+ Revision: 84662
- show 0.99.3.0 notes only when upgrading from an older version

* Mon Sep 10 2007 Olivier Blin <blino@mandriva.org> 0.99.8.1-4mdv2008.0
+ Revision: 84153
- make evdev mouse devices owned by console user (fix synclient, #32955)

* Mon Sep 03 2007 Frederic Crozat <fcrozat@mandriva.com> 0.99.8.1-3mdv2008.0
+ Revision: 78627
- Update patches 40 & 5 with latest version from RH (Fix Mdv bug #32741)
- Patch44 (RH): fix homedir init with namespace module

* Mon Aug 13 2007 Olivier Blin <blino@mandriva.org> 0.99.8.1-2mdv2008.0
+ Revision: 62485
- add scanner devices in the usb group (#29489, #29562)
- make sure devices are accessible by their group if specified in console.perms (#29489)
- remove mode definitions from mdvperms patch (will be done by a one-liner in the spec)
- restore console settings for lp class (wrongly removed in 0.99.6.0 rediff, #29562)
- move lp class in 50-mandriva.perms
- add compatibility symlinks for pam_unix_{auth,acct,passwd,session}.so
- add /etc/security/opasswd file
- add more module checks in check section (from Fedora)
- move checks in check section
- properly include /var/log/faillog and tallylog as ghosts and create them in post script (from Fedora)
- add user and new instance parameters to namespace init (from Fedora)
- fix typo in man pages
- enable libaudit
- rediff mdv perms patch
- do not log an audit error when uid != 0 (from Fedora)
- update to pam-redhat-0.99.8-1
- adapt to new devel library policy
- add signature
- rename sources to match RH spec file
- remove useless chmod

* Tue Jul 24 2007 Olivier Blin <blino@mandriva.org> 0.99.8.1-1mdv2008.0
+ Revision: 55033
- 0.99.8.1
- update RH patches
- package /sbin/unix_update
- remove old packaging hacks
- use new doc directory policy

* Sat Jul 21 2007 David Walluck <walluck@mandriva.org> 0.99.7.1-3mdv2008.0
+ Revision: 54187
- add config-util.pamd


* Wed Feb 07 2007 Olivier Blin <oblin@mandriva.com> 0.99.7.1-2mdv2007.0
+ Revision: 117173
- mark doc dir as docdir
- fix doc installation
- update pam_redhat to 0.99.7-1
- allow more X displays as consoles (RH #227462)

* Wed Jan 24 2007 Olivier Blin <oblin@mandriva.com> 0.99.7.1-1mdv2007.1
+ Revision: 112870
- 0.99.7.1

* Tue Jan 23 2007 Olivier Blin <oblin@mandriva.com> 0.99.7.0-1mdv2007.1
+ Revision: 112280
- 0.99.7.0

* Fri Oct 20 2006 Olivier Blin <oblin@mandriva.com> 0.99.6.3-1mdv2007.1
+ Revision: 71373
- link pam_userdb with db4 (#26242 and #26572)
- pam_loginuid is now in upstream sources
- remove console reset patch, now handled upstream
- 0.99.6.3

* Sat Sep 16 2006 Olivier Blin <oblin@mandriva.com> 0.99.6.0-3mdv2007.0
+ Revision: 61618
- 0.99.6.0-3mdv
- chown IR remote controls devices to console user (Anssi Hannula, #24785)
- add /dev/scd* /dev/sg* /dev/cdrw* /dev/dvdrw* in burner devices list (#25371 and #24541)

* Wed Aug 30 2006 Olivier Blin <oblin@mandriva.com> 0.99.6.0-2mdv2007.0
+ Revision: 58719
- bump release
- make cdrom devices owned by cdrom group

  + Anssi Hannula <anssi@mandriva.org>
    - add /dev/input/by-path/*-joystick to <joystick> class (fixes #23775)
    - make <sound> class devices accessible by audio group (fixes #24300)
    - make <v4l> and <dvb> class devices accessible by video group (fixes #24786)

* Fri Aug 11 2006 Olivier Blin <oblin@mandriva.com> 0.99.6.0-1mdv2007.0
+ Revision: 55258
- use ndbm from db1 to build pam_userdb
- drop html, ps and pdf doc (pdf doc would require Apache's fop to be packaged)
- make doc/txts directory (not provided upstream anymore)
- namespace.init is now provided upstream
- drop more sgml hacks (sgml not used upstream anymore)
- remove pam-0.77-use_uid.patch (fixed upstream)
- remove pam_keyinit patches (merged upstream)
- remove pam-0.99.5.0-access-gai.patch (applied upstream)
- remove pam-0.99.4.0-succif-service.patch (merged upstream)
- remove sgml2latex patch, it doesn't apply anymore since xml is used instead of sgml in 0.99.6.0
- 0.99.6.0
- really use pam-redhat-0.99.6-1
- remove patch merged in pam-redhat 0.99.6-1
- revoke keyrings properly when pam_keyinit called more than once (RH)
- don't log pam_keyinit debug messages by default
- drop ainit from console.handlers (RH)
- add pam_keyinit to the default system-auth file (RH)
- fixed network match in pam_access (from Redhat)
- sync with pam-redhat 0.99.6-1 (and rediff mdvperms, RH merged a lot of our permissions)
- import pam-0.99.5.0-2mdv2007.0

* Tue Jul 04 2006 Olivier Blin <oblin@mandriva.com> 0.99.5.0-2mdv2007.0
- Source500: add ttyACM* devices in the serial class (#23190)
- Patch83 (from Fedora): add service as value to be matched and list
  matching to pam_succeed_if
- use upstream redhat-modules patch

* Thu Jun 29 2006 Olivier Blin <oblin@mandriva.com> 0.99.5.0-1mdv2007.0
- 0.99.5.0
- Patch523: temporary patch to add namespace.init, which is missing from dist
  (extracted from RH old namespace patch)
- package namespace files in /etc/security
- Patch84 (from RH): pam_console_apply shouldn't access /var when called with -r

* Thu Jun 29 2006 Olivier Blin <oblin@mandriva.com> 0.99.4.0-1mdv2007.0
- 0.99.4.0
- from Fedora:
  o pam-0.99.4.0-redhat-modules
  o pam-redhat-0.99.5-1
  o add system-auth and config-util man pages
- drop Patch523 and all pwdb bits
- drop glib2-devel BuildRequires (pam_console_apply don't need it anymore)
- rediff Patch500 (mdv perms)
- drop Patch520 (merged upstream)
- don't check for userdb module, we don't built it
  (it requires an internal libdb copy)
- package pam_tally2

* Thu Feb 02 2006 Olivier Blin <oblin@mandriva.com> 0.99.3.0-6mdk
- update instructions in the README.update.urpmi file (Source4)

* Wed Feb 01 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.99.3.0-5mdk
- patch 500:
  o fix firewire perms (#20270)
  o fix printer perms (#13013)

* Mon Jan 30 2006 Olivier Blin <oblin@mandriva.com> 0.99.3.0-4mdk
- don't build prelude (#20896)
- Patch523: allow to disable pwdb
- disable pam_pwdb
- make unix_chkpwd setuid root again
- Source2: remove hardcoded /lib/security in source
  (even if spec-helper fixes it later)
- don't add video group in %%pre, it's already in the setup package
- remove hardcoded workaround for a (more than) 2 years-old pam
- more BuildRequires fixes: drop autoconf2.1, use glib2-devel
  (thanks to Stefan van der Eijk)
- rpmbuildupdatable
- Source4: README.update.urpmi

* Sat Jan 28 2006 Olivier Blin <oblin@mandriva.com> 0.99.3.0-3mdk
- BuildRequires automake1.8 (Stefan van der Eijk)
- fix again Patch517 (use real patch name)
- fix typo in modules installation test

* Sat Jan 28 2006 Olivier Blin <oblin@mandriva.com> 0.99.3.0-2mdk
- BuildConflicts with libselinux-devel (#20871)
- don't test if modules/pam_selinux is built, we don't want it
- Patch517: fix typo in limits.conf (Andrey Borzenkov, #20872)
- BuildRequires openssl-devel (#20874)
- Patch511: use pam_syslog instead of old _pam_log in pam_limits
  (Andrey Borzenkov, #20876)
- BuildRequires prelude-devel

* Sat Jan 28 2006 Olivier Blin <oblin@mandriva.com> 0.99.3.0-1mdk
- 0.99.3.0
- sync with RH (all of their others patches are either merged upstream,
  or useless in Mandriva, such as SE Linux):
  o drop Patch39 (wasn't needed for 0.77)
  o drop Patch[0,1,2,3,5,6,7,8,9,11,12,13,14,15,16,17,18,19,20],
    Patch[22,23,24,25,26,27,30,31,32,33,35,36,37,40] and Source4
    (dropped during 0.78 upgrade)
  o drop Patch29 (dropped during 0.79 upgrade)
  o drop Patch4 (dropped during 0.80 upgrade)
  o rediff Patch21
  o don't use fakeroot anymore
  o don't enable static-pam
  o drop Patch10 (dropped during 0.99.2.1 upgrade)
  o rediff Patch34
  o fix descriptions
- rediff Patch500, and split out Mandriva-specific perms in Source500
  (installed as 50-mandriva.perms)
- remove devfs-style paths in Patch500/Source500
- drop Patch502 (dead X problem fixed otherwise upstream)
- drop Patch503 (we don't need pam_console_apply_devfsd)
- rediff Patch504 (drop merged parts), Patch508, Patch512
- drop Patch506 (not required anymore to detect cracklib dicts on x86_64)
- drop Patch507 (tty name not found fixed otherwise upstream)
- drop Patch509 (fixed upstream)
- drop Patch513 (fixed otherwise upstream, should still work with lsb-test-pam)
- drop Patch514 (kill pam_console_setowner, pam_console_apply should be used)
- drop Patch515 (/etc/environment test fixed upstream)
- drop Patch516 (RT now supported upstream)
- rediff Patch517 (apply on limits.conf, use new rtprio keyword instead of
  previous rt_priority)
- drop Patch518 (build with gcc 4 works fine now)
- add comments about ghost patches
- Patch520 and Patch521: fix parallel build
- Patch522: ensure that sgml2txt worked
- package new security/console.handlers and security/console.perms.d/
- package pam_filter/upperLOWER
- package libpamc
- package security/chroot.conf
- package lang files
- don't package pwdb_chkpwd
- more description fixes

* Thu Jan 26 2006 Olivier Blin <oblin@mandriva.com> 0.77-37mdk
- handle permissions for /dev/bus/usb

* Tue Jan 24 2006 Olivier Blin <oblin@mandriva.com> 0.77-36mdk
- fix permissions for more DVB devices (merge Patch520 in Patch500)

* Mon Jan 23 2006 Olivier Blin <oblin@mandriva.com> 0.77-35mdk
- update Patch514 to handle multiple arguments in pam_console_setowner,
  (from Andrey Borzenkov, #20269, it's about reimplementing recent
   pam_console_apply in our weird pam_console_setowner)
- use requires instead of prereq for pam-doc

* Tue Jan 10 2006 Thierry Vignaud <tvignaud@mandriva.com> 0.77-34mdk
- patch 520: set perms for DVB devices (#14688)

* Fri Jan 06 2006 Oden Eriksson <oeriksson@mandriva.com> 0.77-33mdk
- drop selinux (P60)
- removed two hunks from P40 (required the selinux patch applied)
- dropped P62 (required the selinux patch applied)
- rebuilt against a non selinux enabled pwdb lib (thanks stefan)

* Wed Oct 05 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 0.77-32mdk
- fix build on ppc64

* Tue Sep 20 2005 Frederic Lepied <flepied@mandriva.com> 0.77-31mdk
- fix uninitialized variable user (aka fix crash on C3)

* Sun Jul 31 2005 Couriousous <couriousous@mandriva.org> 0.77-30mdk
- Don't apply 64bit patch ( fix #16961 )

* Wed Jun 22 2005 Frederic Lepied <flepied@mandriva.com> 0.77-29mdk
- fixed dependencies

* Mon May 16 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.77-28mdk 
- patch 516: add support for RT/nice rlimit settings (kernel-2.6.12+)
- patch 517: enable new RT privileges for audio group in limits.conf
- patch 518: fix build with gcc-4.0

* Thu Apr 07 2005 Frederic Crozat <fcrozat@mandrakesoft.com> 0.77-27mdk 
- Update Patch500 to add /dev/zip* and /dev/jaz* as zip/jaz group for
  console privilege

* Thu Sep 30 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-26mdk
- give access to /dev/nvram in ro for console users
- handle /dev/dri* and /dev/nvidia the same way in startx and *dm modes.

* Tue Sep 21 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-25mdk
- pam_env: don't abort if /etc/environment isn't present (Oded Arbel)
- fix BuildRequires (Oded Arbel)
- create an empty /etc/environment
- add USB joystick devices to console.perms (bug #11190)

* Fri Sep 17 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.77-24mdk
- really build pam_console_apply_devfs against glib-1.2

* Sat Sep 11 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-23mdk
- fixed debug code in pam_console_apply_devfsd
- added a way to debug pam_console_setowner by setting PAM_DEBUG env variable
- don't apply patch63 to have console.lock at the usual place

* Fri Sep 10 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-22mdk
- implement pam_console_setowner for udev

* Thu Sep 09 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.77-21mdk
- add sr* to cdrom group

* Wed Sep 08 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-20mdk
- fixed lookup when a group or a user doesn't exist (bug #11256)
- fixed the group of audio devices when nobody is connected

* Tue Aug 24 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-19mdk
- added /dev/rfcomm* /dev/ircomm* to serial group (Fred Crozat)

* Tue Aug 24 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-18mdk
- put back <serial> group in console.perms

* Tue Aug 24 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-17mdk
- manage dri files perm (bug #10876 )
- manage perm of /dev/raw1394 (bug #9240)
- console.perms more group friendly (bug #3033)
- merged with rh 0.77-54

* Wed Jul 28 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 0.77-16mdk
- Update patch16 to give console permissions to rfcomm devices

* Tue Jul 06 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-15mdk
- fixed typo in provides for devel package

* Sat Jul 03 2004 Stew Benedict <sbenedict@mandrakesoft.com> 0.77-14mdk
- patch for lsb2 lsb-test-pam compliance (patch513)

* Mon Jun 14 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.77-13mdk
- fix buildrequires
- fix provides
- cosmetics

* Tue Feb 24 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-12mdk
- console.perms: /proc/usb => /proc/bus/usb (Marcel Pol) [bug #8285]

* Thu Feb 19 2004 Frederic Lepied <flepied@mandrakesoft.com> 0.77-11mdk
- added a trigger to be able to upgrade

