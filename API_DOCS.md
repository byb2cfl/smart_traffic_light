 智能交通信号灯控制系统 API 文档

 概览

这是一个基于CARLA仿真平台和深度强化学习的智能交通信号灯控制系统的API文档。系统提供训练管理、实时监控、信号灯控制和数据分析等功能。

**基础URL**: `http://localhost:8080/api/v1`

**支持格式**: JSON

---

 认证

目前系统使用API密钥认证。在请求头中包含：

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

---

 核心API端点

 1. 系统管理

 获取系统状态

```http
GET /system/status
```

**响应示例**:
```json
{
  "status": "running",
  "mode": "training",
  "carla_connected": true,
  "total_vehicles": 28,
  "frame_count": 15420,
  "uptime": 3600,
  "version": "1.0.0"
}
```

 启动系统

```http
POST /system/start
```

**请求体**:
```json
{
  "mode": "training",
  "config": {
    "num_vehicles": 30,
    "auto_training": true
  }
}
```

 关闭系统

```http
POST /system/shutdown
```

 2. 训练管理

 开始训练

```http
POST /training/start
```

**请求体**:
```json
{
  "target_efficiency": 0.75,
  "target_mobility": 0.80,
  "target_reward": 0.50,
  "max_episodes": 1000,
  "auto_save_interval": 100
}
```

**响应示例**:
```json
{
  "training_id": "train_20250623_143022",
  "status": "started",
  "config": {
    "target_efficiency": 0.75,
    "target_mobility": 0.80,
    "target_reward": 0.50,
    "max_episodes": 1000
  },
  "estimated_duration": "2-4 hours"
}
```

 获取训练状态

```http
GET /training/status
```

**响应示例**:
```json
{
  "training_active": true,
  "episode_count": 156,
  "progress": 15.6,
  "current_metrics": {
    "avg_reward": 0.342,
    "efficiency": 0.68,
    "mobility": 0.72,
    "avg_speed": 28.5
  },
  "agent_stats": {
    "epsilon": 0.245,
    "memory_size": 8420,
    "avg_loss": 0.0123,
    "learn_steps": 3240
  },
  "targets_status": {
    "efficiency_met": false,
    "mobility_met": false,
    "reward_met": false,
    "stability_counter": 5
  }
}
```

 停止训练

```http
POST /training/stop
```

**响应示例**:
```json
{
  "status": "stopped",
  "final_episode": 234,
  "training_time": 7320,
  "final_metrics": {
    "avg_reward": 0.487,
    "efficiency": 0.73,
    "mobility": 0.79
  },
  "model_saved": true,
  "model_path": "/models/final_model_20250623_143022.pth"
}
```

 获取训练历史

```http
GET /training/history?episodes=50
```

**响应示例**:
```json
{
  "episodes": [
    {
      "episode": 200,
      "timestamp": "2025-06-23T14:30:22Z",
      "avg_reward": 0.456,
      "efficiency": 0.72,
      "mobility": 0.78,
      "avg_speed": 29.1,
      "total_vehicles": 28
    }
  ],
  "summary": {
    "total_episodes": 234,
    "best_episode": 189,
    "best_score": 0.523,
    "improvement_trend": "positive"
  }
}
```

 3. 模型管理

 获取模型列表

```http
GET /models
```

**响应示例**:
```json
{
  "models": [
    {
      "id": "best_model_ep189",
      "name": "best_model_ep189.pth",
      "type": "best",
      "size": "2.1MB",
      "created": "2025-06-23T14:30:22Z",
      "performance": {
        "score": 0.523,
        "efficiency": 0.76,
        "mobility": 0.81
      }
    },
    {
      "id": "auto_save_ep200",
      "name": "auto_save_ep200.pth", 
      "type": "checkpoint",
      "size": "2.1MB",
      "created": "2025-06-23T14:45:15Z"
    }
  ],
  "active_model": "best_model_ep189"
}
```

 加载模型

```http
POST /models/{model_id}/load
```

**响应示例**:
```json
{
  "status": "loaded",
  "model_id": "best_model_ep189",
  "model_info": {
    "episodes_trained": 189,
    "performance_score": 0.523,
    "architecture": "DQN",
    "state_size": 16,
    "action_size": 4
  }
}
```

 保存当前模型

```http
POST /models/save
```

**请求体**:
```json
{
  "name": "manual_save_v1",
  "description": "Manually saved after good performance"
}
```

 删除模型

```http
DELETE /models/{model_id}
```

 4. 交通监控

 获取实时交通数据

```http
GET /traffic/realtime
```

