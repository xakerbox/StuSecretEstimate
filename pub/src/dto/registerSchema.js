"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerSchema = void 0;
const express_validator_1 = require("express-validator");
const registerSchema = [
    (0, express_validator_1.body)("login")
        .isLength({ min: 2 })
        .withMessage("Put the user login")
        .isString()
        .withMessage("You need to send login."),
    (0, express_validator_1.body)("password")
        .isString()
        .withMessage("Use string instead of numbers")
        .isLength({ min: 6 })
        .withMessage("Password has to be at least 6 symbols"),
];
exports.registerSchema = registerSchema;
