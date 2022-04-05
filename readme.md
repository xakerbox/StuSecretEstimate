## Workable routes.

### <span style="color:yellow">/sign-up
```
Request Body:
{
    "login": "Boy Girl",
    "password": "newpassword",
    "email": "boygirl@mail.com"
}
```
### <span style="color:yellow"> /token
Get token for access next routes. (For testing it expires in 20 minutes).
```
{
    "login": "Boy Girl",<br>
    "password": "newpassword"<br>
}
```
### <span style="color:yellow">/list
All routes beneath needs <color>Bearer<color> token in headers with key *Authorization*. To get it use <u>/token</u> route.

### <span style="color:yellow"> /list/:userId
Get all users that are storing in DB.

### <span style="color:yellow"> /calculate
Get user ID from <u>/list</u> route

### <span style="color:yellow"> /calculate/:est
Put the number of estimate starting from 1000

### <span style="color:yellow"> /test-route/:testNumber
Test Python script runner.

### <span style="color:yellow"> /estimate/:enum
Calculate estimate using python-script.

### <span style="color:yellow"> /print/:enum
Print estimate, generates PDF-file with link for download.