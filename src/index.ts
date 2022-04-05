import express from "express";
import bodyParser from "body-parser";
import router from "./routes/router";
import dotenv from "dotenv";
dotenv.config({path: '.././.env'});
import { exec } from "child_process";

const app = express();

console.log(process.env.DB_USER);
console.log(__dirname);

exec('python3 --version', (err, stdout) => {
  console.log('Installed Python version: ', stdout, '\n');
})

exec('node -v', (err, stdout) => {
  console.log('Installed NodeJS version: ', stdout, '\n');
})

app.use(bodyParser.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(__dirname))

app.use(router);

app.listen(process.env.PORT, () => {
  console.log(`Server started on port ${process.env.PORT}`);
});