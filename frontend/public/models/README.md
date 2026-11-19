# 登录页 3D 金箍棒（GLB）

默认文件：`ruyi-jingubang.glb`（供登录背景 `LoginRuyiStaff` 加载）。

## 更换为高精度模型（推荐）

1. 打开 [Kimi 如意金箍棒展示页](https://www.kimi.ai/showcases/3dmake/ruyi-jingubang)，在页面内下载 **GLB**（约 15 万三角面，含 PBR 材质）。
2. 将下载的文件重命名并覆盖为本目录下的 `ruyi-jingubang.glb`。
3. 刷新登录页即可。

也可在 `frontend/.env.development` 中设置自定义路径（无需改名）：

```text
VITE_LOGIN_STAFF_GLB=/models/你的模型.glb
```

## 自动下载（可选）

在 `frontend` 目录执行（依赖当前 Kimi 签名，可能失败则需手动下载）：

```powershell
npm run models:ruyi
```