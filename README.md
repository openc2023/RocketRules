# RocketRules

模块化 Shadowrocket 规则选择器，用 GitHub Pages 托管。勾选规则组，生成 `.conf`
配置文件；也可以直接用仓库里现成的远程配置，一键导入 Shadowrocket。

## 用法

1. 打开 Pages 页面（先在 Settings → Pages → Deploy from a branch → main / (root) 启用）。
2. **现成配置**：点「一键导入 Shadowrocket」直接添加；没反应就复制远程配置地址，
   到 Shadowrocket「配置」→ 右上角 + → 粘贴 → Download → 点一下启用。
3. **自选规则**：勾选需要的组，点「下载 .conf」，在 Shadowrocket「配置」中导入，
   再选择你已有的代理节点，全局路由选「配置」。
4. **分享网址**：复制的网址只用来打开本页面并恢复勾选，**不是**订阅链接。
   想长期订阅自选配置：把下载的 `.conf` 传到仓库 `configs/` 文件夹，
   页面第 4 节会给出对应的远程配置地址和一键导入链接。

默认只勾 Meta 全家桶和 IP 测试网站（`?r=` 参数会记住勾选）。

## 预设配置

| 配置 | 内容 |
| --- | --- |
| `configs/meta-only.conf` | Meta 全家桶 + IP 测试 |
| `configs/ai-only.conf` | ChatGPT、Claude、Gemini、Grok + IP 测试 |
| `configs/social-only.conf` | Meta、TikTok、Telegram、X、Discord + IP 测试 |
| `configs/combined.conf` | 全部 12 组 |

## 加一组新规则

1. 在 `rules/` 下新建 `xxx.list`，每行写 `DOMAIN-SUFFIX,example.com`。
2. 在 `index.html` 的 `ORDER` 和 `META` 里加一行（名字、一句话说明、是否默认勾选）。
3. 如需预设配置，运行 `python3 tools/gen.py` 重新生成 `configs/*.conf`。

页面启动时会先读 `rules/*.list`（唯一数据源），读不到才用页面内置备份，
并校验域名格式和重复，发现问题会在页面上提示。

不含任何代理账号密码；下载后在 Shadowrocket 里选择你已有的代理节点。
