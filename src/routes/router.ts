import express from "express";
import { ControllerClass } from "../controller/controller";
import { registerSchema } from "../dto/registerSchema";
import { requestValidation } from "../dto/requestValidator";
import { AuthValidation } from '../controller/auth.controller';
import { checkReportExistance } from '../utils/checkreports.service';


const tokenValidator = new AuthValidation();

const router = express.Router();
const controller = new ControllerClass();

router.get('/', controller.healthChecker)

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
router.post("/estimate/:enum", tokenValidator.checkAuthorizationToken, controller.getEstimate)
router.post("/print/:enum", tokenValidator.checkAuthorizationToken, controller.generatePdf)

router.get("/report/:enum", controller.sendPdf)

export default router;
