from logging import warning,info
from typing import Type
from numpy import nan,where
from pandas import Timedelta
from .Helper import timing

@timing
def ensure_dtypes(df:Type)-> Type:
    """
    Funcao feita para garantir que as colunas que são supostas 
    serem númericas realmente estarem em formato númerico. Tambem verifica se tem valores nulos.
    """
    df['user_phone'] = df.user_phone.str.replace('\D*','',regex = True).replace('',nan)
    df['original_user_id'] = df.original_user_id.replace('',nan)
    if df['user_phone'].isna().any():
        evid = df.loc[df['user_phone'].isna()][['user_phone','original_user_id','category','queued_date_service']].head().to_dict()
        warning('Detectei nulos na coluna userphone! Formulando tratativa')
        warning(f'Segue evidencias: {evid}')
        start_na = df['user_phone'].isna().sum()
        df['user_phone'] = df.groupby('original_user_id',group_keys = False)['user_phone'].apply(lambda x : x.bfill().ffill())
        end_na = df['user_phone'].isna().sum()
        warning(f'O numero de nulos na coluna user_phone foi de {start_na} para {end_na}')

    if df['original_user_id'].isna().any():
        evid = df.loc[df['original_user_id'].isna()][['user_phone','original_user_id','category','queued_date_service']].head().to_dict()
        warning('Detectei nulos na colunas original_user_id! Formulando tratativa!')
        warning(f'Segue evidencias: {evid}')
        start_na = df['original_user_id'].isna().sum()
        df['original_user_id'] = df.groupby('user_phone',group_keys = False)['original_user_id'].apply(lambda x : x.bfill().ffill())
        end_na = df['original_user_id'].isna().sum()
        warning(f'O numero de nulos na coluna original_user_id foi de {start_na} para {end_na}')
    #  Esperar resolucao do bug
    return df

@timing
def dtype_tracking(df:Type) -> Type:
    """
    Tratando os dtypes para que eles estejam bonitinhos,
    em relacao a memoria, utilizada evitando custos! Em layer.
    """
    dtypes= {
        'chatbot_id':str,
        'user_phone':str,
        'category':str,
        'action':str,
        'suffix':str,
        'original_user_id':str,
        'queued_date_service':'datetime64[ns]',
        'id':str,# Alterar no futuro
    }
    new_df = df.astype(dtype = dtypes)
    return new_df

@timing
def remove_test(df:Type) -> Type:
    """
    Funcao que remove users teste (testes joga fora)
    """
    testers = { 
                'Adriano': '11989999375',
                'Bruno': '13981074058', 
                'Maicon Veiga': '11969309352',
                'Jessica Varçal': '11970325152',
                'Ana Flávia Dumo': '11997842525', 
                'Sabrina Augusta': '11971565507', 
                'Salvo Menezes': '11980602111',
                'Sueli Maria': '11999171150', 
                'Leticia Dominique': '11984435186', 
                'Sueli Ferreira': '11941606552', 
                'Joana Sargo': '351910191617', 
                'Ingrid Lemos': '11987361937', 
                'Harrison Pompilha': '11982454209', 
                'Jefferson Andrade': '11986226831', 
                'Renan': '11943615412',
                'Ana Portillo': '11995879008',
                'Rafael Rodrigues': '11986705117', 
                'Andréia Lorenzoni': '11949855198',
                'Lucas Paixão': '11956075838',
                'Alexandre Pavaneli': '17997472596',
                'Murillo Nozue': '11994117676', 
                'Thiago Rasquino': '11981333149', 
                'Luis Henrique': '11986309778', 
                'Guilherme Garcia': '11984738427', 
                'Gabriel Brandao': '11940667922', 
                'Diego Coutino': '21981025516', 
                'Cintia Oliveira': '11997061023', 
                'Anderson Martins': '11974029844',
                'Alline': '11983842161', 
                'Vinicius Tirello': '34996473073', 
                'Bruna Minnicelli': '11991680459',
                'Guilherme Rapicham':'43999264449'
            }
    filt = df['user_phone'].isin(testers.values())
    if df.loc[filt].empty:
        info('Nenhum teste foi encontrado!')
        return df
    df = df.loc[~filt].reset_index(drop = True)
    return df

