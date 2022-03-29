import bcrypt from "bcrypt";
const saltRounds = 7;
const salt = "StuSuperHero";

const hashPassword = (password: string) => {
  bcrypt.genSalt(saltRounds, function (err, salt) {
    bcrypt.hash(password, salt, function (err, hash) {});
  });
};

export { hashPassword };