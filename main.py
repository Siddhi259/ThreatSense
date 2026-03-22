"""
main.py — ThreatSense
Emotion-Aware Social Engineering Attack Detection System
Run: python main.py
"""

from src.emotion_detector import detect_emotions
from src.risk_scorer import calculate_risk_score
from src.classifier import classify
from src.logger import log_analysis, get_stats


BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║   🛡  ThreatSense                                             ║
║   Emotion-Aware Social Engineering Attack Detection System    ║
║   Detecting threats through psychological manipulation        ║
╚═══════════════════════════════════════════════════════════════╝
"""


def analyze(message: str, save_log: bool = True, use_ml: bool = True) -> dict:
    """Full pipeline: message → emotion → score → classification → ML second opinion."""
    emotions   = detect_emotions(message)
    score_data = calculate_risk_score(emotions)
    result     = classify(score_data)
    result["emotions_detail"] = emotions
    result["ml"] = None

    if use_ml:
        try:
            from src.ml_model import predict as ml_predict
            result["ml"] = ml_predict(message)
        except FileNotFoundError:
            result["ml"] = {"ml_risk_level": "N/A", "ml_confidence": 0,
                            "agreement": None, "probabilities": {}}
        except Exception:
            pass

    if save_log:
        try:
            log_analysis(message, result)
        except Exception:
            pass
    return result


def print_report(message: str, result: dict):
    """Pretty-print the analysis report to console."""
    print("\n" + "─" * 65)
    print(f"📩 Message: {message[:80]}{'...' if len(message) > 80 else ''}")
    print("─" * 65)

    print(f"\n{result['label_emoji']} RISK LEVEL : {result['risk_level']}")
    print(f"📊 RISK SCORE: {result['total_score']}")

    print("\n🧠 Emotion Analysis:")
    for emotion, info in result["emotions_detail"].items():
        if info["detected"]:
            print(f"   ✔ {emotion.capitalize():10s} | matched: {info['matched']}")
        else:
            print(f"   ✗ {emotion.capitalize():10s} | not detected")

    print("\n📐 Score Breakdown:")
    for emotion, pts in result["breakdown"].items():
        bar = "█" * pts if pts > 0 else "-"
        print(f"   {emotion.capitalize():10s}: {pts:2d}  {bar}")

    print(f"\n💡 {result['explanation']}")
    print(f"🛡  Recommendation: {result['recommendation']}")

    ml = result.get("ml")
    if ml and ml.get("ml_risk_level") not in (None, "N/A"):
        conf_pct = int(ml["ml_confidence"] * 100)
        agree    = "✔ agrees" if ml["ml_risk_level"] == result["risk_level"] else "⚠ differs"
        print(f"\n🤖 ML Second Opinion : {ml['ml_risk_level']}  ({conf_pct}% confidence)  [{agree}]")

    print("─" * 65)


def run_demo():
    """Run built-in demo with sample test messages."""
    demo_messages = [
        "Your bank account is blocked. Act immediately or face legal action.",
        "Congratulations! You won a prize. Claim your free reward now!",
        "Meeting postponed to tomorrow. See you then.",
        "URGENT: Government has flagged your account for fraud. Respond now to avoid arrest.",
        "Hi, just checking in. Hope you are doing well.",
    ]
    print(BANNER)
    print("Running DEMO MODE with sample messages...\n")
    for msg in demo_messages:
        result = analyze(msg)
        print_report(msg, result)


def run_interactive():
    """Interactive mode: user types messages."""
    print(BANNER)
    print("Type a message to analyze. Type 'quit' to exit.\n")
    while True:
        message = input("Enter message: ").strip()
        if message.lower() in ("quit", "exit", "q"):
            print("Goodbye! Stay safe online. 🛡  — ThreatSense")
            break
        if not message:
            print("Please enter a message.\n")
            continue
        result = analyze(message)
        print_report(message, result)


if __name__ == "__main__":
    import sys
    from src.logger import get_history

    args = sys.argv[1:]

    if not args:
        run_interactive()

    elif args[0] == "--demo":
        run_demo()

    elif args[0] == "--stats":
        stats = get_stats()
        print(BANNER)
        print("📊 THREATSENSE — ANALYSIS STATISTICS")
        print("─" * 40)
        print(f"  Total scans     : {stats['total']}")
        print(f"  🔴 HIGH risk    : {stats['by_risk'].get('HIGH', 0)}")
        print(f"  🟡 MEDIUM risk  : {stats['by_risk'].get('MEDIUM', 0)}")
        print(f"  🟢 LOW risk     : {stats['by_risk'].get('LOW', 0)}")
        print(f"  Avg risk score  : {stats['avg_score']}")
        if stats["top_emotions"]:
            print(f"  Top emotion     : {stats['top_emotions'][0][0].capitalize()}")
        print("─" * 40)

    elif args[0] == "--history":
        n       = int(args[1]) if len(args) > 1 else 10
        history = get_history()[-n:]
        print(BANNER)
        print(f"📜 THREATSENSE — LAST {len(history)} ANALYSES\n")
        for e in history:
            emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(e["risk_level"], "⬜")
            print(f"  [{e['id']:03d}] {e['timestamp']}  {emoji} {e['risk_level']:6s}  "
                  f"Score:{e['risk_score']:3d}  {e['message'][:45]}...")

    elif args[0] == "--batch":
        if len(args) < 2:
            print("Usage: python main.py --batch <input.csv> [output_dir]")
            import sys; sys.exit(1)
        from src.batch_analyzer import process_csv, print_batch_report
        input_csv  = args[1]
        output_dir = args[2] if len(args) > 2 else "data"
        results, _ = process_csv(input_csv, output_dir)
        print_batch_report(results)

    elif args[0] == "--train":
        from src.ml_model import train
        print(BANNER)
        print("🤖 Training ThreatSense ML Model...\n")
        train(verbose=True)

    elif args[0] == "--evaluate":
        from src.ml_model import evaluate
        print(BANNER)
        evaluate(verbose=True)

    elif args[0] == "--report":
        msg = " ".join(args[1:]) if len(args) > 1 else input("Message to analyze: ")
        from src.report_generator import generate_single_report
        result = analyze(msg)
        print_report(msg, result)
        path = generate_single_report(msg, result)
        print(f"\n📄 ThreatSense HTML report saved → {path}")

    else:
        message = " ".join(args)
        result  = analyze(message)
        print_report(message, result)
