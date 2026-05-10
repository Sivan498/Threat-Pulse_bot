"""
Static data: attack types, countries, OS options, and free RSS/API sources.
All sources here are 100% free — no API key required (NVD key optional).
"""

# ── Attack types ────────────────────────────────────────────────────────────
ATTACK_TYPES = [
    {"id": "ransomware",   "label": "🔒 Ransomware"},
    {"id": "phishing",     "label": "🎣 Phishing"},
    {"id": "apt",          "label": "🕵️ APT / Nation-state"},
    {"id": "zeroday",      "label": "💣 Zero-day"},
    {"id": "ddos",         "label": "🌊 DDoS"},
    {"id": "malware",      "label": "🦠 Malware"},
    {"id": "supply_chain", "label": "⛓️ Supply Chain"},
    {"id": "cve",          "label": "📋 CVE / Vulnerability"},
    {"id": "data_breach",  "label": "💾 Data Breach"},
    {"id": "ics_scada",    "label": "🏭 ICS / SCADA"},
]

# ── Countries / regions ─────────────────────────────────────────────────────
COUNTRIES = [
    {"id": "IL",     "label": "🇮🇱 Israel"},
    {"id": "US",     "label": "🇺🇸 United States"},
    {"id": "EU",     "label": "🇪🇺 Europe"},
    {"id": "UK",     "label": "🇬🇧 United Kingdom"},
    {"id": "RU",     "label": "🇷🇺 Russia (threat actor)"},
    {"id": "CN",     "label": "🇨🇳 China (threat actor)"},
    {"id": "GLOBAL", "label": "🌍 Global"},
]

# ── Operating systems ────────────────────────────────────────────────────────
OS_TYPES = [
    {"id": "windows", "label": "🪟 Windows"},
    {"id": "linux",   "label": "🐧 Linux"},
    {"id": "android", "label": "🤖 Android"},
    {"id": "ios",     "label": "🍎 iOS / macOS"},
    {"id": "network", "label": "🔌 Network Devices"},
    {"id": "cloud",   "label": "☁️ Cloud / SaaS"},
]

# ── Free RSS / API sources ───────────────────────────────────────────────────
# All free, no API key required unless noted.
SOURCES = [
    {
        "id": "cisa",
        "name": "CISA Advisories",
        "url": "https://www.cisa.gov/uscert/ncas/alerts.xml",
        "type": "rss",
        "countries": ["US", "GLOBAL"],
        "attack_types": ["cve", "apt", "ics_scada"],
        "os": [],
    },
    {
        "id": "krebs",
        "name": "Krebs on Security",
        "url": "https://krebsonsecurity.com/feed/",
        "type": "rss",
        "countries": ["US", "GLOBAL"],
        "attack_types": ["ransomware", "phishing", "data_breach", "cve"],
        "os": ["windows"],
    },
    {
        "id": "bleepingcomputer",
        "name": "BleepingComputer",
        "url": "https://www.bleepingcomputer.com/feed/",
        "type": "rss",
        "countries": ["GLOBAL"],
        "attack_types": ["ransomware", "malware", "cve", "zeroday", "data_breach"],
        "os": ["windows", "android", "ios"],
    },
    {
        "id": "threatpost",
        "name": "Threatpost",
        "url": "https://threatpost.com/feed/",
        "type": "rss",
        "countries": ["GLOBAL"],
        "attack_types": ["cve", "zeroday", "apt", "malware"],
        "os": [],
    },
    {
        "id": "crowdstrike",
        "name": "CrowdStrike Blog",
        "url": "https://www.crowdstrike.com/blog/feed",
        "type": "rss",
        "countries": ["GLOBAL"],
        "attack_types": ["apt", "ransomware", "malware"],
        "os": ["windows", "linux"],
    },
    {
        "id": "sans",
        "name": "SANS Internet Stormcast",
        "url": "https://isc.sans.edu/rssfeed_full.xml",
        "type": "rss",
        "countries": ["GLOBAL"],
        "attack_types": ["cve", "malware", "zeroday"],
        "os": [],
    },
    {
        "id": "nvd",
        "name": "NVD (NIST) — New CVEs",
        "url": "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss.xml",
        "type": "rss",
        "countries": ["GLOBAL"],
        "attack_types": ["cve", "zeroday"],
        "os": [],
    },
    {
        "id": "otx",
        "name": "AlienVault OTX Pulses",
        "url": "https://otx.alienvault.com/api/v1/pulses/subscribed",
        "type": "api_otx",   # uses OTX free API (no key needed for public pulses)
        "countries": ["GLOBAL"],
        "attack_types": ["apt", "malware", "phishing", "ransomware"],
        "os": [],
    },
    {
        "id": "exploit_db",
        "name": "Exploit-DB RSS",
        "url": "https://www.exploit-db.com/rss.xml",
        "type": "rss",
        "countries": ["GLOBAL"],
        "attack_types": ["cve", "zeroday"],
        "os": [],
    },
    {
        "id": "cert_il",
        "name": "CERT-IL (Israel)",
        "url": "https://www.gov.il/he/Departments/publications/reports/cert-reports",
        "type": "rss_scrape",  # scrape-based, best effort
        "countries": ["IL"],
        "attack_types": ["cve", "apt", "ransomware"],
        "os": [],
    },
]

# keyword map: attack_type_id → keywords to look for in RSS text
ATTACK_KEYWORDS = {
    "ransomware":   ["ransomware", "ransom", "encrypt", "lockbit", "blackcat", "cl0p"],
    "phishing":     ["phishing", "spear-phish", "credential", "smishing", "vishing"],
    "apt":          ["apt", "nation-state", "advanced persistent", "espionage", "TA", "lazarus", "cozy bear"],
    "zeroday":      ["zero-day", "0-day", "zeroday", "zero day", "in the wild"],
    "ddos":         ["ddos", "denial of service", "botnet flood"],
    "malware":      ["malware", "trojan", "backdoor", "rat ", "infostealer", "worm"],
    "supply_chain": ["supply chain", "solarwinds", "dependency confusion", "typosquatting"],
    "cve":          ["cve-", "vulnerability", "patch tuesday", "exploit", "poc", "proof-of-concept"],
    "data_breach":  ["data breach", "leaked", "exposed database", "data leak", "dumped"],
    "ics_scada":    ["scada", "ics", "industrial", "plc", "ot security", "operational technology"],
}

OS_KEYWORDS = {
    "windows": ["windows", "win32", "active directory", "exchange server", "sharepoint"],
    "linux":   ["linux", "ubuntu", "debian", "rhel", "kernel", "bash"],
    "android": ["android", "apk", "google play"],
    "ios":     ["ios", "iphone", "ipad", "macos", "apple", "safari"],
    "network": ["cisco", "fortinet", "palo alto", "juniper", "router", "firewall", "vpn"],
    "cloud":   ["aws", "azure", "gcp", "kubernetes", "docker", "s3 bucket", "cloud"],
}
