"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.connection = void 0;
const mysql2_1 = __importDefault(require("mysql2"));
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config({ path: '.././.env' });
const connection = mysql2_1.default.createConnection({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    database: process.env.DB_NAME_TESLA,
    password: process.env.DB_PASS
});
exports.connection = connection;
connection.connect((err) => {
    if (err) {
        return console.error("Error: " + err.message);
    }
    else {
        console.log(`Successfully connected Teslaestimate to server on host ${process.env.DB_HOST}`);
    }
});