**响应示例**:
```json
{
  "timestamp": "2025-06-23T14:30:22Z",
  "global_stats": {
    "total_vehicles": 28,
    "total_stopped": 5,
    "avg_speed": 29.1,
    "congestion_ratio": 0.18,
    "mobility_score": 0.82,
    "efficiency_score": 0.74
  },
  "regional_data": {
    "center": {
      "vehicles": 12,
      "avg_speed": 24.5,
      "congestion": 0.25,
      "stopped": 3
    },
    "north": {
      "vehicles": 4,
      "avg_speed": 32.1,
      "congestion": 0.0,
      "stopped": 0
    },
    "south": {
      "vehicles": 5,
      "avg_speed": 35.2,
      "congestion": 0.2,
      "stopped": 1
    },
    "east": {
      "vehicles": 3,
      "avg_speed": 28.7,
      "congestion": 0.33,
      "stopped": 1
    },
    "west": {
      "vehicles": 4,
      "avg_speed": 30.1,
      "congestion": 0.0,
      "stopped": 0
    }
  }
}
```

 获取交通历史数据

```http
GET /traffic/history?start_time=2025-06-23T14:00:00Z&end_time=2025-06-23T15:00:00Z&interval=5m
```

**查询参数**:
- `start_time`: 开始时间 (ISO 8601)
- `end_time`: 结束时间 (ISO 8601)  
- `interval`: 数据间隔 (1m, 5m, 15m, 1h)

 获取性能指标

```http
GET /traffic/metrics
```

**响应示例**:
```json
{
  "current": {
    "efficiency": 0.74,
    "mobility": 0.82,
    "avg_waiting_time": 23.5,
    "throughput": 156.2,
    "fuel_consumption": 0.85
  },
  "compared_to_baseline": {
    "efficiency_improvement": 18.3,
    "mobility_improvement": 12.7,
    "waiting_time_reduction": 31.2,
    "fuel_savings": 15.8
  },
  "trends": {
    "efficiency": "improving",
    "mobility": "stable",
    "throughput": "improving"
  }
}
```

 5. 信号灯控制

 获取信号灯状态

```http
GET /traffic-lights
```

**响应示例**:
```json
{
  "traffic_lights": [
    {
      "id": "tl_001",
      "location": {"x": 100.5, "y": 200.3, "z": 0.5},
      "current_state": "green",
      "current_phase": 0,
      "time_remaining": 25.3,
      "total_phase_time": 35.0
    },
    {
      "id": "tl_002", 
      "location": {"x": -100.2, "y": 150.1, "z": 0.5},
      "current_state": "red",
      "current_phase": 1,
      "time_remaining": 12.7,
      "total_phase_time": 30.0
    }
  ],
  "coordination": {
    "synchronized": true,
    "pattern": "green_wave",
    "efficiency": 0.76
  }
}
```

 手动控制信号灯

```http
POST /traffic-lights/{light_id}/control
```

**请求体**:
```json
{
  "action": "switch_phase",
  "duration": 30,
  "emergency": false
}
```

**可用动作**:
- `extend_phase`: 延长当前相位
- `switch_phase`: 切换相位  
- `emergency_stop`: 紧急停止
- `optimize`: 智能优化

 批量控制信号灯

```http
POST /traffic-lights/batch-control
```

**请求体**:
```json
{
  "lights": ["tl_001", "tl_002"],
  "action": "synchronize",
  "pattern": "green_wave",
  "parameters": {
    "wave_speed": 50,
    "direction": "north_south"
  }
}
```

 6. 配置管理

 获取系统配置

```http
GET /config
```

**响应示例**:
```json
{
  "training": {
    "target_efficiency": 0.75,
    "target_mobility": 0.80,
    "target_reward": 0.50,
    "max_episodes": 1000,
    "stability_window": 20
  },
  "environment": {
    "carla_host": "localhost",
    "carla_port": 2000,
    "map": "Town03",
    "weather": "clear_noon"
  },
  "agent": {
    "learning_rate": 0.001,
    "epsilon": 0.5,
    "epsilon_decay": 0.995,
    "memory_size": 10000
  }
}
```

 更新配置

```http
PUT /config
```

**请求体**:
```json
{
  "training": {
    "target_efficiency": 0.80,
    "max_episodes": 1500
  },
  "agent": {
    "learning_rate": 0.0005
  }
}
```

 7. 数据分析

 生成分析报告

```http
POST /analytics/report
```

**请求体**:
```json
{
  "type": "performance",
  "period": "last_24h",
  "metrics": ["efficiency", "mobility", "throughput"],
  "format": "json"
}
```

