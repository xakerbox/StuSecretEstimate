"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AuthValidation = void 0;
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config({ path: ".././.env" });
class AuthValidation {
    checkAuthorizationToken(req, res, next) {
        try {
            const token = req.headers.authorization.split(" ")[1];
            jsonwebtoken_1.default.verify(token, process.env.JWT_SECRET);
            next();
        }
        catch (e) {
            console.log(e);
            return res.json({
                error: 'Token expired or incorrect. Get new one on /token route.',
            });
        }
    }
}
exports.AuthValidation = AuthValidation;
