#sbs-git:slp/pkgs/xorg/driver/xserver-xorg-misc xserver-xorg-misc 0.0.1 13496ac354ad7f6709f1ef9b880a206a2df41c80

Name:	xorg-x11-misc-exynos
Summary:    X11 X server misc files for exynos
Version:    0.0.56
Release:    1
VCS:        magnolia/adaptation/ap_samsung/xserver-xorg-misc-exynos#xorg-x11-misc-exynos-0.0.6-1-47-g27a0e7218c4e5e6ec98ec5801657f371928eba86
ExclusiveArch:  %arm
Group:      System/X11
License:    MIT
Source0:    %{name}-%{version}.tar.gz
%if "%{?tizen_profile_name}" == "wearable"
Source1:    xorg.service.wearable
Source2:    xresources.service.wearable
Source3:    xscim.service
%else
  %if "%{?tizen_profile_name}" == "mobile"
Source1:    xresources.service.mobile
Source2:    xresources.path
Source3:    xorg.service.mobile
  %endif
%endif

Requires:   xserver-xorg-core
Requires(post):   xkeyboard-config

%description
Description: %{summary}


%prep
%setup -q


%build

%if "%{?tizen_profile_name}" == "wearable"
cd wearable
%else
%if "%{?tizen_profile_name}" == "mobile"
cd mobile
%else
%if "%{?tizen_profile_name}" == "tv"
cd tv
%endif
%endif
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

%if "%{?tizen_profile_name}" == "wearable"
cd wearable
%else
%if "%{?tizen_profile_name}" == "mobile"
cd mobile
%else
%if "%{?tizen_profile_name}" == "tv"
cd tv
%endif
%endif
%endif

rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}
%make_install
%if "%{?tizen_profile_name}" == "mobile"
mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/etc/rc.d/rc3.d/
mkdir -p %{buildroot}/etc/rc.d/rc4.d/
%endif
%if "%{?tizen_profile_name}" == "tv"
mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/etc/rc.d/rc3.d/
mkdir -p %{buildroot}/etc/rc.d/rc4.d/
%endif
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/etc/X11/
%if "%{?tizen_profile_name}" == "wearable"
mkdir -p %{buildroot}/opt/etc/dump.d/module.d
mkdir -p %{buildroot}/usr/bin/
%else
cp -af arm-common/xserver %{buildroot}/etc/rc.d/init.d/
cp -af arm-common/xresources %{buildroot}/etc/rc.d/init.d/
%endif
cp -af arm-common/xsetrc %{buildroot}/etc/X11/
cp -af arm-common/xinitrc %{buildroot}/etc/X11/
%if "%{?tizen_profile_name}" == "wearable"
cp -af arm-common/winsys_log_dump.sh %{buildroot}/opt/etc/dump.d/module.d
%else
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S02xserver
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S02xserver
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc4.d/S80xresources
%if "%{?tizen_profile_name}" == "tv"
cp -af arm-common/winsys_log_dump.sh %{buildroot}/usr/bin/
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc3.d/S80xresources
%endif
%endif
cp -af arm-common/Xorg.sh %{buildroot}/etc/profile.d/
%if "%{?tizen_profile_name}" == "wearable"
mkdir -p %{buildroot}%{_libdir}/systemd/system/basic.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_libdir}/systemd/system/xorg.service
ln -s ../xorg.service %{buildroot}%{_libdir}/systemd/system/basic.target.wants/xorg.service
mkdir -p %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants
install -m 0644 %SOURCE2 %{buildroot}%{_libdir}/systemd/system/xresources.service
ln -s ../xresources.service.wearable %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/xresources.service
install -m 0644 %SOURCE3 %{buildroot}%{_libdir}/systemd/system/xscim.service
ln -s ../xscim.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/xscim.service
%else
%if "%{?tizen_profile_name}" == "mobile"
mkdir -p %{buildroot}%{_libdir}/systemd/system/graphical.target.wants
install -m 0644 %SOURCE3 %{buildroot}%{_libdir}/systemd/system/xorg.service
mkdir -p %{buildroot}%{_libdir}/systemd/system/basic.target.wants/
install -m 0644 %SOURCE3 %{buildroot}%{_libdir}/systemd/system/basic.target.wants/xorg.service
%endif
%endif

%if "%{?tizen_profile_name}" == "tv"
cp -rf arm-hawk-p/* %{buildroot}/etc/X11/
%else
cp -rf arm-e4412/* %{buildroot}/etc/X11/
%endif

mkdir -p %{buildroot}/opt/var/xkb
%if "%{?tizen_profile_name}" == "mobile"
  cp -rf arm-common/tizen_layout_mobile.txt %{buildroot}/opt/var/xkb/tizen_key_layout_temp.txt
%else
  %if "%{?tizen_profile_name}" == "wearable"
    cp -rf arm-common/tizen_layout_wearable.txt %{buildroot}/opt/var/xkb/tizen_key_layout_temp.txt
  %else
    %if "%{?tizen_profile_name}" == "tv"
      cp -rf arm-common/tizen_layout_tv.txt %{buildroot}/opt/var/xkb/tizen_key_layout_temp.txt
    %endif
  %endif
%endif

%post
mkdir -p /opt/var/log

%files
%if "%{?tizen_profile_name}" == "wearable"
%manifest wearable/xorg-x11-misc-exynos.manifest
%else
%if "%{?tizen_profile_name}" == "mobile"
%manifest mobile/xorg-x11-misc-exynos.manifest
%else
%if "%{?tizen_profile_name}" == "tv"
%manifest tv/xorg-x11-misc-hawk-p.manifest
%endif
%endif
%endif
%defattr(-,root,root,-)
/usr/share/license/%{name}
%{_sysconfdir}/profile.d/Xorg.sh
%if "%{?tizen_profile_name}" == "mobile"
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
%endif
%if "%{?tizen_profile_name}" == "tv"
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
%endif
/opt/var/xkb/tizen_key_layout_temp.txt
%attr(-,inhouse,inhouse)
/etc/X11/Xresources
/etc/X11/xinitrc
%if "%{?tizen_profile_name}" == "tv"
/usr/bin/winsys_log_dump.sh
%endif
/etc/X11/xsetrc
/etc/X11/xorg.conf
/etc/X11/xorg.conf.d/*.conf
%if "%{?tizen_profile_name}" == "wearable"
/opt/etc/dump.d/module.d/*
%endif

%{_bindir}/startx
%if "%{?tizen_profile_name}" == "wearable"
%{_libdir}/systemd/system/xorg.service
%{_libdir}/systemd/system/basic.target.wants/xorg.service
%else
%if "%{?tizen_profile_name}" == "mobile"
%{_libdir}/systemd/system/xorg.service
%{_libdir}/systemd/system/basic.target.wants/xorg.service
%endif
%endif
%if "%{?tizen_profile_name}" == "mobile"
%endif
%if "%{?tizen_profile_name}" == "wearable"
%{_libdir}/systemd/system/xresources.service
%endif
%if "%{?tizen_profile_name}" == "wearable"
%{_libdir}/systemd/system/xscim.service
%{_libdir}/systemd/system/multi-user.target.wants/xresources.service
%{_libdir}/systemd/system/multi-user.target.wants/xscim.service
%else
%if "%{?tizen_profile_name}" == "mobile"
%endif
%endif
