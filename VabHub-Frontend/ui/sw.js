// SmartMedia Hub v4.1 - Service Worker
const CACHE_NAME = 'smartmedia-hub-v4.1';
const STATIC_CACHE = 'static-v4.1';
const DYNAMIC_CACHE = 'dynamic-v4.1';

// 需要缓存的静态资源
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/new-index.html',
  '/styles/new-main.css',
  '/styles/new-components.css',
  '/styles/enhanced-styles.css',
  '/styles/theme-manager.css',
  '/js/new-app.js',
  '/js/new-components.js',
  '/js/enhanced-interactions.js',
  '/js/theme-manager.js',
  '/manifest.json',
  '/favicon.svg',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

// 需要缓存的API端点
const API_CACHE = [
  '/api/dashboard',
  '/api/media-library',
  '/api/subscription',
  '/api/recognition',
  '/api/metadata',
  '/api/sync',
  '/api/users'
];

// 安装事件 - 缓存静态资源
self.addEventListener('install', (event) => {
  console.log('Service Worker 安装中...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('缓存静态资源');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('Service Worker 安装完成');
        return self.skipWaiting();
      })
  );
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', (event) => {
  console.log('Service Worker 激活中...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
              console.log('删除旧缓存:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('Service Worker 激活完成');
        return self.clients.claim();
      })
  );
});

// 获取事件 - 缓存策略
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // API请求 - 网络优先，失败时使用缓存
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // 缓存成功的API响应
          if (response.status === 200) {
            const responseClone = response.clone();
            caches.open(DYNAMIC_CACHE)
              .then((cache) => {
                cache.put(request, responseClone);
              });
          }
          return response;
        })
        .catch(() => {
          // 网络失败时使用缓存
          return caches.match(request)
            .then((cachedResponse) => {
              if (cachedResponse) {
                return cachedResponse;
              }
              // 返回离线页面
              return new Response(JSON.stringify({
                error: '网络连接失败',
                offline: true,
                timestamp: Date.now()
              }), {
                headers: { 'Content-Type': 'application/json' }
              });
            });
        })
    );
    return;
  }

  // 静态资源 - 缓存优先
  if (STATIC_ASSETS.some(asset => request.url.includes(asset))) {
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          return fetch(request)
            .then((response) => {
              // 缓存新资源
              const responseClone = response.clone();
              caches.open(STATIC_CACHE)
                .then((cache) => {
                  cache.put(request, responseClone);
                });
              return response;
            });
        })
    );
    return;
  }

  // 其他请求 - 网络优先
  event.respondWith(
    fetch(request)
      .catch(() => {
        // 返回离线提示
        if (request.headers.get('Accept')?.includes('text/html')) {
          return caches.match('/')
            .then((cachedResponse) => {
              return cachedResponse || new Response('网络连接失败，请检查网络连接');
            });
        }
      })
  );
});

// 后台同步 - 处理离线时的数据同步
self.addEventListener('sync', (event) => {
  console.log('后台同步事件:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      syncOfflineData()
    );
  }
});

// 推送通知
self.addEventListener('push', (event) => {
  if (!event.data) return;

  const data = event.data.json();
  const options = {
    body: data.body || 'SmartMedia Hub 有新消息',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/'
    },
    actions: [
      {
        action: 'open',
        title: '查看'
      },
      {
        action: 'close',
        title: '关闭'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(data.title || 'SmartMedia Hub', options)
  );
});

// 通知点击事件
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'open') {
    event.waitUntil(
      clients.matchAll({ type: 'window' })
        .then((clientList) => {
          for (const client of clientList) {
            if (client.url === event.notification.data.url && 'focus' in client) {
              return client.focus();
            }
          }
          if (clients.openWindow) {
            return clients.openWindow(event.notification.data.url);
          }
        })
    );
  }
});

// 离线数据同步函数
async function syncOfflineData() {
  // 从IndexedDB获取离线数据并同步到服务器
  try {
    const db = await openDB();
    const offlineActions = await getAllOfflineActions(db);
    
    for (const action of offlineActions) {
      await syncAction(action);
      await removeOfflineAction(db, action.id);
    }
    
    console.log('离线数据同步完成');
  } catch (error) {
    console.error('离线数据同步失败:', error);
  }
}

// 模拟IndexedDB操作
function openDB() {
  return new Promise((resolve) => {
    // 这里简化处理，实际项目中需要完整的IndexedDB实现
    resolve({
      offlineActions: []
    });
  });
}

function getAllOfflineActions(db) {
  return Promise.resolve(db.offlineActions || []);
}

function removeOfflineAction(db, id) {
  return Promise.resolve();
}

function syncAction(action) {
  return fetch('/api/sync', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(action)
  });
}