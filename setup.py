#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
智能交通系统安装脚本
自动检查依赖、创建目录、初始化配置
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class ProjectSetup:
    """项目安装器"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.python_version = sys.version_info
        self.system = platform.system()
        
    def run_setup(self):
        """运行完整安装流程"""
        print("🚀 智能交通信号灯控制系统 - 安装向导")
        print("=" * 60)
        
        # 检查Python版本
        if not self.check_python_version():
            return False
            
        # 创建项目目录结构
        self.create_directories()
        
        # 安装Python依赖
        if not self.install_dependencies():
            return False
            
        # 创建示例配置
        self.create_sample_configs()
        
        # 创建启动脚本
        self.create_launch_scripts()
        
        # 检查CARLA
        self.check_carla()
        
        # 完成安装
        self.finish_setup()
        
        return True
    
    def check_python_version(self):
        """检查Python版本"""
        print(f"\n🐍 检查Python版本: {self.python_version.major}.{self.python_version.minor}")
        
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 7):
            print("❌ 需要Python 3.7或更高版本")
            print("请升级Python后重新运行安装脚本")
            return False
        
        print("✅ Python版本符合要求")
        return True
    
    def create_directories(self):
        """创建项目目录结构"""
        print("\n📁 创建项目目录...")
        
        directories = [
            'models',           # 模型文件
            'logs',            # 日志文件
            'data',            # 数据文件
            'config',          # 配置文件
            'analysis_output', # 分析输出
            'exports',         # 导出数据
            'temp',            # 临时文件
            'docs',            # 文档
            'scripts'          # 脚本
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(exist_ok=True)
            print(f"✅ {directory}/")
    
    def install_dependencies(self):
        """安装Python依赖"""
        print("\n📦 安装Python依赖...")
        
        # 基础依赖（必需）
        core_dependencies = [
            'numpy>=1.19.0',
            'matplotlib>=3.3.0',
            'pandas>=1.1.0',
            'seaborn>=0.11.0',
            'flask>=2.0.0',
            'pyyaml>=5.4.0',
            'requests>=2.25.0'
        ]
        
        # 可选依赖
        optional_dependencies = [
            'torch>=1.8.0',      # PyTorch (深度学习)
            'tensorboard>=2.4.0', # TensorBoard (可视化)
            'plotly>=5.0.0',      # Plotly (交互式图表)
            'opencv-python>=4.5.0' # OpenCV (图像处理)
        ]
        
        # 安装核心依赖
        print("安装核心依赖...")
        for package in core_dependencies:
            if self.install_package(package, required=True):
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - 安装失败")
                return False
        
        # 安装可选依赖
        print("\n安装可选依赖...")
        for package in optional_dependencies:
            if self.install_package(package, required=False):
                print(f"✅ {package}")
            else:
                print(f"⚠️  {package} - 跳过（可选）")
        
        return True
    
    def install_package(self, package, required=True):
        """安装单个包"""
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package, '--quiet'
            ])
            return True
        except subprocess.CalledProcessError:
            if required:
                print(f"❌ 安装 {package} 失败")
            return False
    
    def create_sample_configs(self):
        """创建示例配置文件"""
        print("\n📝 创建配置文件...")
        
        # 主配置文件
        config_yaml = """# 智能交通系统配置文件
# 修改此文件来自定义系统参数

training:
  target_efficiency: 0.75    # 目标效率
  target_mobility: 0.80      # 目标流动性
  target_reward: 0.50        # 目标奖励
  min_episodes: 100          # 最少训练轮数
  max_episodes: 1000         # 最大训练轮数
  stability_window: 20       # 稳定性窗口
  auto_save_interval: 100    # 自动保存间隔

carla:
  host: "localhost"          # CARLA主机地址
  port: 2000                 # CARLA端口
  timeout: 10.0              # 连接超时
  map_name: "Town03"         # 地图名称
  synchronous_mode: true     # 同步模式
  fixed_delta_seconds: 0.05  # 固定时间步长

agent:
  state_size: 16             # 状态空间大小
  action_size: 4             # 动作空间大小
  learning_rate: 0.001       # 学习率
  epsilon: 0.5               # 初始探索率
  epsilon_min: 0.01          # 最小探索率
  epsilon_decay: 0.995       # 探索率衰减
  memory_size: 10000         # 经验池大小
  batch_size: 64             # 批次大小

environment:
  num_vehicles: 30           # 车辆数量
  min_vehicles: 15           # 最少车辆数
  data_collection_interval: 1.0  # 数据收集间隔
  reward_weights:
    mobility: 0.5            # 流动性权重
    efficiency: 0.3          # 效率权重
    speed: 0.15              # 速度权重
    action: 0.05             # 动作权重

web:
  enabled: true              # 启用Web监控
  host: "0.0.0.0"           # Web服务器地址
  port: 5000                 # Web服务器端口
  debug: false               # 调试模式
  update_interval: 2         # 更新间隔(秒)

# 系统设置
models_dir: "models"         # 模型目录
logs_dir: "logs"            # 日志目录
data_dir: "data"            # 数据目录
debug_mode: false           # 调试模式
verbose_logging: true       # 详细日志
"""
        
        config_path = self.project_root / 'config' / 'config.yaml'
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_yaml)
        print(f"✅ {config_path}")
        
        # 环境变量配置
        env_config = """# 环境变量配置
# 复制此文件为 .env 并修改相应值

# CARLA设置
CARLA_HOST=localhost
CARLA_PORT=2000

# 数据库设置
DATABASE_PATH=traffic_data.db

# Web服务设置
WEB_PORT=5000
WEB_DEBUG=false

