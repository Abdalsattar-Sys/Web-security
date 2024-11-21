import socket
from datetime import datetime

class PortStatus:
    def __init__(self, port, status, protocol="TCP"):
        self.port = port
        self.status = status
        self.protocol = protocol

    def __str__(self):
        return f"Port {self.port} [{self.protocol}]: {'Open' if self.status else 'Closed'}"


class PortScanner:
    def __init__(self, target_ip, port_range=(1, 1024)):
        self.target_ip = target_ip
        self.port_range = port_range
        self.results = []

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)  # تعيين وقت الانتظار
                result = s.connect_ex((self.target_ip, port))  # فحص المنفذ
                status = result == 0
                self.results.append(PortStatus(port, status))
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

    def scan_range(self, start, end):
        print(f"Scanning {self.target_ip} from port {start} to {end}...")
        start_time = datetime.now()
        for port in range(start, end + 1):
            self.scan_port(port)
        end_time = datetime.now()
        print(f"Scan completed in {end_time - start_time}")

    def generate_report(self):
        print("\n--- Scan Report ---")
        for result in self.results:
            if result.status:  # عرض المنافذ المفتوحة فقط
                print(result)


if __name__ == "__main__":
    target = input("Enter target IP: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    scanner = PortScanner(target, (start_port, end_port))
    scanner.scan_range(start_port, end_port)
    scanner.generate_report()
