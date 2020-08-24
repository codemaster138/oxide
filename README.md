# Oxide
Oxide is a simple programming language. **Please note that Oxide is in the initial development phase and has very few features at the moment.**

## Using oxide
Make sure you have python 3.7 or later installed on your machine. Clone this repositiory and open the `python` directory in your terminal. Type `python3 .` to start the repl.

## Syntax
As of right now oxide only features a few different things:
- Mathematical expressions, like
```
oxide> 5 + 5 * 6 ** 7
<· 1399685.0
```
- Floating-point arithmetic (in fact, all numbers in oxide are float!), like
```
oxide> 5.7 * 2.3
<· 13.11
```
- `if`-statements
```
if (1 == 1) var test = 7
if (1 >= 2) {
    var foo = 7
    var bar = 8
}
```
- variables
```
oxide> var test = 17.25
<· 17.25
oxide> test
<· 17.25
```