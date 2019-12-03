# 3D Data processing in structural biology research project
#### Authors: Shay Guterman & Oren Wintner, Supervised by Dina Schneidman
_______________________________________________
Further explained at the power point presentation.

### Motivation: 
Google deep mind team intreduced AI algorithms to the field of computational biology in order to solve unsolvable problems and accelerate demanding computations. Said algorithms can help us understand proteins better and can be applied to improve our health care and medicines.
[Nature article describing the work](https://www.nature.com/articles/d41586-019-01357-6)

### The challenge: 
Protein family(CATHCODE) classification. Can we create an algorithm that can classify proteins through spatial data? Here are 5 representation of 4 proteins, the challenge is to classify each subplot according to its title<br/>
![prediction example](https://i.ibb.co/2qt1VgG/protein-class-task3.png)
### The Data:
The data is mined directly from the PDB (Protein Data Bank). Using one text file to chose the most represented family, and another text file to download the relevant PDB files. We cropped the PDB files to hold only the protein we are intrested in and deleted everything else. We kept the family of every protein to be used as label and N X,Y,Z cloud points as train data. The N Points were mostly sampled from the "skeleton" of the Protein, The C_alpha, C_beta and C_gamma's. 

### Solution Approach: 
Using PointNet [arXiv paper](https://arxiv.org/pdf/1706.02413.pdf) neural network we will solve the task. We feed the network A train array of 40 families, for each family we have 400 example, each example has 256 X,Y,Z cloud points. For the label array, we have an array of size 40 (families) * 400 (examples per family) of numbers between 0 to 39. In short, the dimensions of the train are (40*400 (total examples),256(points),3(X,Y,Z)) and label array of (40 * 400 - integers between 1 and 40)
![prediction example](https://i.ibb.co/WP55hzc/point-net-image2.png)

### First solution: 
We adjusted the dropout, pushed each protein to be centered around zero, zero padded missing values, tuned the augmentation changed some hyper parameters alongside introduction of learning rate plan. 
#### Training plot of the accuracy, we achieved 67% accuracy on a subset of the families
![prediction example](https://i.ibb.co/2SzTSxv/Accuracy-17-67.png)

### Final solution:
We conjuctured that the network might not find the right input rotation, therefore, unable to classify the families. In order evaluate our cojecture we aligned the protein families using classical alignment algorithm before feeding it to the network. 
![prediction example](https://i.ibb.co/LPLpTPx/conf-mat.png)
