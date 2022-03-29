import mysql from 'mysql2';
import dotenv from "dotenv";
dotenv.config({path: '.././.env'});

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  database: process.env.DB_NAME,
  password: process.env.DB_PASS
});

connection.connect((err) => {
  if (err) {
    return console.error("Error: " + err.message);
  }
  else{
    console.log(`Successfully connected Users DB to server on host ${process.env.DB_HOST}`);
  }
});

export { connection };



