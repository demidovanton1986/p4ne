from matplotlib import pyplot
from openpyxl import load_workbook

wb = load_workbook("data_analysis_lab.xlsx")
# print(wb["Data"]["A"][5].value)


def extract_value(cell):
    return cell.value


a_column = list(map(extract_value, wb["Data"]["A"][1:]))
b_column = list(map(extract_value, wb["Data"]["B"][1:]))
c_column = list(map(extract_value, wb["Data"]["C"][1:]))
d_column = list(map(extract_value, wb["Data"]["D"][1:]))

print(a_column)
print(c_column)

pyplot.plot(a_column, c_column, label="Относительная температура")
pyplot.plot(a_column, d_column, label="Активность")

pyplot.xlabel('Годы')
pyplot.legend()
pyplot.show()
