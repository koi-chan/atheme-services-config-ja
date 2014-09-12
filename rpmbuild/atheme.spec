Name:		atheme-services
Version:	7.1.0
Release:	2%{?dist}
Summary:	Atheme IRC Services

Group:		System Environment/Daemons
License:	UnKnown
URL:		http://www.atheme.net/atheme.html
Source0:	http://www.atheme.net/downloads/atheme-services-7.1.0.tar.bz2
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	pcre-devel
BuildRequires:	openssl-devel
#Requires:	

%description
Atheme is a set of services for IRC networks designed for large IRC networks with high scalability requirements. It is relatively mature software, with some code and design derived from another package called Shrike.

%prep
%setup -q


%build
%configure \
	--sysconfdir=%{_sysconfdir}/atheme \
	--enable-fhs-paths \
	--enable-contrib \
	--without-ldap \
	--with-pcre

make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_initddir}
cp %{_sourcedir}/initscript %{buildroot}%{_initddir}/atheme-services
mkdir -p %{buildroot}/etc/sysconfig
cp %{_sourcedir}/sysconfig %{buildroot}/etc/sysconfig/atheme-services


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_prefix}
/var
%{_sysconfdir}
%doc


%changelog
* Fri Sep 12 2014 koi-chan <koi-chan@mail.kazagakure.net> 7.1.0-2
- change initscript. use var:OPTIONS in sysconfig directory.
- added "/etc/sysconfig/atheme-services". 
* Tue Sep 09 2014 koi-chan <koi-chan@mail.kazagakure.net> 7.1.0-1
- first release
