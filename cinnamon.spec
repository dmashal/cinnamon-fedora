%global        _internal_version  5ab432d

%{?filter_setup:
%filter_from_provides /^libcinnamon.so/d;
%filter_from_requires /^libcinnamon.so/d;
%filter_setup
}

Name:           cinnamon
Version:        1.6.7
Release:        7%{?dist}
Summary:        Window management and application launching for GNOME

Group:          User Interface/Desktops
# cinnamon-menu-editor is LGPLv2+
License:        GPLv2+ and LGPLv2+
URL:            http://cinnamon.linuxmint.com
# To generate tarball
# wget https://github.com/linuxmint/Cinnamon/tarball/%%{_internal_version} -O cinnamon-%%{version}.git%%{_internal_version}.tar.gz
Source0:        http://leigh123linux.fedorapeople.org/pub/cinnamon/source/cinnamon-%{version}.tar.gz
Source1:        cinnamon.desktop
Source2:        cinnamon.session
Source3:        cinnamon2d.desktop
Source4:        cinnamon2d.session
Source5:        cinnamon-screensaver.desktop
Source6:        cinnamon2d-screensaver.desktop


# Fix menu structure
Patch0:         cinnamon-1.4.1_menu.patch
Patch1:         cinnamon-1.5.0_datetime_setting.patch
# Replace mint favorites with fedora gnome-shell defaults
Patch2:         cinnamon-1.6.0_favourite-apps-firefox.patch
Patch3:         fedora_icon.patch
Patch4:         cinnamon.css.patch
Patch5:         keyboard_applet.patch
Patch6:         cinnamon_menu_applet.patch
# upstream patches and pending pulls

# https://github.com/linuxmint/Cinnamon/pull/1612
Patch7: cinnamon-pillow.patch


%global clutter_version 1.10.1
%global gobject_introspection_version 0.10.1
%global muffin_version 1.1.0
%global eds_version 2.91.6
%global json_glib_version 0.13.2


BuildRequires:  clutter-devel >= %{clutter_version}
BuildRequires:  dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gjs-devel >= 0.7.14-6
BuildRequires:  glib2-devel
BuildRequires:  GConf2-devel
BuildRequires:  gnome-menus-devel >= 3.1.5-2.fc16
BuildRequires:  gnome-desktop3-devel
BuildRequires:  gobject-introspection >= %{gobject_introspection_version}
BuildRequires:  json-glib-devel >= %{json_glib_version}
BuildRequires:  upower-devel
BuildRequires:  NetworkManager-glib-devel
BuildRequires:  polkit-devel
BuildRequires:  libgudev1-devel
# for screencast recorder functionality
BuildRequires:  gstreamer-devel
BuildRequires:  gtk3-devel
BuildRequires:  intltool
BuildRequires:  libcanberra-devel
BuildRequires:  libcroco-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  libsoup-devel


# for barriers
BuildRequires:  libXfixes-devel >= 5.0
# used in unused BigThemeImage
BuildRequires:  librsvg2-devel
BuildRequires:  muffin-devel >= %{muffin_version}
BuildRequires:  pulseaudio-libs-devel
%ifnarch s390 s390x
BuildRequires:  gnome-bluetooth-libs-devel >= 2.91
BuildRequires:  gnome-bluetooth >= 2.91
%endif
# Bootstrap requirements
BuildRequires: gtk-doc gnome-common
Requires:       gnome-menus%{?_isa} >= 3.0.0-2
# wrapper script uses to restart old GNOME session if run --replace
# from the command line
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}
# needed for loading SVG's via gdk-pixbuf
Requires:       librsvg2%{?_isa}
# needed as it is now split from Clutter
Requires:       json-glib%{?_isa} >= %{json_glib_version}
# might be still be needed.
Requires:       muffin%{?_isa} >= %{muffin_version}
Requires:       upower%{?_isa}
Requires:       polkit%{?_isa} >= 0.100
# needed for session files
Requires:       gnome-session
# needed for schemas
Requires:       at-spi2-atk%{?_isa}
# needed for on-screen keyboard
Requires:       caribou%{?_isa}
# needed for the user menu
Requires:       accountsservice-libs
Requires:       %{name}-settings = %{version}-%{release}


%description
Cinnamon is a Linux desktop which provides advanced
 innovative features and a traditional user experience.

