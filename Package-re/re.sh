tcprewrite --infile=syslog.pcap --outfile=rsyslog.pcap --dstipmap=0.0.0.0/0:10.0.0.2 --enet-dmac=00:00:00:00:00:02
tcprewrite --infile=rsyslog.pcap --outfile=syslog.pcap.pcap --fixcsum
tcpreplay -i h1-eth0 -M 1000 syslog.pcap.pcap
