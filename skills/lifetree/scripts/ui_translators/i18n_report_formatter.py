#!/usr/bin/env python3
"""
LifeTree Multi-Language i18n Report Formatter
Formats Advisor Briefs and Deep Research Reports in English, Simplified Chinese (zh-CN), or German (de-DE).
"""

import sys
import json
from typing import Dict, Any

I18N_DICTIONARY = {
    "zh-CN": {
        "title_advisor_brief": "持牌专业顾问审查简报",
        "disclaimer_header": "法律与专业免责声明",
        "fact_matrix": "客户事实与资质矩阵",
        "recommended_pathway": "推荐最优路径",
        "plan_b_hedge": "Plan B 风险对冲预案",
        "verdict": "推演结论"
    },
    "en": {
        "title_advisor_brief": "Brief for Licensed Professional Advisor",
        "disclaimer_header": "Legal & Professional Disclaimer",
        "fact_matrix": "Client Fact & Qualification Matrix",
        "recommended_pathway": "Recommended Optimal Pathway",
        "plan_b_hedge": "Plan B Risk Hedging Reserve",
        "verdict": "Deduction Verdict"
    },
    "de-DE": {
        "title_advisor_brief": "Briefing für zugelassene Fachberater / Rechtsanwälte",
        "disclaimer_header": "Rechtlicher & Professioneller Haftungsausschluss",
        "fact_matrix": "Mandanten-Fakten & Qualifikationsmatrix",
        "recommended_pathway": "Empfohlener optimaler Pfad",
        "plan_b_hedge": "Plan B Risikoabsicherung",
        "verdict": "Bewertungsergebnis"
    }
}

def format_i18n_report_headers(lang: str = "en") -> Dict[str, str]:
    target_lang = lang if lang in I18N_DICTIONARY else "en"
    return I18N_DICTIONARY[target_lang]

def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "zh-CN"
    res = format_i18n_report_headers(lang)
    print(json.dumps({"language": lang, "i18n_headers": res}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