**响应示例**:
```json
{
  "report_id": "rpt_20250623_143022",
  "generated_at": "2025-06-23T14:30:22Z",
  "period": {
    "start": "2025-06-22T14:30:22Z",
    "end": "2025-06-23T14:30:22Z"
  },
  "summary": {
    "avg_efficiency": 0.742,
    "avg_mobility": 0.819,
    "avg_throughput": 167.3,
    "total_vehicles_processed": 15847,
    "optimization_events": 234
  },
  "insights": [
    "效率在午高峰时段提升了23%",
    "北区交通流动性最佳",
    "建议在16:00-18:00增加信号灯响应频率"
  ]
}
```

 获取统计数据

```http
GET /analytics/stats?metric=efficiency&period=7d&granularity=1h
```

---

 WebSocket API

 实时数据流

连接到 `ws://localhost:8080/ws` 以获取实时数据更新。

**订阅消息**:
```json
{
  "action": "subscribe",
  "channels": ["traffic_data", "training_progress", "alerts"]
}
```

**数据消息示例**:
```json
{
  "channel": "traffic_data",
  "timestamp": "2025-06-23T14:30:22Z",
  "data": {
    "total_vehicles": 28,
    "avg_speed": 29.1,
    "efficiency": 0.74
  }
}
```

---

 错误处理

 HTTP状态码

- `200 OK` - 请求成功
- `201 Created` - 资源创建成功
- `400 Bad Request` - 请求参数错误
- `401 Unauthorized` - 认证失败
- `404 Not Found` - 资源不存在
- `409 Conflict` - 资源冲突（如训练已在进行）
- `500 Internal Server Error` - 服务器内部错误

 错误响应格式

```json
{
  "error": {
    "code": "TRAINING_ALREADY_ACTIVE",
    "message": "训练已在进行中，请先停止当前训练",
    "details": {
      "current_episode": 156,
      "training_id": "train_20250623_143022"
    },
    "timestamp": "2025-06-23T14:30:22Z"
  }
}
```

---

 SDK示例

 Python SDK

```python
import requests
from datetime import datetime

class TrafficControlAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def start_training(self, config=None):
        """开始训练"""
        url = f"{self.base_url}/training/start"
        response = requests.post(url, json=config, headers=self.headers)
        return response.json()
    
    def get_traffic_data(self):
        """获取实时交通数据"""
        url = f"{self.base_url}/traffic/realtime"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def control_traffic_light(self, light_id, action, **params):
        """控制信号灯"""
        url = f"{self.base_url}/traffic-lights/{light_id}/control"
        data = {'action': action, **params}
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()

 使用示例
api = TrafficControlAPI('http://localhost:8080/api/v1', 'your_api_key')

 开始训练
training_result = api.start_training({
    'target_efficiency': 0.80,
    'max_episodes': 500
})

 获取交通数据
traffic_data = api.get_traffic_data()
print(f"当前效率: {traffic_data['global_stats']['efficiency_score']}")

 控制信号灯
api.control_traffic_light('tl_001', 'extend_phase', duration=15)
```

 JavaScript SDK

```javascript
class TrafficControlAPI {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    
    async startTraining(config = {}) {
        const response = await fetch(`${this.baseUrl}/training/start`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify(config)
        });
        return response.json();
    }
    
    async getTrafficData() {
        const response = await fetch(`${this.baseUrl}/traffic/realtime`, {
            headers: this.headers
        });
        return response.json();
    }
    
    // WebSocket连接
    connectWebSocket() {
        const ws = new WebSocket('ws://localhost:8080/ws');
        
        ws.onopen = () => {
            ws.send(JSON.stringify({
                action: 'subscribe',
                channels: ['traffic_data', 'training_progress']
            }));
        };
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log('实时数据:', data);
        };
        
        return ws;
    }
}
```

---

 部署指南

 Docker部署

```yaml
version: '3.8'
services:
  traffic-control-api:
    image: traffic-control:latest
    ports:
      - "8080:8080"
    environment:
      - CARLA_HOST=carla-server
      - CARLA_PORT=2000
      - API_KEY=your_secure_api_key
    depends_on:
      - carla-server
      - redis
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
  
  carla-server:
    image: carlasim/carla:0.9.13
    ports:
      - "2000:2000"
    command: /bin/bash CarlaUE4.sh -world-port=2000
```

 环境要求

- Python 3.8+
- PyTorch 1.8+ (可选，用于DQN)
- CARLA 0.9.13+
- Redis (用于缓存)
- Docker (推荐)

---
