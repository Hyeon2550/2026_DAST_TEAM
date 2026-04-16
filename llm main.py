#!/usr/bin/env python3
"""
AIBB - Defensive Validation Controller
"""
import sys
from modules.docker_manager import DockerManager
from modules.scanner import execute_full_scan
from modules.analysis_engine import AnalysisEngine
from modules.llm_engine import LLMEngine
from modules.reporter import Reporter


class AIBB:
    def __init__(self):
        print("[*] AIBB Initializing")
        self.docker_mgr = DockerManager()
        self.analysis_engine = AnalysisEngine()
        self.llm_engine = LLMEngine()
        self.reporter = Reporter()
        self.targets = []
        self.results = {}

    def run(self):
        print("\n" + "=" * 60)
        print("AIBB Defensive Analysis Started")
        print("=" * 60 + "\n")

        self.load_targets()

        for target in self.targets:
            self.analyze_target(target)

        self.generate_report()

    def load_targets(self):
        self.targets = [
            {
                "name": "shellshock-lab",
                "cve": "CVE-2014-6271",
                "path": "./targets/shellshock",
                "port": 8080,
                "url": "http://localhost:8080",
                "notes": "Controlled lab target for defensive validation"
            }
        ]
        print(f"[*] {len(self.targets)} target(s) loaded")

    def analyze_target(self, target):
        print(f"\n{'=' * 60}")
        print(f"[Target] {target['name']} ({target['cve']})")
        print(f"{'=' * 60}")

        started = False
        try:
            print("\n[Step 1] Starting Docker container")
            started = self.docker_mgr.start_container(target["path"])
            if not started:
                print("[ERROR] Failed to start Docker container")
                self.results[target["name"]] = {"status": "error", "reason": "docker_start_failed"}
                return

            print("\n[Step 2] Running scanner")
            scan_result = execute_full_scan("127.0.0.1", target["port"])
            print("[OK] Scan completed")

            print("\n[Step 3] Rule-based analysis")
            rule_analysis = self.analysis_engine.analyze_scan_result(
                target=target,
                scan_result=scan_result
            )

            print("\n[Step 4] Claude summary")
            llm_summary = self.llm_engine.summarize_analysis(
                target=target,
                scan_result=scan_result,
                analysis=rule_analysis
            )

            self.results[target["name"]] = {
                "status": "completed",
                "target": target,
                "scan_result": scan_result,
                "rule_analysis": rule_analysis,
                "llm_summary": llm_summary,
            }

        except Exception as e:
            self.results[target["name"]] = {
                "status": "error",
                "target": target,
                "reason": str(e)
            }
            print(f"[ERROR] {e}")

        finally:
            if started:
                print("\n[Step 5] Docker cleanup")
                self.docker_mgr.stop_container(target["path"])

    def generate_report(self):
        print("\n" + "=" * 60)
        print("[Report] Final Results")
        print("=" * 60)

        report_text = self.reporter.build_text_report(self.results)
        print(report_text)


def main():
    try:
        app = AIBB()
        app.run()
    except KeyboardInterrupt:
        print("\n[!] User interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()