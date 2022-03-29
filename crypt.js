// const bcrypt = require("bcrypt");
const CryptoJS = require("crypto-js");
require("dotenv").config();

const superWord = process.env.CRYPTO_WORD;
const userPass = "mypassword";

// Encrypt
const ciphertext = CryptoJS.AES.encrypt(userPass, superWord).toString();
console.log(ciphertext);

// Decrypt
// var bytes = CryptoJS.AES.decrypt(ciphertext, superWord);
// var originalText = bytes.toString(CryptoJS.enc.Utf8);
