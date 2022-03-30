export interface UserAuth {
    login: string,
    password: string,
    email: string
}

export enum Environment {
    DEV = 'TEST',
    PROD = 'PROD'
}