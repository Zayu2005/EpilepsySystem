<template>
    <div class="markdown-content" v-html="renderedContent"></div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { marked } from 'marked';

// 配置 marked 选项
onMounted(() => {
    marked.setOptions({
        headerIds: true,
        mangle: false,
        headerPrefix: 'heading-',
        breaks: true,
        gfm: true
    });
});

const props = defineProps({
    content: {
        type: String,
        required: true
    }
});

// 预处理内容，确保标题格式正确
const processedContent = computed(() => {
    if (!props.content) return '';
    
    // 更全面的处理
    return props.content
        // 处理标题格式，确保 # 后有空格
        .replace(/^(#{1,6})([^\s])/gm, '$1 $2')
        // 确保标题前后有换行符以便正确渲染
        .replace(/^(#{1,6}\s.+)$/gm, '\n$1\n')
        // 处理列表项，确保列表项前有换行
        .replace(/^(-|\d+\.)\s/gm, '\n$&')
        // 确保段落之间有足够的换行
        .replace(/\n{3,}/g, '\n\n');
});

// 使用处理后的内容进行渲染
const renderedContent = computed(() => {
    return marked.parse(processedContent.value);
});
</script>

<style>
.markdown-content {
    line-height: 1.8;
    color: #2c3e50;
    font-size: 15px;
}

.markdown-content h1, 
.markdown-content h2, 
.markdown-content h3, 
.markdown-content h4, 
.markdown-content h5, 
.markdown-content h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
}

.markdown-content h1 {
    font-size: 2em;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
}

.markdown-content h2 {
    font-size: 1.5em;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
}

.markdown-content h3 {
    color: #1a73e8;
    font-size: 1.25em;
    margin: 1.5em 0 1em;
    padding-bottom: 0.3em;
}

.markdown-content strong {
    color: #2c3e50;
    font-weight: 600;
}

.markdown-content ol, .markdown-content ul {
    padding-left: 1.5em;
    margin: 1em 0;
} 

.markdown-content li {
    margin: 0.5em 0;
}

.markdown-content p {
    margin: 1em 0;
    line-height: 1.8;
}

.markdown-content pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow: auto;
}

.markdown-content code {
    font-family: Consolas, Monaco, 'Andale Mono', monospace;
    font-size: 14px;
    background-color: rgba(27, 31, 35, 0.05);
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

.markdown-content pre code {
    background-color: transparent;
    padding: 0;
}

/* 添加表格样式 */
.markdown-content table {
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
}

.markdown-content th, 
.markdown-content td {
    border: 1px solid #dfe2e5;
    padding: 8px 12px;
}

.markdown-content th {
    background-color: #f6f8fa;
}

/* 添加引用样式 */
.markdown-content blockquote {
    border-left: 4px solid #dfe2e5;
    padding-left: 16px;
    margin-left: 0;
    color: #6a737d;
}
</style>