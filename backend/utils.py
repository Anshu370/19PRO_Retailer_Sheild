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
