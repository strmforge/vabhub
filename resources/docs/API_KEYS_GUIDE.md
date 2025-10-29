# VabHub排行榜API密钥获取指南

## 📋 概述

VabHub排行榜功能需要配置多个数据源的API密钥才能正常工作。本指南将详细介绍如何获取各个平台的API密钥。

## 🎵 音乐类数据源

### 1. Spotify
**申请地址**: https://developer.spotify.com/dashboard

**步骤**:
1. 登录Spotify开发者平台
2. 创建新应用
3. 获取Client ID和Client Secret
4. 设置重定向URI（可选）

**配置**:
```env
SPOTIFY_API_KEY=your_client_id:your_client_secret
```

### 2. 网易云音乐
**获取方式**: 通过浏览器Cookie获取

**步骤**:
1. 登录网易云音乐网页版
2. 打开开发者工具（F12）
3. 在Application/Storage中找到Cookie
4. 复制`MUSIC_U`和`__csrf`的值

**配置**:
```env
NETEASE_COOKIE=MUSIC_U=xxx; __csrf=xxx
```

### 3. QQ音乐
**申请地址**: https://y.qq.com/ 开放平台

**步骤**:
1. 注册QQ音乐开放平台开发者
2. 创建应用
3. 获取App Key和App Secret

**配置**:
```env
QQ_MUSIC_API_KEY=your_app_key:your_app_secret
```

### 4. Apple Music
**申请地址**: https://developer.apple.com/musickit/

**步骤**:
1. 加入Apple开发者计划
2. 获取MusicKit开发者令牌

**配置**:
```env
APPLE_MUSIC_API_KEY=your_developer_token
```

## 🎬 影视类数据源

### 5. TMDB
**申请地址**: https://www.themoviedb.org/settings/api

**步骤**:
1. 注册TMDB账号
2. 申请API密钥
3. 等待审核（通常很快）

**配置**:
```env
TMDB_API_KEY=your_tmdb_api_key
```

### 6. 豆瓣
**申请地址**: https://developers.douban.com/

**步骤**:
1. 注册豆瓣开发者
2. 创建应用
3. 获取API密钥

**配置**:
```env
DOUBAN_API_KEY=your_douban_api_key
```

### 7. IMDb
**申请地址**: https://imdb-api.com/api

**步骤**:
1. 注册IMDb API账号
2. 获取免费API密钥

**配置**:
```env
IMDB_API_KEY=your_imdb_api_key
```

### 8. 猫眼
**申请地址**: 猫眼开放平台（需联系商务）

**配置**:
```env
MAOYAN_API_KEY=your_maoyan_api_key
```

## 📺 电视剧数据源

### 9. MyDramaList
**申请地址**: https://www.mydramalist.com/api

**步骤**:
1. 注册MyDramaList账号
2. 申请API访问权限

**配置**:
```env
MYDRAMALIST_API_KEY=your_mydramalist_api_key
```

### 10. Viki
**申请地址**: https://www.viki.com/developer

**步骤**:
1. 注册Viki开发者账号
2. 申请API密钥

**配置**:
```env
VIKI_API_KEY=your_viki_api_key
```

### 11. TVmaze
**申请地址**: https://www.tvmaze.com/api

**说明**: TVmaze API无需密钥，但建议注册获取更高限制

**配置**:
```env
TVMAZE_API_KEY=your_username (可选)
```

### 12. Trakt
**申请地址**: https://trakt.tv/oauth/applications

**步骤**:
1. 注册Trakt账号
2. 创建OAuth应用
3. 获取Client ID和Client Secret

**配置**:
```env
TRAKT_API_KEY=your_client_id:your_client_secret
```

## 🔧 配置步骤

### 1. 创建环境变量文件
```bash
# 复制示例文件
cp VabHub-Resources/config/charts_env.sample VabHub-Resources/config/charts_env.env

# 编辑配置文件
vim VabHub-Resources/config/charts_env.env
```

### 2. 填入实际API密钥
根据上面的指南，将获取到的API密钥填入对应位置。

### 3. 启动服务
```bash
cd VabHub-Deploy
./scripts/deploy_charts.sh start
```

## 💡 使用建议

### 优先级配置
如果不想配置所有API密钥，可以按优先级配置：

**高优先级（推荐配置）**:
- TMDB（影视数据最全）
- Spotify（音乐数据权威）
- 网易云音乐（中文音乐）

**中优先级**:
- 豆瓣（中文影视评分）
- QQ音乐（中文音乐补充）

**低优先级**:
- 其他数据源（根据个人需求）

### 免费额度说明
- TMDB: 免费，无限制
- Spotify: 免费额度有限
- 网易云音乐: 通过Cookie免费
- 其他平台: 通常有免费额度

## 🚨 注意事项

1. **API密钥安全**: 不要将API密钥提交到公开仓库
2. **使用限制**: 注意各平台的API调用限制
3. **更新维护**: 定期检查API密钥是否过期
4. **故障排除**: 如果某个数据源失效，系统会自动降级使用其他可用数据源

## 📞 技术支持

如果在配置过程中遇到问题，请参考：
- 各平台官方文档
- VabHub项目文档
- GitHub Issues