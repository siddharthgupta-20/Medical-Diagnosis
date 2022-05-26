
Decision Tree Implementation
dataset: https://www.kaggle.com/itachi9604/disease-symptom-description-dataset/code

==============================================================================================================================================

->the input in the web page should be among the list of the symptoms present in the dataset set space seperated.
->then click on the button in order to predict the outcome 

->working of the tree:
    The tree is designed in such a way that at each iteration it will sub divide the dataset corresponding to the symptom having maximum information gain and finally return the label that is present in max amount in the leaf node ie. the final dataset after dividing.
    The idea behind the tree is to find the  prominent symptom(having maximum information gain in that dataset) and then checking if that symptom is present in the user provided symptom or not. Then accordingly, sub dividing the dataset ie. is symptom present then taking that datapoints in which that symptom is present.  

->furthermore, to avoid the constraint of using particular name for a symptom we can make a dictionary of related words.