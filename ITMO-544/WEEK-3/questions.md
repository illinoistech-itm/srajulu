## Chapter 01 - Designing for a Distributed World

1. What is distributed computing?

    The technique of designing huge systems that distribute work across multiple machines is known as distributed computing. In distributed computing, hundreds or thousands of devices generally collaborate to deliver a huge service.

2. Describe the three major composition patterns in distributed computing.

    The three major composition patterns are:

    i. Load balancer with multiple backend replicas.

    As the name suggests, this pattern consists of a Load balancer and multiple backend replicas, the role of load balancer is to send the requests received by it to a backend replica, the selection of which backend will receive the request has two methods, round robin and least-loaded scheme. In round robin requests are sent in an alternative manner in a loop. For least-loaded scheme the load balancer constantly need to keep a health check (using some metric(s)) of all the backend replicas, so that it know which replicas are available to receive the request, this method seems easy but creates problems when backend replicas are overloaded and start to fail, solution to this problem is to use a slow start algorithm called less naive least-loaded.


    ii. Server with multiple backends

    The server accepts a request, sends queries to several backend servers, and then assembles the final response by merging the responses. When the initial query can be readily deconstructed into a number of independent queries that can be merged to produce the final result, this method is generally adopted. This type of pattern has several advantages, t he backends operate in parallel, t he response does not have to wait for one backend task to finish before starting the next. The system is not tightly coupled. Even if one of the backends fails, the page may still be built by putting in some default information or leaving that part blank.

    iii. Server tree

    A number of servers collaborate, with one serving as the tree root, parent servers underneath it, and leaf servers at the bottom of the tree. This technique is typically used to gain access to a big dataset or corpus. Because the corpus is greater than any one computer can contain, each leaf holds a fraction or shard of the total. To query the whole dataset, the root gets the initial query and passes it to the parents. The query is sent to the leaf servers, which search their sections of the corpus. Each leaf transmits its findings to the parents, who sift and filter them before sending them up to the root. The root then takes all of the parents' responses, combines them, and responds with the entire answer.


3. What are the three patterns discussed for storing state?

    i. State kept in one location.
    
    ii. State sharded and replicated (similar to Load balancer with multiple backend replicas composition pattern)

    iii. Master Slave pattern (Similar to server tree composition pattern)


4. Sometimes a master server does not reply with an answer but instead replies with where the answer can be found. What are the benefits of this method?

    i. When huge volumes of data are being transmitted, a variant of that pattern is more suited.

    ii. Ideally suited for heavy read requests.

    iii. The master would not get quickly overburdened while receiving and relaying massive amounts of data.

    iv. This eliminates the need for the master to act as a middle man for massive data transfers.


5. Section 1.4 describes a distributed file system, including an example of how reading terabytes of data would work. How would writing terabytes of data work?

    The master could reply with a list of machines that have the memory available for the data to be written, and then the requestor could directly write the data to the backend machines, without overloading the master.

6. Explain the CAP Principle. (If you think the CAP Principle is awesome, read “The Part-Time Parliament” (Lamport & Marzullo 1998) and “Paxos Made Simple” (Lamport 2001).)

    CAP is an acronym for consistency, availability, and partition resistance. According to the CAP Principle, it is not feasible to create a distributed system that ensures consistency, availability, and partition resistance. Any one or two of these can be accomplished, but not all three at the same time.

    * **Consistency:** The term "consistency" refers to all nodes seeing the same data at the same time. If there are several replicas and an update is being processed, all users, even if they are reading from separate replicas, see the update go live at the same time. Systems that do not promise consistency may eventually deliver consistency.

    * **Availability:**  Availability ensures that every request receives a response indicating whether it was successful or unsuccessful. In other words, it indicates that the system is operational. According to the CAP Principle, availability also ensures that the system can notify failure.
    
    * **Partition Tolerance:** Partition tolerance refers to the ability of a system to continue operating in the face of unexpected message loss or failure of a component of the system. The most basic example of partition tolerance is when the system runs smoothly even if the machines involved in delivering the service lose their capacity to interact with one another due to a network link failure.



7. What does it mean when a system is loosely coupled? What is the advantage of these systems?

    Loosely coupled systems are those where a large systems are built using other smaller services, which operate independently. These services use abstraction, this enables them to hide their implementation from other services. Advantages of having loosely coupled systems are that they are easy to replace, upgrade, and if implemented properly the enitire architecture becomes scaleable.

8. How do we estimate how fast a system will be able to process a request such as retrieving an email message?

    Speed is one of the crucial metric with respect to get information, store information, compute and transform information, and transmit information. To make an estimation for building a design we can break down the transaction into smaller chunks and take in important factors into considerations, such as how much time will it take for data to be transmitted and received from point A to point B, type of storage device, medium/channel of data transmission,  perform calculation for time required for these transactions to be completed, if the result fits our time budget then we can proceed with our design, or re-evaluate for a better design or alternative measures, such as using different hardware to make our design better.

9. In Section 1.7 three design ideas are presented for how to process email deletion requests. Estimate how long the request will take for deleting an email message for each of the three

    For this example will consider location same as California and Netherlands.


* Approach 1: contacting the server and deleting it from storage: 

150ms for data transfer both ways.
Average size of email is 75 KB,  30 ms to read
Time for seek (best case scenario 1 seek) 10ms




