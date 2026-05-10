# 🛡️ ThreatPulse Bot

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/telegram-bot-26A5E4?style=for-the-badge&logo=telegram"/>
  <img src="https://img.shields.io/badge/deploy-Render%20%7C%20Railway-5364e9?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/sources-free%20APIs%20only-green?style=for-the-badge"/>
  <img src="https://img.shields.io/github/license/yourusername/threatpulse-bot?style=for-the-badge"/>
</p>

> **Personalized Threat Intelligence on Telegram** - stop reading 100 security blogs. Get only what matters to you.

---

## ✨ What it does

Instead of manually checking CISA, BleepingComputer, Krebs, and a dozen other sources, ThreatPulse monitors them all and sends you a Telegram message **only when something matches your profile**.

You define:
-  **Attack types** you care about (Ransomware, Phishing, APT, Zero-day, …)
-  **Countries/regions** you cover (Israel, US, EU, Global, …)
-  **Platforms** you protect (Windows, Linux, Android, iOS, …)
-  **Sources to block** (exclude any source you already follow elsewhere)

---

## User Experience

The onboarding is fully interactive - no commands to memorize:

```
/start
  → Step 1: Choose attack types  (multi-select toggle buttons)
  → Step 2: Choose countries      (multi-select toggle buttons)
  → Step 3: Choose OS/platforms (multi-select toggle buttons)
  → Step 4: Block sources         (exclude what you don't want)
  → Done - alerts start arriving
```

---

## Free Data Sources (no paid API needed)

| Source | Type | Focus |
|--------|------|-------|
| CISA Advisories | RSS | US gov, ICS, critical infra |
| Krebs on Security | RSS | Deep-dive investigations |
| BleepingComputer | RSS | Breaking news |
| Threatpost | RSS | Vulnerabilities, exploits |
| CrowdStrike Blog | RSS | APT, nation-state |
| SANS ISC Stormcast | RSS | Daily briefings |
| NVD (NIST) | RSS | New CVE publications |
| AlienVault OTX | API (free) | Threat pulses, IOCs |
| Exploit-DB | RSS | Public exploits, PoC |
| CERT-IL | RSS | Israel-specific advisories |

All sources are **100% free** - no paid API keys required.

---

## Quick Start

```bash
git clone https://github.com/yourusername/threatpulse-bot.git
cd threatpulse-bot
cp .env .env
# Add your TELEGRAM_BOT_TOKEN to .env
pip install -r requirements.txt
python src/main.py
```

Get your token from [@BotFather](https://t.me/BotFather) → `/newbot`.

---

## Deploy to Render (free, always-on)

1. Push to GitHub
2. [render.com](https://render.com) → **New** → **Blueprint** → connect repo
3. Set `TELEGRAM_BOT_TOKEN` in Environment Variables
4. Deploy

---

## Project Structure

```
threatpulse-bot/
├── src/
│   ├── main.py
│   ├── handlers/
│   │   ├── onboarding.py   ← 4-step guided setup with inline buttons
│   │   ├── settings.py     ← /settings command
│   │   └── status.py       ← /status command
│   ├── modules/
│   │   ├── poller.py       ← fetch → filter → send engine
│   │   └── scheduler.py    ← background APScheduler job
│   └── utils/
│       ├── data.py         ← sources, keywords, attack/OS maps
│       ├── storage.py      ← JSON persistence (profiles + seen)
│       ├── formatters.py   ← Telegram HTML message builder
│       └── config.py       ← env config loader
├── .env.example
├── Dockerfile
├── render.yaml
└── requirements.txt
```

---

## 🤝 Contributing

Ideas welcome:
- [ ] Digest mode - daily/weekly summary instead of real-time
- [ ] Severity scoring per article
- [ ] MITRE ATT&CK technique tagging
- [ ] Slack / Discord webhook support

---

## 📄 License

MIT © [Sivan Shamir](https://github.com/Sivan498)

<p align="center">Built for the security community 🛡️</p>
