#sbs-git:slp/pkgs/xorg/driver/xserver-xorg-misc xserver-xorg-misc 0.0.1 13496ac354ad7f6709f1ef9b880a206a2df41c80
Name:	xorg-x11-misc-exynos
Summary:    X11 X server misc files for exynos
Version:    0.0.1
Release:    3
ExclusiveArch:  %arm
Group:      System/X11
License:    MIT
Source0:    %{name}-%{version}.tar.gz

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
	--with-conf-prefix=/usr

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

rm -fr %{buildroot}/usr/etc/X11/xorg.conf.d*
mkdir -p %{buildroot}/etc/rc.d/init.d/
mkdir -p %{buildroot}/etc/rc.d/rc3.d/
mkdir -p %{buildroot}/etc/rc.d/rc4.d/
mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}/%{_prefix}/etc/X11/
cp -af arm-common/xserver %{buildroot}/etc/rc.d/init.d/
cp -af arm-common/xresources %{buildroot}/etc/rc.d/init.d/
cp -af arm-common/xinitrc %{buildroot}/%{_prefix}/etc/X11/
cp -af arm-common/xsetrc %{buildroot}/%{_prefix}/etc/X11/
cp -af arm-common/Xmodmap %{buildroot}/%{_prefix}/etc/X11/
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc3.d/S02xserver
ln -s /etc/rc.d/init.d/xserver %{buildroot}/etc/rc.d/rc4.d/S02xserver
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc3.d/S80xresources
ln -s /etc/rc.d/init.d/xresources %{buildroot}/etc/rc.d/rc4.d/S80xresources
cp -af arm-common/Xorg.sh %{buildroot}/etc/profile.d/

cp -rf arm-e4412/* %{buildroot}/%{_prefix}/etc/X11/

%preun
rm -f /usr/etc/X11/Xmodmap
rm -f /usr/etc/X11/xorg.conf.d*

%post
mkdir -p /opt/var/log

%files
%defattr(-,root,root,-)
%{_sysconfdir}/profile.d/Xorg.sh
%{_sysconfdir}/rc.d/init.d/*
%{_sysconfdir}/rc.d/rc3.d/*
%{_sysconfdir}/rc.d/rc4.d/*
%attr(-,inhouse,inhouse)
%{_prefix}/etc/X11/Xresources
%{_prefix}/etc/X11/xorg.conf
%{_prefix}/etc/X11/xinitrc
%{_prefix}/etc/X11/xsetrc
%{_prefix}/etc/X11/Xmodmap
%{_prefix}/etc/X11/xorg.conf.d/*.conf
%{_bindir}/startx
