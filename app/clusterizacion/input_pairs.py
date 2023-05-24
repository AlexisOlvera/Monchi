import os, glob
import pickle

par_ao = []
aspectos_todos = []
opiniones_todas = []
sentimientos_todos = []

for filename in glob.glob('et_tok_el-pescadito.txt'):
   with open(filename, 'r') as fp:
        lines = fp.readlines()
        lista_aspectos = {}
        for rev in lines:
            texto, back = rev.split("#### #### ####")
            tripletes = eval(back)
            tokens = texto.split()
            for aspectos, opiniones, sentimiento in tripletes:
                aspecto = ' '.join([tokens[i] for i in aspectos])
                opinion = ' '.join([tokens[i] for i in opiniones])

                aspectos_todos.append(aspecto)
                opiniones_todas.append(opinion)
                sentimientos_todos.append(sentimiento)

                if aspecto in lista_aspectos:
                    if opinion in lista_aspectos[aspecto]:
                        lista_aspectos[aspecto][opinion]["count"]+=1
                    else:
                        lista_aspectos[aspecto][opinion]={
                        "sentimiento": sentimiento,
                        "count": 1
                        }
                else:
                    lista_aspectos[aspecto]={
                        opinion:{
                            "sentimiento": sentimiento,
                            "count": 1
                        }
                    }

        newfile = open('cnt2_'+filename, '+w')
        
        par_ao = list((zip(aspectos_todos, opiniones_todas)))
        print(par_ao)

        for aspecto, opiniones in lista_aspectos.items():
            for opinion, values in opiniones.items():
                    newfile.write("{0}-{1}-{2}\n".format(aspecto, opinion, values['count']))
        newfile.close()

        # Pickle: Serializar lista de tuplas para obtener entrada en "get_triplets.py"
        with open('pairs.pkl', 'wb') as f:
            pickle.dump(par_ao, f) 
        f.close

