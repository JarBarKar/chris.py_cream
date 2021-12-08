# Coding SOP #

1.	Identify the tasks assigned to you, go to Jira dashboard, and shift the tasks to in progress
2. Check Slack channel and Github for any existing unresolve pull request
    - If no merge conflict, review code and merge into main
    - If there is conflict, review code and raise conflict issue with code owner 
3. Pull the repository from Github into local working environment
4.	Create new branch with the naming convention
    *	Creation of new class/feature : “Creation of Class name”
    *	Modification of new class/feature : “Modification of Class name”
    *	Bug Fixes : “Bug fixes for Class”
5.	Publish branch to main repo
6.	Start coding on the tasks assigned
    *	Prior to any class creation, check the ER diagram for the latest design. Check the sql file to ensure the design has been implemented correctly. Create the class based         on the design shown in the sql file
    *	For creation of new class, name the class by capitalising the first letter. If the class name is more than one word, join the words with an underscore. Examples:
          - Course
          -	Academic_record
    *	Class modification. In the event changes are made to a class, check the ER diagram for the changes made. Modify the sql file and update the dummy data word document.           Modify the code according to the sql file, check through all routes related to the class to ensure all changes are reflected correctly. Modify the test cases according         to changes and run all test cases to ensure change has been executed correctly.
    *	Route response. We generally use 2 types of responses only for the sake of simplifying things.
          -	200 – ok cases
          -	500 – anything that goes wrong
7.	After all work has been done, save the work. Add a title of what has been done and a summary of the changes/new work done if needed. Commit the changes to branch. And            pull the commit to the Github repo. If all is fine with the code, create a pull request for the branch to be merged with main.
8.	Check Jenkins to see if the test cases have gone through fine without any errors. If error arises, resolve the errors till all test cases pass on jenkins before moving on to the next step.
9.	Determine whether the changes/new work in the branch requires peer review
    *	Small changes and bug fixes (common agreement that no peer review is needed, merge on your own)
    *	New code like creation of classes, modification of existing code to fit new design (request for code review in slack channel to notify team that code has been done and         pushed)
10.	For code reviewers. Check if the pull request has any merge issues.
    *	If yes, try to determine the reason of conflict and inform code owner, else just inform code owner
    *	If no, look through the code to identify any potential issues. Approve the pull request if there are no issues, else raise concerns with code owner
 
