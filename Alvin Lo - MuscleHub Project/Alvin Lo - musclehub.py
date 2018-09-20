
# coding: utf-8

# # Capstone Project 1: MuscleHub AB Test

# ## Step 1: Get started with SQL

# Like most businesses, Janet keeps her data in a SQL database.  Normally, you'd download the data from her database to a csv file, and then load it into a Jupyter Notebook using Pandas.
# 
# For this project, you'll have to access SQL in a slightly different way.  You'll be using a special Codecademy library that lets you type SQL queries directly into this Jupyter notebook.  You'll have pass each SQL query as an argument to a function called `sql_query`.  Each query will return a Pandas DataFrame.  Here's an example:

# In[1]:


# This import only needs to happen once, at the beginning of the notebook
from codecademySQL import sql_query


# In[2]:


# Here's an example of a query that just displays some data
sql_query('''
SELECT *
FROM visits
LIMIT 5
''')


# In[3]:


# Here's an example where we save the data to a DataFrame
df = sql_query('''
SELECT *
FROM applications
LIMIT 5
''')


# ## Step 2: Get your dataset

# Let's get started!
# 
# Janet of MuscleHub has a SQLite database, which contains several tables that will be helpful to you in this investigation:
# - `visits` contains information about potential gym customers who have visited MuscleHub
# - `fitness_tests` contains information about potential customers in "Group A", who were given a fitness test
# - `applications` contains information about any potential customers (both "Group A" and "Group B") who filled out an application.  Not everyone in `visits` will have filled out an application.
# - `purchases` contains information about customers who purchased a membership to MuscleHub.
# 
# Use the space below to examine each table.

# In[4]:


# import functions library from codecademySQL
from codecademySQL import sql_query


# In[5]:


# Examine first 5 rows of data of visits table
sql_query('''
SELECT *
FROM visits
LIMIT 5
''')


# In[6]:


# Examine first 5 rows of data of fitness_tests table
sql_query('''
SELECT *
FROM fitness_tests
LIMIT 5
''')


# In[7]:


# Examine first 5 rows of data of applications table
sql_query('''
SELECT *
FROM applications
LIMIT 5
''')


# In[8]:


# Examine first 5 rows of data of purchases table
sql_query('''
SELECT *
FROM purchases
LIMIT 5
''')


# We'd like to download a giant DataFrame containing all of this data.  You'll need to write a query that does the following things:
# 
# 1. Not all visits in  `visits` occurred during the A/B test.  You'll only want to pull data where `visit_date` is on or after `7-1-17`.
# 
# 2. You'll want to perform a series of `LEFT JOIN` commands to combine the four tables that we care about.  You'll need to perform the joins on `first_name`, `last_name`, and `email`.  Pull the following columns:
# 
# 
# - `visits.first_name`
# - `visits.last_name`
# - `visits.gender`
# - `visits.email`
# - `visits.visit_date`
# - `fitness_tests.fitness_test_date`
# - `applications.application_date`
# - `purchases.purchase_date`
# 
# Save the result of this query to a variable called `df`.
# 
# Hint: your result should have 5004 rows.  Does it?

# In[9]:


# import data from visits, fitness_tests, applications & purchases table with criteria into a dataframe variable
df = sql_query('''
SELECT visits.first_name, 
        visits.last_name, 
        visits.gender, 
        visits.email, 
        visits.visit_date, 
        fitness_tests.fitness_test_date,
        applications.application_date,
        purchases.purchase_date
FROM visits 
LEFT JOIN fitness_tests 
    ON visits.email = fitness_tests.email
    AND visits.first_name = fitness_tests.first_name
    AND visits.last_name = fitness_tests.last_name
LEFT JOIN applications
    ON visits.email = applications.email
    AND visits.first_name = applications.first_name
    AND visits.last_name = applications.last_name
LEFT JOIN purchases
    ON visits.email = purchases.email
    AND visits.first_name = purchases.first_name
    AND visits.last_name = purchases.last_name
WHERE visits.visit_date >= "7-1-17"
''')


# In[10]:


# Check number of records in dataframe df query
print(len(df))


# ## Step 3: Investigate the A and B groups

# We have some data to work with! Import the following modules so that we can start doing analysis:
# - `import pandas as pd`
# - `from matplotlib import pyplot as plt`

# In[11]:


# import modules for analysis. pandas and pyplot from matplotlib
import pandas as pd
from matplotlib import pyplot as plt


# We're going to add some columns to `df` to help us with our analysis.
# 
# Start by adding a column called `ab_test_group`.  It should be `A` if `fitness_test_date` is not `None`, and `B` if `fitness_test_date` is `None`.

# In[12]:


# Insert a column into df called ab_test_group to determine the test group per entry
df['ab_test_group'] = df.fitness_test_date.apply( lambda x: "A" if pd.notnull(x) else "B")


# In[13]:


# Check if ab_test_group column added properly to df with correct values
print(df.head(5))


# Let's do a quick sanity check that Janet split her visitors such that about half are in A and half are in B.
# 
# Start by using `groupby` to count how many users are in each `ab_test_group`.  Save the results to `ab_counts`.

