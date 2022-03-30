"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ControllerClass = void 0;
// import { v4 as uuidv4 } from "uuid";
const bcrypt_1 = __importDefault(require("bcrypt"));
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
const dotenv_1 = __importDefault(require("dotenv"));
const dbConnection_1 = require("../db/dbConnection");
const dbConnection_tesla_1 = require("../db/dbConnection_tesla");
const child_process_1 = require("child_process");
dotenv_1.default.config({ path: ".././.env" });
const JWT_SECRET = process.env.JWT_SECRET;
class ControllerClass {
    async signUp(req, res, next) {
        try {
            const userData = req.body;
            console.log(userData);
            const hashedPass = await bcrypt_1.default.hash(userData.password, 7);
            userData.password = hashedPass;
            dbConnection_1.connection.query("INSERT INTO users(user_id, user_login, password, email, role) VALUE (UUID(),?,?,?,?)", [userData.login, userData.password, userData.email, "USER"], (err, result) => {
                if (err) {
                    res.json({ error: "The user already exist" });
                }
                else {
                    res.json({
                        status: "Successfuly registered!",
                        user_credentials: userData,
                    });
                }
            });
        }
        catch (e) {
            res.status(401).json({ error: e });
        }
    }
    listUsers(req, res) {
        dbConnection_1.connection.query("SELECT * FROM users", (err, result, fields) => {
            res.send(result);
        });
    }
    listUserById(req, res) {
        try {
            console.log(req.params);
            dbConnection_1.connection.query(`SELECT user_login, password FROM users WHERE user_id='${req.params.userId}'`, (err, result, field) => {
                if (result.length !== 0) {
                    res.json(result);
                }
                else {
                    res.json({ error: "No such user was found in DB" });
                }
            });
        }
        catch (e) {
            res.json({ error: e });
            console.log(e);
        }
    }
    getToken(req, res) {
        try {
            dbConnection_1.connection.query(`SELECT user_login, password, user_id FROM users WHERE user_login='${req.body.login}';`, (err, result) => {
                if (result.length !== 0) {
                    console.log(result);
                    bcrypt_1.default.compare(req.body.password, result[0].password, (err, validation) => {
                        if (validation) {
                            const token = jsonwebtoken_1.default.sign({ payload: result[0].user_id }, JWT_SECRET, { expiresIn: "10m" });
                            res.json({
                                pass: validation,
                                authToken: token,
                                result: result,
                            });
                        }
                        else {
                            res.json({ error: "Password is incorrect" });
                        }
                    });
                }
                else {
                    res.json({ error: "No user was found!" });
                }
            });
        }
        catch (e) {
            res.json(e);
        }
    }
    async getCalculations(req, res) {
        (0, child_process_1.exec)(`python3 etotal.py ${req.params.est}`, (err, stdout, stderr) => {
            console.log(stdout);
            res.json({ sucess: stdout, error: stderr });
        });
    }
    testScript(req, res) {
        (0, child_process_1.exec)(`python3 test.py ${req.params.testNumber}`, (err, stdout, stderr) => {
            console.log(stdout);
            res.json({ sucess: stdout.replace('\n', '. '), error: stderr });
        });
    }
    getEstimate(req, res) {
        try {
            dbConnection_tesla_1.connection.query(`SELECT estnum, fname, lname, cellph FROM ehead WHERE estnum='${req.params.num}'`, (err, result) => {
                console.log(result);
                if (result != undefined && result.length !== 0) {
                    res.json({ your_estimate: req.params.num, success: result[0] });
                }
                else {
                    res.json({ error: 'No such estimate No exist in DB.' });
                }
            });
        }
        catch (e) {
            res.json(e);
        }
    }
}
exports.ControllerClass = ControllerClass;
