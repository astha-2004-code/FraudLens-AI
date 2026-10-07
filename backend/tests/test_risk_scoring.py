from app.analytics.risk_scorer import RiskScorer

def test_risk_scorer_critical():
    mock_analytics = {
        "amount": {"is_anomalous": True, "deviation_pct": 300}, # 20 points
        "velocity": {"is_anomalous": True}, # 20 points
        "device": {"is_new_device": True, "shared_by_others": True}, # 15 points
        "location": {"impossible_travel": True}, # 15 points
        "merchant": {"is_anomalous": True}, # 10 points
        "time": {"is_anomalous": True} # 10 points
    }
    
    scorer = RiskScorer(mock_analytics)
    result = scorer.calculate_score()
    
    assert result["score"] == 90
    assert result["risk_level"] == "CRITICAL"
    assert len(result["signals"]) == 7

def test_risk_scorer_low():
    mock_analytics = {
        "amount": {"is_anomalous": False},
        "velocity": {"is_anomalous": False},
        "device": {"is_new_device": False, "shared_by_others": False},
        "location": {"impossible_travel": False, "is_new_country": False},
        "merchant": {"is_anomalous": False},
        "time": {"is_anomalous": False}
    }
    
    scorer = RiskScorer(mock_analytics)
    result = scorer.calculate_score()
    
    assert result["score"] == 0
    assert result["risk_level"] == "LOW"
    assert len(result["signals"]) == 0
