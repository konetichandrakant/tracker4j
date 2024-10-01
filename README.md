# JobTracker Application

[![DOI](https://zenodo.org/badge/558546454.svg)](https://zenodo.org/badge/latestdoi/558546454)
![MIT license](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub](https://img.shields.io/badge/Language-JavaScript-blue.svg)
![Yarn](https://img.shields.io/badge/Yarn-v1.22.19-green.svg)
![npm](https://img.shields.io/badge/npm-v8.9.0-green.svg)
![Node](https://img.shields.io/badge/node-v16.15.1-green.svg)
![Python](https://img.shields.io/badge/python-v3.8-green.svg)

![Open issues](https://img.shields.io/github/issues-raw/nakraft/tracker4J)
![Closed issues](https://img.shields.io/github/issues-closed-raw/nakraft/tracker4J?color=bright-green)
<!-- [![frontend-build](https://github.com/ekanshsinghal/se-group26-proj1/actions/workflows/frontend_build_test.yml/badge.svg?branch=main)](https://github.com/ekanshsinghal/se-group26-proj1/actions/workflows/frontend_build_test.yml)
[![Backend-build](https://github.com/ekanshsinghal/se-group26-proj1/actions/workflows/backend_build.yml/badge.svg)](https://github.com/ekanshsinghal/se-group26-proj1/actions/workflows/backend_build.yml)
[![Backend-Test](https://github.com/ekanshsinghal/se-group26-proj1/actions/workflows/backend_test.yml/badge.svg)](https://github.com/ekanshsinghal/se-group26-proj1/actions/workflows/backend_test.yml) -->

![Repo Size](https://img.shields.io/github/repo-size/nakraft/tracker4J?color=brightgreen)
[![GitHub Release](https://img.shields.io/github/release/nakraft/tracker4J)](https://github.com/nakraft/tracker4J/releases/)
[![codecov](https://codecov.io/gh/nakraft/tracker4J/branch/master/graph/badge.svg?token=A6c0vrGL1s)](https://codecov.io/gh/nakraft/tracker4J)

## Goal

Your personalized JobTracker application in one place!

## Description

Excel sheets that are complex and disorganized must go! Every job-related data can be managed by our JobTrackr Application, including your job profile, applications, status, important dates, notes, saved applications, job descriptions, recruiter details, compensation and offer package, and more.

## NEW User Workflows (what a significant improvement from v1!)

Our __NEW functionalities__ include: 

- Adding/updating applications with contact information, interview dates, or job requests. 
- Storing your resume for jobs so that you can customize each one
- Tracking career fairs and ensuring you can make it to one on time.
- Querying applications to ensure you can find what you are looking for
- Statistics regarding your job search
- Implemented multithreading and caching of frequent requests on the server to significantly reduce average response time
- Containerized the backend server for horizontal scaling

Plus we care about security and have integrated in Base64 authentication between our server and client! 

Lastly, we want to make sure you can apply to jobs to your hearts content, to __scale__ up the project, we have paginated the applications tab so that you won't be limited by how many applications you can navigate through. 

For more details regarding User Workflows, visit our user workflows which are included in the [install guide](INSTALL.md)

## Introduction

https://user-images.githubusercontent.com/30636208/194798331-9338219d-cdbd-4ff1-96fa-b1425dfc9504.mp4

## Built using

<p align="center">
<img src="https://user-images.githubusercontent.com/30636208/194690148-8e3dbe93-2ede-4da8-a44a-e4ee165b6b3b.png" width="150"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/2300px-React-icon.svg.png" width="150"><img src="https://upload.wikimedia.org/wikipedia/commons/9/9a/Visual_Studio_Code_1.35_icon.svg" width="150"> <img src="https://cdn.worldvectorlogo.com/logos/mongodb-icon-1.svg" width ="150"/> <img src="https://camo.githubusercontent.com/36ecb78d148678488fa43e5916e131906c15ea485b30232739d5633b2e0ce18c/68747470733a2f2f6b6576696e2d62726f776e2e636f6d2f696d616765732f666c61736b2d6c6f676f2e737667" width ="150"/> 
</p>

## Application Demo

https://user-images.githubusercontent.com/30636208/194689139-29cdb217-a9e1-4fea-977d-74cbeb6d6799.mp4

## New Application Demo 
<a href="https://youtu.be/k30zrIrqsV0"><img src="https://github.com/nakraft/tracker4J/blob/master/resources/bg.png"></a>

### Use 

Setup and installation instructions can be found in the [user-friendly install guide](INSTALL.md)

### Testing / Coverage

Run this command to test the backend APIs

```
python backend\tests.py
```

Visit our [results page](/docs/results.md) for more information regarding running our test and code coverage scripts. 

## Tools

-   Preetier Code Formatter
-   PyLint with Flake8

### Built With

-   `react 18.2.x`
-   `babel 7.19.x`
-   `webpack cli 4.x`
-   `sass` (Dart Sass)
-   `Python 3.8+`
-   `Flask`
-   `MongoDB`

Note: This repository is configured with [Dart-sass](https://github.com/sass/dart-sass) and not [Node Sass].


### Third-Party Tools

-   [MongoDB Cloud](https://www.mongodb.com/)

## Contributing

Are you interested in contributing to this project? Visit [our contribution](CONTRIBUTING.md) documentation for details. 
  
Need some ideas on what has been done? Jump on over to our [development project board](https://github.com/users/nakraft/projects/2/views/1) for specific issues we are tracking and log which areas you are planning to help out on. 

This project is made possible by the incredible donation of time from NC State Project Contributors and the advice/support of CSC 510 teaching staff. NC State University has made the resources for this project possible, and will continue to support CSC 510 projects for the forseeable future. 

## Help 

View some common issues users have identified in our [troubleshooting guide](https://github.com/nakraft/tracker4J/blob/master/docs/troubleshooting_guide.md). We list tips and tricks for identifying where the issue may be coming from. Issue reports may be linked to this guide if you identify a bug that is a software limitation. 

You can visit our website with full descriptions of our classes and methods by opening ```index.html``` within your file explorer. Included on the website is user profiles of people who should use the software and success stories!
  
Need more support? Our primary method for addressing bugs and feature requests should be through submitting an issue ticket in the "Issues" tab. If you need additional support, please reach out to our development email develop.nak@gmail.com and a member of the team will be in contact with you shortly. You can also email the development email to asked to be added to our subsriber list for updates regarding the project's development.

## License

Distributed under the MIT License. See `LICENSE` for more information.
