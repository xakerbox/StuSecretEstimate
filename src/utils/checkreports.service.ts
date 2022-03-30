import fs from "fs";
import { NextFunction } from "express";

const checkReportExistance = async (req: any, res: any, next: NextFunction) => {
    console.log(__dirname);
  try {
    const pdf = fs.readFileSync(`/app/pub/estimate_reports/${req.params.enum}.pdf`);
    console.log(pdf);
    next()
  } catch (e) {
    console.log(e);
    res.json({ error: 'No such estimate exist. Generate it at first at route /print.'});
  }
};

export { checkReportExistance };