# In[14]:


# Code to count how many visitors were in group A and B each
ab_counts = df.groupby(['ab_test_group']).visit_date.count().reset_index()


# In[15]:


# Check ab_counts to see if A and B visitors are evenly split
print(ab_counts)


# We'll want to include this information in our presentation.  Let's create a pie cart using `plt.pie`.  Make sure to include:
# - Use `plt.axis('equal')` so that your pie chart looks nice
# - Add a legend labeling `A` and `B`
# - Use `autopct` to label the percentage of each group
# - Save your figure as `ab_test_pie_chart.png`

# In[16]:


# Create pie chart to display results
plt.pie(ab_counts.visit_date.values, labels =["A", "B"],autopct='%0.2f%%')
plt.axis('equal')
plt.legend("A","B")
plt.savefig('ab_test_pie_chart.png')
plt.show()


# ## Step 4: Who picks up an application?

# Recall that the sign-up process for MuscleHub has several steps:
# 1. Take a fitness test with a personal trainer (only Group A)
# 2. Fill out an application for the gym
# 3. Send in their payment for their first month's membership
# 
# Let's examine how many people make it to Step 2, filling out an application.
# 
# Start by creating a new column in `df` called `is_application` which is `Application` if `application_date` is not `None` and `No Application`, otherwise.

# In[17]:


# Insert a column into df called is_application which determines if an application was done or not
df['is_application'] = df.application_date.apply( lambda x: "Application" if pd.notnull(x) else "No Application")


# In[18]:


# Check if is_application column added properly to df with correct values
print(df.head(5))


# Now, using `groupby`, count how many people from Group A and Group B either do or don't pick up an application.  You'll want to group by `ab_test_group` and `is_application`.  Save this new DataFrame as `app_counts`

# In[19]:


# Code to count how many visitors were in group A and B and of those groups how many picked up or didn't pick up application
app_counts = df.groupby(['ab_test_group','is_application']).visit_date.count().reset_index()


# In[20]:


# Print app_counts to see the breakdown of A and B visitors and their respective applications picked up or not
print(app_counts)


# We're going to want to calculate the percent of people in each group who complete an application.  It's going to be much easier to do this if we pivot `app_counts` such that:
# - The `index` is `ab_test_group`
# - The `columns` are `is_application`
# Perform this pivot and save it to the variable `app_pivot`.  Remember to call `reset_index()` at the end of the pivot!

# In[21]:


# Create a pivot of app_counts to show A & B groups who picked up or didn't pick up an application
app_pivot = app_counts.pivot(columns='is_application',index='ab_test_group',values='visit_date').reset_index()


# In[22]:


# Print the current version of the pivot
print(app_pivot)


# Define a new column called `Total`, which is the sum of `Application` and `No Application`.

# In[23]:


# Add a totals column to the pivot
app_pivot['Total'] = app_pivot["Application"] + app_pivot["No Application"]


# In[24]:


# Print pivot table with added Total column
print(app_pivot)


# Calculate another column called `Percent with Application`, which is equal to `Application` divided by `Total`.

# In[25]:


# Add a Percent with Application column to the pivot
app_pivot['Percent with Application'] = app_pivot["Application"] / app_pivot["Total"]


# In[26]:


# Print pivot table with added Percentage with Application column
print(app_pivot)


# It looks like more people from Group B turned in an application.  Why might that be?
# 
# We need to know if this difference is statistically significant.
# 
# Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[27]:


# Import the scipy library chi2_contingency test
from scipy.stats import chi2_contingency


# In[28]:


# Use chi2_contingency test to analyze results
contingency_table = [(250, 2254),(325,2175)]
chi2_stat, pvalue, dof, t = chi2_contingency(contingency_table)
print(pvalue)


# In[29]:


# There is a significant difference between group A & B because the p-value is less than 0.05


# ## Step 4: Who purchases a membership?

# Of those who picked up an application, how many purchased a membership?
# 
# Let's begin by adding a column to `df` called `is_member` which is `Member` if `purchase_date` is not `None`, and `Not Member` otherwise.

# In[30]:


# Insert a column into df called is_member which determines if a visitor purchased a membership or not
df['is_member'] = df.purchase_date.apply(lambda x: "Member" if pd.notnull(x) else "Not Member")


# In[31]:


# Check if is_member column added properly to df with correct values
print(df.head(5))


# Now, let's create a DataFrame called `just_apps` the contains only people who picked up an application.

# In[32]:


# Create a dataframe that only contains records of visitors who picked up an application
just_apps = df[(df.is_application == "Application")]


# In[33]:


# Print just_apps table to check if selection is correct
print(just_apps.head(5))


# Great! Now, let's do a `groupby` to find out how many people in `just_apps` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `member_pivot`.

# In[34]:


# Create pivot table to group by the visitors who are or aren't members from the A & B groups, add total and percentage of 
member_counts = just_apps.groupby(['ab_test_group','is_member']).visit_date.count().reset_index()
member_pivot = member_counts.pivot(columns='is_member',index='ab_test_group',values='visit_date').reset_index()


