## DELTA

To showcase the delta of our work, we have completed a video with the new features. To make it abundantly clear what we have accomplished, we also have provided this writeup: 

## Feature Updates 

### Adding/updating applications with contact information, interview dates, or job requests.

- Previously the tags at the bottom of the cards were not interactive. 
- We added the ability to add contact information 
- and change the location of the application based on its status dynamically. 

### Querying applications to ensure you can find what you are looking for

- We added a search bar that filters on the backend to speed up the software. 
- We also added the capacity to change how you view the data. 

### Storing your resume for jobs so that you can customize each one

- No resume functionality was previously added. Now, you can submit your resume for safekeeping through google's api. 

### Tracking career fairs and ensuring you can make it to one on time.

- We expanded functionality to include tracking of career fairs. 
- Career fairs also have reminders you can set about them that will be sent to your inbox daily. 

### Statistics regarding your job search

- No statistics were previously available. 
- Now a person can track their application status and how they are doing compared to others in the job hunt. In essence, we have 'gamified' the application. 

### Reminders
- Upon setting a reminder, a person can view their upcoming reminders in a tab at the top of the landing page. 
- In addition, a server was set up to send you email reminders regarding your upcoming events. This emailed progress occurs daily. 

### Security 
- Plus we care about security and have integrated in Base64 authentication between our server and client!

## Scalability 

To support scaling, we added the following elements: 

Pagination: 
- We included pagination on the backend so not all results would crash the front end when the users entered too many items. 
- It was tested to allow for about 1000 applications before the server took over 45 seconds to load the documents. 
- By limiting the entries per page, our application remains extremely fast and can store unlimited records per person. 

Runtime: 
- Running  multithreaded server
- caching frequent responses on the server

Dockerization: 
- Implement containerisation for easy horizontal scaling. 