@timing
def flag_duplicated_tracks(df:Type) -> Type:
    """
    Cria coluna timediff e verifica se houve trackings repetidos num periodo de menos que um segundo
    Somente valído para view origin trackings
    """
    df = df.sort_values(by ='queued_date_service').reset_index(drop = True)
    df['timediff'] = (df['queued_date_service'] - df['queued_date_service'].shift())
    df['tracking'] = df['category'] + ' ' + df['suffix']

    filt = (df['timediff'] < Timedelta(seconds = 1)) & (df['suffix'].isin(['origin','view']))
    temp_df = df[['user_phone','timediff','tracking','suffix']].loc[filt]
    flagger = ((temp_df
            .groupby('user_phone')['tracking']
            .transform(lambda x: where(x.eq(x.shift())| x.eq(x.shift(-1)), True, False))))

    if flagger.fillna(False).any():
        warning('Temos trackings duplicado passar amostra para dev!')
        warning(f'Segue evidencias:{temp_df.loc[flagger.fillna(False)].head().to_dict()}')
        

@timing
def steps(s:Type) -> Type:
    """
    Formula coluna steps de acordo com a coluna suffix
    s =  suffix series
    """
    unstepped_trackings = []
    st = []
    for i in s:
        if 'onbo' in i:
            if 'start' in i:
                st.append('1-Onboarding + Retorno')
            elif 'segment' in i:
                st.append('1.1-Opcional-Onboarding escolha de bot')
            else:
                st.append(nan)
        elif 'product-availability' in i:
            if 'cpf-request' in i:
                st.append('3-Informa localizacao e cpf')
            elif 'cpf-validation' in i:
                st.append('3.1-CPF valido (V.2.0)')
            elif 'health-api-orders-validation' in i:
                st.append('3.2-Consulta orders (V.2.1.1)')
            elif 'api-residential-customer-contracts-open-request-validation' in i:
                st.append('3.3-Consulta customer contracts (V.2.1.2)')
            elif 'postalcode-request' in i:
                st.append('3.4-Obtencao de CEP')
            elif 'postalcode-validation' in i:
                st.append('3.5-CEP valido (V.2.2)')
            elif 'postalcode-validation-true' in i:
                st.append('3.6-Pegando complemento')
            elif 'health-api-address-validation' in i:
                st.append('3.7-Endereco sendo validado (V.2.3)')
            elif 'empty-public-space-validation' in i:
                st.append('3.8-Validacao de logradouro (V.2.4)')
            elif 'empty-neighborhood-validation' in i:
                st.append('3.9-Bairro sendo validado (V.2.3)')
            elif 'address-confirmation' in i:
                st.append('3.9.1-Endereco resumido')
            elif 'health-api-residential-customer-contracts-validation' in i:
                st.append('3.9.2-Consulta de CPF na api de base (V.2.9)')
            elif 'client-validation' in i:
                st.append('3.9.3-Localizado na api de base validacao (V.2.10)')
            elif 'product-availability-validation' in i:
                st.append('3.9.4-Produto e disponibilizado na regiao (V.2.11)')
            elif 'health-api-plan-availability-validation' in i:
                st.append('3.9.5-Consulta na api de catalogos(V.2.13)')
            elif 'plans-available-catalog-validation' in i:
                st.append('3.9.6-Plano disponivel no catalogo (V.2.14)')
            else:
                st.append(nan)
        elif 'plan-selection' in i:
            st.append('4-Escolhe plano (Todos produtos)')
        elif 'registration' in i:
            if 'full-name-request' in i:
                st.append('5-Realiza cadastro')
            elif 'name-validation' in i:
                st.append('5.1-Consulta nome valido (V.4.0)')
            elif 'email-request' in i:
                st.append('5.2-Requisicao de email')
            elif 'e-mail-validation' in i:
                st.append('5.3-Consulta email valido (V.4.1)')
            elif 'birth-date-request' in i:
                st.append('5.4-Idade do usuario')
            elif 'birth-date-validation' in i:
                st.append('5.5-Idade do usuario validacao (V.4.2)')
            elif 'birth-date-out-of-range-validation' in i:
                st.append('5.6-Idade do usuario elegibilidade (V.4.3)')
            elif 'identity-number-request' in i:
                st.append('5.7-Pedido de RG')
            elif 'identity-number-validation' in i:
                st.append('5.8-Pedido de RG (V.4.4)')
            elif 'mother-name-request' in i:
                st.append('5.9-Pedido de nome da mae')
            elif 'mother-name-validation' in i:
                st.append('5.9.1-Pedido de nome da mae validation (V.4.5)')
            elif 'additional-phone-number-confirmation' in i:
                st.append('5.9.2-Numero adicional')
            elif 'register-data-confirmation' in i:
                st.append('5.9.3-Confirmacao de data')
            elif 'address-complement-insert-confirmation' in i:
                st.append('6-Informa Complemento')
            elif 'address-complement-confirmation' in i:
                st.append('6.1-Complemento confirmado')
            else:
                st.append(nan)
        elif 'payment' in i:
            if 'invoice-sending-confirmation' in i:
                st.append('7-Metodo de pagamento')
            elif 'invoice-due-date-options' in i:
                st.append('7.1-Escolhe dia de vencimento')
            elif 'payment-method-confirmation-options' in i:
                st.append('7.2-Escolhe forma de pagamento')
            elif 'register-data-confirmation' in i:
                st.append('7.3-Confirma dados')
            else:
                st.append(nan)
        elif 'schedule start' in i:
            st.append('8-Agendamento de instalacao')
        elif 'checkout' in i:
            if 'order-details-confirmation' in i:
                st.append('9-Realiza pedido')
            elif 'order-validation' in i:
                st.append('9.1-Cascata de api (V.F.0)')
            elif 'order-placed' in i:
                st.append('9.2-Finalizado')
            else:
                st.append(nan)
        elif 'error' in i:
            st.append('Horizontal-erros-gerais')
        elif 'human-handoff' in i:
            st.append('Horizontal-Transbordo')
        elif 'decision-tree' in i:
            st.append('Horizontal-Cascatas')
        elif 'feedback' in i:
            st.append('Horizantal-Feedback')
        else:
            unstepped_trackings.append(i)
            st.append(nan)
    if any([i is not nan for i in unstepped_trackings]):
        warning('Voce tem trackings sem steps! Para ver quais são verificar lista unstepped_trackings :)')
    return st

@timing
def errors(s:Type) -> Type:
    """
    Formula coluna de erros
    """
    e = []
    for i in s:
        if 'error' in i:
            if 'unexpected-video' in i:
                e.append('Erro video')
            elif 'unexpected-image' in i:
                e.append('Erro imagem')
            elif 'unexpected-audio' in i:
                e.append('Erro audio')
            elif 'unexpected-file' in i:
                e.append('Erro arquivo')
            elif 'unexpected-cpf' in i:
                e.append('Erro persistente CPF')
            elif 'generic' in i:
                e.append('Erro generico')
            elif 'api' in i:
                e.append('Erro generico API')
            elif 'last-state-unidentified' in i:
                e.append('Erro estado inexistente')
            elif 'bob' in i:
                e.append('Erro Bob')
            else:
                e.append(nan)
        else:
            e.append(nan)
    if any([i is not nan for i in e]):
        info('Aviso: Tivemos erros no bot :(')
    return e

# Migrar para outro lambda
def get_rid_of_undefined(df:Type) -> Type:
    """
    Ver com vini, capacidade extracao
    """
    pass

