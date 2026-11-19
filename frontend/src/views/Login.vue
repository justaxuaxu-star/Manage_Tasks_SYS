<script setup>
import { defineAsyncComponent, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login } from '../stores/auth'

const LoginRuyiStaff = defineAsyncComponent(() => import('../components/LoginRuyiStaff.vue'))

const route = useRoute()
const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

async function submit() {
  loading.value = true
  error.value = ''
  try {
    await login(username.value, password.value)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
    router.replace(redirect)
  } catch {
    error.value = '认证失败：账号或密码不正确'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-root">
    <div class="bg-layer" aria-hidden="true">
      <LoginRuyiStaff class="staff-bg" />
      <div class="orb orb-a" />
      <div class="orb orb-b" />
      <div class="orb orb-c" />
      <div class="grid-floor" />
      <div class="scan-line" />
      <div class="particles">
        <i v-for="n in 24" :key="n" class="particle" :style="{ '--i': n }" />
      </div>
    </div>

    <div class="login-shell">
      <header class="brand-panel">
        <div class="brand-badge">
          <span class="badge-ring" />
          <span class="badge-core">数据中心</span>
        </div>
        <p class="brand-tag">QITIANDASHENG TECH</p>
        <h1 class="brand-title">
          <span class="title-glow">齐天大圣科技</span>
          <span class="title-sub">数据中心后台</span>
        </h1>
        <p class="brand-desc">
          统一身份认证 · 任务协同 · 权限治理<br />
          接入企业级 RBAC 与安全会话通道
        </p>
        <ul class="brand-metrics">
          <li>
            <strong>JWT</strong>
            <span>会话加密</span>
          </li>
          <li>
            <strong>RBAC</strong>
            <span>细粒度授权</span>
          </li>
          <li>
            <strong>实时</strong>
            <span>任务态势感知</span>
          </li>
        </ul>
      </header>

      <section class="form-panel" aria-labelledby="login-heading">
        <div class="form-glow" aria-hidden="true" />
        <div class="form-inner">
          <div class="form-header">
            <p class="form-eyebrow">SECURE ACCESS GATEWAY</p>
            <h2 id="login-heading">身份验证</h2>
            <p class="form-hint">请使用已授权账号登录数据中心管理后台</p>
          </div>

          <form class="login-form" @submit.prevent="submit">
            <label class="field">
              <span class="field-label">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 12a5 5 0 1 0-5-5 5 5 0 0 0 5 5zm0 2c-4.2 0-8 2.2-8 5v1h16v-1c0-2.8-3.8-5-8-5z" /></svg>
                用户名
              </span>
              <input
                v-model="username"
                autocomplete="username"
                placeholder="请输入用户名"
                required
              />
            </label>

            <label class="field">
              <span class="field-label">
                <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17 9h-1V7a4 4 0 0 0-8 0v2H7a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2zm-3 0H10V7a2 2 0 1 1 4 0z" /></svg>
                密码
              </span>
              <div class="password-wrap">
                <input
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  autocomplete="current-password"
                  placeholder="请输入密码"
                  required
                />
                <button
                  class="toggle-pwd"
                  type="button"
                  :aria-label="showPassword ? '隐藏密码' : '显示密码'"
                  @click="showPassword = !showPassword"
                >
                  {{ showPassword ? '隐藏' : '显示' }}
                </button>
              </div>
            </label>

            <p v-if="error" class="form-error" role="alert">{{ error }}</p>

            <button class="submit-btn" type="submit" :disabled="loading">
              <span class="submit-shine" aria-hidden="true" />
              <span class="submit-text">{{ loading ? '正在建立安全会话…' : '进入数据中心后台' }}</span>
            </button>
          </form>

          <p class="form-footer">
            开发演示账号：admin / admin123
          </p>
        </div>
      </section>
    </div>

    <footer class="login-footer">© 齐天大圣科技 · 数据中心运营平台</footer>
  </div>
</template>

<style scoped>
.login-root {
  --cyan: #22d3ee;
  --violet: #a855f7;
  --gold: #fbbf24;
  --deep: #030712;
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  color: #e2e8f0;
  background: var(--deep);
  font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
}

.bg-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.staff-bg {
  z-index: 0;
  mask-image: radial-gradient(ellipse 80% 65% at 36% 52%, #000 28%, transparent 78%);
  -webkit-mask-image: radial-gradient(ellipse 80% 65% at 36% 52%, #000 28%, transparent 78%);
}

.orb {
  z-index: 1;
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.55;
  animation: float-orb 18s ease-in-out infinite;
}

.orb-a {
  width: 420px;
  height: 420px;
  left: -8%;
  top: 10%;
  background: radial-gradient(circle, var(--cyan), transparent 70%);
}

.orb-b {
  width: 520px;
  height: 520px;
  right: -12%;
  top: 30%;
  background: radial-gradient(circle, var(--violet), transparent 70%);
  animation-delay: -6s;
}

.orb-c {
  width: 360px;
  height: 360px;
  left: 40%;
  bottom: -10%;
  background: radial-gradient(circle, var(--gold), transparent 70%);
  animation-delay: -12s;
  opacity: 0.35;
}

@keyframes float-orb {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(24px, -20px) scale(1.08);
  }
}

.grid-floor {
  z-index: 1;
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(34, 211, 238, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34, 211, 238, 0.08) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(ellipse 80% 60% at 50% 100%, black 20%, transparent 75%);
  transform: perspective(400px) rotateX(60deg) scale(1.4);
  transform-origin: center bottom;
  opacity: 0.45;
}

.scan-line {
  z-index: 2;
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--cyan), var(--violet), transparent);
  box-shadow: 0 0 24px var(--cyan);
  animation: scan 6s linear infinite;
  opacity: 0.7;
}

@keyframes scan {
  0% {
    top: -2%;
  }
  100% {
    top: 102%;
  }
}

.particles {
  z-index: 2;
  position: absolute;
  inset: 0;
}

.particle {
  position: absolute;
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: var(--cyan);
  box-shadow: 0 0 8px var(--cyan);
  left: calc((var(--i) * 4.3%) % 100%);
  top: calc((var(--i) * 7.1%) % 100%);
  animation: twinkle calc(2s + (var(--i) % 5) * 0.4s) ease-in-out infinite;
  animation-delay: calc(var(--i) * -0.15s);
  opacity: 0.35;
}

@keyframes twinkle {
  0%,
  100% {
    opacity: 0.15;
    transform: scale(1);
  }
  50% {
    opacity: 0.9;
    transform: scale(1.6);
  }
}

.login-shell {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(340px, 440px);
  gap: clamp(24px, 5vw, 64px);
  align-items: center;
  min-height: 100vh;
  padding: clamp(24px, 5vw, 72px);
  max-width: 1200px;
  margin: 0 auto;
}

.brand-panel {
  padding-right: clamp(0px, 4vw, 32px);
}

.brand-badge {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.badge-ring {
  position: absolute;
  width: 88px;
  height: 88px;
  border-radius: 50%;
  border: 1px solid rgba(34, 211, 238, 0.4);
  box-shadow: 0 0 30px rgba(34, 211, 238, 0.25);
  animation: spin-slow 12s linear infinite;
}

.badge-ring::after {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 1px dashed rgba(251, 191, 36, 0.35);
  animation: spin-slow 18s linear infinite reverse;
}

@keyframes spin-slow {
  to {
    transform: rotate(360deg);
  }
}

.badge-core {
  position: relative;
  padding: 10px 16px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.2em;
  color: var(--gold);
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid rgba(251, 191, 36, 0.35);
  border-radius: 999px;
}

.brand-tag {
  margin: 0 0 12px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.35em;
  color: rgba(34, 211, 238, 0.75);
}

.brand-title {
  margin: 0 0 20px;
  line-height: 1.25;
}

.title-glow {
  display: block;
  font-size: clamp(1.75rem, 4vw, 2.75rem);
  font-weight: 800;
  background: linear-gradient(105deg, #fff 0%, var(--cyan) 45%, var(--gold) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 40px rgba(34, 211, 238, 0.35);
}

.title-sub {
  display: block;
  margin-top: 8px;
  font-size: clamp(1.25rem, 2.5vw, 1.65rem);
  font-weight: 600;
  color: rgba(226, 232, 240, 0.92);
}

.brand-desc {
  margin: 0 0 28px;
  max-width: 28em;
  font-size: 14px;
  line-height: 1.75;
  color: rgba(148, 163, 184, 0.95);
}

.brand-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  list-style: none;
  margin: 0;
  padding: 0;
}

.brand-metrics li {
  flex: 1 1 100px;
  padding: 14px 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(34, 211, 238, 0.08), rgba(168, 85, 247, 0.08));
  border: 1px solid rgba(148, 163, 184, 0.15);
  backdrop-filter: blur(8px);
}

.brand-metrics strong {
  display: block;
  font-size: 13px;
  color: var(--cyan);
  margin-bottom: 4px;
}

.brand-metrics span {
  font-size: 12px;
  color: rgba(148, 163, 184, 0.9);
}

.form-panel {
  position: relative;
  border-radius: 20px;
  padding: 2px;
  background: linear-gradient(135deg, rgba(34, 211, 238, 0.6), rgba(168, 85, 247, 0.5), rgba(251, 191, 36, 0.4));
  box-shadow:
    0 0 60px rgba(34, 211, 238, 0.15),
    0 25px 50px rgba(0, 0, 0, 0.45);
  animation: border-pulse 4s ease-in-out infinite;
}

@keyframes border-pulse {
  0%,
  100% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.15);
  }
}

