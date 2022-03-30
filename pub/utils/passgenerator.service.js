"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.hashPassword = void 0;
const bcrypt_1 = __importDefault(require("bcrypt"));
const saltRounds = 7;
const salt = "StuSuperHero";
const hashPassword = (password) => {
    bcrypt_1.default.genSalt(saltRounds, function (err, salt) {
        bcrypt_1.default.hash(password, salt, function (err, hash) { });
    });
};
exports.hashPassword = hashPassword;
