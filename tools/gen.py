#!/usr/bin/env python3
"""从 rules/*.list 重新生成 configs/*.conf（唯一数据源是 rules/）。

用法：
    python3 tools/gen.py

预设与 index.html 里的 PRESETS 保持一致；生成的 .conf 文本
与页面里同名勾选组合生成的文本逐字节相同。
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RULES_DIR = ROOT / "rules"
CONFIGS_DIR = ROOT / "configs"
REPO_URL = "https://github.com/openc2023/RocketRules"

# 组顺序与 index.html 的 ORDER 一致
ORDER = [
    "meta", "openai", "claude", "gemini", "grok", "youtube",
    "tiktok", "telegram", "x", "discord", "netflix", "ip",
]

LABELS = {
    "meta": "Meta 全家桶",
    "openai": "ChatGPT / OpenAI",
    "claude": "Claude",
    "gemini": "Gemini",
    "grok": "Grok / xAI",
    "youtube": "YouTube",
    "tiktok": "TikTok",
    "telegram": "Telegram",
    "x": "X / Twitter",
    "discord": "Discord",
    "netflix": "Netflix",
    "ip": "IP 测试网站",
}

PRESETS = {
    "meta-only.conf": ["meta", "ip"],
    "ai-only.conf": ["openai", "claude", "gemini", "grok", "ip"],
    "social-only.conf": ["meta", "tiktok", "telegram", "x", "discord", "ip"],
    "combined.conf": ORDER,
}


def load_rules():
    groups = {}
    for key in ORDER:
        domains = []
        for line in (RULES_DIR / f"{key}.list").read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            kind, _, domain = line.partition(",")
            if kind != "DOMAIN-SUFFIX" or not domain or "," in domain:
                raise ValueError(f"rules/{key}.list 格式不对：{line!r}")
            domains.append(domain)
        if not domains:
            raise ValueError(f"rules/{key}.list 是空的")
        groups[key] = domains
    return groups


def build_config(groups, selected):
    lines = [
        "# RocketRules generated config",
        "# Selected: " + ", ".join(selected),
        "# " + REPO_URL,
        "[General]",
        "bypass-system = true",
        "skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, 127.0.0.1, localhost",
        "dns-server = system",
        "",
        "[Rule]",
    ]
    seen = set()
    for key in ORDER:
        if key not in selected:
            continue
        lines.append("# " + LABELS[key])
        for domain in groups[key]:
            if domain in seen:
                continue
            seen.add(domain)
            lines.append(f"DOMAIN-SUFFIX,{domain},PROXY")
    lines.append("FINAL,DIRECT")
    return "\n".join(lines) + "\n"


def main():
    groups = load_rules()
    total = sum(len(v) for v in groups.values())
    print(f"规则组 {len(groups)} 个，域名共 {total} 个")
    CONFIGS_DIR.mkdir(exist_ok=True)
    for filename, selected in PRESETS.items():
        text = build_config(groups, selected)
        (CONFIGS_DIR / filename).write_text(text)
        rules = sum(len(groups[k]) for k in selected)
        print(f"  {filename}: {len(selected)} 组，{rules} 条规则")
    print("完成")


if __name__ == "__main__":
    main()
