
from zxcvbn import zxcvbn


def analyze_password(password):
    if not password:
        return {
            "score": 0,
            "strength": "Not analyzed",
            "entropy": 0,
            "findings": ["Enter a password to begin."],
            "recommendations": ["Use a long, unique password."]
        }

    result = zxcvbn(password)
    score = result["score"]  # 0 to 4
    estimated_score = score * 25

    findings = []
    recommendations = []

    if len(password) < 12:
        findings.append("Password is shorter than 12 characters.")
        recommendations.append(
            "Use a longer password or passphrase."
        )

    if result.get("sequence"):
        findings.append("Predictable pattern or sequence detected.")
        recommendations.append(
            "Avoid predictable sequences and repeated patterns."
        )

    if result.get("guesses", 0) < 1000000:
        findings.append("Password may be relatively easy to guess.")
        recommendations.append(
            "Choose a more unique password."
        )

    if not findings:
        findings.append("No obvious weaknesses found by this assessment.")
        recommendations.append(
            "Use a unique password for every account."
        )

    labels = ["Very weak", "Weak", "Fair", "Strong", "Very strong"]

    # Entropy is an estimate derived from the guess count.
    import math
    entropy = math.log2(max(result.get("guesses", 1), 1))

    return {
        "score": estimated_score,
        "strength": labels[score],
        "entropy": round(entropy, 2),
        "findings": findings,
        "recommendations": recommendations
    }
