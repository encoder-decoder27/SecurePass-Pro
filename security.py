
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
if __name__ == "__main__":
    test_password = "AnUjA_#$"
    result = analyze_password(test_password)

    print("SecurePass Pro Test")
    print("Score:", result["score"])
    print("Strength:", result["strength"])
    print("Estimated entropy:", result["entropy"])
    print("Findings:", result["findings"])
    print("Recommendations:", result["recommendations"])

    import secrets
import string


def generate_password(length=16, use_symbols=True):
    if length < 12:
        raise ValueError("Password length must be at least 12.")

    alphabet = string.ascii_letters + string.digits

    if use_symbols:
        alphabet += "!@#$%^&*()-_=+"

    characters = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
    ]

    if use_symbols:
        characters.append(secrets.choice("!@#$%^&*()-_=+"))

    characters.extend(
        secrets.choice(alphabet)
        for _ in range(length - len(characters))
    )

    secrets.SystemRandom().shuffle(characters)

    return "".join(characters)