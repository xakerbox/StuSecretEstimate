"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const body_parser_1 = __importDefault(require("body-parser"));
const router_1 = __importDefault(require("./routes/router"));
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config({ path: '.././.env' });
const child_process_1 = require("child_process");
const app = (0, express_1.default)();
console.log(process.env.DB_USER);
console.log(__dirname);
(0, child_process_1.exec)('python3 --version', (err, stdout) => {
    console.log('Installed Python version: ', stdout, '\n');
});
(0, child_process_1.exec)('node -v', (err, stdout) => {
    console.log('Installed NodeJS version: ', stdout, '\n');
});
app.use(body_parser_1.default.json());
app.use(express_1.default.urlencoded({ extended: false }));
app.use(express_1.default.static(__dirname));
app.use(router_1.default);
app.listen(process.env.PORT, () => {
    console.log(`Server started on port ${process.env.PORT}`);
});
