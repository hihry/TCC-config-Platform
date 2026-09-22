import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from tcc_platform.agents.qa import run_qa

def test_qa_rejects_hallucinated_message():
    state = {"patch_data": {"message_key": "MSG-HALLUCINATED"}}
    res = run_qa(state)
    assert res["is_valid"] is False
    assert "Invalid message_key: MSG-HALLUCINATED" in res["validation_errors"]
    print("test_qa_rejects_hallucinated_message passed")

def test_qa_rejects_hallucinated_alert():
    state = {"patch_data": {"alert_key": "ALT-FAKE"}}
    res = run_qa(state)
    assert res["is_valid"] is False
    assert "Invalid alert_key: ALT-FAKE" in res["validation_errors"]
    print("test_qa_rejects_hallucinated_alert passed")

def test_qa_accepts_valid_keys():
    # MSG-101 and ALT-001 are part of our mock data
    state = {"patch_data": {"message_key": "MSG-101", "alert_key": "ALT-001"}}
    res = run_qa(state)
    assert res["is_valid"] is True
    assert len(res["validation_errors"]) == 0
    print("test_qa_accepts_valid_keys passed")

def test_qa_accepts_empty_patch():
    state = {"patch_data": {}}
    res = run_qa(state)
    assert res["is_valid"] is True
    print("test_qa_accepts_empty_patch passed")

if __name__ == "__main__":
    test_qa_rejects_hallucinated_message()
    test_qa_rejects_hallucinated_alert()
    test_qa_accepts_valid_keys()
    test_qa_accepts_empty_patch()
    print("\nAll QA deterministic tests passed successfully!")