.form-glow {
  position: absolute;
  inset: 0;
  border-radius: 20px;
  background: radial-gradient(circle at 30% 0%, rgba(34, 211, 238, 0.2), transparent 55%);
  pointer-events: none;
}

.form-inner {
  position: relative;
  padding: clamp(28px, 4vw, 40px);
  border-radius: 18px;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(20px);
}

.form-eyebrow {
  margin: 0 0 8px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.28em;
  color: var(--violet);
}

.form-header h2 {
  margin: 0 0 8px;
  font-size: 1.5rem;
  font-weight: 700;
  color: #f8fafc;
}

.form-hint {
  margin: 0 0 24px;
  font-size: 13px;
  color: rgba(148, 163, 184, 0.95);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: rgba(226, 232, 240, 0.9);
}

.field-label svg {
  width: 16px;
  height: 16px;
  fill: var(--cyan);
  opacity: 0.9;
}

.field input {
  width: 100%;
  padding: 14px 16px;
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  background: rgba(3, 7, 18, 0.65);
  color: #f1f5f9;
  transition:
    border-color 0.2s,
    box-shadow 0.2s,
    background 0.2s;
}

.field input::placeholder {
  color: rgba(100, 116, 139, 0.85);
}

.field input:focus {
  outline: none;
  border-color: rgba(34, 211, 238, 0.65);
  box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.15), 0 0 24px rgba(34, 211, 238, 0.12);
  background: rgba(3, 7, 18, 0.9);
}

