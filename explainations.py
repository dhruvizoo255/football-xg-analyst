def explain_xg(xg):

    if xg < 0.10:
        quality = "Low-quality chance"

    elif xg < 0.30:
        quality = "Decent opportunity"

    elif xg < 0.60:
        quality = "High-quality chance"

    else:
        quality = "Clear-cut opportunity"

    explanation = f"""
Expected Goals (xG): {xg:.3f}

Chance Quality:
{quality}

Historically, shots with similar
characteristics are converted
approximately {xg*100:.1f}%
of the time.
"""

    return explanation