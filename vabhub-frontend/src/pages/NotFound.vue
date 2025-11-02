<template>
  <div class="not-found-page">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <div class="error-message">
        <h1>页面未找到</h1>
        <p>抱歉，您访问的页面不存在或已被移动。</p>
      </div>
      <div class="error-actions">
        <button class="btn btn-primary" @click="goHome">
          <span class="btn-icon">🏠</span>
          返回首页
        </button>
        <button class="btn btn-secondary" @click="goBack">
          <span class="btn-icon">↩️</span>
          返回上一页
        </button>
      </div>
      <div class="error-help">
        <p>如果您认为这是一个错误，请联系系统管理员。</p>
        <div class="help-links">
          <a href="#" @click.prevent="showHelp">帮助中心</a>
          <a href="#" @click.prevent="reportIssue">报告问题</a>
        </div>
      </div>
    </div>
    
    <!-- 帮助模态框 -->
    <div v-if="showHelpModal" class="modal-overlay" @click="showHelpModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>帮助中心</h2>
          <button @click="showHelpModal = false" class="close-btn">×</button>
        </div>
        
        <div class="modal-body">
          <div class="help-content">
            <h3>常见问题</h3>
            <ul>
              <li>检查URL是否正确</li>
              <li>确保您有访问权限</li>
              <li>尝试刷新页面</li>
              <li>清除浏览器缓存</li>
            </ul>
            
            <h3>技术支持</h3>
            <p>如果问题持续存在，请联系技术支持团队：</p>
            <div class="contact-info">
              <p>📧 邮箱: support@vabhub.com</p>
              <p>📞 电话: 400-123-4567</p>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="showHelpModal = false" class="btn btn-primary">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  data() {
    return {
      showHelpModal: false
    }
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    
    goBack() {
      if (window.history.length > 1) {
        this.$router.go(-1)
      } else {
        this.$router.push('/')
      }
    },
    
    showHelp() {
      this.showHelpModal = true
    },
    
    reportIssue() {
      // 这里可以集成问题报告系统
      const issueUrl = `mailto:support@vabhub.com?subject=页面未找到问题报告&body=页面URL: ${window.location.href}`
      window.location.href = issueUrl
    }
  }
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.not-found-content {
  background: white;
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.error-code {
  font-size: 6rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 1rem;
  line-height: 1;
}

.error-message h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #2c3e50;
}

.error-message p {
  font-size: 1.1rem;
  color: #7f8c8d;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.error-help {
  border-top: 1px solid #e9ecef;
  padding-top: 2rem;
}

.error-help p {
  color: #6c757d;
  margin-bottom: 1rem;
}

.help-links {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.help-links a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.help-links a:hover {
  text-decoration: underline;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

.btn-icon {
  font-size: 1.2rem;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  padding: 2rem;
  max-height: 60vh;
  overflow-y: auto;
}

.help-content h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.help-content ul {
  text-align: left;
  margin-bottom: 2rem;
}

.help-content li {
  margin-bottom: 0.5rem;
  color: #6c757d;
}

.contact-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  text-align: left;
}

.contact-info p {
  margin: 0.5rem 0;
  color: #495057;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e9ecef;
  text-align: right;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .not-found-page {
    padding: 1rem;
  }
  
  .not-found-content {
    padding: 2rem;
  }
  
  .error-code {
    font-size: 4rem;
  }
  
  .error-message h1 {
    font-size: 1.5rem;
  }
  
  .error-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
  
  .help-links {
    flex-direction: column;
    align-items: center;
  }
}

/* 动画效果 */
.not-found-content {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-code {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}
</style>