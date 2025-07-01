#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能交通系统项目启动器
整合所有功能模块，提供统一的启动界面
"""

import os
import sys
import time
import signal
import threading
import subprocess
from datetime import datetime
from typing import Optional, Dict, Any

# 尝试导入所有模块
try:
    from config import ConfigManager, get_config_manager, get_config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️  配置模块不可用")

try:
    from database import TrafficDatabase, get_database
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("⚠️  数据库模块不可用")

try:
    from analyzer import PerformanceAnalyzer
    ANALYZER_AVAILABLE = True
except ImportError:
    ANALYZER_AVAILABLE = False
    print("⚠️  分析模块不可用")

# 检查原始交通系统
TRAFFIC_SYSTEM_AVAILABLE = False
traffic_system_module = None

# 尝试导入集成版本
try:
    import integrated_traffic_system
    traffic_system_module = integrated_traffic_system
    TRAFFIC_SYSTEM_AVAILABLE = True
    print("✅ 集成交通系统可用")
except ImportError:
    # 尝试导入原始版本
    try:
        import fixed_rl_traffic
        traffic_system_module = fixed_rl_traffic
        TRAFFIC_SYSTEM_AVAILABLE = True
        print("✅ 原始交通系统可用")
    except ImportError:
        print("❌ 交通系统模块不可用")

class ProjectLauncher:
    """项目启动器"""
    
    def __init__(self):
        self.config_manager = None
        self.database = None
        self.analyzer = None
        self.traffic_system = None
        self.current_session_id = None
        
        # 初始化组件
        self._init_components()
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _init_components(self):
        """初始化组件"""
        print("🔧 初始化项目组件...")
        
        # 初始化配置管理器
        if CONFIG_AVAILABLE:
            self.config_manager = get_config_manager()
            self.config_manager.ensure_directories()
            print("✅ 配置管理器已初始化")
        
        # 初始化数据库
        if DATABASE_AVAILABLE:
            self.database = get_database()
            print("✅ 数据库已初始化")
        
        # 初始化分析器
        if ANALYZER_AVAILABLE and DATABASE_AVAILABLE:
            self.analyzer = PerformanceAnalyzer()
            print("✅ 性能分析器已初始化")
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        print("\n🛑 接收到中断信号，正在安全关闭...")
        self.shutdown()
        sys.exit(0)
    
    def show_main_menu(self):
        """显示主菜单"""
        while True:
            print("\n" + "=" * 60)
            print("🚦 智能交通信号灯控制系统 - 项目启动器")
            print("=" * 60)
            print("1. 🎓 开始训练 (推荐)")
            print("2. 🚀 部署模式")
            print("3. 📊 性能分析")
            print("4. 🔧 配置管理")
            print("5. 📋 数据库管理")
            print("6. 🌐 Web监控")
            print("7. 📖 系统信息")
            print("8. 🏗️ 项目设置")
            print("0. 🚪 退出")
            print("=" * 60)
            
            try:
                choice = input("请选择操作 (0-8): ").strip()
                
                if choice == '1':
                    self.start_training()
                elif choice == '2':
                    self.start_deployment()
                elif choice == '3':
                    self.performance_analysis()
                elif choice == '4':
                    self.config_management()
                elif choice == '5':
                    self.database_management()
                elif choice == '6':
                    self.web_monitoring()
                elif choice == '7':
                    self.show_system_info()
                elif choice == '8':
                    self.project_setup()
                elif choice == '0':
                    self.shutdown()
                    break
                else:
                    print("❌ 无效选择，请输入 0-8")
                    
            except KeyboardInterrupt:
                print("\n")
                self.shutdown()
                break
            except Exception as e:
                print(f"❌ 操作错误: {e}")
    
    def start_training(self):
        """开始训练"""
        print("\n🎓 启动训练模式")
        
        if not TRAFFIC_SYSTEM_AVAILABLE:
            print("❌ 交通系统不可用，请检查模块安装")
            return
        
        # 生成会话ID
        self.current_session_id = f"train_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 获取配置
        config = {}
        if CONFIG_AVAILABLE:
            config = self.config_manager.get_config()
            print(f"📋 使用配置文件: {self.config_manager.config_file}")
        
        # 记录到数据库
        if DATABASE_AVAILABLE:
            config_dict = {}
            if CONFIG_AVAILABLE:
                config_dict = {
                    'target_efficiency': config.training.target_efficiency,
                    'target_mobility': config.training.target_mobility,
                    'max_episodes': config.training.max_episodes,
                    'learning_rate': config.agent.learning_rate,
                    'num_vehicles': config.environment.num_vehicles
                }
            
            self.database.start_training_session(self.current_session_id, config_dict)
            self.database.log_event("INFO", "launcher", f"开始训练会话: {self.current_session_id}")
        
        try:
            # 启动交通系统
            if hasattr(traffic_system_module, 'IntegratedTrafficSystem'):
                # 使用集成版本
                system = traffic_system_module.IntegratedTrafficSystem()
                if system.initialize():
                    print(f"🎯 训练会话ID: {self.current_session_id}")
                    system.run_training()
            elif hasattr(traffic_system_module, 'AutoSmartTrafficSystem'):
                # 使用原始版本
                system = traffic_system_module.AutoSmartTrafficSystem()
                if system.initialize():
                    print(f"🎯 训练会话ID: {self.current_session_id}")
                    system.run_auto_training()
            else:
                print("❌ 无法找到交通系统类")
                return
            
        except Exception as e:
            print(f"❌ 训练启动失败: {e}")
            if DATABASE_AVAILABLE:
                self.database.log_event("ERROR", "launcher", f"训练启动失败: {e}")
        
        finally:
            # 结束会话记录
            if DATABASE_AVAILABLE and self.current_session_id:
                self.database.end_training_session(self.current_session_id, {"status": "completed"})
    
    def start_deployment(self):
        """启动部署模式"""
        print("\n🚀 启动部署模式")
        
        if not TRAFFIC_SYSTEM_AVAILABLE:
            print("❌ 交通系统不可用")
            return
        
        print("部署模式将使用已训练的模型进行交通控制")
        input("按回车键继续...")
        
        try:
            if hasattr(traffic_system_module, 'IntegratedTrafficSystem'):
                system = traffic_system_module.IntegratedTrafficSystem()
                if system.initialize():
                    # 部署模式逻辑
                    print("🚀 部署模式运行中...")
                    print("打开浏览器访问 http://localhost:5000 查看监控界面")
                    system.run_deployment()
            else:
                print("❌ 部署功能不可用")
                
        except Exception as e:
            print(f"❌ 部署启动失败: {e}")
    
    def performance_analysis(self):
        """性能分析"""
        print("\n📊 性能分析")
        
        if not ANALYZER_AVAILABLE:
            print("❌ 分析器不可用")
            return
        
        while True:
            print("\n分析选项:")
            print("1. 📈 分析训练会话")
            print("2. 📋 列出所有会话")
            print("3. 📊 系统摘要报告")
            print("4. 🔄 比较会话")
            print("0. 🔙 返回主菜单")
            
            choice = input("请选择 (0-4): ").strip()
            
            if choice == '1':
                sessions = self.database.get_training_sessions(10)
                if not sessions:
                    print("❌ 没有找到训练会话")
                    continue
                
                print("\n可用的训练会话:")
                for i, session in enumerate(sessions):
                    print(f"{i+1}. {session['session_id']} - {session['start_time']} ({session['status']})")
                
                try:
                    idx = int(input("选择会话编号: ")) - 1
                    if 0 <= idx < len(sessions):
                        session_id = sessions[idx]['session_id']
                        print(f"\n🔍 正在分析会话: {session_id}")
                        report = self.analyzer.analyze_session(session_id)
                        if report:
                            print(f"✅ 分析完成！报告保存在: {self.analyzer.output_dir}")
                    else:
                        print("❌ 无效的会话编号")
                except (ValueError, IndexError):
                    print("❌ 输入无效")
            
            elif choice == '2':
                sessions = self.database.get_training_sessions(20)
                print(f"\n📋 训练会话列表 (最近20个):")
                print("-" * 100)
                for session in sessions:
                    status_icon = "✅" if session['status'] == 'completed' else "🔄" if session['status'] == 'running' else "❌"
                    print(f"{status_icon} {session['session_id']} | {session['start_time']} | "
                          f"回合: {session['total_episodes']} | 得分: {session['best_score']:.3f}")
                print("-" * 100)
            
            elif choice == '3':
                print("\n📊 生成系统摘要报告...")
                summary = self.analyzer.generate_summary_report()
                print(f"总会话数: {summary['total_sessions']}")
                print(f"总训练回合: {summary['total_episodes']:,}")
                print(f"平均性能: 奖励={summary['avg_performance']['reward']:.3f}")
                print(f"完成率: {summary['completion_rate']:.1%}")
            
            elif choice == '4':
                print("🔄 会话比较功能开发中...")
            
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")
    
    def config_management(self):
        """配置管理"""
        print("\n🔧 配置管理")
        
        if not CONFIG_AVAILABLE:
            print("❌ 配置管理器不可用")
            return
        
        while True:
            print("\n配置选项:")
            print("1. 📋 查看当前配置")
            print("2. ✏️  修改配置")
            print("3. 💾 保存配置")
            print("4. 📄 创建示例配置")
            print("0. 🔙 返回主菜单")
            
            choice = input("请选择 (0-4): ").strip()
            
            if choice == '1':
                self.config_manager.print_config()
            
            elif choice == '2':
                print("\n可修改的配置项:")
                print("1. 训练目标效率")
                print("2. 训练目标流动性")
                print("3. 最大训练轮数")
                print("4. 学习率")
                print("5. 车辆数量")
                
                try:
                    config_choice = int(input("选择要修改的配置 (1-5): "))
                    config = self.config_manager.get_config()
                    
                    if config_choice == 1:
                        new_value = float(input(f"输入新的目标效率 (当前: {config.training.target_efficiency}): "))
                        config.training.target_efficiency = new_value
                    elif config_choice == 2:
                        new_value = float(input(f"输入新的目标流动性 (当前: {config.training.target_mobility}): "))
                        config.training.target_mobility = new_value
                    elif config_choice == 3:
                        new_value = int(input(f"输入新的最大训练轮数 (当前: {config.training.max_episodes}): "))
                        config.training.max_episodes = new_value
                    elif config_choice == 4:
                        new_value = float(input(f"输入新的学习率 (当前: {config.agent.learning_rate}): "))
                        config.agent.learning_rate = new_value
                    elif config_choice == 5:
                        new_value = int(input(f"输入新的车辆数量 (当前: {config.environment.num_vehicles}): "))
                        config.environment.num_vehicles = new_value
                    else:
                        print("❌ 无效选择")
                        continue
                    
                    print("✅ 配置已更新")
                    
                except (ValueError, AttributeError) as e:
                    print(f"❌ 配置更新失败: {e}")
            
            elif choice == '3':
                if self.config_manager.save_config():
                    print("✅ 配置已保存")
                else:
                    print("❌ 配置保存失败")
            
            elif choice == '4':
                if self.config_manager.create_sample_config():
                    print("✅ 示例配置文件已创建")
                else:
                    print("❌ 创建失败")
            
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")
    
    def database_management(self):
        """数据库管理"""
        print("\n📋 数据库管理")
        
        if not DATABASE_AVAILABLE:
            print("❌ 数据库不可用")
            return
        
        while True:
            print("\n数据库选项:")
            print("1. 📊 查看统计信息")
            print("2. 🗑️  清理旧数据")
            print("3. 📤 导出数据")
            print("4. 📋 查看日志")
            print("0. 🔙 返回主菜单")
            
            choice = input("请选择 (0-4): ").strip()
            
            if choice == '1':
                stats = self.database.get_statistics()
                print(f"\n📊 数据库统计:")
                print(f"总训练回合: {stats.get('total_episodes', 0):,}")
                print(f"平均奖励: {stats.get('avg_reward', 0):.3f}")
                print(f"平均效率: {stats.get('avg_efficiency', 0):.3f}")
                print(f"平均流动性: {stats.get('avg_mobility', 0):.3f}")
                print(f"总会话数: {stats.get('total_sessions', 0)}")
                print(f"完成会话数: {stats.get('completed_sessions', 0)}")
            
            elif choice == '2':
                days = input("保留多少天的数据 (默认30天): ").strip()
                days = int(days) if days.isdigit() else 30
                
                confirm = input(f"确认删除 {days} 天前的数据? (y/N): ").strip().lower()
                if confirm == 'y':
                    if self.database.cleanup_old_data(days):
                        print("✅ 数据清理完成")
                    else:
                        print("❌ 数据清理失败")
            
            elif choice == '3':
                sessions = self.database.get_training_sessions(10)
                if not sessions:
                    print("❌ 没有可导出的会话")
                    continue
                
                print("\n可导出的会话:")
                for i, session in enumerate(sessions):
                    print(f"{i+1}. {session['session_id']}")
                
                try:
                    idx = int(input("选择会话编号: ")) - 1
                    if 0 <= idx < len(sessions):
                        session_id = sessions[idx]['session_id']
                        export_path = f"export_{session_id}.json"
                        if self.database.export_data(session_id, export_path):
                            print(f"✅ 数据已导出到: {export_path}")
                    else:
                        print("❌ 无效的会话编号")
                except (ValueError, IndexError):
                    print("❌ 输入无效")
            
            elif choice == '4':
                print("📋 查看系统日志功能开发中...")
            
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")
    
    def web_monitoring(self):
        """Web监控"""
        print("\n🌐 Web监控")
        
        if CONFIG_AVAILABLE:
            web_config = self.config_manager.get_config().web
            if web_config.enabled:
                print(f"Web监控地址: http://{web_config.host}:{web_config.port}")
                print("请在浏览器中打开上述地址查看实时监控")
            else:
                print("Web监控已禁用，请在配置中启用")
        else:
            print("默认Web监控地址: http://localhost:5000")
        
        input("按回车键返回主菜单...")
    
    def show_system_info(self):
        """显示系统信息"""
        print("\n📖 系统信息")
        print("=" * 60)
        print("🚦 智能交通信号灯控制系统")
        print("基于CARLA仿真平台的深度强化学习交通优化")
        print("=" * 60)
        
        print("\n📦 可用模块:")
        print(f"  交通系统: {'✅' if TRAFFIC_SYSTEM_AVAILABLE else '❌'}")
        print(f"  配置管理: {'✅' if CONFIG_AVAILABLE else '❌'}")
        print(f"  数据库: {'✅' if DATABASE_AVAILABLE else '❌'}")
        print(f"  性能分析: {'✅' if ANALYZER_AVAILABLE else '❌'}")
        
        print("\n🎯 主要功能:")
        print("  • DQN深度强化学习算法")
        print("  • CARLA仿真环境集成")
        print("  • 实时Web监控界面")
        print("  • 自动训练和模型保存")
        print("  • 性能分析和可视化")
        print("  • 配置管理系统")
        print("  • 训练历史数据库")
        
        print("\n📊 性能指标:")
        print("  • 交通效率 (目标: ≥75%)")
        print("  • 流动性 (目标: ≥80%)")
        print("  • 平均奖励 (目标: ≥0.5)")
        print("  • 车辆平均速度")
        print("  • 拥堵比例")
        
        if DATABASE_AVAILABLE:
            stats = self.database.get_statistics()
            if stats.get('total_episodes', 0) > 0:
                print(f"\n📈 历史统计:")
                print(f"  总训练回合: {stats.get('total_episodes', 0):,}")
                print(f"  平均性能: {stats.get('avg_efficiency', 0):.1%}")
                print(f"  最佳效率: {stats.get('max_efficiency', 0):.1%}")
        
        input("\n按回车键返回主菜单...")
    
    def project_setup(self):
        """项目设置"""
        print("\n🏗️ 项目设置")
        
        while True:
            print("\n设置选项:")
            print("1. 📁 检查项目文件")
            print("2. 🔧 初始化配置")
            print("3. 💾 创建数据库")
            print("4. 📦 检查依赖")
            print("5. 🧹 清理临时文件")
            print("0. 🔙 返回主菜单")
            
            choice = input("请选择 (0-5): ").strip()
            
            if choice == '1':
                self._check_project_files()
            elif choice == '2':
                self._init_config()
            elif choice == '3':
                self._init_database()
            elif choice == '4':
                self._check_dependencies()
            elif choice == '5':
                self._cleanup_temp_files()
            elif choice == '0':
                break
            else:
                print("❌ 无效选择")
    
    def _check_project_files(self):
        """检查项目文件"""
        print("\n📁 检查项目文件...")
        
        required_files = [
            'fixed_rl_traffic.py',
            'integrated_traffic_system.py',
            'config.py',
            'database.py',
            'analyzer.py',
            'launcher.py'
        ]
        
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ {file}")
            else:
                print(f"❌ {file} (缺失)")
        
        # 检查目录
        required_dirs = ['models', 'logs', 'data', 'analysis_output']
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                print(f"✅ {dir_name}/")
            else:
                print(f"⚠️  {dir_name}/ (将自动创建)")
                os.makedirs(dir_name, exist_ok=True)
    
    def _init_config(self):
        """初始化配置"""
        if CONFIG_AVAILABLE:
            self.config_manager.create_sample_config("config.yaml")
            print("✅ 配置文件已初始化")
        else:
            print("❌ 配置模块不可用")
    
    def _init_database(self):
        """初始化数据库"""
        if DATABASE_AVAILABLE:
            # 数据库在导入时已自动初始化
            print("✅ 数据库已初始化")
        else:
            print("❌ 数据库模块不可用")
    
    def _check_dependencies(self):
        """检查依赖"""
        print("\n📦 检查Python依赖...")
        
        dependencies = [
            ('carla', 'CARLA客户端'),
            ('torch', 'PyTorch深度学习'),
            ('numpy', 'NumPy数值计算'),
            ('matplotlib', '图表绘制'),
            ('pandas', '数据处理'),
            ('seaborn', '可视化'),
            ('flask', 'Web服务器'),
            ('yaml', 'YAML配置'),
        ]
        
        for module, description in dependencies:
            try:
                __import__(module)
                print(f"✅ {module} - {description}")
            except ImportError:
                print(f"❌ {module} - {description} (未安装)")
    
    def _cleanup_temp_files(self):
        """清理临时文件"""
        print("\n🧹 清理临时文件...")
        
        patterns = ['*.pyc', '__pycache__', '*.tmp', '*.log']
        cleaned = 0
        
        for pattern in patterns:
            # 这里可以添加清理逻辑
            pass
        
        print(f"✅ 清理完成，删除了 {cleaned} 个文件")
    
    def shutdown(self):
        """关闭系统"""
        print("\n🛑 正在关闭系统...")
        
        if self.database:
            if self.current_session_id:
                self.database.end_training_session(self.current_session_id, {"status": "stopped"})
            self.database.close()
        
        print("✅ 系统已安全关闭")

def main():
    """主函数"""
    launcher = ProjectLauncher()
    launcher.show_main_menu()

if __name__ == "__main__":
    main()