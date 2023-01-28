import airodor
import ipaddress

if __name__ == "__main__":
    mode = airodor.get_mode(
        ip_addr=ipaddress.ip_address("192.168.2.122"),
        group=airodor.VentilationGroup.A)
    print("stop")
