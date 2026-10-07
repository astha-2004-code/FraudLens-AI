from typing import Dict, Any

class RiskScorer:
    def __init__(self, analytics_results: Dict[str, Any]):
        self.results = analytics_results

    def calculate_score(self):
        score = 0
        signals = []
        
        # Amount anomaly (max 20)
        amount_res = self.results.get("amount", {})
        if amount_res.get("is_anomalous"):
            points = min(20, int(amount_res.get("deviation_pct", 0) / 10))
            score += points
            signals.append({"signal_type": "AMOUNT_ANOMALY", "score_impact": points})

        # Velocity anomaly (max 20)
        velocity_res = self.results.get("velocity", {})
        if velocity_res.get("is_anomalous"):
            score += 20
            signals.append({"signal_type": "VELOCITY_ANOMALY", "score_impact": 20})

        # Device anomaly (max 15)
        device_res = self.results.get("device", {})
        if device_res.get("is_new_device"):
            score += 10
            signals.append({"signal_type": "NEW_DEVICE", "score_impact": 10})
        if device_res.get("shared_by_others"):
            score += 5
            signals.append({"signal_type": "SHARED_DEVICE", "score_impact": 5})

        # Location anomaly (max 15)
        location_res = self.results.get("location", {})
        if location_res.get("impossible_travel"):
            score += 15
            signals.append({"signal_type": "IMPOSSIBLE_TRAVEL", "score_impact": 15})
        elif location_res.get("is_new_country"):
            score += 10
            signals.append({"signal_type": "NEW_COUNTRY", "score_impact": 10})

        # Merchant anomaly (max 10)
        merchant_res = self.results.get("merchant", {})
        if merchant_res.get("is_anomalous"):
            score += 10
            signals.append({"signal_type": "MERCHANT_ANOMALY", "score_impact": 10})

        # Time anomaly (max 10)
        time_res = self.results.get("time", {})
        if time_res.get("is_anomalous"):
            score += 10
            signals.append({"signal_type": "TIME_ANOMALY", "score_impact": 10})
            
        score = min(100, score)
        
        if score < 30:
            risk_level = "LOW"
        elif score < 60:
            risk_level = "MEDIUM"
        elif score < 80:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
            
        return {
            "score": score,
            "risk_level": risk_level,
            "signals": signals
        }
