"""Teste temporal de previsão de produtividade; sem uso de dados futuros."""
from pathlib import Path
import csv
import math
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT=Path(__file__).parent

def run():
    df=pd.read_csv(ROOT/'dados'/'cafe_arabica_2014_2024.csv').sort_values(['localidade','ano'])
    grp=df.groupby('localidade',sort=False)
    df['lag_1']=grp['sacas_ha'].shift(1)
    df['lag_2']=grp['sacas_ha'].shift(2)
    df=df.dropna(subset=['sacas_ha','lag_1','lag_2']).copy()
    assert (df['ano']-df.groupby('localidade')['ano'].shift(1)).dropna().eq(1).all()
    train=df[df.ano<=2021].copy();test=df[df.ano>=2022].copy()
    assert train.ano.max()<test.ano.min()
    features=['lag_1','lag_2']
    Xtrain=pd.get_dummies(train[features+['localidade']],columns=['localidade'],dtype=float)
    Xtest=pd.get_dummies(test[features+['localidade']],columns=['localidade'],dtype=float).reindex(columns=Xtrain.columns,fill_value=0)
    # StandardScaler para diferenças de escala; ajuste só no treino.
    model=make_pipeline(StandardScaler(),Ridge(alpha=10))
    model.fit(Xtrain,train['sacas_ha'])
    test['ridge_prev']=model.predict(Xtest)
    test['ano_anterior_prev']=test['lag_1']
    test['dois_anos_prev']=test['lag_2']
    cols=['localidade','ano','sacas_ha','lag_1','lag_2','ridge_prev','ano_anterior_prev','dois_anos_prev']
    test[cols].to_csv(ROOT/'dados'/'avaliacao_modelo.csv',index=False,encoding='utf-8-sig',float_format='%.4f')
    results=[]
    for label,col in [('Ridge','ridge_prev'),('Ano anterior','ano_anterior_prev'),('Dois anos antes','dois_anos_prev')]:
        results.append({'modelo':label,'n_teste':len(test),'mae_sc_ha':round(mean_absolute_error(test['sacas_ha'],test[col]),2),'rmse_sc_ha':round(math.sqrt(mean_squared_error(test['sacas_ha'],test[col])),2)})
    with (ROOT/'dados'/'metricas_modelo.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=list(results[0]));writer.writeheader();writer.writerows(results)
    print(pd.DataFrame(results).to_string(index=False))
    print('Espera Feliz:')
    print(test[test.localidade=='Espera Feliz (MG)'][['ano','sacas_ha','ridge_prev','dois_anos_prev']].round(2).to_string(index=False))
    return results

if __name__=='__main__':run()
