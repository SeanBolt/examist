var path = require("path"),
    webpack = require("webpack");

module.exports = {
    context: __dirname,
    entry: "./src/index.jsx",

    module: {
        loaders: [{
            test: /\.jsx?$/,
            include: [path.resolve(__dirname, "src/"), path.resolve(__dirname, "i18n/")],
            loaders: ["react-hot", "babel"]
        }, {
            test: /\.jsx?$/,
            include: [path.resolve(__dirname, "src/")],
            loader: "eslint" 
        }, {
            test: /\.scss$/,
            include: [path.resolve(__dirname, "style/")],
            loaders: ["style", "css", "sass"]
        }, {
            test: /\.yaml$/,
            loaders: ["json", "yaml"]
        }]
    },

    resolve: {
        extensions: ['', '.js', '.jsx'],
        fallback: path.join(__dirname, "node_modules")
    },

    resolveLoader: {
        fallback: path.join(__dirname, "node_modules")
    },

    output: {
        filename: "index.js",
        path: __dirname + "/build",
        publicPath: "/build/"
    },

    plugins: [
        new webpack.DefinePlugin({
            "process.env.NODE_ENV": process.env.NODE_ENV || "\"development\""
        })
    ]
};