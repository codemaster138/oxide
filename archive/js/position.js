/**
 * Keep track of positions in order to correctly display errors
 */
export default class Pos {
    /**
     * 
     * @param {*} idx Index in text
     * @param {*} ln Line number
     * @param {*} col Column
     * @param {*} fn File name
     * @param {*} text Text
     */
    constructor(idx, ln, col, fn, text) {
        this.idx = idx;
        this.ln = ln;
        this.col = col;
        this.fn = fn;
        this.text = text;
    }

    advance(cur_char) {
        this.idx++;
        this.col++;
        if ((cur_char || ' ') === '\n') {
            this.ln++;
            this.col = 0;
        }
        return this;
    }

    copy() {
        return new Pos(this.idx, this.ln, this.col, this.fn, this.text);
    }
}