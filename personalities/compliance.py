#!/usr/bin/env python3
"""
Compliance Mode Personality - Auditor's Logic with Consultative Clarity
📊 Methodical, regulation-informed cybersecurity guidance.

Part of the PepeluGPT modular personality system.
"""

import random
from typing import Dict, Any, Optional
from datetime import datetime
from .base_personality import BasePersonality, PersonalityMode


class ComplianceMode(BasePersonality):
    """📊 Compliance Mode - Auditor's Logic with Consultative Clarity"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(PersonalityMode.COMPLIANCE)
        self.config = config or {}
        
        # Default control frameworks, can be overridden by config
        default_frameworks = [
            "NIST SP 800-53", "CNSSI-1253", "DoD 8500.01", 
            "ISO 27001", "SOC 2", "FedRAMP"
        ]
        
        behavior_config = self.config.get('behavior', {})
        self.control_frameworks = behavior_config.get('control_frameworks', default_frameworks)
    
    def get_greeting(self) -> str:
        """Generate Compliance mode greeting."""
        framework = random.choice(self.control_frameworks)
        return f"""
┌─────────────────────────────────────────────────────┐
│  📊 COMPLIANCE MODE ACTIVATED - Audit Ready        │
│                                                     │
│  Control Framework: {framework:<28} │
│  Risk Assessment: ACTIVE                            │
│  Documentation: STRUCTURED                          │
│                                                     │
│  ▣ Methodical analysis with risk vernacular        │
│  ▣ Tabular breakdowns and control citations        │
│  ▣ Audit-ready documentation format                │
└─────────────────────────────────────────────────────┘
"""
    
    def format_response(self, content: str, query: str = "", metadata: Optional[Dict[str, Any]] = None) -> str:
        """Format response with Compliance precision."""
        
        # Add compliance header
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"""📊 **COMPLIANCE ASSESSMENT REPORT**
**Generated:** {timestamp}
**Query Classification:** {self._classify_query(query)}
**Risk Level:** {self._assess_risk_level(content)}

---

"""
        
        # Add executive summary
        formatted += "## 🎯 Executive Summary\n\n"
        formatted += self._generate_executive_summary(content) + "\n\n"
        
        # Add detailed findings
        formatted += "## 📋 Detailed Findings\n\n"
        formatted += content + "\n\n"
        
        # Add control mapping
        formatted += "## 🔗 Control Framework Mapping\n\n"
        formatted += self._generate_control_mapping() + "\n\n"
        
        # Add recommendations
        formatted += "## ✅ Recommendations\n\n"
        formatted += self._generate_recommendations(content)
        
        return formatted
    
    def _classify_query(self, query: str) -> str:
        """Classify the compliance query type."""
        classifications = {
            "control": "Control Implementation",
            "audit": "Audit Preparation", 
            "risk": "Risk Assessment",
            "policy": "Policy Development",
            "standard": "Standards Compliance"
        }
        
        for keyword, classification in classifications.items():
            if keyword.lower() in query.lower():
                return classification
        
        return "General Compliance"
    
    def _assess_risk_level(self, content: str) -> str:
        """Assess risk level from content."""
        risk_indicators = ["critical", "high", "vulnerability", "breach", "failure"]
        risk_count = sum(1 for indicator in risk_indicators if indicator in content.lower())
        
        if risk_count >= 3:
            return "🔴 HIGH"
        elif risk_count >= 1:
            return "🟡 MEDIUM"
        else:
            return "🟢 LOW"
    
    def _generate_executive_summary(self, content: str) -> str:
        """Generate compliance executive summary."""
        return ("Assessment completed with focus on regulatory alignment and "
                "control effectiveness. Findings documented with actionable "
                "recommendations for compliance posture improvement.")
    
    def _generate_control_mapping(self) -> str:
        """Generate control framework mapping."""
        framework = random.choice(self.control_frameworks)
        return f"""| Control Family | Framework | Implementation Status |
|---------------|-----------|---------------------|
| Access Control | {framework} | ✅ Compliant |
| System Integrity | {framework} | 🔄 In Progress |
| Risk Management | {framework} | ✅ Compliant |"""
    
    def _generate_recommendations(self, content: str) -> str:
        """Generate compliance recommendations."""
        return """- [ ] Review control implementation against baseline requirements
- [ ] Update documentation to reflect current security posture  
- [ ] Schedule follow-up assessment within 90 days
- [ ] Validate corrective actions through independent testing"""
    
    def get_system_prompt(self) -> str:
        """Get Compliance system prompt."""
        return """You are a Compliance Auditor - precise, methodical, and confident. 
        Use risk vernacular and security language. Provide tabular breakdowns, 
        citations from documents, and annotated flows. Structure responses as 
        audit reports with executive summaries, findings, and recommendations."""
