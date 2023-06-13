# Microservices architecture for composing search and information extraction solutions
This project consists in providing a software, using a microservices architecture, that allows a programmer of a certain model, from the documentation of the developed platform, to implement its model in several machines simultaneously in an automatic way, achieving scalability, and the model can be accessed and interacted with through a web page or even through the API of the model. 

Author: Gonçalo Freixinho - goncalofreixinho@ua.pt - University of Aveiro

Check the version of Docker or install it
-----------------------------------------
Check if you have docker installed and what version you have. If you don't have it, install. In the development of this project Docker version 20.10.21 was used. It is indicated to have the same version on all machines that will be in the Swarm Cluster.
```
docker --version
```

Clone the repository code
-----------------------------------------
```
git clone https://github.com/goncalofreixinho/Platform_Master.git
```
Check SSH Keys permissions
-----------------------------------------
You need to have SSH Keys permissions to be able to add the machines you want to the Swarm Cluster automatically. This requires the username on all machines you wish to add to the Swarm Cluster as Worker Node to be "admin".

Check the value of the Token
-----------------------------------------
By default, the value of the database access Token is always the same. It is recommended to change this value by changing it in the "Token.env" file found in the root directory of the project.

How to Run 
---------------------------------------

To run the Platform, you need to execute the command ./run with some arguments:

1º Argument: Python file for the created model.

2º Argument: Txt file containing the IPs of the machines that will be worker nodes (each ip must be on a different line).

3º Argument: IP that will be the manager node to start the Swarm Cluster.

For example:
```
./run my_model.py list_ips.txt 123456789
```

How to Update 
---------------------------------------
If you make changes to your model and want to update it, without having to stop the Stack and Swarm Cluster created, you can do so using the following command in the root directory of the project:
```
./update
```
How to replicate Django Service
---------------------------------------
When Swarm Cluster is created, three replicas of the Django service are created by default. If you want to change the number of replicas of that service, simply enter the number of replicas you want as an argument, using the following command:

For example:
```
./replication 6
```
