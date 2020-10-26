import random
import math
import copy

class Individuo:
    def __init__(self, crom, f = None, fNorm = None, fAcm = None):
        self.crom = crom
        self.f = f
        self.fNorm = fNorm
        self.fAcm = fAcm
        
    def __eq__(self,outro_individuo:"Individuo"):
        if (self.f == outro_individuo.f):
            return True
        else:
            return False


    # Retorna verdadeiro se o objeto corrrente self é menor do que o objeto passado como parametro
    def __lt__(self,outro_individuo:"Individuo"):
        if (self.f < outro_individuo.f):
            return True
        else:
            return False


    def __str__(self):
        return f"(Cromossomos:{self.crom} f: {self.f} fNorm: {self.fNorm} fAcm: {self.fAcm})"
        
class Ga:    
    def __init__(self, limiteInferior, limiteSuperior, tamanhoPopulacao, funcaoObjetivo, funcaoNormalizacao, funcaoAcm, novaPopulacao, taxaMutacao, iteracoes, logKey = None):
        # parâmetros do GA
        self.limiteInferior = limiteInferior
        self.limiteSuperior = limiteSuperior
        self.tamanhoPopulacao = tamanhoPopulacao
        self.funcaoObjetivo = funcaoObjetivo
        self.funcaoNormalizacao = funcaoNormalizacao
        self.funcaoAcm = funcaoAcm
        self.taxaMutacao = taxaMutacao
        self.novaPopulacao = novaPopulacao
        self.iteracoes = iteracoes
        self.logKey = logKey
        
        # parâmetros gerados
        self.numeroCromossomos = len(limiteInferior)
    
    def log(self, str):
        if self.logKey is True: print(str)
            
    def imprimirPopulacao(self, populacao):
        if self.logKey is True:
            for ind in populacao:
                print(str(ind))
            
    def gerarPopulacaoInicial(self):
        populacao = []
        for ind in range(self.tamanhoPopulacao):
            novoInd = []
            for index, crom in enumerate(self.limiteInferior):
                novoInd.append(random.uniform(self.limiteInferior[index],self.limiteSuperior[index]))
            
            populacao.append(Individuo(novoInd))
        
        return populacao
    
    # Calcula função objetivo, função normalizada
    def calculaFeFNorm(self, populacao):
        somaFNorm = 0;
        for index, ind in enumerate(populacao):
            f = self.funcaoObjetivo(ind.crom)
            fNorm = self.funcaoNormalizacao(f)
            somaFNorm = somaFNorm + fNorm 
            populacao[index].f = f 
            populacao[index].fNorm = fNorm
            
        return populacao, somaFNorm
    
    def calculaFNorm(self, populacao):
        somaFNorm = 0;
        for index, ind in enumerate(populacao):
            fNorm = self.funcaoNormalizacao(ind.f)
            somaFNorm = somaFNorm + fNorm 
            populacao[index].fNorm = fNorm
            
        return populacao, somaFNorm
        
    def calculaFAcm(self, populacao, somaFNorm):
        somaAcm = 0
        for index, ind in enumerate(populacao):
            fAcm = self.funcaoAcm(ind.fNorm, somaFNorm)
            somaAcm = somaAcm + fAcm
            populacao[index].fAcm = somaAcm
        
        return populacao
            
    
    def selecionarIndividuo(self,populacao, fAcmRoleta): 
        for ind in populacao:
            limSuperiorFAcm = ind.fAcm
            
            if(fAcmRoleta < limSuperiorFAcm):
                return ind
            
        print("Algo deu errado na função selecionar Indivíduo")
    
    def crossover(self, parent1, parent2):
        # Devido ao problema que queremos tratar, iremos considerar o crossover no ponto
        # central, mas pode-se alterar esta função para implementar de outras formas
        pontoCentral = math.floor(len(self.limiteInferior)/2)
        
        children1 = []
        children2 = []
        
        for i in range(self.numeroCromossomos):
            if(i < pontoCentral):
                children1.append(parent1.crom[i])
                children2.append(parent2.crom[i])
            else:
                children1.append(parent2.crom[i])
                children2.append(parent1.crom[i])

        return [Individuo(children1), Individuo(children2)]
    
    def mutacao(self, ind):
        for index in range(self.numeroCromossomos):
            if random.random() < self.taxaMutacao:
                novoCrom = random.uniform(self.limiteInferior[index],self.limiteSuperior[index])
                ind.crom[index] = novoCrom
                
        return ind
        
    def gerarPopulacaoIntermediaria(self, populacao):
        populacaoIntermediaria = []
        for i in range(math.floor(self.tamanhoPopulacao/2)):
            parent1 = self.selecionarIndividuo(populacao, random.random())
            parent2 = self.selecionarIndividuo(populacao, random.random())
            childrens = self.crossover(parent1, parent2)
            children1 = self.mutacao(childrens[0])
            children2 = self.mutacao(childrens[1])
            populacaoIntermediaria.append(children1)
            populacaoIntermediaria.append(children2)
         
        populacaoIntermediaria, soma = self.calculaFeFNorm(populacaoIntermediaria)
        populacaoIntermediaria = self.calculaFAcm(populacaoIntermediaria, soma)
        return populacaoIntermediaria
    
    def gerarNovaPopulacao(self, populacao, populacaoIntermediaria):
        populacao = copy.deepcopy(populacao)
        populacaoIntermediaria = copy.deepcopy(populacaoIntermediaria)
        
        novaPopulacao = self.novaPopulacao(populacao, populacaoIntermediaria, self.tamanhoPopulacao)
        
        for index, ind in enumerate(novaPopulacao):
            novaPopulacao[index].fAcm = None
            novaPopulacao[index].fNorm = None
            
        return novaPopulacao
    
    def run(self):
        self.log("Gerando populacao inicial:")
        populacao = self.gerarPopulacaoInicial()
        populacao, soma = self.calculaFeFNorm(populacao)
        populacao = self.calculaFAcm(populacao, soma)
        self.imprimirPopulacao(populacao)
        
        for i in range(self.iteracoes):
            self.log("Iteracao: " + str(i))
            populacaoIntermediaria = self.gerarPopulacaoIntermediaria(populacao)
            populacao = self.gerarNovaPopulacao(populacao, populacaoIntermediaria)
            populacao, soma = self.calculaFNorm(populacao)
            populacao = self.calculaFAcm(populacao, soma)

        self.imprimirPopulacao(populacao)
        return populacao
        