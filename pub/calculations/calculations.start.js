"use strict";
// const { argv, stdout } = require("process");
// const { spawn } = require("child_process");
Object.defineProperty(exports, "__esModule", { value: true });
exports.initializePython = void 0;
const child_process_1 = require("child_process");
async function initializePython(show) {
    const python = (0, child_process_1.spawn)("python", ["test.py", show]);
    python.stdout.on('data', (res) => {
        console.log(res.toString());
    });
    console.log(show);
}
exports.initializePython = initializePython;
