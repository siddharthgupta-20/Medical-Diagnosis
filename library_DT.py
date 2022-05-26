import pandas as pd
import streamlit as st
from sklearn import tree
from sklearn.model_selection import train_test_split
import numpy as np


#loading the dataset
df = pd.read_csv("dataset.csv")
df2 = pd.read_csv('symptom_Description.csv')
df3 = pd.read_csv('symptom_precaution.csv')

s=[]

#finding all the different symptoms in the dataset
for i in range(0,len(df['Disease'])):
    temp =[]
    for j in range(1,18):
        symp = 'Symptom_'+str(j)
        if(pd.isnull(df[symp][i])):
            break
        temp.append(df[symp][i].replace(" ",""))
    s.extend(temp)
s =list(set(s))
s.append("disease")

#creating new dataset which have columns as different symptoms
new_df = pd.DataFrame(0,index = np.arange(0,len(df['Disease'])),columns=s)

#updating the new dataset for each symptom whether it is for a particular disease or not
df.head()
for i in range(0,len(df['Disease'])):
    for j in range(1,18):
        symp = 'Symptom_'+str(j)
        if(pd.isnull(df[symp][i])):
            break

        new_df.at[i,df[symp][i].replace(" ","")] = 1
        


new_df ['disease'] = df['Disease'].tolist()


#creating the input dataset and the label dataset for the descision tree
inputs = new_df.drop('disease',axis='columns')
target = new_df['disease'] 






#spliting the data into training and test
x_train,x_test,y_train,y_test = train_test_split(inputs,target,test_size = 0.2)
model = tree.DecisionTreeClassifier()
model.fit(x_train,y_train)
print(model.score(x_test,y_test))

count =0
infections =[]
#button for the web page
t = st.button("click here")



#list storing the symptoms of the user
infections = [x.lower() for x in st.text_input('Type your symptoms',' ').split(' ')]





if('disease' in s):
    s.pop(-1)
print(len(s))

#test will store the symptoms of the user in the correct format
test = pd.DataFrame(0, index =[0],columns =s)


#have 3 arguements, symptoms list, an empty datframe which will be updated with the symptoms amd the symptoms list.
def pred(infect,sympt,columns):
    for i in infect:
        if i in columns:
            sympt[i][0] =1
    print(len(sympt.columns))
    print(model.predict(sympt))
    st.write(model.predict(sympt))
    return(model.predict(sympt))

#when button pressed the code will predict the disease and will return the discription and precaution if possible.
if t == True:
    print(infections)
    r=pred(infections,test,s)
    #if the predicted disease is in description dataset then print discription
    if r in df2['Disease'].tolist():
        st.write(df2['Description'][df2['Disease'].tolist().index(r)])
    #if precaution of the predicted disease is given then print it 
    if r in df3['Disease'].tolist():
        print("Precautions:")
        st.write(df3['Precaution_1'][df3['Disease'].tolist().index(r)])
        st.write(df3['Precaution_2'][df3['Disease'].tolist().index(r)])
        st.write(df3['Precaution_3'][df3['Disease'].tolist().index(r)])
