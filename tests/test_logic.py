from src.logic import check_procedure_status, compare_procedure_versions, assess_action_readiness, generate_review_brief

def test_current():
    assert check_procedure_status("SOP-104", "2.0")["decision"] == "eligible_for_review"
def test_superseded():
    assert check_procedure_status("SOP-104", "1.0")["decision"] == "hold_for_review"
def test_unknown():
    assert check_procedure_status("SOP-999", "1.0")["found"] is False
def test_compare():
    result = compare_procedure_versions("SOP-104", "1.0", "2.0")
    assert "Stop equipment safely" in result["added_steps"]
def test_missing_compare():
    assert not compare_procedure_versions("SOP-104", "1.0", "9.0")["found"]
def test_not_authorized():
    result = assess_action_readiness("ACT-002")
    assert result["execution_authorized"] is False
def test_missing_approval():
    assert assess_action_readiness("ACT-001")["approval_evidence_status"] == "missing"
def test_brief():
    assert generate_review_brief("SOP-104", "2.0")["source_ref"].startswith("synthetic://")
