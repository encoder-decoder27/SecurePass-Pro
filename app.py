import json
from datetime import datetime, timezone

import streamlit as st
from security import analyze_password, generate_password

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="SecurePass Pro | Security Center",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# THEME / CSS
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --bg: #080D18;
        --panel: #111A2B;
        --panel-2: #152239;
        --border: #263852;
        --muted: #91A5C4;
        --text: #ECF4FF;
        --cyan: #45D6F5;
        --blue: #3983FF;
        --green: #37D996;
        --amber: #F6BB54;
        --red: #FF667A;
    }

    .stApp {
        background:
            radial-gradient(circle at 85% 0%, rgba(39, 105, 190, .15), transparent 28%),
            linear-gradient(145deg, #080D18 0%, #0B1220 55%, #0A1424 100%);
        color: var(--text);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 1.7rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: #0C1423;
        border-right: 1px solid #1D2B40;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 18px 0;
    }

    .brand-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 46px;
        height: 46px;
        border-radius: 14px;
        background: linear-gradient(135deg, #1B72D8, #38D8EE);
        box-shadow: 0 8px 26px rgba(37, 137, 235, .2);
        font-size: 25px;
    }

    .brand-name {
        color: #F4F8FF;
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -.3px;
    }

    .brand-sub {
        color: #8297B7;
        font-size: 11px;
        margin-top: 2px;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 30px 32px;
        border: 1px solid #294767;
        border-radius: 22px;
        background: linear-gradient(115deg, rgba(18, 39, 70, .98), rgba(17, 70, 105, .78));
        margin-bottom: 22px;
    }

    .hero:after {
        content: " ";
        position: absolute;
        width: 250px;
        height: 250px;
        right: -60px;
        top: -110px;
        border: 1px solid rgba(69, 214, 245, .2);
        border-radius: 50%;
        box-shadow: 0 0 0 28px rgba(69, 214, 245, .035),
                    0 0 0 58px rgba(69, 214, 245, .025);
        pointer-events: none;
    }

    .eyebrow {
        color: #70DFF6;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #FFFFFF;
        font-size: clamp(27px, 3vw, 38px);
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0 0 10px 0;
    }

    .hero-copy {
        color: #C0D3EA;
        max-width: 720px;
        font-size: 15px;
        line-height: 1.7;
        margin: 0;
    }

    .section-heading {
        color: #F1F6FF;
        font-size: 21px;
        font-weight: 750;
        margin: 22px 0 5px 0;
    }

    .section-copy {
        color: #8FA5C5;
        font-size: 13px;
        margin-bottom: 16px;
    }

    .metric-card {
        background: linear-gradient(145deg, #121E31, #101827);
        border: 1px solid #263A55;
        border-radius: 17px;
        padding: 19px 20px;
        min-height: 132px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, .10);
    }

    .metric-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #91A7C6;
        font-size: 12px;
        font-weight: 650;
        letter-spacing: .3px;
    }

    .metric-icon {
        width: 31px;
        height: 31px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 9px;
        background: #1A2E49;
        font-size: 16px;
    }

    .metric-number {
        color: #F4F8FF;
        font-size: 29px;
        font-weight: 800;
        margin-top: 12px;
        line-height: 1.15;
    }

    .metric-foot {
        color: #8298B8;
        font-size: 11px;
        margin-top: 7px;
    }

    .scan-row {
        display: flex;
        align-items: center;
        gap: 13px;
        padding: 15px 16px;
        margin: 10px 0;
        border-radius: 13px;
        border: 1px solid rgba(255,255,255,.055);
    }

    .scan-icon {
        width: 38px;
        height: 38px;
        flex: 0 0 38px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 11px;
        font-size: 18px;
    }

    .scan-name {
        color: #F4F7FD;
        font-size: 14px;
        font-weight: 750;
    }

    .scan-message {
        color: #A3B4CD;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 4px;
    }

    .scan-status {
        font-size: 11px;
        font-weight: 850;
        letter-spacing: .8px;
        white-space: nowrap;
    }

    .info-panel {
        background: #111C2E;
        border: 1px solid #273A54;
        border-radius: 16px;
        padding: 19px;
    }

    .small-label {
        color: #8FA5C5;
        font-size: 12px;
        font-weight: 650;
    }

    .recommendation {
        color: #D6E3F5;
        font-size: 13px;
        line-height: 1.55;
        padding: 10px 0;
        border-bottom: 1px solid #223149;
    }

    .recommendation:last-child {
        border-bottom: none;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border: 1px solid #3D83F6;
        border-radius: 11px;
        min-height: 44px;
        background: linear-gradient(100deg, #2269D8, #347FF0);
        color: #FFFFFF;
        font-weight: 750;
        transition: all .15s ease;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        border-color: #60B9FF;
        background: linear-gradient(100deg, #2B79EB, #4192FF);
        color: #FFFFFF;
    }

    div[data-testid="stDownloadButton"] > button {
        border-radius: 10px;
        min-height: 42px;
        font-weight: 700;
    }

    div[data-testid="stTextInput"] input {
        background: #111A2B;
        border: 1px solid #2A3D58;
        border-radius: 10px;
        color: #F3F7FF;
    }

    div[data-testid="stProgress"] > div {
        background: #1B2A40;
        border-radius: 20px;
    }

    div[data-testid="stProgress"] div[role="progressbar"] {
        background: linear-gradient(90deg, #347CF4, #45D6F5);
        border-radius: 20px;
    }

    div[data-testid="stMetric"] {
        background: #111C2E;
        border: 1px solid #263A55;
        padding: 13px 15px;
        border-radius: 12px;
    }

    hr {
        border-color: #24334A !important;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🔐</div>
            <div>
                <div class="brand-name">SecurePass Pro</div>
                <div class="brand-sub">SECURITY COMMAND CENTER</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠  Dashboard",
            "🔍  Password Audit",
            "🔑  Password Generator",
            "📊  Security Analytics",
            "ℹ️  About",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.markdown("**SYSTEM STATUS**")
    st.markdown(
        """
        <div style="color:#37D996;font-size:13px;font-weight:700;">
            ● Local analysis enabled
        </div>
        <div style="color:#8297B7;font-size:11px;margin-top:6px;line-height:1.5;">
            Passwords are analyzed by this app and are not included in reports.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("Educational project • Use test passwords only")

# Shared session state: keep non-sensitive audit results, never the password.
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "last_checks" not in st.session_state:
    st.session_state.last_checks = []
if "last_findings" not in st.session_state:
    st.session_state.last_findings = []
if "last_recommendations" not in st.session_state:
    st.session_state.last_recommendations = []
if "last_generated_password" not in st.session_state:
    st.session_state.last_generated_password = None


def hero(title, subtitle, eyebrow="SECURITY CENTER"):
    st.markdown(
        f"""
        <div class="hero">
            <div class="eyebrow">{eyebrow}</div>
            <div class="hero-title">{title}</div>
            <p class="hero-copy">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label, value, foot, icon):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-top">
                <span>{label}</span>
                <span class="metric-icon">{icon}</span>
            </div>
            <div class="metric-number">{value}</div>
            <div class="metric-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_scanner(checks):
    if not checks:
        st.info(
            "The backend did not return individual checks. "
            "Add a 'checks' list to analyze_password() in security.py."
        )
        return

    for check in checks:
        status = str(check.get("status", "WARNING")).upper()
        name = str(check.get("name", "Security check"))
        message = str(check.get("message", "No details available."))

        if status == "PASS":
            icon, color, bg, label = "✓", "#37D996", "#102C26", "PASS"
        elif status == "FAIL":
            icon, color, bg, label = "×", "#FF667A", "#351B27", "FAIL"
        else:
            icon, color, bg, label = "!", "#F6BB54", "#342A19", "WARNING"

        st.markdown(
            f"""
            <div class="scan-row" style="background:{bg};border-left:4px solid {color};">
                <div class="scan-icon" style="background:{color}18;color:{color};">{icon}</div>
                <div style="flex:1;min-width:0;">
                    <div class="scan-name">{name}</div>
                    <div class="scan-message">{message}</div>
                </div>
                <div class="scan-status" style="color:{color};">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def analyze_and_save(password):
    """Analyze in memory; deliberately do not save the password."""
    result = analyze_password(password)
    score = max(0, min(100, int(result.get("score", 0))))
    strength = str(result.get("strength", "Unknown"))
    entropy = result.get("entropy", 0)
    checks = result.get("checks", [])
    findings = result.get("findings", [])
    recommendations = result.get("recommendations", [])

    if score >= 75:
        risk = "LOW"
    elif score >= 50:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    report = {
        "tool": "SecurePass Pro",
        "audit_date_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "strength_score": score,
        "strength": strength,
        "estimated_risk": risk,
        "estimated_entropy_bits": entropy,
        "security_checks": checks,
        "findings": findings,
        "recommendations": recommendations,
        "note": "Heuristic estimates only. The analyzed password is deliberately excluded.",
    }

    st.session_state.last_report = report
    st.session_state.last_checks = checks
    st.session_state.last_findings = findings
    st.session_state.last_recommendations = recommendations


# ---------------------------------------------------------
# DASHBOARD PAGE
# ---------------------------------------------------------
if page == "🏠  Dashboard":
    hero(
        "Your Password Security, <span style='color:#45D6F5'>At a Glance</span>",
        "Audit password strength, inspect security rules, and create stronger passwords from one workspace.",
        "SECUREPASS PRO • OVERVIEW",
    )

    report = st.session_state.last_report
    if report:
        score_value = f"{report['strength_score']}/100"
        strength_value = report["strength"]
        risk_value = report["estimated_risk"]
        audit_foot = "Most recent audit score"
    else:
        score_value = "—"
        strength_value = "Not tested"
        risk_value = "Unknown"
        audit_foot = "Run an audit to populate this card"

    a, b, c, d = st.columns(4)
    with a:
        metric_card("LATEST SCORE", score_value, audit_foot, "◈")
    with b:
        metric_card("STRENGTH", strength_value, "Based on the latest audit", "⬡")
    with c:
        metric_card("RISK LEVEL", risk_value, "Heuristic assessment", "盾")
    with d:
        passed = sum(str(x.get("status", "")).upper() == "PASS" for x in st.session_state.last_checks)
        total = len(st.session_state.last_checks)
        metric_card("RULES PASSED", f"{passed}/{total}" if total else "—", "Individual policy checks", "✓")

    st.markdown('<div class="section-heading">Quick actions</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">Choose a tool to get started.</div>', unsafe_allow_html=True)

    q1, q2 = st.columns(2)
    with q1:
        with st.container(border=True):
            st.markdown("### 🔍 Password Audit")
            st.write("Score a test password and review rule-by-rule weaknesses.")
            if st.button("Open Password Audit →", key="go_audit", use_container_width=True):
                st.session_state["requested_page"] = "audit"
                st.rerun()
    with q2:
        with st.container(border=True):
            st.markdown("### 🔑 Password Generator")
            st.write("Create a high-entropy random password with customizable options.")
            if st.button("Open Password Generator →", key="go_generator", use_container_width=True):
                st.session_state["requested_page"] = "generator"
                st.rerun()

    # Reflect quick-action selection in sidebar on the next rerun.
    requested = st.session_state.pop("requested_page", None)
    if requested == "audit":
        st.info("Choose **Password Audit** in the sidebar to continue.")
    elif requested == "generator":
        st.info("Choose **Password Generator** in the sidebar to continue.")

    st.markdown('<div class="section-heading">Latest security checks</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-copy">The latest audit summary. No passwords are shown here.</div>', unsafe_allow_html=True)
    if st.session_state.last_checks:
        show_scanner(st.session_state.last_checks)
    else:
        st.info("No audit yet. Open Password Audit and analyze a test password to populate this area.")

# ---------------------------------------------------------
# PASSWORD AUDIT PAGE
# ---------------------------------------------------------
elif page == "🔍  Password Audit":
    hero(
        "Password Security Audit",
        "Analyze a test password, understand its estimated risk, and review each security rule.",
        "ANALYSIS MODULE",
    )

    with st.container(border=True):
        st.markdown("### Enter a test password")
        st.caption("Do not enter a password you use for a real account.")
        with st.form("audit_form", clear_on_submit=False):
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Type a test password...",
                help="Your password is not added to the downloadable report.",
            )
            submitted = st.form_submit_button("🔍 Run Security Audit", use_container_width=True)

    if submitted:
        if not password:
            st.warning("Please enter a test password first.")
        else:
            try:
                analyze_and_save(password)
                st.success("Analysis complete. Review your results below.")
            except Exception as exc:
                st.error("Analysis failed. Check security.py and installed dependencies.")
                st.caption(f"Technical detail: {exc}")

    report = st.session_state.last_report
    if report:
        st.markdown('<div class="section-heading">Assessment overview</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-copy">Scores and risk levels are estimates, not guarantees.</div>', unsafe_allow_html=True)

        score = report["strength_score"]
        score_color = "#37D996" if score >= 75 else "#F6BB54" if score >= 50 else "#FF667A"

        left, right = st.columns([1, 1.7], gap="large")
        with left:
            with st.container(border=True):
                st.markdown(
                    f"""
                    <div style="text-align:center;padding:15px 4px 8px;">
                        <div style="color:#91A5C4;font-size:12px;letter-spacing:1.5px;font-weight:800;">STRENGTH SCORE</div>
                        <div style="font-size:56px;line-height:1.2;font-weight:850;color:{score_color};margin:14px 0 8px;">{score}<span style="font-size:22px;color:#8195B3;">/100</span></div>
                        <div style="color:#D9E7F9;font-size:17px;font-weight:750;">{report['strength']}</div>
                        <div style="color:#91A5C4;font-size:12px;margin-top:8px;">Risk level: {report['estimated_risk']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.progress(score / 100)
        with right:
            st.markdown("#### 🛡️ Security Rules Scanner")
            show_scanner(report.get("security_checks", []))

        st.markdown('<div class="section-heading">Findings & recommendations</div>', unsafe_allow_html=True)
        fcol, rcol = st.columns(2, gap="large")
        with fcol:
            with st.container(border=True):
                st.markdown("#### 🔎 Findings")
                findings = report.get("findings", [])
                if findings:
                    for finding in findings:
                        st.markdown(f"- {finding}")
                else:
                    st.success("No findings were returned.")
        with rcol:
            with st.container(border=True):
                st.markdown("#### 💡 Recommendations")
                recommendations = report.get("recommendations", [])
                if recommendations:
                    for item in recommendations:
                        st.markdown(f"- {item}")
                else:
                    st.info("No recommendations were returned.")

        st.markdown('<div class="section-heading">Export audit report</div>', unsafe_allow_html=True)
        st.download_button(
            "⬇️ Download JSON Report",
            data=json.dumps(report, indent=2),
            file_name="securepass_audit_report.json",
            mime="application/json",
            use_container_width=True,
        )

# ---------------------------------------------------------
# PASSWORD GENERATOR PAGE
# ---------------------------------------------------------
elif page == "🔑  Password Generator":
    hero(
        "Secure Password Generator",
        "Create a randomized password using Python's cryptographically secure random generator.",
        "GENERATION MODULE",
    )

    with st.container(border=True):
        st.markdown("### Customize your password")
        length = st.slider("Password length", min_value=12, max_value=40, value=18, step=1)
        use_symbols = st.checkbox("Include symbols", value=True)

        if st.button("⚡ Generate Secure Password", use_container_width=True):
            try:
                st.session_state.last_generated_password = generate_password(
                    length=length,
                    use_symbols=use_symbols,
                )
            except Exception as exc:
                st.error("Password generation failed. Check security.py.")
                st.caption(f"Technical detail: {exc}")

    generated = st.session_state.last_generated_password
    if generated:
        st.markdown('<div class="section-heading">Your generated password</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.caption("Treat this password as a secret. Anyone who can see your screen may be able to read it.")
            st.code(generated, language=None)
            st.download_button(
                "⬇️ Download Password",
                data=generated,
                file_name="generated_password.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.warning("This demo does not save generated passwords to a database. Store passwords in a reputable password manager.")

# ---------------------------------------------------------
# SECURITY ANALYTICS PAGE
# ---------------------------------------------------------
elif page == "📊  Security Analytics":
    hero(
        "Security Analytics",
        "A quick breakdown of the latest audit's policy checks and risk estimate.",
        "ANALYTICS MODULE",
    )

    report = st.session_state.last_report
    checks = st.session_state.last_checks

    if not report:
        st.info("Run a password audit first. Analytics will summarize that audit only.")
    else:
        passed = sum(str(x.get("status", "")).upper() == "PASS" for x in checks)
        warnings = sum(str(x.get("status", "")).upper() == "WARNING" for x in checks)
        failed = sum(str(x.get("status", "")).upper() == "FAIL" for x in checks)

        a, b, c = st.columns(3)
        a.metric("Passed checks", passed)
        b.metric("Warnings", warnings)
        c.metric("Failed checks", failed)

        st.markdown("### Rule status breakdown")
        if checks:
            chart_data = {
                "Status": ["PASS", "WARNING", "FAIL"],
                "Count": [passed, warnings, failed],
            }
            st.bar_chart(chart_data, x="Status", y="Count", color="#39C8EB")
        else:
            st.info("No individual checks were returned by the backend.")

        st.markdown("### Latest audit")
        st.write(f"**Score:** {report['strength_score']}/100")
        st.write(f"**Strength:** {report['strength']}")
        st.write(f"**Estimated risk:** {report['estimated_risk']}")
        st.write(f"**Audit date:** {report['audit_date_utc']}")
        st.caption("This is the current session's latest audit, not a historical database.")

# ---------------------------------------------------------
# ABOUT PAGE
# ---------------------------------------------------------
elif page == "ℹ️  About":
    hero(
        "About SecurePass Pro",
        "An educational password security auditing project built with Python and Streamlit.",
        "PROJECT INFORMATION",
    )

    st.markdown("### What this tool does")
    st.markdown(
        """
        - Estimates password strength using the configured backend.
        - Displays individual policy checks when the backend provides them.
        - Offers practical recommendations.
        - Generates random passwords when `generate_password()` is available.
        - Exports audit metadata without including the analyzed password.
        """
    )

    st.markdown("### Important limitations")
    st.warning(
        "A strong score does not guarantee account security. This app does not verify "
        "whether a password has appeared in a data breach unless a breach-check feature "
        "is separately implemented and tested."
    )
    st.info(
        "Use test passwords only. The audit runs in the app process; this project is "
        "an educational demo, not a certified security product."
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()
st.caption("🔐 SecurePass Pro  •  Educational Cybersecurity Project  •  Use test passwords only")
