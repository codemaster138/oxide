const path = require('path');

module.exports = {
    mode: 'production',
    entry: './runtime/index.js',
    output: {
        path: path.resolve(__dirname),
        filename: 'index.js'
    }
}