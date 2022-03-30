"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.checkReportExistance = void 0;
const fs_1 = __importDefault(require("fs"));
const checkReportExistance = async (req, res, next) => {
    console.log(__dirname);
    try {
        const pdf = fs_1.default.readFileSync(`/app/pub/estimate_reports/${req.params.enum}.pdf`);
        console.log(pdf);
        next();
    }
    catch (e) {
        console.log(e);
        res.json({ error: 'No such estimate exist. Generate it at first at route /print.' });
    }
};
exports.checkReportExistance = checkReportExistance;
