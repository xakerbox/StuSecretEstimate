import { NextFunction, Request, response, Response } from "express";
import { RowDataPacket } from "mysql2";
// import { v4 as uuidv4 } from "uuid";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
import { UserAuth } from "../interfaces/interfaces";
import { connection as db } from "../db/dbConnection";
import { connection as dbTesla } from "../db/dbConnection_tesla";
import { exec } from "child_process";

dotenv.config({ path: ".././.env" });
const JWT_SECRET = process.env.JWT_SECRET;

export class ControllerClass {
  async signUp(req: Request, res: Response, next: NextFunction) {
    try {
      const userData: UserAuth = req.body;
      console.log(userData);
      const hashedPass = await bcrypt.hash(userData.password, 7);
      userData.password = hashedPass;
      db.query(
        "INSERT INTO users(user_id, user_login, password, email, role) VALUE (UUID(),?,?,?,?)",
        [userData.login, userData.password, userData.email, "USER"],
        (err, result) => {
          if (err) {
            res.json({ error: "The user already exist." });
          } else {
            res.json({
              status: "Successfuly registered!",
              user_credentials: userData,
            });
          }
        }
      );
    } catch (e) {
      res.status(401).json({ error: e });
    }
  }

  listUsers(req: Request, res: Response) {
    db.query("SELECT * FROM users", (err, result, fields) => {
      res.send(result);
    });
  }

  listUserById(req: Request, res: Response) {
    try {
      console.log(req.params);
      db.query(
        `SELECT user_login, password FROM users WHERE user_id='${req.params.userId}'`,
        (err, result: RowDataPacket, field) => {
          if (result.length !== 0) {
            res.json(result);
          } else {
            res.json({ error: "No such user was found in DB" });
          }
        }
      );
    } catch (e) {
      res.json({ error: e });
      console.log(e);
    }
  }

  getToken(req: Request, res: Response) {
    try {
      db.query(
        `SELECT user_login, password, user_id FROM users WHERE user_login='${req.body.login}';`,
        (err, result: RowDataPacket) => {
          if (result.length !== 0) {
            console.log(result);
            bcrypt.compare(
              req.body.password,
              result[0].password,
              (err, validation) => {
                if (validation) {
                  const token = jwt.sign(
                    { payload: result[0].user_id },
                    JWT_SECRET,
                    { expiresIn: "10m" }
                  );
                  res.json({
                    pass: validation,
                    authToken: token,
                    result: result,
                  });
                  console.log({
                    pass: validation,
                    authToken: token,
                    result: result,
                  });
                } else {
                  res.json({ error: "Password is incorrect" });
                }
              }
            );
          } else {
            res.json({ error: "No user was found!" });
          }
        }
      );
    } catch (e) {
      res.json(e);
    }
  }

  async getCalculations(req: Request, res: Response) {
    exec(`python3 etotal_updated.py ${req.params.est}`, (err, stdout, stderr) => {
      console.log(stdout);
      res.json({ sucess: stdout, error: stderr });
    });
  }

  testScript(req: Request, res: Response) {
    exec(`python3 test.py ${req.params.testNumber}`, (err, stdout, stderr) => {
      console.log(stdout);
      res.json({ sucess: stdout.replace('\n', '. '), error: stderr });
    });
  }

  getEstimate(req: Request, res: Response) {
    try {
      dbTesla.query(`SELECT estnum, fname, lname, cellph FROM ehead WHERE estnum='${req.params.num}'`, (err, result: RowDataPacket) => {
        console.log(result);
        if (result != undefined && result.length !== 0) {
          res.json({ your_estimate: req.params.num, success: result[0]})
        } else {
          res.json({ error: 'No such estimate No exist in DB.'})
        }
      })
    } catch (e) {
      res.json(e)
    }
  }
}