The desktop layout is similar to Gnome 2. 
The underlying technology is forked from Gnome Shell.
The emphasis is put on making users feel at home and providing
 them with an easy to use and comfortable desktop experience.

%package 2d
Summary:        Browser plugins for the Cinnamon Desktop
Group:          User Interface/Desktops
BuildArch:	noarch
Requires:       %{name} = %{version}-%{release}

%description 2d
The Cinnamon Desktop provides advanced innovative features and a traditional
user experience. The underlying technology is forked from gnome-shell and the
desktop layout is closer to GNOME2. The emphasis is put on making users look
and feel at home and provide them an easy to use and confortable experience.

%package settings
Summary:        Settings GUI for Cinnamon
Group:          Applications/System
BuildArch:	noarch
# needed for settings
Requires:       pygobject2
Requires:       dbus-python
Requires:       python-lxml
Requires:       gnome-python2-gconf
Requires:       python-imaging

%description settings
The Cinnamon Desktop provides advanced innovative features and a traditional
user experience. The underlying technology is forked from gnome-shell and the
desktop layout is closer to GNOME2. The emphasis is put on making users look
and feel at home and provide them an easy to use and confortable experience.

%package menu-editor
Summary:        Menu editor for Cinnamon based on Alacarte
Group:          Applications/System
BuildArch:	noarch
Requires:       %{name} = %{version}-%{release}
# needed for cinnamon-menu
# https://bugzilla.redhat.com/show_bug.cgi?id=872694
Requires:       gnome-panel

%description menu-editor
The Cinnamon Desktop provides advanced innovative features and a traditional
user experience. The underlying technology is forked from gnome-shell and the
desktop layout is closer to GNOME2. The emphasis is put on making users look
and feel at home and provide them an easy to use and confortable experience.


