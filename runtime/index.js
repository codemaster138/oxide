import Lexer from '../lexer';
import clog from './clog';
import fs from 'fs';
import readlineSync from 'readline-sync';


export const LexerOptions = {
    toks: {
        'FLOAT': /\b[0-9]+\.[0-9]+\b/,
        'INT': /\b[0-9]+\b/,
        'PLUS': /\+/,
        'MINUS': /\-/,
        'POW': /\*\*/,
        'MUL': /\*/,
        'DIV': /\//,
        'LPAREN': /\(/,
        'RPAREN': /\)/,
    }
}

export function run(text) {
    const lex = new Lexer(LexerOptions, text);
    const toks = lex.make_tokens();

    if (toks[1]) return toks[1];
    else return toks[0];
}

function shell() {
    while (true) {
        const text = readlineSync.question('oxide>> ');
        if (text === '.exit') break // .exit exits shell
        clog(run(text));
    }
}

console.log('Oxide v1.0.0 ©2020 - Jake Sarjeant');
console.log('License: GNU GPL v3.0');
console.log('Enjoy :)');

if (process.argv.length > 2) clog(run(fs.readFileSync(process.argv[2])))
    else shell();