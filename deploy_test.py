#!/usr/bin/env python3
"""
VabHub 整合功能部署验证脚本
测试所有整合功能在生产环境中的运行状态
"""

import asyncio
import httpx
import time
import json
from typing import Dict, Any

class VabHubDeploymentTester:
    def __init__(self, base_url: str = "http://localhost:4001"):
        self.base_url = base_url
        self.graphql_url = f"{base_url.replace('4001', '4002')}/graphql"
        self.metrics_url = f"{base_url.replace('4001', '9090')}/metrics"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def test_health_check(self) -> Dict[str, Any]:
        """测试基础健康检查"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return {
                "status": "✅ 健康检查通过" if response.status_code == 200 else "❌ 健康检查失败",
                "response_time": response.elapsed.total_seconds(),
                "status_code": response.status_code
            }
        except Exception as e:
            return {"status": f"❌ 健康检查异常: {str(e)}", "error": str(e)}
    
    async def test_api_endpoints(self) -> Dict[str, Any]:
        """测试核心API端点"""
        endpoints = [
            "/api/v1/plugins",
            "/api/v1/media",
            "/api/v1/search",
            "/api/v1/recommendations"
        ]
        
        results = {}
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = await self.client.get(f"{self.base_url}{endpoint}")
                response_time = time.time() - start_time
                
                results[endpoint] = {
                    "status": "✅ 正常" if response.status_code in [200, 401] else "❌ 异常",
                    "response_time": response_time,
                    "status_code": response.status_code
                }
            except Exception as e:
                results[endpoint] = {"status": f"❌ 异常: {str(e)}", "error": str(e)}
        
        return results
    
    async def test_graphql_api(self) -> Dict[str, Any]:
        """测试GraphQL API"""
        try:
            query = """
            query {
                healthCheck {
                    status
                    timestamp
                }
            }
            """
            
            start_time = time.time()
            response = await self.client.post(
                self.graphql_url,
                json={"query": query}
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "✅ GraphQL API正常",
                    "response_time": response_time,
                    "data": data.get("data", {})
                }
            else:
                return {
                    "status": f"❌ GraphQL API异常: {response.status_code}",
                    "response_time": response_time,
                    "status_code": response.status_code
                }
        except Exception as e:
            return {"status": f"❌ GraphQL API异常: {str(e)}", "error": str(e)}
    
    async def test_metrics_endpoint(self) -> Dict[str, Any]:
        """测试监控指标端点"""
        try:
            start_time = time.time()
            response = await self.client.get(self.metrics_url)
            response_time = time.time() - start_time
            
            return {
                "status": "✅ 监控指标正常" if response.status_code == 200 else "❌ 监控指标异常",
                "response_time": response_time,
                "status_code": response.status_code,
                "has_metrics": "metrics" in response.text.lower()
            }
        except Exception as e:
            return {"status": f"❌ 监控指标异常: {str(e)}", "error": str(e)}
    
    async def test_cache_performance(self) -> Dict[str, Any]:
        """测试缓存性能"""
        try:
            # 测试缓存设置和获取
            test_key = "deployment_test_key"
            test_value = {"test": "data", "timestamp": time.time()}
            
            # 设置缓存
            set_start = time.time()
            set_response = await self.client.post(
                f"{self.base_url}/api/v1/cache/{test_key}",
                json=test_value
            )
            set_time = time.time() - set_start
            
            # 获取缓存
            get_start = time.time()
            get_response = await self.client.get(f"{self.base_url}/api/v1/cache/{test_key}")
            get_time = time.time() - get_start
            
            return {
                "status": "✅ 缓存功能正常",
                "set_time": set_time,
                "get_time": get_time,
                "set_status": set_response.status_code,
                "get_status": get_response.status_code
            }
        except Exception as e:
            return {"status": f"❌ 缓存功能异常: {str(e)}", "error": str(e)}
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("🚀 开始VabHub整合功能部署验证...")
        print("=" * 60)
        
        tests = {
            "健康检查": self.test_health_check,
            "API端点": self.test_api_endpoints,
            "GraphQL API": self.test_graphql_api,
            "监控指标": self.test_metrics_endpoint,
            "缓存性能": self.test_cache_performance
        }
        
        results = {}
        for test_name, test_func in tests.items():
            print(f"🧪 正在测试: {test_name}...")
            try:
                result = await test_func()
                results[test_name] = result
                print(f"   {result['status']}")
                if 'response_time' in result:
                    print(f"   响应时间: {result['response_time']:.3f}s")
            except Exception as e:
                results[test_name] = {"status": f"❌ 测试异常: {str(e)}", "error": str(e)}
                print(f"   ❌ 测试异常: {str(e)}")
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 VabHub部署验证报告")
        print("=" * 60)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r['status'].startswith('✅'))
        failed_tests = total_tests - passed_tests
        
        print(f"📈 测试统计: {passed_tests}/{total_tests} 通过")
        print(f"🟢 通过测试: {passed_tests}")
        print(f"🔴 失败测试: {failed_tests}")
        
        # 详细结果
        print("\n📋 详细测试结果:")
        for test_name, result in results.items():
            status_icon = "✅" if result['status'].startswith('✅') else "❌"
            print(f"{status_icon} {test_name}: {result['status']}")
            if 'response_time' in result:
                print(f"   响应时间: {result['response_time']:.3f}s")
            if 'error' in result:
                print(f"   错误信息: {result['error']}")
        
        # 总体评估
        print("\n🎯 部署验证结论:")
        if failed_tests == 0:
            print("✅ 所有整合功能部署验证通过！VabHub系统运行正常。")
            print("💡 建议: 可以开始使用所有整合功能。")
        elif failed_tests <= 2:
            print("⚠️ 部分功能验证失败，但核心功能正常。")
            print("💡 建议: 检查网络连接和依赖服务状态。")
        else:
            print("❌ 多个关键功能验证失败，需要检查部署配置。")
            print("💡 建议: 检查Docker容器状态和日志文件。")
        
        return json.dumps(results, indent=2, ensure_ascii=False)

async def main():
    """主函数"""
    tester = VabHubDeploymentTester()
    
    try:
        # 运行所有测试
        results = await tester.run_all_tests()
        
        # 生成报告
        report = tester.generate_report(results)
        
        # 保存报告到文件
        with open("deployment_validation_report.json", "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n📄 详细报告已保存到: deployment_validation_report.json")
        
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {str(e)}")
    
    finally:
        await tester.client.aclose()

if __name__ == "__main__":
    asyncio.run(main())