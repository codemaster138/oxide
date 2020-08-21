module.exports = (...args) => {
    console.log(...(args.map(el => el && el.toString ? el.toString() : el)));
}