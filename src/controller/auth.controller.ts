import { NextFunction, Response } from "express";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
dotenv.config({ path: ".././.env" });

export class AuthValidation {
  public checkAuthorizationToken(req: any, res: Response, next: NextFunction) {
    try {
      const token = req.headers.authorization.split(" ")[1];
      console.log(token);
      jwt.verify(token, process.env.JWT_SECRET)

          next();
    } catch (e) {
        console.log(e);
      return res.json({
        error:
          'Token expired or incorrect. Get new one on /token route.',
      });
    }
  }
}
