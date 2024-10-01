## Installation Guide

This document gives the instructions to install a system that allows one to track their job application flows. 

1. Clone the repository

```
git clone https://github.com/nakraft/tracker4J.git
```

2. Install NPM dependencies

```
cd tracker4J
yarn
```


## Install Backend requirements

Open a new terminal inside the backend directory.

`cd tracker4J\backend`


Create a virtual environment called `venv`

```
python -m venv venv
```

For Windows - Activate the virtual environment

```
venv\Scripts\activate.bat
```

For Mac OS - Activate the virtual environment
```
source venv/bin/activate
```

Install required packages for the Flask server

```
pip install -r requirements.txt
```

Run the flask server.

```
python app.py
```
The flask server runs in [http://localhost:8000](http://localhost:8000)

## Available Scripts

### Development Mode

In the project directory, you can run:

```
yarn start
```

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Production Optimised Build

```
yarn build
```

Builds the app for production to the `build` folder.\
It bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

## Testing Guide

- From within the root of the repository, all test suites can be run with: 

```
$ npm run test
```

- And coverage can be determined by running: 

```
$ npm run coverage
```

- For more details, visit the help page from within the terminal: 

```
$ npm run help
```


## User workflows

### Application Workflow 

1. A new user can register their account by clicking the register button. They would then be asked to fill out the account details. 
<img src="/docs/documentation_photos/login.png" alt="drawing" width="480" /> 
<img src="/docs/documentation_photos/register.png" alt="drawing" width="480" /> 

2. The user is returned to the homepage and can login. 
<img src="/docs/documentation_photos/loginfilled.png" alt="drawing" width="480" /> 

3. The user will be on the main dashboard. 
<img src="/docs/documentation_photos/applications.png" alt="drawing" width="480" /> 

4. The user can now add applications to their portal by clicking the add application button in the upper right hand corner. 
<img src="/docs/documentation_photos/createapplication.png" alt="drawing" width="480" /> 

5. They will see the application get added to the applied section of the dashboard. From their they can choose to update contact information for say - one of the managers of the hiring team. 
<img src="/docs/documentation_photos/contact.png" alt="drawing" width="480" /> 

6. They can also change the outcome of their application by clicking the 'change outcome' button on the application card. From here, they are able to enter a specific interview date for the position and set a reminder to follow up with the hiring team. 
<img src="/docs/documentation_photos/interview.png" alt="drawing" width="480" /> 

7. If they are accepted for the job, they can click the change outcome button and watch their accepted job move to the decisions column! 
<img src="/docs/documentation_photos/outcome.png" alt="drawing" width="480" /> 

A couple of cool things to note that a user will like: 
- The site has been scaled to include pages! Now - if a user has had 100s of applications - the page will not crash. A user can safely navigate through their applicaitons to view the details of everything. 
- We are now more secure! Base64 authentication has been implemented to ensure the correct users are accessing the data. 
- We are sending out automated reminders! When a user logs a interview or reminder date, we will send a reminder email to the email address they used on sign up! In addition, we have a popup displaying your upcoming interview dates upon logging into the application. 

### Statistics Workflow 

1. To ensure that the user can identify their overall trends in job applications, a statistics dashboard was put together. It can be found in the upper right user tab button under statistics. 
2. Click on that button and see the following information about your portal: how many applications you've submitted, how many career fairs you've been to, and the overall status of your jobs. 

<img src="/docs/documentation_photos/statistics.png" alt="drawing" width="480" /> 

3. A user can also user the upper right corner to submit a resume to the site for safe keeping. 

## Advanced details

Still looking for more details about expected behavior? Look in our [black box testing suite](https://github.com/nakraft/tracker4J/blob/main/docs/blackBoxTests.pdf) to learn about manual tests you can conduct that will help you learn more about the software. 

Having issue with a dependency not being available? Try to install the needed dependency with ```npm -i module-name```. 

Having an issue with the application functionality? Visit our [troubleshooting_guide](/docs/troubleshooting_guide.md) for advice and debugging options for common problems. 
