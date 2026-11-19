<script setup>
import * as THREE from 'three'
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js'
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js'
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js'
import { onMounted, onUnmounted, ref } from 'vue'

const host = ref(null)

let renderer
let composer
let scene
let camera
let staff
let frameId = 0
let clock
let reduceMotion = false
const texturesToDispose = []

/** 金色卷草祥云雕纹（贴于套筒） */
function createGoldFiligreeTextures() {
  const size = 512
  const colorCanvas = document.createElement('canvas')
  colorCanvas.width = size
  colorCanvas.height = size
  const colorCtx = colorCanvas.getContext('2d')

  const bumpCanvas = document.createElement('canvas')
  bumpCanvas.width = size
  bumpCanvas.height = size
  const bumpCtx = bumpCanvas.getContext('2d')

  const g = colorCtx.createLinearGradient(0, 0, size, size)
  g.addColorStop(0, '#8a6420')
  g.addColorStop(0.35, '#e8c55a')
  g.addColorStop(0.55, '#fff0a8')
  g.addColorStop(0.72, '#d4a832')
  g.addColorStop(1, '#705318')
  colorCtx.fillStyle = g
  colorCtx.fillRect(0, 0, size, size)

  bumpCtx.fillStyle = '#7a7a7a'
  bumpCtx.fillRect(0, 0, size, size)

  function scrollMotif(ctx, bctx, baseX, baseY, flip) {
    const s = flip ? -1 : 1
    ctx.strokeStyle = '#6b4e14'
    ctx.lineWidth = 2.5
    bctx.strokeStyle = '#b5b5b5'
    bctx.lineWidth = 3.5
    const draw = (c, stroke) => {
      c.beginPath()
      c.moveTo(baseX, baseY)
      c.bezierCurveTo(baseX + 22 * s, baseY - 28, baseX + 48 * s, baseY + 18, baseX + 70 * s, baseY)
      c.bezierCurveTo(baseX + 92 * s, baseY - 22, baseX + 110 * s, baseY + 24, baseX + 130 * s, baseY - 4)
      c.strokeStyle = stroke
      c.stroke()
    }
    draw(ctx, '#6b4e14')
    draw(bctx, '#c0c0c0')
    ctx.fillStyle = 'rgba(100, 70, 20, 0.35)'
    bctx.fillStyle = '#a8a8a8'
    for (let k = 0; k < 3; k++) {
      const px = baseX + (30 + k * 28) * s
      const py = baseY + (k % 2) * 10 - 5
      ctx.beginPath()
      ctx.arc(px, py, 5, 0, Math.PI * 2)
      ctx.fill()
      bctx.beginPath()
      bctx.arc(px, py, 5, 0, Math.PI * 2)
      bctx.fill()
    }
  }

  for (let row = 0; row < 6; row++) {
    for (let col = 0; col < 5; col++) {
      scrollMotif(
        colorCtx,
        bumpCtx,
        (col / 5) * size + 40,
        (row / 6) * size + 36,
        (row + col) % 2 === 0,
      )
    }
  }

  const map = new THREE.CanvasTexture(colorCanvas)
  const bumpMap = new THREE.CanvasTexture(bumpCanvas)
  for (const tex of [map, bumpMap]) {
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping
    tex.repeat.set(1.8, 1)
    tex.anisotropy = 8
    texturesToDispose.push(tex)
  }
  map.colorSpace = THREE.SRGBColorSpace
  bumpMap.colorSpace = THREE.NoColorSpace
  return { map, bumpMap }
}

/** 深绛红漆杆（偏哑光） */
function createBurgundyTexture() {
  const w = 128
  const h = 512
  const canvas = document.createElement('canvas')
  canvas.width = w
  canvas.height = h
  const ctx = canvas.getContext('2d')
  const lacquer = ctx.createLinearGradient(0, 0, w, 0)
  lacquer.addColorStop(0, '#4a0a10')
  lacquer.addColorStop(0.3, '#7a1018')
  lacquer.addColorStop(0.5, '#8b1420')
  lacquer.addColorStop(0.7, '#6e0f16')
  lacquer.addColorStop(1, '#3d080c')
  ctx.fillStyle = lacquer
  ctx.fillRect(0, 0, w, h)
  const map = new THREE.CanvasTexture(canvas)
  map.wrapS = THREE.RepeatWrapping
  map.anisotropy = 8
  map.colorSpace = THREE.SRGBColorSpace
  texturesToDispose.push(map)
  return map
}

