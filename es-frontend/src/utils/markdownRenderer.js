import { marked } from 'marked';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

// 配置 marked
marked.setOptions({
  highlight: (code, language) => {
    const validLang = hljs.getLanguage(language) ? language : 'plaintext';
    return hljs.highlight(code, { language: validLang }).value;
  },
  breaks: true,
  gfm: true,
  headerIds: true,
  mangle: false,
  sanitize: false,
  smartLists: true,
  smartypants: true
});

export const renderMarkdown = (content) => {
  return marked(content);
};