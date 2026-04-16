"""
Rule-based analysis engine
"""
from typing import Dict, Any


class AnalysisEngine:
    def analyze_scan_result(self, target: Dict[str, Any], scan_result: str) -> Dict[str, Any]:
        findings = []
        risk_level = "low"

        scan_lower = scan_result.lower()

        if "apache" in scan_lower:
            findings.append("Apache-related service string detected")

        if "cgi" in scan_lower:
            findings.append("CGI-related endpoint or indicator detected")
            risk_level = "medium"

        if "bash" in scan_lower or "shellshock" in scan_lower:
            findings.append("Potential Shellshock-related indicator detected")
            risk_level = "high"

        if "http" in scan_lower and "200" in scan_lower:
            findings.append("HTTP service responded successfully")

        return {
            "target_name": target["name"],
            "cve": target["cve"],
            "risk_level": risk_level,
            "findings": findings,
            "raw_length": len(scan_result),
            "recommendation": self._make_recommendation(risk_level, findings),
        }

    def _make_recommendation(self, risk_level: str, findings: list[str]) -> str:
        if risk_level == "high":
            return "Review the service configuration in the isolated lab and validate whether the indicators are reproducible."
        if risk_level == "medium":
            return "Perform additional defensive validation and confirm whether the exposed component is actually reachable."
        return "No strong indicator found from the current scan output. Continue with baseline verification."