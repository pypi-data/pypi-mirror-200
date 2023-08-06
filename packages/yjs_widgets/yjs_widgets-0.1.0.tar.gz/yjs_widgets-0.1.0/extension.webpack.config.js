const CopyPlugin = require('copy-webpack-plugin');
const path = require('path');

const occPath = [
  __dirname,
  'node_modules',
  'lib',
];
const staticPath = [
  __dirname,
  'yjs-widgets',
  'labextension',
  'static',
];

module.exports = {
  module: {
    rules: [
      {
        type: 'javascript/auto',
        loader: 'file-loader'
      }
      // { test: /\.js$/, loader: 'source-map-loader' }
    ]
  },
  resolve: {
    fallback: {
      fs: false,
      child_process: false,
      crypto: false
    }
  },
  plugins: [
    new CopyPlugin({
      patterns: [
        {
          from: path.join(...occPath),
          to: path.join(...staticPath),
          noErrorOnMissing: true
        }
      ]
    })
  ]
};
