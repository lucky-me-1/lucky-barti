# DISCUSSION

## Requirements
1. Implement a model to represent an appointment with one of two doctors (Strange, Who). Appointments can be arbitrary length i.e. 20 mins, 45 mins, 60 mins
2. Implement a model to represent the working hours of each doctor (9 AM to 5 PM, M-F for Strange, 8 AM to 4 PM M-F for Who). You can assume working hours are the same every week. i.e. The schedule is the same each week.
3. Implement an API to create an appointment, rejecting it if there's a conflict.
4. Implement an API to get all appointments within a time window for a specified doctor.
5. Implement an API to get the first available appointment after a specified time. i.e. I'm a patient and I'm looking for the first available appointment

#### Additional Notes
> There's no strict requirements with regards to technologies as long as you're not importing an existing scheduling library. There's a strong preference with Python and Flask given that is our current tech stack.

---

# Lucky's Thoughts
1. I timeboxed at 3 hours
  - Assume this is a real project. The first thing I would do is analyze the requirements, conduct feasibility, provide estimates on the project, size it accordingly, and then give timeline.
  - I opted for 3 hours. I believe that any take-home project from interviews should not take more than this.
  - This also showcases time management, and scope control.
2. Requirements are not clear. It says `no strict requirements on technologies` but says `strong preference with Python and Flask`. 
  - As an engineer, it is my duty to clarify the requirements. This statement contradicts each other. When dealing with stakeholders, it is usually the engineers who will provide with the tech architecture.
3. Because of the time constraints, I am introducing an MVP. I will discuss with stakeholders what MVP will have and **Additional features** will be provided on an iterative process.
4. No architecturing involved. How many potential users, 100? 100K? 1M? Caching and scaling? Containerization? Who provides the data (Doctors)

### MVP
1. 100% Test Coverage
2. See [README.md](./README.md)
3. 100% Requirements Met

### Future Sprints (Backlog)
1. Authentication 
  - Super important
  - Clients (browser/app/web) - Firebase/Cognito?
  - Server-to-Server - MTLS/Cert based
2. Code cleanup and folder organization
3. AI
  - Question/Answer-based approached.
  - RAG search on schedules
4. ETL
  - Data processing/ingestion
5. Performance considerations
  - E2E testing
6. Documentation
  - Swagger/OpenSpec/etc
7. Logging
  - Splunk/etc
8. Monitoring
  - AppDynamics/OpenTelemetry
9. Caching
  - Redis/ElasticCache/etc
10. Improved Metadata/Scheduling
 - Further improvement on `Doctor` classes, name, adddress, email, contact, etc
 - Holidays?
 - Different working hours per individual day
11. Scaling
 - AWS? GCP?
 - Network balancer + Application Balancer
12. Database
 - Define which DB

