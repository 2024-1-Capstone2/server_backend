// <<<<<<< HEAD
//
//       tailwind.config = {
//         theme: {
//     extend: {
//       colors: {
//         gray: "#fcfcfc",
//         black: "#000",
//         white: "#fff",
//         whitesmoke: {
//           "100": "#f5f5f5",
//           "200": "#efefef",
//           "300": "#e9e9e9",
//         },
//         darkgray: "#989898",
//         lightseagreen: "#00abb3",
//         darkslateblue: {
//           "100": "#013773",
//           "200": "#002854",
//         },
//         gainsboro: {
//           "100": "#e6e6e6",
//           "200": "#e5e5e5",
//           "300": "#d9d9d9",
//         },
//         steelblue: "#5686c4",
//         silver: "#c4c4c4",
//       },
//       spacing: {},
//       fontFamily: {
//         inter: "Inter",
//       },
//       borderRadius: {
//         xl: "20px",
//         "31xl": "50px",
//         mini: "15px",
//       },
//     },
//     fontSize: {
//       mini: "0.938rem",
//       "6xl": "1.563rem",
//       xl: "1.25rem",
//       base: "1rem",
//       "26xl": "2.813rem",
//       "17xl": "2.25rem",
//       "8xl": "1.688rem",
//       "11xl": "1.875rem",
//       "16xl": "2.188rem",
//       "9xl": "1.75rem",
//       "2xl": "1.313rem",
//       "5xl": "1.5rem",
//       lg: "1.125rem",
//       inherit: "inherit",
//     },
//     screens: {
//       mq1500: {
//         raw: "screen and (max-width: 1500px)",
//       },
//       mq1350: {
//         raw: "screen and (max-width: 1350px)",
//       },
//       mq1275: {
//         raw: "screen and (max-width: 1275px)",
//       },
//       mq1225: {
//         raw: "screen and (max-width: 1225px)",
//       },
//       mq1150: {
//         raw: "screen and (max-width: 1150px)",
//       },
//       mq1100: {
//         raw: "screen and (max-width: 1100px)",
//       },
//       mq850: {
//         raw: "screen and (max-width: 850px)",
//       },
//       mq800: {
//         raw: "screen and (max-width: 800px)",
//       },
//       mq750: {
//         raw: "screen and (max-width: 750px)",
//       },
//       mq450: {
//         raw: "screen and (max-width: 450px)",
//           },
//         },
// =======
//
//       tailwind.config = {
//         theme: {
//     extend: {
//       colors: {
//         gray: "#fcfcfc",
//         black: "#000",
//         white: "#fff",
//         whitesmoke: {
//           "100": "#f5f5f5",
//           "200": "#efefef",
//           "300": "#e9e9e9",
//         },
//         darkgray: "#989898",
//         lightseagreen: "#00abb3",
//         darkslateblue: {
//           "100": "#013773",
//           "200": "#002854",
//         },
//         gainsboro: {
//           "100": "#e6e6e6",
//           "200": "#e5e5e5",
//           "300": "#d9d9d9",
//         },
//         steelblue: "#5686c4",
//         silver: "#c4c4c4",
//       },
//       spacing: {},
//       fontFamily: {
//         inter: "Inter",
//       },
//       borderRadius: {
//         xl: "20px",
//         "31xl": "50px",
//         mini: "15px",
//       },
//     },
//     fontSize: {
//       mini: "0.938rem",
//       "6xl": "1.563rem",
//       xl: "1.25rem",
//       base: "1rem",
//       "26xl": "2.813rem",
//       "17xl": "2.25rem",
//       "8xl": "1.688rem",
//       "11xl": "1.875rem",
//       "16xl": "2.188rem",
//       "9xl": "1.75rem",
//       "2xl": "1.313rem",
//       "5xl": "1.5rem",
//       lg: "1.125rem",
//       inherit: "inherit",
//     },
//     screens: {
//       mq1500: {
//         raw: "screen and (max-width: 1500px)",
//       },
//       mq1350: {
//         raw: "screen and (max-width: 1350px)",
//       },
//       mq1275: {
//         raw: "screen and (max-width: 1275px)",
//       },
//       mq1225: {
//         raw: "screen and (max-width: 1225px)",
//       },
//       mq1150: {
//         raw: "screen and (max-width: 1150px)",
//       },
//       mq1100: {
//         raw: "screen and (max-width: 1100px)",
//       },
//       mq850: {
//         raw: "screen and (max-width: 850px)",
//       },
//       mq800: {
//         raw: "screen and (max-width: 800px)",
//       },
//       mq750: {
//         raw: "screen and (max-width: 750px)",
//       },
//       mq450: {
//         raw: "screen and (max-width: 450px)",
//           },
//         },
// >>>>>>> 332cbac19ee1e6e20fd38dd441f1fff36f5fccec
//       },};
//
//     /** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: ["./*.{html,js}", "./!(build|dist|.*)/**/*.{html,js}"],

  tailwind.config={
  theme: {
    extend: {
      colors: {
        whitesmoke: {
          "100": "#f5f5f5",
          "200": "#efefef",
          "300": "#e9e9e9",
        },
        white: "#fff",
        black: "#000",
        darkslateblue: {
          "100": "#013773",
          "200": "#002854",
        },
        darkgray: "#989898",
        gray: "#fcfcfc",
        lightseagreen: "#00abb3",
        gainsboro: {
          "100": "#e6e6e6",
          "200": "#e5e5e5",
          "300": "#d9d9d9",
        },
        steelblue: "#5686c4",
        silver: "#c4c4c4",
        lightgray: "#d1d1d1",
      },
      spacing: {
        '30': '7.5rem',
      },
      fontFamily: {
        inter: "Inter",
      },
      borderRadius: {
        xl: "20px",
        mini: "15px",
        "31xl": "50px",
      },
    },
    fontSize: {
      mini: "0.938rem",
      "11xl": "1.875rem",
      "5xl": "1.5rem",
      lg: "1.125rem",
      "16xl": "2.188rem",
      "9xl": "1.75rem",
      "2xl": "1.313rem",
      xl: "1.25rem",
      base: "1rem",
      "6xl": "1.563rem",
      "26xl": "2.813rem",
      "17xl": "2.25rem",
      "8xl": "1.688rem",
      inherit: "inherit",
    },
    screens: {
      mq1500: {
        raw: "screen and (max-width: 1500px)",
      },
      mq1350: {
        raw: "screen and (max-width: 1350px)",
      },
      mq1275: {
        raw: "screen and (max-width: 1275px)",
      },
      mq1225: {
        raw: "screen and (max-width: 1225px)",
      },
      mq1150: {
        raw: "screen and (max-width: 1150px)",
      },
      mq1100: {
        raw: "screen and (max-width: 1100px)",
      },
      mq850: {
        raw: "screen and (max-width: 850px)",
      },
      mq800: {
        raw: "screen and (max-width: 800px)",
      },
      mq767: {
        raw: "screen and (max-width: 767px)",
      },
      mq750: {
        raw: "screen and (max-width: 750px)",
      },
      mq450: {
        raw: "screen and (max-width: 450px)",
      },
    },
  },
  corePlugins: {
    preflight: false,
  },
};
