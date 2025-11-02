// Iconify 图标构建脚本
const fs = require('fs');
const path = require('path');

console.log('Iconify 图标构建脚本执行中...');

// 创建简单的图标数据文件
const iconData = {
  version: '1.0.0',
  icons: {},
  metadata: {
    buildTime: new Date().toISOString(),
    source: 'Material Design Icons'
  }
};

// 确保 dist 目录存在
const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

// 写入图标数据文件
fs.writeFileSync(
  path.join(distDir, 'icons.json'),
  JSON.stringify(iconData, null, 2)
);

console.log('✅ Iconify 图标构建完成');