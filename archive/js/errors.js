function arrowString(text, start, end) {
    rtn = text;
    rtn += "\n";
    rtn += " ".repeat(start) + "^".repeat(end - start + 1);
    return rtn
}

class Error {
    constructor(type, details, pos_start, pos_end) {
        this.pos_start = pos_start;
        this.pos_end = pos_end;
        this.type = type;
        this.details = details;
    }

    toString() {
        let estr = `\x1b[31;1m${this.type}\x1b[0m: ${this.details}\nFile \'${this.pos_start.fn}\', line ${this.pos_start.ln + 1}\n`;
        estr += arrowString(this.pos_start.text, this.pos_start.col, this.pos_end.col);
        return estr;
    }
}

class InvalidCharError extends Error {
    constructor(details, pos_start) {
        super("Invalid character", details, pos_start, pos_start);
    }
}

class EOFError extends Error {
    constructor(details, pos_start) {
        super("Invalid Syntax", details, pos_start, pos_start);
    }
}

class InvalidTokenError extends Error {
    constructor(tok) {
        super("Invalid Token", tok.value, tok.pos_start, tok.pos_end);
    }
}

class ExpectedTokenError extends Error {
    constructor (details, tok) {
        super("Invalid Token", `Expected ${details} but got '${tok.value}'`, tok.pos_start, tok.pos_end);
    }
}

class RTError extends Error {
    constructor (type, details, pos_start, pos_end, context) {
        super(`Exception \x1b[34;1m${type}\x1b[31;1m`, details, pos_start, pos_end);
        this.context = context;
    }

    toString() {
        let estr = this.createTraceback();
        estr += `\x1b[31;1m${this.type}\x1b[0m: ${this.details}\nFile \'${this.pos_start.fn}\', line ${this.pos_start.ln + 1}\n`;
        estr += arrowString(this.pos_start.text, this.pos_start.col, this.pos_end.col);
        return estr;
    }

    createTraceback() {
        let res = '';
        let pos = this.pos_start;
        let ctx = this.context;

        while (ctx) {
            res = `\tFile ${pos.fn}, line ${pos.ln} in ${ctx.display_name}\n` + res;
            ctx = this.context.parent;
            pos = this.context.parent_entry_pos;
        }
        return `Traceback (most recent call last):\n${res}`;
    }
}

module.exports = {
    InvalidCharError,
    EOFError,
    InvalidTokenError,
    ExpectedTokenError,
    RTError
}