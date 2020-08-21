import Token from './token';
import Pos from '../position';
const { InvalidCharError } = require("../errors");

export default class Lexer {
    constructor(options, text) {
        this.fn = options.fn || "<main>";
        this.text = text;
        this.alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
        this.digit = "0123456789";
        this.alphanum = this.alphabet + this.digit;
        this.toks = options.toks;
        this.keywords = options.keywords;
        this.pos = new Pos(0, 0, 0, this.fn, text);
        this.selection = text;
        this.idx = 0;
        this.advance(0);
    }

    advance(n) {
        for (let i = 0; i < n; i++) {
            this.pos.advance(this.selection[0]);
        }
        this.idx += n;
        this.selection = this.text.substr(this.idx);
    }

    make_tokens() {
        let tokens = [];

        while (this.idx < this.text.length) {
            while ([' ', ' ', '\t'].includes(this.selection[0])) {
                this.advance(1);
            }
            var matched = false;
            for (let type in this.toks) {
                if (this.selection.search(this.toks[type]) === 0) {
                    let val = this.selection.match(this.toks[type])[0];
                    let pos_start = this.pos.copy();
                    this.advance(val.length);
                    matched = new Token(type, val, pos_start, this.pos.copy());
                    break;
                }
            }
            if (matched) {
                tokens.push(matched);
            } else {
                return [null, new InvalidCharError(this.selection[0], this.pos.copy())];
            }
        }

        tokens.push(new Token('EOF', 'EOF', this.pos.copy().advance(), this.pos.copy().advance()))

        return [tokens, null];
    }
}