from IPython.display import HTML
import pandas as pd
  
# creating the dataframe
df = pd.DataFrame({"Name": ['Anurag', 'Manjeet', 'Shubham', 
                            'Saurabh', 'Ujjawal'],
                     
                   "Address": ['Patna', 'Delhi', 'Coimbatore',
                               'Greater noida', 'Patna'],
                     
                   "ID": [20123, 20124, 20145, 20146, 20147],
                     
                   "Sell": [140000, 300000, 600000, 200000, 600000]})
  
text_file = open("indexs.html", "w")
text_file.write(df.to_html())
text_file.close()
