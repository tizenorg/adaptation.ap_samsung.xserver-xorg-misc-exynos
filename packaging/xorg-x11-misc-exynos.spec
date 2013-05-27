#sbs-git:slp/pkgs/xorg/driver/xserver-xorg-misc xserver-xorg-misc 0.0.1 13496ac354ad7f6709f1ef9b880a206a2df41c80
Name:	xorg-x11-misc-exynos
Summary:    X11 X server misc files for exynos
Version:    0.0.5
Release:    4
ExclusiveArch:  %arm
Group:      System/X11
License:    MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    xresources.service

Requires:   xserver-xorg-core
Requires(post):   xkeyboard-config

%description
Description: %{summary}


%prep
%setup -q


%build
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
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/share/license
cp -af COPYING %{buildroot}/usr/share/license/%{name}
%make_install

mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/etc/rc.d/rc3.d/
mkdir -p %{buildroot}/etc/rc.d/rc4.d/
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/etc/X11/
cp -af arm-common/xserver %{buildroot}/etc/rc.d/init.d/
cp -af arm-common/xresources %{buildroot}/etc/rc.d/init.d/
cp -af arm-common/xsetrc %{buildroot}/etc/X11/
cp -af arm-common/Xmodmap %{buildroot}/etc/X11/
cp -af arm-common/xinitrc %{buildroot}/etc/X11/
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S02xserver
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S02xserver
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc4.d/S80xresources
cp -af arm-common/Xorg.sh %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants
install -m 0644 %SOURCE1 %{buildroot}%{_libdir}/systemd/system/xresources.service
ln -s ../xresources.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/xresources.service

cp -rf arm-e4412/* %{buildroot}/etc/X11/

%post
mkdir -p /opt/var/log

%files
%manifest xorg-x11-misc-exynos.manifest
%defattr(-,root,root,-)
/usr/share/license/%{name}
%{_sysconfdir}/profile.d/Xorg.sh
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
%attr(-,inhouse,inhouse)
/etc/X11/Xresources
/etc/X11/xinitrc
/etc/X11/xsetrc
/etc/X11/Xmodmap
/etc/X11/xorg.conf
/etc/X11/xorg.conf.d/*.conf
%{_bindir}/startx
%{_libdir}/systemd/system/xresources.service
%{_libdir}/systemd/system/multi-user.target.wants/xresources.service

