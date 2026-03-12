import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brandDark: '#1F3864',
        brandBlue: '#2E75B6',
        brandLight: '#F5F5F5',
      },
    },
  },
  plugins: [],
}

export default config
