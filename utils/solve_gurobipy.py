import pandas as pd
import gurobipy as gb

def solve_gurobipy(time_params, machines_cool_down_times = {1:4, 2:10, 3:5, 4:20, 5:0}, A_finish_time=60):
    model = gb.Model(name="Machine Product")

    machines = [1, 2, 3, 4, 5]
    products = [1, 2, 3]
    products_dict = {1:"A",2:"B",3:"C"}

    X = model.addVars(((i, j) for i in machines for j in products) , vtype=gb.GRB.INTEGER, name='X') 
    Y = model.addVars(((i, j) for i in machines for j in products), vtype=gb.GRB.CONTINUOUS, name="Y")
    P = model.addVar(vtype=gb.GRB.BINARY, name="P")
    F1 = model.addVar(vtype=gb.GRB.BINARY, name="F1")
    F2 = model.addVar(vtype=gb.GRB.BINARY, name="F2")
    F3 = model.addVar(vtype=gb.GRB.BINARY, name="F3")
    G = model.addVar(vtype=gb.GRB.BINARY, name="G")
    K = model.addVar(vtype=gb.GRB.BINARY, name="K")
    Q = model.addVar(vtype=gb.GRB.BINARY, name="Q")

    L = model.addVar(vtype=gb.GRB.INTEGER, name="L")

    model.setObjective(L, gb.GRB.MINIMIZE)
    model.setParam('OutputFlag', 0)

    M = 1000

    machines_cool_down_times = {1:4, 2:10, 3:5, 4:20, 5:0}

    model.addConstr(L >= Y[4, 1])
    model.addConstr(L >= Y[5, 2])
    model.addConstr(L >= Y[5, 3])

    for machine in machines:
        for product in products:
            model.addConstr(Y[machine, product] >= X[machine, product])
            model.addConstr(X[machine, product] + time_params[machine, product] == Y[machine, product])

    for j in products:
        for i in range(1,len(machines)):
            model.addConstr(Y[i, j] <= X[i+1, j])
    model.addConstr(Y[5, 2] <= Y[5, 3] + 15)

    model.addConstr(Y[4, 1] <= A_finish_time)

    model.addConstr(X[1, 1] - Y[1, 2] >= machines_cool_down_times[1] - M*P)
    model.addConstr(X[1, 2] - Y[1, 1] >= machines_cool_down_times[1] - M*(1 - P))

    model.addConstr(X[2, 2] - Y[2, 1] >= machines_cool_down_times[2] - M*F1)
    model.addConstr(X[2, 1] - Y[2, 2] >= machines_cool_down_times[2] - M*(1 - F1))
    model.addConstr(X[2, 3] - Y[2, 1] >= machines_cool_down_times[2] - M*F2)
    model.addConstr(X[2, 1] - Y[2, 3] >= machines_cool_down_times[2] - M*(1 - F2))
    model.addConstr(X[2, 2] - Y[2, 3] >= machines_cool_down_times[2] - M*F3)
    model.addConstr(X[2, 3] - Y[2, 2] >= machines_cool_down_times[2] - M*(1 - F3))

    model.addConstr(X[3, 3] - Y[3, 1] >= machines_cool_down_times[3] - M*G)
    model.addConstr(X[3, 1] - Y[3, 3] >= machines_cool_down_times[3] - M*(1 - G))

    model.addConstr(X[4, 1] - Y[4, 2] >= machines_cool_down_times[4] - M*K)
    model.addConstr(X[4, 2] - Y[4, 1] >= machines_cool_down_times[4] - M*(1 - K))

    model.addConstr(X[5, 2] - Y[5, 3] >= machines_cool_down_times[5] - M*Q)
    model.addConstr(X[5, 3] - Y[5, 2] >= machines_cool_down_times[5] - M*(1 - Q))

    model.addConstr(F2 + F3 - F1 >= 0)
    model.addConstr(F2 + F3 - F1 <= 1)

    model.update()
    model.optimize() 

    result = {}

    for i in model.getVars():
        result[i.VarName] = (i.X)
    Z = model.getVarByName("L").X

    return Z
    