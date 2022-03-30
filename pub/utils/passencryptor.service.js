"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PasswordEncryptor = void 0;
// import bcrypt from "bcrypt";
const crypto_js_1 = __importDefault(require("crypto-js"));
// Encrypt
class PasswordEncryptor {
    encryptUserPassword(userPass) {
        const encryptedPassword = crypto_js_1.default.AES.encrypt(userPass, "StuSuperHero").toString();
        return encryptedPassword;
    }
    decryptUserPassword(encryptedPass) {
        const bytes = crypto_js_1.default.AES.decrypt(encryptedPass, 'StuSuperHero');
        const userPass = bytes.toString(crypto_js_1.default.enc.Utf8);
        return userPass;
    }
}
exports.PasswordEncryptor = PasswordEncryptor;
// Decrypt
