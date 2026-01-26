import json
import pytest
from datetime import datetime
import os
import sys

# 프로젝트 루트를 path에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "../2-owen-community-be"))

# 각 테스트별 API 호출 로그를 저장할 전역 변수
test_call_logs = {}

@pytest.fixture
def api_client(request):
    """API 호출 입출력을 기록하는 래퍼 클라이언트 피스처"""
    from fastapi.testclient import TestClient
    from main import app
    
    client = TestClient(app)
    nodeid = request.node.nodeid
    test_call_logs[nodeid] = []

    def log_call(method, url, request_data, response):
        try:
            resp_json = response.json()
        except:
            resp_json = response.text

        test_call_logs[nodeid].append({
            "method": method,
            "url": str(url),
            "input": request_data,
            "output": {
                "status_code": response.status_code,
                "body": resp_json
            }
        })

    class WrappedClient:
        def __init__(self, inner):
            self.inner = inner
        def post(self, url, **kwargs):
            resp = self.inner.post(url, **kwargs)
            log_call("POST", url, kwargs.get("json") or kwargs.get("data") or (f"Files: {list(kwargs.get('files').keys())}" if kwargs.get('files') else None), resp)
            return resp
        def get(self, url, **kwargs):
            resp = self.inner.get(url, **kwargs)
            log_call("GET", url, kwargs.get("params"), resp)
            return resp
        def patch(self, url, **kwargs):
            resp = self.inner.patch(url, **kwargs)
            log_call("PATCH", url, kwargs.get("json") or kwargs.get("data"), resp)
            return resp
        def delete(self, url, **kwargs):
            resp = self.inner.delete(url, **kwargs)
            log_call("DELETE", url, None, resp)
            return resp

    return WrappedClient(client)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """테스트 실행 결과와 API 호출 로그를 JSON으로 병합 저장"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": terminalreporter._numcollected,
            "passed": len(terminalreporter.stats.get('passed', [])),
            "failed": len(terminalreporter.stats.get('failed', [])),
            "skipped": len(terminalreporter.stats.get('skipped', [])),
            "error": len(terminalreporter.stats.get('error', [])),
        },
        "details": []
    }

    # 각 테스트별 상세 결과 및 호출 로그 수집
    for status in ['passed', 'failed', 'skipped', 'error']:
        for report in terminalreporter.stats.get(status, []):
            nodeid = report.nodeid
            results["details"].append({
                "nodeid": nodeid,
                "status": status,
                "duration": getattr(report, "duration", 0),
                "calls": test_call_logs.get(nodeid, []),  # 수집된 API 호출 로그 병합
                "message": str(report.longrepr) if report.longrepr else None
            })

    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(current_dir, "test_results.json")
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[JSON Log] 상세 리포트가 생성되었습니다: {log_path}")
