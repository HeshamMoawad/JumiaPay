# import pandas as pd
# import openpyxl

# wb = openpyxl.load_workbook('yas.xlsx')
# ws = wb['Sheet1']
# df = pd.DataFrame(ws.values)
# df.dropna(inplace=True)
# h = df[12:]
# print(h[1:])


# response = []
# for row in df.index:
#     res = (f"{df.iloc[row][0]}",f"{df.iloc[row][1]}")
#     if f"{df.iloc[row][0]}" != 'None' :
#         response.append(res)
# header = df.loc[0]
# df.drop(0 , inplace= True)
# df.columns = header.tolist()
# code = df[['Code','Number']]
# Number = df['Number']

# # print(df)
# # print(header)
# print(code)
# code['Numbersss'] = Number.to_list()
# print(code)



