/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Deep Forest theme colors
        forest: {
          darkest: '#1A3A2E',  // Sidebar
          dark: '#2D5F4C',      // Middle panel
          light: '#E8F3ED',     // Right panel/content
        },
        emerald: {
          DEFAULT: '#10B981',   // Primary accent
        },
        gold: {
          DEFAULT: '#F59E0B',   // Secondary accent
        }
      },
    },
  },
  plugins: [],
}
