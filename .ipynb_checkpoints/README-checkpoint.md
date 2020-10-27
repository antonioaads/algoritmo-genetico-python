# Algorítmo Genético em Python
Algorítimo Genético desenvolvido durante a disciplina de IA do CEFET-MG, curso de Engenharia da Computação.

## Premissas de desenvolvimento

Durante o desenvolvimento deste algorítimo, o foco principal foi manter ele o mais genérico possível, para poder aplicar a diversas aplicações sem grandes alterações. Para isso, faz-se necessário a passagem de alguns parâmetros para a instância do GA, que serão definidas abaixo, na ordem em que devem ser passados:

limiteInferior, limiteSuperior, tamanhoPopulacao, funcaoObjetivo, funcaoNorm, funcaoAcm, novaPopulacao, taxaMutacao, iteracoes
- limiteInferior: Trata-se de um array que deve possuir os limites inferiores dos cromossomos dos indivíduos que serão criados
- limiteSuperior: Trata-se de um array que deve possuir os limites superiores dos cromossomos dos indivíduos que serão criados (necessariamente do mesmo tamanho que o limiteInferior)
- tamanhoPopulacao: Trata-se do tamanho da população que será gerada e manipulada
- funcaoObjetivo: Trata-se de uma função que deverá se espelhar na função objetivo. Recebe como parâmetro um array correspondente aos cromossomos do indivíduo, que podem ser tratados internamente a função da maneira que for mais apropriada ao problema
