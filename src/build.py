#!/usr/bin/env python3

'''
Módulo auxiliar de migração de modelos e realização de testes.
'''

import os
import shutil

from mapi.utils import Exit


__FLASK_APP__ = 'main.py'

__FILES__ = ['admin-credentials.txt', 'company-credentials.txt',
             'worker-credentials.txt', 'app.db']

__DIRS__ = ['migrations']


class Builder:
    '''
    Classe auxiliar para construção de migração de modelos e limpeza de dados e
    diretórios temporários.
    '''
    def __init__(self):
        self.cmds = []

    @staticmethod
    def clean():
        '''
        Remove os arquivos e diretórios gerados pela migração de modelos e
        pelos testes unitários
        '''
        for file in __FILES__:
            if os.path.isfile(file):
                os.remove(file)

        for dir_ in __DIRS__:
            if os.path.exists(dir_):
                shutil.rmtree(dir_)

    @staticmethod
    def env():
        '''
        Define as variáveis de ambiente necessárias, caso ainda não tenham sido
        definidas.
        '''
        if not os.environ.get(__FLASK_APP__):
            os.environ['FLASK_APP'] = __FLASK_APP__

    @staticmethod
    def show(msg):
        '''
        Imprime o status do comando com espaçamento na tela.
        '''
        print('\n\n\n{0}\n\n\n'.format(msg))

    def inc(self, cmd, msg):
        '''
        Incrementa um comando/instrução a ser realizado no ambiente.
        '''
        self.cmds.append({
            'cmd': cmd,
            'msg': msg
        })

    def run(self):
        '''
        Executa todas as instruções, em ordem, assim como imprime na tela a
        descrição.
        '''
        for i in self.cmds:
            self.show(i['msg'])

            err = os.system(i['cmd'])
            if err:
                return False

        return True


def main():
    '''
    Método de execução principal. Define as intruções a serem executadas e em
    qual ordem. Limpa e prepara o ambiente antes da execução. Finaliza com
    antecedência caso alguma das instruções falhe.
    '''
    b = Builder()

    b.clean()
    b.env()

    b.inc('flask db init', 'Migrating models...')
    b.inc('flask db migrate', 'Generating new revision...')
    b.inc('flask db upgrade', 'Upgrading model version...')

    if not b.run():
        Exit.with_fail('Something went wrong.')


if __name__ == '__main__':
    # Entrypoint do script.
    try:
        main()
        print('\n\n\n')

    except KeyboardInterrupt:
        Exit.SIGINT()