.password-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.password-wrap input {
  padding-right: 72px;
}

.toggle-pwd {
  position: absolute;
  right: 8px;
  padding: 6px 10px;
  font-size: 12px;
  color: var(--cyan);
  background: transparent;
  border: none;
  border-radius: 8px;
}

.toggle-pwd:hover {
  background: rgba(34, 211, 238, 0.1);
}

.form-error {
  margin: 0;
  padding: 10px 12px;
  font-size: 13px;
  color: #fecaca;
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.35);
  border-radius: 10px;
}

.submit-btn {
  position: relative;
  margin-top: 6px;
  padding: 15px 20px;
  border: none;
  border-radius: 12px;
  overflow: hidden;
  font-size: 15px;
  font-weight: 700;
  color: #030712;
  background: linear-gradient(90deg, var(--cyan), #38bdf8, var(--gold));
  box-shadow: 0 8px 32px rgba(34, 211, 238, 0.35);
  transition: transform 0.15s, box-shadow 0.2s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 12px 40px rgba(34, 211, 238, 0.45);
}

.submit-btn:disabled {
  opacity: 0.7;
}

.submit-shine {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    105deg,
    transparent 30%,
    rgba(255, 255, 255, 0.45) 50%,
    transparent 70%
  );
  transform: translateX(-100%);
  animation: shine 3s ease-in-out infinite;
}

@keyframes shine {
  0% {
    transform: translateX(-100%);
  }
  60%,
  100% {
    transform: translateX(100%);
  }
}

.submit-text {
  position: relative;
  z-index: 1;
}

.form-footer {
  margin: 20px 0 0;
  font-size: 12px;
  text-align: center;
  color: rgba(100, 116, 139, 0.9);
}

.login-footer {
  position: relative;
  z-index: 1;
  padding: 16px;
  text-align: center;
  font-size: 12px;
  color: rgba(100, 116, 139, 0.75);
}

@media (max-width: 900px) {
  .staff-bg {
    mask-image: radial-gradient(ellipse 90% 50% at 50% 38%, #000 22%, transparent 80%);
    -webkit-mask-image: radial-gradient(ellipse 90% 50% at 50% 38%, #000 22%, transparent 80%);
  }

  .login-shell {
    grid-template-columns: 1fr;
    justify-items: center;
    padding-top: 48px;
    padding-bottom: 80px;
  }

  .brand-panel {
    text-align: center;
    padding-right: 0;
  }

  .brand-desc {
    margin-left: auto;
    margin-right: auto;
  }

  .brand-metrics {
    justify-content: center;
  }

  .form-panel {
    width: min(440px, 100%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .orb,
  .scan-line,
  .particle,
  .badge-ring,
  .submit-shine,
  .form-panel {
    animation: none;
  }
}
</style>