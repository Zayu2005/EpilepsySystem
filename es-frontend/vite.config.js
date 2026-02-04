import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import vueJsx from '@vitejs/plugin-vue-jsx';
// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vueJsx(),
        vueDevTools(),
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        },
    }
    ,
    server: {
        host: '0.0.0.0',
        proxy: {
            '/api': {
                target: 'http://localhost:8080', // 后端服务地址
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    },
    // server: {
    //     host: '0.0.0.0',
    //     proxy: {
    //         // 代理 API 请求到后端
    //         '/api': {
    //             target: 'http://localhost:8080', // 后端服务地址
    //             changeOrigin: true,
    //             rewrite: (path) => path.replace(/^\/api/, '')
    //         },
    //         // 新增：代理七牛云图片路径请求
    //         '/cloud.epilepsy-detect.xyz': {
    //             target: 'http://cloud.epilepsy-detect.xyz', // 七牛云实际域名
    //             changeOrigin: true,
    //             rewrite: (path) => path.replace(/^\/cloud.epilepsy-detect.xyz/, '') // 移除路径前缀
    //         }
    //     }
    // }
})
