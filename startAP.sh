#Impostare l IP della interfaccia
ifconfig wlan1 10.0.0.1 netmask 255.255.255.0

#iniziare il servizio per l access point e il DHCP
hostapd APConf/hostapd.conf & dnsmasq -C APConf/dnsmasq.conf -d
