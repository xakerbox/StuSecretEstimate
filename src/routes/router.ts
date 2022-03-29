import express from "express";
import { ControllerClass } from "../controller/controller";
import { registerSchema } from "../dto/registerSchema";
import { requestValidation } from "../dto/requestValidator";
import { AuthValidation } from '../controller/auth.controller';

const tokenValidator = new AuthValidation();

const router = express.Router();
const controller = new ControllerClass();

router.post(
  "/sign-up",
  registerSchema,
  requestValidation,
  controller.signUp
);
router.post("/token", controller.getToken);
router.get("/list",  tokenValidator.checkAuthorizationToken, controller.listUsers);
router.get("/list/:userId", tokenValidator.checkAuthorizationToken, controller.listUserById);
router.post("/calculate", tokenValidator.checkAuthorizationToken, controller.getCalculations)
router.post("/calculate/:est", tokenValidator.checkAuthorizationToken, controller.getCalculations)
router.post("/test-route/:testNumber", tokenValidator.checkAuthorizationToken, controller.testScript)
router.post("/estimate/:num", tokenValidator.checkAuthorizationToken, controller.getEstimate)

export default router;