%prep
%setup -q -n linuxmint-Cinnamon-%{_internal_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# keyboard applet patch
# https://github.com/linuxmint/Cinnamon/issues/1337#issuecomment-10342075
%if 0%{?fedora} > 17
%patch5 -p1
%endif

%patch6 -p1

# upstream patches and pending pulls
%patch7 -p1


# remove gschema
rm -rf data/org.cinnamon.gschema.xml
# make changes for settings move to /usr/share
mv files/usr/lib/cinnamon-settings files%{_datadir}
sed -i -e 's@/usr/lib@/usr/share@g' files%{_bindir}/cinnamon-settings \
  files%{_datadir}/cinnamon-settings/cinnamon-settings.py \
  js/ui/panel.js cinnamon.pot
# make changes for menu-editor move to /usr/share
mv files/usr/lib/cinnamon-menu-editor files%{_datadir}
rm -rf files/usr/lib
sed -i -e 's@/usr/lib@/usr/share@g' files%{_bindir}/cinnamon-menu-editor \
  files%{_datadir}/cinnamon-menu-editor/Alacarte/MainWindow.py
sed -i -e 's@-OOt@-t@g' files%{_bindir}/cinnamon-menu-editor
# remove and replace the session files as they don't work with fedora (can't be bothered to patch it)
rm -f files%{_bindir}/gnome-session-cinnamon  \
 files%{_datadir}/xsessions/cinnamon*.desktop \
 files%{_datadir}/gnome-session/sessions/cinnamon*.session
install -pm 644 %SOURCE1 %SOURCE3 files%{_datadir}/xsessions/
install -pm 644 %SOURCE2 %SOURCE4 files%{_datadir}/gnome-session/sessions/
# files replaced with fedora files
rm -f files%{_datadir}/desktop-directories/cinnamon-{menu-applications,utility,utility-accessibility,development,education,game,graphics,network,audio-video,office,system-tools,other}.directory

rm -f configure
rm -rf debian/
NOCONFIGURE=1 ./autogen.sh

%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-error=deprecated-declarations"
%configure --disable-static --enable-compile-warnings=yes
make V=1 %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

# Remove .la file
rm -rf $RPM_BUILD_ROOT/%{_libdir}/cinnamon/libcinnamon.la

# Remove firefox plugin
rm -rf $RPM_BUILD_ROOT/%{_libdir}/mozilla

# Add autostart files for gnome-screensaver
%if 0%{?fedora} > 17
mkdir $RPM_BUILD_ROOT/%{_sysconfdir}/xdg/autostart/
install -pm 0644 %{SOURCE5} %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/
%endif

desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/cinnamon.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/cinnamon2d.desktop

desktop-file-install                                 \
 --add-category="Utility"                            \
 --remove-category="DesktopSettings"                 \
 --remove-key="Encoding"                             \
 --add-only-show-in="GNOME"                          \
 --delete-original                                   \
 --dir=$RPM_BUILD_ROOT%{_datadir}/applications       \
 $RPM_BUILD_ROOT%{_datadir}/applications/*


%find_lang %{name}

%postun
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files -f %{name}.lang
%doc COPYING README
%{_bindir}/cinnamon
%exclude %{_bindir}/cinnamon-launcher
%{_bindir}/cinnamon-extension-tool
%{_sysconfdir}/xdg/menus/cinnamon-applications.menu
%if 0%{?fedora} > 17
%{_sysconfdir}/xdg/autostart/cinnamon*-screensaver.desktop
%endif
%{_datadir}/desktop-directories/cinnamon-*.directory
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/applications/cinnamon.desktop
%{_datadir}/applications/cinnamon-add-panel-launcher.desktop
%{_datadir}/xsessions/cinnamon.desktop
%{_datadir}/gnome-session/sessions/cinnamon.session
%{_datadir}/cinnamon/
%{_datadir}/dbus-1/services/org.Cinnamon.HotplugSniffer.service
%{_libdir}/cinnamon/
%{_libexecdir}/cinnamon/cinnamon-perf-helper
%{_libexecdir}/cinnamon/cinnamon-hotplug-sniffer
%{_mandir}/man1/cinnamon.1.*
%{_mandir}/man1/cinnamon-extension-tool.1.*
%{_mandir}/man1/cinnamon-launcher.1.*
%{_mandir}/man1/gnome-session-cinnamon.1.*

%files settings
%{_sysconfdir}/xdg/menus/cinnamon-settings.menu
%{_bindir}/cinnamon-settings
%{_datadir}/cinnamon-settings/
%{_datadir}/applications/cinnamon-settings.desktop
%{_mandir}/man1/cinnamon-settings.1.*

%files menu-editor
%{_bindir}/cinnamon-menu-editor
%{_datadir}/cinnamon-menu-editor/
%{_datadir}/applications/cinnamon-menu-editor.desktop
%{_mandir}/man1/cinnamon-menu-editor.1.*

%files 2d
%{_bindir}/cinnamon2d
%{_bindir}/gnome-session-cinnamon2d
%{_datadir}/applications/cinnamon2d.desktop
%{_datadir}/gnome-session/sessions/cinnamon2d.session
%{_datadir}/xsessions/cinnamon2d.desktop
%{_mandir}/man1/gnome-session-cinnamon2d.1.*
%{_mandir}/man1/cinnamon2d.1.*


%changelog
* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 1.6.7-7
- Rebuilt for cogl soname bump

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 1.6.7-6
- Rebuilt for libgnome-desktop soname bump

* Mon Feb  4 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6.7-5
- Add patch that's been accepted upstream for pillow support

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.6.7-4
- Rebuild for new cogl

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 1.6.7-3
- Rebuilt for libgnome-desktop3 3.7.3 soname bump

* Wed Nov 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.7-2
- change requires on main package

* Wed Nov 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.7-1
- update to 1.6.7 release
- split menu setting, settings and 2d into sub-packages

* Wed Nov 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.6-3
- drop requires libgnomekbd (rhbz 874218)
- fix error in datetime patch
- drop requires nemo and add to comps instead (rhbz 875197)

* Tue Nov 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.6-2
- add keyboard applet patch

* Sun Nov 11 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.6-1
- update to 1.6.6 release

* Wed Nov 07 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.4-2
- add requires gnome-panel (rhbz 872694)
- add requires libgnomekbd (rhbz 874218)

* Wed Oct 31 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.4-1
- update to 1.6.4 release
- change the default apps and panel launchers

* Sat Oct 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.3-1
- update to 1.6.3 release
- add license for cinnamon-menu-editor
- remove -OO from cinnamon-menu-editor script
- drop upstream patch

* Sat Oct 13 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.1-3
- autostart for gnome-screensaver so lock works
- mozilla desktop fix

* Tue Oct 09 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.1-2
- fix settings applet icons
- patch font size (Bzr 864050)

* Thu Sep 27 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.1-1
- update to 1.6.1 release

* Wed Sep 26 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-3
- remove requires nautilus and swap it for nemo
- drop nemo patch

* Tue Sep 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-2
- patch bluetooth applet

* Mon Sep 17 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-1
- update to 1.6.0 release
- drop upstream patches
- add requires python-imaging, gnome-python2-gconf and python-imaging
- patch to use nautilus instead of nemo

* Thu Aug 23 2012 Dan Horák <dan[at]danny.cz> - 1.5.2-6
- fix build without BlueTooth

* Fri Aug 17 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-5
- rebuilt for new cogl version
- patch bluetooth applet
- use patch to fix windows quick list applet
- patch for new cogl api

* Sun Aug 12 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-4
- Fix directory ownership

* Sun Jul 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-3
- Add requires nautilus for settings
- Remove fedora logo from package to enable generic spins

* Fri Jul 27 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-2
- patch systray applet

* Thu Jul 26 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-1
- update to 1.5.2 release

* Tue Jul 24 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-0.1.git49593cb
- Update to the latest snapshot
- Remove buildrequires telepathy-glib-devel, telepathy-logger-devel and folks-devel
- Drop obsolete patches
- Add buildrequires libsoup-devel libgnome-keyring-devel

* Sat Jul 21 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.10.git7959517
- Add requires accountsservice-libs

* Sat Jul 21 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.9.git7959517
- Add patch to port window settings to gsettings

* Fri Jul 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.8.git7959517
- filter provides and requires
- Remove requires dbus-x11
- Add -p to install

* Fri Jul 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.7.git7959517
- Remove %%define and rebase settings patch
- Hardcode version for patches
- Rearrange patches
- Use install rather than cp
- Fix scriptlets
- Remove hardcoded file name from %%prep
- Preserve timestamps in %%install
- Remove extension from manpage in %%files
- Add requires dbus-x11

* Fri Jul 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.6.git7959517
- Fix macro in comment rpmlint error

* Thu Jul 19 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.5.git7959517
- Correct spelling mistake
- Add descriptions for patches 

* Wed Jul 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.4.git7959517
- bump spec version to fix repo issue

* Wed Jul 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.3.git7959517
- bump spec version to fix repo issue

* Wed Jul 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.2.git7959517
- bump spec version to fix repo issue

* Wed Jul 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-0.1.git7959517
- Update to the latest snapshot

* Mon May 28 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.4.0-5.UP1
- Silence glib-compile-schemas scriplets
- fix firefox patch for f17
- fix power applet for f16

* Mon May 28 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.4.0-4.UP1
- add notification patch

* Mon May 28 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.4.0-3.UP1
- change %%define to %%global
- fix files listed twice in %%files section
- version patches
- remove %%config from files (gnome-shell and gnome-menus doesn't use them
  for the equivalent files)
- drop login theme patch

* Sun May 27 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.4.0-2.UP1
- add configure option so it compiles on F17
- fix release tag

* Sun May 27 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.4.0-1.UP1
- update to 1.4.0.UP1-1

* Wed Mar 14 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.4.0-2
- fix un-themed shutdown

* Tue Mar 13 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Mon Feb 20 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.3.1-1
- update to 1.3.1
- remove static lib
- remove mozilla plugin

* Fri Feb 17 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.3.0-1
- update to 1.3.0 release

* Mon Jan 22 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.2.0-1
- update to 1.2.0 release
- add build requires muffin-devel
- add Br libgudev1-devel
- add only-show-in=GNOME to settings desktop file
- make changes for source changes, applets, settings and session added
- delete session files and use my own
- move settings from lib to usr (it had no libs)
- replace menu icon
- change description

* Wed Jan 04 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.1.3-2
- add requires gnome-session
- clean up spec file ready for review

* Mon Jan 02 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.1.3-1
- update to version 1.1.3

* Sun Jan 01 2012 Leigh Scott <leigh123linux@fedoraproject.org> - 1.1.2-2
- fix firefox launchers

* Fri Dec 30 2011 Leigh Scott <leigh123linux@fedoraproject.org> - 1.1.2-1
- first build based on gnome-shell srpm
- add session files

