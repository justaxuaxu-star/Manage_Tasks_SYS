import { mkdir, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const outDir = path.join(root, 'public', 'models')
const outFile = path.join(outDir, 'ruyi-jingubang.glb')

const showcaseUrl = 'https://www.kimi.ai/showcases/3dmake/ruyi-jingubang'

async function main() {
  const pageRes = await fetch(showcaseUrl, {
    headers: { 'user-agent': 'Mozilla/5.0', accept: 'text/html' },
  })
  if (!pageRes.ok) throw new Error(`无法打开 Kimi 展示页：${pageRes.status}`)
  const html = await pageRes.text()
  const match = html.match(/model=(https%3A%2F%2F[^&"\s]+)/)
  if (!match) throw new Error('未在页面中找到 GLB 下载地址，请手动下载后放入 public/models/ruyi-jingubang.glb')
  const modelUrl = decodeURIComponent(match[1])
  const glbRes = await fetch(modelUrl, {
    headers: {
      referer: showcaseUrl,
      'user-agent': 'Mozilla/5.0',
    },
  })
  if (!glbRes.ok) throw new Error(`GLB 下载失败（${glbRes.status}），签名可能已过期，请从浏览器手动下载`)
  const buf = Buffer.from(await glbRes.arrayBuffer())
  if (buf.length < 10_000) throw new Error('下载文件过小，可能不是有效 GLB')
  await mkdir(outDir, { recursive: true })
  await writeFile(outFile, buf)
  console.log(`已保存 ${outFile}（${(buf.length / 1024 / 1024).toFixed(2)} MB）`)
}

main().catch((err) => {
  console.error(err.message)
  process.exit(1)
})