<template>
  <div class="user-preferences">
    <div class="preferences-header">
      <h3>个性化推荐设置</h3>
      <p>根据您的偏好优化推荐结果</p>
    </div>

    <div class="preferences-content">
      <!-- 类型偏好 -->
      <div class="preference-section">
        <h4>喜欢的类型</h4>
        <div class="genres-grid">
          <label 
            v-for="genre in availableGenres" 
            :key="genre"
            class="genre-checkbox"
          >
            <input 
              type="checkbox" 
              :value="genre" 
              v-model="preferences.favoriteGenres"
            />
            <span class="checkbox-label">{{ genre }}</span>
          </label>
        </div>
      </div>

      <!-- 排除类型 -->
      <div class="preference-section">
        <h4>排除的类型</h4>
        <div class="genres-grid">
          <label 
            v-for="genre in availableGenres" 
            :key="genre"
            class="genre-checkbox"
          >
            <input 
              type="checkbox" 
              :value="genre" 
              v-model="preferences.excludedGenres"
            />
            <span class="checkbox-label">{{ genre }}</span>
          </label>
        </div>
      </div>

      <!-- 评分偏好 -->
      <div class="preference-section">
        <h4>评分偏好</h4>
        <div class="rating-preferences">
          <div class="preference-item">
            <label>最低评分:</label>
            <input 
              type="range" 
              v-model="preferences.minRating" 
              min="0" 
              max="10" 
              step="0.1"
              class="rating-slider"
            />
            <span class="rating-value">{{ preferences.minRating }}</span>
          </div>
          
          <div class="preference-item">
            <label>年份范围:</label>
            <div class="year-range">
              <input 
                type="number" 
                v-model="preferences.minYear" 
                placeholder="起始年份"
                class="year-input"
              />
              <span>至</span>
              <input 
                type="number" 
                v-model="preferences.maxYear" 
                placeholder="结束年份"
                class="year-input"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 个性化设置 -->
      <div class="preference-section">
        <h4>个性化设置</h4>
        <div class="personalization-settings">
          <label class="setting-item">
            <input type="checkbox" v-model="preferences.enablePersonalization" />
            <span>启用个性化推荐</span>
          </label>
          
          <label class="setting-item">
            <input type="checkbox" v-model="preferences.showSimilarityScores" />
            <span>显示相似度分数</span>
          </label>
          
          <label class="setting-item">
            <input type="checkbox" v-model="preferences.autoLoadRecommendations" />
            <span>自动加载推荐</span>
          </label>
        </div>
      </div>

      <!-- 保存按钮 -->
      <div class="preference-actions">
        <button @click="savePreferences" class="save-btn" :disabled="saving">
          {{ saving ? '保存中...' : '保存设置' }}
        </button>
        <button @click="resetPreferences" class="reset-btn">
          恢复默认
        </button>
      </div>
    </div>

    <!-- 保存状态提示 -->
    <div v-if="saveStatus" class="save-status" :class="saveStatus.type">
      {{ saveStatus.message }}
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'

export default {
  name: 'UserPreferences',
  setup() {
    const saving = ref(false)
    const saveStatus = ref(null)
    
    const availableGenres = [
      '科幻', '动作', '喜剧', '爱情', '悬疑', '恐怖', '惊悚',
      '动画', '纪录片', '剧情', '冒险', '奇幻', '犯罪', '战争',
      '音乐', '歌舞', '家庭', '历史', '传记', '运动'
    ]

    // 默认偏好设置
    const defaultPreferences = {
      favoriteGenres: ['科幻', '动作', '悬疑'],
      excludedGenres: ['恐怖', '惊悚'],
      minRating: 7.0,
      minYear: 2010,
      maxYear: new Date().getFullYear(),
      enablePersonalization: true,
      showSimilarityScores: true,
      autoLoadRecommendations: false
    }

    const preferences = reactive({ ...defaultPreferences })

    // 保存偏好设置
    const savePreferences = async () => {
      saving.value = true
      
      try {
        const response = await fetch('/api/ai/recommend/preferences', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: 'current_user', // 实际应用中应该使用真实的用户ID
            preferences: preferences,
            favorite_genres: preferences.favoriteGenres,
            excluded_genres: preferences.excludedGenres
          })
        })

        if (response.ok) {
          saveStatus.value = {
            type: 'success',
            message: '偏好设置保存成功'
          }
        } else {
          throw new Error('保存失败')
        }
      } catch (error) {
        saveStatus.value = {
          type: 'error',
          message: '保存失败，请重试'
        }
        console.error('保存偏好设置失败:', error)
      } finally {
        saving.value = false
        
        // 3秒后清除状态提示
        setTimeout(() => {
          saveStatus.value = null
        }, 3000)
      }
    }

    // 重置偏好设置
    const resetPreferences = () => {
      Object.assign(preferences, defaultPreferences)
      saveStatus.value = {
        type: 'info',
        message: '已恢复默认设置'
      }
      
      setTimeout(() => {
        saveStatus.value = null
      }, 3000)
    }

    // 加载用户偏好
    const loadUserPreferences = async () => {
      try {
        const response = await fetch('/api/ai/recommend/preferences/current_user')
        if (response.ok) {
          const data = await response.json()
          if (data.success && data.preferences) {
            Object.assign(preferences, data.preferences)
          }
        }
      } catch (error) {
        console.error('加载用户偏好失败:', error)
      }
    }

    onMounted(() => {
      loadUserPreferences()
    })

    return {
      preferences,
      availableGenres,
      saving,
      saveStatus,
      savePreferences,
      resetPreferences
    }
  }
}
</script>

<style scoped>
.user-preferences {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-width: 800px;
  margin: 0 auto;
}

.preferences-header {
  text-align: center;
  margin-bottom: 2rem;
}

.preferences-header h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.preferences-header p {
  color: #6c757d;
  font-size: 0.9rem;
}

.preference-section {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.preference-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.preference-section h4 {
  color: #495057;
  margin-bottom: 1rem;
  font-weight: 600;
}

.genres-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.5rem;
}

.genre-checkbox {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.genre-checkbox:hover {
  border-color: #007bff;
}

.genre-checkbox input {
  margin-right: 0.5rem;
}

.checkbox-label {
  font-size: 0.9rem;
  color: #495057;
}

.rating-preferences {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.preference-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.preference-item label {
  min-width: 80px;
  font-weight: 500;
  color: #495057;
}

.rating-slider {
  flex: 1;
  max-width: 200px;
}

.rating-value {
  min-width: 30px;
  text-align: center;
  font-weight: bold;
  color: #007bff;
}

.year-range {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.year-input {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.personalization-settings {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.setting-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.setting-item input {
  margin: 0;
}

.preference-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.save-btn, .reset-btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.save-btn {
  background: #007bff;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #0056b3;
}

.save-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.reset-btn {
  background: #6c757d;
  color: white;
}

.reset-btn:hover {
  background: #545b62;
}

.save-status {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  text-align: center;
  font-weight: 500;
}

.save-status.success {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.save-status.error {
  background: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.save-status.info {
  background: #d1ecf1;
  color: #0c5460;
  border: 1px solid #bee5eb;
}

@media (max-width: 768px) {
  .user-preferences {
    padding: 1rem;
    margin: 0 1rem;
  }
  
  .genres-grid {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
  
  .preference-item {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  
  .preference-actions {
    flex-direction: column;
  }
  
  .year-range {
    justify-content: center;
  }
}
</style>