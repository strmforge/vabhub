import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { visualizer } from 'rollup-plugin-visualizer'
import autoprefixer from 'autoprefixer'

export default defineConfig({
  plugins: [
    vue({
      // Vue 3 特性支持
      reactivityTransform: true
    }),
    AutoImport({
      resolvers: [ElementPlusResolver()],
      dts: 'src/auto-imports.d.ts',
      imports: [
        'vue',
        'vue-router',
        'pinia',
        {
          '@vueuse/core': [
            'useMouse',
            'useLocalStorage',
            'useSessionStorage',
            'useDebounceFn',
            'useThrottleFn'
          ]
        }
      ],
      eslintrc: {
        enabled: true
      }
    }),
    Components({
      resolvers: [ElementPlusResolver()],
      dts: 'src/components.d.ts',
      // 自动注册 components 目录下的组件
      dirs: ['src/components', 'src/components/ui'],
      // 排除不需要自动注册的文件
      exclude: [/node_modules/, /\*.test.(js|ts)$/, /\*.spec.(js|ts)$/]
    }),
    // 打包分析插件（仅在生产环境启用）
    process.env.ANALYZE === 'true' && visualizer({
      filename: 'dist/stats.html',
      open: true,
      gzipSize: true,
      brotliSize: true
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '~': resolve(__dirname, 'node_modules')
    }
  },
  server: {
    port: 3000,
    host: true,
    cors: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true
      }
    },
    // 热更新配置
    hmr: {
      overlay: true
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: process.env.NODE_ENV !== 'production', // 开发环境开启sourcemap
    minify: process.env.NODE_ENV === 'production' ? 'terser' : false,
    terserOptions: {
      compress: {
        drop_console: process.env.NODE_ENV === 'production',
        drop_debugger: process.env.NODE_ENV === 'production'
      }
    },
    rollupOptions: {
      output: {
        // 智能代码分割
        manualChunks: (id) => {
          if (id.includes('node_modules')) {
            if (id.includes('vue')) {
              return 'vue'
            }
            if (id.includes('element-plus')) {
              return 'element-plus'
            }
            if (id.includes('lodash') || id.includes('axios')) {
              return 'utils'
            }
            if (id.includes('pinia') || id.includes('vue-router')) {
              return 'core'
            }
            // 其他第三方库
            return 'vendor'
          }
          // 业务代码按页面分割
          if (id.includes('src/pages')) {
            const match = id.match(/src\/pages\/([^/]+)\/.*\.vue$/)
            if (match && match[1]) {
              return `page-${match[1].toLowerCase()}`
            }
          }
        },
        chunkFileNames: 'js/[name]-[hash].js',
        entryFileNames: 'js/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const extType = assetInfo.name.split('.')[1]
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            return 'images/[name]-[hash][extname]'
          }
          if (/woff|woff2|eot|ttf|otf/i.test(extType)) {
            return 'fonts/[name]-[hash][extname]'
          }
          return 'assets/[name]-[hash][extname]'
        }
      }
    },
    // 优化构建输出
    chunkSizeWarningLimit: 2000,
    // 启用 CSS 代码分割
    cssCodeSplit: true,
    // 预加载关键资源
    reportCompressedSize: false
  },
  optimizeDeps: {
    include: [
      'vue',
      'vue-router',
      'pinia',
      'element-plus',
      '@element-plus/icons-vue',
      'axios',
      'lodash-es'
    ],
    exclude: []
  },
  // 环境变量配置
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: process.env.NODE_ENV !== 'production'
  },
  // CSS 配置
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "@/styles/variables.scss" as *;`
      }
    },
    postcss: {
      plugins: [
        autoprefixer({
          overrideBrowserslist: ['last 2 versions', '> 1%', 'IE 10']
        })
      ]
    }
  }
})