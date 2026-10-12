
import html

GREEN = "#28a745"
RED = "#dc3545"


def esc(value):
    return html.escape(str(value))


def summary_html(extracted, skills):
    text = extracted.get("summary") or f"Professional with experience in {', '.join(skills[:5])}."
    paragraphs = "".join(
        f"<p>{esc(p.strip())}</p>" for p in text.split("\n\n") if p.strip()
    )
    return paragraphs or "<p>No summary provided.</p>"


def experience_html(entries):
    items = ""
    for exp in entries[:3]:
        if not isinstance(exp, dict):
            continue

        descriptions = exp.get("descriptions") or []
        if not descriptions and exp.get("description"):
            descriptions = [exp["description"]]
        bullets = "".join(f"<li>{esc(d)}</li>" for d in descriptions[:5] if d)

        items += f"""
            <div class="experience-item">
                <h3>{esc(exp.get("role", "Professional"))}</h3>
                <p class="company">{esc(exp.get("company", "Company"))} · {esc(exp.get("duration", "1 year"))}</p>
                <ul class="description-list">{bullets}</ul>
            </div>"""
    return items or "<p>No experience listed.</p>"


def generate_html_report(extracted, skills, classification):
    profile = classification.get("profile", "Unknown")
    accepted = classification.get("result") == "ACCEPTED"
    color = GREEN if accepted else RED

    if accepted:
        message = f"The normalized qualifications satisfy an accepted {esc(profile)} pattern."
    else:
        message = "The normalized qualifications do not satisfy any accepted profile pattern."

    # badges are glued together
    badges = "".join(f'<span class="skill-badge">{esc(s)}</span>' for s in skills)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ResumeLens - Candidate Profile</title>
    <style>
        :root {{ --purple: #667eea; --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f4f6f8;
            padding: 40px 20px;
            color: #333;
            line-height: 1.6;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            overflow: hidden;
        }}
        .header {{
            background: var(--gradient);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.8em; margin-bottom: 15px; font-weight: 600; }}
        .header p {{ opacity: 0.95; font-size: 1.1em; }}
        .content {{ padding: 40px; }}
        .section {{ margin-bottom: 35px; }}
        .section h2 {{
            color: var(--purple);
            border-bottom: 3px solid var(--purple);
            padding-bottom: 10px;
            margin-bottom: 20px;
            font-size: 1.5em;
            font-weight: 600;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        .info-item, .experience-item {{
            background: #f8f9fa;
            padding: 18px;
            border-radius: 10px;
            border-left: 4px solid var(--purple);
        }}
        .info-item strong {{
            color: var(--purple);
            display: block;
            font-size: 0.9em;
            text-transform: uppercase;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }}
        .summary-text {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            line-height: 1.8;
        }}
        .summary-text p {{ margin-bottom: 15px; }}
        .summary-text p:last-child {{ margin-bottom: 0; }}
        .experience-item {{ margin-bottom: 15px; }}
        .experience-item h3 {{ color: #333; margin-bottom: 8px; font-size: 1.2em; }}
        .company {{
            color: #666;
            font-size: 0.95em;
            margin-bottom: 12px;
            font-style: italic;
        }}
        .description-list {{ margin-left: 20px; color: #555; }}
        .description-list li {{ margin-bottom: 8px; }}
        .skills-container {{ display: flex; flex-wrap: wrap; }}
        .skill-badge {{
            display: inline-block;
            background: var(--gradient);
            color: white;
            padding: 8px 16px;
            font-size: 0.9em;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .evaluation {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            border-left: 5px solid {color};
        }}
        .evaluation p {{ margin-bottom: 12px; font-size: 1.05em; }}
        .evaluation .result {{
            font-size: 1.4em;
            font-weight: bold;
            color: {color};
            margin: 15px 0;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .footer {{
            text-align: center;
            padding: 25px;
            color: #999;
            font-size: 0.85em;
            border-top: 1px solid #e0e0e0;
            background: #f8f9fa;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{esc(extracted.get("name", "Unknown"))}</h1>
            <p>Candidate Profile generated by ResumeLens</p>
        </div>

        <div class="content">
            <div class="section">
                <h2>Personal Information</h2>
                <div class="info-grid">
                    <div class="info-item"><strong>Email:</strong>{esc(extracted.get("email") or "Unknown")}</div>
                    <div class="info-item"><strong>Location:</strong>{esc(extracted.get("location", "Unknown"))}</div>
                    <div class="info-item"><strong>Current role:</strong>{esc(profile)}</div>
                </div>
            </div>

            <div class="section">
                <h2>Profile Summary</h2>
                <div class="summary-text">{summary_html(extracted, skills)}</div>
            </div>

            <div class="section">
                <h2>Experience</h2>
                {experience_html(extracted.get("experience", []))}
            </div>

            <div class="section">
                <h2>Normalized Technical Skills</h2>
                <div class="skills-container">{badges}</div>
            </div>

            <div class="section">
                <h2>Qualification Evaluation</h2>
                <div class="evaluation">
                    <p><strong>Profile evaluated:</strong> {esc(profile)}</p>
                    <p class="result">Qualification pattern: {"ACCEPTED" if accepted else "REJECTED"}</p>
                    <p>{message}</p>
                </div>
            </div>
        </div>

        <div class="footer">
            Generated by ResumeLens · Formal Language-Based Resume Screening
        </div>
    </div>
</body>
</html>"""