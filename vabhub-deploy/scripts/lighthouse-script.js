// Lighthouse 测试脚本
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');
const fs = require('fs');

async function runLighthouse(url, options = {}) {
    const chrome = await chromeLauncher.launch({
        chromeFlags: ['--headless', '--no-sandbox', '--disable-dev-shm-usage']
    });
    
    options.port = chrome.port;
    
    try {
        const runnerResult = await lighthouse(url, options);
        
        // 返回测试结果
        return {
            score: runnerResult.lhr.categories.performance.score * 100,
            metrics: {
                firstContentfulPaint: runnerResult.lhr.audits['first-contentful-paint'].numericValue,
                largestContentfulPaint: runnerResult.lhr.audits['largest-contentful-paint'].numericValue,
                cumulativeLayoutShift: runnerResult.lhr.audits['cumulative-layout-shift'].numericValue,
                totalBlockingTime: runnerResult.lhr.audits['total-blocking-time'].numericValue,
                speedIndex: runnerResult.lhr.audits['speed-index'].numericValue
            },
            report: runnerResult.report
        };
    } finally {
        await chrome.kill();
    }
}

// 导出函数供其他脚本使用
if (require.main === module) {
    // 直接运行时的处理
    const url = process.argv[2] || 'http://localhost:8090';
    
    runLighthouse(url).then(results => {
        console.log('Lighthouse Results:');
        console.log(`Performance Score: ${results.score}%`);
        console.log('Core Web Vitals:');
        console.log(`  First Contentful Paint: ${results.metrics.firstContentfulPaint}ms`);
        console.log(`  Largest Contentful Paint: ${results.metrics.largestContentfulPaint}ms`);
        console.log(`  Cumulative Layout Shift: ${results.metrics.cumulativeLayoutShift}`);
        console.log(`  Total Blocking Time: ${results.metrics.totalBlockingTime}ms`);
        console.log(`  Speed Index: ${results.metrics.speedIndex}ms`);
        
        // 保存报告
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const reportFile = `/app/reports/lighthouse-${timestamp}.html`;
        fs.writeFileSync(reportFile, results.report);
        console.log(`Full report saved to: ${reportFile}`);
        
    }).catch(error => {
        console.error('Lighthouse test failed:', error);
        process.exit(1);
    });
}

module.exports = { runLighthouse };