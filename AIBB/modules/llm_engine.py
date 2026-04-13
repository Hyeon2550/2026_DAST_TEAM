import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("❌ ANTHROPIC_API_KEY가 .env에 없습니다!")
        
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
        self.conversation_history = []

    def analyze_result(self, command_output: str, cve_type: str) -> str:
        """공격 실행 결과를 분석하고 다음 단계를 제안합니다."""
        system_prompt = """You are a cybersecurity education assistant analyzing results 
        from a Vulhub CTF lab exercise. 
        Analyze the command output and determine:
        1. Was the attack successful?
        2. What was the result?
        3. What should be the next step?
        Be concise and educational."""

        user_message = f"""
        CVE: {cve_type}
        Command output: {command_output}
        
        Analyze this result and suggest next steps.
        """

        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history
        )

        assistant_message = response.content[0].text

        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def generate_report(self, attack_log: list) -> str:
        """전체 공격 과정을 분석해서 보고서를 생성합니다."""
        system_prompt = """You are a cybersecurity education assistant.
        Generate a concise penetration testing report based on the attack log.
        Include: summary, vulnerabilities found, commands used, results."""

        user_message = f"Generate a report for this attack log:\n{attack_log}"

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        return response.content[0].text

    def reset_history(self):
        """새로운 공격 세션 시작 시 히스토리 초기화"""
        self.conversation_history = []