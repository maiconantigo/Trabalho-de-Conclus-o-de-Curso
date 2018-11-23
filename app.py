import numpy as np
import pandas as pd

base = pd.read_csv('base.csv')
classe = base.pop(base.keys()[-1])
previsores = base.values

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

scaler_previsores = scaler.fit(previsores)
previsores2 = scaler_previsores.transform(previsores)

from sklearn.neural_network import MLPRegressor

modelo = MLPRegressor(hidden_layer_sizes = (50, 30), learning_rate = 'adaptive', max_iter = 1000)

modelo.fit(previsores2, classe)

def compare(item1, item2):
    comparacao = [np.concatenate(([item1[1], item1[2], item1[3], item1[4], item1[5], item1[6]], [item2[1], item2[2], item2[3], item2[4], item2[5], item2[6]]))]
    comparacao = scaler_previsores.transform(comparacao)
    return modelo.predict(comparacao)

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def geradados(Nome, tarefas, ciclo):
    ntars = []
    for t1 in tarefas:
        ntars.append(
            [
                t1.codigo,
                t1.categoria_tarefa(), 
                t1.origem_tarefa(),
                t1.categoria_cliente(),
                t1.cliente_implantacao(),
                t1.media_satisfacao(),
                t1.tempo_espera(),
            ]
        )

    ntars = np.array(ntars)

    tarefas_ordenadas = sorted(ntars, key=cmp_to_key(compare))
    tarefas_ordenadas = np.array(tarefas_ordenadas)

    print('Execução: %s Ciclo: %s' % (Nome, ciclo))    
    for t in tarefas_ordenadas:
        peso = t[1] + t[2] + t[3] + t[4] + t[5] + t[6]        
        print("codigo: %.2f categoria_tarefa: %.2f origem_tarefa: %.2f categoria_cliente: %.2f cliente_implantacao: %.2f media_satisfacao: %.2f tempo_espera: %.2f peso: %.2f" % (t[0], t[1], t[2], t[3], t[4], t[5], t[6], peso))


#o conjunto que será classificado deve ser previamente carregado 
geradados('25 Tarefas', tars25, 1)
#geradados('35 Tarefas', tars35, 1)
#geradados('50 Tarefas', tars50, 1)
#geradados('75 Tarefas', tars75, 1)
#geradados('100 Tarefas', tars100, 1)