function makeGoldCarved(tex) {
  return new THREE.MeshPhysicalMaterial({
    color: 0xffffff,
    map: tex.map,
    bumpMap: tex.bumpMap,
    bumpScale: 0.038,
    metalness: 1,
    roughness: 0.16,
    clearcoat: 0.65,
    clearcoatRoughness: 0.08,
    envMapIntensity: 1.45,
    emissive: 0xffb84d,
    emissiveIntensity: 0.12,
  })
}

function makeGoldPolished() {
  return new THREE.MeshPhysicalMaterial({
    color: 0xffe7a0,
    metalness: 1,
    roughness: 0.08,
    clearcoat: 0.85,
    clearcoatRoughness: 0.05,
    envMapIntensity: 1.75,
    emissive: 0xffcc66,
    emissiveIntensity: 0.22,
  })
}

function makeBurgundyShaft(map) {
  return new THREE.MeshPhysicalMaterial({
    color: 0xffffff,
    map,
    metalness: 0.02,
    roughness: 0.48,
    clearcoat: 0.35,
    clearcoatRoughness: 0.35,
    envMapIntensity: 0.35,
  })
}

function addShaftCyl(group, r, len, mat, cx = 0) {
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len, 64), mat)
  mesh.rotation.z = Math.PI / 2
  mesh.position.x = cx
  group.add(mesh)
}

/** 模板结构：金箍 → 雕花金套筒 → 平口金帽 */
function addTemplateEnd(group, sign, joinX, r, carvedMat, polishMat) {
  const d = sign
  const junctionX = joinX + d * 0.02

  const hoop = new THREE.Mesh(
    new THREE.TorusGeometry(r * 1.12, r * 0.07, 16, 64),
    polishMat,
  )
  hoop.rotation.y = Math.PI / 2
  hoop.position.x = junctionX
  group.add(hoop)

  const collar = new THREE.Mesh(
    new THREE.CylinderGeometry(r * 1.18, r * 1.18, r * 0.2, 48),
    polishMat,
  )
  collar.rotation.z = Math.PI / 2
  collar.position.x = junctionX + d * r * 0.14
  group.add(collar)

  const sleeveLen = 0.58
  const sleeveR = r * 1.32
  const sleeveX = junctionX + d * (r * 0.14 + sleeveLen / 2 + 0.02)
  addShaftCyl(group, sleeveR, sleeveLen, carvedMat, sleeveX)

  const sleeveRing = new THREE.Mesh(
    new THREE.TorusGeometry(sleeveR * 1.02, r * 0.05, 14, 56),
    polishMat,
  )
  sleeveRing.rotation.y = Math.PI / 2
  sleeveRing.position.x = sleeveX
  group.add(sleeveRing)

  const capLen = 0.11
  const capR = sleeveR * 0.96
  const capX = junctionX + d * (r * 0.14 + sleeveLen + capLen / 2 + 0.05)
  addShaftCyl(group, capR, capLen, polishMat, capX)

  const tipDisc = new THREE.Mesh(
    new THREE.CylinderGeometry(capR * 1.02, capR * 1.02, r * 0.035, 48),
    polishMat,
  )
  tipDisc.rotation.z = Math.PI / 2
  tipDisc.position.x = capX + d * (capLen / 2 + r * 0.02)
  group.add(tipDisc)
}

function buildStaff() {
  const group = new THREE.Group()
  const filigree = createGoldFiligreeTextures()
  const burgundyMap = createBurgundyTexture()
  const carvedMat = makeGoldCarved(filigree)
  const polishMat = makeGoldPolished()
  const redMat = makeBurgundyShaft(burgundyMap)

  const r = 0.098
  const shaftLen = 4.35
  const half = shaftLen / 2

  addShaftCyl(group, r, shaftLen, redMat)

  const centerCollar = new THREE.Mesh(
    new THREE.CylinderGeometry(r * 1.22, r * 1.22, r * 0.14, 48),
    polishMat,
  )
  centerCollar.rotation.z = Math.PI / 2
  group.add(centerCollar)

  const centerFiligree = new THREE.Mesh(
    new THREE.TorusGeometry(r * 1.42, r * 0.045, 16, 64),
    carvedMat,
  )
  centerFiligree.rotation.y = Math.PI / 2
  group.add(centerFiligree)

  const centerGem = new THREE.Mesh(
    new THREE.OctahedronGeometry(r * 0.22, 0),
    polishMat,
  )
  centerGem.rotation.z = Math.PI / 4
  group.add(centerGem)

  addTemplateEnd(group, 1, half, r, carvedMat, polishMat)
  addTemplateEnd(group, -1, -half, r, carvedMat, polishMat)

  group.rotation.set(0.22, -0.42, 0.62)
  return group
}

