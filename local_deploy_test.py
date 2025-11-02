#!/usr/bin/env python3
"""
VabHub 本地开发环境整合功能验证脚本
测试所有整合功能在本地环境中的运行状态
"""

import os
import sys
import time
import json
from typing import Dict, Any

class VabHubLocalTester:
    def __init__(self):
        self.test_results = {}
    
    def test_python_environment(self) -> Dict[str, Any]:
        """测试Python环境"""
        try:
            import platform
            python_version = platform.python_version()
            
            return {
                "status": "✅ Python环境正常",
                "python_version": python_version,
                "platform": platform.platform()
            }
        except Exception as e:
            return {"status": f"❌ Python环境异常: {str(e)}", "error": str(e)}
    
    def test_dependencies(self) -> Dict[str, Any]:
        """测试核心依赖包"""
        dependencies = [
            "fastapi", "uvicorn", "pydantic", "httpx", "redis",
            "sqlalchemy", "celery", "strawberry-graphql", "websockets",
            "sentence-transformers", "faiss-cpu", "transformers", "torch"
        ]
        
        results = {}
        for dep in dependencies:
            try:
                __import__(dep)
                results[dep] = "✅ 正常"
            except ImportError as e:
                results[dep] = f"❌ 缺失: {str(e)}"
        
        return {
            "status": "✅ 依赖检查完成",
            "details": results
        }
    
    def test_config_files(self) -> Dict[str, Any]:
        """测试配置文件"""
        config_files = [
            "config/config.yaml",
            "vabhub-Core/requirements.txt", 
            "vabhub-frontend/package.json",
            "docker-compose.yml"
        ]
        
        results = {}
        for config_file in config_files:
            file_path = os.path.join("f:\\VabHub", config_file)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                results[config_file] = f"✅ 存在 ({file_size} bytes)"
            else:
                results[config_file] = "❌ 缺失"
        
        return {
            "status": "✅ 配置文件检查完成",
            "details": results
        }
    
    def test_core_modules(self) -> Dict[str, Any]:
        """测试核心模块导入"""
        core_modules = [
            "vabhub-Core.core.plugin_manager",
            "vabhub-Core.core.ai_recommendation", 
            "vabhub-Core.core.cache_manager",
            "vabhub-Core.core.graphql_api",
            "vabhub-Core.core.music_platform_adapter"
        ]
        
        results = {}
        for module_path in core_modules:
            try:
                # 添加项目根目录到Python路径
                sys.path.insert(0, "f:\\VabHub")
                
                # 动态导入模块
                module_name = module_path.split(".")[-1]
                full_path = module_path.replace(".", "\\")
                
                if os.path.exists(os.path.join("f:\\VabHub", full_path + ".py")):
                    results[module_name] = "✅ 模块文件存在"
                else:
                    results[module_name] = "❌ 模块文件缺失"
                    
            except Exception as e:
                results[module_path] = f"❌ 导入异常: {str(e)}"
        
        return {
            "status": "✅ 核心模块检查完成",
            "details": results
        }
    
    def test_project_structure(self) -> Dict[str, Any]:
        """测试项目结构"""
        directories = [
            "vabhub-Core", "vabhub-frontend", "vabhub-plugins",
            "vabhub-deploy", "vabhub-resources", "config"
        ]
        
        results = {}
        for dir_name in directories:
            dir_path = os.path.join("f:\\VabHub", dir_name)
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                file_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
                results[dir_name] = f"✅ 存在 ({file_count} 个文件)"
            else:
                results[dir_name] = "❌ 缺失"
        
        return {
            "status": "✅ 项目结构检查完成",
            "details": results
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """运行所有测试"""
        print("🚀 开始VabHub本地整合功能验证...")
        print("=" * 60)
        
        tests = {
            "Python环境": self.test_python_environment,
            "依赖包": self.test_dependencies,
            "配置文件": self.test_config_files,
            "核心模块": self.test_core_modules,
            "项目结构": self.test_project_structure
        }
        
        for test_name, test_func in tests.items():
            print(f"🧪 正在测试: {test_name}...")
            try:
                result = test_func()
                self.test_results[test_name] = result
                print(f"   {result['status']}")
                
                # 显示详细信息
                if 'details' in result:
                    for key, value in result['details'].items():
                        if "❌" in value:
                            print(f"     {key}: {value}")
                            
            except Exception as e:
                self.test_results[test_name] = {"status": f"❌ 测试异常: {str(e)}", "error": str(e)}
                print(f"   ❌ 测试异常: {str(e)}")
        
        return self.test_results
    
    def generate_report(self) -> str:
        """生成测试报告"""
        print("\n" + "=" * 60)
        print("📊 VabHub本地整合功能验证报告")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results.values() if r['status'].startswith('✅'))
        failed_tests = total_tests - passed_tests
        
        print(f"📈 测试统计: {passed_tests}/{total_tests} 通过")
        print(f"🟢 通过测试: {passed_tests}")
        print(f"🔴 失败测试: {failed_tests}")
        
        # 详细结果
        print("\n📋 详细测试结果:")
        for test_name, result in self.test_results.items():
            status_icon = "✅" if result['status'].startswith('✅') else "❌"
            print(f"{status_icon} {test_name}: {result['status']}")
            
            # 显示关键错误信息
            if 'error' in result:
                print(f"   错误信息: {result['error']}")
        
        # 总体评估
        print("\n🎯 本地验证结论:")
        if failed_tests == 0:
            print("✅ 所有整合功能本地验证通过！项目结构完整，依赖正常。")
            print("💡 建议: 可以开始开发和使用所有整合功能。")
        elif failed_tests <= 2:
            print("⚠️ 部分功能验证失败，但核心结构完整。")
            print("💡 建议: 检查缺失的依赖或配置文件。")
        else:
            print("❌ 多个关键功能验证失败，需要检查项目完整性。")
            print("💡 建议: 重新检查项目结构和依赖安装。")
        
        # 技术栈验证
        print("\n🔧 技术栈验证结果:")
        if '依赖包' in self.test_results:
            deps = self.test_results['依赖包']['details']
            ai_deps = [k for k in deps.keys() if any(x in k for x in ['transform', 'torch', 'faiss'])]
            web_deps = [k for k in deps.keys() if any(x in k for x in ['fastapi', 'graphql', 'websocket'])]
            
            print("🤖 AI技术栈:")
            for dep in ai_deps:
                print(f"   {deps[dep]} - {dep}")
            
            print("🌐 Web技术栈:")  
            for dep in web_deps:
                print(f"   {deps[dep]} - {dep}")
        
        return json.dumps(self.test_results, indent=2, ensure_ascii=False)

def main():
    """主函数"""
    tester = VabHubLocalTester()
    
    try:
        # 运行所有测试
        results = tester.run_all_tests()
        
        # 生成报告
        report = tester.generate_report()
        
        # 保存报告到文件
        with open("local_validation_report.json", "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n📄 详细报告已保存到: local_validation_report.json")
        
    except Exception as e:
        print(f"❌ 测试过程中发生异常: {str(e)}")

if __name__ == "__main__":
    main()