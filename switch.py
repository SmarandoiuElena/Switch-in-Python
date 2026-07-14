#!/usr/bin/env python3

from scapy.all import sniff, sendp, Ether

tabela_mac = {}

interfete = ["sw-eth0", "sw-eth1", "sw-eth2"]

def proceseaza_pachet(pachet):
	if not pachet.haslayer(Ether):
		return

	mac_sursa = pachet[Ether].src
	mac_destinatie = pachet[Ether].dst
	interfata_intrare = pachet.sniffed_on

	if tabela_mac.get(mac_sursa) != interfata_intrare:
		print(f"{mac_sursa} - {interfata_intrare}")

	tabela_mac[mac_sursa] = interfata_intrare

	if mac_destinatie in tabela_mac:
		interfata_iesire = tabela_mac[mac_destinatie]

		if interfata_iesire != interfata_intrare:
			sendp(pachet, iface=interfata_iesire, verbose=False)
	else:
		for iface in interfete:
			if iface != interfata_intrare:
				sendp(pachet, iface=iface, verbose=False)

print("switch is running")
sniff(iface=interfete, prn = proceseaza_pachet, store=0, filter="inbound")