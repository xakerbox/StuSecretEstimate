// const { argv, stdout } = require("process");
// const { spawn } = require("child_process");

import { argv, stdout } from 'process';
import { spawn } from 'child_process';

async function initializePython(show: any) {
    const python = spawn("python", ["test.py", show]);
    python.stdout.on('data', (res) => {
        console.log(res.toString());
    })
    console.log(show);
  }

export { initializePython };