
def compare_df(dfA, dfB):
    npA = dfA.to_numpy()
    npB = dfB.to_numpy()
    list_difference = [element.tolist() for element in npA if element not in npB]
    return list_difference