# In[35]:


print(member_pivot)


# In[36]:


# Add a Total and a Percent Purchase column
member_pivot['Total'] = member_pivot["Member"] + member_pivot["Not Member"]
member_pivot['Percent Purchase'] = member_pivot["Member"] / member_pivot["Total"]


# In[37]:


# Print updated pivot with Total and Percent Purchase columns
print(member_pivot)


# It looks like people who took the fitness test were more likely to purchase a membership **if** they picked up an application.  Why might that be?
# 
# Just like before, we need to know if this difference is statistically significant.  Choose a hypothesis tests, import it from `scipy` and perform it.  Be sure to note the p-value.
# Is this result significant?

# In[38]:


# Use chi2_contingency test to analyze results
contingency_table2 = [(200,50),(250,75)]
chi2_stat, pvalue, dof, t = chi2_contingency(contingency_table2)
print(pvalue)


# In[39]:


# There is not a significant difference between group A & B because the p-value is larger than 0.05


# Previously, we looked at what percent of people **who picked up applications** purchased memberships.  What we really care about is what percentage of **all visitors** purchased memberships.  Return to `df` and do a `groupby` to find out how many people in `df` are and aren't members from each group.  Follow the same process that we did in Step 4, including pivoting the data.  You should end up with a DataFrame that looks like this:
# 
# |is_member|ab_test_group|Member|Not Member|Total|Percent Purchase|
# |-|-|-|-|-|-|
# |0|A|?|?|?|?|
# |1|B|?|?|?|?|
# 
# Save your final DataFrame as `final_member_pivot`.

# In[40]:


# Create a pivot table to summarize members or not members from group A and B
total_members = df.groupby(['ab_test_group','is_member']).visit_date.count().reset_index()
final_member_pivot = total_members.pivot(columns='is_member',index='ab_test_group',values='visit_date').reset_index()
final_member_pivot['Total'] = final_member_pivot["Member"] + final_member_pivot["Not Member"]
final_member_pivot['Percent Purchase'] = final_member_pivot["Member"] / final_member_pivot["Total"]
print(final_member_pivot)


# Previously, when we only considered people who had **already picked up an application**, we saw that there was no significant difference in membership between Group A and Group B.
# 
# Now, when we consider all people who **visit MuscleHub**, we see that there might be a significant different in memberships between Group A and Group B.  Perform a significance test and check.

# In[41]:


# Use chi2_contingency test to analyze results
contingency_table3 = [(200,2304),(250,2250)]
chi2_stat, pvalue, dof, t = chi2_contingency(contingency_table3)
print(pvalue)


# In[42]:


# There is a significant difference between group A & B because the p-value is less than 0.05


# ## Step 5: Summarize the acquisition funel with a chart

# We'd like to make a bar chart for Janet that shows the difference between Group A (people who were given the fitness test) and Group B (people who were not given the fitness test) at each state of the process:
# - Percent of visitors who apply
# - Percent of applicants who purchase a membership
# - Percent of visitors who purchase a membership
# 
# Create one plot for **each** of the three sets of percentages that you calculated in `app_pivot`, `member_pivot` and `final_member_pivot`.  Each plot should:
# - Label the two bars as `Fitness Test` and `No Fitness Test`
# - Make sure that the y-axis ticks are expressed as percents (i.e., `5%`)
# - Have a title

# In[43]:


# Bar graph of app_pivot
ax = plt.subplot()
plt.bar(range(len(app_pivot)), app_pivot['Percent with Application'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0,0.05,0.10,0.15])
ax.set_yticklabels(['0%', '5%','10%', '15%'])
plt.xlabel("Group")
plt.ylabel("Percentage of Applicants")
plt.title('MuscleHub Visitors Who Fill Application')
plt.savefig("visitors_apply_percent.png")
plt.show()


# In[44]:


# Bar graph of member_pivot
ax = plt.subplot()
plt.bar(range(len(member_pivot)), member_pivot['Percent Purchase'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0,0.25,0.50,0.75,1.00])
ax.set_yticklabels(['0%', '25%','50%', '75%','100%'])
plt.xlabel("Group")
plt.ylabel("Percentage of Purchasers")
plt.title('MuscleHub Applicants Who Purchase Membership')
plt.savefig("apply_purchase_percent.png")
plt.show()


# In[45]:


# Bar graph of final_member_pivot
ax = plt.subplot()
plt.bar(range(len(final_member_pivot)), final_member_pivot['Percent Purchase'].values)
ax.set_xticks(range(len(app_pivot)))
ax.set_xticklabels(['Fitness Test', 'No Fitness Test'])
ax.set_yticks([0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12])
ax.set_yticklabels(['0%', '1%','2%', '3%','4%','5%', '6%','7%', '8%','9%','10%', '11%','12%'])
plt.xlabel("Group")
plt.ylabel("Percentage of Purchases")
plt.title('MuscleHub Visitors Who Purchase Memberships')
plt.savefig("visitor_purchase_percent.png")
plt.show()

