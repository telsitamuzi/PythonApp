Feature: Login to Event Application

User Story: As a user, I want to log into my account so I can view events specific to me

Scenario: As a user, I want to navigate to the login page so that I can login to my account.
Given I am on the login page
When I first open the website
Then I should see the username and password field
And I can enter my username and password
And click the submit button
Then I should be on the home page
