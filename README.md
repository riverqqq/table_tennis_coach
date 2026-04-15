# 乒乓球场外教练 MVP

这是一个可以在手机浏览器打开的最小可用原型。

## 现在具备的能力

- 记录得分按钮和失分按钮
- 每次点击给对应标签加 1
- 支持最多选择 3 个对手特征
- 点击“开始布置战术”后，根据本局累计事件生成下一局建议
- 输出包括：局势判断、主战术、风险提醒、3 条执行建议

## 项目结构

```text
app/
  main.py               FastAPI 入口
  models.py             Pydantic 请求/响应模型
  analysis.py           局势分析层
  rules_engine.py       战术规则引擎
  tags.py               标签库
  static/
    index.html          页面
    styles.css          样式
    app.js              前端逻辑
tests/
  test_rules.py         本地规则测试
requirements.txt
```

## 本地运行

### 1. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动后端

```bash
uvicorn app.main:app --reload
```

### 4. 打开浏览器

访问：

```text
http://127.0.0.1:8000
```

手机同局域网测试时，把 `127.0.0.1` 换成你电脑的局域网 IP。

## 操作说明

- 左边是得分按钮，右边是失分按钮
- 左键点击：该标签 +1
- 右键点击：该标签 -1
- 下面可以选最多 3 个对手特征
- 点击“开始布置战术”生成下一局建议
- 点击“清空本局记录”重置本局数据

## 你下一步最值得做的升级

1. 增加每局独立保存，而不是只有当前局
2. 增加赛后总结页
3. 增加用户技能包，让建议只使用用户会的技术
4. 增加比赛创建页（赛制、对手备注、器材）
5. 增加规则配置文件，让规则不写死在 Python 里
