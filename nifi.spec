%define debug_package %{nil}

Name:    nifi
Version: 1.13.2
Release: 1%{?dist}
Summary: NiFi an easy to use, powerful, and reliable system to process and distribute data
License: Apache License, Version 2.0
Group: Development/Tools/Other
URL:     http://nifi.apache.org/
Source0: https://archive.apache.org/dist/%{name}/%{version}/%{name}-%{version}-bin.tar.gz
Source1: %{name}.service
BuildArch: noarch

Buildroot: %{_tmppath}/%{name}-%{version}-root


Requires: systemd java-headless


%description

Put simply, NiFi was built to automate the flow of data between systems. While the term 'dataflow' is used in a variety of contexts, we use it here to mean the automated and managed flow of information between systems. This problem space has been around ever since enterprises had more than one system, where some of the systems created data and some of the systems consumed data.


%prep

%build
/bin/true

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
tar --strip-components=1 -C %{buildroot}%{_sharedstatedir}/%{name} -xvf %{SOURCE0}
ln -sf %{_sharedstatedir}/%{name}/conf/ %{_sysconfdir}/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# patch user
sed -i -e 's/run.as=.*/run.as=%{name}/' %{buildroot}%{_sharedstatedir}/%{name}/conf/bootstrap.conf

%clean
rm -rf %{buildroot}


%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
          -c "NIFI services" %{name}
exit 0

%post
%systemd_post %{name}.service
ln -sf %{_sharedstatedir}/%{name}/conf/ %{_sysconfdir}/%{name}

%preun
%systemd_preun %{name}.service

%postun
case "$1" in
  0)
    # This is an uninstallation.
    getent passwd %{name} >/dev/null && userdel %{name}
    getent group %{name} >/dev/null && groupdel %{name}
  ;;
  1)
    # This is an upgrade.
  ;;
esac
%systemd_postun_with_restart %{name}.service


%files
%defattr(-,root,root)
%dir %attr(-, %{name}, %{name}) %{_sharedstatedir}/%{name}
%dir %attr(-, %{name}, %{name}) %{_sysconfdir}/%{name}
%dir %attr(-, %{name}, %{name}) %{_localstatedir}/log/%{name}
%attr(-, %{name}, %{name}) %{_sharedstatedir}/%{name}/*
%config(noreplace) %attr(640, %{name}, %{name}) %{_sharedstatedir}/%{name}/conf/*
%attr(644, root, root) %{_unitdir}/%{name}.service





%changelog
* Wed Feb 16 2022 Okladin Dmitriy <sentoz66@gmail.com> - 1.13.2
- Update to 1.13.2

* Tue Feb 09 2021 Okladin Dmitriy <sentoz66@gmail.com> - 1.11.4
- initial build