function resize() {
  if (!host.value || !renderer || !camera) return
  const w = host.value.clientWidth
  const h = host.value.clientHeight
  if (w < 1 || h < 1) return
  camera.aspect = w / h
  camera.updateProjectionMatrix()
  renderer.setSize(w, h, false)
  composer?.setSize(w, h)
}

function tick() {
  frameId = requestAnimationFrame(tick)
  const t = clock.getElapsedTime()
  if (staff) {
    const speed = reduceMotion ? 0.05 : 1
    staff.rotation.y = t * 0.28 * speed
    staff.rotation.x = 0.22 + Math.sin(t * 0.45 * speed) * 0.07
    staff.rotation.z = 0.62 + Math.cos(t * 0.35 * speed) * 0.04
    staff.position.y = Math.sin(t * 0.65 * speed) * 0.1
    staff.position.x = 0.78 + Math.cos(t * 0.22 * speed) * 0.06
  }
  if (composer) composer.render()
  else renderer?.render(scene, camera)
}

onMounted(() => {
  reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (!host.value) return

  clock = new THREE.Clock()
  scene = new THREE.Scene()

  camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100)
  camera.position.set(-0.2, 0.08, 7.2)

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true, powerPreference: 'high-performance' })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setClearColor(0x000000, 0)
  renderer.outputColorSpace = THREE.SRGBColorSpace
  renderer.toneMapping = THREE.ACESFilmicToneMapping
  renderer.toneMappingExposure = 1.22
  host.value.appendChild(renderer.domElement)
  renderer.domElement.className = 'staff-gl'

  const pmrem = new THREE.PMREMGenerator(renderer)
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture
  pmrem.dispose()

  composer = new EffectComposer(renderer)
  composer.addPass(new RenderPass(scene, camera))
  const bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), 0.42, 0.55, 0.2)
  bloom.threshold = 0.62
  bloom.strength = reduceMotion ? 0.15 : 0.42
  bloom.radius = 0.55
  composer.addPass(bloom)

  scene.add(new THREE.AmbientLight(0x9090a0, 0.55))
  scene.add(new THREE.HemisphereLight(0xfff8ee, 0x1a1020, 0.55))

  const key = new THREE.DirectionalLight(0xffffff, 2)
  key.position.set(5, 4, 6)
  scene.add(key)

  const goldLight = new THREE.SpotLight(0xffe2a0, 2.8, 28, Math.PI / 5, 0.35)
  goldLight.position.set(2, 3, 7)
  scene.add(goldLight)

  const fill = new THREE.DirectionalLight(0xc4b5fd, 0.35)
  fill.position.set(-3, -2, 4)
  scene.add(fill)

  staff = buildStaff()
  staff.position.set(0.82, -0.06, 0)
  staff.scale.setScalar(1.3)
  scene.add(staff)

  resize()
  window.addEventListener('resize', resize)
  tick()
})

onUnmounted(() => {
  cancelAnimationFrame(frameId)
  window.removeEventListener('resize', resize)
  texturesToDispose.forEach((t) => t.dispose())
  composer?.dispose()
  staff?.traverse((obj) => {
    if (obj.isMesh) {
      obj.geometry?.dispose()
      if (Array.isArray(obj.material)) obj.material.forEach((m) => m.dispose())
      else obj.material?.dispose()
    }
  })
  renderer?.dispose()
  if (renderer?.domElement?.parentNode) {
    renderer.domElement.parentNode.removeChild(renderer.domElement)
  }
})
</script>

<template>
  <div ref="host" class="staff-stage" aria-hidden="true" />
</template>

<style scoped>
.staff-stage {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.staff-stage :deep(.staff-gl) {
  display: block;
  width: 100% !important;
  height: 100% !important;
  object-fit: cover;
  opacity: 0.97;
  filter:
    drop-shadow(0 0 48px rgba(255, 196, 90, 0.45))
    drop-shadow(0 16px 36px rgba(0, 0, 0, 0.35));
}
</style>