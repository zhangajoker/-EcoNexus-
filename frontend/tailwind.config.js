/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        eco: {
          // 极暗深林绿（作为全局渐变底色）
          dark: '#022c22',
          // 半透明翡翠绿（配合毛玻璃效果）
          panel: 'rgba(6, 78, 59, 0.45)',
          // 柔和的植物茎秆绿边框
          border: 'rgba(16, 185, 129, 0.3)',
          // 荧光生机绿（核心数据高亮）
          primary: '#34d399',
          // 琥珀金/警示橙（用于预警，比纯红更贴合自然主题）
          alert: '#fbbf24',
          // 浅艾草绿（替代冷灰色文字）
          text: '#a7f3d0'
        }
      }
    },
  },
  plugins: [],
}