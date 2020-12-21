# Security
#### Mohammed Ahmad
====
The security of user information is of great importance. As an added benefit of using flask - a python microframework - and sqlalchemy - an object relational mapping framework - to provide users with an interactive web experience; the frameworks also protect the information of users by together sanitising user input and mitigating sql injection.

### Input sanitisation
Input sanitisation is the process in which the user input is taken and is parsed of anything that could trigger unusual functioning. In python this includes the special characters like ",' and \. When these are present in an input python will read them as part of the code and with the correct combination and execution, malicious parties can get python to run code that they want it to run. Alternatively users can inject javascript into the database that can run on other users' machines. The implications of this is that the attacker can use python and javascript to pilfer or corrupt data as well as create backdoors and expose more vulnerabilities.

Luckily flask automatically reads all form data as raw string literals and so there is no need for the special characters to be escaped. This is by default the way inputs are read in python3 and thus there is no confusion for the developer. Furthermore flask also provides the user with a function that converts user input into a file system safe format so that files can be easily stored on the system without causing breaking errors.

Flask, by default, configures Jinja2 to handle cross-site scripting by automatically escaping all user created data. This is thus a very effective form of santisation and its inclusion in flask is a very good thing. However, this even includes input from the server side which as a result prevented the twitter_extended application from adding html from an input that functions executed on. To workaround this instead of disabling the escaping of inputs it was decided that javascript would instead be used to create html elements when the page loaded. Because this work around exists without reducing security flask's inclusion of the auto escaping feature is overall an effective solution.

Flask can also be configured to use marshmallow. A serialization/deserialization library that ensures that the data passed to python is valid.

## Mitigating SQL injection
SQL injection is a very devastating attack which can allow malicious actors to directly execute sql code through the inputs of the application. This is due to a lack of security between the bridge from the api programming language to the sql database language. The implications of this means that attackers can view or delete the entire database with just a single well crafted input.

ORM's resolve this issue by being the bridge between the api language and the database language, performing all the required validation and sanitisation to make the data safe, before forwarding the data to the database. Because the ORM has been developed with the efforts of many developers that have familiarised themselves with the possibilties of sql injection; the ORM that they've developed is extremely robust and handles just about every possible weak point. For the developer this means they do not have to manually research and create code to handle sql injection and as aresult their job is made easier and there is no room for human error.

SQLalchemy provides this very service by interfacing directly with flask and flask marshmallow. Instead of simply creating a insert statement that will insert data into the database an insert statement is automatically created by sqlalchemy when an initialized sqlalchemy model is added to a session in the orm. The statement then executes and if an error occurs within the database the ORM will raise that error in python3, adding even more security to the process. On the other hand SQLalchemy takes away from the traditional style of working with a database and abstracts it to the point where the developer does not work with sql  except under very special cirucmstances. This can be seen as both a good and bad thing as the developer might not have any understanding of how the database works but is still able to get by with the orm.



# Obligations of a developer
A developer has professional, ethical and legal obligations both in and out of the workplace. This report aims to discuss whether these obligations are warranted and who/what is impacted by them.

## professional obligations
Professional obligations are those obligations associated with being courteous and responsible when carrying out ones duties. This involves the professional properly understanding and communicating the responsibilities of their role as well as well as more nuanced details such as delivering their work on time. There is more to it than just blind compliance however; being a professional also means that one is able to have boundaries of their own which should be respected.

### Timely delivery
Corporate entities function on deadlines and for the entities to be efficient it is extremely important that deadlines are met. As a developer/operations professional there is a degree of leniency that is afforded by employers due to the unpredictable nature of working in an industry with no firm procedures. This leniency however should only be extended in the event where the developer is facing actual difficulty and not complacent because their untimeliness is very likely to upset numerous people.

On the other hand, management has been known to rush developers to meet unrealistic deadlines without understanding the consequences of doing so. Very often, as a result of the rushed circumstances the developer is forced to compromise the quality of their work. However very often is this recognized as a lack of professionalism on managements behalf and the high turnover in the industry is most likely telling of this double standard. In a true professional setting developers should not be forced to compromise on the quality of the system they are working on in exchange for a faster delivery to the market.

### Explicitness about ongoing maintenance of systems
With the ever growing needs of consumers there is always a need to update the systems in place whether that means scaling the system to handle larger loads or adopting new technology to provide new services or improve already existing services. Other things like security and resources always need to be maintained. Ultimately developers need to communicate the importance that they play once the product is pushed to the market and the development role they fulfilled is over.

This also means that employers need to understand what is being communicated to them and be completely aware of the consequences of an impulsive measure to cut costs such as making the developers redundant once development has ended.

## Ethical obligations
Ethical obligations are at most times independent of legal obligations. An action may not have any legal implications however if it is going to effect someone/something negatively then it is of ethical concern. Two notorious ethical concerns are the collection of data by organizations and working for corporations that have a negative impact on society.

### Collection of data
Collecting information on users is a very common practice in the industry and organizations are able to make detailed profiles on their users without running into any legal trouble. This is an ethically questionable practice as if the organization does not properly secure the information of their users, the information can be used by hackers to harm them. Developers are unlikely to have a say in what data the organization collects on users, however very often the developer is responsible for making sure that the data does not fall into the wrong hands. Therefore it is the developers ethical responsibility to ensure they have done their due diligence in properly securing the systems and minimizing the amount of damage that would be caused in the event of a security breach.

### Choosing who to work for
The developer has the final say in who they choose to work for. This means that the ethical responsibility of aiding companies that are malicious in nature falls on the developer. Unfortunately companies that don't practice good ethics also have monetary incentives that may make it difficult for a developer to turn them down. On the other hand developers can also work for organizations that do a great deal of good and are more often than not their choice goes unrecognized. Ultimately the developer is best suited to make the final decision on which organizations they provide their services to and the developer at the very least should be able to live with the direct consequences of the work they end up doing. 

## Legal obligations
Legal obligations are the obligations that are directly tied in with the law. Unlawful actions that a developer takes are directly punishable by the government they are liable for. This includes bringing harm to the public or breaking the terms of agreement they sign when they begin working for an employer.

### Software Development Agreement
The software development agreement is an agreement signed by employer and employee to protect  intellectual property. More often than not however the employer manages to sneak a few conditions in that are disadvantageous to the developer such as a non compete clause which persists even after the employee contract is terminated. Other parts of the agreement 
require confidentiality from the developer while prohibiting the developer of any ownership of the product they are working on. While these are all very legal practices that do protect the intellectual property of the company, they are also hazardous to the well being of the developer. 

### Public safety
Developers have a lot of power over others and this trend is only becoming more potent. Developers can use their positions to commit acts of terrorism such as adding malware to self driving cars that cause traffic collisions. When developers add in this malicious code they are legally prosecutable and can be charged with felonies. Additionally developers can be held responsible for tragedies when they had no evil intent simply because they are a scape goat for when things go wrong.