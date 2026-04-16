"""
Claude LLM engine
"""
import os
import json
from anthropic import Anthropic


class LLMEngine:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        self.client = Anthropic(api_key=api_key)

    def summarize_analysis(self, target: dict, scan_result: str, analysis: dict) -> str:
        prompt = {
            "target": {
                "name": target["name"],
                "cve": target["cve"],
                "url": target["url"],
            },
            "rule_analysis": analysis,
            "scan_excerpt": scan_result[:4000]
        }

        system_prompt = (
            "You are a defensive security analysis assistant. "
            "Summarize the scan findings for a controlled lab environment. "
            "Do not provide exploitation instructions. "
            "Focus on risk, evidence, and safe next-step validation."
        )

        response = self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=700,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this defensive validation data:\n\n{json.dumps(prompt, ensure_ascii=False, indent=2)}"
                }
            ]
        )

        parts = []
        for block in response.content:
            if getattr(block, "type", None) == "text":
                parts.append(block.text)
        return "\n".join(parts).strip()