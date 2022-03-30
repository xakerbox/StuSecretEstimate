declare namespace NodeJS {
    export interface ProcessEnv {
      PORT: number;
      CRYPTO_WORD: string;
      DB_HOST: string;
      DB_USER: string;
      DB_NAME: string;
      DB_NAME_TESLA: string;
      DB_PASS: string;
      ENVIRONMENT: Environment;
      JWT_SECRET: string;
    }
}

