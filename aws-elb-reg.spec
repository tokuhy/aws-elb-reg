Summary: AWS EC2 instances are added to or deleted from ELB, automatically.
Name: aws-elb-reg
Version: 1.0.0
Release: 1%{?dist2:.%{dist2}}
License: Apache License, Version 2.0
URL: http://github.com/tokuhy/aws-elb-reg
Source0: %{name}-%{version}.tar.gz
Group: Applications/System
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)
Requires: python >= 2.6

%description
When the EC2 instance start/stop, run the registration/deregistration to ELB
automatically based on the tag information of an instance.

%prep
%setup -q

%build

%install
%{__rm} -rf %{buildroot}

%{__install} -Dp -m0755 %{name}.py \
                        %{buildroot}%{_sbindir}/%{name}
%{__install} -Dp -m0755 %{name}.init \
                        %{buildroot}%{_initrddir}/%{name}
%{__install} -Dp -m0600 %{name}.sysconf \
                        %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
  /sbin/chkconfig --del %{name}
fi

%files
%defattr(-, root, root, 0644)
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0600, root, root) %{_sysconfdir}/sysconfig/%{name}
%attr(0755, root, root) %{_initrddir}/%{name}
%attr(0755, root, root) %{_sbindir}/%{name}
%doc LICENSE README.md

%changelog
* Fri Oct 25 2013 Fumiaki Tokuyama <tokuhy@gmail.com>
- Version 1.0.0-1
