import nmap
import json
import subprocess

def run_nmap_scan(target_ip, port_range="1-1000"):
    print(f"[*] Nmap 스캔 시작: {target_ip} (포트: {port_range})")
    
    nm = nmap.PortScanner()
    
    try:
        nm.scan(target_ip, port_range, arguments='-sV -T4')
        
        scan_results = {
            "target_ip": target_ip,
            "host_status": "down",
            "open_ports": [],
            "error": None
        }
        
        for host in nm.all_hosts():
            scan_results["host_status"] = nm[host].state()
            
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                
                for port in ports:
                    port_data = nm[host][proto][port]
                    if port_data['state'] == 'open':
                        port_info = {
                            "port": port,
                            "protocol": proto,
                            "service_name": port_data['name'],
                            "version": port_data.get('version', 'unknown')
                        }
                        scan_results["open_ports"].append(port_info)
                        
        return json.dumps(scan_results, indent=4, ensure_ascii=False)
        
    except Exception as e:
        error_result = {"target_ip": target_ip, "error": str(e)}
        return json.dumps(error_result, indent=4, ensure_ascii=False)


# Nuclei는 나중에 구현

if __name__ == "__main__":
    test_target = "127.0.0.1" 
    
    print("=== AIBB Scanner Module Test ===")
    result = run_nmap_scan(test_target, "8080")
    print("\n[LLM 전달용 파싱 데이터]")
    print(result)
