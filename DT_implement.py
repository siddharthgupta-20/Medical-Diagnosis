import pandas as pd
#from sklearn.model_selection import train_test_split
import numpy as np
import math
import streamlit as st

#for calculating the entropy of the dataset divided
def entropy(dataset):
    sys_entropy = 0
    freq = dict()
    for i in dataset['disease']:
    
        if i in freq:
            freq[i] +=1 
        else:
            freq[i] = 1
        
    for keys in freq.keys():
        prob1 = freq[keys]/len(dataset['disease'])
        prob2 = 1 - prob1
        if prob1 != 1:
            sys_entropy += -(prob1*math.log(prob1,2))-(prob2*math.log(prob2,2))
        else:
            sys_entropy = 0
    return sys_entropy


#for calculating the frequency of a specific disease in a particular divided dataset
def freq(diseases):
    rt =dict()
    for i in diseases['disease']:
        if i in rt.keys():
            rt[i] +=1
        else:
            rt[i] =1
    maxi = max(rt, key=lambda x:rt[x])
    
    return maxi


#loading the data
df = pd.read_csv("dataset.csv")
df2 = pd.read_csv('symptom_Description.csv')
df3 = pd.read_csv('symptom_precaution.csv')



#finding all diferent symptoms
s=[]
for i in range(0,len(df['Disease'])):
    temp =[]
    for j in range(1,18):
        symp = 'Symptom_'+str(j)
        if(pd.isnull(df[symp][i])):
            break
        temp.append(df[symp][i].replace(' ',''))
    s.extend(temp)
s =list(set(s))

print(len(s))
s.append("disease")

#the dataframe will store the data in the required format(column names as symptoms) i.e. for each symptom 1 if present and 0 if not for a particular disease
new_df = pd.DataFrame(0,index = np.arange(0,len(df['Disease'])),columns=s)
for i in range(0,len(df['Disease'])):
    for j in range(1,18):
        symp = 'Symptom_'+str(j)
        if(pd.isnull(df[symp][i])):
            break

        new_df.at[i,df[symp][i].replace(" ","")] = 1
        #new_df.loc[:,(df.loc[:,(symp,i)],i)] = 1
#new_df['disease'] = df['Disease'].tolist()

new_df ['disease'] = df['Disease'].tolist()


#input the infections of the user in the web page
infections = [x.lower() for x in st.text_input('Type your symptoms',' ').split(' ')]
t = st.button("click here")

# we will convert the user input into a dataframe just in the format of new_df 
test = pd.DataFrame(0, index =[0],columns =s)


#the tree is defined here. The logic behind tree traversal is given in the README file
#accuracy of the tree: 100%
def TREE(dataset,sympt):
    for j in range(63):
        system = entropy(dataset)
        if system ==0:  #stop traversing if the divided dataset contains only one class
            break
        else:
            dataset2 =dataset.drop('disease', axis=1)
            sub =0
            maxim = 0
            t2 =''
            for i in dataset2.columns:
                count1 =dataset.loc[dataset2[i] == 1]
                count2 =dataset.loc[dataset2[i] == 0]
                prob3 =len(count1[i])/(len(count1[i])+len(count2[i]))
                prob4 =len(count2[i])/(len(count1[i])+len(count2[i]))
                sub = (prob3*entropy(count1))+ (prob4*entropy(count2))
                if (system - sub)>maxim:
                    maxim = system-sub
                    t2 =i
            temp=sympt.get(key = t2)
            #if the symptom on which the dataset is divided is present in the input
            if int(temp) == 1:    
                dataset3 = dataset.loc[dataset[t2] == 1]
                dataset = dataset3.drop(i, axis=1)
            elif int(temp) == 0:
                dataset4 = dataset.loc[dataset[t2] == 0]
                dataset = dataset4.drop(i, axis=1)
            sympt.drop(i, axis =1)
        j+=1
    return dataset  #finally return the dataset in which the predicted class is maximum


#triggered when button is clicked on the web page
def pred(infect,sympt,columns,dtset):
    for i in infect:
        if i in columns:
            sympt[i][0] =1
    output = TREE(dtset,sympt)
    print(freq(output))
    st.write(freq(output))
    return freq(output)


#if button pressed
if t == True:
    result = pred(infections,test,s,new_df)
    print(result)

    #if the predicted disease is in description dataset then print discription
    if result in df2['Disease'].tolist():
        st.write(df2['Description'][df2['Disease'].tolist().index(result)])
       
    if result in df3['Disease'].tolist():
        print("Precautions:")
        st.write("precautions:")
        st.write(df3['Precaution_1'][df3['Disease'].tolist().index(result)])
        st.write(df3['Precaution_2'][df3['Disease'].tolist().index(result)])
        st.write(df3['Precaution_3'][df3['Disease'].tolist().index(result)])
    





