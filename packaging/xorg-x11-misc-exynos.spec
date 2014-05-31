#sbs-git:slp/pkgs/xorg/driver/xserver-xorg-misc xserver-xorg-misc 0.0.1 13496ac354ad7f6709f1ef9b880a206a2df41c80

Name:	xorg-x11-misc-exynos
Summary:    X11 X server misc files for exynos
Version:    0.0.37
Release:    1
VCS:        magnolia/adaptation/ap_samsung/xserver-xorg-misc-exynos#xorg-x11-misc-exynos-0.0.6-1-47-g27a0e7218c4e5e6ec98ec5801657f371928eba86
ExclusiveArch:  %arm
Group:      System/X11
License:    MIT
Source0:    %{name}-%{version}.tar.gz
%if "%{_repository}" == "wearable"
Source1:    xorg.service
Source2:    xresources.service.wearable
Source3:    xscim.service
%else
Source1:    xresources.service.mobile
Source2:    xresources.path
%endif

Requires:   xserver-xorg-core
Requires:   xorg-x11-drv-evdev-multitouch
Requires(post):   xkeyboard-config

%description
Description: %{summary}


%prep
%setup -q


%build

%if "%{_repository}" == "wearable"
cd wearable
%else
cd mobile
%endif

{
for f in `find arm-common/ -name "*.in"`; do
	cat $f > ${f%.in};
	sed -i -e "s#@PREFIX@#/usr#g" ${f%.in};
	sed -i -e "s#@DATADIR@#/opt#g" ${f%.in};
	chmod a+x ${f%.in};
done
}

%reconfigure \
	--with-arch=arm \
	--with-conf-prefix=/

make %{?jobs:-j%jobs}

%install

%if "%{_repository}" == "wearable"
cd wearable
%else
cd mobile
%endif

rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}
%make_install
%if "%{_repository}" == "mobile"
mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/etc/rc.d/rc3.d/
mkdir -p %{buildroot}/etc/rc.d/rc4.d/
%endif
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/etc/X11/
%if "%{_repository}" == "wearable"
mkdir -p %{buildroot}/opt/etc/dump.d/module.d
mkdir -p %{buildroot}/usr/bin/
%else
cp -af arm-common/xserver %{buildroot}/etc/rc.d/init.d/
cp -af arm-common/xresources %{buildroot}/etc/rc.d/init.d/
%endif
cp -af arm-common/xsetrc %{buildroot}/etc/X11/
cp -af arm-common/Xmodmap %{buildroot}/etc/X11/
cp -af arm-common/xinitrc %{buildroot}/etc/X11/
%if "%{_repository}" == "wearable"
cp -af arm-common/winsys_log_dump.sh %{buildroot}/opt/etc/dump.d/module.d
cp -af arm-common/screenshot %{buildroot}%{_bindir}/
cp -af arm-common/screenshot-arm %{buildroot}%{_bindir}/
%else
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S02xserver
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S02xserver
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc4.d/S80xresources
%endif
cp -af arm-common/Xorg.sh %{buildroot}/etc/profile.d/
%if "%{_repository}" == "wearable"
mkdir -p %{buildroot}%{_libdir}/systemd/system/basic.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_libdir}/systemd/system/xorg.service
ln -s ../xorg.service %{buildroot}%{_libdir}/systemd/system/basic.target.wants/xorg.service
mkdir -p %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants
install -m 0644 %SOURCE2 %{buildroot}%{_libdir}/systemd/system/xresources.service
ln -s ../xresources.service.wearable %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/xresources.service
install -m 0644 %SOURCE3 %{buildroot}%{_libdir}/systemd/system/xscim.service
ln -s ../xscim.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/xscim.service
%else
mkdir -p %{buildroot}%{_libdir}/systemd/system/graphical.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_libdir}/systemd/system/xresources.service
install -m 0644 %SOURCE2 %{buildroot}%{_libdir}/systemd/system/xresources.path
ln -s ../xresources.path %{buildroot}%{_libdir}/systemd/system/graphical.target.wants/
%endif

cp -rf arm-e4412/* %{buildroot}/etc/X11/

%post
mkdir -p /opt/var/log

%files
%if "%{_repository}" == "wearable"
%manifest wearable/xorg-x11-misc-exynos.manifest
%else
%manifest mobile/xorg-x11-misc-exynos.manifest
%endif
%defattr(-,root,root,-)
/usr/share/license/%{name}
%{_sysconfdir}/profile.d/Xorg.sh
%if "%{_repository}" == "mobile"
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
%endif
%attr(-,inhouse,inhouse)
/etc/X11/Xresources
/etc/X11/xinitrc
/etc/X11/xsetrc
/etc/X11/Xmodmap
/etc/X11/xorg.conf
/etc/X11/xorg.conf.d/*.conf
%if "%{_repository}" == "wearable"
/opt/etc/dump.d/module.d/*
%endif
%{_bindir}/startx
%if "%{_repository}" == "wearable"
%{_bindir}/screenshot
%{_bindir}/screenshot-arm
%{_libdir}/systemd/system/xorg.service
%{_libdir}/systemd/system/basic.target.wants/xorg.service
%endif
%{_libdir}/systemd/system/xresources.service
%if "%{_repository}" == "wearable"
%{_libdir}/systemd/system/xscim.service
%{_libdir}/systemd/system/multi-user.target.wants/xresources.service
%{_libdir}/systemd/system/multi-user.target.wants/xscim.service
%else
%{_libdir}/systemd/system/xresources.path
%{_libdir}/systemd/system/graphical.target.wants/xresources.path
%endif
