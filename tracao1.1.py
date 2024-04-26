#%% chamda
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy 

def indice_tencao_maior(vetor, ten):
    index_of_element = -1
    for i in range(len(vetor)):
        if vetor[i] >= ten:
            index_of_element = i
            break
    return index_of_element

def indice_tencao_menor(vetor, ten):
    index_of_element = -1
    for i in range(len(vetor)):
        if vetor[i] <= ten:
            index_of_element = i
            break
    return index_of_element

path = []

path = np.append(path,"exemplo1")
path = np.append(path,"exemplo2")
path = np.append(path,"exemplo3")
path = np.append(path,"exemplo4")
path = np.append(path,"exemplo5")
path = np.append(path,"exemplo6")
path = np.append(path,"exemplo7")
path = np.append(path,"exemplo8")

lim_esc = []
lim_res = []
tensao = []
deform = []
alongamento = []

path1 = []
for i in range(len(path)):
    un = path[i] + ".csv"
    path1 = np.append(path1,un)
    
save = []
for i in range(len(path)):
    un = path[i] + ".png"
    save = np.append(save,un)

for k in range(len(path)):
    ge = pd.read_csv(path1[k], skiprows=0, delimiter=",")
    
    strain = ge.iloc[:,2].tolist()
    stress = ge.iloc[:,4].tolist()
    
    for i in range(len(strain)):
        strain[i] = strain[i]/1000
    
# =============================================================================
#     Regressao para identificação do limite de escoamento
# =============================================================================
    
    ind_reg1 = indice_tencao_maior(stress, 400)
    ind_reg2 = indice_tencao_maior(stress, 600)
    
    aux1 = strain[ind_reg1:ind_reg2]
    auy1 = stress[ind_reg1:ind_reg2]
    
    slope1, intercept1, r_value, p_value, std_err = scipy.stats.linregress(aux1, auy1)
    
# =============================================================================
#     definicao do limite de resistencia (UTS)
# =============================================================================
    
    UTS = 0
    for i in range(len(stress)):
        if stress[i] >= UTS:
            UTS = stress[i]
    
    quebra1 = 0
    
# =============================================================================
#     determinacao do limite de escoamento
# =============================================================================
    
    for i in range(1,len(stress)):
        if stress[i-1]-stress[i] >= 10:
            quebra1 = i
    
    stress1 = stress[0:quebra1]
    strain1 = strain[0:quebra1]
        
    stress_aux = stress[quebra1:]
    strain_aux = strain[quebra1:]
    
    quebra2 = 0
    for i in range(len(stress_aux)):
        if stress_aux[i] >= stress1[quebra1-1]:
            quebra2 = i
            break
    
    stress2 = stress_aux[quebra2-1:]
    strain2 = strain_aux[quebra2-1:]
    
    stress_suprema = np.append(stress1,stress2)
    strain_suprema = np.append(strain1,strain2)
    
    
    index = 0
    for i in range(1,len(strain_suprema)):
        if strain_suprema[i-1]-strain_suprema[i] >= 0.2:
            index = i
            break
    
    indice_strain_add = strain_suprema[i-1]-strain_suprema[i]
    
    for i in range(index,len(strain_suprema)):
        strain_suprema[i] = strain_suprema[i] + indice_strain_add
        
    
    index = 0
    for i in range(len(strain_suprema)):
        if strain_suprema[i] >= 0.2:
            index = i
            break
    
    strain_le = []
    stress_le = []
    
    strain_le = np.append(strain_le,0.2)
    stress_le = np.append(stress_le,0)
    
    
    for i in range(200):
        strain_le = np.append(strain_le, i*0.01 + 0.2)
        a = slope1*i*0.01
        stress_le = np.append(stress_le, a)
    
    
    along = strain_suprema[-1]
    
    for i in range(len(stress_le)+index):
        u = indice_tencao_maior(strain_le, strain_suprema[i])
    
        if stress_suprema[i] <= stress_le[u]:
            le = stress_suprema[i]
            break
    
# =============================================================================
#     Grafico individual para cada material testado
# =============================================================================
    
    plt.plot(strain_suprema,stress_suprema, color='Blue', label=path[k], linewidth=3)
    plt.plot(strain_le, stress_le, ls='--', color='Black', label='Fitted line', linewidth=1)
    plt.xlabel('Deformação (%)')
    plt.ylabel('Tensão (MPa)')
    plt.xticks(np.arange(0, strain_suprema[-1]+2, step=1))
    plt.yticks(np.arange(0, UTS+200, step=100))
    plt.legend()
    plt.xlim([0,strain_suprema[-1]+1])
    plt.ylim([0,UTS+50])
    #plt.savefig(save[k], dpi = 300)
    plt.show()
    
    lim_esc = np.append(lim_esc, le)
    lim_res = np.append(lim_res, UTS)
    alongamento = np.append(alongamento, along)
    
    tensao.append(stress_suprema)
    deform.append(strain_suprema)

# =============================================================================
#               Chamando todas as curvas para o gráfico conjunto
# =============================================================================
#%% grafico geral

for i in range(len(path)):
    plt.plot(deform[i],tensao[i], label=path[i], linewidth=1)
plt.xlabel('Deformação (%)')
plt.ylabel('Tensão (MPa)')
plt.xticks(np.arange(0, 13, step=1))
plt.yticks(np.arange(0, UTS+200, step=100))
plt.legend()
plt.xlim([0,11])
plt.ylim([0,1500])
#plt.savefig('tracao.png', dpi = 300)
plt.show()

# =============================================================================
# chamada para exibir todas as propriedades de cada material ensaiado
# =============================================================================
#%% propriedades de cada materiais

for i in range(len(path)):
    print(path[i])
    print("Limite de escoamento: ", lim_esc[i])
    print("Limite de resistência: ", lim_res[i])
    print("Alongamento na ruptura: ", alongamento[i])