# 日志级别
LOG_LEVEL=INFO

# 模型保存路径
MODEL_SAVE_PATH=models/

# 分析输出路径
ANALYSIS_OUTPUT_PATH=analysis_output/
"""
        
        env_path = self.project_root / 'config' / 'env.example'
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_config)
        print(f"✅ {env_path}")
    
    def create_launch_scripts(self):
        """创建启动脚本"""
        print("\n🚀 创建启动脚本...")
        
        # Windows批处理脚本
        if self.system == "Windows":
            batch_script = """@echo off
echo 启动智能交通系统...
echo.

cd /d "%~dp0"

echo 检查Python环境...
python --version
if errorlevel 1 (
    echo Python未安装或不在PATH中
    pause
    exit /b 1
)

echo.
echo 选择运行模式:
echo 1. 训练模式
echo 2. 部署模式
echo 3. 性能分析
echo 4. Web监控
echo 5. 项目启动器
echo.

set /p choice="请输入选择 (1-5): "

if "%choice%"=="1" (
    echo 启动训练模式...
    python integrated_traffic_system.py
) else if "%choice%"=="2" (
    echo 启动部署模式...
    python integrated_traffic_system.py --deploy
) else if "%choice%"=="3" (
    echo 启动性能分析...
    python analyzer.py --summary
) else if "%choice%"=="4" (
    echo 启动Web监控...
    python web_server.py
) else if "%choice%"=="5" (
    echo 启动项目启动器...
    python launcher.py
) else (
    echo 无效选择
    pause
    exit /b 1
)

pause
"""
            
            script_path = self.project_root / 'scripts' / 'start.bat'
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(batch_script)
            print(f"✅ {script_path}")
        
        # Unix Shell脚本
        shell_script = """#!/bin/bash
# 智能交通系统启动脚本

echo "🚦 启动智能交通系统..."
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

echo "✅ Python环境正常"
echo ""

# 显示菜单
echo "选择运行模式:"
echo "1. 🎓 训练模式"
echo "2. 🚀 部署模式"
echo "3. 📊 性能分析"
echo "4. 🌐 Web监控"
echo "5. 🏗️ 项目启动器"
echo ""

read -p "请输入选择 (1-5): " choice

case $choice in
    1)
        echo "🎓 启动训练模式..."
        python3 integrated_traffic_system.py
        ;;
    2)
        echo "🚀 启动部署模式..."
        python3 integrated_traffic_system.py --deploy
        ;;
    3)
        echo "📊 启动性能分析..."
        python3 analyzer.py --summary
        ;;
    4)
        echo "🌐 启动Web监控..."
        python3 web_server.py
        ;;
    5)
        echo "🏗️ 启动项目启动器..."
        python3 launcher.py
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
"""
        
        script_path = self.project_root / 'scripts' / 'start.sh'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(shell_script)
        
        # 设置执行权限
        if self.system in ["Linux", "Darwin"]:
            os.chmod(script_path, 0o755)
        
        print(f"✅ {script_path}")
    
    def check_carla(self):
        """检查CARLA环境"""
        print("\n🚗 检查CARLA环境...")
        
        try:
            import carla
            print("✅ CARLA Python客户端已安装")
            
            # 尝试连接CARLA服务器
            try:
                client = carla.Client('localhost', 2000)
                client.set_timeout(2.0)
                world = client.get_world()
                print("✅ CARLA服务器连接成功")
                print(f"📍 当前地图: {world.get_map().name}")
            except Exception:
                print("⚠️  CARLA服务器未运行或无法连接")
                print("请确保CARLA仿真器正在运行在localhost:2000")
                
        except ImportError:
            print("❌ CARLA Python客户端未安装")
            print("请按照以下步骤安装CARLA:")
            print("1. 下载CARLA仿真器: https://github.com/carla-simulator/carla/releases")
            print("2. 安装Python客户端: pip install carla")
    
    def finish_setup(self):
        """完成安装"""
        print("\n🎉 安装完成!")
        print("=" * 60)
        print("项目已成功设置，你现在可以:")
        print("")
        print("1. 🚀 快速开始:")
        print("   python launcher.py")
        print("")
        print("2. 🎓 直接开始训练:")
        print("   python integrated_traffic_system.py")
        print("")
        print("3. 🌐 启动Web监控:")
        print("   打开浏览器访问: http://localhost:5000")
        print("")
        print("4. 📊 性能分析:")
        print("   python analyzer.py --summary")
        print("")
        print("📁 项目结构:")
        print("   ├── config/           # 配置文件")
        print("   ├── models/           # 训练模型")
        print("   ├── logs/             # 系统日志")
        print("   ├── data/             # 数据文件")
        print("   ├── analysis_output/  # 分析报告")
        print("   └── scripts/          # 启动脚本")
        print("")
        print("📖 使用说明:")
        print("   1. 确保CARLA仿真器正在运行")
        print("   2. 运行 python launcher.py 开始使用")
        print("   3. 选择训练模式开始AI学习")
        print("   4. 打开Web界面查看实时监控")
        print("")
        print("🆘 需要帮助?")
        print("   查看README.md或运行 python launcher.py")
        print("=" * 60)

def main():
    """主函数"""
    setup = ProjectSetup()
    
    print("欢迎使用智能交通系统安装向导!")
    print("此脚本将自动配置项目环境和依赖")
    print("")
    
    confirm = input("是否继续安装? (y/N): ").strip().lower()
    if confirm != 'y':
        print("安装已取消")
        return
    
    try:
        if setup.run_setup():
            print("\n✅ 安装成功完成!")
        else:
            print("\n❌ 安装过程中出现错误")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  安装被用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 安装失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())