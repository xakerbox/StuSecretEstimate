import { body } from "express-validator";

const registerSchema = [
  body("login")
    .isLength({ min: 2 })
    .withMessage("Put the user login")
    .isString()
    .withMessage("You need to send login."),
  body("password")
    .isString()
    .withMessage("Use string instead of numbers")
    .isLength({ min: 6 })
    .withMessage("Password has to be at least 6 symbols"),
];

export { registerSchema };
