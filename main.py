#!/usr/bin/env python3
"""
AIBB (AI BunkerBuster) - Main Controller
"""
import sys
import time
import json
from pathlib import Path

# Module imports
from modules.docker_manager import DockerManager
from modules.scanner import run_nmap_scan

class AIBB:
    def __init__(self):
        print("[*] AIBB (AI BunkerBuster) Initializing")
        self.docker_mgr = DockerManager()
        self.targets = []
        self.results = {}
        
    def run(self):
        """Main execution function"""
        print("\n" + "="*50)
        print("AIBB Automated Penetration Testing Started")
        print("="*50 + "\n")
        
        # 1. Load targets
        self.load_targets()
        
        # 2. Attack each target
        for target in self.targets:
            self.attack_target(target)
        
        # 3. Generate final report
        self.generate_report()
    
    def load_targets(self):
        """Load attack targets"""
        self.targets = [
            {
                "name": "shellshock",
                "cve": "CVE-2014-6271",
                "path": "./targets/shellshock",
                "port": 8080,
                "url": "http://localhost:8080"
            }
        ]
        print(f"[*] {len(self.targets)} target(s) loaded")
    
    def attack_target(self, target):
        """Attack individual target"""
        print(f"\n{'='*50}")
        print(f"[Target] {target['name']} ({target['cve']})")
        print(f"{'='*50}")
        
        # Step 1: Start Docker
        print(f"\n[Step 1] Starting Docker container")
        if not self.docker_mgr.start_container(target['path']):
            print("[ERROR] Failed to start Docker")
            return
        
        # Step 2: Run Scanner
        print(f"\n[Step 2] Port scanning")
        try:
            scan_result = run_nmap_scan("127.0.0.1", str(target['port']))
            print(f"[Scan Result]\n{scan_result}")
        except Exception as e:
            print(f"[ERROR] Scanner failed: {e}")
        
        # Step 3: LLM Attack
        print(f"\n[Step 3] AI attack started")
        print(f"[OK] Attack completed (temporary)")
        
        # Step 4: Docker cleanup
        print(f"\n[Step 4] Docker cleanup")
        self.docker_mgr.stop_container(target['path'])
        
        self.results[target['name']] = {
            "success": False,
            "flag": None
        }
    
    def generate_report(self):
        """Generate final report"""
        print("\n" + "="*50)
        print("[Report] Final Results")
        print("="*50)
        
        for name, result in self.results.items():
            status = "[SUCCESS]" if result['success'] else "[FAIL]"
            print(f"{name}: {status}")
            if result['flag']:
                print(f"  Flag: {result['flag']}")

def main():
    try:
        aibb = AIBB()
        aibb.run()
    except KeyboardInterrupt:
        print("\n\n[!] User interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
