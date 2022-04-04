# StartWork 
## Table of contents
1. [Description](#1-description)
2. [Tech stack](#2-tech-stacks)
3. [Miroservices involved](#3-microservices-involved)
    - Simple Microservices
    - Complex microservices
4. [Pre-requisites](#4-pre-requisites)
5. [Setup guide](#5-setup-guide)

## 1. Description
It is a platform that allows you to search for startup jobs & apply for them if you are a job seeker! If you happen to be a startup owner, you can also post jobs to look for the expertise you need. This aims to allow facilitation of jobs in the face of the rising gig economy.

## 2. Tech stacks
- Python & Flask (For the microservices)
- RabbitMQ (for AMQP)
- php (for frontend)
- html (for frontend)
- css (for frontend)
- jquery (for frontend)
- Vanilla Javascript (for frontend)
- Firebase - Realtime Database (for data storage)
- 0Auth (For authentication)
- Docker (for containerisation of the microservices)

## 3. Microservices involved
- Simple Microservices (SMS)
  - Activity (activitySMS.py) : tracks activity
  - Error (errorSMS.py) : tracks error in the microservices
  - User Notification (userNotificationSMS.py) : notifies job seekers of their application outcomes
  - Owner Notification (ownerNotificationSMS.py) : notifies owners of job seekers accepting their notifications
  - Job (jobSMS.py) : handles data relating to the jobs & updating their vacancies when associated applications are accepted
  - Application (applicationSMS.py) : handles job applications 
  - UserStatus (userStatusSMS.py) : allows job seekers to accept and reject job offers (when their job applications are accepted) 
  - OwnerStatus (ownerStatusSMS.py) : allows startup owners to accept/reject job applications
- Complex Microservices (CMS)
  - Accept/Reject (accjCMS.py) : allows startup owners to accept/reject job applications via the UI
  - Apply Job (applyJobCMS.py) : allows job seekers to apply for job positions by startup owners via the UI
  - Create Job (createJobCMS.py) : allows startup owners to create jobs via the UI for job seekers to apply 
  - User Decision (userDecisionCMS.py) : allows startup owners to accept/reject jobs should their applications get accepted

## 4. Pre-requisites
- Visual studio code (python & docker extensions required)
- Docker 
- Github extension (for command line)
- Python libraries:
  - pyrebase (to enable firebase)
  - pyrebase4 (to ensure firebase does not have errors; there are slight issues in pyrebase itself)
  - flask (to enable the microservices to work)
  - pika (to enable RabbitMQ)
  - requests (enable HTTP communication)
  - flask-cors (to enable CORS)

## 5. Setup guide
1. The link to the repo is: https://github.com/DemonDia/ESD_Project
2. In your command prompt, type the following: https://github.com/DemonDia/ESD_Project
3. Your command prompt should look like this: 
<img width="567" alt="image" src="https://user-images.githubusercontent.com/47315402/161437019-2232ec1d-bc26-46e3-87c4-cdb0ce392d00.png">

4. In our destination, you should see the folder "ESD_Project"
5. Click on the folder in step 4. You should see the following as shown below:

<img width="928" alt="image" src="https://user-images.githubusercontent.com/47315402/161437152-6e0ab360-579d-46b4-94f5-29ef46c2f4c7.png">

6. Open this folder in your visual studio code.

NOTE: make sure you are in the folder destination in visual studio code as shown below:

<img width="374" alt="image" src="https://user-images.githubusercontent.com/47315402/161437285-169381e5-446f-445e-ab7f-6b0c7721be50.png">

7. Open docker-compose.yml and replace 'puturdockerid' with your docker ID
8. Open a terminal and type "docker-compose up" (this builds and runs all the microservices as mentioned)
9. Open another terminal and type "python main.py" 
10. Go to http://localhost:5020/ and you should see something like this:
<img width="1359" alt="image" src="https://user-images.githubusercontent.com/47315402/161437557-0e980ba8-4124-4ca4-934e-b015f5136bbe.png">

11. Click the Google sign in button
12. To access the job seeker pages, use a non-SMU gmail account to login
13. To access the startup owner page, use a SMU gmail account to login
14. Happy exploring!
