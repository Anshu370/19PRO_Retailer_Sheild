from virustotal import scan_url_virustotal

async def scan_and_parse(link: str):
    try:
        scan_result = await scan_url_virustotal(link)
        stats = scan_result["data"]["attributes"]["stats"]
        return {
            "link": link,
            "harmless": stats.get("harmless", 0),
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "timeout": stats.get("timeout", 0),
            "undetected": stats.get("undetected", 0)
        }
    except Exception as e:
        print(f"⚠️ Failed to parse VirusTotal response for {link}: {e}")
        return {
            "link": link,
            "harmless": "error",
            "malicious": "error",
            "suspicious": "error",
            "timeout": "error",
            "undetected": "error"
        }


# Security Score Calculation Function
def compute_security_score(vt_records, nlp_result: dict) -> dict:
    malicious_links = 0
    suspicious_links = 0

    for record in vt_records:
        stats = record.get("data", {}).get("attributes", {}).get("stats", {})
        malicious_links += stats.get("malicious", 0)
        suspicious_links += stats.get("suspicious", 0)

    total_flags = malicious_links + suspicious_links

    # Scale: total_flags gets 60% weight, NLP gets 40%
    link_score = max(0, 100 - total_flags * 10)  # lose 10 points per flag
    nlp_score = int((1 - nlp_result.get("phishing_probability", 0)) * 100)

    total_score = int(0.6 * link_score + 0.4 * nlp_score)

    return {
        "malicious_links": malicious_links,
        "suspicious_links": suspicious_links,
        "link_score": link_score,
        "nlp_score": nlp_score,
        "total_score": total_score,
        "risk_level": (
            "High" if total_score < 50 else
            "Moderate" if total_score < 75 else
            "Low"
        )
    }