export default class Token {
    constructor(type_, value, pos_start, pos_end) {
        this.type = type_;
        this.value = value;
        this.pos_start = pos_start;
        this.pos_end = pos_end;
    }

    in(...args) {
        for (let r of args) {
            if (this.type === r) {
                return true;
            }
        }
        return false
    }

    matches(...args) {
        for (let i = 0; i < args.length; i++) {
            if (this.type === args[i][0] && (args[i].length > 1 ? (this.value === args[i][1]) : true)) {
                return true;
            }
        }
        return false;
    }

    toString() {
        if (this.value) return `[${this.type}:${this.value}]`;
        return `[${this.type}]`;
    }
}