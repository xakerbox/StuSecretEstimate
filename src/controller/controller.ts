import { NextFunction, Request, response, Response } from "express";
import { RowDataPacket } from "mysql2";
// import { v4 as uuidv4 } from "uuid";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
import fs from "fs";

import { UserAuth, Environment } from "../interfaces/interfaces";
import { connection as db } from "../db/dbConnection";
import { connection as dbTesla } from "../db/dbConnection_tesla";
import { exec } from "child_process";
// import { Environment } from "@types/"


dotenv.config({ path: ".././.env" });
const JWT_SECRET = process.env.JWT_SECRET;

// PROD or DEV could be changed on .env file.
const HOST_NAME = process.env.ENVIRONMENT ==  Environment.PROD ?  "190.92.148.46:4200" : "localhost:4200";
const WORKING_DIR = process.env.ENVIRONMENT == Environment.PROD ? "/app/pub/estimate_reports/" : "/Users/vladimirkuzin/StuProj/Vlad3ServREST/pub/estimate_reports"

export class ControllerClass {
  async signUp(req: Request, res: Response, next: NextFunction) {
    try {
      const userData: UserAuth = req.body;
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
                    { expiresIn: "20m" }
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
    exec(
      `python3 etotal_updated.py ${req.params.est}`,
      (err, stdout, stderr) => {
        console.log(stdout);
        if (!err) {
        const [ epntrate, emecrate, ebodrate, efrarate , estrrate , eglarate , edetrate, eothrate ] = stdout.replace('\n','').split(' ');
        res.json({
          sucess: true,
          calculations: {
            epntrate,
            emecrate,
            ebodrate,
            efrarate,
            estrrate,
            eglarate,
            edetrate,
            eothrate
          }
        });
      } else {
        res.json({ err: err })
      }
      }
    );
  }

  testScript(req: Request, res: Response) {
    exec(`python3 test.py ${req.params.testNumber}`, (err, stdout, stderr) => {
      console.log(stdout);
      res.json({ sucess: stdout.replace("\n", ". "), error: stderr });
    });
  }

  getEstimate(req: Request, res: Response) {
    try {
      dbTesla.query(
        `SELECT estnum, fname, lname, cellph FROM ehead WHERE estnum='${req.params.enum}'`,
        (err, result: RowDataPacket) => {
          console.log(result);
          if (result != undefined && result.length !== 0) {
            res.json({ your_estimate: req.params.enum, success: result[0] });
          } else {
            res.json({ error: "No such estimate No exist in DB." });
          }
        }
      );
    } catch (e) {
      res.json(e);
    }
  }

  generatePdf(req: Request, res: Response) {
    try {
      exec(`python3 rgenx.py ${req.params.enum}`, (err, stdout, stderr) => {
        console.log(err);
        if (!err) {
          console.log(stdout);
          res.json({
            sucess: stdout.replace("\n", " "),
            estimate_pdf: `http://${HOST_NAME}/report/${req.params.enum}`,
            error: stderr,
          });
      } else {
          res.json({ error: 'No match with such Estimate #. Try another number.' })
      }
      });
    } catch (e) {
        res.json(e);
        console.log(e);
    }
  }

  sendPdf(req: Request, res: Response) {
    try {
      if (fs.existsSync(`${WORKING_DIR}/EST_${req.params.enum}.pdf`)) {
        const file = fs.createReadStream(
          `${WORKING_DIR}/EST_${req.params.enum}.pdf`
        );
        const stat = fs.statSync(
          `${WORKING_DIR}/EST_${req.params.enum}.pdf`
        );
        res.setHeader("Content-Length", stat.size);
        res.setHeader("Content-Type", "application/pdf");
        res.setHeader(
          "Content-Disposition",
          `attachment; filename=EST_${req.params.enum}.pdf`
        );
        file.pipe(res);
      } else {
          res.json({ error: 'Sorry, at first generate Estimate report with such number.'});
      }
      
    } catch (e) {
      res.json({ error: 'Sorry, at first generate Estimate report with such number.' });
      console.log(e);
    }
  }

  healthChecker(req: Request, res: Response) {
    res.status(200).json({ status: 'The server is up and working well.'})
  }
}
