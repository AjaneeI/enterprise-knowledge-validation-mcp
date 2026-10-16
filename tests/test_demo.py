"""Exercise the actual stakeholder fallback command as a separate client process."""
import json
import subprocess
import sys

def test_demo_runs_without_http_or_paid_services():
    result=subprocess.run([sys.executable,'-m','src.demo'],text=True,capture_output=True,timeout=20)
    assert result.returncode==0, result.stderr
    report=json.loads(result.stdout)
    assert report['server']['name']=='Knowledge Operations Demo'
    assert report['transport']=='stdio'
    assert report['scenarios']['superseded']['status']=='superseded'
    assert report['scenarios']['missing_approval']['ready_for_human_review'] is False
    assert report['scenarios']['positive_control']['ready_for_human_review'] is True
    assert report['spoof_rejected'] is True
    assert report['scenarios']['positive_control']['execution_authorized'] is False


def test_demo_rejects_nonlocal_unauthenticated_endpoint():
    result=subprocess.run([sys.executable,'-m','src.demo','--url','https://example.com/mcp'],text=True,capture_output=True,timeout=5)
    assert result.returncode!=0
    assert 'loopback' in result.stderr
