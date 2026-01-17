// start Tailwind in Watchmode, to recreate CSS when a File Changes:
// npx tailwindcss -i .\website\static\src\tailwind.css -o .\website\static\css\tailwind.css --watch

/**
 * When you make a change to a HTML Template File with Tailwindcss in watch mode, the following happens:
 * Detects file change
 * Detect File changes in content:
 * Scancs flie for class names
 * Compares with previous build
 * Adds/removes CSS rules
 * Rewrites output CSS file
 * Prints done in terminal
 */

/** @type {import('tailwindcss').Config} */
module.exports = {
    // The files Tailwind scans for TAilWIND Class names
    content: [
      "./website/templates/**/*.html"
    ],
    theme: {
      extend: {},
    },
    plugins: [
      require("@tailwindcss/typography"),
    ],
  };
  